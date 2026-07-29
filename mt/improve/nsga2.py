"""mt.improve.nsga2 — multi-objective evolution (Engine A, docs/03 §2 / docs/06).

NSGA-II on the gauntlet's Pareto front (return, robustness, capacity, simplicity,
orthogonality) — never a single scalar, so the search cannot Goodhart onto one over-tuned
peak. Parents are selected by non-dominated rank + crowding distance; offspring are bred
with the genome mutate/crossover operators (which stay inside the registry's bounds).
"""
from __future__ import annotations

from typing import List, Tuple

import numpy as np

from mt.genome.schema import Genome
from mt.genome.ops import mutate, novelty_mutate, crossover, distance
from mt.gauntlet.runner import GauntletReport


def _num(v, fill: float) -> float:
    """Coerce to a FINITE float — None *and* NaN/inf map to the conservative fill, so a
    degenerate objective can never poison the domination test (np.all(a>=b) is all-False
    against NaN, which would silently scramble the Pareto fronts)."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return fill
    return x if np.isfinite(x) else fill


def objectives(report: GauntletReport) -> np.ndarray:
    """The maximize-all objective vector (missing/NaN objectives get conservative fills).

    `edge_t` is deliberately included and deliberately FIRST-CLASS: it is the only component that
    does not move when the trial ledger grows. Ranking purely on N-deflated quantities made a
    parent and its child incomparable across generations, since both were being shifted by a
    counter that has nothing to do with either strategy (docs/15 §4).

    ONLY `k_ratio` was added from the equity-shape family, and that restraint is deliberate.
    Pareto dominance degrades badly as objectives multiply — beyond roughly five or six, almost
    every solution is non-dominated, every front collapses into one, and selection falls back to
    crowding distance alone, which is diversity pressure with no quality pressure behind it. This
    vector is already at seven. `persistence` and `recovery_factor` are therefore recorded, gated
    and reported, but they do NOT get their own axis: k_ratio is the one that carries information
    the others miss (a t-statistic of the equity trend, so it prices choppiness), while the other
    two are largely monotone in drawdown and return, which are represented already."""
    f = report.fitness
    ds = f.get("deflated_sharpe")
    if ds is None:
        ds = f.get("net_sharpe")
    ds = _num(ds, -10.0)
    edge = _num(f.get("edge_t"), -10.0)                 # N-INDEPENDENT strength
    omp = _num(f.get("one_minus_pbo"), 0.0)
    cap = _num(f.get("capacity_sharpe_2x"), -10.0)
    nac = _num(f.get("neg_archive_corr"), 0.0)
    neg_cx = _num(f.get("neg_complexity", -6), -6.0)
    oos = _num(f.get("cpcv_oos_sharpe"), 0.0)          # reward configs that survive CPCV OOS (B7)
    kr = _num(f.get("k_ratio"), -5.0)                  # SHAPE: straightness of the equity climb
    return np.array([ds, edge, omp, cap, neg_cx, nac, oos, kr], dtype=float)


def _dominates(a: np.ndarray, b: np.ndarray) -> bool:
    return bool(np.all(a >= b) and np.any(a > b))


def fast_non_dominated_sort(objs: List[np.ndarray]) -> List[List[int]]:
    n = len(objs)
    S = [[] for _ in range(n)]
    nd = [0] * n
    fronts: List[List[int]] = [[]]
    for p in range(n):
        for q in range(n):
            if p == q:
                continue
            if _dominates(objs[p], objs[q]):
                S[p].append(q)
            elif _dominates(objs[q], objs[p]):
                nd[p] += 1
        if nd[p] == 0:
            fronts[0].append(p)
    i = 0
    while fronts[i]:
        nxt: List[int] = []
        for p in fronts[i]:
            for q in S[p]:
                nd[q] -= 1
                if nd[q] == 0:
                    nxt.append(q)
        i += 1
        fronts.append(nxt)
    return fronts[:-1]


def crowding_distance(front: List[int], objs: List[np.ndarray]) -> dict:
    if not front:
        return {}
    m = len(objs[0])
    dist = {i: 0.0 for i in front}
    for k in range(m):
        order = sorted(front, key=lambda i: objs[i][k])
        dist[order[0]] = dist[order[-1]] = float("inf")
        lo, hi = objs[order[0]][k], objs[order[-1]][k]
        span = (hi - lo) or 1.0
        for j in range(1, len(order) - 1):
            dist[order[j]] += (objs[order[j + 1]][k] - objs[order[j - 1]][k]) / span
    return dist


def select_parent_indices(reports: List[GauntletReport], k: int) -> List[int]:
    """Indices of the top-k reports by (non-dominated rank, then crowding distance).

    Returning INDICES (not genomes) is what lets the caller keep each surviving genome paired
    with its OWN report — pairing the rank-ordered genomes with the pool-ordered reports would
    silently mismatch them and corrupt the next generation's Pareto ranking of the elites."""
    if not reports:
        return []
    objs = [objectives(r) for r in reports]
    fronts = fast_non_dominated_sort(objs)
    ordered: List[int] = []
    for front in fronts:
        cd = crowding_distance(front, objs)
        ordered.extend(sorted(front, key=lambda i: -cd[i]))
    return ordered[:max(1, k)]


def select_parents(genomes: List[Genome], reports: List[GauntletReport], k: int) -> List[Genome]:
    """Top-k genomes by (non-dominated rank, then crowding distance)."""
    if not genomes:
        return []
    return [genomes[i] for i in select_parent_indices(reports, k)]


def breed(parents: List[Genome], n_children: int, rng: np.random.Generator,
          op_weights=None, avoid: List[Genome] = None) -> List[Genome]:
    """Offspring via crossover (+ mutation) or mutation, staying registry-valid.

    `op_weights` biases new primitives toward measured contribution; `avoid` (the current archive
    elites) turns the mutation step into a novelty-seeking one, so a converged parent pool stops
    emitting parameter jitter on the same idea. Each child is also compared against its siblings,
    so one call cannot return a batch of clones."""
    if not parents:
        return []
    children: List[Genome] = []
    avoid = list(avoid or [])
    for _ in range(n_children):
        if len(parents) >= 2 and rng.random() < 0.6:
            i, j = rng.integers(len(parents)), rng.integers(len(parents))
            child = crossover(parents[int(i)], parents[int(j)], rng)
            if rng.random() < 0.5:
                child = novelty_mutate(child, rng, avoid + children, op_weights=op_weights)
        else:
            parent = parents[int(rng.integers(len(parents)))]
            child = novelty_mutate(parent, rng, avoid + children, op_weights=op_weights)
        if child.typecheck()[0]:
            children.append(child)
    return children


def diverse_subset(genomes: List[Genome], k: int) -> List[int]:
    """Indices of a max-min structurally diverse subset (greedy farthest-point), order-preserving
    on the first pick. Used for warm-start: taking the top-k by score alone reseeded each marathon
    with near-identical elites, so 'compounding' compounded one idea."""
    if not genomes:
        return []
    chosen = [0]
    while len(chosen) < min(k, len(genomes)):
        best_i, best_d = None, -1.0
        for i in range(len(genomes)):
            if i in chosen:
                continue
            d = min(distance(genomes[i], genomes[c]) for c in chosen)
            if d > best_d:
                best_i, best_d = i, d
        if best_i is None:
            break
        chosen.append(best_i)
    return chosen
