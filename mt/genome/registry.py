"""mt.genome.registry — the primitive vocabulary under the full declaration contract.

Implements the docs/11 §1 contract and §8 registration gate: every primitive declares
typed I/O, bounded args + sampling priors, a point-in-time (PIT) leakage contract,
`data_requires`, a cost class, tags, and provenance — and is rejected at the door if it is
untyped, leaky (`uses_future`), unbounded, or unsatisfiable. This is the front-door filter
that keeps an unbounded, no-privilege space *valid* rather than chaotic; the Gauntlet
(docs/05) is the back-door filter that keeps conclusions honest.

Breadth policy (docs/11): SMC/ICT is one family among many. `computable=True` primitives
have a builder in mt.sim.features and flow through the thin slice today (incl. the Auction
Market Theory proxy subset); `computable=False` ones are *declared* for planning /
type-checking and light up as their data or wrappers land (see docs/12).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

# ─── the type system (docs/11 §2) ────────────────────────────────────────
FEATURE_TYPES = {
    "Series[price]", "Series[price_level]", "Series[return]", "Series[osc_0_100]",
    "Series[zscore]", "Series[rank]", "Series[binary]", "Series[categorical]", "Series",
}
STAGE_OUTPUT = {"signal": "Signal", "sizing": "Position", "risk": "OrderIntent"}
STAGES = {"feature", "signal", "sizing", "risk", "meta", "transform"}


@dataclass(frozen=True)
class ArgSpec:
    """One argument's type, bounds, and sampling prior."""
    kind: str                      # "int" | "float" | "choice" | "bool"
    low: float = 0.0
    high: float = 1.0
    log: bool = False
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
        if self.kind in ("choice", "bool"):
            return self.sample(rng)
        step = (self.high - self.low) * 0.15
        return self.clamp(v + rng.normal(0.0, step))

    def is_bounded(self) -> bool:
        if self.kind == "choice":
            return len(self.choices) > 0
        if self.kind == "bool":
            return True
        return math.isfinite(self.low) and math.isfinite(self.high) and self.high > self.low


@dataclass(frozen=True)
class Pit:
    """Point-in-time / leakage contract (docs/11 §1). `uses_future` MUST be False."""
    lookback: object = "= window"
    uses_future: bool = False
    closed_bar_only: bool = True


@dataclass(frozen=True)
class OpSpec:
    name: str
    stage: str
    args: Dict[str, ArgSpec] = field(default_factory=dict)
    output: str = "Series[zscore]"
    inputs: tuple = ("Series",)
    data_requires: tuple = ("ohlcv",)
    cost_class: str = "cheap"       # cheap | medium | heavy
    tags: tuple = ()
    pit: Pit = field(default_factory=Pit)
    provenance: dict = field(default_factory=lambda: {"source": "human", "version": "1.0.0"})
    computable: bool = False         # True ⇒ a builder exists in mt.sim.features
    needs: tuple = ()                # back-compat: non-ohlcv feeds (derived if empty)
    doc: str = ""

    def sample_args(self, rng: np.random.Generator) -> dict:
        return {k: spec.sample(rng) for k, spec in self.args.items()}


class RegistrationError(ValueError):
    pass


def _validate(op: OpSpec) -> None:
    """The registration gate (docs/11 §8) — reject before it can poison a genome."""
    if op.stage not in STAGES:
        raise RegistrationError(f"{op.name}: unknown stage {op.stage!r}")
    if op.pit.uses_future:
        raise RegistrationError(f"{op.name}: uses_future=True is never allowed (leakage)")
    if op.stage in ("feature", "transform") and op.output not in FEATURE_TYPES:
        raise RegistrationError(f"{op.name}: unknown output type {op.output!r}")
    if op.stage in STAGE_OUTPUT and op.output != STAGE_OUTPUT[op.stage]:
        raise RegistrationError(f"{op.name}: {op.stage} op must output {STAGE_OUTPUT[op.stage]}")
    for k, spec in op.args.items():
        if not spec.is_bounded():
            raise RegistrationError(f"{op.name}: arg {k!r} is unbounded")
    if not op.data_requires:
        raise RegistrationError(f"{op.name}: empty data_requires")


