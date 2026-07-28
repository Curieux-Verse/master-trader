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
from typing import List, Optional

import numpy as np

from mt.config import LIBRARY_ROOT

_root = str(LIBRARY_ROOT)
if LIBRARY_ROOT.exists() and _root not in sys.path:
    sys.path.append(_root)   # append (not insert) — never shadow mt's own imports

# A per-observation Sharpe this large is not a strategy — it is a (near-)constant return series
# whose std is floating-point noise, not zero (e.g. std≈2e-19 for a literal constant), so the
# `std==0` / `sigma<1e-12` guards miss it and it reports an astronomical, spurious "significance".
# Real per-bar Sharpes are ≲0.5; even a legendary one is <1. 50 is ~100× the strongest test edge,
# so this can never reject a real strategy — it only rejects numerical degeneracy (docs/14 review).
MAX_SANE_SR_PP = 50.0

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
    # compounded equity per bootstrap path → FRACTIONAL drawdown (peak-to-trough / peak), the
    # same definition the executor summary reports; cumsum of simple returns understates DD.
    # A single-bar return ≤ −100% is RUIN: floor per-bar growth at 0 so equity can't go negative
    # (which otherwise makes (peak−equity)/peak produce NaN at r=−1 or values >1 at r<−1). Once
    # equity hits 0 it stays 0 → drawdown is 100%. Result is always in [0,1]; benign (no-ruin) paths
    # are unchanged since the clamp is then a no-op (this keeps the 0.60 gate threshold calibrated).
    growth = np.maximum(1.0 + r[_sb_indices(len(r), block, n_sims, rng)], 0.0)
    equity = np.cumprod(growth, axis=1)
    running_max = np.maximum.accumulate(equity, axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        dd = np.where(running_max > 0, (running_max - equity) / running_max, 1.0)
    max_dd = np.max(dd, axis=1)
    thr = float(np.percentile(max_dd, 95))
    tail = max_dd[max_dd >= thr]
    return {
        "n": int(len(r)), "block_length": int(block), "n_sims": int(n_sims),
        "max_dd_median": float(np.median(max_dd)),
        "max_dd_95": thr,
        "cvar_95": float(tail.mean()) if len(tail) else thr,
        "engine": "cc_trading" if HAVE_CC_MC else "mt_fallback",
    }


def reality_check(returns: List[float], n_trials: int = 1, n_sims: int = 2000, seed: int = 42) -> dict:
    """Non-parametric bootstrap Reality Check — an INDEPENDENT multiple-testing firewall next to
    the (parametric) Deflated Sharpe. White (2000) / Hansen SPA in spirit: stationary-block
    bootstrap the return series under the null of zero mean, get the single-trial bootstrap
    p-value that the Sharpe > 0 is luck, then adjust it for the family size N with a Šidák FWER
    correction. Because it makes NO distributional assumption about the Sharpe estimator, it
    catches edges that look significant parametrically but are driven by a few lucky blocks."""
    r = np.asarray([x for x in returns if np.isfinite(x)], float)
    T = len(r)
    if T < 10 or r.std(ddof=1) == 0:
        return {"error": "too_few_returns", "n": int(T)}
    sr = float(r.mean() / r.std(ddof=1))
    if not np.isfinite(sr) or abs(sr) > MAX_SANE_SR_PP:   # near-constant series → spurious huge Sharpe
        return {"error": "degenerate_sharpe", "n": int(T), "raw_sharpe": round(sr, 5)}
    rng = np.random.default_rng(seed)
    block = _opt_block(r)
    idx = _sb_indices(T, block, n_sims, rng)
    paths = (r - r.mean())[idx]                                # recenter → the null (zero mean)
    mu = paths.mean(axis=1)
    sd = paths.std(axis=1, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        null_sr = np.where(sd > 0, mu / sd, 0.0)
    p_single = float((np.sum(null_sr >= sr) + 1) / (n_sims + 1))   # one-sided, +1 smoothing
    N = max(1, int(n_trials))
    p_fwer = float(1.0 - (1.0 - p_single) ** N)                # Šidák family-wise adjustment
    return {
        "n": int(T), "raw_sharpe": round(sr, 5), "block_length": int(block),
        "p_single": round(p_single, 5), "n_trials": N, "p_fwer": round(p_fwer, 5),
        "is_significant": bool(sr > 0 and p_fwer < 0.05),
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


# Below this family size the E[max SR] deflation is modest, so the null-dispersion fallback
# (σ_SR ≈ sr_se) is safe. At or above it, an honest cross-trial σ_SR (from the ledger) is required
# — without one, the fallback under-deflates for autocorrelated/structured returns and would
# false-admit a best-of-N selection overfit, so G4 fails closed (docs/14 cold-ledger hardening).
DSR_RELIABLE_N_MAX = 5


def sharpe_std_error(returns: List[float]) -> Optional[float]:
    """Standard error of the per-observation Sharpe (Mertens/Bailey, skew+kurtosis adjusted).

    This is the null sampling spread of a Sharpe estimated on THIS series, ≈1/√T. It is the
    statistically correct dispersion for a max-statistic computed on data that played no part in
    selection (Stage B), and it is the floor below which the pooled ledger σ_SR must never be
    trusted (Stage A) — see `deflated_sharpe(sigma_floor=…)`."""
    from scipy.stats import skew, kurtosis
    r = np.asarray([float(x) for x in returns if np.isfinite(x)], dtype=float)
    T = len(r)
    if T < 10:
        return None
    sigma = float(r.std(ddof=1))
    if sigma < 1e-12:
        return None
    sr = float(r.mean()) / sigma
    if not np.isfinite(sr) or abs(sr) > MAX_SANE_SR_PP:
        return None
    s = float(skew(r)); g4 = float(kurtosis(r, fisher=True)) + 3.0
    return float(np.sqrt(max(1e-12, (1.0 - s * sr + ((g4 - 1.0) / 4.0) * sr ** 2) / (T - 1))))


def deflated_sharpe(returns: List[float], n_trials: int, annualization_factor: float = 365.0,
                    sr_trial_std: float = None, sigma_floor: bool = False) -> dict:
    """Correct Deflated Sharpe — the multiple-testing firewall (docs/05 G4).

    `n_trials` is the honest family size from the Result Ledger; `sr_trial_std` is the std of
    per-observation Sharpes across those trials (the ledger's dispersion) — the σ_SR that
    scales the deflation threshold. A candidate is significant iff its Sharpe clears the
    expected maximum Sharpe of N lucky trials.

    When `sr_trial_std` is missing (a cold ledger) the deflation is only trustworthy for a small
    family (N ≤ DSR_RELIABLE_N_MAX); beyond that the result is flagged `reliable=False` and
    `is_significant` is forced False — the caller must not admit or high-water-mark it until the
    ledger warms up (Bailey & López de Prado: record all trials AND their dispersion).
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
    if not np.isfinite(sr) or abs(sr) > MAX_SANE_SR_PP:   # near-constant series (std≈float noise) →
        return {"error": "degenerate_sharpe", "n": int(T)}   # spurious huge Sharpe; not a real edge
    s = float(skew(r)); ek = float(kurtosis(r, fisher=True)); g4 = ek + 3.0
    sr_se = float(np.sqrt(max(1e-12, (1.0 - s * sr + ((g4 - 1.0) / 4.0) * sr ** 2) / (T - 1))))
    have_ledger_sigma = bool(sr_trial_std and sr_trial_std > 0)
    sigma_sr = float(sr_trial_std) if have_ledger_sigma else sr_se
    # T-AWARENESS. The ledger's σ_SR is pooled over trials whose horizons differ by an order of
    # magnitude, and T = bars/horizon — measured spread within one candidate pool: 27 … 2066
    # observations. The null sampling sd of a Sharpe is 1/√T, so a single pooled σ_SR is right at
    # one horizon and wrong at every other; where it falls BELOW this candidate's own sampling
    # error it under-deflates, which is how an in-sample best-z of +2.7 turns into a negative
    # out-of-sample z. Never deflate by less than the candidate's own standard error.
    sigma_floored = False
    if sigma_floor and have_ledger_sigma and sigma_sr < sr_se:
        sigma_sr = sr_se
        sigma_floored = True

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
    reliable = bool(have_ledger_sigma or N <= DSR_RELIABLE_N_MAX)
    return {
        "n_returns": int(T), "raw_sharpe": round(sr, 5),
        "sr_annualized": round(sr * float(np.sqrt(min(T, annualization_factor))), 5),
        "skewness": round(s, 5), "excess_kurtosis": round(ek, 5), "sr_std_error": round(sr_se, 6),
        "sigma_sr": round(sigma_sr, 6),
        "sigma_sr_source": ("sr_se_floor" if sigma_floored else
                            ("ledger" if have_ledger_sigma else "fallback")),
        "n_trials": N, "expected_max_sr": round(e_max, 5), "reliable": reliable,
        "deflated_sharpe": round(dsr, 5), "dsr_z_score": round(z, 5), "dsr_pvalue": round(dsr_pvalue, 5),
        "is_significant": bool(dsr_pvalue < 0.05 and reliable), "haircut_pct": round(haircut, 2),
        "engine": "mt_dsr",
    }
