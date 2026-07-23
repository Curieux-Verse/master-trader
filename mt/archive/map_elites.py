"""mt.archive.map_elites — behavioral niching over the Result Ledger's survivors.

Niche = (market, holding-period bucket, turnover bucket, exposure style) — a thin instance
of the docs/06 §2 axes [holding × regime × exposure]. Regime/factor-tilt axes attach as
G5 regime slicing and attribution come online. Occupy an empty cell; replace a less-fit
incumbent; otherwise the newcomer is compost for the critic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from mt.genome.schema import Genome
from mt.gauntlet.runner import GauntletReport
from mt.sim.evalresult import EvalResult
from mt.store.db import MTStore


def niche_key(market: str, descriptor: dict) -> str:
    return ":".join([
        market,
        str(descriptor.get("hold_bucket", "?")),
        str(descriptor.get("turnover_bucket", "?")),
        str(descriptor.get("exposure_bucket", "?")),
        str(descriptor.get("regime", "all")),          # regime as a diversity axis (docs/06)
    ])


@dataclass
class InsertOutcome:
    niche: str
    action: str          # "occupy" | "replace" | "keep"
    scalar_fitness: float


class MapElites:
    def __init__(self, store: MTStore):
        self.store = store

    def insert(self, genome: Genome, res: EvalResult, report: GauntletReport) -> InsertOutcome:
        """Insert a gauntlet-passing genome into its behavioral niche."""
        nk = niche_key(genome.meta.market, res.behavioral_descriptor)
        action = self.store.upsert_archive(
            niche_key=nk, genome_id=genome.genome_id, market=genome.meta.market,
            fitness=report.fitness, descriptor=res.behavioral_descriptor,
            scalar_fit=report.scalar_fitness,
        )
        return InsertOutcome(niche=nk, action=action, scalar_fitness=report.scalar_fitness)

    def coverage(self) -> int:
        return len(self.store.archive_rows())

    def elites(self) -> List:
        return self.store.archive_rows()
