"""mt.gauntlet.gates — the individual gates. Any failure rejects the candidate.

Thin slice: G1/G4/G5 are real pass/fail; G2/G3/G6/G7/G8 return status="deferred" so the
report is honest about what has and hasn't been tested. No gate compensates for another
(the 5-gate no-compensation philosophy, docs/05 §2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import numpy as np
import pandas as pd

from mt.adapters.cclib import deflated_sharpe, bootstrap_drawdown

MIN_PERIODS = 20
MAX_SINGLE_PERIOD_SHARE = 0.50   # no single rebalance may be >50% of gross P&L
DSR_PVALUE_MAX = 0.05
MAX_DD_95_CAP = 0.60             # bootstrap 95th-pct max drawdown ceiling


@dataclass
class GateResult:
    name: str
    status: str                  # "pass" | "fail" | "deferred"
    stats: Dict = field(default_factory=dict)
    reason: str = ""

    @property
    def passed(self) -> bool:
        return self.status in ("pass", "deferred")   # deferred does not block in the thin slice

    @property
    def enforced(self) -> bool:
        return self.status in ("pass", "fail")


def g1_sanity(net: pd.Series) -> GateResult:
    n = int(len(net))
    if n < MIN_PERIODS:
        return GateResult("G1_sanity", "fail", {"n_periods": n}, f"too few periods ({n} < {MIN_PERIODS})")
    total_abs = float(net.abs().sum())
    share = float(net.abs().max() / total_abs) if total_abs > 0 else 1.0
    if share > MAX_SINGLE_PERIOD_SHARE:
        return GateResult("G1_sanity", "fail", {"single_period_share": share},
                          f"one period is {share:.0%} of gross P&L (>{MAX_SINGLE_PERIOD_SHARE:.0%})")
    sharpe = float(net.mean() / net.std(ddof=1)) if net.std(ddof=1) > 0 else float("nan")
    if not np.isfinite(sharpe):
        return GateResult("G1_sanity", "fail", {}, "degenerate return series (zero variance)")
    return GateResult("G1_sanity", "pass", {"n_periods": n, "single_period_share": round(share, 3)})


def g2_purged_wf() -> GateResult:
    return GateResult("G2_purged_wf", "deferred", reason="purged walk-forward — wraps backtest/purged_cv.py (P2)")


def g3_cpcv_pbo() -> GateResult:
    return GateResult("G3_cpcv_pbo", "deferred", reason="CPCV → PBO — the genuinely-new gate (P2)")


def g4_deflated_sharpe(net: pd.Series, trial_count: int, ann_factor: float = 365.0) -> GateResult:
    dsr = deflated_sharpe(net.tolist(), n_trials=max(1, trial_count), annualization_factor=ann_factor)
    if "error" in dsr:
        return GateResult("G4_deflated_sharpe", "fail", dsr, dsr["error"])
    raw = float(dsr.get("raw_sharpe", 0.0))
    pval = dsr.get("dsr_pvalue")
    sig = bool(dsr.get("is_significant", False))
    passed = sig and raw > 0 and (pval is not None and pval < DSR_PVALUE_MAX)
    reason = "" if passed else (
        f"raw_sharpe={raw:.2f}, dsr_p={pval}, trials={trial_count} — not significant after deflation"
    )
    return GateResult("G4_deflated_sharpe", "pass" if passed else "fail",
                      {"raw_sharpe": raw, "dsr_pvalue": pval, "is_significant": sig,
                       "trial_count": trial_count, "engine": dsr.get("engine")}, reason)


def g5_robustness(net: pd.Series, seed: int = 42) -> GateResult:
    boot = bootstrap_drawdown(net.tolist(), n_sims=3000, seed=seed)
    if "error" in boot:
        return GateResult("G5_robustness", "fail", boot, boot["error"])
    dd95 = float(boot.get("max_dd_95", 1.0))
    passed = dd95 < MAX_DD_95_CAP
    reason = "" if passed else f"bootstrap 95th-pct max-DD {dd95:.2f} exceeds cap {MAX_DD_95_CAP:.2f}"
    return GateResult("G5_robustness", "pass" if passed else "fail",
                      {"max_dd_95": dd95, "cvar_95": boot.get("cvar_95"),
                       "block_length": boot.get("block_length"), "engine": boot.get("engine")}, reason)


def g6_transfer() -> GateResult:
    return GateResult("G6_transfer", "deferred", reason="unseen-symbol / cross-market OOS (P2)")


def g7_capacity() -> GateResult:
    return GateResult("G7_capacity", "deferred", reason="2× cost + sqrt-impact capacity stress (P2)")


def g8_orthogonality() -> GateResult:
    return GateResult("G8_orthogonality", "deferred", reason="marginal-Sharpe vs archive (P2)")
