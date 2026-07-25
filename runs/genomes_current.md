# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-25 01:01 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **23,030** |
| Deflated-Sharpe trial count (raw N) | **46,843** *(evals 30,690 + 16,153 screened)* |
| **Effective** independent trials (N_eff) | **100** *(ρ̄=0.00997654369379357 — the bar the DSR actually uses)* |
| Admitted to archive | **0** |
| Rejected | **23,030** (100.0%) |
| Distinct families explored | **31** |
| Lessons accumulated | **1,123** |
| Best DSR-z | **+1.961** vs bar 1.645 — ✅ **cleared the bar** |

> ### ⚠️ Headline: a candidate cleared the significance bar — and was still rejected
> Genome `92899a1eb4ff76a8` reached **DSR-z +1.96** (> 1.645), i.e. its edge is *not* explainable by luck across 46,843 trials. It was nonetheless killed at **`G1_sanity`** — a *later*, independent gate. This is the layered gauntlet working as designed: clearing multiple-testing is necessary, not sufficient.

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `92899a1eb4ff76a8` | crypto | **1.96** ✅ | 0.6128 | 12.82 | 0.005 | cross_sectional | trend | `G1_sanity` |
| 2 | `4cc1c11a475fe279` | crypto | **1.81** ✅ | 0.5274 | 4.11 | 0.076 | cross_sectional | low_vol | `G3_cpcv_pbo` |
| 3 | `bc79c4c201fddd54` | crypto | **1.70** ✅ | 0.5274 | 4.11 | 0.082 | cross_sectional | low_vol | `G3_cpcv_pbo` |
| 4 | `76946198801d27d9` | crypto | **1.55** | 0.5466 | 4.26 | 0.094 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 5 | `162a6bcf68f0641f` | crypto | **1.47** | 0.5473 | 4.27 | 0.094 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 6 | `03a9f426fb309c85` | crypto | **1.42** | 0.5473 | 4.27 | 0.094 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 7 | `5372d7c62a8ad2dc` | xau | **1.34** | 0.6339 | 12.11 | 0.007 | cross_sectional | trend | `G4_deflated_sharpe` |
| 8 | `285941482ae0d739` | crypto | **1.33** | 0.5473 | 4.27 | 0.078 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 9 | `12e0835f7c70d5e5` | crypto | **1.31** | 0.5473 | 4.27 | 0.094 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 10 | `9025b5bc6478f5fa` | crypto | **1.28** | 0.4904 | 3.82 | 0.105 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 11 | `e4071ffe0900c639` | crypto | **1.25** | 0.6212 | 8.77 | 0.014 | cross_sectional | chop | `G4_deflated_sharpe` |
| 12 | `b60100788154e319` | crypto | **1.24** | 0.4085 | 3.19 | 0.092 | cross_sectional | all | `G4_deflated_sharpe` |
| 13 | `19f6bdd38569d18b` | crypto | **1.20** | 0.5473 | 4.27 | 0.094 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 14 | `27917e82a73d4dcf` | crypto | **1.16** | 0.2891 | 3.19 | 0.121 | cross_sectional | all | `G4_deflated_sharpe` |
| 15 | `b1a50cad25f1431a` | crypto | **1.11** | 0.4599 | 3.36 | 0.079 | cross_sectional | all | `G4_deflated_sharpe` |
| 16 | `bce0427ab1cc3476` | crypto | **1.11** | 0.4631 | 3.38 | 0.077 | cross_sectional | all | `G4_deflated_sharpe` |
| 17 | `e2a26bca56a4ef97` | crypto | **1.11** | 0.2908 | 3.21 | 0.113 | cross_sectional | all | `G4_deflated_sharpe` |
| 18 | `4a8d36589c2e1bdc` | crypto | **1.08** | 0.5905 | 6.03 | 0.024 | cross_sectional | high_vol | `G1_sanity` |
| 19 | `36c53be0e83d2fcd` | crypto | **1.08** | 0.5338 | 4.16 | 0.099 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 20 | `55f3a567b0180946` | crypto | **1.06** | 0.2831 | 3.12 | 0.086 | cross_sectional | all | `G4_deflated_sharpe` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `92899a1eb4ff76a8` — DSR-z 1.96 · died at `G1_sanity` · families: breakout, pattern**
```
[crypto] gated_and (short_bias, regime=trend) on 4h
  features: consolidation_score(window=9); breakout(window=19)
  sizing:   rank_bucket(top_frac=0.21123277162711157, gross=1.964734706231826, per_name_cap=0.11575441816741633)
  risk:     horizon_hold(horizon=5, cost_stress=1.3923186204733105)
  id=92899a1eb4ff76a8  gen=1  by=evo_mutate  nodes=5
```
**#2 · `4cc1c11a475fe279` — DSR-z 1.81 · died at `G3_cpcv_pbo` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=68); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.2135625949420252)
  id=4cc1c11a475fe279  gen=10  by=evo_mutate  nodes=5
