# 🧬 Master Trader — Genome Population Report

*Generated 2026-11-04 04:29 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **141,091** |
| Deflated-Sharpe trial count (raw N) | **732,915** *(evals 141,091 + 591,824 screened)* |
| **Effective** independent trials (N_eff) | **921,282** *(ρ̄=0.009479465655650323 — the bar the DSR actually uses)* |
| Admitted to archive | **10092** |
| Rejected | **130,999** (92.8%) |
| Distinct families explored | **31** |
| Lessons accumulated | **252,598** |
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
| `—` | 86,882 | 61.6% | — |
| `GS_screen` | 23,789 | 16.9% | — |
| `ADMITTED` | 10,092 | 7.2% | **cleared every gate** |
| `G1_sanity` | 8,727 | 6.2% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 5,863 | 4.2% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 2,322 | 1.6% | parameter tuning overfit (high PBO) |
| `G9_plateau` | 1,720 | 1.2% | — |
| `G5_robustness` | 1,331 | 0.9% | bootstrap tail drawdown too large |
| `G8_orthogonality` | 344 | 0.2% | duplicates an existing archive member |
| `G2_oos` | 21 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 50606 | 2151 | 1.50 | ████████████████·· |
| `xau` | 46152 | 5532 | 0.76 | ████████·········· |
| `fx` | 44333 | 2409 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 113682 | 4622 | 1.50 | ████████████████·· |
| `directional` | 27409 | 5470 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 88233 | 10071 | 1.50 | ████████████████·· |
| `llm` | 13854 | 13 | 1.35 | ███████████████··· |
| `template` | 10647 | 0 | 0.31 | ███··············· |
| `random` | 13933 | 6 | -0.67 | ·················· |
| `miner` | 14424 | 2 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 66740 | 3058 | 1.50 | ████████████████·· |
| `low_vol` | 28963 | 5819 | 0.76 | ████████·········· |
| `chop` | 28014 | 1074 | 0.22 | ██················ |
| `trend` | 8600 | 97 | 0.02 | ·················· |
| `high_vol` | 8774 | 44 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 105525 | 5667 | 1.50 | ████████████████·· |
| `kelly_fraction` | 3715 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 21515 | 4398 | 0.76 | ████████·········· |
| `vol_target` | 5862 | 8 | -0.01 | ·················· |
| `atr_scaled` | 4474 | 10 | -1.56 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 12703 | 1806 | 1.50 | ████████████████·· |
| `liquidity` | 12341 | 1800 | 1.50 | ████████████████·· |
| `macro` | 24293 | 2545 | 1.38 | ███████████████··· |
| `regime` | 6545 | 1152 | 1.38 | ███████████████··· |
| `rates` | 4226 | 611 | 1.38 | ███████████████··· |
| `momentum` | 19864 | 1752 | 0.86 | █████████········· |
| `trend` | 13842 | 1313 | 0.86 | █████████········· |
| `auction_market_theory` | 10181 | 1351 | 0.85 | █████████········· |
| `market_profile` | 7115 | 1116 | 0.85 | █████████········· |
| `volatility` | 15028 | 3094 | 0.76 | ████████·········· |
| `statistical` | 14733 | 4346 | 0.76 | ████████·········· |
| `mean_reversion` | 11103 | 3838 | 0.76 | ████████·········· |
| `ict` | 4768 | 1095 | 0.75 | ████████·········· |
| `smc` | 4768 | 1095 | 0.75 | ████████·········· |
| `positioning` | 21421 | 2162 | 0.60 | ███████··········· |
| `ml_derived` | 4315 | 927 | 0.60 | ███████··········· |
| `order_flow` | 2265 | 96 | 0.55 | ██████············ |
| `cross_asset` | 987 | 126 | 0.53 | ██████············ |
| `intermarket` | 981 | 126 | 0.53 | ██████············ |
| `pattern` | 8383 | 391 | 0.46 | █████············· |
| `breakout` | 8370 | 391 | 0.46 | █████············· |
| `oscillator` | 10050 | 433 | 0.40 | ████·············· |
| `event` | 806 | 141 | 0.12 | █················· |
| `volume` | 3762 | 277 | 0.03 | ·················· |
| `mixed` | 66333 | 975 | -0.01 | ·················· |
| `volume_profile` | 2018 | 69 | -0.16 | ·················· |
| `crypto` | 1159 | 164 | -0.30 | ·················· |
| `funding` | 1159 | 164 | -0.30 | ·················· |
| `persistence` | 1653 | 26 | -0.51 | ·················· |
| `calendar` | 12 | 0 | -1.69 | ·················· |
| `sentiment` | 1 | 0 | — | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_2151a43e` | 2 | +19.283 | **carries signal** |
| `intx_987d68e3` | 2 | +16.725 | **carries signal** |
| `intx_e3f7eacf` | 2 | +12.317 | **carries signal** |
| `intx_b56274fc` | 2 | +11.044 | **carries signal** |
| `intx_9f81d9e7` | 2 | +10.655 | **carries signal** |
| `intx_cd71e4f7` | 2 | +10.383 | **carries signal** |
| `intx_ca1f399c` | 2 | +10.157 | **carries signal** |
| `intx_cdfae457` | 2 | +9.642 | **carries signal** |
| `intx_01f14384` | 2 | +7.578 | **carries signal** |
| `intx_5a3b5c9d` | 2 | +7.350 | **carries signal** |
| `intx_a16ff4f4` | 2 | +6.851 | **carries signal** |
| `intx_e6f884fd` | 2 | +6.794 | **carries signal** |
| `intx_911ab9c3` | 2 | +6.511 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_42af0c76` | 18 | +6.426 | **carries signal** |

