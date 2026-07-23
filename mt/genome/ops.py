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


def mutate(g: Genome, rng: np.random.Generator) -> Genome:
    """Perturb exactly one node/arg within registry bounds (docs/03 §2)."""
    child = copy.deepcopy(g)
    choices = ["arg", "swap_feature", "add_feature", "remove_feature", "signal_dir", "sizing_arg", "risk_arg"]
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
        new_op = pool[int(rng.integers(len(pool)))]
        f.op = new_op.name
        f.args = new_op.sample_args(rng)
    elif move == "add_feature":
        pool = _feature_ops_for(child.meta.market)
        new_op = pool[int(rng.integers(len(pool)))]
        child.features.append(FeatureNode(_new_feature_id(child.features), new_op.name, new_op.sample_args(rng)))
    elif move == "remove_feature":
        del child.features[int(rng.integers(len(child.features)))]
    elif move == "signal_dir":
        spec = REGISTRY[child.signal.op]
        if "direction" in spec.args:
            child.signal.args["direction"] = spec.args["direction"].sample(rng)
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
