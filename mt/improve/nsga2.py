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
from mt.genome.ops import mutate, crossover
from mt.gauntlet.runner import GauntletReport


def objectives(report: GauntletReport) -> np.ndarray:
    """The maximize-all objective vector (missing objectives get conservative fills)."""
    f = report.fitness
    ds = f.get("deflated_sharpe")
    if ds is None:
        ds = f.get("net_sharpe")
    ds = float(ds) if ds is not None else -10.0
    omp = f.get("one_minus_pbo"); omp = float(omp) if omp is not None else 0.0
    cap = f.get("capacity_sharpe_2x"); cap = float(cap) if cap is not None else -10.0
    nac = f.get("neg_archive_corr"); nac = float(nac) if nac is not None else 0.0
    neg_cx = float(f.get("neg_complexity", -6))
    return np.array([ds, omp, cap, neg_cx, nac], dtype=float)


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


def select_parents(genomes: List[Genome], reports: List[GauntletReport], k: int) -> List[Genome]:
    """Top-k by (non-dominated rank, then crowding distance)."""
    if not genomes:
        return []
    objs = [objectives(r) for r in reports]
    fronts = fast_non_dominated_sort(objs)
    ordered: List[int] = []
    for front in fronts:
        cd = crowding_distance(front, objs)
        ordered.extend(sorted(front, key=lambda i: -cd[i]))
    return [genomes[i] for i in ordered[:max(1, k)]]


def breed(parents: List[Genome], n_children: int, rng: np.random.Generator) -> List[Genome]:
    """Offspring via crossover (+ mutation) or mutation, staying registry-valid."""
    if not parents:
        return []
    children: List[Genome] = []
    for _ in range(n_children):
        if len(parents) >= 2 and rng.random() < 0.6:
            i, j = rng.integers(len(parents)), rng.integers(len(parents))
            child = crossover(parents[int(i)], parents[int(j)], rng)
            if rng.random() < 0.5:
                child = mutate(child, rng)
        else:
            child = mutate(parents[int(rng.integers(len(parents)))], rng)
        if child.typecheck()[0]:
            children.append(child)
    return children
