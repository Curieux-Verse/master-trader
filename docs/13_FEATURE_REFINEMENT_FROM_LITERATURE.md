# Feature Refinement from the Literature

*Companion to `genome_family_research_dossier.md`. I read the cited sources, mapped each family to its actual implementation in [`mt/sim/features.py`](../mt/sim/features.py) and [`mt/adapters/cclib.py`](../mt/adapters/cclib.py), and turned "here is the literature" into "here is the specific line to change and why." Every item names the current code, what the source actually prescribes, the concrete upgrade, and an honest priority.*

---

## Implementation status (shipped)

| Item | Status |
|---|---|
| **Effective-N Deflated Sharpe** (§0) | ✅ shipped — `ret_sig` signatures, `avg_trial_corr` ρ̄, `effective_trial_count` N/(1+(N−1)ρ̄); loop feeds N_eff; self-test experiment (C) gates on it. *Confirmed live: raw 87 → N_eff 9.* |
| Microstructure: `vpin`, `kyle_lambda`, `amihud_illiquidity` (§2) | ✅ shipped |
| Stat: `mean_reversion_halflife`, real `hurst` (aggregated-variance), `coint_zscore` (§3) | ✅ shipped |
| Vol: `har_vol` (HAR-RV), `range_vol` (Yang-Zhang) (§4) | ✅ shipped |
| Trend: `tsmom_blend` (§1) | ✅ shipped |
| Profile: real `poc_distance_real`, `value_area_real` (numba) (§2) | ✅ shipped |
| Positioning: `cot_index` (Williams), `rel_strength` (Murphy) (§6) | ✅ shipped |
| Event: `cesi_surprise` (§7) · Sizing: Kelly μ-shrinkage (§8) · `adx` Wilder option | ✅ shipped |
| **Feature attribution** (leave-one-out ΔDSR-z) | ✅ shipped — `attributions` table + report §4.7 |
| **HMM regime** (§5) | ⏸️ **deferred** — smoothed HMM posteriors use the backward pass (future data) → lookahead, and per-eval EM would slow the marathon. Shipping it would violate the anti-overfit contract. Revisit only with walk-forward *filtered* posteriors. |
| Lo-MacKinlay VR bias correction (§3) | ⏭️ skipped — the downstream cross-sectional z-score neutralizes the level bias it fixes. |

*74 registered ops (was 60); 64 computable features. Every batch: 23/23 tests + self-test TRUSTWORTHY.*

---

## Context — why this exists

The 5-hour marathon tested 24,882 genomes and admitted zero. That is the gauntlet working, but the dossier's sources expose two separable questions the run *cannot* distinguish:

1. **Is the admission bar mis-calibrated?** The Deflated Sharpe uses a raw trial count N=54,238 as if all trials were independent. They are not — genomes share features heavily. López de Prado's *own* DSR paper (Appendix 3) says N must be the number of **effectively independent** trials. Over-counting N inflates the bar and can manufacture a 100%-rejection that isn't real.
2. **Are the features too crude to carry the edge that exists?** A large share of `mt/sim/features.py` is self-described "lightweight proxies" (`hurst` = "cheap proxy", SMC/AMT = "proxy", `dist_to_poc` = "proxy: VWAP"). The literature prescribes sharper estimators for the *same* ideas — and crypto now has **real order flow**, which unlocks a whole microstructure family the proxies only imitate.

This document fixes both. **#1 is the single highest-value change in the entire system** — it governs every admit/reject decision.

---

## 0 · The methodology fix that dominates everything — effective number of trials

**Source:** Bailey & López de Prado, *The Deflated Sharpe Ratio* (JPM 2014), Eq. (1) + **Appendix 3** (I extracted this from the paper PDF directly). *AFML* Ch. 8 gives the clustering method.

**What the paper says (verbatim structure of Eq. 1):**
> `E[max SR] ≈ E[{SR}] + √V[{SR}] · ( (1−γ)·Φ⁻¹(1 − 1/N) + γ·Φ⁻¹(1 − 1/(N·e)) )`
> "Appendix 3 shows how N can be determined when the trials are **not independent**."

**Current code** — [`cclib.py:deflated_sharpe`](../mt/adapters/cclib.py) implements Eq. (1) faithfully (`e_max = sigma_sr·((1−γ)z1 + γz2)`, with `E[{SR}]=0` under the null — correct). **But `N` is the raw ledger count** ([`loop.py`](../mt/improve/loop.py) → `store.trial_count(market)`), and `sigma_sr` is the cross-trial Sharpe dispersion. Treating 54k correlated genomes as 54k independent trials pushes `Φ⁻¹(1−1/N)` far into the tail and over-deflates.

