# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-30 04:03 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **25,872** |
| Deflated-Sharpe trial count (raw N) | **47,472** *(evals 25,872 + 21,600 screened)* |
| **Effective** independent trials (N_eff) | **37,608** *(ρ̄=0.03527929442166004 — the bar the DSR actually uses)* |
| Admitted to archive | **1742** |
| Rejected | **24,130** (93.3%) |
| Distinct families explored | **31** |
| Lessons accumulated | **10,735** |
| Best DSR-z | **+1.568** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `6e827e1824cd5c23` | crypto | **1.57** | 0.6035 | 4.26 | 0.036 | cross_sectional | all | `G3_cpcv_pbo` |
| 2 | `f9b357250744cb4d` | crypto | **1.50** | 0.5998 | 4.23 | 0.031 | cross_sectional | all | `G3_cpcv_pbo` |
| 3 | `75ff10bcaaa26e9e` | crypto | **1.47** | 0.5688 | 4.01 | 0.055 | cross_sectional | all | `G9_plateau` |
| 4 | `97cb163c7403b95a` | crypto | **1.46** | 0.5634 | 3.97 | 0.036 | cross_sectional | all | `G3_cpcv_pbo` |
| 5 | `db1116ef1b1daa2e` | crypto | **1.45** | 0.8313 | 5.61 | 0.034 | cross_sectional | all | `ADMITTED` |
| 6 | `f91ac9df4c92294d` | crypto | **1.44** | 0.8360 | 5.65 | 0.033 | cross_sectional | all | `ADMITTED` |
| 7 | `791009c7f085c6aa` | crypto | **1.43** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 8 | `6d03423485a0e4a7` | crypto | **1.43** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 9 | `c7f59950aa197236` | crypto | **1.42** | 0.8318 | 5.62 | 0.033 | cross_sectional | all | `ADMITTED` |
| 10 | `7e6ad3c6df7a9643` | crypto | **1.42** | 0.5725 | 4.04 | 0.037 | cross_sectional | all | `G3_cpcv_pbo` |
| 11 | `e2932cabac0a7ae1` | crypto | **1.41** | 0.8367 | 5.65 | 0.032 | cross_sectional | all | `ADMITTED` |
| 12 | `726f5f4697c4db1c` | crypto | **1.41** | 0.8314 | 5.62 | 0.034 | cross_sectional | all | `ADMITTED` |
| 13 | `a7ff27f45f42bd85` | crypto | **1.40** | 0.5978 | 4.22 | 0.051 | cross_sectional | all | `G3_cpcv_pbo` |
| 14 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 15 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 16 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 17 | `cd01243357770202` | crypto | **1.29** | 0.8015 | 5.41 | 0.043 | cross_sectional | all | `ADMITTED` |
| 18 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `ec58e5f691d88894` | crypto | **1.20** | 0.7262 | 4.91 | 0.059 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |

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
**#3 · `75ff10bcaaa26e9e` — DSR-z 1.47 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=75ff10bcaaa26e9e  gen=14  by=evo_mutate  nodes=5
```
**#4 · `97cb163c7403b95a` — DSR-z 1.46 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=29)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=97cb163c7403b95a  gen=21  by=evo_mutate  nodes=4
```
**#5 · `db1116ef1b1daa2e` — DSR-z 1.45 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.009601909168493)
  id=db1116ef1b1daa2e  gen=41  by=evo_mutate  nodes=4
```
**#6 · `f91ac9df4c92294d` — DSR-z 1.44 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0491530175959747)
  id=f91ac9df4c92294d  gen=56  by=evo_mutate  nodes=4
```
**#7 · `791009c7f085c6aa` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=791009c7f085c6aa  gen=59  by=evo_crossover  nodes=4
```
**#8 · `6d03423485a0e4a7` — DSR-z 1.43 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=6d03423485a0e4a7  gen=44  by=evo_crossover  nodes=4
```
**#9 · `c7f59950aa197236` — DSR-z 1.42 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.3153903380020915)
  id=c7f59950aa197236  gen=61  by=evo_mutate  nodes=4
