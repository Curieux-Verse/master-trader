"""mt.genome.registry — the vetted primitive vocabulary and its argument bounds.

The registry is what makes randomly-assembled genomes *structurally valid by
construction*: every op declares its stage, argument ranges, and a sampling prior, so
generation / mutation / typecheck all share one source of truth (docs/02 §4). This is a
deliberately small SEED of the vast, open-ended vocabulary docs/02 describes — new
primitives (SMC detectors via CC_Trading's compute_smc_features, mined factors, LLM
inventions) are appended here and every engine can use them immediately.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


@dataclass(frozen=True)
class ArgSpec:
    """One argument's type, bounds, and sampling prior."""
    kind: str                      # "int" | "float" | "choice" | "bool"
    low: float = 0.0
    high: float = 1.0
    log: bool = False              # log-uniform sampling (windows)
    choices: tuple = ()
    default: object = None

    def sample(self, rng: np.random.Generator):
        if self.kind == "choice":
            return self.choices[int(rng.integers(len(self.choices)))]
        if self.kind == "bool":
            return bool(rng.integers(2))
        if self.log:
            v = math.exp(rng.uniform(math.log(self.low), math.log(self.high)))
        else:
            v = rng.uniform(self.low, self.high)
        return int(round(v)) if self.kind == "int" else float(v)

    def clamp(self, v):
        if self.kind == "choice":
            return v if v in self.choices else self.default
        if self.kind == "bool":
            return bool(v)
        v = max(self.low, min(self.high, v))
        return int(round(v)) if self.kind == "int" else float(v)

    def mutate(self, v, rng: np.random.Generator):
        """Perturb one step within bounds (a local nudge, not a resample)."""
        if self.kind in ("choice", "bool"):
            return self.sample(rng)
        span = (self.high - self.low)
        step = span * 0.15
        return self.clamp(v + rng.normal(0.0, step))


@dataclass(frozen=True)
class OpSpec:
    name: str
    stage: str                     # "feature" | "signal" | "sizing" | "risk"
    args: Dict[str, ArgSpec] = field(default_factory=dict)
    needs: tuple = ()              # data requirements, e.g. ("funding_rate",)
    doc: str = ""

    def sample_args(self, rng: np.random.Generator) -> dict:
        return {k: spec.sample(rng) for k, spec in self.args.items()}


# ─── the seed vocabulary ─────────────────────────────────────────────────

_FEATURES = [
    OpSpec("momentum", "feature",
           {"lookback": ArgSpec("int", 5, 200, log=True, default=84),
            "skip": ArgSpec("int", 0, 5, default=1)},
           doc="risk-adjusted price momentum P[t-skip]/P[t-skip-lookback]-1"),
    OpSpec("reversion", "feature",
           {"lookback": ArgSpec("int", 1, 20, default=3)},
           doc="short-horizon mean reversion: negative recent return"),
    OpSpec("ema_dist", "feature",
           {"window": ArgSpec("int", 5, 200, log=True, default=50)},
           doc="distance of close from its EMA, in ATR units"),
    OpSpec("rsi", "feature",
           {"window": ArgSpec("int", 5, 50, default=14)},
           doc="Wilder RSI, centered to [-1,1]"),
    OpSpec("realized_vol", "feature",
           {"window": ArgSpec("int", 5, 120, log=True, default=48)},
           doc="rolling realized volatility (negated: prefer calmer names)"),
    OpSpec("breakout", "feature",
           {"window": ArgSpec("int", 10, 120, log=True, default=55)},
           doc="Donchian breakout distance in ATR units"),
    OpSpec("atr_pct", "feature",
           {}, doc="ATR / close (volatility feature; already in the frame)"),
    OpSpec("funding_z", "feature",
           {"window": ArgSpec("int", 8, 200, log=True, default=72)},
           needs=("funding_rate",),
           doc="funding-rate z-score (crypto perps) — contrarian to crowded funding"),
]

_SIGNALS = [
    OpSpec("weighted_blend", "signal",
           {"direction": ArgSpec("choice", choices=("long_bias", "short_bias", "neutral"),
                                 default="neutral")},
           doc="row z-score sum of features (the honest v1 blend)"),
    OpSpec("gated_and", "signal",
           {"threshold": ArgSpec("float", 0.0, 2.0, default=0.5),
            "direction": ArgSpec("choice", choices=("long_bias", "short_bias"),
                                  default="long_bias")},
           doc="long/short only where every feature clears a z-threshold"),
]

_SIZING = [
    OpSpec("rank_bucket", "sizing",
           {"top_frac": ArgSpec("float", 0.05, 0.30, default=0.10),
            "gross": ArgSpec("float", 0.5, 2.0, default=1.0),
            "per_name_cap": ArgSpec("float", 0.02, 0.20, default=0.10)},
           doc="long top-frac / short bottom-frac, dollar-neutral, capped"),
    OpSpec("vol_target", "sizing",
           {"target_ann_vol": ArgSpec("float", 0.05, 0.40, default=0.15),
            "top_frac": ArgSpec("float", 0.05, 0.30, default=0.10),
            "per_name_cap": ArgSpec("float", 0.02, 0.20, default=0.10)},
           doc="rank bucket scaled to a target annualized volatility"),
]

_RISK = [
    OpSpec("horizon_hold", "risk",
           {"horizon": ArgSpec("int", 1, 48, log=True, default=6),
            "cost_stress": ArgSpec("float", 1.0, 1.0, default=1.0)},
           doc="non-overlapping holding horizon (bars); cost_stress multiplies costs"),
]

REGISTRY: Dict[str, OpSpec] = {op.name: op for op in (_FEATURES + _SIGNALS + _SIZING + _RISK)}


def ops_for_stage(stage: str) -> List[OpSpec]:
    return [op for op in REGISTRY.values() if op.stage == stage]


def get(name: str) -> Optional[OpSpec]:
    return REGISTRY.get(name)