**The upgrade — estimate effective N (`N_eff ≤ N`):**
- **Equicorrelation estimator (cheap, ship first):** `N_eff = N / (1 + (N−1)·ρ̄)`, where `ρ̄` is the average pairwise correlation of trial *returns*. As `ρ̄→0`, `N_eff→N`; as `ρ̄→1`, `N_eff→1`.
- **Getting `ρ̄` without storing every return series:** we already have [`ops.distance()`](../mt/genome/ops.py) (feature-set Jaccard + stage diffs). Genomes sharing features produce correlated P&L, so `ρ̄ ≈ mean(1 − distance)` over a sample of ledger genomes is a defensible, near-free proxy. **Better:** persist a small fixed-length return *signature* (e.g. 64 sign-bucketed points) per genome in a new `result_ledger.ret_sig` column and compute real average correlation on a sample.
- **Clustering estimator (LdP Appendix 3 / AFML Ch. 8, ship second):** cluster trial return signatures (correlation distance → hierarchical clustering); `N_eff = number of clusters`. This is what López de Prado actually recommends.

**Files:** [`cclib.py`](../mt/adapters/cclib.py) (`deflated_sharpe` takes `n_eff`), [`store/db.py`](../mt/store/db.py) (store return signatures + an `effective_trial_count()`), [`loop.py`](../mt/improve/loop.py) (pass `n_eff`). **Guard:** keep raw N as a floor-free option and log both, so we can *see* how much the bar moves. This is testable directly against the self-test.

> **Expected effect:** the bar drops materially. Genomes that hovered at DSR-z 1.2–1.6 (we saw a real 1.27 and a transient 1.62) may legitimately clear it. This is the difference between "no edge exists" and "we were charging for tests we didn't independently run."

---

## 1 · Trend & momentum — `trend`, `momentum` (your strongest cluster; deepest evidence)

**Sources:** Moskowitz-Ooi-Pedersen, *Time Series Momentum* (JFE 2012); Hurst-Ooi-Pedersen, *A Century of Evidence* (JPM 2017).

| Current | Literature | Upgrade | Priority |
|---|---|---|---|
| [`momentum()`](../mt/sim/features.py): single-lookback `pxratio/vol` | TSMOM = **sign of past-12m excess return, scaled by inverse ex-ante vol**, targeted to constant vol | It's already vol-scaled ✓. Add a **multi-horizon blend** op `tsmom_blend` averaging normalized momentum at short/med/long lookbacks (AQR "trends everywhere") — one feature instead of the search having to rediscover the blend | **P1** |
| [`adx()`](../mt/sim/features.py): rolling-mean smoothing (`≈Wilder, ~10× faster`) | Wilder's ADX uses **EWM (α=1/w)** | Minor fidelity gap; optionally offer a `wilder=True` arg. Low value | P2 |

The dossier's key observation stands: the best genome's DSR-z 1.27 is **`adx`+`breakout` doing the work**, with `order_block_strength` riding along. That's a reason to *trust* this cluster and invest the multi-horizon blend here — not in SMC.

---

## 2 · Microstructure & order flow — `order_flow`, `auction_market_theory` (biggest opportunity — crypto flow is now REAL)

**Sources:** Kyle (Econometrica 1985); Easley-López de Prado-O'Hara, *VPIN* (2012); Amihud (2002); Glosten-Milgrom (1985).

Crypto klines carry real taker-buy volume ([`_real_delta`](../mt/sim/features.py) = `2·taker_buy − volume`). Current features (`order_flow_imbalance`, `aggressor_ratio`, `cumulative_delta`, `trade_intensity`) use only the **signed mean** of flow. The literature's canonical measures are missing — and they're directly computable:

| New primitive | Formula (from the sources) | What it captures |
|---|---|---|
| **`vpin`** (toxicity) | Rolling `Σ|buy−sell| / Σ(buy+sell)` over a window — the **absolute** imbalance (Easley-LdP order-flow toxicity). Distinct from OFI, which is signed | Flow *toxicity* — spikes precede volatility/liquidity events. Our real buy/sell beats their BVC approximation |
| **`kyle_lambda`** (price impact) | Rolling slope of `Δprice` on signed volume: `cov(Δp, signed_vol)/var(signed_vol)` | Illiquidity / how much order flow *moves* price. High λ = fragile |
| **`amihud_illiquidity`** | Rolling mean of `|return| / (close·volume)` | Robust illiquidity; well-evidenced cross-sectional premium |

**Files:** add three builders to [`features.py`](../mt/sim/features.py) + register in [`registry.py`](../mt/genome/registry.py) with `data_requires=("taker_buy",)` (crypto-gated, like the existing flow ops). **Priority P0** — highest expected signal-per-effort, on your least-crowded, now-available data.

