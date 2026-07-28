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
    fdr_threshold: Optional[float] = None                 # Stage-A BHY discovery threshold
    fdr_q: float = 0.10
    fresh_sigma: bool = False                             # Stage B: derive σ_SR from THIS series


STAGE_EXPLORE = "A"     # screening: FDR-controlled, N-independent, holdout is FORBIDDEN
STAGE_CONFIRM = "B"     # confirmation: full FWER Deflated Sharpe on a pre-registered finalist list


@dataclass
class GauntletReport:
    genome_id: str
    market: str
    passed: bool
    failed_gate: Optional[str]
    gates: Dict[str, dict] = field(default_factory=dict)
    fitness: Dict = field(default_factory=dict)
    scalar_fitness: float = float("-inf")
    stage: str = STAGE_EXPLORE

    @property
    def promoted(self) -> bool:
        """Cleared the exploratory screen — a CANDIDATE, never a tradeable verdict."""
        return self.passed and self.stage == STAGE_EXPLORE

    @property
    def cleared(self) -> bool:
        """Cleared the full confirmatory gauntlet on sealed data. The only tradeable verdict."""
        return self.passed and self.stage == STAGE_CONFIRM

    def summary_line(self) -> str:
        verdict = ("PROMOTE" if self.stage == STAGE_EXPLORE else "CLEAR") if self.passed \
            else f"REJECT@{self.failed_gate}"
        g4 = self.gates.get("G4_deflated_sharpe", {})
        return (f"{self.genome_id} [{self.market:6}] {verdict:16} stage={self.stage} "
                f"sharpe={g4.get('raw_sharpe')} dsr_p={g4.get('dsr_pvalue')}")


