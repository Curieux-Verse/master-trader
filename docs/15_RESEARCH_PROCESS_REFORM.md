# 15 — Research Process Reform: exploration vs confirmation, diversity, and the portfolio

> The system was asking the hardest possible question — *"is there a single genome whose Sharpe
> survives deflation for every trial we ever ran?"* — and answering it with a search that improved
> the population mean while never extending the tail. This document records why that was the wrong
> question, what institutions actually do, and what changed.

## 0. The evidence that prompted this

Measured on the last production brain (23,030 genomes, 524 generations) and on controlled
reruns of the pre-change code:

| Finding | Measurement |
|---|---|
| Nothing ever cleared | 0 admitted of 23,030 |
| …but the multiple-testing bar was **not** the binding constraint | 3 candidates reached z = +1.96 / +1.81 / +1.70; they died at `G1_sanity` (one bar was >50% of gross P&L) and `G3_cpcv_pbo` |
| The archive was permanently empty | 0 niches → G8 measured a real correlation on **0 of 400** verdicts |
| The search improved the mean, not the tail | best dsr_z at lineage depth 0 was never beaten at depth ≥2; child beat parent 31% of the time, mean Δz −0.24 |
| Mode collapse | production top-20 were parameter jitter on one `obv`×`vwap_distance` idea |
| Lessons were write-only | 1,123 stored, **3** distinct prescriptions, all at confidence 0.5, **zero** readers outside report rendering |
| Attribution was write-only | `vwap_distance` measured at +1.59 mean ΔDSR-z over 30 observations; no generator read it |
| The "targeted fix" was random | 8 of 10 gate branches fell through to a uniform random mutation; the two real repairs sat behind gates that fired 2 and 0 times |
| 25% of the trial count was self-inflicted | duplicate evaluations of already-tested genomes, bit-identical results; one genome evaluated 12× |
| The holdout was not a holdout | pre-short-circuit, `G6_transfer` ran on **all 23,030** genomes |
| N_eff was blind to duplication | equicorrelation reported ρ̄ = 0.00998 → N_eff = 100, while the top-20 were near-clones |

## 1. What institutions do

- **Separate exploration from confirmation.** FWER control is a *confirmatory* instrument; FDR is
  the *exploratory* one. Using the former as a screen produces many missed discoveries
  (Harvey & Liu, *False (and Missed) Discoveries in Financial Economics*, JF 2020 — which also
  prices Type II error explicitly). The protocol is two-stage with a time-stamped boundary.
- **Write down what you tried, and pre-register.** Man Group: *"we do keep a record of the things
  we try"*; researchers must *"write down the data partitioning and the methodology and
  expectations"* before analysis; a deliberate *"culture of failure"* so nobody is pushed into
  data mining.
- **Cluster trials before counting them.** López de Prado's ONC / hierarchical / spectral
  estimators of the effective number of independent trials.
- **Hunt many weak, decorrelated signals — not one strong one.** WorldQuant: >20M alphas,
  deliberately weaker, scored as low-correlation baskets. AlphaGen (KDD 2023): optimize the
  combined IC of the alpha **set**.
- **Penalise similarity continuously.** AutoAlpha's PCA-QD discounts fitness by similarity to what
  is already found; AlphaAgent (KDD 2025) adds AST-level structural novelty.
- **Aggregate failures to the level that steers the next cycle.** XALPHA (2026): generation-level
  outcome → cycle-level pattern → **archetype-level research cues**, with failed alphas feeding
  the cues. RD-Agent(Q): closed hypothesis→implement→validate→feedback over a persistent knowledge
  base with a bandit scheduler.
- **The QD archive keeps the best per niche, with no global quality bar** (canonical MAP-Elites);
  parent selection by *curiosity* (+1 on insertion, −0.5 on failure).

## 2. The two-stage protocol

```
Stage A — EXPLORE                        Stage B — CONFIRM
────────────────────                     ─────────────────
GS_screen   (BHY-FDR, q=0.10)   enforced  G4  Deflated Sharpe   enforced
G4, G4b     (FWER)              advisory  G4b Reality Check     enforced
G1/G5/G2/G7/G8                  enforced  G3  CPCV → PBO        enforced
G3          (expensive)         skipped   G6  transfer          enforced
G6          FORBIDDEN — sealed            on the SEALED holdout
   ↓                                         ↑
promoted → MAP-Elites archive  ──── pre-registration (hash + timestamp) ────┘
```

- **`GS_screen` is N-independent.** It ranks on `t = SR·√T`, which carries no family-size term, so
  a parent and its child are comparable across generations. Under the old design the score moved
  because the *ledger* grew, which meant every learning mechanism was training on a partly
  confounded label.