**Market/Volume Profile** (`market_profile`, `volume_profile`): [`dist_to_poc`](../mt/sim/features.py)/`value_area_position` are explicitly "proxy: VWAP." Steidlmayer/Dalton define POC = **price level of max volume** and Value Area = the contiguous **70% of volume**. With footprint (`fp_*`) or even by binning bar volume into price buckets, a real developing POC/VA is computable → `poc_distance_real`, `value_area_real`. **P1.**

---

## 3 · Statistical / mean-reversion / persistence — `statistical`, `mean_reversion`, `persistence`

**Source:** Ernest Chan, *Algorithmic Trading* (the toolkit index for this whole cluster); Lo-MacKinlay variance ratio.

This cluster has the **crudest proxies vs. the richest prescribed toolkit** — high-value.

| Current | Chan's method | Upgrade | Priority |
|---|---|---|---|
| [`hurst()`](../mt/sim/features.py) = `0.5 + 0.5·autocorr` (self-labeled "cheap proxy") | **R/S analysis or DFA** — regress `log(R/S)` on `log(window)`; slope = H | Real vectorized **R/S Hurst** over a window. H>0.5 trending, <0.5 reverting | **P1** |
| *(missing)* | **Half-life of mean reversion** (Ornstein-Uhlenbeck): fit `Δy = λ·y₋₁ + μ`; `half_life = −ln2/λ` | New `mean_reversion_halflife` op — *the* central Chan mean-reversion feature | **P0** |
| [`variance_ratio()`](../mt/sim/features.py): `vq/(q·v1)−1`, overlapping | **Lo-MacKinlay VR** with the unbiased overlapping-obs correction + a heteroskedasticity-robust form | Add the bias correction; it's a few terms | P2 |
| [`rolling_corr()`](../mt/sim/features.py) only | Chan/pairs: **cointegration residual z-score** (Johansen/Engle-Granger) & **Kalman-filtered hedge ratio** | New `coint_zscore` vs the benchmark (`ref_close`) — a real stat-arb signal, not just beta | P1 |

---

## 4 · Volatility — `volatility`

**Source:** Corsi HAR-RV (2009); Engle/Bollerslev ARCH/GARCH.

| Current | Literature | Upgrade | Priority |
|---|---|---|---|
| [`realized_vol()`](../mt/sim/features.py): close-to-close std; [`atr_expansion()`](../mt/sim/features.py): crude short/long ATR ratio | **HAR-RV**: vol as daily / weekly(5) / monthly(22) RV components | `har_vol` op = ratio of short-horizon RV to long-horizon RV (the informative HAR contrast) — a principled `atr_expansion` | **P1** |
| close-to-close only | **Range estimators** (Parkinson, Garman-Klass, Yang-Zhang) are far more efficient and we already have OHLC | `range_vol` op (Yang-Zhang) — better vol with the data we already store | P1 |

---

## 5 · Regime — `regime`, `ml_derived`

**Source:** Hamilton (Econometrica 1989); Ang-Bekaert (RFS 2002, FAJ 2004).

**Current** [`regime_mask()`](../mt/sim/features.py) / `vol_regime_tag`: percentile thresholds on realized vol & trend strength. Good, cheap, PIT-safe.

**Upgrade — a real regime-switching classifier.** Fit a 2–3 state **Gaussian HMM** on `(return, |return|)` (bull/bear/high-vol), use the smoothed state as the regime and its posterior probability as a *feature*. `hmmlearn.GaussianHMM` is the standard; keep it an **optional accelerator** like numba (guarded import; percentile fallback if absent) so CI never breaks. This makes your marquee "regime as a search axis" literature-grade. **P1** (heavier; behind the effective-N and microstructure work).

---

## 6 · Positioning & macro — `positioning`, `macro`, `intermarket`, `cross_asset`

**Source:** Larry Williams, *Secrets of the COT Report*; John Murphy, *Intermarket Analysis*.

| Current | Literature | Upgrade | Priority |
|---|---|---|---|
| [`cot_zscore()`](../mt/sim/features.py): rolling mean of `cot_z` | **Williams COT Index** = `100·(net − minₙ)/(maxₙ − minₙ)` — a %-range (stochastic) over 26/52 weeks; extremes are contrarian | Add `cot_index` (the actual Williams construction) alongside the z-score | P1 |
| [`rolling_corr()`](../mt/sim/features.py) only | Murphy: **lead-lag** & **relative strength** across assets | `lead_lag_corr` (cross-corr at lag k) + `rel_strength` vs benchmark | P2 |

