"""mt.improve — the self-improvement loop (docs/06): all three mechanisms, each where best.

  • Evolutionary (NSGA-II + the QD archive) improves the *strategies* — nsga2.py
  • LLM/heuristic critic (Reflexion/Voyager) improves the *hypotheses & lessons* — critic.py
  • Bandit meta-controller improves *where to spend search* — bandit.py
  • Factor miner mints IC-positive primitives data-first — miner.py

The inner discovery loop (loop.py) ties generators → simulator → gauntlet → archive →
critic → bandit, so every generation the archive gets more diverse and robust, the lesson
library gets wiser, and the generators get better-aimed. That compounding is the asset.
"""
from mt.improve.loop import DiscoveryLoop, EngineMix

__all__ = ["DiscoveryLoop", "EngineMix"]
