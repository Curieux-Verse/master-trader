# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-30 14:10 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **48,713** |
| Deflated-Sharpe trial count (raw N) | **93,163** *(evals 48,713 + 44,450 screened)* |
| **Effective** independent trials (N_eff) | **64,878** *(ρ̄=0.04241820226163183 — the bar the DSR actually uses)* |
| Admitted to archive | **5430** |
| Rejected | **43,283** (88.9%) |
| Distinct families explored | **31** |
| Lessons accumulated | **23,250** |
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
| `GS_screen` | 16,837 | 34.6% | — |
| `—` | 16,632 | 34.1% | — |
| `ADMITTED` | 5,430 | 11.1% | **cleared every gate** |
| `G1_sanity` | 4,319 | 8.9% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,772 | 7.7% | parameter tuning overfit (high PBO) |
| `G0_eval` | 663 | 1.4% | did not produce a valid backtest |
| `G9_plateau` | 599 | 1.2% | — |
| `G8_orthogonality` | 297 | 0.6% | duplicates an existing archive member |
| `G5_robustness` | 147 | 0.3% | bootstrap tail drawdown too large |
| `G2_oos` | 17 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 17028 | 1729 | 1.57 | █████████████████· |
| `xau` | 16095 | 2561 | 0.83 | █████████········· |
| `fx` | 15590 | 1140 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 38202 | 3045 | 1.57 | █████████████████· |
| `directional` | 10511 | 2385 | 0.73 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 41442 | 5408 | 1.57 | █████████████████· |
| `llm` | 1166 | 15 | 1.40 | ███████████████··· |
| `template` | 607 | 0 | 0.31 | ███··············· |
| `miner` | 4736 | 7 | -0.24 | ·················· |
| `random` | 762 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 23027 | 2354 | 1.57 | █████████████████· |
| `low_vol` | 16268 | 2608 | 0.83 | █████████········· |
| `chop` | 2840 | 6 | 0.22 | ██················ |
| `trend` | 2570 | 421 | 0.02 | ·················· |
| `high_vol` | 4008 | 41 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 40504 | 3943 | 1.57 | █████████████████· |
| `kelly_fraction` | 1017 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 6379 | 1476 | 0.73 | ████████·········· |
| `vol_target` | 678 | 1 | -1.05 | ·················· |
| `atr_scaled` | 135 | 0 | -2.19 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 8313 | 1769 | 1.57 | █████████████████· |
| `liquidity` | 7833 | 1764 | 1.57 | █████████████████· |
| `macro` | 12494 | 1899 | 1.40 | ███████████████··· |
| `positioning` | 8207 | 1283 | 1.40 | ███████████████··· |
| `rates` | 4742 | 725 | 1.38 | ███████████████··· |
| `regime` | 4616 | 701 | 1.38 | ███████████████··· |
| `momentum` | 8436 | 933 | 0.86 | █████████········· |
| `trend` | 7499 | 842 | 0.86 | █████████········· |
| `auction_market_theory` | 7429 | 1066 | 0.85 | █████████········· |
| `market_profile` | 4161 | 775 | 0.85 | █████████········· |
| `statistical` | 11722 | 2001 | 0.83 | █████████········· |
| `pattern` | 1742 | 146 | 0.83 | █████████········· |
| `breakout` | 1604 | 146 | 0.83 | █████████········· |
| `volatility` | 6155 | 887 | 0.73 | ████████·········· |
| `mean_reversion` | 4828 | 1305 | 0.73 | ████████·········· |
| `ict` | 5742 | 616 | 0.63 | ███████··········· |
| `smc` | 5742 | 616 | 0.63 | ███████··········· |
| `order_flow` | 1726 | 198 | 0.55 | ██████············ |
| `cross_asset` | 1141 | 96 | 0.53 | ██████············ |
| `intermarket` | 1127 | 96 | 0.53 | ██████············ |
| `oscillator` | 4321 | 235 | 0.40 | ████·············· |
| `event` | 1377 | 160 | 0.12 | █················· |
| `volume` | 2660 | 201 | 0.03 | ·················· |
| `mixed` | 7721 | 585 | -0.11 | ·················· |
| `volume_profile` | 1418 | 133 | -0.16 | ·················· |
| `crypto` | 660 | 127 | -0.30 | ·················· |
| `funding` | 660 | 127 | -0.30 | ·················· |
| `ml_derived` | 1459 | 186 | -0.33 | ·················· |
| `persistence` | 1540 | 32 | -0.51 | ·················· |
| `calendar` | 40 | 0 | -1.69 | ·················· |
| `sentiment` | 22 | 0 | — | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `amihud_illiquidity` | 7731 | +1.581 | **carries signal** |
| `intx_2f8a5346` | 3 | +1.208 | **carries signal** |
| `intx_2fdc80a0` | 17 | +1.191 | **carries signal** |
| `intx_cbab1b3b` | 1222 | +1.190 | **carries signal** |
| `liquidity_sweep` | 3159 | +1.113 | **carries signal** |
| `intx_efbc5645` | 2027 | +1.108 | **carries signal** |
| `fed_policy_bias` | 3953 | +1.093 | **carries signal** |
| `intx_0228c153` | 11 | +1.080 | **carries signal** |
| `fed_repricing` | 961 | +0.930 | **carries signal** |
| `intx_05645eba` | 199 | +0.894 | **carries signal** |
| `intx_ecf2c12e` | 2051 | +0.888 | **carries signal** |
| `intx_e75bf6dc` | 1007 | +0.849 | **carries signal** |
| `intx_49fa7f67` | 44 | +0.844 | **carries signal** |
| `momentum` | 3549 | +0.739 | **carries signal** |