---

## 7 · Event & calendar — `calendar`, `event`

**Source:** Citigroup Economic Surprise Index (CESI) — native to FX/gold, unlike PEAD (equities).

**Current** [`event_surprise()`](../mt/sim/features.py): rolling mean of `impact·(actual−forecast)`. **CESI standardizes** each surprise by its own trailing dispersion and applies time-decay. Upgrade: `cesi_surprise` = `impact · (actual−forecast)/std(surprise)` with exponential decay — same idea, correctly normalized so a "big" surprise is big *relative to that series' history*. **P2** (the free calendar feed is thin/recent — do after data depth improves).

---

## 8 · Position sizing — `kelly_fraction`, `vol_target`, `rank_bucket`

**Source:** Kelly (1956); Thorp; O'Connell (CFA).

**Current** [`_kelly_leverage`](../mt/sim/executor.py): trailing `μ/σ²`, half-Kelly, capped. Already sound. The universal practitioner warning (Thorp/O'Connell) is that **full Kelly is fragile to estimation error in μ** — and the report confirms it (kelly genomes underperformed rank_bucket). Upgrade: **shrink the numerator** — `f = frac · shrink(μ)/σ²` with `shrink(μ) = μ · T/(T+k)` (James-Stein-style toward 0), so a noisy short-history μ can't command full leverage. **P2**, cheap.

---

## 9 · Where the literature says *don't over-invest* — honest calls

- **`ict`, `smc`** — the one cluster in your taxonomy with **zero peer-reviewed backing** (dossier §3). Keep the existing proxies (they cost nothing and compete fairly), but **do not build them out**. Instead add **per-feature attribution** (below) to *quantify* whether `order_block_strength` adds anything beyond the `adx`/`breakout` it rides with. Let the data retire it, not a human.
- **`sentiment`** — worst family, and the toolkit is equity-native. Don't port equity put/call ratios; if anything, feed it the **COT/positioning** signal from §6. Low priority.
- **`mixed`** (your largest bucket, worst DSR-z −1.73) — not a family; it's kitchen-sink genomes. The lesson is *construction discipline*, which the effective-N fix and NSGA complexity penalty already push toward.

---

## Cross-cutting: attribution (so we learn *which feature* carried a genome)

The dossier's sharpest point: the 1.27 came from a 5-tag genome where conventional trend features did the work. Add a **leave-one-feature-out ΔDSR** to the critic's post-mortem ([`critic.py`](../mt/improve/critic.py)): for a near-miss, re-evaluate with each feature dropped and record the DSR delta. This tells us empirically which primitives are inert (retire them) and which carry signal (invest) — turning 26 families of guesswork into measured contribution. **P1.**

---

## Prioritized roadmap

**P0 — do first (bar calibration + best data):**
1. **Effective-N Deflated Sharpe** (§0) — re-calibrates every decision; may change the 100%-rejection outcome.
2. **Microstructure trio** — `vpin`, `kyle_lambda`, `amihud_illiquidity` (§2) — real crypto flow, least-crowded edge.
3. **`mean_reversion_halflife`** (§3) — the central missing stat-arb feature.

**P1 — high value:**
4. Real **R/S `hurst`** + **cointegration z-score** (§3) · 5. **HAR-RV / Yang-Zhang** vol (§4) · 6. **`tsmom_blend`** (§1) · 7. **real POC/Value-Area** (§2) · 8. **HMM regime** (§5, optional dep) · 9. **`cot_index`** (§6) · 10. **feature attribution** in the critic.

**P2 — refinements:** Lo-MacKinlay VR correction, Wilder ADX, CESI standardization, Kelly μ-shrinkage, lead-lag/relative-strength.

---

## Verification

- Every new primitive registers through the [`registry.py`](../mt/genome/registry.py) gate (typed, bounded, PIT-safe, `computable=True`) and is unit-checked for lookahead: `feature[t]` must use only `≤ t` data.
- **Effective-N:** extend [`selftest_gauntlet.py`](../mt/selftest_gauntlet.py) with a correlated-trials experiment — plant N near-duplicate genomes; confirm `N_eff ≪ N` and that a genuine edge still admits while the planted overfit still rejects. This is the go/no-go for the whole change.
- Run `mt.run_system --source lake` on the (now crypto-inclusive) lake before/after each batch and watch **best-z** in the digest — the effective-N fix should visibly lift it; the microstructure features should appear in the top-candidate DSL recipes.
- Full `pytest` + self-test green after every batch, as with prior work.

---

🔒 *Research/paper only. A refined feature makes the search sharper and the bar honest — it does not make any strategy a recommendation to trade.*