REGISTRY: Dict[str, OpSpec] = {}


def register(op: OpSpec) -> OpSpec:
    _validate(op)
    # back-compat: keep `needs` = required feeds beyond ohlcv (funding detection etc.)
    if not op.needs:
        object.__setattr__(op, "needs", tuple(d for d in op.data_requires if d != "ohlcv"))
    REGISTRY[op.name] = op
    return op


def ops_for_stage(stage: str) -> List[OpSpec]:
    return [op for op in REGISTRY.values() if op.stage == stage]


def computable_feature_ops() -> List[OpSpec]:
    return [op for op in REGISTRY.values() if op.stage == "feature" and op.computable]


def get(name: str) -> Optional[OpSpec]:
    return REGISTRY.get(name)


def _win(default, lo=5, hi=200):
    return ArgSpec("int", lo, hi, log=True, default=default)


# ═══ SEED VOCABULARY ══════════════════════════════════════════════════════
# Registered through the gate. Grouped by catalog family (docs/11 §3).

# ── 3.3 momentum / 3.1 return / 3.2 trend / 3.4 vol / classical (computable) ──
register(OpSpec("momentum", "feature", {"lookback": _win(84), "skip": ArgSpec("int", 0, 5, default=1)},
                output="Series[zscore]", cost_class="cheap", tags=("momentum", "classical_ta"),
                computable=True, doc="risk-adjusted price momentum"))
register(OpSpec("reversion", "feature", {"lookback": ArgSpec("int", 1, 20, default=3)},
                output="Series[return]", tags=("mean_reversion",), computable=True,
                doc="short-horizon mean reversion"))
register(OpSpec("ema_dist", "feature", {"window": _win(50)}, output="Series[zscore]",
                tags=("trend", "classical_ta"), computable=True, doc="close distance from EMA in ATR"))
register(OpSpec("rsi", "feature", {"window": ArgSpec("int", 5, 50, default=14)},
                output="Series[osc_0_100]", tags=("momentum", "oscillator"), computable=True))
register(OpSpec("realized_vol", "feature", {"window": _win(48, 5, 120)}, output="Series[return]",
                tags=("volatility",), computable=True, doc="rolling realized vol (negated)"))
register(OpSpec("breakout", "feature", {"window": _win(55, 10, 120)}, output="Series[zscore]",
                tags=("breakout", "pattern"), computable=True, doc="Donchian breakout distance in ATR"))
register(OpSpec("atr_pct", "feature", {}, output="Series[return]", tags=("volatility",),
                computable=True, pit=Pit(lookback=14), doc="ATR/close (low-vol tilt)"))

# ── 3.6 microstructure / order flow ──
register(OpSpec("funding_z", "feature", {"window": _win(72, 8, 200)}, output="Series[zscore]",
                data_requires=("ohlcv", "funding_rate"), cost_class="medium",
                tags=("microstructure", "funding", "crypto"), computable=True,
                doc="funding-rate z-score (contrarian to crowded funding)"))
register(OpSpec("order_flow_imbalance", "feature", {"window": _win(48, 5, 200)}, output="Series[zscore]",
                data_requires=("taker_buy",), cost_class="medium", tags=("microstructure", "order_flow"),
                computable=True, doc="net aggressor fraction from REAL Binance taker-buy volume"))
register(OpSpec("aggressor_ratio", "feature", {"window": _win(48, 5, 200)}, output="Series[return]",
                data_requires=("taker_buy",), cost_class="medium", tags=("microstructure", "order_flow", "auction_market_theory"),
                computable=True, doc="market-buy vs market-sell share (real taker-buy), centered"))