```
**#10 · `7e6ad3c6df7a9643` — DSR-z 1.42 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); amihud_illiquidity(window=32)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=7e6ad3c6df7a9643  gen=21  by=evo_mutate  nodes=5
```
**#11 · `e2932cabac0a7ae1` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.4917968356069782, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=e2932cabac0a7ae1  gen=55  by=evo_mutate  nodes=4
```
**#12 · `726f5f4697c4db1c` — DSR-z 1.41 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.582012, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=726f5f4697c4db1c  gen=74  by=evo_crossover  nodes=4
```
**#13 · `a7ff27f45f42bd85` — DSR-z 1.40 · died at `G3_cpcv_pbo` · families: liquidity, macro, microstructure, positioning**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); cot_zscore(window=27)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=a7ff27f45f42bd85  gen=20  by=llm_critic  nodes=5
```
**#14 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#15 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#16 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#17 · `cd01243357770202` — DSR-z 1.29 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.987931652984258, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=cd01243357770202  gen=79  by=evo_mutate  nodes=4
```
**#18 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#19 · `ec58e5f691d88894` — DSR-z 1.20 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=ec58e5f691d88894  gen=25  by=evo_mutate  nodes=4
```
**#20 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `GS_screen` | 15,738 | 60.8% | — |
| `G1_sanity` | 4,618 | 17.8% | degenerate / too few periods, or one period dominates P&L |
| `ADMITTED` | 1,742 | 6.7% | **cleared every gate** |
| `G3_cpcv_pbo` | 1,515 | 5.9% | parameter tuning overfit (high PBO) |
| `G0_eval` | 1,370 | 5.3% | did not produce a valid backtest |
| `—` | 287 | 1.1% | — |
| `G9_plateau` | 252 | 1.0% | — |
| `G8_orthogonality` | 197 | 0.8% | duplicates an existing archive member |
| `G5_robustness` | 151 | 0.6% | bootstrap tail drawdown too large |
| `G2_oos` | 2 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 9068 | 452 | 1.57 | █████████████████· |
| `xau` | 8311 | 923 | 0.98 | ███████████······· |
| `fx` | 8493 | 367 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 20705 | 829 | 1.57 | █████████████████· |
| `directional` | 5167 | 913 | 0.43 | █████············· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 20014 | 1721 | 1.57 | █████████████████· |
| `llm` | 1164 | 17 | 1.40 | ███████████████··· |
| `template` | 590 | 0 | 0.31 | ███··············· |
| `miner` | 3407 | 4 | -0.24 | ·················· |
| `random` | 697 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 11736 | 587 | 1.57 | █████████████████· |
| `low_vol` | 8827 | 1083 | 0.98 | ███████████······· |
| `trend` | 825 | 62 | 0.47 | █████············· |
| `chop` | 1694 | 1 | 0.22 | ██················ |
| `high_vol` | 2790 | 9 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 21800 | 1447 | 1.57 | █████████████████· |
| `kelly_fraction` | 1004 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 2279 | 282 | 0.43 | █████············· |
| `vol_target` | 664 | 3 | -1.05 | ·················· |
| `atr_scaled` | 125 | 0 | -2.19 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 3291 | 445 | 1.57 | █████████████████· |
| `liquidity` | 2952 | 444 | 1.57 | █████████████████· |
| `macro` | 6476 | 519 | 1.47 | ████████████████·· |
| `rates` | 2351 | 119 | 1.47 | ████████████████·· |
| `regime` | 2203 | 103 | 1.47 | ████████████████·· |
| `positioning` | 4439 | 460 | 1.40 | ███████████████··· |
| `statistical` | 5821 | 561 | 0.98 | ███████████······· |
| `pattern` | 1195 | 58 | 0.98 | ███████████······· |
| `breakout` | 1083 | 58 | 0.98 | ███████████······· |
| `momentum` | 5952 | 479 | 0.86 | █████████········· |
| `trend` | 4628 | 300 | 0.86 | █████████········· |
| `auction_market_theory` | 3854 | 267 | 0.85 | █████████········· |
| `market_profile` | 1712 | 120 | 0.85 | █████████········· |
| `ict` | 3906 | 265 | 0.63 | ███████··········· |
| `smc` | 3906 | 265 | 0.63 | ███████··········· |
| `order_flow` | 1067 | 69 | 0.55 | ██████············ |
| `cross_asset` | 943 | 49 | 0.53 | ██████············ |
| `intermarket` | 930 | 49 | 0.53 | ██████············ |
| `oscillator` | 3360 | 181 | 0.47 | █████············· |
| `volume` | 1826 | 153 | 0.47 | █████············· |
| `mean_reversion` | 1806 | 301 | 0.46 | █████············· |
| `volatility` | 3959 | 338 | 0.31 | ███··············· |
| `event` | 907 | 73 | 0.12 | █················· |
| `mixed` | 2484 | 173 | -0.11 | ·················· |
| `volume_profile` | 989 | 135 | -0.20 | ·················· |
| `persistence` | 1263 | 20 | -0.51 | ·················· |
| `ml_derived` | 887 | 67 | -0.54 | ·················· |
| `crypto` | 362 | 40 | -0.54 | ·················· |
| `funding` | 362 | 40 | -0.54 | ·················· |
| `calendar` | 40 | 0 | -1.69 | ·················· |
| `sentiment` | 22 | 0 | -2.95 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `liquidity_sweep` | 1869 | +2.035 | **carries signal** |
| `fed_policy_bias` | 936 | +1.894 | **carries signal** |
| `fed_repricing` | 549 | +1.815 | **carries signal** |
| `amihud_illiquidity` | 2108 | +1.566 | **carries signal** |
| `variance_ratio` | 95 | +1.305 | **carries signal** |
| `tsmom_blend` | 208 | +1.095 | **carries signal** |
| `vol_regime_tag` | 695 | +1.060 | **carries signal** |
| `momentum` | 1959 | +1.050 | **carries signal** |
| `rel_strength` | 584 | +0.931 | **carries signal** |
| `intx_c441a7af` | 290 | +0.841 | **carries signal** |
| `intx_cfbc8793` | 72 | +0.649 | **carries signal** |
| `intx_b8f9f9ec` | 2 | +0.640 | **carries signal** |
| `atr_expansion` | 1206 | +0.627 | **carries signal** |
| `adx` | 735 | +0.498 | **carries signal** |
| `intx_a7876d13` | 275 | +0.464 | **carries signal** |

---

## 5 · Archive (27 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.055 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:position:low:long:low_vol` | fx | 0.600 |
| `xau:intraday:low:long:low_vol` | xau | 0.554 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:low_vol` | fx | 0.476 |
| `xau:intraday:trade:long:trend` | xau | 0.448 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.402 |
| `crypto:position:med:neutral:all` | crypto | 0.380 |
| `fx:position:low:long:all` | fx | 0.311 |
| `crypto:position:med:neutral:chop` | crypto | 0.282 |
| `fx:swing:med:long:low_vol` | fx | 0.247 |
| `fx:swing:med:long:all` | fx | 0.247 |
| `fx:swing:low:long:all` | fx | 0.205 |
| `xau:intraday:low:neutral:trend` | xau | 0.135 |
| `xau:intraday:low:long:all` | xau | 0.065 |
| `crypto:intraday:low:neutral:all` | crypto | -0.013 |
| `xau:intraday:trade:long:high_vol` | xau | -0.022 |
| `crypto:intraday:med:neutral:all` | crypto | -0.032 |
| `crypto:swing:med:neutral:all` | crypto | -0.035 |
| `crypto:swing:low:neutral:all` | crypto | -0.068 |

## 6 · Lessons library (10,735)

- ×15 — [PASS] auction_market_theory+crypto+event+funding+ict+interaction+intx_8e0d4062+liquidity+macro+market_profile+micros
- ×10 — [PASS] interaction+intx_6ff832ad+intx_a99b3c1a+intx_c1240e5f+intx_e4425d6a+macro+mined+positioning+statistical on a c
- ×10 — [PASS] volatility on a directional book promoted to the candidate pool
- ×8 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×7 — [PASS] adx+candlestick_pattern+interaction+mined on a directional book promoted to the candidate pool
- ×7 — [PASS] liquidity+microstructure on a cross_sectional book promoted to the candidate pool
- ×6 — [PASS] interaction+liquidity_sweep+mean_reversion+mined+order_block_strength+statistical on a directional book promot
- ×6 — [PASS] adx+candlestick_pattern+interaction+liquidity_sweep+mined+order_block_strength on a directional book promoted 
- ×6 — [PASS] adx+candlestick_pattern+interaction+liquidity_sweep+mean_reversion+mined+order_block_strength+statistical on a
- ×5 — [PASS] ict+liquidity+microstructure+momentum+smc on a cross_sectional book promoted to the candidate pool
- ×4 — [GS_screen] macro+positioning (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_single=0.009
- ×4 — [GS_screen] interaction+intx_6ff832ad+intx_a99b3c1a+macro+mined+momentum+oscillator+positioning (cross_sectional) — raw pr
- ×4 — [PASS] interaction+intx_6ff832ad+intx_a99b3c1a+intx_c1240e5f+intx_e4425d6a+macro+mined+positioning on a cross_section
- ×4 — [GS_screen] macro+ml_derived+rates+regime (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_
- ×4 — [GS_screen] interaction+intx_6ff832ad+intx_a99b3c1a+intx_c1240e5f+intx_e4425d6a+macro+mined+positioning+statistical (cross

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*