"""mt.sim.directional — Tier-2 event-driven, per-symbol DIRECTIONAL executor.

The complement to the cross-sectional Tier-1 book: this trades each symbol on its own
signal with a López-de-Prado **triple-barrier** overlay (ATR take-profit / stop-loss / time
stop), simulating the intrabar path with high/low. It is how SMC-style, breakout, and
single-instrument (XAU) strategies get tested — a whole phenotype the rank-bucket engine
cannot express. Same EvalResult contract, so the gauntlet treats both identically.

Signals are standardized *over time per symbol* (rolling z), never cross-sectionally, so a
one-instrument market is first-class. Every trade pays the shared round-trip cost.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from mt.adapters.cclib import round_trip_cost_bps
from mt.config import MARKETS
from mt.data.panel import NormPanel
from mt.genome.schema import Genome
from mt.sim import features as F
from mt.sim.evalresult import EvalResult


def _tf_minutes(tf: str) -> int:
    tf = tf.strip()
    if tf and tf[0].isdigit():
        unit, val = tf[-1].lower(), int(tf[:-1])
    else:
        unit, val = tf[0].lower(), int(tf[1:] or 1)
    return {"m": 1, "h": 60, "d": 1440}[unit] * val


def _time_z(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    mu = df.rolling(window, min_periods=max(10, window // 4)).mean()
    sd = df.rolling(window, min_periods=max(10, window // 4)).std().replace(0, np.nan)
    return (df - mu) / sd


class Tier2Executor:
    MIN_TRADES = 15

    def __init__(self, seed: int = 4242):
        self.seed = seed

    def evaluate(self, genome: Genome, panel: NormPanel) -> EvalResult:
        res = EvalResult(genome_id=genome.genome_id, market=genome.meta.market, fidelity="tier2",
                         seed=self.seed, snapshot_id=panel.snapshot_id)
        ok, issues = genome.typecheck()
        if not ok:
            res.error = "typecheck: " + "; ".join(issues); return res

        tf = panel.primary_tf
        close = panel.close_matrix(tf)
        high = panel.field_matrix("high", tf).reindex_like(close)
        low = panel.field_matrix("low", tf).reindex_like(close)
        atr = panel.field_matrix("atr_14", tf).reindex_like(close)
        if close.empty or close.shape[0] < 40:
            res.error = "insufficient_data"; return res

        feat_z: Dict[str, pd.DataFrame] = {}
        for node in genome.features:
            try:
                mat = F.compute(node.op, panel, node.args, tf).reindex(index=close.index, columns=close.columns)
                z = _time_z(mat)
                if z.notna().any().any():
                    feat_z[node.id] = z
            except Exception as e:
                res.summary.setdefault("feature_errors", []).append(f"{node.op}: {e}")
        if not feat_z:
            res.error = "no_valid_features"; return res

        sig = self._signal(genome, feat_z, close)

        r = genome.risk.args
        entry_thr = float(r.get("entry_thr", 0.6))
        sl_mult = float(r.get("sl_mult", 1.5)); tp_mult = float(r.get("tp_mult", 2.5))
        max_bars = int(r.get("max_bars", 16)); cost_stress = float(r.get("cost_stress", 1.0))
        mkt = MARKETS.get(genome.meta.market)
        cost = (round_trip_cost_bps(half_spread_bps=(mkt.half_spread_bps if mkt else 2.0),
                                    fee_bps_per_side=(mkt.fee_bps_per_side if mkt else 5.0),
                                    funding_rate=None) / 1e4) * cost_stress

        rets: List[float] = []
        times: List = []
        bars_held: List[int] = []
        sides: List[int] = []
        idx = close.index
        for sym in close.columns:
            c = close[sym].to_numpy(float); h = high[sym].to_numpy(float)
            lo = low[sym].to_numpy(float); a = atr[sym].to_numpy(float)
            s = sig[sym].to_numpy(float)
            for exit_i, held, ret, side in _sim_symbol(c, h, lo, a, s, entry_thr, sl_mult, tp_mult, max_bars, cost):
                rets.append(ret); times.append(idx[exit_i]); bars_held.append(held); sides.append(side)

        if len(rets) < self.MIN_TRADES:
            res.error = f"too_few_trades({len(rets)})"; return res

        order = np.argsort([pd.Timestamp(t).value for t in times])
        net = pd.Series([rets[i] for i in order], index=[times[i] for i in order])
        res.net_returns = net
        res.turnover = pd.Series(1.0, index=net.index)   # one round trip per trade
        res.summary = self._summarize(net, bars_held, tf)
        res.behavioral_descriptor = self._descriptor(bars_held, sides, genome)
        return res

    def _signal(self, genome: Genome, feat_z: Dict[str, pd.DataFrame], grid: pd.DataFrame) -> pd.DataFrame:
        direction = genome.signal.args.get("direction", "neutral")
        if genome.signal.op in ("gated_and", "gated_or"):
            thr = float(genome.signal.args.get("threshold", 0.5))
            use_or = genome.signal.op == "gated_or"
            short = direction == "short_bias"
            gate = None
            for z in feat_z.values():
                g = (z < -thr) if short else (z > thr)
                gate = g if gate is None else ((gate | g) if use_or else (gate & g))
            mat = gate.astype(float) if gate is not None else grid * 0.0
            return (-mat if short else mat).reindex(index=grid.index, columns=grid.columns).fillna(0.0)
        blended = np.tanh(sum(z.fillna(0.0) for z in feat_z.values()) / max(1, len(feat_z)))
        if direction == "long_bias":
            blended = blended.clip(lower=0.0)
        elif direction == "short_bias":
            blended = blended.clip(upper=0.0)
        return blended.reindex(index=grid.index, columns=grid.columns).fillna(0.0)

    def _summarize(self, net: pd.Series, bars_held: List[int], tf: str) -> dict:
        span_bars = 1
        if len(net) > 1:
            span_bars = max(1, (pd.Timestamp(net.index[-1]) - pd.Timestamp(net.index[0])).total_seconds()
                            / 60.0 / _tf_minutes(tf))
        years = max(1e-6, span_bars * _tf_minutes(tf) / 525600.0)
        tpy = len(net) / years
        mean = float(net.mean()); sd = float(net.std(ddof=1)) if len(net) > 1 else 0.0
        sharpe = (mean / sd * np.sqrt(tpy)) if sd > 0 else float("nan")
        curve = net.cumsum()
        return {
            "n_periods": int(len(net)), "n_trades": int(len(net)),
            "net_sharpe": sharpe, "ann_return": mean * tpy,
            "ann_vol": sd * np.sqrt(tpy),
            "max_dd": float((curve.cummax() - curve).max()) if len(curve) else float("nan"),
            "hit_rate": float((net > 0).mean()), "avg_trade_ret": mean,
            "avg_bars_held": float(np.mean(bars_held)) if bars_held else 0.0,
            "avg_turnover": 1.0, "trades": int(len(net)), "periods_per_year": tpy,
        }

    def _descriptor(self, bars_held: List[int], sides: List[int], genome: Genome) -> dict:
        avg_hold = float(np.mean(bars_held)) if bars_held else 0.0
        hold = ("scalp" if avg_hold <= 3 else "intraday" if avg_hold <= 10
                else "swing" if avg_hold <= 30 else "position")
        net_side = float(np.mean(sides)) if sides else 0.0
        expo = "long" if net_side > 0.2 else "short" if net_side < -0.2 else "both"
        return {"hold_bucket": hold, "turnover_bucket": "trade", "exposure_bucket": expo,
                "median_holding_bars": int(avg_hold), "phenotype": "directional",
                "complexity": genome.complexity()}


def _sim_symbol(c, h, lo, a, s, entry_thr, sl_mult, tp_mult, max_bars, cost) -> List[Tuple[int, int, float, int]]:
    """Triple-barrier path sim for one symbol. Non-overlapping; SL checked before TP
    (conservative on the intrabar ambiguity)."""
    trades: List[Tuple[int, int, float, int]] = []
    n = len(c)
    i = 0
    while i < n - 1:
        sv, av = s[i], a[i]
        if not (np.isfinite(sv) and np.isfinite(av)) or av <= 0 or abs(sv) < entry_thr or not np.isfinite(c[i]):
            i += 1
            continue
        side = 1 if sv > 0 else -1
        entry = c[i]
        sl = entry - side * sl_mult * av
        tp = entry + side * tp_mult * av
        exit_price = None
        j = i + 1
        bars = 0
        while j < n and bars < max_bars:
            hj, lj = h[j], lo[j]
            if side == 1:
                if lj <= sl:
                    exit_price = sl; break
                if hj >= tp:
                    exit_price = tp; break
            else:
                if hj >= sl:
                    exit_price = sl; break
                if lj <= tp:
                    exit_price = tp; break
            j += 1
            bars += 1
        if exit_price is None:
            j = min(j, n - 1)
            exit_price = c[j]
        ret = side * (exit_price - entry) / entry - cost
        trades.append((j, max(1, bars), float(ret), side))
        i = j + 1
    return trades
