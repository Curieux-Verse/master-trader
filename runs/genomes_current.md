# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-31 14:18 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **74,658** |
| Deflated-Sharpe trial count (raw N) | **144,960** *(evals 74,658 + 70,302 screened)* |
| **Effective** independent trials (N_eff) | **102,955** *(ρ̄=0.05320192562682754 — the bar the DSR actually uses)* |
| Admitted to archive | **8089** |
| Rejected | **66,569** (89.2%) |
| Distinct families explored | **31** |
| Lessons accumulated | **36,661** |
| Best DSR-z | **+1.568** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `6e827e1824cd5c23` | crypto | **1.57** | 0.6035 | 4.26 | 0.036 | cross_sectional | all | `G3_cpcv_pbo` |
| 2 | `f9b357250744cb4d` | crypto | **1.50** | 0.5998 | 4.23 | 0.031 | cross_sectional | all | `G3_cpcv_pbo` |
| 3 | `97cb163c7403b95a` | crypto | **1.46** | 0.5634 | 3.97 | 0.036 | cross_sectional | all | `G3_cpcv_pbo` |
| 4 | `db1116ef1b1daa2e` | crypto | **1.45** | 0.8313 | 5.61 | 0.034 | cross_sectional | all | `ADMITTED` |
| 5 | `f91ac9df4c92294d` | crypto | **1.44** | 0.8360 | 5.65 | 0.033 | cross_sectional | all | `ADMITTED` |
| 6 | `791009c7f085c6aa` | crypto | **1.43** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 7 | `6d03423485a0e4a7` | crypto | **1.43** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 8 | `c7f59950aa197236` | crypto | **1.42** | 0.8318 | 5.62 | 0.033 | cross_sectional | all | `ADMITTED` |
| 9 | `7e6ad3c6df7a9643` | crypto | **1.42** | 0.5725 | 4.04 | 0.037 | cross_sectional | all | `G3_cpcv_pbo` |
| 10 | `e2932cabac0a7ae1` | crypto | **1.41** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 11 | `726f5f4697c4db1c` | crypto | **1.41** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 12 | `a7ff27f45f42bd85` | crypto | **1.40** | 0.5978 | 4.22 | 0.051 | cross_sectional | all | `G3_cpcv_pbo` |
| 13 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 14 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 15 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 16 | `cd01243357770202` | crypto | **1.29** | 0.8015 | 5.41 | 0.043 | cross_sectional | all | `ADMITTED` |
| 17 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 18 | `ec58e5f691d88894` | crypto | **1.20** | 0.7262 | 4.91 | 0.059 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `64eed38552709d9a` | crypto | **1.16** | 0.7519 | 5.08 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `6e827e1824cd5c23` — DSR-z 1.57 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=6e827e1824cd5c23  gen=12  by=evo_crossover  nodes=4
```
**#2 · `f9b357250744cb4d` — DSR-z 1.50 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.3522641431182003, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=f9b357250744cb4d  gen=30  by=evo_mutate  nodes=4
```
**#3 · `97cb163c7403b95a` — DSR-z 1.46 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=29)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=97cb163c7403b95a  gen=21  by=evo_mutate  nodes=4
```
**#4 · `db1116ef1b1daa2e` — DSR-z 1.45 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.009601909168493)
  id=db1116ef1b1daa2e  gen=41  by=evo_mutate  nodes=4
```
**#5 · `f91ac9df4c92294d` — DSR-z 1.44 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0491530175959747)
  id=f91ac9df4c92294d  gen=56  by=evo_mutate  nodes=4
```
**#6 · `791009c7f085c6aa` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=791009c7f085c6aa  gen=59  by=evo_crossover  nodes=4
```
**#7 · `6d03423485a0e4a7` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=6d03423485a0e4a7  gen=44  by=evo_crossover  nodes=4
```
**#8 · `c7f59950aa197236` — DSR-z 1.42 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.3153903380020915)
  id=c7f59950aa197236  gen=61  by=evo_mutate  nodes=4
```
**#9 · `7e6ad3c6df7a9643` — DSR-z 1.42 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); amihud_illiquidity(window=32)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=7e6ad3c6df7a9643  gen=21  by=evo_mutate  nodes=5
```
**#10 · `e2932cabac0a7ae1` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=e2932cabac0a7ae1  gen=55  by=evo_mutate  nodes=4
```
**#11 · `726f5f4697c4db1c` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=726f5f4697c4db1c  gen=74  by=evo_crossover  nodes=4
```
**#12 · `a7ff27f45f42bd85` — DSR-z 1.40 · died at `G3_cpcv_pbo` · families: liquidity, macro, microstructure, positioning**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); cot_zscore(window=27)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=a7ff27f45f42bd85  gen=20  by=llm_critic  nodes=5
```
**#13 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#14 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#15 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#16 · `cd01243357770202` — DSR-z 1.29 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.987931652984258, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=cd01243357770202  gen=79  by=evo_mutate  nodes=4
```
**#17 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#18 · `ec58e5f691d88894` — DSR-z 1.20 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=ec58e5f691d88894  gen=25  by=evo_mutate  nodes=4
```
**#19 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
**#20 · `64eed38552709d9a` — DSR-z 1.16 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.4384386928813)
  id=64eed38552709d9a  gen=36  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `—` | 38,779 | 51.9% | — |
