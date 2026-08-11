# 🧬 Master Trader — Genome Population Report

*Generated 2026-08-11 14:40 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **129,870** |
| Deflated-Sharpe trial count (raw N) | **318,186** *(evals 129,870 + 188,316 screened)* |
| **Effective** independent trials (N_eff) | **270,886** *(ρ̄=0.0394268051978291 — the bar the DSR actually uses)* |
| Admitted to archive | **11502** |
| Rejected | **118,368** (91.1%) |
| Distinct families explored | **31** |
| Lessons accumulated | **89,289** |
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
| `—` | 86,766 | 66.8% | — |
| `GS_screen` | 17,299 | 13.3% | — |
| `ADMITTED` | 11,502 | 8.9% | **cleared every gate** |
| `G1_sanity` | 7,604 | 5.9% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,507 | 2.7% | parameter tuning overfit (high PBO) |
| `G0_eval` | 1,345 | 1.0% | did not produce a valid backtest |
| `G9_plateau` | 1,284 | 1.0% | — |
| `G8_orthogonality` | 290 | 0.2% | duplicates an existing archive member |
| `G5_robustness` | 222 | 0.2% | bootstrap tail drawdown too large |
| `G2_oos` | 51 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 46192 | 2830 | 1.50 | ████████████████·· |
| `xau` | 38211 | 6955 | 0.83 | █████████········· |
| `fx` | 45467 | 1717 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 97318 | 4635 | 1.50 | ████████████████·· |
| `directional` | 32552 | 6867 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 107603 | 11484 | 1.50 | ████████████████·· |
| `llm` | 7461 | 11 | 1.35 | ███████████████··· |
| `template` | 4128 | 0 | 0.31 | ███··············· |
| `random` | 4545 | 0 | -0.67 | ·················· |
| `miner` | 6133 | 7 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 73263 | 4119 | 1.50 | ████████████████·· |
| `low_vol` | 38909 | 7110 | 0.83 | █████████········· |
| `chop` | 4824 | 14 | 0.22 | ██················ |
| `trend` | 6887 | 214 | 0.02 | ·················· |
| `high_vol` | 5987 | 45 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 100147 | 6058 | 1.50 | ████████████████·· |
| `kelly_fraction` | 1189 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 25117 | 5433 | 0.76 | ████████·········· |
| `vol_target` | 2112 | 1 | -1.05 | ·················· |
| `atr_scaled` | 1305 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 20747 | 2735 | 1.50 | ████████████████·· |
| `liquidity` | 20131 | 2726 | 1.50 | ████████████████·· |
| `macro` | 21559 | 2368 | 1.38 | ███████████████··· |
| `regime` | 12695 | 1757 | 1.38 | ███████████████··· |
| `rates` | 7379 | 921 | 1.38 | ███████████████··· |
| `momentum` | 19834 | 2254 | 0.86 | █████████········· |
| `trend` | 16703 | 1781 | 0.86 | █████████········· |
| `auction_market_theory` | 15781 | 1926 | 0.85 | █████████········· |
| `market_profile` | 12563 | 1703 | 0.85 | █████████········· |
| `statistical` | 21841 | 5458 | 0.83 | █████████········· |
| `pattern` | 3084 | 105 | 0.83 | █████████········· |
| `breakout` | 2980 | 105 | 0.83 | █████████········· |
| `volatility` | 18657 | 4374 | 0.76 | ████████·········· |
| `mean_reversion` | 14901 | 4689 | 0.76 | ████████·········· |
| `ict` | 5968 | 1557 | 0.75 | ████████·········· |
| `smc` | 5968 | 1557 | 0.75 | ████████·········· |
| `positioning` | 16755 | 1827 | 0.60 | ███████··········· |
| `ml_derived` | 9774 | 1415 | 0.60 | ███████··········· |
| `order_flow` | 1960 | 161 | 0.55 | ██████············ |
| `cross_asset` | 1551 | 189 | 0.53 | ██████············ |
| `intermarket` | 1504 | 189 | 0.53 | ██████············ |
| `oscillator` | 3305 | 182 | 0.40 | ████·············· |
| `event` | 2085 | 228 | 0.12 | █················· |
| `volume` | 3825 | 300 | 0.03 | ·················· |
| `mixed` | 55143 | 1101 | -0.11 | ·················· |
| `volume_profile` | 1596 | 101 | -0.16 | ·················· |
| `crypto` | 2594 | 276 | -0.30 | ·················· |
| `funding` | 2594 | 276 | -0.30 | ·················· |
| `persistence` | 891 | 27 | -0.51 | ·················· |
| `calendar` | 15 | 0 | -1.69 | ·················· |
| `sentiment` | 10 | 0 | -17.94 | ·················· |

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
| `intx_62a4f5a8` | 2 | +5.872 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_9a54d399` | 2 | +4.831 | **carries signal** |
| `intx_11c3fc85` | 8 | +3.177 | **carries signal** |
| `intx_a8d3bd78` | 5 | +2.499 | **carries signal** |
| `intx_025b0355` | 760 | +2.426 | **carries signal** |
| `intx_f116e2af` | 473 | +2.393 | **carries signal** |
| `intx_47a8478d` | 62 | +2.344 | **carries signal** |

---

## 5 · Archive (64 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.857 |
| `xau:swing:trade:long:low_vol` | xau | 1.215 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
| `fx:position:low:long:all` | fx | 0.750 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `fx:position:med:long:all` | fx | 0.693 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `crypto:position:high:neutral:all` | crypto | 0.641 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:intraday:med:neutral:chop` | fx | 0.525 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.505 |
| `xau:intraday:low:neutral:all` | xau | 0.495 |
| `fx:position:low:neutral:all` | fx | 0.494 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.427 |
| `fx:swing:med:long:all` | fx | 0.416 |
| `crypto:position:low:short:all` | crypto | 0.405 |

