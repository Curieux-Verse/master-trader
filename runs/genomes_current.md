# 🧬 Master Trader — Genome Population Report

*Generated 2026-11-10 04:52 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **141,563** |
| Deflated-Sharpe trial count (raw N) | **755,223** *(evals 141,563 + 613,660 screened)* |
| **Effective** independent trials (N_eff) | **700,541** *(ρ̄=0.0739561895344011 — the bar the DSR actually uses)* |
| Admitted to archive | **10125** |
| Rejected | **131,438** (92.8%) |
| Distinct families explored | **31** |
| Lessons accumulated | **259,957** |
| Best DSR-z | **+1.503** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `f9b357250744cb4d` | crypto | **1.50** | 0.5998 | 4.23 | 0.031 | cross_sectional | all | `G3_cpcv_pbo` |
| 2 | `db1116ef1b1daa2e` | crypto | **1.45** | 0.8313 | 5.61 | 0.034 | cross_sectional | all | `ADMITTED` |
| 3 | `f91ac9df4c92294d` | crypto | **1.44** | 0.8360 | 5.65 | 0.033 | cross_sectional | all | `ADMITTED` |
| 4 | `791009c7f085c6aa` | crypto | **1.43** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 5 | `6d03423485a0e4a7` | crypto | **1.43** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 6 | `c7f59950aa197236` | crypto | **1.42** | 0.8318 | 5.62 | 0.033 | cross_sectional | all | `ADMITTED` |
| 7 | `7e6ad3c6df7a9643` | crypto | **1.42** | 0.5725 | 4.04 | 0.037 | cross_sectional | all | `G3_cpcv_pbo` |
| 8 | `e2932cabac0a7ae1` | crypto | **1.41** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 9 | `726f5f4697c4db1c` | crypto | **1.41** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 10 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 11 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 12 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 13 | `cd01243357770202` | crypto | **1.29** | 0.8015 | 5.41 | 0.043 | cross_sectional | all | `ADMITTED` |
| 14 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 15 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 16 | `64eed38552709d9a` | crypto | **1.16** | 0.7519 | 5.08 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 17 | `473219061ecd274b` | crypto | **1.13** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 18 | `427fb1bac0b4316a` | crypto | **1.12** | 0.9182 | 6.20 | 0.042 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `ebe2e17a51d99e1d` | crypto | **1.12** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `d46787c84831d425` | crypto | **1.12** | 0.8781 | 5.93 | 0.038 | cross_sectional | all | `G3_cpcv_pbo` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `f9b357250744cb4d` — DSR-z 1.50 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.3522641431182003, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=f9b357250744cb4d  gen=30  by=evo_mutate  nodes=4
```
**#2 · `db1116ef1b1daa2e` — DSR-z 1.45 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.009601909168493)
  id=db1116ef1b1daa2e  gen=41  by=evo_mutate  nodes=4
```
**#3 · `f91ac9df4c92294d` — DSR-z 1.44 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0491530175959747)
  id=f91ac9df4c92294d  gen=56  by=evo_mutate  nodes=4
```
**#4 · `791009c7f085c6aa` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=791009c7f085c6aa  gen=59  by=evo_crossover  nodes=4
```
**#5 · `6d03423485a0e4a7` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=6d03423485a0e4a7  gen=44  by=evo_crossover  nodes=4
```
**#6 · `c7f59950aa197236` — DSR-z 1.42 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.3153903380020915)
  id=c7f59950aa197236  gen=61  by=evo_mutate  nodes=4
```
**#7 · `7e6ad3c6df7a9643` — DSR-z 1.42 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); amihud_illiquidity(window=32)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=7e6ad3c6df7a9643  gen=21  by=evo_mutate  nodes=5
```
**#8 · `e2932cabac0a7ae1` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=e2932cabac0a7ae1  gen=55  by=evo_mutate  nodes=4
```
**#9 · `726f5f4697c4db1c` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=726f5f4697c4db1c  gen=74  by=evo_crossover  nodes=4
```
**#10 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#11 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#12 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#13 · `cd01243357770202` — DSR-z 1.29 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.987931652984258, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=cd01243357770202  gen=79  by=evo_mutate  nodes=4
```
**#14 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#15 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
**#16 · `64eed38552709d9a` — DSR-z 1.16 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.4384386928813)
  id=64eed38552709d9a  gen=36  by=evo_mutate  nodes=4
