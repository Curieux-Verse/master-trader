"""mt.gauntlet.multipletest — honest family-size accounting and the two-stage error control.

Two distinct jobs live here, and keeping them apart is the whole point (docs/15):

  • **K_eff** — how many *effectively independent* trials a correlated family represents.
    The naive equicorrelation formula N/(1+(N−1)ρ̄) is known to fail exactly where we need
    it: it reads only the SHAPE of the correlation spectrum, not its scale, so adding
    duplicate strategies barely moves it (our production brain reported ρ̄=0.00998 → N_eff=100
    while its own top-20 were near-clones). We instead invert an extreme-value identity:
    a family whose maximum squared z-score behaves like the max of `x` i.i.d. χ²₁ variables
    IS, for selection-bias purposes, `x` independent trials. That number responds correctly
    to duplication because duplication lowers the expected maximum.

  • **Error control at the right stage.** Exploration and confirmation are different
    statistical regimes (Harvey & Liu 2020; standard multiple-comparison practice): FWER
    control (what the Deflated Sharpe does) is a *confirmatory* tool and is far too
    conservative to screen with — it guards against a single false positive at the cost of
    many missed discoveries. Screening therefore uses Benjamini–Hochberg–Yekutieli FDR,
    which is valid under ARBITRARY dependence between trials (the BY `c(m)` correction) —
    essential here, since our trials share features by construction.

Nothing in this module relaxes the confirmatory bar. It makes the exploratory bar honest
so that the search has a signal to learn from, and hands a SMALL, pre-registered family to
the confirmatory stage where the Deflated Sharpe still rules.
"""
from __future__ import annotations

import math
from typing import List, Optional, Sequence

import numpy as np

# Integration grid for E[max χ²₁]. P(χ²₁ > 80) ≈ 4e-19, so truncating at 80 is exact to
# double precision even for families of 1e6 trials.
_T_GRID = np.linspace(0.0, 80.0, 4001)
_MIN_SIGS_FOR_KEFF = 8          # below this the correlation matrix is noise, not structure


def _chi2_1_cdf(t: np.ndarray) -> np.ndarray:
    """CDF of χ²₁ = erf(sqrt(t/2)) — closed form, so no scipy dependency in the hot path."""
    from scipy.special import erf
    return erf(np.sqrt(np.maximum(t, 0.0) / 2.0))


_F_GRID = _chi2_1_cdf(_T_GRID)


def expected_max_chi2(x: float) -> float:
    """E[max of `x` i.i.d. χ²₁ draws], for REAL x ≥ 1.

    Via the survival identity E[max] = ∫₀^∞ (1 − F(t)^x) dt. Defined for non-integer x, and
    strictly increasing in x — which is what lets us invert it to get an effective count."""
    x = max(1.0, float(x))
    with np.errstate(divide="ignore", invalid="ignore"):
        surv = 1.0 - np.power(_F_GRID, x)
    return float(np.trapezoid(surv, _T_GRID))


