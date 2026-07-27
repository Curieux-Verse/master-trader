"""mt.genome.ops — the search operators over genomes (mutate / crossover / distance).

Thin but real: enough for the template+random+mutation generator in the thin slice, and
the natural home for the NSGA-II / MAP-Elites variation operators in Phase 3. Every
operator produces a *structurally valid* genome by staying inside the registry's bounds.
"""
from __future__ import annotations

import copy
from typing import List

import numpy as np

from mt.config import available_feeds
from mt.genome.registry import REGISTRY, ops_for_stage, computable_feature_ops
from mt.genome.schema import Genome, FeatureNode, SignalSpec, SizingSpec, RiskSpec


def _new_feature_id(existing: List[FeatureNode]) -> str:
    n = len(existing)
    ids = {f.id for f in existing}
    while f"f{n}" in ids:
        n += 1
    return f"f{n}"


def _feature_ops_for(market: str) -> List:
    """Computable feature ops whose data this market can satisfy — keeps evo mutation from
    introducing inert cross-market features (e.g. taker-buy order flow on OANDA FX)."""
    feeds = available_feeds(market)
    ops = [op for op in computable_feature_ops() if all(d in feeds for d in op.data_requires)]
    return ops or computable_feature_ops()          # never empty (fallback to full set)


def _pick_op(pool: List, rng: np.random.Generator, op_weights=None):
    """Choose a feature op — biased by MEASURED contribution when evidence exists.

    `op_weights` comes from the attribution table (mean leave-one-out ΔDSR-z per primitive). Until
    now every generator sampled the ~74 primitives uniformly no matter what the system had learned:
    attribution measured, for instance, `vwap_distance` at +1.59 mean ΔDSR-z over 30 observations,
    wrote it to a table, rendered it in a markdown report, and then kept sampling it exactly as
    often as an inert primitive. This is the wire that closes that loop.

    Weights are floored toward uniform upstream, so a primitive can never be starved out entirely
    — the search stays able to rediscover something the early evidence dismissed."""
    if not op_weights:
        return pool[int(rng.integers(len(pool)))]
    w = np.array([float(op_weights.get(op.name, 0.0)) for op in pool], dtype=float)
    if not np.isfinite(w).all() or w.sum() <= 0:
        return pool[int(rng.integers(len(pool)))]
    return pool[int(rng.choice(len(pool), p=w / w.sum()))]


def mutate(g: Genome, rng: np.random.Generator, op_weights=None) -> Genome:
    """Perturb exactly one node/arg within registry bounds (docs/03 §2)."""
    child = copy.deepcopy(g)
    choices = ["arg", "swap_feature", "add_feature", "remove_feature", "signal_dir",
               "signal_regime", "sizing_arg", "risk_arg"]
    if len(child.features) <= 1:
        choices = [c for c in choices if c != "remove_feature"]
    move = choices[int(rng.integers(len(choices)))]

    if move == "arg" and child.features:
        f = child.features[int(rng.integers(len(child.features)))]
        spec = REGISTRY[f.op]
        if spec.args:
            k = list(spec.args)[int(rng.integers(len(spec.args)))]
            f.args[k] = spec.args[k].mutate(f.args.get(k, spec.args[k].default), rng)
    elif move == "swap_feature" and child.features:
        pool = _feature_ops_for(child.meta.market)
        f = child.features[int(rng.integers(len(child.features)))]
        new_op = _pick_op(pool, rng, op_weights)
        f.op = new_op.name
        f.args = new_op.sample_args(rng)
    elif move == "add_feature":
        pool = _feature_ops_for(child.meta.market)
        new_op = _pick_op(pool, rng, op_weights)
        child.features.append(FeatureNode(_new_feature_id(child.features), new_op.name, new_op.sample_args(rng)))
    elif move == "remove_feature":
        del child.features[int(rng.integers(len(child.features)))]
    elif move == "signal_dir":
        spec = REGISTRY[child.signal.op]
        if "direction" in spec.args:
            child.signal.args["direction"] = spec.args["direction"].sample(rng)
    elif move == "signal_regime":                        # explore regime conditioning (docs/06)
        spec = REGISTRY[child.signal.op]
        if "regime" in spec.args:
            child.signal.args["regime"] = spec.args["regime"].sample(rng)
    elif move == "sizing_arg":
        spec = REGISTRY[child.sizing.op]
        if spec.args:
            k = list(spec.args)[int(rng.integers(len(spec.args)))]
            child.sizing.args[k] = spec.args[k].mutate(child.sizing.args.get(k, spec.args[k].default), rng)
    elif move == "risk_arg":
        spec = REGISTRY[child.risk.op]
        if spec.args:
            k = list(spec.args)[int(rng.integers(len(spec.args)))]
            child.risk.args[k] = spec.args[k].mutate(child.risk.args.get(k, spec.args[k].default), rng)

    child.generator = "evo_mutate"
    child.parents = [g.genome_id]
    child.generation = g.generation + 1
    return child