## 6 · Lessons library (89,289)

- ×13 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×12 — [GS_screen] auction_market_theory+hurst+ict+interaction+intx_03db8e1d+intx_8777c77c+intx_8e0d4062+intx_95944cb1+intx_a16b7
- ×8 — [GS_screen] interaction+intx_080bbe39+intx_10e814d4+intx_e6144124+macro+mined+poc_distance_real+positioning (cross_section
- ×7 — [GS_screen] interaction+intx_01e05829+intx_10e814d4+intx_13e60945+intx_1dafe536+intx_fc1a7433+mined+poc_distance_real (cro
- ×7 — [PASS] adx+candlestick_pattern+ict+interaction+intx_0507d207+intx_3086ff7a+intx_382083bf+intx_753ea6e7+intx_8e0d4062+
- ×6 — [GS_screen] liquidity+macro+mean_reversion+microstructure+momentum+positioning+statistical (cross_sectional) — raw predict
- ×6 — [GS_screen] auction_market_theory+liquidity+market_profile+microstructure+ml_derived+momentum+regime+trend (cross_sectiona
- ×6 — [GS_screen] liquidity+macro+microstructure+positioning (cross_sectional) — raw predictive strength too weak to clear the F
- ×5 — [GS_screen] har_vol+interaction+intx_10e814d4+intx_13e60945+intx_2f41065c+intx_8eae474d+intx_92873c43+intx_ba9e2ee2+intx_f
- ×5 — [GS_screen] interaction+intx_19456efa+intx_315232f3+intx_4334a9e2+intx_7f80f9ab+intx_8d20bcb1+intx_b55640b0+mined (cross_s
- ×4 — [GS_screen] interaction+intx_315232f3+intx_7f80f9ab+mined (cross_sectional) — raw predictive strength too weak to clear th
- ×4 — [PASS] adx+candlestick_pattern+interaction+intx_0507d207+intx_382083bf+mean_reversion+mined+statistical on a directio
- ×4 — [GS_screen] interaction+intx_10e814d4+intx_495677d1+intx_d18f920f+mined+poc_distance_real (cross_sectional) — raw predicti
- ×4 — [GS_screen] interaction+intx_01e05829+intx_1dafe536+mined+statistical (cross_sectional) — raw predictive strength too weak
- ×4 — [G1_sanity] interaction+intx_2384226f+intx_755afa36+mined (cross_sectional) — degenerate P&L — too few trades, or one bar 

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*