def _invert_expected_max(target: float, hi: float) -> float:
    """Smallest x ≥ 1 whose E[max of x χ²₁] equals `target` (bisection; E is monotone in x)."""
    lo = 1.0
    if target <= expected_max_chi2(lo):
        return 1.0
    if target >= expected_max_chi2(hi):
        return float(hi)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if expected_max_chi2(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def independence_ratio(signatures: Sequence[np.ndarray], n_sims: int = 4000,
                       seed: int = 7) -> Optional[float]:
    """Fraction of a correlated trial sample that behaves as independent, in [1/k, 1].

    `signatures` are standardized P&L-path signatures (one per trial). We build their
    correlation matrix Σ, Monte-Carlo E[max_i z_i²] for z ~ N(0, Σ), and invert the χ²₁
    extreme-value curve to get K_eff. Returning a RATIO (not a count) is what lets the caller
    scale a bounded sample up to the full ledger without re-correlating 46,843 series."""
    sigs = [np.asarray(s, float) for s in signatures if s is not None and len(s) >= 8]
    sigs = [s for s in sigs if np.isfinite(s).all() and s.std() > 0]
    k = len(sigs)
    if k < _MIN_SIGS_FOR_KEFF:
        return None
    m = min(s.size for s in sigs)
    X = np.vstack([s[:m] for s in sigs])
    with np.errstate(invalid="ignore", divide="ignore"):
        C = np.corrcoef(X)
    if not np.isfinite(C).all():
        C = np.nan_to_num(C, nan=0.0, posinf=0.0, neginf=0.0)
        np.fill_diagonal(C, 1.0)
    # DEBIAS (Bickel–Levina hard thresholding). Signatures are short (24 buckets), so two
    # INDEPENDENT trials still show a sample correlation of order 1/√(m−1) ≈ 0.21 by chance.
    # Left uncorrected that noise lowers E[max z²], lowers K_eff, and therefore UNDER-deflates
    # the Sharpe — the permissive direction, the one we must never drift in.
    # HARD threshold, not soft: soft-shrinking would also drag a genuine ρ≈1.0 duplicate pair
    # down to ≈0.79 and stop near-clones collapsing (measured: K_eff 1 → 6, i.e. it would break
    # the very case this estimator exists to catch). Zeroing sub-noise entries instead leaves
    # true co-movement exactly intact, and any weak-but-real correlation it discards only pushes
    # K_eff UP — more deflation, the safe direction.
    noise = 2.0 / math.sqrt(max(2, m - 1))
    off = ~np.eye(k, dtype=bool)
    C[off] = np.where(np.abs(C[off]) > noise, C[off], 0.0)
    # Nearest-PSD nudge: clip negative eigenvalues, then renormalize to a correlation matrix.
    w, V = np.linalg.eigh(C)
    C = V @ np.diag(np.clip(w, 1e-10, None)) @ V.T
    d = np.sqrt(np.clip(np.diag(C), 1e-12, None))
    C = C / np.outer(d, d)
    try:
        L = np.linalg.cholesky(C + 1e-10 * np.eye(k))
    except np.linalg.LinAlgError:
        return None
    rng = np.random.default_rng(seed)
    z = L @ rng.standard_normal((k, int(n_sims)))
    e_max = float(np.mean(np.max(z ** 2, axis=0)))
    k_eff = _invert_expected_max(e_max, hi=float(k))
    return float(min(1.0, max(1.0 / k, k_eff / k)))


def effective_trials(n_total: int, signatures: Sequence[np.ndarray] = (),
                     rho: Optional[float] = None) -> dict:
    """The family size the Deflated Sharpe should actually be given.

    Primary estimator is the EVT independence ratio measured on a sample of trial signatures,
    scaled to the full ledger. Falls back to the equicorrelation formula (and finally to raw N)
    when there is not enough correlation structure to measure. Always reports which estimator
    ran, because silently switching the deflation basis would make z incomparable over time."""
    n_total = max(1, int(n_total))
    ratio = independence_ratio(signatures) if len(signatures) >= _MIN_SIGS_FOR_KEFF else None
    if ratio is not None:
        n_eff = int(max(1, min(n_total, round(ratio * n_total))))
        return {"n_eff": n_eff, "method": "evt", "independence_ratio": round(ratio, 5),
                "n_total": n_total}
    if rho and rho > 0 and n_total > 1:
        n_eff = int(max(1, round(n_total / (1.0 + (n_total - 1) * float(rho)))))
        return {"n_eff": n_eff, "method": "equicorrelation", "rho": round(float(rho), 5),
                "n_total": n_total}
    return {"n_eff": n_total, "method": "raw", "n_total": n_total}


# ─── Stage-A screening: Benjamini–Hochberg–Yekutieli FDR ────────────────────
def bhy_threshold(pvalues: Sequence[float], q: float = 0.10) -> Optional[float]:
    """Largest p that is still a discovery at false-discovery-rate `q`, under ARBITRARY
    dependence (the Yekutieli c(m)=Σ1/i correction — required because our trials share
    features and are therefore not independent or positively-regression-dependent).

    Returns None when nothing in the batch is a discovery. This is the EXPLORATORY bar: it
    accepts that a known fraction `q` of promotions are false, in exchange for not discarding
    the true positives that FWER control would bury (Harvey & Liu 2020)."""
    p = np.asarray([x for x in pvalues if x is not None and np.isfinite(x)], dtype=float)
    m = p.size
    if m == 0:
        return None
    p = np.sort(np.clip(p, 0.0, 1.0))
    c_m = float(np.sum(1.0 / np.arange(1, m + 1)))          # harmonic number H_m
    crit = (np.arange(1, m + 1) / (m * c_m)) * float(q)
    below = np.nonzero(p <= crit)[0]
    if below.size == 0:
        return None
    return float(p[below[-1]])


def fdr_discoveries(pvalues: Sequence[float], q: float = 0.10) -> np.ndarray:
    """Boolean mask of which p-values are BHY discoveries at rate `q` (order preserved)."""
    thr = bhy_threshold(pvalues, q)
    arr = np.asarray([np.nan if x is None else x for x in pvalues], dtype=float)
    if thr is None:
        return np.zeros(arr.shape, dtype=bool)
    return np.nan_to_num(arr, nan=1.0) <= thr


def sharpe_pvalue(sharpe_pp: Optional[float], n_periods: Optional[int]) -> Optional[float]:
    """One-sided p-value that a SINGLE strategy's per-observation Sharpe > 0, with no
    multiple-testing penalty at all. This is the N-INDEPENDENT quantity Stage A ranks on —
    the whole reason a child can be compared to its parent without the ledger's growth
    contaminating the comparison. t = SR·√T, normal approximation (T is large here)."""
    if sharpe_pp is None or n_periods is None:
        return None
    try:
        sr = float(sharpe_pp); t_obs = int(n_periods)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(sr) or t_obs < 2:
        return None
    from scipy.stats import norm
    return float(1.0 - norm.cdf(sr * math.sqrt(t_obs)))
