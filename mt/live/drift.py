"""mt.live.drift — concept-drift detection & kill switches (docs/07 §4).

Three layers, fastest to slowest: Page-Hinkley change-point on the live P&L stream, a
rolling Probabilistic Sharpe Ratio of live-vs-backtest expectation, and hard portfolio
circuit breakers. The response is graduated (throttle → quarantine → halt), not binary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np


class PageHinkley:
    """Page-Hinkley test for a DECREASE in the mean of a return stream (edge decay).

    Tracks the cumulative deviation m_T = Σ(x − x̄ + δ) and its running maximum; a downward
    change-point is flagged when M_T − m_T exceeds λ (the classic decrease-detection form)."""
    def __init__(self, delta: float = 0.0005, lam: float = 0.05):
        self.delta = delta; self.lam = lam
        self.n = 0; self.mean = 0.0; self.sum = 0.0; self.max_sum = 0.0

    def update(self, x: float) -> bool:
        if not np.isfinite(x):
            return False
        self.n += 1
        self.mean += (x - self.mean) / self.n
        self.sum += (x - self.mean + self.delta)
        self.max_sum = max(self.max_sum, self.sum)
        return (self.max_sum - self.sum) > self.lam


def probabilistic_sharpe_ratio(returns: List[float], benchmark_sr: float = 0.0) -> float:
    """PSR: probability the true (per-observation) Sharpe exceeds a benchmark (Bailey & LdP)."""
    from scipy.stats import norm, skew, kurtosis
    r = np.asarray([x for x in returns if np.isfinite(x)], float)
    if len(r) < 10 or r.std(ddof=1) == 0:
        return 0.5
    sr = r.mean() / r.std(ddof=1)
    s = float(skew(r)); k = float(kurtosis(r, fisher=True)) + 3.0
    se = np.sqrt(max(1e-12, (1 - s * sr + ((k - 1) / 4) * sr ** 2) / (len(r) - 1)))
    return float(norm.cdf((sr - benchmark_sr) / se))


@dataclass
class DriftMonitor:
    """Per-strategy monitor: Page-Hinkley + rolling PSR vs the backtest-expected Sharpe."""
    backtest_sr_pp: float                                # expected per-observation Sharpe
    ph: PageHinkley = field(default_factory=PageHinkley)
    live: List[float] = field(default_factory=list)
    quarantined: bool = False

    def update(self, day_return: float) -> str:
        """Return the response: 'ok' | 'throttle' | 'quarantine'."""
        self.live.append(day_return)
        changed = self.ph.update(day_return)
        if changed:
            self.quarantined = True
            return "quarantine"
        if len(self.live) >= 10:
            psr = probabilistic_sharpe_ratio(self.live, benchmark_sr=0.0)
            # live edge no longer credibly positive, or far below backtest expectation
            if psr < 0.40:
                self.quarantined = True
                return "quarantine"
            if psr < 0.55 or (self.backtest_sr_pp > 0 and np.mean(self.live) < 0):
                return "throttle"
        return "ok"


def circuit_breaker(equity: List[float], max_dd: float = 0.25, daily_loss: float = 0.08) -> str:
    """Portfolio-level hard limits — cut risk regardless of any single strategy."""
    if len(equity) < 2:
        return "ok"
    eq = np.asarray(equity, float)
    peak = np.maximum.accumulate(eq)
    dd = float((peak - eq)[-1] / peak[-1]) if peak[-1] > 0 else 0.0
    last = float(eq[-1] - eq[-2])
    if dd >= max_dd:
        return "halt"
    if last <= -daily_loss:
        return "throttle"
    return "ok"
