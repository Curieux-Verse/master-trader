"""mt.live.allocator — the regime-aware, correlation-aware online allocator (docs/07 §3).

A Hedge/EXP3-style online weighting shifts risk toward what is *currently* working without
over-reacting to noise, conditioned on the current regime (up-weight strategies whose niche
matches it) and shrunk by correlation so the book stays diversified. Same bandit math as the
discovery meta-controller, pointed at risk instead of search.
"""
from __future__ import annotations

from typing import Dict, List

import numpy as np


class HedgeAllocator:
    def __init__(self, strategy_ids: List[str], eta: float = 3.0):
        self.ids = list(strategy_ids)
        self.eta = eta
        n = max(1, len(self.ids))
        self.w = {s: 1.0 / n for s in self.ids}

    def update(self, rewards: Dict[str, float]) -> None:
        """Multiplicative-weights update on per-strategy realized returns (Hedge)."""
        for s in self.ids:
            self.w[s] *= float(np.exp(self.eta * float(rewards.get(s, 0.0))))
        self._normalize()

    def regime_adjust(self, regime_match: Dict[str, float]) -> None:
        """Up-weight strategies whose behavioral niche matches the current regime."""
        for s in self.ids:
            self.w[s] *= max(0.1, float(regime_match.get(s, 1.0)))
        self._normalize()

    def correlation_shrink(self, corr: Dict[str, float]) -> None:
        """Down-weight strategies highly correlated with the rest of the book."""
        for s in self.ids:
            self.w[s] /= (1.0 + max(0.0, float(corr.get(s, 0.0))))
        self._normalize()

    def throttle(self, sid: str, factor: float = 0.5) -> None:
        if sid in self.w:
            self.w[sid] *= factor
            self._normalize()

    def drop(self, sid: str) -> None:
        if sid in self.w:
            self.w[sid] = 0.0
            self._normalize()

    def weights(self) -> Dict[str, float]:
        return dict(self.w)

    def _normalize(self) -> None:
        tot = sum(self.w.values())
        if tot <= 0:
            n = max(1, len([s for s in self.ids]))
            self.w = {s: 1.0 / n for s in self.ids}
        else:
            self.w = {s: v / tot for s, v in self.w.items()}
