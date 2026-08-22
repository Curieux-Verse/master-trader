# 🧬 Master Trader — Genome Population Report

*Generated 2026-08-22 04:47 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **134,496** |
| Deflated-Sharpe trial count (raw N) | **389,530** *(evals 134,496 + 255,034 screened)* |
| **Effective** independent trials (N_eff) | **280,475** *(ρ̄=0.08404044139311423 — the bar the DSR actually uses)* |
| Admitted to archive | **13051** |
| Rejected | **121,445** (90.3%) |
| Distinct families explored | **31** |
| Lessons accumulated | **120,162** |
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
| `—` | 89,527 | 66.6% | — |
| `GS_screen` | 15,742 | 11.7% | — |
| `ADMITTED` | 13,051 | 9.7% | **cleared every gate** |
| `G1_sanity` | 7,648 | 5.7% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,640 | 2.7% | parameter tuning overfit (high PBO) |
| `G0_eval` | 2,153 | 1.6% | did not produce a valid backtest |
| `G9_plateau` | 1,872 | 1.4% | — |
| `G2_oos` | 374 | 0.3% | shines in-sample, decays out-of-sample |
| `G8_orthogonality` | 290 | 0.2% | duplicates an existing archive member |
| `G5_robustness` | 199 | 0.1% | bootstrap tail drawdown too large |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 48367 | 4248 | 1.50 | ████████████████·· |
| `xau` | 37981 | 7079 | 0.83 | █████████········· |
| `fx` | 48148 | 1724 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 103245 | 6071 | 1.50 | ████████████████·· |
| `directional` | 31251 | 6980 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 114388 | 13032 | 1.50 | ████████████████·· |
| `llm` | 3969 | 11 | 1.35 | ███████████████··· |
| `template` | 3946 | 0 | 0.31 | ███··············· |
| `random` | 3768 | 0 | -0.67 | ·················· |
| `miner` | 8425 | 8 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 80745 | 4616 | 1.50 | ████████████████·· |
| `low_vol` | 37453 | 7309 | 0.83 | █████████········· |
| `chop` | 7545 | 925 | 0.22 | ██················ |
| `trend` | 4867 | 160 | 0.02 | ·················· |
| `high_vol` | 3886 | 41 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 104958 | 7379 | 1.50 | ████████████████·· |
| `kelly_fraction` | 845 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 26536 | 5662 | 0.76 | ████████·········· |
| `vol_target` | 1072 | 1 | -1.05 | ·················· |
| `atr_scaled` | 1085 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 18244 | 2454 | 1.50 | ████████████████·· |
| `liquidity` | 17833 | 2439 | 1.50 | ████████████████·· |
| `macro` | 19066 | 2155 | 1.38 | ███████████████··· |
| `regime` | 11362 | 1557 | 1.38 | ███████████████··· |
| `rates` | 7638 | 853 | 1.38 | ███████████████··· |
| `trend` | 17360 | 2484 | 0.86 | █████████········· |
| `momentum` | 16767 | 1955 | 0.86 | █████████········· |
| `auction_market_theory` | 14781 | 1743 | 0.85 | █████████········· |
| `market_profile` | 12068 | 1499 | 0.85 | █████████········· |
| `statistical` | 22840 | 5538 | 0.83 | █████████········· |
| `pattern` | 8061 | 1776 | 0.83 | █████████········· |
| `breakout` | 7969 | 1776 | 0.83 | █████████········· |
| `volatility` | 18997 | 4495 | 0.76 | ████████·········· |
| `mean_reversion` | 15851 | 4782 | 0.76 | ████████·········· |
| `ict` | 5996 | 1490 | 0.75 | ████████·········· |
| `smc` | 5996 | 1490 | 0.75 | ████████·········· |
| `positioning` | 14251 | 1651 | 0.60 | ███████··········· |
| `ml_derived` | 8426 | 1277 | 0.60 | ███████··········· |
| `order_flow` | 1181 | 144 | 0.55 | ██████············ |
| `cross_asset` | 1022 | 176 | 0.53 | ██████············ |
| `intermarket` | 972 | 176 | 0.53 | ██████············ |
| `oscillator` | 3163 | 152 | 0.40 | ████·············· |
| `event` | 2253 | 204 | 0.12 | █················· |
| `volume` | 3407 | 308 | 0.03 | ·················· |
| `mixed` | 60849 | 1231 | -0.11 | ·················· |
| `volume_profile` | 997 | 96 | -0.16 | ·················· |
| `crypto` | 1970 | 234 | -0.30 | ·················· |
| `funding` | 1970 | 234 | -0.30 | ·················· |
| `persistence` | 886 | 24 | -0.51 | ·················· |
| `calendar` | 10 | 0 | -1.69 | ·················· |
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
| `intx_911ab9c3` | 2 | +6.511 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_62a4f5a8` | 2 | +5.872 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_9a54d399` | 2 | +4.831 | **carries signal** |
| `intx_08644014` | 36 | +3.344 | **carries signal** |
| `intx_96edab0f` | 7 | +2.453 | **carries signal** |
| `intx_72d5925f` | 2 | +2.390 | **carries signal** |

