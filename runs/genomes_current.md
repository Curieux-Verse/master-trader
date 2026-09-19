# 🧬 Master Trader — Genome Population Report

*Generated 2026-09-19 04:33 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **137,687** |
| Deflated-Sharpe trial count (raw N) | **507,379** *(evals 137,687 + 369,692 screened)* |
| **Effective** independent trials (N_eff) | **504,186** *(ρ̄=0.03028094478151351 — the bar the DSR actually uses)* |
| Admitted to archive | **12190** |
| Rejected | **125,497** (91.1%) |
| Distinct families explored | **31** |
| Lessons accumulated | **168,732** |
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
| `—` | 88,745 | 64.5% | — |
| `GS_screen` | 18,929 | 13.7% | — |
| `ADMITTED` | 12,190 | 8.9% | **cleared every gate** |
| `G1_sanity` | 7,884 | 5.7% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,735 | 2.7% | parameter tuning overfit (high PBO) |
| `G0_eval` | 3,621 | 2.6% | did not produce a valid backtest |
| `G9_plateau` | 1,902 | 1.4% | — |
| `G5_robustness` | 353 | 0.3% | bootstrap tail drawdown too large |
| `G8_orthogonality` | 311 | 0.2% | duplicates an existing archive member |
| `G2_oos` | 17 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 53250 | 3152 | 1.50 | ████████████████·· |
| `xau` | 37247 | 6845 | 0.83 | █████████········· |
| `fx` | 47190 | 2193 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 102912 | 5420 | 1.50 | ████████████████·· |
| `directional` | 34775 | 6770 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 102921 | 12169 | 1.50 | ████████████████·· |
| `llm` | 6303 | 12 | 1.35 | ███████████████··· |
| `template` | 4679 | 0 | 0.31 | ███··············· |
| `random` | 12696 | 3 | -0.67 | ·················· |
| `miner` | 11088 | 6 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 66875 | 4323 | 1.50 | ████████████████·· |
| `low_vol` | 41310 | 7123 | 0.83 | █████████········· |
| `chop` | 15166 | 608 | 0.22 | ██················ |
| `trend` | 7217 | 99 | 0.02 | ·················· |
| `high_vol` | 7119 | 37 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 97806 | 6643 | 1.50 | ████████████████·· |
| `kelly_fraction` | 3395 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 27327 | 5532 | 0.76 | ████████·········· |
| `vol_target` | 5803 | 2 | -1.05 | ·················· |
| `atr_scaled` | 3356 | 4 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 8060 | 2284 | 1.50 | ████████████████·· |
| `liquidity` | 7710 | 2275 | 1.50 | ████████████████·· |
| `macro` | 17635 | 1939 | 1.38 | ███████████████··· |
| `regime` | 4000 | 1440 | 1.38 | ███████████████··· |
| `rates` | 2571 | 763 | 1.38 | ███████████████··· |
| `momentum` | 15383 | 2628 | 0.86 | █████████········· |
| `trend` | 12427 | 1912 | 0.86 | █████████········· |
| `auction_market_theory` | 5486 | 1580 | 0.85 | █████████········· |
| `market_profile` | 3978 | 1388 | 0.85 | █████████········· |
| `statistical` | 20309 | 5378 | 0.83 | █████████········· |
| `pattern` | 10367 | 887 | 0.83 | █████████········· |
| `breakout` | 10338 | 887 | 0.83 | █████████········· |
| `mean_reversion` | 15541 | 4785 | 0.76 | ████████·········· |
| `volatility` | 14285 | 3675 | 0.76 | ████████·········· |
| `ict` | 5344 | 1406 | 0.75 | ████████·········· |
| `smc` | 5344 | 1406 | 0.75 | ████████·········· |
| `positioning` | 15748 | 1472 | 0.60 | ███████··········· |
| `ml_derived` | 2583 | 1171 | 0.60 | ███████··········· |
| `order_flow` | 988 | 118 | 0.55 | ██████············ |
| `cross_asset` | 394 | 168 | 0.53 | ██████············ |
| `intermarket` | 370 | 168 | 0.53 | ██████············ |
| `oscillator` | 10117 | 949 | 0.40 | ████·············· |
| `event` | 442 | 182 | 0.12 | █················· |
| `volume` | 2136 | 235 | 0.03 | ·················· |
| `mixed` | 68400 | 1225 | -0.11 | ·················· |
| `volume_profile` | 847 | 80 | -0.16 | ·················· |
| `crypto` | 715 | 218 | -0.30 | ·················· |
| `funding` | 715 | 218 | -0.30 | ·················· |
| `persistence` | 552 | 28 | -0.51 | ·················· |
| `calendar` | 17 | 0 | -1.69 | ·················· |
| `sentiment` | 6 | 0 | -20.43 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_2151a43e` | 2 | +19.283 | **carries signal** |
| `intx_987d68e3` | 2 | +16.725 | **carries signal** |
| `intx_7cd0e389` | 2 | +12.957 | **carries signal** |
| `intx_51b1b978` | 2 | +11.687 | **carries signal** |
| `intx_b56274fc` | 2 | +11.044 | **carries signal** |
| `intx_39ebaed9` | 2 | +10.526 | **carries signal** |
| `intx_ca1f399c` | 2 | +10.157 | **carries signal** |
| `intx_5191f1a1` | 15 | +8.524 | **carries signal** |
| `intx_d77b40a2` | 3 | +8.415 | **carries signal** |
| `intx_44967b18` | 37 | +8.243 | **carries signal** |
| `intx_b9823837` | 72 | +8.204 | **carries signal** |
| `intx_4d3d5099` | 13 | +8.026 | **carries signal** |
| `intx_76be7af0` | 38 | +7.771 | **carries signal** |
| `intx_1a9f34c1` | 41 | +7.566 | **carries signal** |
| `intx_2104a8b8` | 5 | +7.541 | **carries signal** |

---

## 5 · Archive (88 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:scalp:trade:long:low_vol` | xau | 2.740 |
| `xau:intraday:trade:long:low_vol` | xau | 2.554 |
| `xau:swing:trade:long:low_vol` | xau | 1.553 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
| `fx:position:low:long:all` | fx | 0.750 |
| `fx:position:med:long:all` | fx | 0.748 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `xau:intraday:low:neutral:all` | xau | 0.713 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.691 |
| `fx:swing:low:long:chop` | fx | 0.670 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `crypto:position:high:neutral:all` | crypto | 0.641 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.634 |
| `fx:swing:low:neutral:chop` | fx | 0.610 |
| `fx:swing:low:long:all` | fx | 0.610 |
| `xau:intraday:trade:long:chop` | xau | 0.580 |
| `fx:intraday:med:neutral:chop` | fx | 0.525 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:swing:low:short:low_vol` | crypto | 0.510 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.505 |
| `crypto:position:low:neutral:all` | crypto | 0.497 |
| `fx:position:low:neutral:all` | fx | 0.494 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |

## 6 · Lessons library (168,732)

- ×18 — [PASS] interaction+intx_01d36f0b+intx_218ac4c2+intx_48cd464a+intx_549c5216+intx_5519b55d+intx_876faca5+intx_9c85e9c3+
- ×6 — [GS_screen] breakout+interaction+intx_011edeee+intx_0507d207+intx_05645eba+intx_06f14519+intx_12692236+intx_2f8a0ced+intx_
- ×6 — [PASS] interaction+intx_05645eba+intx_4f4b182d+intx_981d69f8+intx_b132b6cc+mined+value_area_position+value_area_real 
- ×5 — [PASS] interaction+intx_218ac4c2+intx_48cd464a+intx_549c5216+intx_5519b55d+intx_876faca5+intx_9c85e9c3+mined+momentum
- ×5 — [PASS] mean_reversion+statistical on a directional book promoted to the candidate pool
- ×5 — [PASS] interaction+intx_218ac4c2+intx_48cd464a+intx_549c5216+intx_5519b55d+intx_876faca5+intx_9c85e9c3+intx_c1240e5f+
- ×4 — [GS_screen] interaction+intx_01d36f0b+intx_218ac4c2+intx_48cd464a+intx_549c5216+intx_5519b55d+intx_61059c5c+intx_a01af2cf+
- ×4 — [PASS] interaction+intx_0c7bda3f+intx_107a686b+intx_14539bcd+intx_e379cdeb+mined+momentum+oscillator on a cross_secti
- ×3 — [PASS] interaction+intx_28cc6b21+mean_reversion+mined+order_block_strength+statistical on a directional book promoted
- ×3 — [GS_screen] crypto+funding+interaction+intx_a16b7695+intx_ab31bc67+liquidity+macro+microstructure+mined+ml_derived+momentu
- ×3 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical+volatilit
- ×3 — [PASS] interaction+intx_01d36f0b+intx_218ac4c2+intx_48cd464a+intx_549c5216+intx_5519b55d+intx_61059c5c+intx_a01af2cf+
- ×3 — [GS_screen] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical+volatilit
- ×3 — [GS_screen] macro+positioning (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_single=0.009
- ×3 — [PASS] interaction+intx_981d69f8+intx_b132b6cc+mined+value_area_position+value_area_real on a directional book promot

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*