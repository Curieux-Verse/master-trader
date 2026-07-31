# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-31 04:05 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **62,306** |
| Deflated-Sharpe trial count (raw N) | **120,579** *(evals 62,306 + 58,273 screened)* |
| **Effective** independent trials (N_eff) | **86,714** *(ρ̄=0.0324205177637609 — the bar the DSR actually uses)* |
| Admitted to archive | **7117** |
| Rejected | **55,189** (88.6%) |
| Distinct families explored | **31** |
| Lessons accumulated | **30,628** |
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
| `—` | 28,740 | 46.1% | — |
| `GS_screen` | 15,456 | 24.8% | — |
| `ADMITTED` | 7,117 | 11.4% | **cleared every gate** |
| `G1_sanity` | 5,478 | 8.8% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,972 | 6.4% | parameter tuning overfit (high PBO) |
| `G0_eval` | 555 | 0.9% | did not produce a valid backtest |
| `G9_plateau` | 528 | 0.8% | — |
| `G8_orthogonality` | 311 | 0.5% | duplicates an existing archive member |
| `G5_robustness` | 135 | 0.2% | bootstrap tail drawdown too large |
| `G2_oos` | 14 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 21690 | 2589 | 1.57 | █████████████████· |
| `xau` | 20537 | 3165 | 0.83 | █████████········· |
| `fx` | 20079 | 1363 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 48418 | 4101 | 1.57 | █████████████████· |
| `directional` | 13888 | 3016 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 53473 | 7098 | 1.57 | █████████████████· |
| `llm` | 1450 | 13 | 1.40 | ███████████████··· |
| `template` | 882 | 0 | 0.31 | ███··············· |
| `miner` | 5412 | 6 | -0.24 | ·················· |
| `random` | 1089 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 30102 | 3458 | 1.57 | █████████████████· |
| `low_vol` | 20558 | 3255 | 0.83 | █████████········· |
| `chop` | 3475 | 7 | 0.22 | ██················ |
| `trend` | 2876 | 327 | 0.02 | ·················· |
| `high_vol` | 5295 | 70 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 50754 | 4832 | 1.57 | █████████████████· |
| `kelly_fraction` | 1086 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 9496 | 2274 | 0.76 | ████████·········· |
| `vol_target` | 769 | 1 | -1.05 | ·················· |
| `atr_scaled` | 201 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 10892 | 2516 | 1.57 | █████████████████· |
| `liquidity` | 10356 | 2510 | 1.57 | █████████████████· |
| `macro` | 15591 | 2503 | 1.40 | ███████████████··· |
| `positioning` | 10409 | 1618 | 1.40 | ███████████████··· |
| `regime` | 6263 | 1304 | 1.38 | ███████████████··· |
| `rates` | 6080 | 1193 | 1.38 | ███████████████··· |
| `momentum` | 11429 | 1818 | 0.86 | █████████········· |
| `trend` | 9956 | 1512 | 0.86 | █████████········· |
| `auction_market_theory` | 9957 | 1802 | 0.85 | █████████········· |
| `market_profile` | 6261 | 1519 | 0.85 | █████████········· |
| `statistical` | 14173 | 2567 | 0.83 | █████████········· |
| `pattern` | 1979 | 115 | 0.83 | █████████········· |
| `breakout` | 1826 | 115 | 0.83 | █████████········· |
| `volatility` | 8314 | 1520 | 0.76 | ████████·········· |
| `mean_reversion` | 6474 | 1823 | 0.76 | ████████·········· |
| `ict` | 6444 | 776 | 0.75 | ████████·········· |
| `smc` | 6444 | 776 | 0.75 | ████████·········· |
| `ml_derived` | 2931 | 831 | 0.60 | ███████··········· |
| `order_flow` | 2087 | 246 | 0.55 | ██████············ |
| `cross_asset` | 1265 | 104 | 0.53 | ██████············ |
| `intermarket` | 1250 | 104 | 0.53 | ██████············ |
| `oscillator` | 4766 | 200 | 0.40 | ████·············· |
| `event` | 2103 | 440 | 0.12 | █················· |
| `volume` | 3083 | 206 | 0.03 | ·················· |
| `mixed` | 11823 | 685 | -0.11 | ·················· |
| `volume_profile` | 1702 | 122 | -0.16 | ·················· |
| `crypto` | 739 | 135 | -0.30 | ·················· |
| `funding` | 739 | 135 | -0.30 | ·················· |
| `persistence` | 1642 | 32 | -0.51 | ·················· |
| `calendar` | 40 | 0 | -1.69 | ·················· |
| `sentiment` | 23 | 0 | -20.43 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_d77b40a2` | 2 | +4.885 | **carries signal** |
| `intx_9c77b83f` | 13 | +4.489 | **carries signal** |
| `amihud_illiquidity` | 11389 | +1.402 | **carries signal** |
| `intx_2f8a5346` | 3 | +1.208 | **carries signal** |
| `intx_efbc5645` | 4098 | +1.176 | **carries signal** |
| `intx_49fa7f67` | 235 | +1.164 | **carries signal** |
| `intx_40fdcf76` | 852 | +1.075 | **carries signal** |
| `fed_policy_bias` | 4699 | +1.042 | **carries signal** |
| `intx_cbab1b3b` | 2339 | +0.980 | **carries signal** |
| `intx_c9af9e0d` | 3 | +0.977 | **carries signal** |
| `intx_0228c153` | 371 | +0.933 | **carries signal** |
| `vol_regime_tag` | 3335 | +0.927 | **carries signal** |
| `intx_e75bf6dc` | 1123 | +0.924 | **carries signal** |
| `intx_3190c15f` | 140 | +0.899 | **carries signal** |

---

## 5 · Archive (45 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.530 |
| `xau:swing:trade:long:low_vol` | xau | 1.011 |
| `xau:scalp:trade:long:low_vol` | xau | 0.740 |
| `crypto:position:med:neutral:all` | crypto | 0.733 |
| `fx:position:low:long:low_vol` | fx | 0.667 |
| `fx:position:med:long:low_vol` | fx | 0.635 |
| `xau:intraday:low:long:low_vol` | xau | 0.617 |
| `xau:intraday:low:neutral:low_vol` | xau | 0.614 |
| `fx:position:low:long:all` | fx | 0.602 |
| `fx:position:med:long:all` | fx | 0.555 |
| `fx:swing:med:long:high_vol` | fx | 0.518 |
| `xau:intraday:low:long:all` | xau | 0.477 |
| `fx:position:low:neutral:low_vol` | fx | 0.477 |
| `fx:position:med:long:high_vol` | fx | 0.470 |
| `xau:intraday:trade:long:trend` | xau | 0.448 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.417 |
| `xau:intraday:low:neutral:all` | xau | 0.404 |
| `xau:intraday:low:long:trend` | xau | 0.389 |
| `xau:intraday:trade:long:high_vol` | xau | 0.361 |
| `crypto:position:med:neutral:chop` | crypto | 0.356 |
| `fx:position:low:long:high_vol` | fx | 0.345 |
| `crypto:position:high:neutral:all` | crypto | 0.342 |
| `xau:swing:low:long:trend` | xau | 0.333 |

## 6 · Lessons library (30,628)

- ×15 — [PASS] adx+amihud_illiquidity+auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_5a1e9077+intx_a16b76
- ×12 — [PASS] auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_a16b7695+intx_ab31bc67+liquidity+market_pro
- ×9 — [PASS] ict+interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+smc+statistical+v
- ×8 — [GS_screen] interaction+intx_62a4f5a8+intx_678cc793+macro+mined+positioning (cross_sectional) — raw predictive strength to
- ×6 — [PASS] volatility on a directional book promoted to the candidate pool
- ×5 — [GS_screen] interaction+intx_080bbe39+intx_10e814d4+intx_39165f4d+intx_495677d1+intx_4f97afa7+intx_6ff832ad+intx_a99b3c1a+
- ×4 — [PASS] adx+candlestick_pattern+interaction+mined+momentum+volatility on a directional book promoted to the candidate 
- ×4 — [PASS] adx+candlestick_pattern+interaction+mined+momentum on a directional book promoted to the candidate pool
- ×4 — [PASS] ict+interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_faa29648+intx_fe341f6e+mean_reversion+mined+smc
- ×4 — [G1_sanity] adx+amihud_illiquidity+auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_5a1e9077+intx_62a4f5
- ×3 — [PASS] adx+candlestick_pattern+interaction+mined+trend on a directional book promoted to the candidate pool
- ×3 — [PASS] adx+candlestick_pattern+interaction+mined on a directional book promoted to the candidate pool
- ×3 — [PASS] amihud_illiquidity+auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_5a1e9077+intx_a16b7695+i
- ×3 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mined+volatility on a directional book pro
- ×3 — [PASS] auction_market_theory+interaction+intx_a16b7695+intx_ab31bc67+liquidity+market_profile+microstructure+mined+ml

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*