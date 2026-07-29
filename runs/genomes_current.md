# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-29 21:02 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **12,466** |
| Deflated-Sharpe trial count (raw N) | **21,559** *(evals 12,466 + 9,093 screened)* |
| **Effective** independent trials (N_eff) | **15,898** *(ρ̄=0.02821564609867714 — the bar the DSR actually uses)* |
| Admitted to archive | **442** |
| Rejected | **12,024** (96.5%) |
| Distinct families explored | **31** |
| Lessons accumulated | **4,299** |
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
| 5 | `7e6ad3c6df7a9643` | crypto | **1.42** | 0.5725 | 4.04 | 0.037 | cross_sectional | all | `G3_cpcv_pbo` |
| 6 | `a7ff27f45f42bd85` | crypto | **1.40** | 0.5978 | 4.22 | 0.051 | cross_sectional | all | `G3_cpcv_pbo` |
| 7 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 8 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 9 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 10 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 11 | `ec58e5f691d88894` | crypto | **1.20** | 0.7262 | 4.91 | 0.059 | cross_sectional | all | `G3_cpcv_pbo` |
| 12 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 13 | `64eed38552709d9a` | crypto | **1.16** | 0.7519 | 5.08 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 14 | `473219061ecd274b` | crypto | **1.13** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 15 | `ebe2e17a51d99e1d` | crypto | **1.12** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 16 | `1e91960d528e08e6` | crypto | **1.00** | 0.6495 | 4.39 | 0.064 | cross_sectional | all | `ADMITTED` |
| 17 | `88d45506624808b5` | xau | **0.98** | 0.8637 | 18.08 | 0.000 | cross_sectional | low_vol | `G8_orthogonality` |
| 18 | `4ec5fdcb324d8efb` | crypto | **0.96** | 0.7322 | 4.95 | 0.059 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `6edd3e376d21fb4a` | crypto | **0.95** | 0.6110 | 4.26 | 0.068 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `f10b1be8ae237541` | crypto | **0.94** | 0.8138 | 5.50 | 0.027 | cross_sectional | all | `G3_cpcv_pbo` |

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
**#5 · `7e6ad3c6df7a9643` — DSR-z 1.42 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); amihud_illiquidity(window=32)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=7e6ad3c6df7a9643  gen=21  by=evo_mutate  nodes=5
```
**#6 · `a7ff27f45f42bd85` — DSR-z 1.40 · died at `G3_cpcv_pbo` · families: liquidity, macro, microstructure, positioning**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); cot_zscore(window=27)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=a7ff27f45f42bd85  gen=20  by=llm_critic  nodes=5
```
**#7 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#8 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#9 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#10 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#11 · `ec58e5f691d88894` — DSR-z 1.20 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=ec58e5f691d88894  gen=25  by=evo_mutate  nodes=4
```
**#12 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
**#13 · `64eed38552709d9a` — DSR-z 1.16 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.4384386928813)
  id=64eed38552709d9a  gen=36  by=evo_mutate  nodes=4
```
**#14 · `473219061ecd274b` — DSR-z 1.13 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=473219061ecd274b  gen=49  by=evo_mutate  nodes=4
```
**#15 · `ebe2e17a51d99e1d` — DSR-z 1.12 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=ebe2e17a51d99e1d  gen=51  by=evo_crossover  nodes=4
```
**#16 · `1e91960d528e08e6` — DSR-z 1.00 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=20)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=1e91960d528e08e6  gen=51  by=evo_mutate  nodes=4
```
**#17 · `88d45506624808b5` — DSR-z 0.98 · died at `G8_orthogonality` · families: breakout, pattern, statistical**
```
[xau] gated_and (long_bias, regime=low_vol) on H4
  features: autocorr(lag=2, window=43); breakout(window=76)
  sizing:   rank_bucket(top_frac=0.4136012810233344, gross=1.9409931460238488, per_name_cap=0.036402453175584396)
  risk:     horizon_hold(horizon=5, cost_stress=1.0)
  id=88d45506624808b5  gen=23  by=evo_mutate  nodes=5
