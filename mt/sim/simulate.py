"""mt.sim.simulate — phenotype-aware dispatcher (Tier-1 cross-sectional / Tier-2 directional).

The genome's `meta.execution` gene selects the engine, so the *same* search explores both a
rank-bucket book AND per-symbol directional trading. Both emit the one EvalResult contract.
"""
from __future__ import annotations

from mt.data.panel import NormPanel
from mt.genome.schema import Genome
from mt.sim.evalresult import EvalResult
from mt.sim.executor import Tier1Executor
from mt.sim.directional import Tier2Executor


def evaluate(genome: Genome, panel: NormPanel, seed: int = 4242) -> EvalResult:
    if genome.meta.execution == "directional":
        return Tier2Executor(seed).evaluate(genome, panel)
    return Tier1Executor(seed).evaluate(genome, panel)