```
**#3 · `bc79c4c201fddd54` — DSR-z 1.70 · died at `G3_cpcv_pbo` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=68); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.12350657160542175)
  risk:     horizon_hold(horizon=36, cost_stress=1.2135625949420252)
  id=bc79c4c201fddd54  gen=11  by=evo_mutate  nodes=5
```
**#4 · `76946198801d27d9` — DSR-z 1.55 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.2135625949420252)
  id=76946198801d27d9  gen=7  by=evo_mutate  nodes=5
```
**#5 · `162a6bcf68f0641f` — DSR-z 1.47 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8571957403432453, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.166335240208377)
  id=162a6bcf68f0641f  gen=9  by=evo_mutate  nodes=5
```
**#6 · `03a9f426fb309c85` — DSR-z 1.42 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=2.0, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.166335240208377)
  id=03a9f426fb309c85  gen=11  by=evo_mutate  nodes=5
```
**#7 · `5372d7c62a8ad2dc` — DSR-z 1.34 · died at `G4_deflated_sharpe` · families: momentum, oscillator, trend**
```
[xau] weighted_blend (neutral, regime=trend) on H4
  features: slope(window=14); rsi(window=42)
  sizing:   kelly_fraction(kelly_frac=0.3794662597642904, max_leverage=2.57814803153096, top_frac=0.15891282380533073, gross=1.4384159194254644, per_name_cap=0.18798005726867567)
  risk:     horizon_hold(horizon=6, cost_stress=1.0)
  id=5372d7c62a8ad2dc  gen=5  by=evo_crossover  nodes=5
```
**#8 · `285941482ae0d739` — DSR-z 1.33 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.09561908827898306)
  risk:     horizon_hold(horizon=36, cost_stress=1.166335240208377)
  id=285941482ae0d739  gen=9  by=evo_mutate  nodes=5
```
**#9 · `12e0835f7c70d5e5` — DSR-z 1.31 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.7609412576313028, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.166335240208377)
  id=12e0835f7c70d5e5  gen=11  by=evo_mutate  nodes=5
```
**#10 · `9025b5bc6478f5fa` — DSR-z 1.28 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=79); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.2135625949420252)
  id=9025b5bc6478f5fa  gen=12  by=evo_mutate  nodes=5
```
**#11 · `e4071ffe0900c639` — DSR-z 1.25 · died at `G4_deflated_sharpe` · families: mixed**
```
[crypto] gated_and (short_bias, regime=chop) on 4h
  features: intx_fb1fc5e4()
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=11, cost_stress=1.0807515974333983)
  id=e4071ffe0900c639  gen=24  by=evo_mutate  nodes=4
```
**#12 · `b60100788154e319` — DSR-z 1.24 · died at `G4_deflated_sharpe` · families: volume**
```
[crypto] weighted_blend (neutral) on 4h
  features: obv(window=53); intx_ed242081()
  sizing:   rank_bucket(top_frac=0.2, gross=0.6974957158272533, per_name_cap=0.16356884108253814)
  risk:     horizon_hold(horizon=36, cost_stress=1.2135625949420252)
  id=b60100788154e319  gen=10  by=evo_mutate  nodes=5
```
**#13 · `19f6bdd38569d18b` — DSR-z 1.20 · died at `G4_deflated_sharpe` · families: auction_market_theory, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: obv(window=53); vwap_distance(window=43)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.166335240208377)
  id=19f6bdd38569d18b  gen=8  by=evo_mutate  nodes=5
```
**#14 · `27917e82a73d4dcf` — DSR-z 1.16 · died at `G4_deflated_sharpe` · families: oscillator, trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: cci(window=98); ma_cross(fast=10, slow=134)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=18, cost_stress=1.0)
  id=27917e82a73d4dcf  gen=5  by=evo_crossover  nodes=5
```
**#15 · `b1a50cad25f1431a` — DSR-z 1.11 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: ma_cross(fast=15, slow=56)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=41, cost_stress=1.6964507807197573)
  id=b1a50cad25f1431a  gen=17  by=evo_mutate  nodes=4
