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

from mt.adapters.cclib import (deflated_sharpe, bootstrap_drawdown, round_trip_cost_bps,
                               reality_check, MAX_SANE_SR_PP)
from mt.config import MARKETS
from mt.gauntlet import cpcv

MIN_PERIODS = 20
MAX_SINGLE_PERIOD_SHARE = 0.50
DSR_PVALUE_MAX = 0.05
MAX_DD_95_CAP = 0.60
PBO_MAX = 0.50
MAX_ARCHIVE_CORR = 0.90       # above this the fitness discount starts biting
CLONE_CORR = 0.99             # above this it is the same strategy — hard reject
FDR_Q = 0.10                  # Stage-A false-discovery rate (docs/15 §4)


@dataclass
class GateResult:
    name: str
    status: str                  # "pass" | "fail" | "deferred"
    stats: Dict = field(default_factory=dict)
    reason: str = ""
    advisory: bool = False       # measured and reported, but never rejects at this stage

    @property
    def passed(self) -> bool:
        return self.status in ("pass", "deferred")

    @property
    def enforced(self) -> bool:
        return (not self.advisory) and self.status in ("pass", "fail")

    def as_advisory(self) -> "GateResult":
        return GateResult(self.name, self.status, self.stats, self.reason, advisory=True)


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
    srpp = _sharpe(net.to_numpy())
    # a non-finite OR implausibly huge per-bar Sharpe means near-zero variance — a (near-)constant
    # series whose std is float noise, not a real edge (its huge Sharpe would else pass G4b / G4).
    if not np.isfinite(srpp) or abs(srpp) > MAX_SANE_SR_PP:
        return GateResult("G1_sanity", "fail",
                          {"sharpe_pp": None if not np.isfinite(srpp) else round(srpp, 3)},
                          "degenerate return series (near-zero variance / implausible Sharpe)")
    return GateResult("G1_sanity", "pass",
                      {"n_periods": n, "single_period_share": round(share, 3), "sharpe_pp": round(srpp, 3)})


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


# ── GS Stage-A screen: FDR-controlled, N-INDEPENDENT (docs/15 §4) ──────────
def gs_screen(net: pd.Series, fdr_threshold: Optional[float], q: float = 0.10) -> GateResult:
    """The EXPLORATORY bar. Admits a candidate to the pool when its single-strategy p-value clears
    a Benjamini–Hochberg–Yekutieli threshold computed over the recent trial population.

    Why this and not G4: the Deflated Sharpe is a max-statistic FWER control. Applied to every
    exploratory candidate at a family size of every trial ever run, it is a confirmatory
    instrument used as a screen — the setting the multiple-comparisons literature specifically
    warns produces many missed discoveries. Worse for a *learning* system, its output moves when
    the ledger grows, so the same genome scores differently in generation 10 and generation 500
    and no parent→child comparison means anything.

    `t = SR·√T` carries no family-size term at all, so this score is stable across the whole
    marathon. The BHY correction (valid under arbitrary dependence — our trials share features)
    keeps the promotion rate honest: at q=0.10 roughly one in ten promotions is expected to be
    false, which is the correct trade for a stage whose output still has to survive Stage B."""
    n = int(len(net))
    if n < MIN_PERIODS:
        return GateResult("GS_screen", "fail", {"n_periods": n}, f"too few periods ({n})")
    from mt.gauntlet.multipletest import sharpe_pvalue
    srpp = _sharpe(net.to_numpy())
    if not np.isfinite(srpp) or abs(srpp) > MAX_SANE_SR_PP:
        return GateResult("GS_screen", "fail", {"sharpe_pp": None}, "degenerate return series")
    p = sharpe_pvalue(srpp, n)
    edge_t = float(srpp * np.sqrt(n))
    if fdr_threshold is None:                       # nothing in the batch is a discovery yet
        return GateResult("GS_screen", "fail",
                          {"p_single": p, "edge_t": round(edge_t, 4), "fdr_threshold": None,
                           "fdr_q": q},
                          f"no BHY discovery at q={q} in the current trial population")
    passed = bool(p is not None and p <= fdr_threshold and srpp > 0)
    reason = "" if passed else (f"p={None if p is None else round(p, 5)} > BHY threshold "
                                f"{round(fdr_threshold, 5)} at q={q}")
    return GateResult("GS_screen", "pass" if passed else "fail",
                      {"p_single": None if p is None else round(p, 6), "edge_t": round(edge_t, 4),
                       "fdr_threshold": round(fdr_threshold, 6), "fdr_q": q}, reason)


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
    # include a representative funding charge for perp markets so the 2× cost stress doesn't
    # silently understate round-trip cost for crypto (funding is a real, recurring leg).
    fr = 0.0001 if (mkt and mkt.has_funding) else None
    cost_per = round_trip_cost_bps(half_spread_bps=(mkt.half_spread_bps if mkt else 2.0),
                                   fee_bps_per_side=(mkt.fee_bps_per_side if mkt else 5.0),
                                   funding_rate=fr) / 1e4
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
        mask = np.isfinite(a) & np.isfinite(b)          # correlate the finite overlap, don't skip on a
        if mask.sum() < 20:                              # single NaN (which would silently read as orthogonal)
            continue
        a, b = a[mask], b[mask]
        if a.std() == 0 or b.std() == 0:
            continue
        c = abs(float(np.corrcoef(a, b)[0, 1]))
        if np.isfinite(c):
            max_corr = max(max_corr, c)
    # Hard-reject only a near-EXACT clone; everything between MAX_ARCHIVE_CORR and that is handled
    # by a continuous fitness DISCOUNT in the runner's scalarization. A hard 0.90 wall was safe
    # while the archive was empty (it never fired: 0 of 400 verdicts measured a real correlation),
    # but now that the archive admits by niche it would become a false-reject wall on genuinely
    # related-but-distinct strategies. Penalising similarity continuously — rather than forbidding
    # it — is what redirects the search instead of merely blocking it (AutoAlpha PCA-QD; WorldQuant
    # discounts an alpha's score by its max correlation to the existing pool).
    passed = max_corr < CLONE_CORR
    reason = "" if passed else f"return corr {max_corr:.2f} ≥ {CLONE_CORR} — an exact duplicate of an archive member"
    return GateResult("G8_orthogonality", "pass" if passed else "fail",
                      {"max_corr": round(max_corr, 3),
                       "similarity_penalty": round(max(0.0, max_corr - MAX_ARCHIVE_CORR) /
                                                   max(1e-9, CLONE_CORR - MAX_ARCHIVE_CORR), 3)},
                      reason)


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
