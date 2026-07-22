"""mt.improve.bandit — the meta-controller (docs/06 §4).

A Thompson-sampling bandit over the generation engines. Reward = did the genome improve the
QD archive (occupy/replace a niche)? So the system *learns how to generate*, shifting budget
toward whichever engine is currently producing archive-improving genomes — not just what to
trade. Same math the live allocator (docs/07) points at risk instead of search.
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, List

import numpy as np

ENGINES = ["template", "random", "evo", "miner", "llm"]


def engine_of(generator: str) -> str:
    g = (generator or "").lower()
    if g.startswith("template"):
        return "template"
    if g.startswith("evo"):
        return "evo"
    if g.startswith("miner") or g.startswith("intx"):
        return "miner"
    if g.startswith("llm") or g.startswith("critic"):
        return "llm"
    return "random"


class EngineBandit:
    def __init__(self, engines: List[str] = None, seed: int = 4242):
        self.engines = list(engines or ENGINES)
        self.alpha: Dict[str, float] = {e: 1.0 for e in self.engines}
        self.beta: Dict[str, float] = {e: 1.0 for e in self.engines}
        self.rng = np.random.default_rng(seed)

    def sample_engine(self) -> str:
        draws = {e: self.rng.beta(self.alpha[e], self.beta[e]) for e in self.engines}
        return max(draws, key=draws.get)

    def allocate(self, n: int) -> Dict[str, int]:
        picks = Counter(self.sample_engine() for _ in range(max(1, n)))
        return {e: picks.get(e, 0) for e in self.engines}

    def update(self, engine: str, reward: float) -> None:
        reward = float(max(0.0, min(1.0, reward)))
        if engine in self.alpha:
            self.alpha[engine] += reward
            self.beta[engine] += 1.0 - reward

    def weights(self) -> Dict[str, float]:
        return {e: self.alpha[e] / (self.alpha[e] + self.beta[e]) for e in self.engines}