---

## 5 · Archive (97 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:scalp:trade:long:low_vol` | xau | 2.740 |
| `xau:intraday:trade:long:low_vol` | xau | 2.554 |
| `xau:swing:trade:long:low_vol` | xau | 1.553 |
| `fx:position:low:neutral:all` | fx | 0.818 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
| `fx:position:low:long:all` | fx | 0.798 |
| `fx:swing:low:long:chop` | fx | 0.753 |
| `fx:position:med:long:all` | fx | 0.748 |
| `xau:intraday:low:long:trend` | xau | 0.738 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `xau:intraday:low:neutral:all` | xau | 0.713 |
| `fx:swing:low:neutral:chop` | fx | 0.711 |
| `crypto:intraday:trade:short:chop` | crypto | 0.696 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.691 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `fx:swing:med:long:chop` | fx | 0.649 |
| `crypto:position:high:neutral:all` | crypto | 0.641 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.634 |
| `fx:swing:low:long:all` | fx | 0.610 |
| `xau:intraday:trade:long:chop` | xau | 0.580 |
| `crypto:intraday:trade:short:all` | crypto | 0.555 |
| `fx:intraday:med:neutral:chop` | fx | 0.525 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:swing:low:short:low_vol` | crypto | 0.510 |

## 6 · Lessons library (252,598)

- ×11 — [GS_screen] interaction+intx_1f414506+intx_42055f3a+intx_4807b2dc+intx_4b3d0eab+intx_78328689+intx_97f22c70+mined+momentum
- ×9 — [GS_screen] interaction+intx_14539bcd+intx_27dc106a+intx_405ab659+intx_770c5352+intx_96e8b190+intx_ca069136+intx_d4b0d2ae+
- ×9 — [GS_screen] interaction+intx_2f41065c+intx_39165f4d+intx_96e8b190+intx_a2b3aba9+intx_ca069136+intx_d4b0d2ae+intx_f084521e+
- ×5 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×5 — [PASS] interaction+intx_14539bcd+intx_405ab659+macro+mined+positioning on a cross_sectional book promoted to the cand
- ×4 — [GS_screen] interaction+intx_14539bcd+intx_405ab659+macro+mined+positioning (cross_sectional) — raw predictive strength to
- ×4 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×4 — [GS_screen] interaction+intx_53994686+intx_5cbe5561+intx_5e83ad23+intx_666963b3+intx_ede23478+intx_f852ea6a+liquidity+macr
- ×4 — [GS_screen] liquidity+microstructure+momentum (cross_sectional) — raw predictive strength too weak to clear the FDR screen
- ×4 — [GS_screen] breakout+pattern+statistical (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_s
- ×4 — [GS_screen] interaction+intx_47d7caa3+intx_8848ce7f+mined (cross_sectional) — raw predictive strength too weak to clear th
- ×4 — [GS_screen] liquidity+macro+microstructure+rates+regime (cross_sectional) — raw predictive strength too weak to clear the 
- ×3 — [G1_sanity] interaction+intx_030d2e02+intx_1e2a2b66+intx_57babc1d+intx_d89087f9+mined (cross_sectional) — degenerate P&L —
- ×3 — [PASS] macro+positioning on a cross_sectional book promoted to the candidate pool
- ×3 — [GS_screen] ict+interaction+intx_3086ff7a+intx_5e4e3ecd+intx_753ea6e7+intx_8e0d4062+intx_d2df6440+intx_fe341f6e+mean_rever

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*