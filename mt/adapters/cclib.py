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
# NOTE: mt implements DSR itself rather than delegating to CC_Trading's
# SMC_ML.compute_deflated_sharpe. That function computes the multiple-testing threshold as
# E[max SR] = sqrt(2·ln N) WITHOUT scaling by the SR standard error σ_SR, which for a
# per-observation-Sharpe return series (~0.05–0.5) makes the bar ~30× too high — it would
# reject every realistic edge, so the archive could never admit anything. The correct
# deflation scales the threshold by σ_SR (Bailey & López de Prado 2014, eq. 6). We estimate
# σ_SR from the Result Ledger's cross-trial Sharpe dispersion when available, else from the
# candidate's own SR standard error (the √(1/T) proxy). CC_Trading's version is retained for
# reference/cross-checks only.
try:
    from SMC_ML.smc_ml_diagnostics import compute_deflated_sharpe as cc_compute_deflated_sharpe  # type: ignore
    HAVE_CC_DSR = True
except Exception:  # pragma: no cover
    HAVE_CC_DSR = False
    cc_compute_deflated_sharpe = None


def deflated_sharpe(returns: List[float], n_trials: int, annualization_factor: float = 365.0,
                    sr_trial_std: float = None) -> dict:
    """Correct Deflated Sharpe — the multiple-testing firewall (docs/05 G4).

    `n_trials` is the honest family size from the Result Ledger; `sr_trial_std` is the std of
    per-observation Sharpes across those trials (the ledger's dispersion) — the σ_SR that
    scales the deflation threshold. A candidate is significant iff its Sharpe clears the
    expected maximum Sharpe of N lucky trials.
    """
    from scipy.stats import norm, skew, kurtosis
    r = np.asarray([float(x) for x in returns if np.isfinite(x)], dtype=float)
    T = len(r)
    if T < 10:
        return {"error": "too_few_returns", "n": int(T)}
    mu = float(r.mean()); sigma = float(r.std(ddof=1))
    if sigma < 1e-12:
        return {"error": "zero_variance"}
    sr = mu / sigma                                   # per-observation Sharpe
    s = float(skew(r)); ek = float(kurtosis(r, fisher=True)); g4 = ek + 3.0
    sr_se = float(np.sqrt(max(1e-12, (1.0 - s * sr + ((g4 - 1.0) / 4.0) * sr ** 2) / (T - 1))))
    sigma_sr = float(sr_trial_std) if (sr_trial_std and sr_trial_std > 0) else sr_se

    N = max(1, int(n_trials))
    if N > 1:                                          # Bailey & López de Prado E[max SR]
        gamma = 0.5772156649
        z1 = float(norm.ppf(1.0 - 1.0 / N))
        z2 = float(norm.ppf(1.0 - 1.0 / (N * np.e)))
        e_max = sigma_sr * ((1.0 - gamma) * z1 + gamma * z2)
    else:
        e_max = 0.0

    z = (sr - e_max) / sr_se
    dsr = float(norm.cdf(z))
    dsr_pvalue = float(1.0 - dsr)                      # probability the edge is a multiple-testing artifact
    haircut = float(max(0.0, (e_max / abs(sr) - 1.0)) * 100.0) if abs(sr) > 1e-10 else 0.0
    return {
        "n_returns": int(T), "raw_sharpe": round(sr, 5),
        "sr_annualized": round(sr * float(np.sqrt(min(T, annualization_factor))), 5),
        "skewness": round(s, 5), "excess_kurtosis": round(ek, 5), "sr_std_error": round(sr_se, 6),
        "sigma_sr": round(sigma_sr, 6), "n_trials": N, "expected_max_sr": round(e_max, 5),
        "deflated_sharpe": round(dsr, 5), "dsr_z_score": round(z, 5), "dsr_pvalue": round(dsr_pvalue, 5),
        "is_significant": bool(dsr_pvalue < 0.05), "haircut_pct": round(haircut, 2), "engine": "mt_dsr",
    }
