"""mt.improve.loop — the inner discovery loop (docs/06 §7).

One generation = generate (budget split across engines by the bandit) → simulate → ledger →
gauntlet → archive → critic (lessons + targeted fixes) → bandit reallocation. Every loop the
archive gets more diverse and robust, the lesson library gets wiser, and the generators get
better-aimed. Breadth is enforced structurally: the bandit funds *all* engines, the archive
niches by behaviour, and no family is privileged — the Gauntlet decides.
"""
from __future__ import annotations

import json
import math
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional, Tuple

import numpy as np

from mt.generators import TemplateSampler
from mt.genome.schema import Genome, SignalSpec, SizingSpec, RiskSpec
from mt.genome.registry import REGISTRY
from mt.sim import evaluate
from mt.gauntlet import Gauntlet, GauntletContext, GauntletReport
from mt.gauntlet.runner import STAGE_EXPLORE
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
    reused: int = 0             # evaluations that repeated a known genome (charged no new trial)


class DiscoveryLoop:
    def __init__(self, store: MTStore, market: str, panel, holdout_panel=None,
                 seed: int = 4242, use_ollama: bool = False, explore_floor=None):
        self.store = store
        self.market = market
        self.panel = panel
        self.holdout = holdout_panel
        self.seed = seed
        self.use_ollama = use_ollama
        # optional targeted-engine floor (e.g. {"evo":0.3,"miner":0.2}) so a long unattended
        # search keeps spending N on directed engines, not blind random (docs/06 §4).
        self.explore_floor = explore_floor
        self.sampler = TemplateSampler(seed=seed)
        self.bandit = EngineBandit(seed=seed)
        self.bandit.restore(store.load_bandit(market))       # compound the meta-controller (docs/14)
        self.gauntlet = Gauntlet()
        self.archive = MapElites(store)
        self.rng = np.random.default_rng(seed)
        self.parents: List[Tuple[Genome, object]] = []
        self.archive_returns: Dict[str, np.ndarray] = {}
        self.member_returns: Dict[str, object] = {}          # genome_id → net returns, for the book
        self.pending_mutations: List[Genome] = []
        # G10's empirical reference: edge_t of RANDOMLY CONSTRUCTED genomes on this panel. Bounded
        # and rolling, because the panel it describes is fixed but the sample should stay recent
        # enough to reflect the current lake snapshot.
        self.random_ref: Deque[float] = deque(maxlen=400)
        self.generation = 0
        # Rebuild the miner's persisted vocabulary FIRST: warm-start reconstructs genomes from the
        # store, and any genome built on a minted intx_* op fails typecheck until its op exists
        # again — which is how the most-evolved elites were being silently dropped every marathon.
        self.restored_ops = miner_mod.restore_minted(store)
        self.op_weights = store.feature_op_weights(market)   # measured ΔDSR-z → search direction
        self.warm_started = self._warm_start_parents()       # seed evolution from the best-ever frontier

    def _warm_start_parents(self, k: int = 12, pool_mult: int = 3) -> int:
        """Seed the NSGA-II parent pool from the hall-of-fame so evolution CONTINUES from the
        best-ever frontier instead of re-exploring from random every marathon (docs/14). Parents
        are reconstructed from the PERSISTED report fitness — no re-evaluation, so the honest
        Deflated-Sharpe trial count is untouched (re-testing a known genome is not a new trial).

        Selection is by CURIOSITY over a wider candidate pool, then filtered for structural
        diversity. Taking the top-k by dsr_z alone (the previous rule) returned twelve near-clones
        in production, so the compounding mechanism was faithfully compounding a single idea; and
        z ranks by score, whereas what a stalled search needs is parents that have historically
        been productive stepping stones (Monte Carlo Elites)."""
        cands: List[Tuple[Genome, object]] = []
        seen = set()
        rows = list(self.store.hof_top(self.market, limit=k * pool_mult, order="curiosity"))
        rows += list(self.store.hof_top(self.market, limit=k * pool_mult, order="z"))
        for r in rows:
            gid = r["genome_id"]
            if gid in seen:
                continue
            seen.add(gid)
            g = self.store.get_genome(gid)
            if g is None or not g.typecheck()[0]:
                continue
            try:
                fitness = json.loads(r["fitness"]) if r["fitness"] else {}
            except Exception:
                fitness = {}
            sf = r["scalar_fit"]
            rep = GauntletReport(genome_id=gid, market=self.market, passed=bool(r["passed"]),
                                 failed_gate=None, gates={}, fitness=fitness,
                                 scalar_fitness=float(sf) if sf is not None else 0.0)
            cands.append((g, rep))
        if len(cands) > k:
            idx = nsga2.diverse_subset([g for g, _ in cands], k)
            cands = [cands[i] for i in idx]
        self.parents = cands
        return len(cands)

    # ─── Stage-A screening threshold ─────────────────────────────────────
    def _fdr_threshold(self) -> float:
        """The BHY discovery threshold for this generation, from the recent trial population.

        Recomputed each generation because it is a property of the CURRENT candidate distribution,
        not a fixed constant — that is what makes it a false-DISCOVERY-rate control rather than an
        arbitrary p-value cutoff."""
        from mt.gauntlet.multipletest import bhy_threshold
        from mt.gauntlet.gates import FDR_Q
        pvals = self.store.recent_pvalues(self.market, sample=500)
        return bhy_threshold(pvals, q=FDR_Q)

    # ─── one generation ──────────────────────────────────────────────────
    def run_generation(self, batch_size: int = 16) -> dict:
        self.generation += 1
        alloc = self.bandit.allocate(batch_size, floors=self.explore_floor)
        produced: List[Tuple[Genome, str]] = []
        for engine, cnt in alloc.items():
            for g in self._generate(engine, cnt):
                produced.append((g, engine))

        # cross-trial σ_SR for the DSR deflation: per-market, but borrow the GLOBAL ledger dispersion
        # when this market is still cold (< 8 finite trials) so a sparse market isn't deflated with the
        # weak per-candidate fallback. If even the global ledger is cold, G4 fails closed (docs/14).
        sr_std = self.store.sr_trial_std(self.market) or self.store.sr_trial_std(None)
        rho = self.store.avg_trial_corr(self.market)         # P&L co-movement → effective trial count
        keff = self.store.effective_trials(self.market, rho)
        fdr_thr = self._fdr_threshold()
        # NOTE holdout_panel is deliberately NOT passed during exploration. G6 transfer is
        # confirm-only now; leaving the sealed panel reachable here is exactly how the last
        # production run ended up reading it 23,030 times (docs/15 §4).
        ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, self.seed), panel=self.panel,
                              holdout_panel=None, archive_returns=self.archive_returns,
                              seed=self.seed, sr_trial_std=sr_std, fdr_threshold=fdr_thr,
                              random_ref=list(self.random_ref),
                              random_ref_k=max(1, len(produced)))

        mix = EngineMix(produced=Counter(), admits=Counter())
        fam_tested: Counter = Counter()
        pheno_tested: Counter = Counter()
        new_reports: List[Tuple[Genome, object]] = []
        dsr_z: List[float] = []                              # distance-to-bar (N-aware): how close to G4
        edge_t: List[float] = []                             # single-strategy t-stat (N-INDEPENDENT): learning

        for g, engine in produced:
            mix.produced[engine] += 1
            for t in families(g):
                fam_tested[t] += 1
            pheno_tested[g.meta.execution] += 1

            self.store.register_genome(g)
            res = evaluate(g, self.panel, self.seed)
            _eid, is_new_trial = self.store.record_eval(res)
            if not is_new_trial:
                mix.reused += 1                              # a repeat is not a new hypothesis
            n_eff = int(keff["n_eff"])
            report = self.gauntlet.run(g, res, trial_count=n_eff, ctx=ctx, stage=STAGE_EXPLORE)
            self.store.record_gauntlet(g.genome_id, self.market, report.passed,
                                       report.failed_gate, report.gates, report.fitness)

            spp = res.summary.get("sharpe_pp"); npd = res.summary.get("n_periods", 0)
            et = (float(spp) * np.sqrt(npd)) if (spp is not None and np.isfinite(spp) and npd > 1) else None
            if et is not None:
                edge_t.append(et)                            # SR·√T — significance free of the N penalty
                # G10's reference distribution is built from the genomes the `random` engine was
                # going to produce anyway, so the empirical bar costs no extra backtests. It has
                # to come from RANDOM construction specifically: evolved genomes are the thing
                # being tested, and calibrating a bar on them would compare the search to itself.
                if engine == "random":
                    self.random_ref.append(et)

            # CYCLE-LEVEL memory: one fact row per family tag, so "which families die where" is a
            # GROUP BY instead of unparseable prose (docs/15 §3).
            g4stats = report.gates.get("G4_deflated_sharpe", {}) or {}
            z = g4stats.get("dsr_z")
            self.store.record_trial_facts(
                g.genome_id, self.market, families(g), g.meta.execution,
                str(g.signal.args.get("regime", "all")), g.sizing.op,
                report.failed_gate, report.promoted,
                float(z) if (z is not None and np.isfinite(z)) else None, et)

            reward = 0.0
            if report.promoted:
                outcome = self.archive.insert(g, res, report)
                if outcome.action in ("occupy", "replace"):
                    # OCCUPYING A NEW NICHE AND BEATING AN INCUMBENT ARE NOT THE SAME ACHIEVEMENT.
                    # Rewarding both at 1.0 quietly handed the whole budget to `evo`: beating a
                    # tuned incumbent on raw fitness is something only an evolved child of that
                    # incumbent can usually do, while opening an unexplored cell is precisely what
                    # template/random/miner/llm exist for. With one flat reward the exploratory
                    # engines could never score, and the archive sat at 26 of ~540 cells (4.8%)
                    # while `evo` refined the same ones. Discovery now pays strictly more.
                    reward = 1.0 if outcome.action == "occupy" else 0.6
                    self.archive_returns[outcome.niche] = res.net_returns.to_numpy()
                    self.member_returns[g.genome_id] = res.net_returns
                else:
                    reward = 0.3
                mix.admits[engine] += 1
                for p in (g.parents or []):                  # curiosity: reward the stepping stone
                    self.store.bump_curiosity(p, 1.0)
            else:
                for p in (g.parents or []):
                    self.store.bump_curiosity(p, -0.5)

            # Post-mortem on every promotion, and on failures weighted toward NEAR-MISSES rather
            # than uniformly at random: a genome that missed by a hair carries far more information
            # than one that was never close, and the old flat 15% sample spent most of its budget
            # on the latter.
            near = (et is not None and et > 0.5)
            if report.promoted or (self.rng.random() < (0.5 if near else 0.08)):
                out = critique(g, report, res, self.store, self.rng, use_ollama=self.use_ollama,
                               op_weights=self.op_weights,
                               avoid=[p for p, _ in self.parents])
                if out["suggested_mutation"] is not None and len(self.pending_mutations) < 24:
                    self.pending_mutations.append(out["suggested_mutation"])

            # only trust the DSR z when the deflation is reliable (a warm ledger σ_SR, or a tiny
            # family): a cold-ledger, under-deflated z must NOT enter best-z / the hall-of-fame, or it
            # would inflate the all-time high-water mark permanently (docs/14 cold-ledger hardening).
            if z is not None and np.isfinite(z) and g4stats.get("reliable", True):
                dsr_z.append(float(z))
                # persist the best-ever high-water mark (independent of the pass bar) so best-z
                # ratchets across marathons and warm-start has elites to breed from (docs/14).
                self.store.upsert_hof(g.genome_id, self.market, float(z), report.scalar_fitness,
                                      report.passed, report.fitness, res.summary.get("sharpe_pp"),
                                      edge_t=et)
                if not report.promoted:
                    # dense shaping: credit the engine for producing NEAR-MISSES too, scaled by how
                    # close to the bar — but capped at 0.25, strictly below the keep(0.3)/occupy(1.0)
                    # rewards, so clearing the screen always dominates.
                    reward = max(reward, min(0.25, 0.25 * max(0.0, float(z) / 1.645)))
            # ATTRIBUTION now triggers on edge_t, which is N-INDEPENDENT. The old `dsr_z > 0.5`
            # trigger fired less and less as the ledger grew — measured at 0 rows across a
            # 25-generation run — so the one mechanism producing hard per-primitive evidence shut
            # itself off exactly as the search matured (docs/15 §3.2).
            if et is not None and et > 1.0 and len(g.features) > 1:
                self._attribute(g, float(z) if (z is not None and np.isfinite(z)) else 0.0,
                                n_eff, sr_std)

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
        a, b = self.bandit.snapshot()
        self.store.save_bandit(self.market, a, b)            # persist the learned engine budget (docs/14)
        # refresh the measured search direction for the next generation
        self.op_weights = self.store.feature_op_weights(self.market)
        # Two distinct signals: edge_t median (N-INDEPENDENT — is generation finding more raw edge?
        # rising ⇒ learning, flat ⇒ space exhausted) and dsr_z best (N-aware — how close the single
        # closest genome is to actually clearing G4 right now).
        return {
            "generation": self.generation,
            "produced": dict(mix.produced), "admits": dict(mix.admits),
            "reused_evals": mix.reused,
            "bandit_weights": {k: round(v, 3) for k, v in mix.weights.items()},
            "families_tested": dict(fam_tested), "phenotypes_tested": dict(pheno_tested),
            "archive_coverage": self.archive.coverage(self.market),
            "qd_score": round(self.archive.qd_score(self.market), 4),
            "lessons": self.store.lesson_count(),
            "sr_trial_std": None if sr_std is None else round(sr_std, 5),
            "trial_corr": None if rho is None else round(rho, 4),
            "raw_trials": keff["n_total"],
            "effective_trials": int(keff["n_eff"]),
            "keff_method": keff["method"],
            "fdr_threshold": None if fdr_thr is None else round(fdr_thr, 6),
            "promoted": sum(mix.admits.values()),
            "edge_t_median": None if not edge_t else round(float(np.median(edge_t)), 4),
            "edge_t_best": None if not edge_t else round(float(np.max(edge_t)), 4),
            "dsr_z_best": None if not dsr_z else round(float(np.max(dsr_z)), 4),
            "n_backtested": len(edge_t),
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
            return [self.sampler._archetype(self.market, self._pick_archetype(kinds))
                    for _ in range(cnt)]
        if engine == "random":
            # Half blind, half AIMED AT AN EMPTY CELL. Blind sampling kept re-landing in the same
            # few niches: the production archive held 26 of ~540 reachable cells (4.8%) with the
            # `short` exposure bucket empty in every market, so QD-score sat flat at +9.11 while
            # the search reported 26k "admissions" that were all replacements of the same
            # incumbents. Goal-switching toward unoccupied cells is the standard MAP-Elites answer.
            aimed = cnt // 2
            return ([self._targeted(self.market) for _ in range(aimed)] +
                    [self.sampler._random(self.market) for _ in range(cnt - aimed)])
        if engine == "evo":
            if self.parents:
                kids = nsga2.breed([g for g, _ in self.parents], cnt, self.rng,
                                   op_weights=self.op_weights,
                                   avoid=self._archive_genomes())
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

    # ─── quality-diversity: aim at cells nobody has occupied ────────────────
    HOLD_HORIZON = {"scalp": (1, 2), "intraday": (3, 6), "swing": (7, 24), "position": (25, 48)}
    REGIMES = ("all", "low_vol", "high_vol", "trend", "chop")
    EXPOSURE_DIR = {"long": "long_bias", "short": "short_bias", "neutral": "neutral"}

    def _empty_cells(self) -> List[tuple]:
        """Reachable (hold, exposure, regime) combinations with no archive incumbent.

        Turnover is deliberately excluded: it emerges from the backtest and cannot be dialled in at
        generation time, so targeting it would just be noise. The other three axes are all direct
        genome arguments, which is what makes this emitter actually steerable."""
        occupied = set()
        for r in self.store.archive_rows(self.market):
            parts = str(r["niche_key"]).split(":")
            if len(parts) >= 5:
                occupied.add((parts[1], parts[3], parts[4]))     # hold, exposure, regime
        return [(h, e, g) for h in self.HOLD_HORIZON for e in self.EXPOSURE_DIR
                for g in self.REGIMES if (h, e, g) not in occupied]

    def _targeted(self, market: str) -> Genome:
        """A random genome steered toward an unoccupied behavioural cell."""
        empty = self._empty_cells()
        g = self.sampler._random(market)
        if not empty:
            return g
        hold, expo, regime = empty[int(self.rng.integers(len(empty)))]
        lo, hi = self.HOLD_HORIZON[hold]
        try:
            if g.risk.op == "horizon_hold":
                g.risk.args["horizon"] = int(self.rng.integers(lo, hi + 1))
            if "regime" in g.signal.args:
                g.signal.args["regime"] = regime
            if "direction" in g.signal.args:
                want = self.EXPOSURE_DIR[expo]
                allowed = REGISTRY[g.signal.op].args["direction"].choices
                if want in allowed:
                    g.signal.args["direction"] = want
        except Exception:
            return self.sampler._random(market)
        return g if g.typecheck()[0] else self.sampler._random(market)

    def build_book(self, n_books_tried: Optional[int] = None) -> Optional[dict]:
        """Assemble and test the PORTFOLIO of archive elites (docs/15 §5).

        Member return series are recomputed by re-evaluating archive incumbents on the search
        panel. That is a repeat of a known hypothesis, not a new one, so — exactly as for
        warm-start parents and champion re-validation — it is deliberately NOT written to the
        result ledger and charges no trial."""
        from mt.improve import book as book_mod
        series = dict(self.member_returns)
        for r in self.store.archive_rows(self.market):
            gid = r["genome_id"]
            if gid in series:
                continue
            g = self.store.get_genome(gid)
            if g is None or not g.typecheck()[0]:
                continue
            try:
                res = evaluate(g, self.panel, self.seed)     # NOT ledgered — a repeat, not a trial
            except Exception:
                continue
            if res.ok:
                series[gid] = res.net_returns
        if len(series) < book_mod.MIN_MEMBERS:
            return None
        self.member_returns = series
        # prior rounds of book assembly; this round's own selection trials are added inside
        tried = n_books_tried if n_books_tried is not None else self.store.prereg_count(self.market)
        sr_std = self.store.sr_trial_std(self.market) or self.store.sr_trial_std(None)
        return book_mod.build_book(series, n_books_tried=tried, sr_trial_std=sr_std)

    def _attribute(self, g: Genome, base_z: float, n_eff: int, sr_std) -> None:
        """Leave-one-feature-out ΔDSR-z: re-evaluate the genome with each feature dropped and
        record how much the Deflated-Sharpe z falls — the empirical contribution of each primitive
        (so we learn e.g. whether order_block_strength adds anything beyond the trend it rides)."""
        import copy
        from mt.adapters.cclib import deflated_sharpe
        for i in range(len(g.features)):
            gg = copy.deepcopy(g)
            del gg.features[i]
            if not gg.typecheck()[0]:
                continue
            try:
                res2 = evaluate(gg, self.panel, self.seed)
                if not res2.ok:
                    continue
                d = deflated_sharpe(res2.net_returns.tolist(), n_trials=max(1, n_eff), sr_trial_std=sr_std)
                z2 = d.get("dsr_z_score")
                if z2 is not None:
                    self.store.record_attribution(self.market, g.features[i].op, base_z - float(z2))
            except Exception:
                continue

    def _archive_genomes(self, limit: int = 24) -> List[Genome]:
        """Current archive elites as Genome objects — the 'do not re-derive this' set that makes
        breeding novelty-seeking instead of locally-converging."""
        out = []
        for r in self.store.archive_rows(self.market)[:limit]:
            g = self.store.get_genome(r["genome_id"])
            if g is not None and g.typecheck()[0]:
                out.append(g)
        return out

    def _pick_archetype(self, kinds: List[str]) -> str:
        """ARCHETYPE-LEVEL cue (docs/15 §3): bias which strategy theme gets sampled next by what
        the accumulated failure record says about each family's raw predictive strength.

        This is the tier that was entirely missing. The system wrote 1,123 post-mortems and then
        chose its next archetype uniformly at random, so nothing it learned about *themes* could
        ever influence what it tried. Weights are floored so no theme is ever eliminated — a family
        that looks dead on 30 samples may not be dead on 3,000."""
        priors = {t: (n, pr, e) for t, n, pr, e in self.store.family_priors(self.market)}
        if not priors:
            return kinds[int(self.rng.integers(len(kinds)))]
        w = []
        for k in kinds:
            hit = [v for t, v in priors.items() if t == k or k in t or t in k]
            edge = max((v[2] for v in hit), default=0.0)
            w.append(math.exp(max(-3.0, min(3.0, edge))))
        w = np.array(w, dtype=float)
        w = 0.6 * (w / w.sum()) + 0.4 * (1.0 / len(kinds))   # floor toward uniform
        return kinds[int(self.rng.choice(len(kinds), p=w / w.sum()))]

    def _mine(self, cnt: int) -> List[Genome]:
        if self.rng.random() < 0.4:                      # occasionally grow the vocabulary
            miner_mod.mint_interaction(self.panel, self.rng, store=self.store, market=self.market)
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
