# 🧬 Master Trader — Genome Population Report

*Generated 2026-08-05 04:10 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **120,497** |
| Deflated-Sharpe trial count (raw N) | **238,061** *(evals 120,497 + 117,564 screened)* |
| **Effective** independent trials (N_eff) | **155,804** *(ρ̄=0.03907712580272821 — the bar the DSR actually uses)* |
| Admitted to archive | **9751** |
| Rejected | **110,746** (91.9%) |
| Distinct families explored | **31** |
| Lessons accumulated | **57,856** |
| Best DSR-z | **+1.503** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `f9b357250744cb4d` | crypto | **1.50** | 0.5998 | 4.23 | 0.031 | cross_sectional | all | `G3_cpcv_pbo` |
| 2 | `97cb163c7403b95a` | crypto | **1.46** | 0.5634 | 3.97 | 0.036 | cross_sectional | all | `G3_cpcv_pbo` |
| 3 | `db1116ef1b1daa2e` | crypto | **1.45** | 0.8313 | 5.61 | 0.034 | cross_sectional | all | `ADMITTED` |
| 4 | `f91ac9df4c92294d` | crypto | **1.44** | 0.8360 | 5.65 | 0.033 | cross_sectional | all | `ADMITTED` |
| 5 | `791009c7f085c6aa` | crypto | **1.43** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 6 | `6d03423485a0e4a7` | crypto | **1.43** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 7 | `c7f59950aa197236` | crypto | **1.42** | 0.8318 | 5.62 | 0.033 | cross_sectional | all | `ADMITTED` |
| 8 | `7e6ad3c6df7a9643` | crypto | **1.42** | 0.5725 | 4.04 | 0.037 | cross_sectional | all | `G3_cpcv_pbo` |
| 9 | `e2932cabac0a7ae1` | crypto | **1.41** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 10 | `726f5f4697c4db1c` | crypto | **1.41** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 11 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 12 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 13 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 14 | `cd01243357770202` | crypto | **1.29** | 0.8015 | 5.41 | 0.043 | cross_sectional | all | `ADMITTED` |
| 15 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 16 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 17 | `64eed38552709d9a` | crypto | **1.16** | 0.7519 | 5.08 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 18 | `473219061ecd274b` | crypto | **1.13** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `427fb1bac0b4316a` | crypto | **1.12** | 0.9182 | 6.20 | 0.042 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `ebe2e17a51d99e1d` | crypto | **1.12** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `f9b357250744cb4d` — DSR-z 1.50 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.3522641431182003, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=f9b357250744cb4d  gen=30  by=evo_mutate  nodes=4
```
**#2 · `97cb163c7403b95a` — DSR-z 1.46 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=29)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=97cb163c7403b95a  gen=21  by=evo_mutate  nodes=4
```
**#3 · `db1116ef1b1daa2e` — DSR-z 1.45 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.009601909168493)
  id=db1116ef1b1daa2e  gen=41  by=evo_mutate  nodes=4
```
**#4 · `f91ac9df4c92294d` — DSR-z 1.44 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0491530175959747)
  id=f91ac9df4c92294d  gen=56  by=evo_mutate  nodes=4
```
**#5 · `791009c7f085c6aa` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=791009c7f085c6aa  gen=59  by=evo_crossover  nodes=4
```
**#6 · `6d03423485a0e4a7` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=6d03423485a0e4a7  gen=44  by=evo_crossover  nodes=4
```
**#7 · `c7f59950aa197236` — DSR-z 1.42 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.3153903380020915)
  id=c7f59950aa197236  gen=61  by=evo_mutate  nodes=4