```
**#17 · `473219061ecd274b` — DSR-z 1.13 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=473219061ecd274b  gen=49  by=evo_mutate  nodes=4
```
**#18 · `427fb1bac0b4316a` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=66)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.09311457267804286)
  risk:     horizon_hold(horizon=48, cost_stress=1.0433464695652956)
  id=427fb1bac0b4316a  gen=44  by=evo_mutate  nodes=4
```
**#19 · `ebe2e17a51d99e1d` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=ebe2e17a51d99e1d  gen=51  by=evo_crossover  nodes=4
```
**#20 · `d46787c84831d425` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=64)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4256268738732438, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=d46787c84831d425  gen=83  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `—` | 87,432 | 61.8% | — |
| `GS_screen` | 23,005 | 16.3% | — |
| `ADMITTED` | 10,125 | 7.2% | **cleared every gate** |
| `G1_sanity` | 9,172 | 6.5% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 6,001 | 4.2% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 2,472 | 1.7% | parameter tuning overfit (high PBO) |
| `G9_plateau` | 1,696 | 1.2% | — |
| `G5_robustness` | 1,289 | 0.9% | bootstrap tail drawdown too large |
| `G8_orthogonality` | 353 | 0.2% | duplicates an existing archive member |
| `G2_oos` | 18 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 49317 | 2398 | 1.50 | ████████████████·· |
| `xau` | 46663 | 5527 | 0.76 | ████████·········· |
| `fx` | 45583 | 2200 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 114799 | 4637 | 1.50 | ████████████████·· |
| `directional` | 26764 | 5488 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 87363 | 10105 | 1.50 | ████████████████·· |
| `llm` | 14943 | 12 | 1.35 | ███████████████··· |
| `template` | 9626 | 0 | 0.31 | ███··············· |
| `random` | 14410 | 6 | -0.67 | ·················· |
| `miner` | 15221 | 2 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 71012 | 3139 | 1.50 | ████████████████·· |
| `low_vol` | 27818 | 5816 | 0.76 | ████████·········· |
| `trend` | 9034 | 119 | 0.58 | ██████············ |
| `chop` | 25252 | 1003 | 0.22 | ██················ |
| `high_vol` | 8447 | 48 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 106693 | 5680 | 1.50 | ████████████████·· |
| `kelly_fraction` | 3737 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 20999 | 4416 | 0.76 | ████████·········· |
| `vol_target` | 5595 | 10 | -0.01 | ·················· |
| `atr_scaled` | 4539 | 10 | -1.56 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 13473 | 2063 | 1.50 | ████████████████·· |
| `liquidity` | 13206 | 2057 | 1.50 | ████████████████·· |
| `macro` | 22765 | 2380 | 1.38 | ███████████████··· |
| `regime` | 6238 | 1190 | 1.38 | ███████████████··· |
| `rates` | 4118 | 602 | 1.38 | ███████████████··· |
| `momentum` | 20821 | 1918 | 0.86 | █████████········· |
| `trend` | 12696 | 1260 | 0.86 | █████████········· |
| `auction_market_theory` | 9144 | 1320 | 0.85 | █████████········· |
| `market_profile` | 6173 | 1088 | 0.85 | █████████········· |
| `volatility` | 14543 | 3086 | 0.76 | ████████·········· |
| `statistical` | 14179 | 4339 | 0.76 | ████████·········· |
| `mean_reversion` | 10931 | 3832 | 0.76 | ████████·········· |
| `ict` | 4941 | 1078 | 0.75 | ████████·········· |
| `smc` | 4941 | 1078 | 0.75 | ████████·········· |
| `positioning` | 19865 | 1999 | 0.60 | ███████··········· |
| `ml_derived` | 3735 | 965 | 0.60 | ███████··········· |
| `mixed` | 68079 | 1000 | 0.58 | ██████············ |
| `order_flow` | 1968 | 95 | 0.55 | ██████············ |
| `cross_asset` | 807 | 125 | 0.53 | ██████············ |
| `intermarket` | 800 | 125 | 0.53 | ██████············ |
| `pattern` | 8027 | 361 | 0.46 | █████············· |
| `breakout` | 8000 | 361 | 0.46 | █████············· |
| `oscillator` | 11498 | 375 | 0.40 | ████·············· |
| `event` | 664 | 137 | 0.12 | █················· |
| `volume` | 3998 | 413 | 0.03 | ·················· |
| `volume_profile` | 1786 | 68 | -0.16 | ·················· |
| `crypto` | 963 | 164 | -0.30 | ·················· |
| `funding` | 963 | 164 | -0.30 | ·················· |
| `persistence` | 1602 | 26 | -0.51 | ·················· |
| `calendar` | 10 | 0 | -1.69 | ·················· |
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
| `intx_cd71e4f7` | 2 | +10.383 | **carries signal** |
| `intx_ca1f399c` | 2 | +10.157 | **carries signal** |
| `intx_cdfae457` | 2 | +9.642 | **carries signal** |
| `intx_01f14384` | 2 | +7.578 | **carries signal** |
| `intx_5a3b5c9d` | 2 | +7.350 | **carries signal** |
| `intx_a16ff4f4` | 2 | +6.851 | **carries signal** |
| `intx_e6f884fd` | 2 | +6.794 | **carries signal** |
| `intx_911ab9c3` | 2 | +6.511 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_451d38d9` | 151 | +5.132 | **carries signal** |
| `intx_964d4fc3` | 204 | +5.022 | **carries signal** |

---

## 5 · Archive (103 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:scalp:trade:long:low_vol` | xau | 2.740 |
| `xau:intraday:trade:long:low_vol` | xau | 2.554 |
| `xau:swing:trade:long:low_vol` | xau | 1.553 |
| `crypto:swing:trade:short:high_vol` | crypto | 1.016 |
| `crypto:intraday:trade:short:low_vol` | crypto | 0.989 |
| `crypto:swing:trade:short:trend` | crypto | 0.942 |
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

