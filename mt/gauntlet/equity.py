"""mt.gauntlet.equity — shape-of-the-equity-curve statistics.

Sharpe answers "how much return per unit of volatility". It says nothing about the *path*: two
strategies with identical Sharpe can climb steadily or lurch between long flat spells and a
handful of enormous days. The second is far more fragile out of sample — its result rests on
fewer independent events — and nothing in the fitness vector could previously tell them apart.

Three complementary statistics, all computed from the net-return series:

  • K-RATIO (Kestner) — the t-statistic of the equity trend. A least-squares line is fitted to
    the LOG cumulative equity and the slope is divided by its own standard error, so a curve that
    rises in a straight line scores far above one that reaches the same endpoint through violent
    swings. This is the principled form of the "linearity" idea; the R² that people usually reach
    for measures how well a LINE fits, which rewards a smooth curve even when it slopes downward,
    and is scale-free in a way that ignores how many observations produced it.

  • PERSISTENCE — the fraction of non-overlapping sub-periods that are individually profitable.
    Catches the strategy whose entire edge is two lucky windows.

  • RECOVERY FACTOR — total return divided by maximum drawdown. The return actually earned per
    unit of worst-case pain, which is what a human deciding whether to keep a strategy running
    actually cares about.

None of these is a significance test and none is used as one. They enter the multi-objective
fitness (and the reports) as SHAPE information, alongside the statistical gates that decide
whether an edge exists at all.
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Sequence

import numpy as np

MIN_OBS = 12
# A K-ratio is slope/standard-error, so a near-CONSTANT return series drives the denominator to
# float noise and the ratio to ~1e15 — the same degenerate-statistic failure that let a
# contaminated σ_SR reach 2,497 and drive every Deflated Sharpe to −∞. Such a series is not a
# flawless strategy, it is a broken one (G1 rejects it on exactly these grounds), so the value is
# clamped rather than allowed to dominate a Pareto sort or a report.
MAX_K_RATIO = 20.0


def _clean(returns: Sequence[float]) -> np.ndarray:
    r = np.asarray([float(x) for x in returns], dtype=float)
    return r[np.isfinite(r)]


def k_ratio(returns: Sequence[float], periods_per_year: Optional[float] = None) -> Optional[float]:
    """Kestner's K-ratio: slope of the log-equity regression ÷ standard error of that slope.

    Returns the 2013 revision, which rescales by √(periods per year)/n so the number is
    comparable across sampling frequencies and history lengths. Without that rescaling a
    longer backtest scores higher purely for being longer.

    Interpretation: it is a t-statistic. Values ≳ 1 indicate a trend that is real relative to
    the wobble around it; ≤ 0 means no reliable upward drift at all.
    """
    r = _clean(returns)
    n = r.size
    if n < MIN_OBS:
        return None
    # log equity: cumulative sum of log1p is the exact log of the compounded curve, and it keeps
    # a catastrophic -100% period from producing a NaN that silently kills the regression.
    with np.errstate(divide="ignore", invalid="ignore"):
        steps = np.log1p(np.clip(r, -0.999999, None))
    if not np.all(np.isfinite(steps)):
        return None
    equity = np.cumsum(steps)
    x = np.arange(n, dtype=float)
    xm, ym = x.mean(), equity.mean()
    sxx = float(((x - xm) ** 2).sum())
    if sxx <= 0:
        return None
    slope = float(((x - xm) * (equity - ym)).sum() / sxx)
    resid = equity - (ym + slope * (x - xm))
    dof = n - 2
    if dof <= 0:
        return None
    s2 = float((resid ** 2).sum()) / dof
    se = math.sqrt(s2 / sxx) if s2 > 0 else 0.0
    # relative tolerance, not `se <= 0`: the residual scatter of a near-constant series is float
    # noise many orders below the slope, which is finite and positive but still meaningless.
    if se <= 1e-12 * max(1.0, abs(slope)):
        return math.copysign(MAX_K_RATIO, slope) if slope else 0.0
    t = slope / se
    ppy = float(periods_per_year) if periods_per_year and periods_per_year > 0 else float(n)
    kr = t * math.sqrt(ppy) / n
    if not np.isfinite(kr):
        return None
    return float(max(-MAX_K_RATIO, min(MAX_K_RATIO, kr)))


def persistence(returns: Sequence[float], n_buckets: int = 8) -> Optional[float]:
    """Fraction of equal-length, NON-OVERLAPPING sub-periods with a positive total return.

    Non-overlapping matters: rolling windows share observations, so a single spectacular period
    would appear in many windows and inflate the score exactly for the strategy this is meant
    to catch."""
    r = _clean(returns)
    if r.size < MIN_OBS:
        return None
    k = max(2, min(int(n_buckets), r.size // 3))
    edges = np.array_split(r, k)
    wins = sum(1 for b in edges if b.size and float(b.sum()) > 0.0)
    return float(wins) / float(k)


def recovery_factor(returns: Sequence[float]) -> Optional[float]:
    """Total compounded return ÷ maximum drawdown (both as fractions).

    Capped at a finite value: a strategy with a vanishing drawdown would otherwise produce an
    infinity that propagates into the fitness vector and scrambles the Pareto sort."""
    r = _clean(returns)
    if r.size < MIN_OBS:
        return None
    eq = np.cumprod(1.0 + np.clip(r, -0.999999, None))
    peak = np.maximum.accumulate(eq)
    dd = float(np.max((peak - eq) / np.where(peak > 0, peak, np.nan))) if eq.size else 0.0
    total = float(eq[-1] - 1.0)
    if not np.isfinite(dd) or dd <= 1e-9:
        return 20.0 if total > 0 else 0.0
    return float(max(-20.0, min(20.0, total / dd)))


def equity_metrics(returns: Sequence[float], periods_per_year: Optional[float] = None) -> Dict:
    """All three, in one call, with None where the series is too short to support them."""
    return {
        "k_ratio": k_ratio(returns, periods_per_year),
        "persistence": persistence(returns),
        "recovery_factor": recovery_factor(returns),
    }
