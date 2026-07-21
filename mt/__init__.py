"""Master Trader — the meta-layer strategy-discovery factory.

A closed loop that manufactures, simulates, validates, archives, and self-improves
trading strategies expressed as typed *genomes*. Sits above the existing per-market
stacks (CC_Trading / FX_Trading), reusing their battle-tested pure functions via
subprocess isolation (see mt.adapters) rather than rewriting them.

The null hypothesis is that every strategy is worthless; the whole machine exists to
*reject*, not to confirm. See docs/00..10 for the architecture.
"""
from __future__ import annotations

__version__ = "0.0.1"
