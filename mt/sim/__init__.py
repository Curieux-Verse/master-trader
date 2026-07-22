"""mt.sim — the multi-fidelity simulator.

Thin slice = Tier 1 only: a vectorized, cost-aware, cross-sectional backtest that mirrors
CC_Trading's backtest/engine.py but is *genome-driven* (features/weights/horizon chosen by
the genome, not hard-coded) and market-agnostic. Tier-2 (event-driven) and Tier-3 (tick)
are the P1 deepening. Every tier emits the same EvalResult (docs/04 §5).
"""
from mt.sim.evalresult import EvalResult
from mt.sim.executor import Tier1Executor
from mt.sim.directional import Tier2Executor
from mt.sim.simulate import evaluate

__all__ = ["EvalResult", "Tier1Executor", "Tier2Executor", "evaluate"]
