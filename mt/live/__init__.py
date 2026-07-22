"""mt.live — the paper/shadow rung and live adaptation (docs/07).

The deliverable formally STOPS at paper/shadow (R1). The machine recommends promotions but
NEVER self-authorizes a live-capital action (docs/07 §6). This layer generalizes shadow
trading (run archive genomes on a live feed through the SAME simulator), adds a regime-aware
online allocator, and a graduated drift-response ladder (Page-Hinkley / rolling PSR /
circuit breakers) so decayed strategies are quarantined before they matter.
"""
from mt.live.paper import PaperBook
from mt.live.allocator import HedgeAllocator
from mt.live.drift import PageHinkley, DriftMonitor

__all__ = ["PaperBook", "HedgeAllocator", "PageHinkley", "DriftMonitor"]