```
**#18 · `4ec5fdcb324d8efb` — DSR-z 0.96 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=4ec5fdcb324d8efb  gen=60  by=evo_mutate  nodes=4
```
**#19 · `6edd3e376d21fb4a` — DSR-z 0.95 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=45, cost_stress=1.6320938700249077)
  id=6edd3e376d21fb4a  gen=20  by=evo_mutate  nodes=4
```
**#20 · `f10b1be8ae237541` — DSR-z 0.94 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3, gross=0.8647831983512492, per_name_cap=0.05302264635441836)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=f10b1be8ae237541  gen=56  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `GS_screen` | 8,161 | 65.5% | — |
| `G1_sanity` | 2,434 | 19.5% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 546 | 4.4% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 467 | 3.7% | parameter tuning overfit (high PBO) |
| `ADMITTED` | 442 | 3.5% | **cleared every gate** |
| `G5_robustness` | 144 | 1.2% | bootstrap tail drawdown too large |
| `G8_orthogonality` | 139 | 1.1% | duplicates an existing archive member |
| `G9_plateau` | 133 | 1.1% | — |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 4391 | 81 | 1.57 | █████████████████· |
| `xau` | 3912 | 255 | 0.98 | ███████████······· |
| `fx` | 4163 | 106 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 10290 | 190 | 1.57 | █████████████████· |
| `directional` | 2176 | 252 | 0.33 | ████·············· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 7928 | 423 | 1.57 | █████████████████· |
| `llm` | 1142 | 18 | 1.40 | ███████████████··· |
| `template` | 575 | 0 | 0.31 | ███··············· |
| `miner` | 2180 | 1 | -0.24 | ·················· |
| `random` | 641 | 0 | -0.57 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 6173 | 182 | 1.57 | █████████████████· |
| `low_vol` | 3163 | 227 | 0.98 | ███████████······· |
| `trend` | 524 | 25 | 0.47 | █████············· |
| `chop` | 757 | 0 | 0.22 | ██················ |
| `high_vol` | 1849 | 8 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 9762 | 334 | 1.57 | █████████████████· |
| `kelly_fraction` | 851 | 0 | 0.93 | ██████████········ |
| `fixed_fractional` | 1080 | 105 | -0.34 | ·················· |
| `vol_target` | 656 | 3 | -1.05 | ·················· |
| `atr_scaled` | 117 | 0 | -2.19 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 1192 | 79 | 1.57 | █████████████████· |
| `liquidity` | 968 | 78 | 1.57 | █████████████████· |
| `macro` | 2702 | 105 | 1.47 | ████████████████·· |
| `regime` | 976 | 19 | 1.47 | ████████████████·· |
| `rates` | 968 | 19 | 1.47 | ████████████████·· |
| `positioning` | 1740 | 89 | 1.40 | ███████████████··· |
| `statistical` | 2473 | 103 | 0.98 | ███████████······· |
| `pattern` | 986 | 39 | 0.98 | ███████████······· |
| `breakout` | 897 | 39 | 0.98 | ███████████······· |
| `momentum` | 2989 | 202 | 0.86 | █████████········· |
| `trend` | 2799 | 159 | 0.86 | █████████········· |
| `auction_market_theory` | 2403 | 142 | 0.85 | █████████········· |
| `market_profile` | 976 | 46 | 0.85 | █████████········· |
| `order_flow` | 769 | 51 | 0.55 | ██████············ |
| `oscillator` | 2005 | 145 | 0.47 | █████············· |
| `volume` | 1285 | 111 | 0.47 | █████············· |
| `mean_reversion` | 516 | 29 | 0.46 | █████············· |
| `volatility` | 2096 | 118 | 0.31 | ███··············· |
| `cross_asset` | 580 | 15 | 0.31 | ███··············· |
| `intermarket` | 567 | 15 | 0.31 | ███··············· |
| `mixed` | 837 | 48 | -0.11 | ·················· |
| `volume_profile` | 688 | 104 | -0.20 | ·················· |
| `ict` | 1397 | 45 | -0.24 | ·················· |
| `smc` | 1397 | 45 | -0.24 | ·················· |
| `persistence` | 868 | 8 | -0.51 | ·················· |
| `crypto` | 91 | 0 | -0.77 | ·················· |
| `funding` | 91 | 0 | -0.77 | ·················· |
| `event` | 81 | 0 | -0.93 | ·················· |
| `ml_derived` | 50 | 0 | -1.11 | ·················· |
| `calendar` | 40 | 0 | -1.69 | ·················· |
| `sentiment` | 22 | 0 | -2.95 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `fed_policy_bias` | 461 | +3.262 | **carries signal** |
| `rel_strength` | 292 | +1.786 | **carries signal** |
| `amihud_illiquidity` | 559 | +1.281 | **carries signal** |
| `atr_expansion` | 677 | +1.157 | **carries signal** |
| `adx` | 470 | +1.049 | **carries signal** |
| `intx_137ddd7b` | 2 | +0.940 | **carries signal** |
| `tsmom_blend` | 142 | +0.803 | **carries signal** |
| `intx_b8f9f9ec` | 2 | +0.640 | **carries signal** |
| `order_flow_imbalance` | 24 | +0.637 | **carries signal** |
| `autocorr` | 208 | +0.588 | **carries signal** |
| `liquidity_sweep` | 295 | +0.573 | **carries signal** |
| `momentum` | 610 | +0.473 | **carries signal** |
| `structure_break` | 235 | +0.404 | **carries signal** |
| `macd` | 1416 | +0.385 | **carries signal** |
| `intx_91446ccb` | 282 | +0.333 | **carries signal** |

---

## 5 · Archive (23 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 0.976 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `xau:intraday:low:long:low_vol` | xau | 0.554 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `fx:position:low:long:low_vol` | fx | 0.508 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `xau:intraday:trade:long:trend` | xau | 0.448 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.274 |
| `fx:swing:med:long:low_vol` | fx | 0.247 |
| `fx:swing:med:long:all` | fx | 0.247 |
| `fx:swing:low:long:all` | fx | 0.205 |
| `crypto:position:med:neutral:all` | crypto | 0.174 |
| `fx:position:low:long:all` | fx | 0.077 |
| `xau:intraday:low:long:all` | xau | 0.065 |
| `crypto:intraday:low:neutral:all` | crypto | -0.021 |
| `crypto:intraday:med:neutral:all` | crypto | -0.034 |
| `crypto:swing:low:neutral:all` | crypto | -0.072 |
| `crypto:intraday:trade:long:low_vol` | crypto | -0.104 |
| `fx:intraday:low:long:all` | fx | -0.108 |
| `crypto:swing:med:neutral:all` | crypto | -0.219 |
| `xau:intraday:trade:long:high_vol` | xau | -0.422 |

## 6 · Lessons library (4,299)

- ×12 — [PASS] adx+candlestick_pattern+interaction+mined on a directional book promoted to the candidate pool
- ×11 — [GS_screen] auction_market_theory+macro+market_profile+momentum+oscillator+persistence+positioning+statistical (cross_sect
- ×10 — [PASS] auction_market_theory+market_profile+momentum+oscillator+trend+volatility+volume+volume_profile on a direction
- ×8 — [GS_screen] breakout+pattern+volatility (directional) — raw predictive strength too weak to clear the FDR screen [p_single
- ×8 — [GS_screen] macro+positioning+statistical (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_
- ×8 — [GS_screen] momentum+oscillator (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_single=0.0
- ×7 — [G3_cpcv_pbo] auction_market_theory+market_profile+momentum+oscillator+trend+volatility+volume+volume_profile (directional) 
- ×6 — [GS_screen] auction_market_theory+market_profile+momentum+oscillator+trend+volatility+volume+volume_profile (directional) 
- ×5 — [PASS] momentum+oscillator+trend on a cross_sectional book promoted to the candidate pool
- ×5 — [PASS] adx+candlestick_pattern+interaction+liquidity_sweep+mean_reversion+mined+order_block_strength+statistical on a
- ×4 — [PASS] auction_market_theory+market_profile+momentum+oscillator+statistical+trend+volume+volume_profile on a directio
- ×4 — [GS_screen] auction_market_theory+macro+market_profile+positioning (cross_sectional) — raw predictive strength too weak to
- ×4 — [GS_screen] adx+candlestick_pattern+interaction+mean_reversion+mined+statistical (directional) — raw predictive strength t
- ×4 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×4 — [GS_screen] cross_asset+intermarket+macro+rates+regime+volume (cross_sectional) — raw predictive strength too weak to clea

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*