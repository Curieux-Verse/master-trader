"""mt.gauntlet.runner — run the gates in sequence and emit the fitness vector.

A candidate must pass every *enforced* gate. The fitness vector (docs/05 §4) is
deliberately multi-objective to avoid Goodhart; the thin slice fills the objectives it can
measure (deflated Sharpe, complexity) and marks the rest as pending so the archive
scalarization is honest about what it optimizes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from mt.genome.schema import Genome
from mt.sim.evalresult import EvalResult
from mt.gauntlet import gates as G


@dataclass
class GauntletReport:
    genome_id: str
    market: str
    passed: bool
    failed_gate: Optional[str]
    gates: Dict[str, dict] = field(default_factory=dict)
    fitness: Dict = field(default_factory=dict)
    scalar_fitness: float = float("-inf")

    def summary_line(self) -> str:
        verdict = "ADMIT" if self.passed else f"REJECT@{self.failed_gate}"
        dsr = self.gates.get("G4_deflated_sharpe", {}).get("raw_sharpe")
        p = self.gates.get("G4_deflated_sharpe", {}).get("dsr_pvalue")
        return f"{self.genome_id} [{self.market:6}] {verdict:22} sharpe={dsr} dsr_p={p}"


class Gauntlet:
    """Sequential gate runner. `trial_count` comes from the Result Ledger — the honest N."""

    def run(self, genome: Genome, res: EvalResult, trial_count: int) -> GauntletReport:
        market = genome.meta.market
        gid = genome.genome_id
        report = GauntletReport(genome_id=gid, market=market, passed=False, failed_gate=None)

        if not res.ok:
            report.failed_gate = "G0_eval"
            report.gates["G0_eval"] = {"status": "fail", "reason": res.error or "no returns"}
            return report

        net = res.net_returns
        ppy = float(res.summary.get("periods_per_year", 365.0))
        ordered: List[G.GateResult] = [
            G.g1_sanity(net),
            G.g2_purged_wf(),
            G.g3_cpcv_pbo(),
            G.g4_deflated_sharpe(net, trial_count, ann_factor=ppy),
            G.g5_robustness(net, seed=res.seed),
            G.g6_transfer(),
            G.g7_capacity(),
            G.g8_orthogonality(),
        ]

        passed_all = True
        for gate in ordered:
            report.gates[gate.name] = {"status": gate.status, "reason": gate.reason, **gate.stats}
            if gate.enforced and not gate.passed and passed_all:
                passed_all = False
                report.failed_gate = gate.name  # first hard failure

        report.passed = passed_all
        report.fitness = self._fitness(genome, res, report)
        report.scalar_fitness = self._scalarize(report.fitness)
        return report

    def _fitness(self, genome: Genome, res: EvalResult, report: GauntletReport) -> Dict:
        g4 = report.gates.get("G4_deflated_sharpe", {})
        return {
            "deflated_sharpe": g4.get("raw_sharpe"),      # skill after trial correction (maximize)
            "dsr_pvalue": g4.get("dsr_pvalue"),
            "one_minus_pbo": None,                        # G3 pending
            "regime_breadth": None,                       # G5 regime slicing pending
            "capacity_usd": None,                         # G7 pending
            "neg_complexity": -genome.complexity(),       # Occam (minimize nodes)
            "neg_archive_corr": None,                     # G8 pending
            "net_sharpe": res.summary.get("net_sharpe"),
            "max_dd": res.summary.get("max_dd"),
        }

    def _scalarize(self, fitness: Dict) -> float:
        """Single scalar for archive replacement (a projection of the Pareto objectives)."""
        ds = fitness.get("deflated_sharpe")
        if ds is None:
            ds = fitness.get("net_sharpe") or 0.0
        complexity_pen = -0.05 * abs(fitness.get("neg_complexity", 0))
        return float(ds) + complexity_pen
