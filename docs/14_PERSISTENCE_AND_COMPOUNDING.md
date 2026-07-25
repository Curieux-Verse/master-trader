# Persistence & Compounding — what must survive across marathons

*Why two consecutive digests showed best-z **+1.49 → −0.06** even though the brain was "persisting", what actually compounded vs. reset, how institutions handle cross-session research memory, and the fix (shipped). The goal of the whole system is that running it consistently across weeks makes it **better every time** — that only happens if the right things persist.*

---

## Implementation status (shipped)

| Item | Status |
|---|---|
| **Hall-of-Fame** — persistent best-ever genomes, independent of the pass bar (`hall_of_fame` table) | ✅ shipped — `upsert_hof`, `best_z_alltime`, `hof_top`, `backfill_hof` |
| **All-time best-z** — headline best-z is the high-water mark, floored by the HoF; per-run climb shown as *this run* | ✅ shipped — `_convergence(z_trend, best_z_floor=…)`; both reports |
| **Backfill** — an existing brain's best-ever genomes surface immediately from historical `gauntlet_reports` | ✅ shipped — idempotent, runs once at marathon start |
| **Warm-start** — NSGA-II parents seeded from the HoF frontier each marathon (no re-evaluation) | ✅ shipped — `DiscoveryLoop._warm_start_parents` |
| **Bandit persistence** — the engine meta-controller's Beta posterior survives restarts | ✅ shipped — `bandit_state` table; `save_bandit`/`load_bandit`; `EngineBandit.snapshot`/`restore` |
| **Dense bandit reward** — near-misses credit the engine (scaled by dsr_z, capped below any pass) | ✅ shipped — `loop.py`, bounded ≤ 0.25 < keep 0.30 < occupy 1.00 |
| **Durable snapshot** — integrity-checked gzip of the brain to a `state` branch; restored on cache miss | ✅ shipped — `mt/store/snapshot.py` + `marathon.yml` |
| **Champion/challenger** — the best-ever genome re-validated OOS on the unseen holdout each digest; reign tracked | ✅ shipped — `champion_track` table (NOT the ledger); `_champions`; digest section |

*Honest-N is untouched: warm-start reconstructs parents from stored fitness and champion re-eval is never ledgered, so the Deflated-Sharpe trial count still counts only genuine discovery trials. Self-test **TRUSTWORTHY** after every batch.*

---

## The symptom

Two Telegram digests, same day:

| | 10:34 run | 16:12 run |
|---|---|---|
| elapsed | 2723 s (~45 min) | 633 s (~10 min) |
| trials (all-time ledger) | 3379 | **4113** ↑ |
| rejected (all-time) | 2208 | **2688** ↑ |
| lessons (all-time) | 126 | **138** ↑ |
| **best-z** | **+1.49** | **−0.06** ↓ |
| families | 52 | 35 |
| phenotypes | 2208 | 480 |

The ledger, rejections, and lessons **compounded** (they are read from the persisted DB). best-z, families, and phenotypes **reset** — they were computed only from the *current run's* in-memory state. The 16:12 run was a younger, ¼-length, cold-started run that simply had not re-climbed yet. best-z did not measure the brain; it measured one short run.

## The diagnosis (grounded in the code, before the fix)

- **best-z was per-run.** [`run_continuous.py`] set `z_trend = []` at the start of every marathon; [`run_system._convergence`] computed `best_z = max(z_trend…)` over that in-memory list only. Nothing read the persisted store. A new/short/unlucky run therefore reported a lower best-z with no memory of prior runs.
- **Nothing retained the champion.** The MAP-Elites archive admits only **gauntlet PASSERS** ([`loop.py`], [`map_elites.py`]). Since nothing cleared the bar, the archive stayed at **0 niches** — so the +1.49 near-miss was never stored as an elite. Its *lesson* persisted; the *genome* did not.
- **The search restarted from random.** `DiscoveryLoop.__init__` built `self.parents = []`, a fresh `EngineBandit()`, empty `pending_mutations`. So each marathon re-explored from scratch, climbed for hours, then discarded the entire evolved population at process exit.
- **The asymmetry.** The **penalty** compounded (N grows → the DSR bar for a given Sharpe gets harder), while the **reward** was discarded (the candidates that could clear it were forgotten every run). The system accumulated the cost of searching and threw away the fruit.