---

## 5 · Archive (65 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.857 |
| `xau:scalp:trade:long:low_vol` | xau | 1.543 |
| `xau:swing:trade:long:low_vol` | xau | 1.215 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
| `fx:position:low:long:all` | fx | 0.750 |
| `fx:position:med:long:all` | fx | 0.748 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `crypto:position:high:neutral:all` | crypto | 0.641 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:intraday:med:neutral:chop` | fx | 0.525 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.505 |
| `xau:intraday:low:neutral:all` | xau | 0.496 |
| `fx:position:low:neutral:all` | fx | 0.494 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `crypto:position:high:neutral:chop` | crypto | 0.475 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `fx:position:med:neutral:all` | fx | 0.429 |
| `crypto:position:low:neutral:all` | crypto | 0.427 |

## 6 · Lessons library (120,162)

- ×16 — [PASS] breakout+interaction+intx_011edeee+intx_0507d207+intx_05645eba+intx_06f14519+intx_12692236+intx_2f8a0ced+intx_
- ×14 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×14 — [PASS] breakout+interaction+intx_011edeee+intx_0507d207+intx_06f14519+intx_12692236+intx_2f8a0ced+intx_2f8a5346+intx_
- ×7 — [PASS] breakout+interaction+intx_07b6ad25+intx_0f5c18ca+intx_346a0f82+intx_3d05d214+intx_e927eded+mined+pattern+slope
- ×6 — [PASS] volatility on a directional book promoted to the candidate pool
- ×6 — [GS_screen] interaction+intx_006ec67c+intx_10e814d4+intx_5433bf83+intx_c9f52768+mined+poc_distance_real+tsmom_blend (cross
- ×6 — [PASS] breakout+interaction+intx_011edeee+intx_0507d207+intx_12692236+intx_2f5a1871+intx_405ab659+intx_5fdddd9f+intx_
- ×5 — [GS_screen] cumulative_delta+interaction+intx_0129b3f9+intx_0d1f9748+intx_10e814d4+intx_14305a58+intx_2d2c770d+intx_3d05d2
- ×5 — [PASS] breakout+interaction+intx_011edeee+intx_0507d207+intx_06f14519+intx_12692236+intx_26f3586d+intx_2f8a0ced+intx_
- ×4 — [GS_screen] interaction+intx_10e814d4+intx_8b9d71b3+intx_dd595c5b+mined+poc_distance_real (cross_sectional) — raw predicti
- ×4 — [PASS] adx+candlestick_pattern+ict+interaction+intx_0507d207+intx_3086ff7a+intx_382083bf+intx_753ea6e7+intx_8e0d4062+
- ×4 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical+volatilit
- ×3 — [GS_screen] interaction+intx_10e814d4+intx_13e60945+intx_19456efa+intx_3d05d214+intx_8d20bcb1+intx_8eae474d+intx_92873c43+
- ×3 — [GS_screen] interaction+intx_14539bcd+intx_405ab659+mined (cross_sectional) — raw predictive strength too weak to clear th
- ×3 — [G3_cpcv_pbo] adx+candlestick_pattern+interaction+intx_0507d207+intx_382083bf+mean_reversion+mined+statistical (directional)

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*