"""mt.adapters — isolated reuse of the per-market stacks.

Each market (crypto/CC_Trading, fx & xau/FX_Trading) exposes its pure functions through
a subprocess worker launched with that stack's root on PYTHONPATH. Because the stacks
share top-level package names (core/xsec/backtest/concepts), this per-process isolation
is the *only* safe way to touch more than one of them in a single run.
"""
from mt.adapters.market import MarketAdapter, build_all_panels

__all__ = ["MarketAdapter", "build_all_panels"]
