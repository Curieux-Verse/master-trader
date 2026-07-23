"""mt.improve.loop — the inner discovery loop (docs/06 §7).

One generation = generate (budget split across engines by the bandit) → simulate → ledger →
gauntlet → archive → critic (lessons + targeted fixes) → bandit reallocation. Every loop the
archive gets more diverse and robust, the lesson library gets wiser, and the generators get
better-aimed. Breadth is enforced structurally: the bandit funds *all* engines, the archive
niches by behaviour, and no family is privileged — the Gauntlet decides.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from mt.generators import TemplateSampler
from mt.genome.schema import Genome, SignalSpec, SizingSpec, RiskSpec
from mt.sim import evaluate
from mt.gauntlet import Gauntlet, GauntletContext
from mt.archive import MapElites
from mt.store import MTStore
from mt.improve import nsga2, miner as miner_mod
from mt.improve.bandit import EngineBandit
from mt.improve.critic import critique, families


@dataclass
class EngineMix:
    produced: Dict[str, int] = field(default_factory=dict)
    admits: Dict[str, int] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)


class DiscoveryLoop:
    def __init__(self, store: MTStore, market: str, panel, holdout_panel=None,
                 seed: int = 4242, use_ollama: bool = False):
        self.store = store
        self.market = market
        self.panel = panel
        self.holdout = holdout_panel
        self.seed = seed
        self.use_ollama = use_ollama
        self.sampler = TemplateSampler(seed=seed)
        self.bandit = EngineBandit(seed=seed)
        self.gauntlet = Gauntlet()
        self.archive = MapElites(store)
        self.rng = np.random.default_rng(seed)
        self.parents: List[Tuple[Genome, object]] = []
        self.archive_returns: Dict[str, np.ndarray] = {}
        self.pending_mutations: List[Genome] = []
        self.generation = 0

    # ─── one generation ──────────────────────────────────────────────────
    def run_generation(self, batch_size: int = 16) -> dict:
        self.generation += 1
        alloc = self.bandit.allocate(batch_size)
        produced: List[Tuple[Genome, str]] = []
        for engine, cnt in alloc.items():
            for g in self._generate(engine, cnt):
                produced.append((g, engine))

        sr_std = self.store.sr_trial_std(self.market)
        ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, self.seed), panel=self.panel,
                              holdout_panel=self.holdout, archive_returns=self.archive_returns,
                              seed=self.seed, sr_trial_std=sr_std)

        mix = EngineMix(produced=Counter(), admits=Counter())
        fam_tested: Counter = Counter()
        pheno_tested: Counter = Counter()
        new_reports: List[Tuple[Genome, object]] = []

        for g, engine in produced:
            mix.produced[engine] += 1
            for t in families(g):
                fam_tested[t] += 1
            pheno_tested[g.meta.execution] += 1

            self.store.register_genome(g)
            res = evaluate(g, self.panel, self.seed)
            self.store.record_eval(res)
            n_trials = self.store.trial_count(self.market)     # per-market N, paired with per-market σ_SR
            report = self.gauntlet.run(g, res, trial_count=n_trials, ctx=ctx)
            self.store.record_gauntlet(g.genome_id, self.market, report.passed,
                                       report.failed_gate, report.gates, report.fitness)

            reward = 0.0
            if report.passed:
                outcome = self.archive.insert(g, res, report)
                if outcome.action in ("occupy", "replace"):
                    reward = 1.0
                    self.archive_returns[outcome.niche] = res.net_returns.to_numpy()
                else:
                    reward = 0.3
                mix.admits[engine] += 1

            if report.passed or self.rng.random() < 0.15:
                out = critique(g, report, res, self.store, self.rng, use_ollama=self.use_ollama)
                if out["suggested_mutation"] is not None and len(self.pending_mutations) < 24:
                    self.pending_mutations.append(out["suggested_mutation"])

            self.bandit.update(engine, reward)
            new_reports.append((g, report))

        # refresh the NSGA-II parent pool (elitist: keep the best across generations). Only
        # genomes that produced a usable backtest are eligible to breed; pair each survivor with
        # its OWN report (index-based) so cross-generation Pareto ranking stays honest.
        pool = self.parents + [(g, r) for g, r in new_reports if r.passed or r.scalar_fitness > float("-inf")]
        if pool:
            idx = nsga2.select_parent_indices([r for _, r in pool], k=12)
            self.parents = [pool[i] for i in idx]
        else:
            self.parents = []

        mix.weights = self.bandit.weights()
        return {
            "generation": self.generation,
            "produced": dict(mix.produced), "admits": dict(mix.admits),
            "bandit_weights": {k: round(v, 3) for k, v in mix.weights.items()},
            "families_tested": dict(fam_tested), "phenotypes_tested": dict(pheno_tested),
            "archive_coverage": self.archive.coverage(),
            "lessons": self.store.lesson_count(),
            "sr_trial_std": None if sr_std is None else round(sr_std, 5),
        }

    # ─── engines ─────────────────────────────────────────────────────────
    def _generate(self, engine: str, cnt: int) -> List[Genome]:
        if cnt <= 0:
            return []
        if engine == "template":
            kinds = [k for k in self.sampler.ARCHETYPES]
            from mt.config import MARKETS
            if not MARKETS[self.market].has_funding:
                kinds = [k for k in kinds if k != "carry"]
            return [self.sampler._archetype(self.market, kinds[int(self.rng.integers(len(kinds)))])
                    for _ in range(cnt)]
        if engine == "random":
            return [self.sampler._random(self.market) for _ in range(cnt)]
        if engine == "evo":
            if self.parents:
                kids = nsga2.breed([g for g, _ in self.parents], cnt, self.rng)
                return kids or [self.sampler._random(self.market) for _ in range(cnt)]
            return [self.sampler._random(self.market) for _ in range(cnt)]
        if engine == "miner":
            return self._mine(cnt)
        if engine == "llm":
            out = self.pending_mutations[:cnt]
            self.pending_mutations = self.pending_mutations[cnt:]
            while len(out) < cnt:
                out.append(self.sampler._random(self.market))
            return out
        return [self.sampler._random(self.market) for _ in range(cnt)]

    def _mine(self, cnt: int) -> List[Genome]:
        if self.rng.random() < 0.4:                      # occasionally grow the vocabulary
            miner_mod.mint_interaction(self.panel, self.rng)
            self.store.record_screening(self.market, 1, kind="miner_intx")   # 1 IC-screened pair
        n_cand = max(9, cnt * 3)
        seeds = miner_mod.mine_features(self.panel, n_candidates=n_cand, rng=self.rng, top=cnt)
        # every candidate the miner IC-screened is a hidden selection trial; charge the ones it
        # did NOT promote to a genome (the promoted ones get their own ledger eval below).
        self.store.record_screening(self.market, max(0, n_cand - len(seeds)), kind="miner_ic")
        genomes: List[Genome] = []
        for i, (fnode, _ic) in enumerate(seeds):
            fnode.id = "f1"
            g = Genome(self.sampler._meta(self.market), [fnode],
                       SignalSpec("weighted_blend", {"direction": "neutral"}),
                       SizingSpec("rank_bucket", {"top_frac": 0.2, "gross": 1.0, "per_name_cap": 0.15}),
                       RiskSpec("horizon_hold", {"horizon": 6, "cost_stress": 1.0}),
                       generator="miner")
            genomes.append(g)
        while len(genomes) < cnt:
            genomes.append(self.sampler._random(self.market))
        return genomes