class Gauntlet:
    def run(self, genome: Genome, res: EvalResult, trial_count: int,
            ctx: Optional[GauntletContext] = None, stage: str = STAGE_EXPLORE) -> GauntletReport:
        """Run the gates for one stage.

        **Stage A (explore)** screens on `GS_screen` (FDR, N-independent) plus every cheap
        structural gate. G4's Deflated Sharpe is still COMPUTED — best-z remains the headline
        convergence metric — but it is advisory here, because a confirmatory max-statistic applied
        to every candidate is what kept the archive empty. G6 transfer is never run: the holdout
        must not be touched during exploration or it stops being out-of-sample.

        **Stage B (confirm)** enforces everything, including G4 at the pre-registered family size
        and G6 against the sealed holdout.

        Within a stage, all CHEAP gates are measured even after the first failure. The previous
        short-circuit saved compute but left the fitness vector mostly unfilled for the ~100% of
        genomes that fail, which collapsed NSGA-II's six objectives to two and removed the
        multi-objective diversity pressure the search depends on. Only the genuinely expensive
        rungs (G3 CPCV = m extra backtests, G6 = a holdout backtest) stay gated behind success."""
        report = GauntletReport(genome_id=genome.genome_id, market=genome.meta.market,
                                passed=False, failed_gate=None, stage=stage)
        if not res.ok:
            report.failed_gate = "G0_eval"
            report.gates["G0_eval"] = {"status": "fail", "reason": res.error or "no returns"}
            return report

        net = res.net_returns
        ppy = float(res.summary.get("periods_per_year", 365.0))
        seed = ctx.seed if ctx else res.seed
        sr_std = ctx.sr_trial_std if ctx else None
        fdr_thr = ctx.fdr_threshold if ctx else None
        fdr_q = ctx.fdr_q if ctx else G.FDR_Q
        explore = (stage == STAGE_EXPLORE)

        # STAGE B USES A FRESH-DATA NULL SPREAD, NOT THE EXPLORATORY LEDGER'S σ_SR.
        # E[max SR] = σ_SR·E[max of N] asks "how high would the best of N score by luck?". In
        # Stage A the observed cross-trial dispersion is the right answer. On the pre-registered
        # holdout no selection happened, so under the null each finalist's Sharpe is just a fresh
        # estimate whose spread is its own standard error ≈1/√T. Reusing the exploratory σ_SR there
        # charges for the selection a second time — it is 1.5–3.4× the fresh-data s.e., and since
        # E[max] scales linearly with σ it pushed the xau bar to a 0.43 per-period Sharpe, which
        # nothing can clear. Measured: same book, z −0.50 (shipped) vs +2.32 (fresh σ).
        if not explore and ctx is not None and ctx.fresh_sigma:
            from mt.adapters.cclib import sharpe_std_error
            fresh = sharpe_std_error(net.tolist())
            if fresh and fresh > 0:
                sr_std = fresh

        # (1) VALIDITY — a degenerate series makes every downstream statistic meaningless, so this
        # is the one place a hard short-circuit is still correct.
        g1 = G.g1_sanity(net)
        report.gates[g1.name] = {"status": g1.status, "reason": g1.reason, **g1.stats}
        if not g1.passed:
            report.failed_gate = g1.name
            report.fitness = self._fitness(genome, res, report)
            report.scalar_fitness = self._scalarize(report.fitness)
            return report

        # (2) CHEAP QUALITY — all measured, always, so failures still produce a full fitness vector.
        g4 = G.g4_deflated_sharpe(net, trial_count, ann_factor=ppy, sr_trial_std=sr_std)
        # G4 and G4b are BOTH family-wise-error instruments (parametric E[max SR] and a Šidák-
        # corrected bootstrap respectively). They belong to the same stage: enforcing G4b during
        # exploration while G4 is advisory would leave a confirmatory bar screening every
        # candidate through the back door — measured killing 159 candidates that had already
        # cleared the FDR screen. Both are measured always, enforced only at confirmation.
        g4b = G.g4b_reality_check(net, trial_count, seed=seed)
        cheap = [
            G.gs_screen(net, fdr_thr, q=fdr_q) if explore else g4.as_advisory(),
            g4.as_advisory() if explore else g4,
            g4b.as_advisory() if explore else g4b,
            G.g5_robustness(net, seed=seed),
            G.g2_oos_degradation(net),
            G.g7_capacity(genome, res, ctx),
            G.g8_orthogonality(res, ctx),
        ]
        passed_all = True
        for gate in cheap:
            report.gates[gate.name] = {"status": gate.status, "reason": gate.reason,
                                       "advisory": gate.advisory, **gate.stats}
            if gate.enforced and not gate.passed and passed_all:
                passed_all = False
                report.failed_gate = gate.name

        # (3) EXPENSIVE — only for survivors. G6 reads the sealed holdout and is CONFIRM-ONLY.
        if passed_all:
            expensive = [lambda: G.g3_cpcv_pbo(genome, ctx)]
            if not explore:
                expensive.append(lambda: G.g6_transfer(genome, ctx))
            for thunk in expensive:
                gate = thunk()
                report.gates[gate.name] = {"status": gate.status, "reason": gate.reason,
                                           "advisory": gate.advisory, **gate.stats}
                if gate.enforced and not gate.passed:
                    passed_all = False
                    report.failed_gate = gate.name
                    break

        report.passed = passed_all
        report.fitness = self._fitness(genome, res, report)
        report.scalar_fitness = self._scalarize(report.fitness)
        return report

    def _fitness(self, genome: Genome, res: EvalResult, report: GauntletReport) -> Dict:
        g4 = report.gates.get("G4_deflated_sharpe", {})
        g3 = report.gates.get("G3_cpcv_pbo", {})
        g7 = report.gates.get("G7_capacity", {})
        g8 = report.gates.get("G8_orthogonality", {})
        gs = report.gates.get("GS_screen", {})
        pbo = g3.get("pbo")
        return {
            "deflated_sharpe": g4.get("raw_sharpe"),
            "dsr_pvalue": g4.get("dsr_pvalue"),
            "dsr_z": g4.get("dsr_z"),
            # N-INDEPENDENT strength. Carried in the fitness vector so NSGA-II can rank on a
            # signal that does not move when the ledger grows (docs/15 §4).
            "edge_t": gs.get("edge_t"),
            "screen_p": gs.get("p_single"),
            "one_minus_pbo": None if pbo is None else round(1.0 - pbo, 3),
            "cpcv_oos_sharpe": g3.get("oos_sharpe_median"),   # CPCV OOS Sharpe distribution (B7)
            "capacity_sharpe_2x": g7.get("sharpe_2x_cost"),
            "neg_complexity": -genome.complexity(),
            "neg_archive_corr": None if g8.get("max_corr") is None else -g8["max_corr"],
            "similarity_penalty": g8.get("similarity_penalty"),
            "net_sharpe": res.summary.get("net_sharpe"),
            "max_dd": res.summary.get("max_dd"),
            "max_dd_duration": res.summary.get("max_dd_duration"),
            "phenotype": genome.meta.execution,
        }

    def _scalarize(self, fitness: Dict) -> float:
        return scalarize(fitness)


def scalarize(fitness: Dict) -> float:
    """The single ranking number for the archive and the hall of fame.

    Shared as a module function so `mt.store.db` can rank identically without importing the
    runner (the two used to be hand-copied and could silently drift apart).

    The similarity term is the AutoAlpha/WorldQuant device: rather than only forbidding a
    duplicate, DISCOUNT a candidate in proportion to how much it overlaps what we already hold.
    A hard gate blocks; a discount redirects — which is what a search that had collapsed onto
    near-clones of one idea actually needs."""
    ds = fitness.get("deflated_sharpe")
    if ds is None:
        ds = fitness.get("net_sharpe") or 0.0
    try:
        base = float(ds)
    except (TypeError, ValueError):
        base = 0.0
    omp = fitness.get("one_minus_pbo")
    if omp is not None:
        base *= max(0.0, float(omp))         # discount by overfitting probability
    sim = fitness.get("similarity_penalty")
    if sim is not None:
        base *= max(0.0, 1.0 - float(sim))   # discount by redundancy with the archive
    return base - 0.05 * abs(float(fitness.get("neg_complexity", 0) or 0))
