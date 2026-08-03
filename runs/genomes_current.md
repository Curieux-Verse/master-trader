# 🧬 Master Trader — Genome Population Report

*Generated 2026-08-03 07:08 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **88,030** |
| Deflated-Sharpe trial count (raw N) | **170,678** *(evals 88,030 + 82,648 screened)* |
| **Effective** independent trials (N_eff) | **126,458** *(ρ̄=0.023313273586967765 — the bar the DSR actually uses)* |
| Admitted to archive | **8740** |
| Rejected | **79,290** (90.1%) |
| Distinct families explored | **31** |
| Lessons accumulated | **42,438** |
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
| 12 | `0ab5c357ba5b0ba8` | crypto | **1.38** | 0.5725 | 4.04 | 0.047 | cross_sectional | all | `G9_plateau` |
| 13 | `bb0f922875834061` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 14 | `f933bee037781a52` | crypto | **1.35** | 0.5661 | 3.99 | 0.056 | cross_sectional | all | `G9_plateau` |
| 15 | `cd01243357770202` | crypto | **1.29** | 0.8015 | 5.41 | 0.043 | cross_sectional | all | `ADMITTED` |
| 16 | `4b35b04ef47097b3` | crypto | **1.22** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 17 | `ec58e5f691d88894` | crypto | **1.20** | 0.7262 | 4.91 | 0.059 | cross_sectional | all | `G3_cpcv_pbo` |
| 18 | `2c6d479031c53128` | crypto | **1.18** | 0.7493 | 5.06 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 19 | `64eed38552709d9a` | crypto | **1.16** | 0.7519 | 5.08 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |
| 20 | `473219061ecd274b` | crypto | **1.13** | 0.7556 | 5.10 | 0.056 | cross_sectional | all | `G3_cpcv_pbo` |

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
**#12 · `0ab5c357ba5b0ba8` — DSR-z 1.38 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.06321046330781907)
  risk:     horizon_hold(horizon=44, cost_stress=1.6320938700249077)
  id=0ab5c357ba5b0ba8  gen=15  by=evo_mutate  nodes=5
```
**#13 · `bb0f922875834061` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=bb0f922875834061  gen=15  by=evo_mutate  nodes=5
```
**#14 · `f933bee037781a52` — DSR-z 1.35 · died at `G9_plateau` · families: liquidity, macro, microstructure, rates, regime**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80); fed_policy_bias(window=11)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=44, cost_stress=1.841941733546131)
  id=f933bee037781a52  gen=16  by=llm_critic  nodes=5
```
**#15 · `cd01243357770202` — DSR-z 1.29 · died at `ADMITTED` · families: liquidity, microstructure**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=81)
  sizing:   rank_bucket(top_frac=0.3, gross=1.987931652984258, per_name_cap=0.074638)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=cd01243357770202  gen=79  by=evo_mutate  nodes=4
```
**#16 · `4b35b04ef47097b3` — DSR-z 1.22 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=4b35b04ef47097b3  gen=30  by=evo_mutate  nodes=4
```
**#17 · `ec58e5f691d88894` — DSR-z 1.20 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=80)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=ec58e5f691d88894  gen=25  by=evo_mutate  nodes=4
```
**#18 · `2c6d479031c53128` — DSR-z 1.18 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.6320938700249077)
  id=2c6d479031c53128  gen=31  by=evo_crossover  nodes=4
```
**#19 · `64eed38552709d9a` — DSR-z 1.16 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.4384386928813)
  id=64eed38552709d9a  gen=36  by=evo_mutate  nodes=4
```
**#20 · `473219061ecd274b` — DSR-z 1.13 · died at `G3_cpcv_pbo` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=58)
  sizing:   rank_bucket(top_frac=0.3887775642386677, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=48, cost_stress=1.174031461273827)
  id=473219061ecd274b  gen=49  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `—` | 49,692 | 56.4% | — |
