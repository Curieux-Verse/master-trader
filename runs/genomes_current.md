# 🧬 Master Trader — Genome Population Report

*Generated 2026-09-03 04:22 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **135,567** |
| Deflated-Sharpe trial count (raw N) | **418,114** *(evals 135,567 + 282,547 screened)* |
| **Effective** independent trials (N_eff) | **382,269** *(ρ̄=0.013201796920289378 — the bar the DSR actually uses)* |
| Admitted to archive | **12310** |
| Rejected | **123,257** (90.9%) |
| Distinct families explored | **31** |
| Lessons accumulated | **132,884** |
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
| `—` | 90,010 | 66.4% | — |
| `GS_screen` | 16,741 | 12.3% | — |
| `ADMITTED` | 12,310 | 9.1% | **cleared every gate** |
| `G1_sanity` | 8,441 | 6.2% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,413 | 2.5% | parameter tuning overfit (high PBO) |
| `G0_eval` | 2,307 | 1.7% | did not produce a valid backtest |
| `G9_plateau` | 1,744 | 1.3% | — |
| `G8_orthogonality` | 302 | 0.2% | duplicates an existing archive member |
| `G5_robustness` | 189 | 0.1% | bootstrap tail drawdown too large |
| `G2_oos` | 110 | 0.1% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 47432 | 3685 | 1.50 | ████████████████·· |
| `xau` | 38149 | 7052 | 0.83 | █████████········· |
| `fx` | 49986 | 1573 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 104689 | 5346 | 1.50 | ████████████████·· |
| `directional` | 30878 | 6964 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 115510 | 12295 | 1.50 | ████████████████·· |
| `llm` | 3401 | 10 | 1.35 | ███████████████··· |
| `template` | 3725 | 0 | 0.31 | ███··············· |
| `random` | 3507 | 0 | -0.67 | ·················· |
| `miner` | 9424 | 5 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 77332 | 4016 | 1.50 | ████████████████·· |
| `low_vol` | 38893 | 7309 | 0.83 | █████████········· |
| `chop` | 10856 | 822 | 0.22 | ██················ |
| `trend` | 4510 | 126 | 0.02 | ·················· |
| `high_vol` | 3976 | 37 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 106408 | 6599 | 1.50 | ████████████████·· |
| `kelly_fraction` | 799 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 26468 | 5701 | 0.76 | ████████·········· |
| `vol_target` | 1011 | 1 | -1.05 | ·················· |
| `atr_scaled` | 881 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 15473 | 2354 | 1.50 | ████████████████·· |
| `liquidity` | 15063 | 2344 | 1.50 | ████████████████·· |
| `macro` | 18671 | 2010 | 1.38 | ███████████████··· |
| `regime` | 9565 | 1488 | 1.38 | ███████████████··· |
| `rates` | 6280 | 791 | 1.38 | ███████████████··· |
| `trend` | 17404 | 2269 | 0.86 | █████████········· |
| `momentum` | 14856 | 1857 | 0.86 | █████████········· |
| `auction_market_theory` | 12183 | 1649 | 0.85 | █████████········· |
| `market_profile` | 9640 | 1428 | 0.85 | █████████········· |
| `statistical` | 22937 | 5365 | 0.83 | █████████········· |
| `pattern` | 11023 | 1352 | 0.83 | █████████········· |
| `breakout` | 10948 | 1352 | 0.83 | █████████········· |
| `volatility` | 18695 | 4313 | 0.76 | ████████·········· |
| `mean_reversion` | 15890 | 4691 | 0.76 | ████████·········· |
| `ict` | 5505 | 1367 | 0.75 | ████████·········· |
| `smc` | 5505 | 1367 | 0.75 | ████████·········· |
| `positioning` | 14909 | 1532 | 0.60 | ███████··········· |
| `ml_derived` | 7130 | 1213 | 0.60 | ███████··········· |
| `order_flow` | 1083 | 125 | 0.55 | ██████············ |
| `cross_asset` | 968 | 171 | 0.53 | ██████············ |
| `intermarket` | 919 | 171 | 0.53 | ██████············ |
| `oscillator` | 3515 | 130 | 0.40 | ████·············· |
| `event` | 1693 | 184 | 0.12 | █················· |
| `volume` | 3360 | 262 | 0.03 | ·················· |
| `mixed` | 61012 | 1302 | -0.11 | ·················· |
| `volume_profile` | 822 | 99 | -0.16 | ·················· |
| `crypto` | 1878 | 224 | -0.30 | ·················· |
| `funding` | 1878 | 224 | -0.30 | ·················· |
| `persistence` | 842 | 22 | -0.51 | ·················· |
| `calendar` | 9 | 0 | -1.69 | ·················· |
| `sentiment` | 3 | 0 | -20.43 | ·················· |

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
| `intx_5a3b5c9d` | 2 | +7.350 | **carries signal** |
| `intx_382083bf` | 2 | +7.016 | **carries signal** |
| `intx_c73aa979` | 117 | +6.645 | **carries signal** |
| `intx_911ab9c3` | 2 | +6.511 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_62a4f5a8` | 2 | +5.872 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_0a59f355` | 143 | +5.299 | **carries signal** |
| `intx_9a54d399` | 2 | +4.831 | **carries signal** |
| `intx_55ce37c0` | 13 | +4.017 | **carries signal** |

