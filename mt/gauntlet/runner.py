"""mt.gauntlet.runner — run the gates and emit the multi-objective fitness vector.

A candidate must pass every *enforced* gate. Gates run cheap→expensive so most die early
(successive halving). The fitness vector is deliberately multi-objective to avoid Goodhart
(docs/05 §4): it fills the objectives measured and leaves the rest None so the archive
scalarization is honest about what it optimizes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from mt.genome.schema import Genome
from mt.sim.evalresult import EvalResult
from mt.gauntlet import gates as G


@dataclass
class GauntletContext:
    """Everything the re-evaluating gates (G3 CPCV, G6 transfer) and G8 need."""
    eval_fn: Optional[Callable] = None            # (genome, panel) -> EvalResult
    panel: object = None                          # the search panel (for CPCV variants)
    holdout_panel: object = None                  # locked, unseen (for transfer)
    archive_returns: Dict = field(default_factory=dict)   # niche -> return array (for orthogonality)
    seed: int = 4242
    sr_trial_std: Optional[float] = None                  # ledger σ_SR for the DSR deflation
    cpcv_variants: int = 3
    cpcv_groups: int = 6


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
        g4 = self.gates.get("G4_deflated_sharpe", {})
        return f"{self.genome_id} [{self.market:6}] {verdict:22} sharpe={g4.get('raw_sharpe')} dsr_p={g4.get('dsr_pvalue')}"


class Gauntlet:
    def run(self, genome: Genome, res: EvalResult, trial_count: int,
            ctx: Optional[GauntletContext] = None) -> GauntletReport:
        report = GauntletReport(genome_id=genome.genome_id, market=genome.meta.market,
                                passed=False, failed_gate=None)
        if not res.ok:
            report.failed_gate = "G0_eval"
            report.gates["G0_eval"] = {"status": "fail", "reason": res.error or "no returns"}
            return report

        net = res.net_returns
        ppy = float(res.summary.get("periods_per_year", 365.0))
        seed = ctx.seed if ctx else res.seed

        # cheap → expensive (all enforced; first failure short-circuits the rest)
        sr_std = ctx.sr_trial_std if ctx else None
        ordered = [
            G.g1_sanity(net),
            G.g4_deflated_sharpe(net, trial_count, ann_factor=ppy, sr_trial_std=sr_std),
            G.g4b_reality_check(net, trial_count, seed=seed),
            G.g5_robustness(net, seed=seed),
            G.g2_oos_degradation(net),
            G.g7_capacity(genome, res, ctx),
            G.g8_orthogonality(res, ctx),
            G.g3_cpcv_pbo(genome, ctx),
            G.g6_transfer(genome, ctx),
        ]

        passed_all = True
        for gate in ordered:
            report.gates[gate.name] = {"status": gate.status, "reason": gate.reason, **gate.stats}
            if gate.enforced and not gate.passed and passed_all:
                passed_all = False
                report.failed_gate = gate.name

        report.passed = passed_all
        report.fitness = self._fitness(genome, res, report)
        report.scalar_fitness = self._scalarize(report.fitness)
        return report

    def _fitness(self, genome: Genome, res: EvalResult, report: GauntletReport) -> Dict:
        g4 = report.gates.get("G4_deflated_sharpe", {})
        g3 = report.gates.get("G3_cpcv_pbo", {})
        g7 = report.gates.get("G7_capacity", {})
        g8 = report.gates.get("G8_orthogonality", {})
        pbo = g3.get("pbo")
        return {
            "deflated_sharpe": g4.get("raw_sharpe"),
            "dsr_pvalue": g4.get("dsr_pvalue"),
            "one_minus_pbo": None if pbo is None else round(1.0 - pbo, 3),
            "cpcv_oos_sharpe": g3.get("oos_sharpe_median"),   # CPCV OOS Sharpe distribution (B7)
            "capacity_sharpe_2x": g7.get("sharpe_2x_cost"),
            "neg_complexity": -genome.complexity(),
            "neg_archive_corr": None if g8.get("max_corr") is None else -g8["max_corr"],
            "net_sharpe": res.summary.get("net_sharpe"),
            "max_dd": res.summary.get("max_dd"),
            "max_dd_duration": res.summary.get("max_dd_duration"),
            "phenotype": genome.meta.execution,
        }

    def _scalarize(self, fitness: Dict) -> float:
        ds = fitness.get("deflated_sharpe")
        if ds is None:
            ds = fitness.get("net_sharpe") or 0.0
        base = float(ds)
        omp = fitness.get("one_minus_pbo")
        if omp is not None:
            base *= max(0.0, omp)            # discount by overfitting probability
        return base - 0.05 * abs(fitness.get("neg_complexity", 0))
