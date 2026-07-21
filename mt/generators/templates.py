"""mt.generators.templates — Engine D: parameterized archetypes + fully-random genomes.

Cheap, dumb, and essential: it seeds behavioral diversity, keeps the population from
inbreeding, and — via the random stream — discovers structure no archetype encodes. Every
genome it emits is structurally valid by construction (it only draws from the registry).
"""
from __future__ import annotations

from typing import List

import numpy as np

from mt.config import MARKETS
from mt.genome.registry import REGISTRY, ops_for_stage
from mt.genome.schema import Genome, Meta, FeatureNode, SignalSpec, SizingSpec, RiskSpec


class TemplateSampler:
    def __init__(self, seed: int = 4242):
        self.rng = np.random.default_rng(seed)

    def _meta(self, market: str) -> Meta:
        m = MARKETS[market]
        return Meta(market=market, htf=m.htf, mtf=m.mtf, ltf=m.ltf,
                    rebalance=m.htf, cost_profile=f"{market}_default")

    def _feature_ops(self, market: str) -> List[str]:
        """Feature ops usable on this market (drop funding on non-funding markets)."""
        has_funding = MARKETS[market].has_funding
        ops = [op.name for op in ops_for_stage("feature")]
        if not has_funding:
            ops = [o for o in ops if "funding_rate" not in REGISTRY[o].needs]
        return ops

    # ─── named archetypes ────────────────────────────────────────────────
    def _archetype(self, market: str, kind: str) -> Genome:
        rng = self.rng
        h = int(rng.integers(4, 13))
        if kind == "trend":
            feats = [FeatureNode("f1", "momentum", {"lookback": int(rng.integers(40, 160)), "skip": 1}),
                     FeatureNode("f2", "breakout", {"window": int(rng.integers(30, 90))})]
            sig = SignalSpec("weighted_blend", {"direction": "neutral"})
        elif kind == "reversion":
            feats = [FeatureNode("f1", "reversion", {"lookback": int(rng.integers(1, 6))}),
                     FeatureNode("f2", "rsi", {"window": int(rng.integers(7, 21))})]
            sig = SignalSpec("weighted_blend", {"direction": "neutral"}); h = int(rng.integers(1, 4))
        elif kind == "lowvol":
            feats = [FeatureNode("f1", "atr_pct", {}),
                     FeatureNode("f2", "realized_vol", {"window": int(rng.integers(20, 80))})]
            sig = SignalSpec("weighted_blend", {"direction": "neutral"})
        elif kind == "carry" and MARKETS[market].has_funding:
            feats = [FeatureNode("f1", "funding_z", {"window": int(rng.integers(48, 120))})]
            sig = SignalSpec("gated_and", {"threshold": float(round(rng.uniform(0.3, 1.0), 2)),
                                           "direction": "long_bias"})
        else:  # breakout-momentum gate
            feats = [FeatureNode("f1", "breakout", {"window": int(rng.integers(30, 90))}),
                     FeatureNode("f2", "momentum", {"lookback": int(rng.integers(40, 120)), "skip": 1})]
            sig = SignalSpec("gated_and", {"threshold": float(round(rng.uniform(0.3, 1.0), 2)),
                                           "direction": "long_bias"})
        sizing = SizingSpec("rank_bucket", {"top_frac": float(round(rng.uniform(0.1, 0.25), 2)),
                                            "gross": 1.0, "per_name_cap": 0.15})
        risk = RiskSpec("horizon_hold", {"horizon": h, "cost_stress": 1.0})
        return Genome(self._meta(market), feats, sig, sizing, risk, generator=f"template:{kind}")

    # ─── fully-random genome ─────────────────────────────────────────────
    def _random(self, market: str) -> Genome:
        rng = self.rng
        ops = self._feature_ops(market)
        n = int(rng.integers(1, 4))
        feats = []
        for i in range(n):
            op = ops[int(rng.integers(len(ops)))]
            feats.append(FeatureNode(f"f{i+1}", op, REGISTRY[op].sample_args(rng)))
        sig_op = ops_for_stage("signal")[int(rng.integers(len(ops_for_stage("signal"))))]
        sig = SignalSpec(sig_op.name, sig_op.sample_args(rng))
        siz_op = ops_for_stage("sizing")[int(rng.integers(len(ops_for_stage("sizing"))))]
        siz = SizingSpec(siz_op.name, siz_op.sample_args(rng))
        risk_op = REGISTRY["horizon_hold"]
        risk = RiskSpec("horizon_hold", risk_op.sample_args(rng))
        return Genome(self._meta(market), feats, sig, siz, risk, generator="random")

    # ─── batch API ───────────────────────────────────────────────────────
    def sample(self, market: str, n_random: int = 6) -> List[Genome]:
        kinds = ["trend", "reversion", "lowvol", "carry", "breakout"]
        genomes = [self._archetype(market, k) for k in kinds]
        genomes += [self._random(market) for _ in range(n_random)]
        return genomes
