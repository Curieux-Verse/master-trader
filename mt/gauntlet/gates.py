"""mt.gauntlet.gates — the individual gates. Any enforced failure rejects the candidate.

Ordered cheap→expensive by the runner so most candidates die on the cheap rungs
(successive-halving over the gauntlet). No gate compensates for another (docs/05 §2).
Gates that need to re-evaluate the genome (G3 CPCV, G6 transfer) run only when a
GauntletContext with an evaluator is supplied; otherwise they report "deferred".
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np
import pandas as pd

from mt.adapters.cclib import deflated_sharpe, bootstrap_drawdown, round_trip_cost_bps, reality_check
from mt.config import MARKETS
from mt.gauntlet import cpcv

MIN_PERIODS = 20
MAX_SINGLE_PERIOD_SHARE = 0.50
DSR_PVALUE_MAX = 0.05
MAX_DD_95_CAP = 0.60
PBO_MAX = 0.50
MAX_ARCHIVE_CORR = 0.90


@dataclass
class GateResult:
    name: str
    status: str                  # "pass" | "fail" | "deferred"
    stats: Dict = field(default_factory=dict)
    reason: str = ""

    @property
    def passed(self) -> bool:
        return self.status in ("pass", "deferred")

    @property
    def enforced(self) -> bool:
        return self.status in ("pass", "fail")


def _sharpe(x: np.ndarray) -> float:
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    sd = x.std(ddof=1) if len(x) > 1 else 0.0
    return float(x.mean() / sd) if sd > 0 else float("nan")


# ── G1 sanity ─────────────────────────────────────────────────────────────
def g1_sanity(net: pd.Series) -> GateResult:
    n = int(len(net))
    if n < MIN_PERIODS:
        return GateResult("G1_sanity", "fail", {"n_periods": n}, f"too few periods ({n} < {MIN_PERIODS})")
    total_abs = float(net.abs().sum())
    share = float(net.abs().max() / total_abs) if total_abs > 0 else 1.0
    if share > MAX_SINGLE_PERIOD_SHARE:
        return GateResult("G1_sanity", "fail", {"single_period_share": share},
                          f"one period is {share:.0%} of gross P&L")
    if not np.isfinite(_sharpe(net.to_numpy())):
        return GateResult("G1_sanity", "fail", {}, "degenerate return series")
    return GateResult("G1_sanity", "pass", {"n_periods": n, "single_period_share": round(share, 3)})


# ── G2 in-sample / out-of-sample degradation (cheap) ───────────────────────
def g2_oos_degradation(net: pd.Series) -> GateResult:
    n = len(net)
    if n < MIN_PERIODS:
        return GateResult("G2_oos", "fail", {"n": n}, "too few periods for IS/OOS split")
    half = n // 2
    is_mean = float(net.iloc[:half].mean()); oos_mean = float(net.iloc[half:].mean())
    # a strategy that only shines in-sample dies here
    passed = not (is_mean > 0 and oos_mean < 0.10 * is_mean)
    reason = "" if passed else f"OOS mean {oos_mean:.2e} collapses vs IS {is_mean:.2e}"
    return GateResult("G2_oos", "pass" if passed else "fail",
                      {"is_mean": is_mean, "oos_mean": oos_mean}, reason)


# ── G4 Deflated Sharpe (multiple-testing firewall) ─────────────────────────
def g4_deflated_sharpe(net: pd.Series, trial_count: int, ann_factor: float = 365.0,
                       sr_trial_std: float = None) -> GateResult:
    dsr = deflated_sharpe(net.tolist(), n_trials=max(1, trial_count), annualization_factor=ann_factor,
                          sr_trial_std=sr_trial_std)
    if "error" in dsr:
        return GateResult("G4_deflated_sharpe", "fail", dsr, dsr["error"])
    raw = float(dsr.get("raw_sharpe", 0.0)); pval = dsr.get("dsr_pvalue"); sig = bool(dsr.get("is_significant", False))
    reliable = bool(dsr.get("reliable", True))
    passed = sig and raw > 0 and (pval is not None and pval < DSR_PVALUE_MAX)
    if not reliable:                                    # cold ledger: no cross-trial σ_SR at non-trivial N
        reason = (f"deflation not trustworthy — no ledger σ_SR yet at N={trial_count} "
                  f"(fail-closed until the trial ledger warms up)")
    elif not passed:
        reason = f"raw_sharpe={raw:.2f}, dsr_p={pval}, trials={trial_count} — not significant"
    else:
        reason = ""
    return GateResult("G4_deflated_sharpe", "pass" if passed else "fail",
                      {"raw_sharpe": raw, "dsr_pvalue": pval, "dsr_z": dsr.get("dsr_z_score"),
                       "expected_max_sr": dsr.get("expected_max_sr"), "is_significant": sig,
                       "reliable": reliable, "sigma_sr_source": dsr.get("sigma_sr_source"),
                       "trial_count": trial_count, "engine": dsr.get("engine")}, reason)


# ── G4b Reality Check (non-parametric multiple-testing firewall, alongside G4) ─
def g4b_reality_check(net: pd.Series, trial_count: int, seed: int = 42) -> GateResult:
    rc = reality_check(net.tolist(), n_trials=max(1, trial_count), seed=seed)
    if "error" in rc:
        return GateResult("G4b_reality_check", "fail", rc, rc["error"])
    passed = bool(rc.get("is_significant", False))
    reason = "" if passed else (f"bootstrap p_fwer={rc.get('p_fwer')} (N={trial_count}) — Sharpe "
                                f"not significant under stationary-block resampling")
    return GateResult("G4b_reality_check", "pass" if passed else "fail",
                      {"p_single": rc.get("p_single"), "p_fwer": rc.get("p_fwer"),
                       "raw_sharpe": rc.get("raw_sharpe"), "trial_count": trial_count,
                       "engine": rc.get("engine")}, reason)


# ── G5 robustness: stationary-block bootstrap ──────────────────────────────
def g5_robustness(net: pd.Series, seed: int = 42) -> GateResult:
    boot = bootstrap_drawdown(net.tolist(), n_sims=3000, seed=seed)
    if "error" in boot:
        return GateResult("G5_robustness", "fail", boot, boot["error"])
    dd95 = float(boot.get("max_dd_95", 1.0))
    passed = dd95 < MAX_DD_95_CAP
    reason = "" if passed else f"bootstrap 95th-pct max-DD {dd95:.2f} > cap {MAX_DD_95_CAP:.2f}"
    return GateResult("G5_robustness", "pass" if passed else "fail",
                      {"max_dd_95": dd95, "cvar_95": boot.get("cvar_95"), "engine": boot.get("engine")}, reason)


# ── G7 capacity / cost stress (2× costs, cheap linear model) ───────────────
def g7_capacity(genome, res, ctx) -> GateResult:
    mkt = MARKETS.get(genome.meta.market)
    cost_per = round_trip_cost_bps(half_spread_bps=(mkt.half_spread_bps if mkt else 2.0),
                                   fee_bps_per_side=(mkt.fee_bps_per_side if mkt else 5.0),
                                   funding_rate=None) / 1e4
    net = res.net_returns
    turn = res.turnover.reindex(net.index).fillna(0.0) if len(res.turnover) else pd.Series(1.0, index=net.index)
    net_2x = net - turn * cost_per                      # charge one extra round trip ⇒ 2× friction
    sh2 = _sharpe(net_2x.to_numpy())
    passed = np.isfinite(sh2) and sh2 > 0
    reason = "" if passed else f"edge evaporates under 2× costs (sharpe_2x={sh2:.2f})"
    return GateResult("G7_capacity", "pass" if passed else "fail",
                      {"sharpe_2x_cost": None if not np.isfinite(sh2) else round(sh2, 3)}, reason)


# ── G8 orthogonality vs the current archive ────────────────────────────────
def g8_orthogonality(res, ctx) -> GateResult:
    archive_returns = getattr(ctx, "archive_returns", {}) or {}
    if not archive_returns:
        return GateResult("G8_orthogonality", "pass", {"max_corr": None, "note": "empty archive"})
    r = res.net_returns.to_numpy(float)
    max_corr = 0.0
    for other in archive_returns.values():
        o = np.asarray(other, float)
        m = min(len(r), len(o))
        if m < 20:
            continue
        a, b = r[-m:], o[-m:]
        if a.std() == 0 or b.std() == 0:
            continue
        c = abs(float(np.corrcoef(a, b)[0, 1]))
        if np.isfinite(c):
            max_corr = max(max_corr, c)
    passed = max_corr < MAX_ARCHIVE_CORR
    reason = "" if passed else f"return corr {max_corr:.2f} ≥ {MAX_ARCHIVE_CORR} — duplicates an archive member"
    return GateResult("G8_orthogonality", "pass" if passed else "fail", {"max_corr": round(max_corr, 3)}, reason)


# ── G3 CPCV → PBO (expensive; needs evaluator) ─────────────────────────────
def g3_cpcv_pbo(genome, ctx) -> GateResult:
    if ctx is None or ctx.eval_fn is None or ctx.panel is None:
        return GateResult("G3_cpcv_pbo", "deferred", reason="no evaluator/panel in context")
    rng = np.random.default_rng(getattr(ctx, "seed", 42))
    variants = cpcv.param_variants(genome, m=getattr(ctx, "cpcv_variants", 6), rng=rng)
    mat = cpcv.returns_matrix(variants, ctx.panel, ctx.eval_fn)
    stats = cpcv.cscv_stats(mat, n_groups=getattr(ctx, "cpcv_groups", 8))
    if stats is None:
        return GateResult("G3_cpcv_pbo", "deferred", reason="insufficient data for CSCV")
    pbo = stats["pbo"]
    passed = pbo <= PBO_MAX
    reason = "" if passed else f"PBO={pbo:.2f} > {PBO_MAX} — parameter selection likely overfit"
    return GateResult("G3_cpcv_pbo", "pass" if passed else "fail",
                      {"pbo": round(pbo, 3),
                       "oos_sharpe_median": (None if stats["oos_sharpe_median"] is None
                                             else round(stats["oos_sharpe_median"], 3)),
                       "prob_oos_positive": (None if stats["prob_oos_positive"] is None
                                             else round(stats["prob_oos_positive"], 3))}, reason)


# ── G6 transfer / true out-of-sample (expensive; needs holdout) ────────────
def g6_transfer(genome, ctx) -> GateResult:
    if ctx is None or ctx.eval_fn is None or getattr(ctx, "holdout_panel", None) is None:
        return GateResult("G6_transfer", "deferred", reason="no holdout panel in context")
    hres = ctx.eval_fn(genome, ctx.holdout_panel)
    if not hres.ok:
        return GateResult("G6_transfer", "fail", {"holdout_error": hres.error}, "did not run on holdout")
    hsh = float(hres.summary.get("net_sharpe", float("nan")))
    passed = np.isfinite(hsh) and hsh > 0
    reason = "" if passed else f"edge does not transfer to held-out data (holdout sharpe={hsh:.2f})"
    return GateResult("G6_transfer", "pass" if passed else "fail",
                      {"holdout_sharpe": None if not np.isfinite(hsh) else round(hsh, 3)}, reason)