## 6 · Lessons library (259,957)

- ×17 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×10 — [GS_screen] liquidity+macro+microstructure+rates+regime (cross_sectional) — raw predictive strength too weak to clear the 
- ×7 — [GS_screen] liquidity+macro+microstructure+positioning (cross_sectional) — raw predictive strength too weak to clear the F
- ×7 — [GS_screen] interaction+intx_14539bcd+intx_16f6ebcd+intx_27dc106a+intx_2e7d802f+intx_2f41065c+intx_405ab659+intx_545064f9+
- ×6 — [PASS] interaction+intx_137ddd7b+intx_16aa9ad2+intx_3b97b11a+intx_421762f1+intx_82714592+intx_9545338d+liquidity+micr
- ×6 — [GS_screen] interaction+intx_16f6ebcd+intx_32b625ae+intx_43358a66+intx_a140ca24+intx_c9e8c607+intx_caac6070+intx_cfbc8793+
- ×5 — [PASS] fvg_gap+interaction+intx_05be4188+intx_137ddd7b+intx_16aa9ad2+intx_16e5ef70+intx_192bc6f5+intx_3b85adb2+intx_3
- ×5 — [PASS] amihud_illiquidity+interaction+intx_1b124f84+intx_4334a9e2+intx_4e0f2187+intx_7045ff6b+intx_b55640b0+macro+min
- ×4 — [GS_screen] dist_to_poc+interaction+intx_14539bcd+intx_218ac4c2+intx_405ab659+intx_ab2eddd8+intx_b0c5b5aa+intx_cada3db7+in
- ×4 — [GS_screen] momentum+oscillator+volatility (directional) — raw predictive strength too weak to clear the FDR screen [p_sin
- ×3 — [GS_screen] fvg_gap+interaction+intx_05be4188+intx_137ddd7b+intx_16aa9ad2+intx_16e5ef70+intx_192bc6f5+intx_3b85adb2+intx_3
- ×3 — [PASS] interaction+intx_0529678c+intx_2c28f658+intx_7201b206+intx_ba60ed41+liquidity+microstructure+mined+momentum+vo
- ×3 — [GS_screen] interaction+intx_0b759993+intx_8958872a+macro+mined+positioning (cross_sectional) — raw predictive strength to
- ×3 — [PASS] fvg_gap+interaction+intx_05be4188+intx_137ddd7b+intx_16aa9ad2+intx_192bc6f5+intx_3b97b11a+intx_3f64b63b+intx_4
- ×3 — [GS_screen] dist_to_poc+interaction+intx_ab2eddd8+intx_dcd81f81+intx_e04c1e10+mined (cross_sectional) — raw predictive str

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*