---

## 5 · Archive (44 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.530 |
| `xau:swing:trade:long:low_vol` | xau | 1.011 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:position:low:long:all` | fx | 0.602 |
| `fx:position:med:long:all` | fx | 0.555 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `crypto:position:med:neutral:all` | crypto | 0.482 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:trend` | xau | 0.448 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.417 |
| `xau:intraday:low:long:trend` | xau | 0.389 |
| `crypto:position:med:neutral:chop` | crypto | 0.356 |
| `fx:position:low:long:high_vol` | fx | 0.345 |
| `crypto:position:high:neutral:all` | crypto | 0.342 |
| `xau:swing:low:long:trend` | xau | 0.333 |
| `xau:intraday:low:neutral:chop` | xau | 0.332 |
| `xau:intraday:low:neutral:trend` | xau | 0.271 |
| `crypto:position:med:neutral:trend` | crypto | 0.247 |

## 6 · Lessons library (23,250)

- ×18 — [PASS] auction_market_theory+hurst+interaction+intx_a16b7695+intx_ab31bc67+intx_ca069136+liquidity+macro+market_profi
- ×12 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+liquidity_sweep+mean_reversion+mined+order_block_strength+statistical+
- ×10 — [PASS] adx+candlestick_pattern+interaction+intx_3086ff7a+intx_753ea6e7+intx_b4416742+intx_efbc5645+liquidity_sweep+me
- ×8 — [PASS] auction_market_theory+event+hurst+ict+interaction+intx_03db8e1d+intx_8777c77c+intx_8e0d4062+intx_95944cb1+intx
- ×5 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+mean_reversion+mined+statistical+volatility on a directional book prom
- ×5 — [GS_screen] cumulative_delta+interaction+intx_0fe63907+intx_39165f4d+intx_495677d1+intx_4f97afa7+intx_d18f920f+mined (cros
- ×5 — [PASS] hurst+interaction+intx_a16b7695+intx_ab31bc67+intx_ca069136+liquidity+macro+microstructure+mined+rates+regime+
- ×5 — [PASS] liquidity+microstructure on a cross_sectional book promoted to the candidate pool
- ×5 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical on a dire
- ×4 — [PASS] interaction+intx_080bbe39+intx_10e814d4+intx_e6144124+macro+mined+poc_distance_real+positioning on a cross_sec
- ×3 — [PASS] interaction+intx_3086ff7a+intx_6e4c2080+intx_753ea6e7+intx_df49cc32+liquidity_sweep+mean_reversion+mined+order
- ×3 — [GS_screen] amihud_illiquidity+interaction+intx_7045ff6b+mined (cross_sectional) — raw predictive strength too weak to cle
- ×3 — [PASS] hurst+interaction+intx_95666e08+intx_ca069136+intx_efbc5645+liquidity+macro+microstructure+mined+rates+regime+
- ×3 — [PASS] auction_market_theory+hurst+interaction+intx_a16b7695+intx_ab31bc67+liquidity+macro+market_profile+microstruct
- ×3 — [PASS] ema_dist+interaction+mined+momentum on a cross_sectional book promoted to the candidate pool

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*