| `GS_screen` | 16,858 | 19.2% | — |
| `ADMITTED` | 8,740 | 9.9% | **cleared every gate** |
| `G1_sanity` | 6,030 | 6.8% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,885 | 4.4% | parameter tuning overfit (high PBO) |
| `G0_eval` | 1,907 | 2.2% | did not produce a valid backtest |
| `G9_plateau` | 512 | 0.6% | — |
| `G8_orthogonality` | 286 | 0.3% | duplicates an existing archive member |
| `G5_robustness` | 115 | 0.1% | bootstrap tail drawdown too large |
| `G2_oos` | 5 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 29807 | 3300 | 1.57 | █████████████████· |
| `xau` | 28098 | 4141 | 0.83 | █████████········· |
| `fx` | 30125 | 1299 | 0.32 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 67019 | 4708 | 1.57 | █████████████████· |
| `directional` | 21011 | 4032 | 0.76 | ████████·········· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 70328 | 8728 | 1.57 | █████████████████· |
| `llm` | 4956 | 9 | 1.35 | ███████████████··· |
| `template` | 2834 | 0 | 0.31 | ███··············· |
| `miner` | 6399 | 3 | -0.24 | ·················· |
| `random` | 3513 | 0 | -0.67 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 42430 | 4120 | 1.57 | █████████████████· |
| `low_vol` | 26663 | 4135 | 0.83 | █████████········· |
| `chop` | 5261 | 10 | 0.22 | ██················ |
| `trend` | 5673 | 400 | 0.02 | ·················· |
| `high_vol` | 8003 | 75 | -0.37 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 69425 | 5703 | 1.57 | █████████████████· |
| `kelly_fraction` | 1688 | 10 | 0.85 | █████████········· |
| `fixed_fractional` | 14648 | 3026 | 0.76 | ████████·········· |
| `vol_target` | 1568 | 1 | -1.05 | ·················· |
| `atr_scaled` | 701 | 0 | -2.73 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `microstructure` | 15134 | 3169 | 1.57 | █████████████████· |
| `liquidity` | 14436 | 3145 | 1.57 | █████████████████· |
| `macro` | 19494 | 2455 | 1.38 | ███████████████··· |
| `regime` | 9854 | 2213 | 1.38 | ███████████████··· |
| `rates` | 7355 | 1069 | 1.38 | ███████████████··· |
| `momentum` | 16972 | 2796 | 0.86 | █████████········· |
| `trend` | 14407 | 2194 | 0.86 | █████████········· |
| `auction_market_theory` | 13697 | 2323 | 0.85 | █████████········· |
| `market_profile` | 9107 | 2033 | 0.85 | █████████········· |
| `statistical` | 18112 | 3033 | 0.83 | █████████········· |
| `pattern` | 2924 | 138 | 0.83 | █████████········· |
| `breakout` | 2760 | 138 | 0.83 | █████████········· |
| `volatility` | 12305 | 2246 | 0.76 | ████████·········· |
| `mean_reversion` | 8835 | 2300 | 0.76 | ████████·········· |
| `ict` | 7699 | 809 | 0.75 | ████████·········· |
| `smc` | 7699 | 809 | 0.75 | ████████·········· |
| `positioning` | 13469 | 1780 | 0.60 | ███████··········· |
| `ml_derived` | 6103 | 1882 | 0.60 | ███████··········· |
| `order_flow` | 2640 | 216 | 0.55 | ██████············ |
| `cross_asset` | 1888 | 265 | 0.53 | ██████············ |
| `intermarket` | 1868 | 265 | 0.53 | ██████············ |
| `oscillator` | 5954 | 226 | 0.40 | ████·············· |
| `event` | 2446 | 308 | 0.12 | █················· |
| `volume` | 4316 | 274 | 0.03 | ·················· |
| `mixed` | 21154 | 867 | -0.11 | ·················· |
| `volume_profile` | 2210 | 109 | -0.16 | ·················· |
| `crypto` | 1544 | 387 | -0.30 | ·················· |
| `funding` | 1544 | 387 | -0.30 | ·················· |
| `persistence` | 2016 | 31 | -0.51 | ·················· |
| `calendar` | 50 | 0 | -1.69 | ·················· |
| `sentiment` | 29 | 0 | -17.94 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `intx_d77b40a2` | 3 | +8.415 | **carries signal** |
| `intx_4cc472c3` | 2 | +6.510 | **carries signal** |
| `intx_cada3db7` | 26 | +5.899 | **carries signal** |
| `intx_2d2c770d` | 2 | +5.351 | **carries signal** |
| `intx_72d2ef7d` | 40 | +5.340 | **carries signal** |
| `intx_634b10e7` | 206 | +4.647 | **carries signal** |
| `intx_2e781688` | 155 | +4.342 | **carries signal** |
| `intx_ab41ce7c` | 109 | +3.777 | **carries signal** |
| `intx_64624138` | 3 | +3.748 | **carries signal** |
| `intx_1b019378` | 19 | +2.700 | **carries signal** |
| `intx_134c693a` | 14 | +2.049 | **carries signal** |
| `intx_5c98e1f8` | 13 | +2.009 | **carries signal** |
| `intx_9c85e9c3` | 156 | +1.924 | **carries signal** |
| `intx_c3fb2de8` | 2 | +1.763 | **carries signal** |
| `intx_25dbb457` | 187 | +1.648 | **carries signal** |