CONVERGED_DISTANCE = 0.35       # below this, the parent is already inside a crowded region


def novelty_mutate(g: Genome, rng: np.random.Generator, avoid: List[Genome],
                   op_weights=None, tries: int = 6) -> Genome:
    """Mutate, preferring the child that is STRUCTURALLY furthest from what we already hold —
    but ONLY when the parent is in a crowded region.

    A plain single-node perturbation is a local move, so a converged population keeps producing
    near-copies of its own elites (production's top-20 were parameter jitter on one
    obv×vwap_distance idea). Sampling several candidate children and keeping the most distant one
    is the cheap structural analogue of AlphaAgent's AST-similarity regularizer, and it costs no
    extra backtest since only the winner is evaluated.

    Applying it UNCONDITIONALLY is a mistake, though: novelty selection ignores fitness, so in an
    already-diverse region it just throws away good local moves. Since the archive now supplies
    standing diversity pressure (behavioural niching plus the similarity discount), the operator
    only needs to intervene where convergence actually is — when the parent sits within
    CONVERGED_DISTANCE of something already held. Elsewhere a plain mutation is the better move."""
    if not avoid:
        return mutate(g, rng, op_weights=op_weights)
    crowding = min((distance(g, o) for o in avoid), default=1.0)
    if crowding > CONVERGED_DISTANCE:
        return mutate(g, rng, op_weights=op_weights)
    best, best_d = None, -1.0
    for _ in range(max(1, tries)):
        child = mutate(g, rng, op_weights=op_weights)
        if not child.typecheck()[0]:
            continue
        d = min((distance(child, o) for o in avoid), default=1.0)
        if d > best_d:
            best, best_d = child, d
    return best if best is not None else mutate(g, rng, op_weights=op_weights)


def crossover(g1: Genome, g2: Genome, rng: np.random.Generator) -> Genome:
    """Swap typed subtrees: g1's features married to g2's signal/sizing/risk (docs/03 §2)."""
    child = copy.deepcopy(g1)
    child.signal = copy.deepcopy(g2.signal)
    if rng.random() < 0.5:
        child.sizing = copy.deepcopy(g2.sizing)
    if rng.random() < 0.5:
        child.risk = copy.deepcopy(g2.risk)
    child.generator = "evo_crossover"
    child.parents = [g1.genome_id, g2.genome_id]
    child.generation = max(g1.generation, g2.generation) + 1
    return child


def distance(g1: Genome, g2: Genome) -> float:
    """Structural distance in [0,1]: 1 - Jaccard(feature ops), blended with stage diffs."""
    ops1 = {f.op for f in g1.features}
    ops2 = {f.op for f in g2.features}
    union = ops1 | ops2
    jac = 1.0 - (len(ops1 & ops2) / len(union)) if union else 0.0
    stage_diff = sum([
        g1.signal.op != g2.signal.op,
        g1.sizing.op != g2.sizing.op,
        g1.risk.op != g2.risk.op,
    ]) / 3.0
    return 0.6 * jac + 0.4 * stage_diff