```
**#8 · `7e6ad3c6df7a9643` — DSR-z 1.42 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); amihud_illiquidity(window=32)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=7e6ad3c6df7a9643  gen=21  by=evo_mutate  nodes=5
```
**#9 · `e2932cabac0a7ae1` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=e2932cabac0a7ae1  gen=55  by=evo_mutate  nodes=4
```
**#10 · `726f5f4697c4db1c` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=726f5f4697c4db1c  gen=74  by=evo_crossover  nodes=4
```
**#11 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#12 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#13 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#14 · `cd01243357770202` — DSR-z 1.29 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.987931652984258, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=cd01243357770202  gen=79  by=evo_mutate  nodes=4
```
**#15 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#16 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
**#17 · `64eed38552709d9a` — DSR-z 1.16 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.4384386928813)
  id=64eed38552709d9a  gen=36  by=evo_mutate  nodes=4
```
**#18 · `473219061ecd274b` — DSR-z 1.13 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=473219061ecd274b  gen=49  by=evo_mutate  nodes=4
```
**#19 · `427fb1bac0b4316a` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=66)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.09311457267804286)
  risk:     horizon_hold(horizon=48, cost_stress=1.0433464695652956)
  id=427fb1bac0b4316a  gen=44  by=evo_mutate  nodes=4
```
**#20 · `ebe2e17a51d99e1d` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=ebe2e17a51d99e1d  gen=51  by=evo_crossover  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `—` | 80,371 | 66.7% | — |
| `GS_screen` | 17,044 | 14.1% | — |
| `ADMITTED` | 9,751 | 8.1% | **cleared every gate** |
| `G1_sanity` | 6,902 | 5.7% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,385 | 2.8% | parameter tuning overfit (high PBO) |
| `G0_eval` | 1,583 | 1.3% | did not produce a valid backtest |
| `G9_plateau` | 929 | 0.8% | — |
| `G8_orthogonality` | 278 | 0.2% | duplicates an existing archive member |
| `G5_robustness` | 235 | 0.2% | bootstrap tail drawdown too large |
| `G2_oos` | 19 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 41688 | 2940 | 1.50 | ████████████████·· |
| `xau` | 37673 | 5116 | 0.83 | █████████········· |
| `fx` | 41136 | 1695 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 90124 | 4744 | 1.50 | ████████████████·· |
| `directional` | 30373 | 5007 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 97072 | 9735 | 1.50 | ████████████████·· |
| `llm` | 7156 | 12 | 1.35 | ███████████████··· |
| `template` | 4160 | 0 | 0.31 | ███··············· |
| `miner` | 7148 | 4 | -0.24 | ·················· |
| `random` | 4961 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 58481 | 4160 | 1.50 | ████████████████·· |
| `low_vol` | 37695 | 5302 | 0.83 | █████████········· |
| `chop` | 6708 | 11 | 0.22 | ██················ |
| `trend` | 7572 | 228 | 0.02 | ·················· |
| `high_vol` | 10041 | 50 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 93039 | 5693 | 1.50 | ████████████████·· |
| `kelly_fraction` | 1966 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 21640 | 4047 | 0.76 | ████████·········· |
| `vol_target` | 2639 | 1 | -1.05 | ·················· |
| `atr_scaled` | 1213 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 19139 | 2803 | 1.50 | ████████████████·· |
| `liquidity` | 18183 | 2793 | 1.50 | ████████████████·· |
| `macro` | 23721 | 2588 | 1.38 | ███████████████··· |
| `regime` | 12021 | 1874 | 1.38 | ███████████████··· |
| `rates` | 8313 | 973 | 1.38 | ███████████████··· |
| `momentum` | 20571 | 2337 | 0.86 | █████████········· |
| `trend` | 17734 | 1872 | 0.86 | █████████········· |
| `auction_market_theory` | 16413 | 2115 | 0.85 | █████████········· |
| `market_profile` | 11096 | 1793 | 0.85 | █████████········· |
| `statistical` | 22561 | 3662 | 0.83 | █████████········· |
| `pattern` | 3890 | 140 | 0.83 | █████████········· |
| `breakout` | 3734 | 140 | 0.83 | █████████········· |
| `volatility` | 16809 | 2987 | 0.76 | ████████·········· |
| `mean_reversion` | 12321 | 2916 | 0.76 | ████████·········· |
| `ict` | 8461 | 894 | 0.75 | ████████·········· |
| `smc` | 8461 | 894 | 0.75 | ████████·········· |
| `positioning` | 17340 | 1973 | 0.60 | ███████··········· |
| `ml_derived` | 8046 | 1555 | 0.60 | ███████··········· |
| `order_flow` | 3309 | 268 | 0.55 | ██████············ |
| `cross_asset` | 2167 | 193 | 0.53 | ██████············ |
| `intermarket` | 2147 | 193 | 0.53 | ██████············ |
| `oscillator` | 6466 | 183 | 0.40 | ████·············· |
| `event` | 2576 | 267 | 0.12 | █················· |
| `volume` | 5168 | 228 | 0.03 | ·················· |
| `mixed` | 37010 | 1079 | -0.11 | ·················· |
| `volume_profile` | 2650 | 107 | -0.16 | ·················· |
| `crypto` | 2325 | 287 | -0.30 | ·················· |
| `funding` | 2325 | 287 | -0.30 | ·················· |
| `persistence` | 2075 | 31 | -0.51 | ·················· |
| `calendar` | 37 | 0 | -1.69 | ·················· |
| `sentiment` | 11 | 0 | -17.94 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_7cd0e389` | 2 | +12.957 | **carries signal** |
| `intx_39ebaed9` | 2 | +10.526 | **carries signal** |
| `intx_ca1f399c` | 2 | +10.157 | **carries signal** |
| `intx_c9d46590` | 2 | +8.570 | **carries signal** |
| `intx_d77b40a2` | 3 | +8.415 | **carries signal** |
| `intx_911ab9c3` | 2 | +6.511 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_896c4ec5` | 194 | +2.971 | **carries signal** |
| `intx_ae3fec3d` | 83 | +2.642 | **carries signal** |
| `intx_a4af6119` | 459 | +2.535 | **carries signal** |
| `intx_72d2ef7d` | 795 | +2.503 | **carries signal** |
| `intx_2e781688` | 340 | +2.296 | **carries signal** |
| `intx_16f6ebcd` | 2 | +2.267 | **carries signal** |
| `intx_634b10e7` | 454 | +2.237 | **carries signal** |