| `GS_screen` | 15,811 | 21.2% | — |
| `ADMITTED` | 8,089 | 10.8% | **cleared every gate** |
| `G1_sanity` | 5,486 | 7.3% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 4,242 | 5.7% | parameter tuning overfit (high PBO) |
| `G0_eval` | 1,318 | 1.8% | did not produce a valid backtest |
| `G9_plateau` | 510 | 0.7% | — |
| `G8_orthogonality` | 297 | 0.4% | duplicates an existing archive member |
| `G5_robustness` | 112 | 0.2% | bootstrap tail drawdown too large |
| `G2_oos` | 14 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 25337 | 3136 | 1.57 | █████████████████· |
| `xau` | 24340 | 3615 | 0.83 | █████████········· |
| `fx` | 24981 | 1338 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 57393 | 4590 | 1.57 | █████████████████· |
| `directional` | 17265 | 3499 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 62082 | 8073 | 1.57 | █████████████████· |
| `llm` | 2750 | 11 | 1.40 | ███████████████··· |
| `template` | 1692 | 0 | 0.31 | ███··············· |
| `miner` | 5916 | 5 | -0.24 | ·················· |
| `random` | 2218 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 36028 | 3981 | 1.57 | █████████████████· |
| `low_vol` | 22848 | 3574 | 0.83 | █████████········· |
| `chop` | 4329 | 8 | 0.22 | ██················ |
| `trend` | 4601 | 426 | 0.02 | ·················· |
| `high_vol` | 6852 | 100 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 59907 | 5532 | 1.57 | █████████████████· |
| `kelly_fraction` | 1369 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 11871 | 2546 | 0.76 | ████████·········· |
| `vol_target` | 1082 | 1 | -1.05 | ·················· |
| `atr_scaled` | 429 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 12974 | 2992 | 1.57 | █████████████████· |
| `liquidity` | 12363 | 2973 | 1.57 | █████████████████· |
| `macro` | 16926 | 2450 | 1.40 | ███████████████··· |
| `positioning` | 11462 | 1727 | 1.40 | ███████████████··· |
| `regime` | 7837 | 1913 | 1.38 | ███████████████··· |
| `rates` | 6366 | 1026 | 1.38 | ███████████████··· |
| `momentum` | 14013 | 2557 | 0.86 | █████████········· |
| `trend` | 12130 | 2042 | 0.86 | █████████········· |
| `auction_market_theory` | 11890 | 2206 | 0.85 | █████████········· |
| `market_profile` | 7771 | 1934 | 0.85 | █████████········· |
| `statistical` | 15947 | 2765 | 0.83 | █████████········· |
| `pattern` | 2403 | 115 | 0.83 | █████████········· |
| `breakout` | 2246 | 115 | 0.83 | █████████········· |
| `volatility` | 10114 | 1809 | 0.76 | ████████·········· |
| `mean_reversion` | 7601 | 2014 | 0.76 | ████████·········· |
| `ict` | 7328 | 822 | 0.75 | ████████·········· |
| `smc` | 7328 | 822 | 0.75 | ████████·········· |
| `ml_derived` | 4447 | 1570 | 0.60 | ███████··········· |
| `order_flow` | 2339 | 237 | 0.55 | ██████············ |
| `cross_asset` | 1559 | 187 | 0.53 | ██████············ |
| `intermarket` | 1541 | 187 | 0.53 | ██████············ |
| `oscillator` | 5336 | 227 | 0.40 | ████·············· |
| `event` | 2298 | 379 | 0.12 | █················· |
| `volume` | 3504 | 233 | 0.03 | ·················· |
| `mixed` | 16436 | 817 | -0.11 | ·················· |
| `volume_profile` | 1939 | 116 | -0.16 | ·················· |
| `crypto` | 1194 | 296 | -0.30 | ·················· |
| `funding` | 1194 | 296 | -0.30 | ·················· |
| `persistence` | 1801 | 31 | -0.51 | ·················· |
| `calendar` | 47 | 0 | -1.69 | ·················· |
| `sentiment` | 27 | 0 | -17.94 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_d77b40a2` | 2 | +4.885 | **carries signal** |
| `intx_9c85e9c3` | 110 | +2.603 | **carries signal** |
| `intx_d7fd686a` | 84 | +2.247 | **carries signal** |
| `intx_ca25f3f2` | 70 | +1.686 | **carries signal** |
| `amihud_illiquidity` | 14593 | +1.444 | **carries signal** |
| `intx_9c77b83f` | 134 | +1.288 | **carries signal** |
| `intx_2f8a5346` | 3 | +1.208 | **carries signal** |
| `intx_405ab659` | 11 | +1.162 | **carries signal** |
| `intx_40fdcf76` | 913 | +1.073 | **carries signal** |
| `intx_efbc5645` | 4702 | +1.068 | **carries signal** |
| `vol_regime_tag` | 5846 | +1.044 | **carries signal** |
| `fed_policy_bias` | 4781 | +1.017 | **carries signal** |
| `intx_49fa7f67` | 546 | +1.015 | **carries signal** |

---

## 5 · Archive (47 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.530 |
| `xau:swing:trade:long:low_vol` | xau | 1.138 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:position:low:long:all` | fx | 0.602 |
| `xau:intraday:trade:long:trend` | xau | 0.584 |
| `fx:position:med:long:all` | fx | 0.555 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.427 |
| `xau:intraday:low:neutral:all` | xau | 0.404 |
| `xau:intraday:low:long:trend` | xau | 0.389 |
| `xau:intraday:trade:long:high_vol` | xau | 0.361 |
| `crypto:position:med:neutral:chop` | crypto | 0.356 |
| `fx:position:low:long:high_vol` | fx | 0.345 |
| `crypto:position:high:neutral:all` | crypto | 0.342 |
| `xau:swing:low:long:trend` | xau | 0.333 |