register(OpSpec("trade_intensity", "feature", {"window": _win(48, 5, 200)}, output="Series[zscore]",
                data_requires=("taker_buy",), cost_class="medium", tags=("microstructure", "auction_market_theory"),
                computable=True, doc="auction speed: z-score of real trades-per-bar"))
# canonical microstructure measures on REAL order flow (docs/13 §2)
register(OpSpec("vpin", "feature", {"window": _win(48, 10, 300)}, output="Series[return]",
                data_requires=("taker_buy",), cost_class="medium",
                tags=("microstructure", "order_flow", "auction_market_theory"), computable=True,
                doc="VPIN order-flow toxicity Σ|buy−sell|/Σvol (Easley-López de Prado-O'Hara 2012)"))
register(OpSpec("kyle_lambda", "feature", {"window": _win(48, 10, 300)}, output="Series[zscore]",
                data_requires=("taker_buy",), cost_class="medium", tags=("microstructure", "order_flow", "liquidity"),
                computable=True, doc="Kyle's λ price impact cov(ret,flow)/var(flow) (Kyle 1985)"))
register(OpSpec("amihud_illiquidity", "feature", {"window": _win(48, 10, 300)}, output="Series[return]",
                cost_class="cheap", tags=("microstructure", "liquidity"), computable=True,
                doc="Amihud (2002) illiquidity: rolling mean |return|/dollar-volume"))

# ── 3.15 Auction Market Theory & order flow (AMT proxies computable; footprint declared) ──
register(OpSpec("dist_to_poc", "feature", {"window": _win(60, 20, 240)}, output="Series[zscore]",
                cost_class="medium", tags=("auction_market_theory", "volume_profile"), computable=True,
                doc="distance to developing volume POC in ATR (proxy)"))
register(OpSpec("value_area_position", "feature", {"window": _win(60, 20, 240)}, output="Series[categorical]",
                cost_class="medium", tags=("auction_market_theory", "market_profile"), computable=True,
                doc="above / inside / below the developing value area (proxy)"))
register(OpSpec("cumulative_delta", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                cost_class="medium", tags=("auction_market_theory", "order_flow"), computable=True,
                doc="cumulative volume delta via close-location proxy (extends cvd)"))
register(OpSpec("delta_divergence", "feature", {"window": ArgSpec("int", 5, 60, default=14)},
                output="Series[zscore]", cost_class="medium", tags=("auction_market_theory", "order_flow"),
                computable=True, doc="price up / delta down → absorption warning (proxy)"))
register(OpSpec("rotation_factor", "feature", {"window": ArgSpec("int", 5, 60, default=20)},
                output="Series[zscore]", cost_class="cheap", tags=("auction_market_theory",),
                computable=True, doc="TPO up/down rotation count proxy"))
register(OpSpec("stacked_imbalance", "feature", {"n_levels": ArgSpec("int", 2, 6, default=3)},
                output="Series[zscore]", data_requires=("trades",), cost_class="heavy",
                tags=("auction_market_theory", "order_flow", "footprint"), computable=True,
                doc="consecutive lopsided footprint levels from REAL aggTrades (fp_stacked)"))
register(OpSpec("absorption", "feature", {"window": ArgSpec("int", 3, 50, default=10)},
                output="Series[zscore]", data_requires=("trades",), cost_class="heavy",
                tags=("auction_market_theory", "order_flow", "footprint"), computable=True,
                doc="aggressive volume that failed to move price, from REAL aggTrades (fp_absorption)"))

# ── extended computable families (breadth mandate — no school privileged) ──
# trend
register(OpSpec("sma_dist", "feature", {"window": _win(50)}, output="Series[zscore]",
                tags=("trend", "classical_ta"), computable=True))
register(OpSpec("ma_cross", "feature",
                {"fast": ArgSpec("int", 3, 50, default=12), "slow": _win(48, 10, 200)},
                output="Series[zscore]", tags=("trend",), computable=True))
register(OpSpec("slope", "feature", {"window": _win(20, 5, 120)}, output="Series[zscore]",
                tags=("trend",), computable=True))