---

## 5 · Archive (55 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.530 |
| `xau:swing:trade:long:low_vol` | xau | 1.215 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `fx:position:med:long:all` | fx | 0.693 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:position:low:long:all` | fx | 0.602 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `xau:intraday:low:neutral:all` | xau | 0.495 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.427 |
| `xau:intraday:low:long:trend` | xau | 0.389 |
| `xau:intraday:trade:long:high_vol` | xau | 0.361 |
| `crypto:position:med:neutral:chop` | crypto | 0.356 |
| `fx:position:low:long:high_vol` | fx | 0.345 |
| `crypto:position:med:short:all` | crypto | 0.345 |
| `crypto:position:high:neutral:all` | crypto | 0.342 |

## 6 · Lessons library (57,856)

- ×10 — [GS_screen] auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_a16b7695+intx_ab31bc67+liquidity+market_pro
- ×8 — [GS_screen] interaction+intx_ca069136+mined+vol_regime_tag (cross_sectional) — raw predictive strength too weak to clear t
- ×6 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×6 — [GS_screen] amihud_illiquidity+cci+dist_to_poc+interaction+intx_006ec67c+intx_10e814d4+intx_1f414506+intx_42055f3a+intx_6f
- ×6 — [GS_screen] breakout+interaction+intx_40f73767+intx_56f51694+intx_caac6070+intx_e2df0078+mined+pattern (cross_sectional) —
- ×5 — [PASS] auction_market_theory+interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined
- ×5 — [GS_screen] crypto+funding+interaction+intx_a16b7695+intx_ab31bc67+intx_ca069136+liquidity+microstructure+mined+ml_derived
- ×5 — [GS_screen] interaction+intx_080bbe39+intx_10e814d4+intx_39165f4d+intx_495677d1+intx_4f97afa7+intx_6ff832ad+intx_a99b3c1a+
- ×4 — [PASS] interaction+intx_39165f4d+intx_4f97afa7+intx_6ff832ad+intx_a99b3c1a+intx_c1240e5f+intx_e4425d6a+macro+mined+po
- ×4 — [GS_screen] interaction+intx_10e814d4+intx_56f51694+intx_cf2675c4+mined+poc_distance_real (cross_sectional) — raw predicti
- ×3 — [GS_screen] breakout+interaction+intx_40f73767+intx_e2df0078+mined+pattern (cross_sectional) — raw predictive strength too
- ×3 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+mined+volatility on a directional book promoted to the candidate pool
- ×3 — [PASS] adx+candlestick_pattern+interaction+intx_0507d207+intx_382083bf+intx_8e0d4062+intx_fe341f6e+mean_reversion+min
- ×3 — [PASS] interaction+intx_0507d207+intx_382083bf+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical on a dire
- ×3 — [PASS] interaction+intx_10e814d4+intx_ceae8a96+intx_d790d760+mined+poc_distance_real on a cross_sectional book promot

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*