- **`G4` and `G4b` are both FWER instruments** and therefore belong to the same stage. Enforcing
  G4b during exploration while G4 was advisory left a confirmatory bar screening every candidate
  through the back door — measured killing 159 candidates that had already cleared the FDR screen.
- **Stage B earns its small family size with fresh data, not by relabelling.** Multiplicity is over
  the hypotheses *carried forward*, which is the standard sample-splitting argument, and it is only
  valid because Stage A never touches the holdout.
- **Nothing is tradeable without Stage B.** The archive records `promoted` and `cleared`
  separately; only `cleared` reaches the paper book.

## 3. Diversity

- Archive admits **by behavioural niche**, not by clearing a bar (canonical MAP-Elites).
- `scalarize()` applies a **continuous similarity discount**; G8 hard-rejects only near-exact
  clones (ρ ≥ 0.99). A hard 0.90 wall was harmless while the archive was empty and would have
  become a false-reject wall once it filled.
- **Curiosity-weighted, diversity-filtered warm start.** Top-k by z returned 12 near-clones.
- `novelty_mutate` prefers the structurally most distant child — but **only when the parent is in a
  crowded region** (`CONVERGED_DISTANCE`). Applying novelty unconditionally discards good local
  moves in already-diverse regions.
- **QD-score** (Σ max(0, fitness) over occupied niches) is reported alongside best-z. Floored at
  zero so filling a cell can never lower it.

## 4. Failure memory

Three tiers, replacing prose that nothing could read:

1. **Generation-level** — full cheap-gate vector on every genome. Only G3/G6 stay behind success;
   the old short-circuit left NSGA-II with 2 live objectives out of 7.
2. **Cycle-level** — `trial_facts`: one row per (genome, family tag) with gate, promotion, z and
   edge_t. Aggregation is a `GROUP BY`.
3. **Archetype-level** — `family_priors()` biases which theme the template sampler picks next, and
   `feature_op_weights()` (softmax over measured leave-one-out ΔDSR-z) biases which primitive a
   mutation reaches for. Both floored toward uniform so nothing is ever starved out.

Attribution now triggers on **edge_t**, not the N-deflated z: the old trigger fired less as the
ledger grew (measured 0 rows in a 25-generation run), so the one mechanism producing hard evidence
shut itself off exactly as the search matured.

## 5. The portfolio

`k` decorrelated strategies at t ≈ 0.4 combine to t ≈ 0.4·√k. The hall of fame already held
genomes at that individual strength. `mt/improve/book.py` selects members greedily on **marginal**
book Sharpe under a correlation cap, and charges the DSR:

- the **combinations examined during selection** (in-sample book-z fell +6.02 → +1.32 when this
  was added), and
- a σ_SR estimated by **resampling books of the same size** — not the ledger's genome-level σ_SR,
  which is a different object and over-deflated so badly it produced z = −49.6.

Null control: books of pure noise score max z = +1.1 over 6 seeds (below the bar); books over a
real edge clear it 6/6.

## 6. Verification

`python -m mt.selftest_gauntlet` — 11 experiments, all must pass for TRUSTWORTHY:

| | Experiment | Asserts |
|---|---|---|
| A | Overfit trap | best-of-40 on noise is rejected |
| B | Real-edge control | a real edge clears **both** stages |
| C | Effective-N over the ledger | correlated trials collapse, diverse ones don't |
| D | Directional CPCV | variants time-aligned on the union calendar |
| E | Gate robustness | degenerate/ruinous series can't slip |
| F | K_eff vs duplication | 30 clones→1, 30 diverse→27, 25+5→6 |
| G | Ledger dedup | same genome 5× → trial_count 1 |
| H | Two-stage | confirmation still rejects; holdout never in Stage A |
| I | Archive + book | portfolio beats best member, pays for selection, **noise stays insignificant** |
| J | Minted vocabulary | intx_* genomes survive a restart |
| K | Failure memory | facts aggregate; repairs target the failing statistic |

## 7. Measured effect (identical conditions, 25 gens × 16, edgeless data)

| | Before | After |
|---|---|---|
| Gates measured on a failure | 3 of 9 | **9 of 9** |
| Attribution rows | 0 | **167** |
| Critic repairs actually tested | 0 (0.0%) | **66 (16.5%)** |
| Critic vs blind mutation (beat parent) | n/a — identical operations | **35% vs 9%** |
| Distinct lesson confidences | 1 | **39** |
| Duplicate evals charged to N | 12.8% | **0** |
| Genomes retained as search memory | 63.2% | **75.2%** |
| Holdout accesses | unbudgeted (23,030 in production) | **counted; 0 during exploration** |

Governance is unchanged: paper only, no autonomous live-capital action, promotions are
recommendations for a human.
