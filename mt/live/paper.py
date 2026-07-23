"""mt.live.paper — the paper/shadow rung R1 (docs/07 §2).

Runs archive elites on a LIVE data feed through the *same* event-driven simulator, so a
divergence between live-paper and backtest is information (regime change / capacity / a data
bug), not a mystery. Steps day-by-day: each day realizes per-strategy returns, the allocator
reweights (Hedge + regime + correlation), the drift monitors watch each strategy, and hard
circuit breakers guard the book. NO ORDERS ARE EVER PLACED — this is simulation only.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from mt.genome.schema import Genome
from mt.sim import evaluate
from mt.live.allocator import HedgeAllocator
from mt.live.drift import DriftMonitor, circuit_breaker, probabilistic_sharpe_ratio


class PaperBook:
    def __init__(self, market: str, elites: List[Tuple[Genome, float]], seed: int = 4242):
        self.market = market
        self.seed = seed
        self.strategies = elites                          # [(genome, backtest_sr_pp)]
        self.ids = [g.genome_id for g, _ in elites]
        self.alloc = HedgeAllocator(self.ids)
        self.monitors: Dict[str, DriftMonitor] = {
            g.genome_id: DriftMonitor(backtest_sr_pp=float(sr or 0.0)) for g, sr in elites
        }
        self.live_returns: Dict[str, List[float]] = {gid: [] for gid in self.ids}
        self.equity: List[float] = [1.0]
        self.events: List[str] = []
        self.halted = False

    def run(self, live_panel, n_days: int = 12, regime_match: Dict[str, float] = None) -> dict:
        if not self.strategies:
            return {"error": "no elites to paper-trade", "daily": [], "events": []}
        # each elite's live return series on the unseen continuation
        series: Dict[str, np.ndarray] = {}
        for g, _ in self.strategies:
            res = evaluate(g, live_panel, self.seed)
            series[g.genome_id] = res.net_returns.to_numpy() if res.ok else np.array([])

        daily = []
        for d in range(n_days):
            day_rewards: Dict[str, float] = {}
            for gid in self.ids:
                arr = series[gid]
                if len(arr) == 0:
                    r = 0.0
                else:
                    lo, hi = int(d * len(arr) / n_days), int((d + 1) * len(arr) / n_days)
                    chunk = arr[lo:hi]
                    r = float(np.mean(chunk)) if len(chunk) else 0.0
                day_rewards[gid] = r
                self.live_returns[gid].append(r)
                if not self.monitors[gid].quarantined:
                    resp = self.monitors[gid].update(r)
                    if resp == "quarantine":
                        self.alloc.drop(gid)
                        self.events.append(f"day {d}: QUARANTINE {gid} — drift detected (→ back to R1/critic)")
                    elif resp == "throttle":
                        self.alloc.throttle(gid)

            w = self.alloc.weights()
            book_r = float(sum(w[gid] * day_rewards[gid] for gid in self.ids))
            self.equity.append(self.equity[-1] * (1.0 + book_r))

            cb = circuit_breaker(self.equity)
            if cb == "halt":
                self.events.append(f"day {d}: PORTFOLIO CIRCUIT BREAKER — flatten book")
                self.halted = True
            self.alloc.update(day_rewards)
            if regime_match:
                self.alloc.regime_adjust(regime_match)
            self._correlation_shrink()                       # keep the book diversified (docs/07 §3)
            daily.append({"day": d, "book_return": round(book_r, 5),
                          "equity": round(self.equity[-1], 5), "weights": {k: round(v, 3) for k, v in w.items()}})
            if self.halted:
                break

        return {
            "daily": daily, "events": self.events, "equity": self.equity,
            "final_weights": {k: round(v, 3) for k, v in self.alloc.weights().items()},
            "live_vs_backtest": self._live_vs_backtest(),
            "book_sharpe": self._book_sharpe(daily),
            "halted": self.halted,
        }

    def _correlation_shrink(self, window: int = 20, min_obs: int = 6) -> None:
        """Down-weight each strategy by its mean |correlation| with the rest of the book, from
        the accumulated live returns — the correlation-aware half of the docs/07 allocator."""
        if len(self.ids) < 2:
            return
        series = {gid: np.asarray(self.live_returns[gid][-window:], float) for gid in self.ids}
        L = min(len(v) for v in series.values())
        if L < min_obs:
            return
        M = np.vstack([series[gid][-L:] for gid in self.ids])
        if not np.all(M.std(axis=1) > 0):
            return
        C = np.corrcoef(M)
        corr = {}
        for i, gid in enumerate(self.ids):
            off = [abs(C[i, j]) for j in range(len(self.ids)) if j != i and np.isfinite(C[i, j])]
            corr[gid] = float(np.mean(off)) if off else 0.0
        self.alloc.correlation_shrink(corr)

    def _live_vs_backtest(self) -> Dict[str, dict]:
        out = {}
        for g, bt in self.strategies:
            gid = g.genome_id
            live = self.live_returns[gid]
            live_sr = (np.mean(live) / np.std(live, ddof=1)) if (len(live) > 1 and np.std(live, ddof=1) > 0) else float("nan")
            out[gid] = {
                "backtest_sr_pp": round(float(bt or 0.0), 4),
                "live_sr_pp": None if not np.isfinite(live_sr) else round(float(live_sr), 4),
                "live_psr": round(probabilistic_sharpe_ratio(live), 3),
                "quarantined": self.monitors[gid].quarantined,
                "tracks_backtest": bool(np.isfinite(live_sr) and (bt or 0) > 0 and live_sr > 0),
            }
        return out

    def _book_sharpe(self, daily: List[dict]) -> float:
        rs = np.array([d["book_return"] for d in daily], float)
        if len(rs) < 2 or rs.std(ddof=1) == 0:
            return float("nan")
        return round(float(rs.mean() / rs.std(ddof=1) * np.sqrt(252)), 3)
