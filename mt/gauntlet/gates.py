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
# G9 plateau: a neighbour "survives" if it keeps this share of the centre's t-stat, and the
# genome passes if at least PLATEAU_MIN_PCT of its neighbours survive. 50%/50% is deliberately
# forgiving — the target is the strategy whose edge VANISHES one parameter step away, not one
# that merely degrades.
PLATEAU_RETAIN = 0.50
PLATEAU_MIN_PCT = 50.0
# G10 beat-random: family-wise α spent across the candidates screened against one reference
# distribution, and the minimum reference sample before the gate will express an opinion.
BEAT_RANDOM_ALPHA = 0.05
MIN_RANDOM_REF = 30


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
                       sr_trial_std: float = None, sigma_floor: bool = True) -> GateResult:
    dsr = deflated_sharpe(net.tolist(), n_trials=max(1, trial_count), annualization_factor=ann_factor,
                          sr_trial_std=sr_trial_std, sigma_floor=sigma_floor)
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
                       "sigma_sr": dsr.get("sigma_sr"), "n_returns": dsr.get("n_returns"),
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
    return cpcv_and_plateau(genome, ctx)[0]


def cpcv_and_plateau(genome, ctx):
    """Run the parameter neighbourhood ONCE and answer both questions it can answer.

    G3 (PBO) and G9 (plateau) both need the [T × K] variant return matrix, which is the single
    most expensive object the gauntlet builds — K extra backtests per candidate. Building it
    twice to run two gates would double the cost of the whole expensive tier for no information
    gain, so the two gates are produced together and the runner appends both."""
    if ctx is None or ctx.eval_fn is None or ctx.panel is None:
        d = GateResult("G3_cpcv_pbo", "deferred", reason="no evaluator/panel in context")
        return d, GateResult("G9_plateau", "deferred", reason="no evaluator/panel in context")
    rng = np.random.default_rng(getattr(ctx, "seed", 42))
    variants = cpcv.param_variants(genome, m=getattr(ctx, "cpcv_variants", 6), rng=rng)
    mat = cpcv.returns_matrix(variants, ctx.panel, ctx.eval_fn)
    stats = cpcv.cscv_stats(mat, n_groups=getattr(ctx, "cpcv_groups", 8))

    if stats is None:
        g3 = GateResult("G3_cpcv_pbo", "deferred", reason="insufficient data for CSCV")
    else:
        pbo = stats["pbo"]
        passed = pbo <= PBO_MAX
        g3 = GateResult("G3_cpcv_pbo", "pass" if passed else "fail",
                        {"pbo": round(pbo, 3),
                         "oos_sharpe_median": (None if stats["oos_sharpe_median"] is None
                                               else round(stats["oos_sharpe_median"], 3)),
                         "prob_oos_positive": (None if stats["prob_oos_positive"] is None
                                               else round(stats["prob_oos_positive"], 3))},
                        "" if passed else f"PBO={pbo:.2f} > {PBO_MAX} — parameter selection likely overfit")

    p = cpcv.plateau_stats(mat, retain=PLATEAU_RETAIN)
    if p is None:
        g9 = GateResult("G9_plateau", "deferred", reason="no usable parameter neighbourhood")
    else:
        ok = p["plateau_pass_pct"] >= PLATEAU_MIN_PCT
        g9 = GateResult("G9_plateau", "pass" if ok else "fail", p,
                        "" if ok else (f"only {p['plateau_pass_pct']:.0f}% of {p['plateau_n']} "
                                       f"parameter neighbours keep ≥{int(PLATEAU_RETAIN*100)}% of the "
                                       f"edge (need {PLATEAU_MIN_PCT:.0f}%) — a spike, not a plateau"))
    return g3, g9


# ── G10 empirical reference distribution: skill vs a randomly CONSTRUCTED strategy ──
def g10_beat_random(net: pd.Series, ctx) -> GateResult:
    """Does this genome beat a randomly constructed strategy on the same data, often enough?

    Every other significance gate here is PARAMETRIC: the Deflated Sharpe assumes the trial
    Sharpes are normal with dispersion σ_SR, and we measured how badly that assumption can fail
    — a contaminated ledger drove σ_SR to 2,497 and every z to −∞, and a σ_SR pooled over trials
    whose T differs 76× is wrong at nearly every horizon. This gate needs no σ at all. It
    compares the candidate's N-independent t-statistic against the EMPIRICAL distribution of
    t-statistics produced by random genomes evaluated on the same panel.

    The bar is MULTIPLICITY-AWARE, which is the part that makes it a test rather than a
    leaderboard. Requiring a fixed percentile (Algory OS uses 85%) means that screening k
    candidates against the same reference distribution yields k·(1−q) expected false passes; at
    q=0.85 and the thousands of genomes a marathon evaluates, that is not a control at all.
    Here the required quantile is q = 1 − α/k (Bonferroni over the candidates screened against
    this reference), so the bar RISES as the search gets wider — the empirical analogue of
    E[max of N], measured rather than assumed.

    It is deliberately advisory in Stage A: it is a reference distribution over the strategy
    SPACE, not a null hypothesis about the data. Random genomes are not guaranteed edgeless —
    some random momentum rule really does work — so failing it is evidence of weakness, not
    proof of absence."""
    ref = getattr(ctx, "random_ref", None) if ctx is not None else None
    n = int(len(net))
    if not ref or len(ref) < MIN_RANDOM_REF or n < MIN_PERIODS:
        return GateResult("G10_beat_random", "deferred",
                          {"random_n": (0 if not ref else len(ref))},
                          "no reference distribution of random strategies yet")
    srpp = _sharpe(net.to_numpy())
    if not np.isfinite(srpp) or abs(srpp) > MAX_SANE_SR_PP:
        return GateResult("G10_beat_random", "fail", {"edge_t": None}, "degenerate return series")
    edge_t = float(srpp * np.sqrt(n))
    arr = np.asarray([x for x in ref if np.isfinite(x)], dtype=float)
    beat_pct = float(np.mean(arr < edge_t) * 100.0)
    k = max(1, int(getattr(ctx, "random_ref_k", 1) or 1))
    required = (1.0 - BEAT_RANDOM_ALPHA / k) * 100.0
    required = float(min(required, 100.0 * (1.0 - 1.0 / (len(arr) + 1))))   # can't exceed resolution
    passed = beat_pct >= required
    return GateResult("G10_beat_random", "pass" if passed else "fail",
                      {"edge_t": round(edge_t, 4), "beat_random_pct": round(beat_pct, 2),
                       "br_required_pct": round(required, 2), "random_n": int(arr.size),
                       "br_adaptive_k": k},
                      "" if passed else (f"beat {beat_pct:.0f}% of {arr.size} random strategies, "
                                         f"bar is {required:.1f}% at k={k}"))


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