register(OpSpec("adx", "feature", {"window": ArgSpec("int", 5, 50, default=14)},
                output="Series[zscore]", tags=("trend", "classical_ta"), computable=True))
# oscillators
register(OpSpec("macd", "feature",
                {"fast": ArgSpec("int", 5, 20, default=12), "slow": ArgSpec("int", 20, 60, default=26),
                 "signal": ArgSpec("int", 5, 20, default=9)}, output="Series[zscore]",
                tags=("momentum", "oscillator"), computable=True))
register(OpSpec("stoch", "feature", {"window": ArgSpec("int", 5, 50, default=14)},
                output="Series[osc_0_100]", tags=("oscillator",), computable=True))
register(OpSpec("cci", "feature", {"window": _win(20, 5, 100)}, output="Series[zscore]",
                tags=("oscillator",), computable=True))
register(OpSpec("williams_r", "feature", {"window": ArgSpec("int", 5, 50, default=14)},
                output="Series[osc_0_100]", tags=("oscillator",), computable=True))
register(OpSpec("roc", "feature", {"window": _win(12, 2, 120)}, output="Series[return]",
                tags=("momentum",), computable=True))
# volatility
register(OpSpec("bb_position", "feature", {"window": _win(20, 10, 100), "mult": ArgSpec("float", 1.5, 3.0, default=2.0)},
                output="Series[osc_0_100]", tags=("volatility",), computable=True))
register(OpSpec("atr_expansion", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                tags=("volatility",), computable=True))
register(OpSpec("vol_of_vol", "feature", {"window": _win(48, 10, 200)}, output="Series[return]",
                tags=("volatility",), computable=True))
# volume
register(OpSpec("obv", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                tags=("volume",), computable=True))
register(OpSpec("vwap_distance", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                tags=("volume", "auction_market_theory"), computable=True))
register(OpSpec("rel_volume", "feature", {"window": _win(48, 10, 200)}, output="Series[return]",
                tags=("volume",), computable=True))
register(OpSpec("volume_zscore", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                tags=("volume",), computable=True))
# statistical / econometric
register(OpSpec("autocorr", "feature", {"lag": ArgSpec("int", 1, 10, default=1), "window": _win(48, 20, 200)},
                output="Series[zscore]", cost_class="medium", tags=("statistical",), computable=True))
register(OpSpec("variance_ratio", "feature", {"window": _win(96, 40, 300), "q": ArgSpec("int", 2, 10, default=4)},
                output="Series[zscore]", cost_class="medium", tags=("statistical",), computable=True,
                doc="trend vs mean-revert diagnostic"))
register(OpSpec("rolling_skew", "feature", {"window": _win(48, 20, 200)}, output="Series[zscore]",
                tags=("statistical",), computable=True))
register(OpSpec("rolling_kurt", "feature", {"window": _win(48, 20, 200)}, output="Series[zscore]",
                tags=("statistical",), computable=True))
register(OpSpec("price_zscore", "feature", {"window": _win(48, 10, 200)}, output="Series[zscore]",
                tags=("statistical", "mean_reversion"), computable=True))
# pattern
register(OpSpec("consolidation_score", "feature", {"window": _win(20, 8, 100)}, output="Series[osc_0_100]",
                tags=("pattern",), computable=True))

# ── other families: declared-only, to show the contract's breadth (docs/12 §2) ──
register(OpSpec("hurst", "feature", {"window": _win(120, 40, 400)}, output="Series[zscore]",
                cost_class="medium", tags=("statistical", "persistence"), computable=True,
                doc="Hurst exponent (aggregated-variance method): H−0.5, >0 trending <0 reverting"))
register(OpSpec("mean_reversion_halflife", "feature", {"window": _win(60, 20, 240)}, output="Series[zscore]",
                cost_class="medium", tags=("statistical", "mean_reversion"), computable=True,
                doc="Ornstein-Uhlenbeck MR alpha: deviation×reversion-speed from rolling AR(1) (Chan)"))