```
**#16 · `bce0427ab1cc3476` — DSR-z 1.11 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: ma_cross(fast=15, slow=113)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=41, cost_stress=1.7070568444386747)
  id=bce0427ab1cc3476  gen=22  by=evo_mutate  nodes=4
```
**#17 · `e2a26bca56a4ef97` — DSR-z 1.11 · died at `G4_deflated_sharpe` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=123)
  sizing:   rank_bucket(top_frac=0.2, gross=1.3255007666614573, per_name_cap=0.15)
  risk:     horizon_hold(horizon=18, cost_stress=1.0)
  id=e2a26bca56a4ef97  gen=4  by=evo_mutate  nodes=4
```
**#18 · `4a8d36589c2e1bdc` — DSR-z 1.08 · died at `G1_sanity` · families: oscillator, trend**
```
[crypto] gated_and (short_bias, regime=high_vol) on 4h
  features: cci(window=98); ma_cross(fast=10, slow=176)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=21, cost_stress=1.0)
  id=4a8d36589c2e1bdc  gen=11  by=evo_mutate  nodes=5
```
**#19 · `36c53be0e83d2fcd` — DSR-z 1.08 · died at `G4_deflated_sharpe` · families: auction_market_theory, cross_asset, intermarket, volume**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: vwap_distance(window=43); rel_strength(window=21)
  sizing:   rank_bucket(top_frac=0.06964909140958207, gross=1.8537822973234503, per_name_cap=0.11557559787236346)
  risk:     horizon_hold(horizon=36, cost_stress=1.0)
  id=36c53be0e83d2fcd  gen=11  by=evo_mutate  nodes=5
```
**#20 · `55f3a567b0180946` — DSR-z 1.06 · died at `G4_deflated_sharpe` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=123)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=18, cost_stress=1.0)
  id=55f3a567b0180946  gen=3  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 17,550 | 76.2% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 3,759 | 16.3% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 1,718 | 7.5% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 2 | 0.0% | parameter tuning overfit (high PBO) |
| `—` | 1 | 0.0% | — |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 7581 | 0 | 1.96 | ██████████████████ |
| `xau` | 7619 | 0 | 1.34 | ███████████████··· |
| `fx` | 7830 | 0 | -0.33 | ·················· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 20186 | 0 | 1.96 | ██████████████████ |
| `directional` | 2844 | 0 | 0.00 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 10495 | 0 | 1.96 | ██████████████████ |
| `random` | 5004 | 0 | 0.44 | █████············· |
| `template` | 3861 | 0 | 0.17 | ██················ |
| `miner` | 3669 | 0 | 0.04 | ·················· |
| `llm` | 1 | 0 | -0.55 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `trend` | 2481 | 0 | 1.96 | ██████████████████ |
| `low_vol` | 2344 | 0 | 1.81 | ██████████████████ |
| `chop` | 3875 | 0 | 1.25 | ██████████████···· |
| `all` | 11213 | 0 | 1.24 | ██████████████···· |
| `high_vol` | 3117 | 0 | 1.08 | ████████████······ |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 16908 | 0 | 1.96 | ██████████████████ |
| `kelly_fraction` | 1382 | 0 | 1.34 | ███████████████··· |
| `atr_scaled` | 1039 | 0 | 0.57 | ██████············ |
| `vol_target` | 1837 | 0 | 0.39 | ████·············· |
| `fixed_fractional` | 1864 | 0 | -0.12 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `pattern` | 1990 | 0 | 1.96 | ██████████████████ |
| `breakout` | 1538 | 0 | 1.96 | ██████████████████ |
| `auction_market_theory` | 3115 | 0 | 1.81 | ██████████████████ |
| `volume` | 1674 | 0 | 1.81 | ██████████████████ |
| `trend` | 4372 | 0 | 1.34 | ███████████████··· |
| `momentum` | 3612 | 0 | 1.34 | ███████████████··· |
| `oscillator` | 2679 | 0 | 1.34 | ███████████████··· |
| `mixed` | 2980 | 0 | 1.25 | ██████████████···· |
| `microstructure` | 858 | 0 | 1.11 | ████████████······ |
| `liquidity` | 507 | 0 | 1.11 | ████████████······ |
| `cross_asset` | 1116 | 0 | 1.08 | ████████████······ |
| `intermarket` | 803 | 0 | 1.08 | ████████████······ |
| `statistical` | 4569 | 0 | 0.99 | ███████████······· |
| `mean_reversion` | 2934 | 0 | 0.99 | ███████████······· |
| `order_flow` | 924 | 0 | 0.90 | ██████████········ |
| `ict` | 818 | 0 | 0.61 | ███████··········· |
| `smc` | 818 | 0 | 0.61 | ███████··········· |
| `volatility` | 4413 | 0 | 0.58 | ██████············ |
| `macro` | 2416 | 0 | 0.56 | ██████············ |
| `sentiment` | 260 | 0 | 0.56 | ██████············ |
| `crypto` | 184 | 0 | 0.31 | ███··············· |
| `funding` | 184 | 0 | 0.31 | ███··············· |
| `market_profile` | 974 | 0 | 0.09 | █················· |
| `event` | 829 | 0 | -0.01 | ·················· |
| `calendar` | 717 | 0 | -0.01 | ·················· |
| `volume_profile` | 911 | 0 | -0.06 | ·················· |
| `persistence` | 725 | 0 | -0.06 | ·················· |
| `positioning` | 1630 | 0 | -0.16 | ·················· |
| `regime` | 346 | 0 | -0.42 | ·················· |
| `ml_derived` | 222 | 0 | -0.42 | ·················· |
| `rates` | 240 | 0 | -1.22 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `breakout` | 2 | +3.202 | **carries signal** |
| `vwap_distance` | 30 | +1.588 | **carries signal** |
| `rotation_factor` | 2 | +1.249 | **carries signal** |
| `obv` | 27 | +1.151 | **carries signal** |
| `cci` | 15 | +1.118 | **carries signal** |
| `mean_reversion_halflife` | 2 | +1.094 | **carries signal** |
| `slope` | 5 | +1.079 | **carries signal** |
| `rel_strength` | 5 | +0.675 | **carries signal** |
| `rsi` | 6 | +0.569 | **carries signal** |
| `ma_cross` | 11 | +0.392 | **carries signal** |
| `delta_divergence` | 3 | +0.181 | **carries signal** |

