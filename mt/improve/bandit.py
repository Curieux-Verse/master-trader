"""mt.improve.bandit — the meta-controller (docs/06 §4).

A Thompson-sampling bandit over the generation engines. Reward = did the genome improve the
QD archive (occupy/replace a niche)? So the system *learns how to generate*, shifting budget
toward whichever engine is currently producing archive-improving genomes — not just what to
trade. Same math the live allocator (docs/07) points at risk instead of search.
"""
from __future__ import annotations

from collections import Counter, deque
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


MEMORY = 400.0      # effective observation memory per arm (posterior is rescaled above this)
DISCOUNT = 0.999    # per-update multiplicative forgetting
MIN_SHARE = 0.05    # guaranteed batch share per engine, so no arm can be starved to death


class EngineBandit:
    """Discounted Thompson sampling over the generation engines.

    UNDISCOUNTED Beta posteriors are an ABSORBING STATE, and the production brain reached it:
    after ~34k pulls the counts were evo α=782.8/β=33205 against template α=1.0/β=8939, so
    template's 99.9th-percentile draw (0.00046) sat 40× below evo's *mean* (0.023). Measured on
    the real bandit_state: evo won 20000/20000 Thompson draws in all three markets, and a starved
    arm needed 210–419 CONSECUTIVE successes to recover — from an arm that is never sampled. Four
    of five engines, including the LLM critic, were permanently excluded from the search.

    Two changes, both standard for non-stationary bandits (Raj & Kalyani; Trovò et al.):
      • a discount factor plus a cap on effective memory, so evidence ages out and the posterior
        keeps enough variance to re-explore — recovery now takes ~12 successes, not 400;
      • EXTREME-VALUE credit assignment (Fialho et al., PPSN 2008): an engine is rewarded by the
        BEST outcome in a sliding window of its recent offspring, not the mean. In a search whose
        goal is to extend the tail, an engine that produces one breakthrough in fifty is more
        valuable than one that reliably produces mediocrity, and mean-based credit cannot see that.
    """

    def __init__(self, engines: List[str] = None, seed: int = 4242,
                 memory: float = MEMORY, discount: float = DISCOUNT, window: int = 50):
        self.engines = list(engines or ENGINES)
        self.alpha: Dict[str, float] = {e: 1.0 for e in self.engines}
        self.beta: Dict[str, float] = {e: 1.0 for e in self.engines}
        self.memory = float(memory)
        self.discount = float(discount)
        self.window = int(window)
        self.recent: Dict[str, deque] = {e: deque(maxlen=self.window) for e in self.engines}
        self.rng = np.random.default_rng(seed)

    def sample_engine(self) -> str:
        draws = {e: self.rng.beta(self.alpha[e], self.beta[e]) for e in self.engines}
        return max(draws, key=draws.get)

    def allocate(self, n: int, floors: Dict[str, float] = None) -> Dict[str, int]:
        picks = Counter(self.sample_engine() for _ in range(max(1, n)))
        alloc = {e: picks.get(e, 0) for e in self.engines}

        # FORCED EXPLORATION. Discounting alone cannot rescue a collapsed arm, because rescaling
        # preserves the posterior MEAN: after the production collapse evo's mean (0.023) still sat
        # 200× above template's (0.000112), so template was never sampled, never generated fresh
        # evidence, and could never be discounted back into contention. A small guaranteed share
        # per engine is what makes the forgetting mechanism reachable — the standard fix for
        # tracking a non-stationary reward (Hartland/Sebag dynamic MAB; DiscountedTS).
        need_min = max(1, int(MIN_SHARE * max(1, n)))
        if n >= len(self.engines):
            for e in self.engines:
                if alloc[e] >= need_min:
                    continue
                deficit = need_min - alloc[e]
                for d in sorted(self.engines, key=lambda x: -alloc[x]):
                    if d == e or alloc[d] <= need_min:
                        continue
                    take = min(deficit, alloc[d] - need_min)
                    alloc[d] -= take; alloc[e] += take; deficit -= take
                    if deficit <= 0:
                        break

        if floors:                                           # guarantee a targeted-engine minimum
            for e, frac in floors.items():
                if e not in alloc:
                    continue
                need = int(np.ceil(frac * max(1, n)))
                deficit = need - alloc[e]
                if deficit <= 0:
                    continue
                donors = sorted((x for x in self.engines if x not in floors),
                                key=lambda x: -alloc[x])
                for d in donors:
                    take = min(deficit, alloc[d])
                    alloc[d] -= take; alloc[e] += take; deficit -= take
                    if deficit <= 0:
                        break
        return alloc

    def update(self, engine: str, reward: float) -> None:
        """Record one outcome, then age the posterior and cap its effective memory.

        The credit actually applied is the MAXIMUM reward in this engine's recent window (extreme
        value), so a rare breakthrough keeps an engine alive long enough to be tried again."""
        reward = float(max(0.0, min(1.0, reward)))
        if engine not in self.alpha:
            return
        self.recent[engine].append(reward)
        credit = max(self.recent[engine]) if self.recent[engine] else reward
        g = self.discount
        self.alpha[engine] = self.alpha[engine] * g + credit
        self.beta[engine] = self.beta[engine] * g + (1.0 - credit)
        total = self.alpha[engine] + self.beta[engine]
        if total > self.memory:                       # keep the posterior able to move again
            k = self.memory / total
            self.alpha[engine] *= k
            self.beta[engine] *= k
        self.alpha[engine] = max(1e-3, self.alpha[engine])
        self.beta[engine] = max(1e-3, self.beta[engine])

    def weights(self) -> Dict[str, float]:
        return {e: self.alpha[e] / (self.alpha[e] + self.beta[e]) for e in self.engines}

    # ─── persistence so the meta-controller compounds across marathons (docs/14) ──
    def snapshot(self) -> tuple:
        """(alpha, beta) copies for saving to the store."""
        return dict(self.alpha), dict(self.beta)

    def restore(self, state: Dict[str, tuple]) -> None:
        """Reload learned Beta posteriors ({engine: (alpha, beta)}) from a prior marathon, so the
        engine that was earning its keep keeps its budget instead of resetting to a uniform prior.

        Restored counts are RESCALED to the memory cap. Without this, a brain saved under the old
        unbounded scheme (β up to 33,205) would reload its own absorbing state and stay collapsed
        forever — the discounting below could never dig it out."""
        for e, ab in (state or {}).items():
            if e in self.alpha and ab:
                a, b = float(ab[0]), float(ab[1])
                total = a + b
                if total > self.memory:
                    k = self.memory / total
                    a *= k; b *= k
                self.alpha[e] = max(1e-3, a); self.beta[e] = max(1e-3, b)
