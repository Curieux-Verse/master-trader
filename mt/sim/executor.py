"""mt.sim.executor — Tier-1 vectorized, cost-aware, genome-driven backtest.

Mirrors CC_Trading's backtest/engine.py (non-overlapping horizon, rank-bucket book,
cost-on-turnover) but the features, weights, signal logic, and horizon come from the
*genome* rather than being hard-coded — and it runs on any market's NormPanel. Fitness is
always the NET, post-cost return (docs/04 §3). The one cost model is CC_Trading's
round_trip_cost via mt.adapters.cclib.
"""
from __future__ import annotations

from typing import Dict, Tuple

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


class Tier1Executor:
    def __init__(self, seed: int = 4242):
        self.seed = seed

    def evaluate(self, genome: Genome, panel: NormPanel) -> EvalResult:
        gid = genome.genome_id
        market = genome.meta.market
        res = EvalResult(genome_id=gid, market=market, seed=self.seed, snapshot_id=panel.snapshot_id)

        ok, issues = genome.typecheck()
        if not ok:
            res.error = "typecheck: " + "; ".join(issues)
            return res

        tf = panel.primary_tf
        close = panel.close_matrix(tf)
        if close.empty or close.shape[0] < 30:
            res.error = "insufficient_data"
            return res

        # ── features → z-scored matrices on the common grid ──────────────
        feat_z: Dict[str, pd.DataFrame] = {}
        for node in genome.features:
            try:
                mat = F.compute(node.op, panel, node.args, tf).reindex(index=close.index, columns=close.columns)
                z = F.zscore_rows(mat)
                if z.notna().any().any():
                    feat_z[node.id] = z
            except Exception as e:                       # a broken feature is skipped, not fatal
                res.summary.setdefault("feature_errors", []).append(f"{node.op}: {e}")
        if not feat_z:
            res.error = "no_valid_features"
            return res

        mode, matrix = self._signal(genome, feat_z, close)

        # ── non-overlapping horizon backtest ─────────────────────────────
        horizon = int(genome.risk.args.get("horizon", 6))
        cost_stress = float(genome.risk.args.get("cost_stress", 1.0))
        mkt = MARKETS.get(market)
        cost_bps = round_trip_cost_bps(
            half_spread_bps=(mkt.half_spread_bps if mkt else 2.0),
            fee_bps_per_side=(mkt.fee_bps_per_side if mkt else 5.0),
            funding_rate=None,
        )
        cost_per_turnover = (cost_bps / 1e4) * cost_stress

        top_frac = float(genome.sizing.args.get("top_frac", 0.10))
        gross = float(genome.sizing.args.get("gross", 1.0))
        per_name_cap = float(genome.sizing.args.get("per_name_cap", 0.10))

        # numpy-vectorized backtest loop (matrix/fwd aligned to close grid; ~20× faster than .loc)
        idx = close.index
        mat_np = matrix.reindex(index=close.index, columns=close.columns).to_numpy()
        fwd_np = (close.shift(-horizon) / close - 1.0).to_numpy()

        dates, nets, grosses, turns, net_expo, names_traded = [], [], [], [], [], []
        prev_w = None
        for pos in range(0, len(idx) - horizon, horizon):
            row = mat_np[pos]; fr = fwd_np[pos]
            valid = np.isfinite(fr)
            if valid.sum() < 4:
                continue
            w = self._weights_np(mode, row, valid, top_frac, gross, per_name_cap)
            if not np.any(w):
                continue
            gross_ret = float(np.sum(w * np.where(valid, fr, 0.0)))
            turnover = float(np.abs(w).sum()) if prev_w is None else float(np.abs(w - prev_w).sum())
            nets.append(gross_ret - turnover * cost_per_turnover)
            grosses.append(gross_ret)
            turns.append(turnover)
            net_expo.append(float(w.sum()))
            names_traded.append(int(np.count_nonzero(w)))
            dates.append(idx[pos])
            prev_w = w

        if not dates:
            res.error = "no_rebalance_periods"
            return res

        net = pd.Series(nets, index=dates)
        # optional vol-target rescaling (docs/02 §3): linear in weights ⇒ scale the series
        if genome.sizing.op == "vol_target":
            net = self._vol_target(net, genome, tf, horizon)

        res.net_returns = net
        res.turnover = pd.Series(turns, index=dates)
        res.summary = self._summarize(net, pd.Series(grosses, index=dates), pd.Series(turns, index=dates),
                                      cost_per_turnover, tf, horizon, names_traded)
        res.behavioral_descriptor = self._descriptor(horizon, turns, net_expo, genome)
        return res

    # ── signal combination ───────────────────────────────────────────────
    def _signal(self, genome: Genome, feat_z: Dict[str, pd.DataFrame], grid: pd.DataFrame) -> Tuple[str, pd.DataFrame]:
        direction = genome.signal.args.get("direction", "neutral")
        if genome.signal.op in ("gated_and", "gated_or"):
            thr = float(genome.signal.args.get("threshold", 0.5))
            use_or = genome.signal.op == "gated_or"
            short = direction == "short_bias"
            gate = None
            for z in feat_z.values():
                g = (z < -thr) if short else (z > thr)
                if gate is None:
                    gate = g
                else:
                    gate = (gate | g) if use_or else (gate & g)
            mat = gate.astype(float) if gate is not None else grid * 0.0
            if short:
                mat = -mat
            return "gated", mat.reindex(index=grid.index, columns=grid.columns).fillna(0.0)

        # weighted_blend: equal-weight z-score sum (the honest v1 blend)
        total = sum(z.fillna(0.0) for z in feat_z.values())
        counts = sum(z.notna().astype(float) for z in feat_z.values())
        alpha = total / counts.replace(0, np.nan)
        if direction == "short_bias":
            alpha = -alpha
        return "dense", alpha

    # ── weighting ─────────────────────────────────────────────────────────
    def _weights_np(self, mode: str, row: np.ndarray, valid: np.ndarray,
                    top_frac: float, gross: float, per_name_cap: float) -> np.ndarray:
        """Numpy rank-bucket / gated weights for one rebalance row (the hot path)."""
        w = np.zeros(len(row))
        finite = valid & np.isfinite(row)
        if mode == "gated":
            active = finite & (row != 0.0)
            k = int(active.sum())
            if k == 0:
                return w
            w[active] = np.sign(row[active]) * (gross / k)
            return np.clip(w, -per_name_cap, per_name_cap)
        # dense: long top-frac / short bottom-frac, dollar-neutral (engine.rank_bucket_weights)
        fin_idx = np.where(finite)[0]
        m = len(fin_idx)
        if m < 4:
            return w
        k = max(1, int(m * top_frac))
        order = fin_idx[np.argsort(row[fin_idx])]        # ascending by alpha
        w[order[-k:]] = (gross / 2.0) / k                # longs (top)
        w[order[:k]] = -(gross / 2.0) / k                # shorts (bottom)
        return np.clip(w, -per_name_cap, per_name_cap)

    def _vol_target(self, net: pd.Series, genome: Genome, tf: str, horizon: int) -> pd.Series:
        target = float(genome.sizing.args.get("target_ann_vol", 0.15))
        ppy = (525600.0 / _tf_minutes(tf)) / horizon
        est = net.std(ddof=1) * np.sqrt(ppy)
        if not np.isfinite(est) or est <= 0:
            return net
        k = float(np.clip(target / est, 0.1, 3.0))
        return net * k

    # ── summary + descriptor ──────────────────────────────────────────────
    def _summarize(self, net, gross, turnover, cost_per_turnover, tf, horizon, names_traded) -> dict:
        ppy = (525600.0 / _tf_minutes(tf)) / horizon
        mean = float(net.mean()); sd = float(net.std(ddof=1)) if len(net) > 1 else 0.0
        sharpe = (mean / sd * np.sqrt(ppy)) if sd > 0 else float("nan")
        curve = net.cumsum()
        max_dd = float((curve.cummax() - curve).max()) if len(curve) else float("nan")
        return {
            "n_periods": int(len(net)),
            "net_sharpe": sharpe,
            "sharpe_pp": (mean / sd) if sd > 0 else float("nan"),   # per-observation (for ledger σ_SR)
            "ann_return": mean * ppy,
            "ann_vol": sd * np.sqrt(ppy),
            "max_dd": max_dd,
            "hit_rate": float((net > 0).mean()),
            "avg_turnover": float(turnover.mean()),
            "avg_cost_drag": float(turnover.mean() * cost_per_turnover),
            "trades": int(np.sum(names_traded)),
            "periods_per_year": ppy,
        }

    def _descriptor(self, horizon, turns, net_expo, genome: Genome) -> dict:
        hold = ("scalp" if horizon <= 2 else "intraday" if horizon <= 6
                else "swing" if horizon <= 24 else "position")
        avg_turn = float(np.mean(turns)) if turns else 0.0
        turn_bucket = "low" if avg_turn < 0.5 else "med" if avg_turn < 1.5 else "high"
        net_e = float(np.mean(net_expo)) if net_expo else 0.0
        expo = "neutral" if abs(net_e) < 0.1 else ("long" if net_e > 0 else "short")
        return {
            "hold_bucket": hold, "turnover_bucket": turn_bucket, "exposure_bucket": expo,
            "median_holding_bars": int(horizon), "avg_turnover": avg_turn, "net_exposure": net_e,
            "complexity": genome.complexity(),
        }