## 6 · Lessons library (36,661)

- ×19 — [PASS] auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_a16b7695+intx_ab31bc67+liquidity+market_pro
- ×14 — [PASS] interaction+intx_0507d207+intx_3086ff7a+intx_382083bf+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion
- ×7 — [PASS] cross_asset+crypto+funding+interaction+intermarket+intx_a16b7695+intx_ab31bc67+intx_ca069136+liquidity+microst
- ×6 — [PASS] adx+candlestick_pattern+interaction+mined on a directional book promoted to the candidate pool
- ×6 — [PASS] amihud_illiquidity+consolidation_score+cross_asset+crypto+funding+interaction+intermarket+intx_5a1e9077+intx_6
- ×6 — [PASS] hurst+interaction+intx_137ddd7b+intx_421762f1+intx_a16b7695+intx_ab31bc67+liquidity+microstructure+mined+rotat
- ×6 — [G3_cpcv_pbo] amihud_illiquidity+consolidation_score+cross_asset+crypto+funding+interaction+intermarket+intx_5a1e9077+intx_a
- ×5 — [GS_screen] interaction+intx_39165f4d+intx_4f97afa7+intx_58001d43+intx_6a4a9e33+macro+mined+positioning+statistical (cross
- ×4 — [G1_sanity] interaction+intx_315232f3+intx_7f80f9ab+mined (cross_sectional) — degenerate P&L — too few trades, or one bar 
- ×4 — [PASS] auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_a16b7695+intx_ab31bc67+market_profile+mined
- ×4 — [G3_cpcv_pbo] amihud_illiquidity+consolidation_score+cross_asset+crypto+funding+interaction+intermarket+intx_5a1e9077+intx_6
- ×3 — [PASS] auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+liquidity+market_profile+microstructure+mined+ml
- ×3 — [G3_cpcv_pbo] cross_asset+crypto+funding+interaction+intermarket+intx_a16b7695+intx_ab31bc67+intx_ca069136+liquidity+microst
- ×3 — [GS_screen] interaction+intx_10e814d4+intx_39165f4d+intx_495677d1+intx_4f97afa7+intx_6ff832ad+intx_a99b3c1a+intx_d18f920f+
- ×3 — [GS_screen] auction_market_theory+volume_profile (cross_sectional) — raw predictive strength too weak to clear the FDR scr

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*