---

## 5 · Archive (0 niches)

*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*

## 6 · Lessons library (1,123)

- ×2 — [G4_deflated_sharpe] calendar+event+interaction+intx_3139e2f8+intx_eef070fc+ma_cross+macro+mean_reversion+mined+order_block_strengt
- ×1 — [G4_deflated_sharpe] interaction+intx_75c6fb4e+mined+poc_distance_real (directional) — edge indistinguishable from luck after trial
- ×1 — [G0_eval] interaction+intx_4d58344d+intx_9549bf1f+macro+mined+positioning+volatility (directional) — did not produce a v
- ×1 — [G4_deflated_sharpe] amihud_illiquidity+interaction+intx_04a5db61+intx_75c6fb4e+intx_c710988f+intx_fb1fc5e4+mined+poc_distance_real
- ×1 — [G4_deflated_sharpe] fvg_gap+interaction+intx_1041d940+mined+value_area_real+williams_r (cross_sectional) — edge indistinguishable 
- ×1 — [G1_sanity] candlestick_pattern+interaction+intx_170d4053+intx_59514131+mined+order_block_strength+trend (cross_sectional)
- ×1 — [G0_eval] interaction+intx_0cd83c53+intx_310d82e5+mined+vwap_distance (cross_sectional) — did not produce a valid backte
- ×1 — [G1_sanity] interaction+intx_2614014e+intx_ac9fb8e0+mined+trend (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] candlestick_pattern+interaction+intx_2614014e+intx_c1787148+mined+order_block_strength+volume (cross_sectional
- ×1 — [G0_eval] bb_position+interaction+intx_170d4053+intx_7e2f6c14+intx_c3219e94+intx_f031f0fa+intx_fe4c1308+mined (direction
- ×1 — [G1_sanity] breakout+interaction+intx_230518a4+intx_59514131+mined+pattern (cross_sectional) — degenerate or too few trade
- ×1 — [G1_sanity] fvg_gap+interaction+intx_1041d940+mined+momentum (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] interaction+mean_reversion+mined+momentum+order_block_strength+oscillator+rotation_factor+volatility (cross_se
- ×1 — [G4_deflated_sharpe] adx+atr_expansion+candlestick_pattern+interaction+mined+order_block_strength+trend (cross_sectional) — edge in
- ×1 — [G4_deflated_sharpe] interaction+mined+trend+value_area_real+williams_r (cross_sectional) — edge indistinguishable from luck after 

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*