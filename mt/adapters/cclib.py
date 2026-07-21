"""mt.adapters.cclib — the ONE in-process boundary to CC_Trading's pure library.

CC_Trading is the "library" market: its cost model, stationary bootstrap, and Deflated
Sharpe are the shared machinery every market's returns flow through (docs/01 §4, docs/10).
This module is the only place that puts CC_Trading's root on the mt process's sys.path,
so the crypto stack's top-level packages (core/xsec/backtest) enter the process in exactly
one controlled spot. FX/XAU are NEVER imported in-process — only via subprocess workers —
which is what keeps the namespace clash impossible here.

Every re-export has a pure local fallback so mt still runs (degraded) if CC_Trading moves.
"""
from __future__ import annotations

import sys
from typing import List

import numpy as np

from mt.config import LIBRARY_ROOT

_root = str(LIBRARY_ROOT)
if LIBRARY_ROOT.exists() and _root not in sys.path:
    sys.path.append(_root)   # append (not insert) — never shadow mt's own imports

# ─── cost model ──────────────────────────────────────────────────────────
try:
    from backtest.costs import round_trip_cost as _round_trip_cost  # type: ignore
    HAVE_CC_COSTS = True
except Exception:  # pragma: no cover - fallback path
    HAVE_CC_COSTS = False

    class _CB:
        def __init__(self, total): self.total_bps = total

    def _round_trip_cost(*, half_spread_bps, fee_bps_per_side=5.0, funding_rate=None,
                         holding_hours=8.0, side="BULL", funding_interval_hours=8.0, impact_bps=0.0):
        fee = 2.0 * fee_bps_per_side
        spread = 2.0 * half_spread_bps
        funding = 0.0 if funding_rate is None else float(funding_rate) * (holding_hours / funding_interval_hours) * 1e4
        return _CB(fee + spread + funding + impact_bps)


def round_trip_cost_bps(*, half_spread_bps: float, fee_bps_per_side: float = 5.0,
                        funding_rate=None, holding_hours: float = 8.0, impact_bps: float = 0.0) -> float:
    """Round-trip cost in bps via CC_Trading's shared model (docs/04 §3)."""
    cb = _round_trip_cost(half_spread_bps=half_spread_bps, fee_bps_per_side=fee_bps_per_side,
                          funding_rate=funding_rate, holding_hours=holding_hours, impact_bps=impact_bps)
    return float(cb.total_bps)


# ─── stationary bootstrap (Politis & Romano) ─────────────────────────────
try:
    from analysis.smc_monte_carlo import (  # type: ignore
        stationary_bootstrap_indices as _sb_indices,
        _optimal_block_length as _opt_block,
    )
    HAVE_CC_MC = True
except Exception:  # pragma: no cover
    HAVE_CC_MC = False

    def _opt_block(returns) -> int:
        r = np.asarray(returns, float)
        n = len(r)
        if n < 8:
            return 1
        ac = np.corrcoef(r[:-1], r[1:])[0, 1] if n > 2 else 0.0
        ac = 0.0 if not np.isfinite(ac) else abs(ac)
        return int(max(1, min(n // 2, round((n ** (1 / 3)) * (1 + 2 * ac)))))

    def _sb_indices(n, block_length, n_sims, rng):
        p = 1.0 / max(1, block_length)
        idx = np.empty((n_sims, n), dtype=int)
        for s in range(n_sims):
            i = int(rng.integers(n))
            for t in range(n):
                idx[s, t] = i
                if rng.random() < p:
                    i = int(rng.integers(n))
                else:
                    i = (i + 1) % n
        return idx


def bootstrap_drawdown(returns: List[float], n_sims: int = 5000, seed: int = 42) -> dict:
    """Stationary-block bootstrap of the return series → max-DD / CVaR distribution."""
    r = np.asarray([x for x in returns if np.isfinite(x)], float)
    if len(r) < 10:
        return {"n": int(len(r)), "error": "too_few_returns"}
    rng = np.random.default_rng(seed)
    block = _opt_block(r)
    curves = np.cumsum(r[_sb_indices(len(r), block, n_sims, rng)], axis=1)
    running_max = np.maximum.accumulate(curves, axis=1)
    max_dd = np.max(running_max - curves, axis=1)
    thr = float(np.percentile(max_dd, 95))
    tail = max_dd[max_dd >= thr]
    return {
        "n": int(len(r)), "block_length": int(block), "n_sims": int(n_sims),
        "max_dd_median": float(np.median(max_dd)),
        "max_dd_95": thr,
        "cvar_95": float(tail.mean()) if len(tail) else thr,
        "engine": "cc_trading" if HAVE_CC_MC else "mt_fallback",
    }


# ─── Deflated Sharpe (Bailey & López de Prado) ───────────────────────────
try:
    from SMC_ML.smc_ml_diagnostics import compute_deflated_sharpe as _cc_dsr  # type: ignore
    HAVE_CC_DSR = True
except Exception:  # pragma: no cover
    HAVE_CC_DSR = False
    _cc_dsr = None


def deflated_sharpe(returns: List[float], n_trials: int, annualization_factor: float = 365.0) -> dict:
    """Deflated Sharpe via CC_Trading's implementation (the multiple-testing firewall,
    docs/05 G4). `n_trials` is the honest family size from the Result Ledger."""
    r = [float(x) for x in returns if np.isfinite(x)]
    if len(r) < 10:
        return {"error": "too_few_returns", "n": len(r)}
    if HAVE_CC_DSR:
        out = _cc_dsr(r, n_trials=n_trials, annualization_factor=annualization_factor)
        out["engine"] = "cc_trading"
        return out
    # minimal fallback (used only if CC_Trading is unavailable)
    from scipy import stats
    arr = np.asarray(r)
    sr = arr.mean() / arr.std(ddof=1) if arr.std(ddof=1) > 0 else 0.0
    n = len(arr)
    sk = float(stats.skew(arr)); ku = float(stats.kurtosis(arr, fisher=True))
    se = np.sqrt(max(1e-9, (1 - sk * sr + (ku) / 4.0 * sr ** 2) / (n - 1)))
    emax = np.sqrt(2 * np.log(max(2, n_trials))) * se
    z = (sr - emax) / se
    p = 1.0 - float(stats.norm.cdf(z))
    return {"raw_sharpe": float(sr), "sr_annualized": float(sr * np.sqrt(annualization_factor)),
            "expected_max_sr": float(emax), "dsr_z_score": float(z), "dsr_pvalue": float(p),
            "is_significant": bool(p < 0.05), "engine": "mt_fallback", "n_trials": int(n_trials)}
