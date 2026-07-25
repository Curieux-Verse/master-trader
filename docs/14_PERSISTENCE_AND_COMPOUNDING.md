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

## Addendum — gauntlet gate correctness review (all gates)

A full audit of the overfitting immune system (all 9 gates + the DSR / Reality-Check / bootstrap / CSCV math) for code that could wrongly admit or reject strategies. **Clean:** G1, G2, G4b, G5, G6, G7, G8, the effective-N (ρ̄→N_eff) machinery, and — verified, not assumed — G4's **units** (`sharpe_pp` and the internal `sr` are both per-observation, so no 46× scale error). Four issues found; all fixed and proven (self-test **TRUSTWORTHY**: A trap, B edge, C effective-N, D directional-CPCV).

- **F1 — CPCV variants could be identical → deterministic false-reject.** `param_variants` perturbed only numeric *feature* args; genomes whose features expose none (`atr_pct`, `order_block_strength`, `fvg_gap`, `candlestick_pattern` — the SMC/ICT set) produced m identical variants → `cscv_pbo` returns **1.0** → G3 rejects, unrelated to overfitting. **Fix:** perturb numerics across the whole genome (feature+signal+sizing+risk); if variants still can't be made distinct, `returns_matrix` returns None → G3 **defers** (a param-insensitive genome can't be tuning-overfit).
- **F2 — directional CPCV was position-aligned, not time-aligned.** `returns_matrix` tail-aligned variant returns by trade position; directional variants trade at different times (with duplicate exit bars), so rows mixed different calendar times → invalid PBO for directional strategies (and, after F1, for cross-sectional variants whose perturbed horizon changes the rebalance grid). **Fix:** collapse duplicate timestamps and align on the **union calendar** (flat bars = 0). Proven by self-test D (matrix is the 100-bar union, not the 34-bar position-min).
- **F4 — G4 under-deflates without a ledger σ_SR.** The Deflated Sharpe passed a best-of-40 selection overfit (**dsr_z +3.13**) when σ_SR fell back to the candidate's own SE (~4× too small); with the real cross-trial σ_SR the ledger computes (0.127) it correctly rejects (**dsr_z −3.79**). Production always supplies the ledger σ_SR, so steady-state is sound — but the self-test was under-testing G4 and masking this with a G3 artifact. **Fix:** the self-test now computes σ_SR from its own trials exactly as the ledger does, so the trap is caught at **G4, the correct multiple-testing firewall**.
  - **Cold-ledger hardening (shipped).** The residual transient window — a fresh brain / sparse market with no cross-trial σ_SR yet, whose N can still be inflated by screening trials — is now closed three ways: (1) a cold market **borrows the global ledger σ_SR** (`sr_trial_std(market) or sr_trial_std(None)`); (2) if σ_SR is still unavailable and the family is non-trivial (**N > `DSR_RELIABLE_N_MAX`=5**), `deflated_sharpe` flags `reliable=False` and G4 **fails closed** (`is_significant`→False) — small families (N≤5, e.g. the real-edge control) still use the fallback safely; (3) an unreliable, under-deflated z is **kept out of best-z and the hall-of-fame** so it can never inflate the persistent all-time high-water mark. Proven: cold N=40 → fail-closed, warm σ_SR → honest, cold N=3 → still admits real edges; self-test TRUSTWORTHY.
- **F3 — no gate short-circuit (performance).** The runner eagerly ran all 9 gates for every genome (G3 = m extra backtests, G6 = a holdout backtest) despite the "cheap→expensive" docstring. **Fix:** thunk the gates and stop at the first enforced failure — admission is unchanged; the expensive rungs now only run for survivors.

### Second pass — robustness of the remaining gates (G1, G2, G4b, G5, G6, G7, G8)

An adversarial stress of every remaining gate + its supporting math (bootstrap, Reality-Check, cost, block-bootstrap fallbacks) with pathological inputs (empty / all-zero / all-negative / single-spike / NaN-laden / near-constant / heavy-tailed / ruinous). No crashes (G7 handles directional duplicate-timestamp turnover fine). Four issues fixed:

- **B1 (real) — a (near-)constant return series reported an astronomical spurious Sharpe.** `np.full(200, 0.001).std(ddof=1)` is ≈2e-19 (float noise, not 0), so the Sharpe is ≈4.6e15; it passed **G1** (`isfinite` only) and **G4b** (`std==0` only), and a near-constant band (std ~1e-9) even passed **G4** (`sr_se` scales with `sr`, pinning the t-stat at ≈√(2T)). **Fix:** a shared plausibility cap `MAX_SANE_SR_PP=50` (≈100× the strongest test edge; no real per-bar Sharpe approaches it) — G1, G4b, and `deflated_sharpe` now reject a per-observation Sharpe beyond it as degenerate.
- **B2 (real) — G5 drawdown broke on ruin.** `cumprod(1+r)` with a bar ≤ −100% drove equity non-positive → `(peak−equity)/peak` gave **NaN** (at r=−1) or **>1** (at r<−1); reachable under leveraged sizing. **Fix:** floor per-bar growth at 0 (ruin ⇒ equity 0) and guard the division → drawdown is always in **[0,1]**, ruin = 1.0. Benign (no-ruin) paths are byte-identical, so the 0.60 gate threshold stays calibrated.
- **B3 (minor) — G8 read a NaN correlation as orthogonal** (`max_corr=0`), so a NaN-laden duplicate evaded the dedup gate. **Fix:** correlate the finite pairwise overlap.
- **B4 (minor) — G7's 2× cost stress dropped crypto funding** (`funding_rate=None`, 14 vs 19 bps). **Fix:** include a representative funding charge for perp markets.

Locked in by a new self-test experiment **(E) gate robustness** — a (near-)constant series must be rejected at G1 and a ruin path's drawdown must stay in [0,1]. Self-test go/no-go is now A trap · B edge · C effective-N · D directional-CPCV · E robustness.

## References

- D. H. Bailey & M. López de Prado, *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*, J. Portfolio Management (2014). SSRN 2460551.
- M. López de Prado, *A Data-Science Solution to the Multiple-Testing Crisis in Financial Research* (2019). SSRN 3177057.
- J.-B. Mouret & J. Clune, *Illuminating Search Spaces by Mapping Elites* (2015). arXiv:1504.04909.
- F.-A. Fortin et al., *DEAP: Evolutionary Algorithms Made Easy*, JMLR 13 (2012). (Hall-of-Fame + checkpointing.)
- M. Poloczek, J. Wang & P. Frazier, *Warm Starting Bayesian Optimization* (2016). arXiv:1608.03585.
- MLflow *Model Registry* — champion/challenger aliases (docs).