register(OpSpec("coint_zscore", "feature", {"window": _win(90, 30, 300)}, output="Series[zscore]",
                data_requires=("cross_asset",), cost_class="medium", tags=("statistical", "mean_reversion", "cross_asset"),
                computable=True, doc="cointegration-residual z-score vs benchmark (Engle-Granger/Chan pairs)"))
register(OpSpec("candlestick_pattern", "feature",
                {"pattern": ArgSpec("choice", choices=("engulfing", "pin", "doji", "inside"), default="engulfing")},
                output="Series[categorical]", tags=("pattern",), computable=True,
                doc="signed candlestick pattern flag"))
register(OpSpec("order_block_strength", "feature", {}, output="Series[zscore]", cost_class="medium",
                tags=("smc", "ict"), computable=True,
                doc="net recent displacement-after-opposite-candle pressure (SMC OB proxy, ATR)"))
register(OpSpec("rolling_corr", "feature", {"window": _win(60, 20, 200)},
                output="Series[zscore]", data_requires=("cross_asset",), cost_class="medium",
                tags=("cross_asset", "intermarket"), computable=True,
                doc="rolling correlation of returns with the market benchmark (BTC / gold)"))
# SMC / ICT — lightweight computable time-series proxies (full concepts/* remain snapshot-only)
register(OpSpec("structure_break", "feature", {"window": _win(20, 8, 100)}, output="Series[categorical]",
                cost_class="medium", tags=("smc", "ict"), computable=True,
                doc="break of structure: close beyond the prior N-bar swing extreme"))
register(OpSpec("fvg_gap", "feature", {}, output="Series[zscore]", cost_class="medium",
                tags=("smc", "ict"), computable=True, doc="signed fair-value-gap size in ATR"))
register(OpSpec("liquidity_sweep", "feature", {"window": _win(20, 8, 100)}, output="Series[categorical]",
                cost_class="medium", tags=("smc", "ict"), computable=True,
                doc="swept-then-reclaim of a prior swing extreme (stop run)"))
register(OpSpec("cot_zscore", "feature", {"window": _win(26, 4, 104)},
                output="Series[zscore]", data_requires=("cot",), cost_class="cheap",
                tags=("macro", "positioning"), computable=True,
                doc="CFTC COT net-positioning z-score (from enriched cot_z column)"))
register(OpSpec("news_sentiment", "feature", {"window": _win(24, 4, 168)}, output="Series[zscore]",
                data_requires=("news",), cost_class="medium", tags=("sentiment", "macro"), computable=True,
                doc="GDELT news tone (from enriched news_tone column)"))
register(OpSpec("event_surprise", "feature", {"window": _win(12, 2, 72)}, output="Series[zscore]",
                data_requires=("calendar",), cost_class="cheap", tags=("macro", "calendar", "event"),
                computable=True, doc="economic-event surprise (ForexFactory/MetalsMine/CryptoCraft)"))
register(OpSpec("vol_regime_tag", "feature", {"tiers": ArgSpec("int", 3, 5, default=4)},
                output="Series[zscore]", cost_class="medium",
                tags=("regime", "ml_derived"), computable=True,
                doc="volatility-regime percentile in [-1,1] (model-free vol tier)"))

# ── §4 signal ops ──
_REGIME = ArgSpec("choice", choices=("all", "low_vol", "high_vol", "trend", "chop"), default="all")
register(OpSpec("weighted_blend", "signal",
                {"direction": ArgSpec("choice", choices=("long_bias", "short_bias", "neutral"), default="neutral"),
                 "regime": _REGIME},
                output="Signal", inputs=("Series[zscore]",), tags=("blend",), computable=True,
                doc="row z-score sum of features, optionally conditioned to a regime"))