---

## 5 · Archive (49 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:intraday:trade:long:low_vol` | xau | 1.530 |
| `xau:swing:trade:long:low_vol` | xau | 1.138 |
| `xau:intraday:trade:long:trend` | xau | 0.801 |
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
| `xau:intraday:low:neutral:all` | xau | 0.459 |
| `xau:intraday:trade:long:all` | xau | 0.446 |
| `fx:swing:low:long:high_vol` | fx | 0.432 |
| `crypto:position:low:neutral:all` | crypto | 0.427 |
| `xau:intraday:low:long:trend` | xau | 0.389 |
| `xau:intraday:trade:long:high_vol` | xau | 0.361 |
| `crypto:position:med:neutral:chop` | crypto | 0.356 |
| `fx:position:low:long:high_vol` | fx | 0.345 |
| `crypto:position:high:neutral:all` | crypto | 0.342 |
| `xau:swing:low:long:trend` | xau | 0.333 |

## 6 · Lessons library (42,438)

- ×7 — [PASS] volatility on a directional book promoted to the candidate pool
- ×6 — [PASS] interaction+intx_1578410f+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_ecf2c12e+intx_fe341f6e+mean_reversion
- ×6 — [PASS] har_vol+interaction+mined+value_area_position+volatility on a directional book promoted to the candidate pool
- ×5 — [GS_screen] interaction+intx_6ff832ad+intx_a99b3c1a+macro+mined+positioning (cross_sectional) — raw predictive strength to
- ×5 — [PASS] har_vol+interaction+mined+value_area_position on a directional book promoted to the candidate pool
- ×4 — [GS_screen] amihud_illiquidity+auction_market_theory+interaction+intx_137ddd7b+intx_421762f1+intx_5a1e9077+liquidity+macro
- ×4 — [GS_screen] interaction+mined+reversion+value_area_position (cross_sectional) — raw predictive strength too weak to clear 
- ×4 — [PASS] interaction+intx_8e0d4062+intx_fe341f6e+mined+volatility on a directional book promoted to the candidate pool
- ×4 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×4 — [GS_screen] auction_market_theory+liquidity+macro+market_profile+microstructure+rates+regime (cross_sectional) — raw predi
- ×4 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+statistical+volatilit
- ×3 — [PASS] interaction+intx_3086ff7a+intx_753ea6e7+intx_8e0d4062+intx_fe341f6e+mean_reversion+mined+reversion+statistical
- ×3 — [GS_screen] adx+candlestick_pattern+interaction+mined (directional) — raw predictive strength too weak to clear the FDR sc
- ×3 — [GS_screen] interaction+intx_6ff832ad+intx_a99b3c1a+intx_c1240e5f+intx_e4425d6a+ma_cross+macro+mined+positioning+rolling_s
- ×3 — [G1_sanity] interaction+intx_2072404a+intx_3d05d214+intx_96188933+intx_96565680+intx_aea7ae3e+intx_e66eeacb+mined (cross_s

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*