---

## 5 · Archive (70 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:scalp:trade:long:low_vol` | xau | 2.740 |
| `xau:intraday:trade:long:low_vol` | xau | 2.554 |
| `xau:swing:trade:long:low_vol` | xau | 1.363 |
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
| `fx:swing:low:long:all` | fx | 0.610 |
| `fx:intraday:med:neutral:chop` | fx | 0.525 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.505 |
| `fx:position:low:neutral:all` | fx | 0.494 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `crypto:position:high:neutral:chop` | crypto | 0.475 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:intraday:med:neutral:all` | fx | 0.440 |

## 6 · Lessons library (132,884)

- ×8 — [PASS] volatility on a directional book promoted to the candidate pool
- ×8 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×7 — [GS_screen] interaction+intx_be1d0efc+mined+structure_break (cross_sectional) — raw predictive strength too weak to clear 
- ×7 — [GS_screen] interaction+intx_14539bcd+mined+rel_volume (cross_sectional) — raw predictive strength too weak to clear the F
- ×7 — [GS_screen] breakout+interaction+intx_011edeee+intx_0507d207+intx_06f14519+intx_12692236+intx_40f73767+intx_525eb3f5+intx_
- ×6 — [GS_screen] interaction+intx_39165f4d+intx_4f97afa7+mined+momentum+oscillator (cross_sectional) — raw predictive strength 
- ×6 — [GS_screen] interaction+intx_05619c19+intx_27564229+mined (cross_sectional) — raw predictive strength too weak to clear th
- ×5 — [GS_screen] amihud_illiquidity+interaction+intx_10e814d4+intx_458d91e4+intx_58001d43+intx_6a4a9e33+intx_7045ff6b+intx_b6c7
- ×5 — [GS_screen] interaction+intx_10e814d4+intx_13e60945+intx_19456efa+intx_5872255c+intx_8d20bcb1+intx_8eae474d+intx_92873c43+
- ×5 — [GS_screen] interaction+intx_10e814d4+intx_58001d43+intx_6a4a9e33+intx_c1240e5f+intx_e4425d6a+macro+mined+poc_distance_rea
- ×5 — [GS_screen] interaction+intx_3e6273f0+intx_b588ee74+intx_ceae8a96+intx_d790d760+macro+mined+positioning+statistical (cross
- ×4 — [PASS] adx+candlestick_pattern+interaction+mean_reversion+mined+statistical on a directional book promoted to the can
- ×4 — [GS_screen] interaction+intx_11b7cd52+intx_4eec473c+intx_5e6d7d2a+intx_a3a6288c+mined (directional) — raw predictive stren
- ×4 — [GS_screen] breakout+interaction+intx_07b6ad25+intx_0f5c18ca+intx_346a0f82+intx_3d05d214+intx_95020b8c+intx_cbbc077a+intx_
- ×4 — [PASS] har_vol+interaction+mined+value_area_position+volatility on a directional book promoted to the candidate pool

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*