register(OpSpec("gated_and", "signal",
                {"threshold": ArgSpec("float", 0.0, 2.0, default=0.5),
                 "direction": ArgSpec("choice", choices=("long_bias", "short_bias"), default="long_bias"),
                 "regime": _REGIME},
                output="Signal", inputs=("Series[zscore]",), tags=("logic", "gate"), computable=True,
                doc="long/short only where EVERY feature clears a z-threshold, optionally regime-gated"))
register(OpSpec("gated_or", "signal",
                {"threshold": ArgSpec("float", 0.0, 2.0, default=0.7),
                 "direction": ArgSpec("choice", choices=("long_bias", "short_bias"), default="long_bias"),
                 "regime": _REGIME},
                output="Signal", inputs=("Series[zscore]",), tags=("logic", "gate"), computable=True,
                doc="long/short where ANY feature clears a z-threshold, optionally regime-gated"))

# ── §5 sizing ops ──
register(OpSpec("rank_bucket", "sizing",
                {"top_frac": ArgSpec("float", 0.05, 0.30, default=0.10),
                 "gross": ArgSpec("float", 0.5, 2.0, default=1.0),
                 "per_name_cap": ArgSpec("float", 0.02, 0.20, default=0.10)},
                output="Position", inputs=("Signal",), tags=("cross_sectional",), computable=True))
register(OpSpec("vol_target", "sizing",
                {"target_ann_vol": ArgSpec("float", 0.05, 0.40, default=0.15),
                 "top_frac": ArgSpec("float", 0.05, 0.30, default=0.10),
                 "per_name_cap": ArgSpec("float", 0.02, 0.20, default=0.10)},
                output="Position", inputs=("Signal",), tags=("vol_target",), computable=True))
register(OpSpec("kelly_fraction", "sizing",
                {"kelly_frac": ArgSpec("float", 0.2, 1.0, default=0.5),      # 0.5 = half Kelly (practitioner default)
                 "max_leverage": ArgSpec("float", 1.0, 5.0, default=3.0),
                 "top_frac": ArgSpec("float", 0.05, 0.30, default=0.10),
                 "gross": ArgSpec("float", 0.5, 2.0, default=1.0),
                 "per_name_cap": ArgSpec("float", 0.02, 0.20, default=0.10)},
                output="Position", inputs=("Signal",), tags=("kelly", "capital_management"), computable=True,
                doc="growth-optimal book leverage f*=(mu/sigma^2), fractional/half-Kelly, from TRAILING stats"))

# ── §6 risk overlays ──
register(OpSpec("horizon_hold", "risk",
                {"horizon": ArgSpec("int", 1, 48, log=True, default=6),
                 "cost_stress": ArgSpec("float", 1.0, 2.0, default=1.0)},
                output="OrderIntent", inputs=("Position",), tags=("holding",), computable=True,
                doc="non-overlapping holding horizon; cost_stress multiplies costs"))
register(OpSpec("triple_barrier", "risk",
                {"entry_thr": ArgSpec("float", 0.2, 1.5, default=0.6),
                 "sl_mult": ArgSpec("float", 0.5, 3.0, default=1.5),
                 "tp_mult": ArgSpec("float", 1.0, 5.0, default=2.5),
                 "max_bars": ArgSpec("int", 4, 48, log=True, default=16),
                 "cost_stress": ArgSpec("float", 1.0, 2.0, default=1.0)},
                output="OrderIntent", inputs=("Position",), tags=("directional", "labeling"), computable=True,
                doc="López-de-Prado triple barrier (ATR TP/SL + time stop) — directional phenotype"))

# ── §5 sizing (directional) ──
register(OpSpec("fixed_fractional", "sizing", {"f": ArgSpec("float", 0.02, 0.30, default=0.10)},
                output="Position", inputs=("Signal",), tags=("directional",), computable=True))
register(OpSpec("atr_scaled", "sizing", {"atr_mult": ArgSpec("float", 0.5, 4.0, default=1.5)},
                output="Position", inputs=("Signal",), tags=("directional",), computable=True))
