# 🧬 Master Trader — Genome Population Report

*Generated 2026-09-09 21:23 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **136,107** |
| Deflated-Sharpe trial count (raw N) | **455,825** *(evals 136,107 + 319,718 screened)* |
| **Effective** independent trials (N_eff) | **465,551** *(ρ̄=0.022052888449313825 — the bar the DSR actually uses)* |
| Admitted to archive | **12019** |
| Rejected | **124,088** (91.2%) |
| Distinct families explored | **31** |
| Lessons accumulated | **147,958** |
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
| `—` | 88,071 | 64.7% | — |
| `GS_screen` | 18,671 | 13.7% | — |
| `ADMITTED` | 12,019 | 8.8% | **cleared every gate** |
| `G1_sanity` | 8,397 | 6.2% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 3,394 | 2.5% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 3,356 | 2.5% | parameter tuning overfit (high PBO) |
| `G9_plateau` | 1,595 | 1.2% | — |
| `G8_orthogonality` | 299 | 0.2% | duplicates an existing archive member |
| `G5_robustness` | 289 | 0.2% | bootstrap tail drawdown too large |
| `G2_oos` | 16 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 49239 | 3317 | 1.50 | ████████████████·· |
| `xau` | 37478 | 6995 | 0.83 | █████████········· |
| `fx` | 49390 | 1707 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 103699 | 5114 | 1.50 | ████████████████·· |
| `directional` | 32408 | 6905 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 108308 | 12000 | 1.50 | ████████████████·· |
| `llm` | 5553 | 12 | 1.35 | ███████████████··· |
| `template` | 4815 | 0 | 0.31 | ███··············· |
| `random` | 7320 | 3 | -0.67 | ·················· |
| `miner` | 10111 | 4 | -1.00 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 71537 | 3995 | 1.50 | ████████████████·· |
| `low_vol` | 39442 | 7268 | 0.83 | █████████········· |
| `chop` | 13989 | 605 | 0.22 | ██················ |
| `trend` | 5581 | 114 | 0.02 | ·················· |
| `high_vol` | 5558 | 37 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 101896 | 6340 | 1.50 | ████████████████·· |
| `kelly_fraction` | 2019 | 9 | 0.85 | █████████········· |
| `fixed_fractional` | 27049 | 5664 | 0.76 | ████████·········· |
| `vol_target` | 3139 | 2 | -1.05 | ·················· |
| `atr_scaled` | 2004 | 4 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 10267 | 2328 | 1.50 | ████████████████·· |
| `liquidity` | 9847 | 2319 | 1.50 | ████████████████·· |
| `macro` | 18389 | 2218 | 1.38 | ███████████████··· |
| `regime` | 5849 | 1473 | 1.38 | ███████████████··· |
| `rates` | 3801 | 783 | 1.38 | ███████████████··· |
| `trend` | 15221 | 2003 | 0.86 | █████████········· |
| `momentum` | 11344 | 1901 | 0.86 | █████████········· |
| `auction_market_theory` | 8116 | 1628 | 0.85 | █████████········· |
| `market_profile` | 5902 | 1413 | 0.85 | █████████········· |
| `statistical` | 22167 | 5357 | 0.83 | █████████········· |
| `pattern` | 13106 | 1020 | 0.83 | █████████········· |
| `breakout` | 13058 | 1020 | 0.83 | █████████········· |
| `volatility` | 16929 | 4176 | 0.76 | ████████·········· |
| `mean_reversion` | 15381 | 4642 | 0.76 | ████████·········· |
| `ict` | 4650 | 1334 | 0.75 | ████████·········· |
| `smc` | 4650 | 1334 | 0.75 | ████████·········· |
| `positioning` | 16045 | 1741 | 0.60 | ███████··········· |
| `ml_derived` | 4417 | 1198 | 0.60 | ███████··········· |
| `order_flow` | 1082 | 123 | 0.55 | ██████············ |
| `cross_asset` | 549 | 169 | 0.53 | ██████············ |
| `intermarket` | 511 | 169 | 0.53 | ██████············ |
| `oscillator` | 4303 | 186 | 0.40 | ████·············· |
| `event` | 1069 | 183 | 0.12 | █················· |
| `volume` | 3038 | 254 | 0.03 | ·················· |
| `mixed` | 64296 | 1274 | -0.11 | ·················· |
| `volume_profile` | 900 | 94 | -0.16 | ·················· |
| `crypto` | 1156 | 221 | -0.30 | ·················· |
| `funding` | 1156 | 221 | -0.30 | ·················· |
| `persistence` | 886 | 22 | -0.51 | ·················· |
| `calendar` | 13 | 0 | -1.69 | ·················· |
| `sentiment` | 5 | 0 | -20.43 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_2151a43e` | 2 | +19.283 | **carries signal** |
| `intx_d14535c7` | 3 | +18.201 | **carries signal** |
| `intx_57d53023` | 6 | +14.083 | **carries signal** |
| `intx_755a0a56` | 10 | +13.446 | **carries signal** |
| `intx_7cd0e389` | 2 | +12.957 | **carries signal** |
| `intx_39ebaed9` | 2 | +10.526 | **carries signal** |
| `intx_ca1f399c` | 2 | +10.157 | **carries signal** |
| `intx_a78bb443` | 7 | +9.211 | **carries signal** |
| `intx_d5f8dbe2` | 53 | +9.168 | **carries signal** |
| `intx_c9d46590` | 2 | +8.570 | **carries signal** |
| `intx_d77b40a2` | 3 | +8.415 | **carries signal** |
| `intx_d89087f9` | 31 | +8.352 | **carries signal** |
| `intx_3817217e` | 56 | +8.229 | **carries signal** |
| `intx_7ba96055` | 47 | +8.151 | **carries signal** |
| `intx_4b752ddb` | 22 | +8.109 | **carries signal** |

---

## 5 · Archive (79 niches)

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

## 6 · Lessons library (147,958)

- ×7 — [GS_screen] har_vol+interaction+intx_04493e40+intx_25ed34c7+intx_2f41065c+intx_39165f4d+intx_392410bd+intx_40fdcf76+intx_4
- ×6 — [GS_screen] cumulative_delta+interaction+intx_0fe63907+intx_10e814d4+intx_25ed34c7+intx_3c6db177+intx_495677d1+intx_ab2edd
- ×6 — [PASS] volatility on a directional book promoted to the candidate pool
- ×5 — [GS_screen] adx+auction_market_theory+interaction+intx_a16b7695+intx_ab31bc67+intx_f27ad431+liquidity+market_profile+micro
- ×5 — [PASS] interaction+intx_3f64b63b+mined+sma_dist+volatility on a directional book promoted to the candidate pool
- ×5 — [GS_screen] interaction+intx_107a686b+intx_32b625ae+intx_7d20d966+intx_88a1813b+intx_981d69f8+intx_a140ca24+intx_b0c5b5aa+
- ×4 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical+volatilit
- ×4 — [GS_screen] breakout+delta_divergence+interaction+intx_011edeee+intx_0507d207+intx_12692236+intx_5fdddd9f+intx_64624138+in
- ×4 — [GS_screen] breakout+delta_divergence+interaction+intx_0507d207+intx_64624138+intx_895d3755+mined+pattern+trend (cross_sec
- ×4 — [PASS] adx+candlestick_pattern+ict+interaction+intx_0507d207+intx_3086ff7a+intx_382083bf+intx_753ea6e7+intx_8e0d4062+
- ×4 — [G1_sanity] breakout+interaction+intx_980b0e06+mined (cross_sectional) — degenerate P&L — too few trades, or one bar domin
- ×3 — [G3_cpcv_pbo] adx+candlestick_pattern+ict+interaction+intx_0507d207+intx_3086ff7a+intx_382083bf+intx_753ea6e7+intx_8e0d4062+
- ×3 — [GS_screen] interaction+intx_4807b2dc+intx_78328689+intx_a9134b07+intx_ed51d0d3+macro+mined+positioning+roc+rolling_kurt (
- ×3 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×3 — [GS_screen] liquidity+macro+microstructure+rates+regime (cross_sectional) — raw predictive strength too weak to clear the 

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*