"""mt.generators.templates — Engine D: parameterized archetypes + fully-random genomes.

Cheap, dumb, and essential: it seeds behavioral diversity, keeps the population from
inbreeding, and — via the random stream — discovers structure no archetype encodes. Every
genome it emits is structurally valid by construction (it only draws from the registry).
"""
from __future__ import annotations

from typing import List

import numpy as np

from mt.config import MARKETS, available_feeds
from mt.genome.registry import REGISTRY, ops_for_stage, computable_feature_ops
from mt.genome.schema import Genome, Meta, FeatureNode, SignalSpec, SizingSpec, RiskSpec

__all__ = ["available_feeds", "TemplateSampler"]


class TemplateSampler:
    def __init__(self, seed: int = 4242):
        self.rng = np.random.default_rng(seed)

    def _meta(self, market: str, execution: str = "cross_sectional") -> Meta:
        m = MARKETS[market]
        return Meta(market=market, htf=m.htf, mtf=m.mtf, ltf=m.ltf,
                    rebalance=m.htf, cost_profile=f"{market}_default", execution=execution)

    def _feature_ops(self, market: str) -> List[str]:
        """Computable feature ops whose data_requires this market can satisfy (docs/12 §5).

        Declared-only primitives (e.g. AMT footprint needing `trades`) are registered for
        planning/typecheck but excluded here so genomes never carry inert features."""
        feeds = available_feeds(market)
        return [op.name for op in computable_feature_ops()
                if all(d in feeds for d in op.data_requires)]

    # ─── named archetypes (broad coverage — no single style favored) ──────
    ARCHETYPES = ["trend", "momentum_burst", "reversion", "oscillator_revert", "breakout",
                  "carry", "lowvol", "volexp", "statistical", "volume_flow", "auction", "macd_trend",
                  # directional phenotype (Tier-2, triple-barrier)
                  "dir_trend", "dir_revert", "dir_breakout"]

    def _fn(self, i, op, **args):
        return FeatureNode(f"f{i}", op, args)

    def _archetype(self, market: str, kind: str) -> Genome:
        rng = self.rng
        h = int(rng.integers(4, 13))
        # weighted toward 'all' (~57%) so the search keeps both unconditional and regime-conditioned
        reg = lambda: ("all", "all", "all", "low_vol", "high_vol", "trend", "chop")[int(rng.integers(7))]
        blend = SignalSpec("weighted_blend", {"direction": "neutral", "regime": reg()})
        gate = lambda d="long_bias", t=(0.3, 1.0): SignalSpec("gated_and", {"threshold": round(float(rng.uniform(*t)), 2), "direction": d, "regime": reg()})
        gor = lambda d="long_bias", t=(0.3, 1.0): SignalSpec("gated_or", {"threshold": round(float(rng.uniform(*t)), 2), "direction": d, "regime": reg()})

        if kind in ("dir_trend", "dir_revert", "dir_breakout"):
            return self._directional(market, kind)

        if kind == "trend":
            feats = [self._fn(1, "momentum", lookback=int(rng.integers(40, 160)), skip=1),
                     self._fn(2, "adx", window=int(rng.integers(10, 28))),
                     self._fn(3, "slope", window=int(rng.integers(10, 40)))]; sig = blend
        elif kind == "momentum_burst":
            feats = [self._fn(1, "roc", window=int(rng.integers(5, 30))),
                     self._fn(2, "rel_volume", window=int(rng.integers(20, 60)))]; sig = gor(); h = int(rng.integers(2, 6))
        elif kind == "reversion":
            feats = [self._fn(1, "reversion", lookback=int(rng.integers(1, 6))),
                     self._fn(2, "rsi", window=int(rng.integers(7, 21))),
                     self._fn(3, "bb_position", window=int(rng.integers(15, 40)), mult=2.0)]; sig = blend; h = int(rng.integers(1, 4))
        elif kind == "oscillator_revert":
            feats = [self._fn(1, "stoch", window=int(rng.integers(9, 28))),
                     self._fn(2, "williams_r", window=int(rng.integers(9, 28))),
                     self._fn(3, "cci", window=int(rng.integers(14, 40)))]; sig = blend; h = int(rng.integers(1, 5))
        elif kind == "breakout":
            feats = [self._fn(1, "breakout", window=int(rng.integers(30, 90))),
                     self._fn(2, "atr_expansion", window=int(rng.integers(20, 60)))]; sig = gate()
        elif kind == "carry" and MARKETS[market].has_funding:
            feats = [self._fn(1, "funding_z", window=int(rng.integers(48, 120)))]; sig = gate()
        elif kind == "lowvol":
            feats = [self._fn(1, "atr_pct"), self._fn(2, "realized_vol", window=int(rng.integers(20, 80))),
                     self._fn(3, "vol_of_vol", window=int(rng.integers(30, 90)))]; sig = blend
        elif kind == "volexp":
            feats = [self._fn(1, "atr_expansion", window=int(rng.integers(20, 80))),
                     self._fn(2, "breakout", window=int(rng.integers(20, 60)))]; sig = gate()
        elif kind == "statistical":
            feats = [self._fn(1, "variance_ratio", window=int(rng.integers(60, 200)), q=int(rng.integers(2, 8))),
                     self._fn(2, "hurst", window=int(rng.integers(60, 200))),
                     self._fn(3, "autocorr", lag=1, window=int(rng.integers(40, 120)))]; sig = blend
        elif kind == "volume_flow":
            feats = [self._fn(1, "obv", window=int(rng.integers(30, 90))),
                     self._fn(2, "vwap_distance", window=int(rng.integers(30, 90))),
                     self._fn(3, "volume_zscore", window=int(rng.integers(20, 60)))]; sig = blend
        elif kind == "auction":
            feats = [self._fn(1, "dist_to_poc", window=int(rng.integers(40, 120))),
                     self._fn(2, "value_area_position", window=int(rng.integers(40, 120))),
                     self._fn(3, "cumulative_delta", window=int(rng.integers(30, 90)))]; sig = blend
        else:  # macd_trend
            feats = [self._fn(1, "macd", fast=12, slow=26, signal=9),
                     self._fn(2, "ma_cross", fast=int(rng.integers(8, 20)), slow=int(rng.integers(30, 80)))]; sig = gor()

        sizing = SizingSpec("rank_bucket", {"top_frac": round(float(rng.uniform(0.1, 0.25)), 2),
                                            "gross": 1.0, "per_name_cap": 0.15})
        risk = RiskSpec("horizon_hold", {"horizon": h, "cost_stress": 1.0})
        return Genome(self._meta(market), feats, sig, sizing, risk, generator=f"template:{kind}")

    # ─── directional (Tier-2, triple-barrier) archetypes ─────────────────
    def _directional(self, market: str, kind: str) -> Genome:
        rng = self.rng
        reg = ("all", "all", "all", "low_vol", "high_vol", "trend", "chop")[int(rng.integers(7))]
        if kind == "dir_trend":
            feats = [self._fn(1, "momentum", lookback=int(rng.integers(40, 140)), skip=1),
                     self._fn(2, "adx", window=int(rng.integers(10, 28)))]
            sig = SignalSpec("weighted_blend", {"direction": "long_bias" if rng.random() < 0.6 else "neutral", "regime": reg})
        elif kind == "dir_revert":
            feats = [self._fn(1, "rsi", window=int(rng.integers(7, 21))),
                     self._fn(2, "bb_position", window=int(rng.integers(15, 40)), mult=2.0)]
            sig = SignalSpec("weighted_blend", {"direction": "neutral", "regime": reg})
        else:  # dir_breakout
            feats = [self._fn(1, "breakout", window=int(rng.integers(30, 90))),
                     self._fn(2, "atr_expansion", window=int(rng.integers(20, 60)))]
            sig = SignalSpec("gated_or", {"threshold": round(float(rng.uniform(0.4, 1.0)), 2), "direction": "long_bias", "regime": reg})
        siz = SizingSpec("fixed_fractional", {"f": round(float(rng.uniform(0.05, 0.2)), 2)})
        risk = RiskSpec("triple_barrier", {"entry_thr": round(float(rng.uniform(0.4, 1.0)), 2),
                                           "sl_mult": round(float(rng.uniform(1.0, 2.5)), 2),
                                           "tp_mult": round(float(rng.uniform(1.5, 4.0)), 2),
                                           "max_bars": int(rng.integers(8, 32)), "cost_stress": 1.0})
        return Genome(self._meta(market, "directional"), feats, sig, siz, risk, generator=f"template:{kind}")

    # ─── fully-random genome (coherent phenotype) ────────────────────────
    def _random(self, market: str) -> Genome:
        rng = self.rng
        ops = self._feature_ops(market)
        feats = [FeatureNode(f"f{i+1}", op := ops[int(rng.integers(len(ops)))], REGISTRY[op].sample_args(rng))
                 for i in range(int(rng.integers(1, 4)))]
        sig_op = ops_for_stage("signal")[int(rng.integers(len(ops_for_stage("signal"))))]
        sig = SignalSpec(sig_op.name, sig_op.sample_args(rng))
        if rng.random() < 0.35:                          # directional phenotype
            siz_name = ("fixed_fractional", "atr_scaled")[int(rng.integers(2))]
            siz = SizingSpec(siz_name, REGISTRY[siz_name].sample_args(rng))
            risk = RiskSpec("triple_barrier", REGISTRY["triple_barrier"].sample_args(rng))
            meta = self._meta(market, "directional")
        else:                                             # cross-sectional phenotype
            siz_name = ("rank_bucket", "vol_target", "kelly_fraction")[int(rng.integers(3))]
            siz = SizingSpec(siz_name, REGISTRY[siz_name].sample_args(rng))
            risk = RiskSpec("horizon_hold", REGISTRY["horizon_hold"].sample_args(rng))
            meta = self._meta(market, "cross_sectional")
        return Genome(meta, feats, sig, siz, risk, generator="random")

    # ─── batch API ───────────────────────────────────────────────────────
    def sample(self, market: str, n_random: int = 6) -> List[Genome]:
        kinds = [k for k in self.ARCHETYPES if not (k == "carry" and not MARKETS[market].has_funding)]
        genomes = [self._archetype(market, k) for k in kinds]
        genomes += [self._random(market) for _ in range(n_random)]
        return genomes
