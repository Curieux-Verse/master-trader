"""mt.archive — the quality-DIVERSITY archive (MAP-Elites), not a leaderboard.

A grid of behavioral niches, each holding the single best (by scalar fitness) genome whose
behavior falls in that cell. This forces coverage of the behavioral space, so the stable is
genuinely diverse — the "dozens of concurrent, different strategies" requirement satisfied
by design, and a portfolio robust because its members fail at different times (docs/06 §2).
"""
from mt.archive.map_elites import MapElites

__all__ = ["MapElites"]