Everything needed to fix it was **already in the DB**: `genomes.body` (full spec) and `gauntlet_reports.gates` (every genome's `dsr_z`) and `gauntlet_reports.fitness` (the objective vector). It was simply never read back.

## How institutions / the field handle this

The consistent principle: **the elite memory is a persistent, first-class artifact, separate from the search process that runs in bursts.**

1. **Hall-of-Fame vs. elitism (evolutionary computation).** Elitism keeps the best in the *active* population; a **Hall-of-Fame** copies the best-ever individual aside so it *cannot* be lost, and frameworks (DEAP) pair it with **checkpoint/restart** to resume evolution across sessions. — *Fortin et al., DEAP (JMLR 2012); Baeldung, "Elitism in Evolutionary Algorithms."*
2. **The QD archive *is* the deliverable, resumed across runs.** MAP-Elites' archive of diverse elites is the product; modern implementations checkpoint it and **seed the next run's population from previously-discovered elites.** — *Mouret & Clune, "Illuminating search spaces by mapping elites" (2015); OpenEvolve MAP-Elites checkpoint/resume.*
3. **Warm-starting search across runs (Bayesian optimization / AutoML).** Don't restart from random — use historical evaluations as the **initial design / surrogate prior** so each run continues where the last stopped. — *Poloczek, Wang & Frazier, "Warm starting Bayesian optimization" (2016).*
4. **Champion/challenger registries (MLOps / quant).** A persistent registry holds the current **@champion** and promotes a **@challenger** only after it beats it on gates — governance for "what is our best, and what earned the right to replace it." — *MLflow Model Registry (aliases).*
5. **Honest multiple-testing ledger (this is sacred here).** "Record all trials and correctly cluster the effectively-independent ones." Retaining/re-testing a **known** genome is not a new hypothesis, so champion retention does **not** conflict with honest-N — re-tests are simply not ledgered. — *Bailey & López de Prado, "The Deflated Sharpe Ratio" (2014); López de Prado, "A Data-Science Solution to the Multiple-Testing Crisis" (2019).*

## The fix — persist the reward, not just the penalty

Three tiers, each mapped to a precedent above. **None relaxes any gate**; the HoF and champion track are search-memory and reporting devices. Tradeable still requires clearing G4 under honest N_eff.

- **P0 — Hall-of-Fame + all-time best-z.** Every genome's best-ever `dsr_z` is retained in `hall_of_fame` regardless of passing. The headline best-z is `max(this-run climb, all-time high-water)`, so it **ratchets and never spuriously regresses**; the per-run value is still shown as *this run*. `backfill_hof` seeds the table from an existing brain's history on first upgrade. *(HoF.)*
- **P1 — Warm-start + compounding meta-controller.** Each marathon seeds NSGA-II parents from the HoF frontier (reconstructed from stored fitness — **no re-evaluation, honest-N untouched**), so evolution *continues* instead of restarting. The engine bandit's posterior persists across runs, and a **dense reward** credits near-misses (scaled by `dsr_z`, capped strictly below any pass) so the meta-controller can learn which engine is closing the gap *before* anything clears. *(Warm-start BO + QD resume.)*
- **P2 — Durability + OOS certification.** An integrity-checked gzip snapshot is pushed to a single-commit `state` branch and restored on a cache miss, removing the 7-day-eviction risk now that the brain is the crown jewels. The standing champion (top HoF genome per market) is **re-validated out-of-sample on the unseen holdout every digest** and its reign tracked in `champion_track` (never the trial ledger) — so the "best strategy" is certified by *surviving repeated OOS challenges over weeks*, not by one run's best-z. *(Model registry / champion-challenger.)*

## Proof (all green)

- Gauntlet self-test **TRUSTWORTHY** (trap_ok, edge_ok, neff_ok) after every batch — the immune system is unchanged.
- **Ratchet, end-to-end:** two separate marathons on the real crypto lake — run 1 reached best-z +0.048, run 2 (shorter, different seed) found +1.18; the reported all-time best-z went +0.048 → +1.177 and never dropped. A cold run whose within-run best is −0.30 now reports the held +1.18 instead of looking like a crash.
- **Warm-start / bandit:** run 2 logs `warm-started 12 elites from hall-of-fame · bandit restored`; parents load best-z-first with **zero** new ledger rows; the bandit's learned skew survives the restart.
- **Durability / champion:** snapshot save→evict→restore round-trips; a corrupt snapshot is refused by the integrity gate (the good brain is never overwritten); the champion is tracked with an incrementing reign and the trial ledger is unchanged by re-validation.

## Honest caveat — what this does and does not buy

Compounding does **not** guarantee a "perfect strategy." It guarantees the search *retains and builds on* progress instead of resetting, so best-z becomes a true multi-week convergence curve and weeks of free compute are cumulative. The ceiling is still set by (a) the information in the data and (b) the honesty of the deflation. If best-z plateaus below the bar under honest N_eff, that is the system correctly reporting that the edge is not in this data/representation — the "feed it new data / conditioning" steer. This fix makes the **structure** lever accumulate; the **data** lever (deeper history, real order flow) remains the other half. See [`05_VALIDATION_GAUNTLET.md`](05_VALIDATION_GAUNTLET.md), [`06_SELF_IMPROVEMENT_LOOP.md`](06_SELF_IMPROVEMENT_LOOP.md).

## References

- D. H. Bailey & M. López de Prado, *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*, J. Portfolio Management (2014). SSRN 2460551.
- M. López de Prado, *A Data-Science Solution to the Multiple-Testing Crisis in Financial Research* (2019). SSRN 3177057.
- J.-B. Mouret & J. Clune, *Illuminating Search Spaces by Mapping Elites* (2015). arXiv:1504.04909.
- F.-A. Fortin et al., *DEAP: Evolutionary Algorithms Made Easy*, JMLR 13 (2012). (Hall-of-Fame + checkpointing.)
- M. Poloczek, J. Wang & P. Frazier, *Warm Starting Bayesian Optimization* (2016). arXiv:1608.03585.
- MLflow *Model Registry* — champion/challenger aliases (docs).
