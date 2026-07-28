# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-28 04:02 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **158,465** |
| Deflated-Sharpe trial count (raw N) | **354,983** *(evals 237,663 + 117,320 screened)* |
| **Effective** independent trials (N_eff) | **264,408** *(ρ̄=0.029257442502756723 — the bar the DSR actually uses)* |
| Admitted to archive | **3631** |
| Rejected | **154,834** (97.7%) |
| Distinct families explored | **31** |
| Lessons accumulated | **18,906** |
| Best DSR-z | **+2.345** vs bar 1.645 — ✅ **cleared the bar** |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `a18e5b4116136194` | crypto | **2.35** ✅ | 0.9566 | 6.53 | 0.035 | cross_sectional | all | `G8_orthogonality` |
| 2 | `964e4bf4fbacc8f7` | crypto | **2.32** ✅ | 0.9492 | 6.48 | 0.035 | cross_sectional | all | `G8_orthogonality` |
| 3 | `89a27681b38b0520` | crypto | **2.32** ✅ | 0.9568 | 6.53 | 0.035 | cross_sectional | all | `G8_orthogonality` |
| 4 | `2e85552d653efedf` | crypto | **2.28** ✅ | 0.9565 | 6.53 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 5 | `114eeb894a0cc7ad` | crypto | **2.24** ✅ | 0.9608 | 6.56 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 6 | `44336b2629822dda` | crypto | **2.23** ✅ | 0.9414 | 6.43 | 0.035 | cross_sectional | all | `G8_orthogonality` |
| 7 | `0a5b18d055087eaa` | crypto | **2.22** ✅ | 0.9608 | 6.56 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 8 | `721f3eb7f677cb55` | crypto | **2.19** ✅ | 0.9590 | 6.55 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 9 | `757bf6b2afe3e6e7` | crypto | **2.17** ✅ | 0.9541 | 6.51 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 10 | `5b4ceda18d0ce825` | crypto | **2.17** ✅ | 0.9553 | 6.52 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 11 | `b82c7b568fa01438` | crypto | **2.13** ✅ | 0.9541 | 6.51 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 12 | `367d789e05a29a5b` | crypto | **2.13** ✅ | 0.9610 | 6.56 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 13 | `6748ff23112c403d` | crypto | **2.12** ✅ | 0.9526 | 6.50 | 0.053 | cross_sectional | all | `ADMITTED` |
| 14 | `203e87acbc70d506` | crypto | **2.11** ✅ | 0.9508 | 6.49 | 0.053 | cross_sectional | all | `ADMITTED` |
| 15 | `6b67d42e33f78f49` | crypto | **2.10** ✅ | 0.9562 | 6.53 | 0.053 | cross_sectional | all | `ADMITTED` |
| 16 | `e9c2d285112d1a5c` | crypto | **2.10** ✅ | 0.9415 | 6.43 | 0.053 | cross_sectional | all | `ADMITTED` |
| 17 | `58233c33043ebf60` | crypto | **2.09** ✅ | 0.9571 | 6.53 | 0.053 | cross_sectional | all | `ADMITTED` |
| 18 | `b2b22a197c72b51a` | crypto | **2.08** ✅ | 0.9456 | 6.45 | 0.053 | cross_sectional | all | `G8_orthogonality` |
| 19 | `98608bfaf3fa9ea4` | crypto | **2.08** ✅ | 0.9415 | 6.43 | 0.053 | cross_sectional | all | `ADMITTED` |
| 20 | `b90757e9fa877bda` | crypto | **2.07** ✅ | 0.9186 | 6.27 | 0.035 | cross_sectional | all | `ADMITTED` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `a18e5b4116136194` — DSR-z 2.35 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.0921862561511815)
  risk:     horizon_hold(horizon=47, cost_stress=1.0034517329096022)
  id=a18e5b4116136194  gen=186  by=evo_mutate  nodes=6
```
**#2 · `964e4bf4fbacc8f7` — DSR-z 2.32 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.0921862561511815)
  risk:     horizon_hold(horizon=47, cost_stress=1.152415413989577)
  id=964e4bf4fbacc8f7  gen=188  by=evo_mutate  nodes=6
```
**#3 · `89a27681b38b0520` — DSR-z 2.32 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.0921862561511815)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=89a27681b38b0520  gen=185  by=evo_mutate  nodes=6
```
**#4 · `2e85552d653efedf` — DSR-z 2.28 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.9383322651666948, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=2e85552d653efedf  gen=189  by=evo_mutate  nodes=6
```
**#5 · `114eeb894a0cc7ad` — DSR-z 2.24 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7573397835453717, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=114eeb894a0cc7ad  gen=241  by=evo_mutate  nodes=6
```
**#6 · `44336b2629822dda` — DSR-z 2.23 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.0921862561511815)
  risk:     horizon_hold(horizon=47, cost_stress=1.308208430289754)
  id=44336b2629822dda  gen=186  by=evo_mutate  nodes=6
```
**#7 · `0a5b18d055087eaa` — DSR-z 2.22 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7573397835453717, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=0a5b18d055087eaa  gen=188  by=evo_mutate  nodes=6
```
**#8 · `721f3eb7f677cb55` — DSR-z 2.19 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0398229746950594)
  id=721f3eb7f677cb55  gen=248  by=evo_mutate  nodes=6
```
**#9 · `757bf6b2afe3e6e7` — DSR-z 2.17 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.1381591122691177)
  id=757bf6b2afe3e6e7  gen=260  by=evo_mutate  nodes=6
```
**#10 · `5b4ceda18d0ce825` — DSR-z 2.17 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.1143000713965123)
  id=5b4ceda18d0ce825  gen=260  by=evo_mutate  nodes=6
```
**#11 · `b82c7b568fa01438` — DSR-z 2.13 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.136773263191575)
  id=b82c7b568fa01438  gen=281  by=evo_mutate  nodes=6
```
**#12 · `367d789e05a29a5b` — DSR-z 2.13 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=367d789e05a29a5b  gen=247  by=evo_mutate  nodes=6
```
**#13 · `6748ff23112c403d` — DSR-z 2.12 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0866180485904633)
  id=6748ff23112c403d  gen=176  by=evo_crossover  nodes=6
```
**#14 · `203e87acbc70d506` — DSR-z 2.11 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.1213448964992694)
  id=203e87acbc70d506  gen=159  by=evo_mutate  nodes=6
```
**#15 · `6b67d42e33f78f49` — DSR-z 2.10 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.018164475540221)
  id=6b67d42e33f78f49  gen=187  by=evo_mutate  nodes=6
```
**#16 · `e9c2d285112d1a5c` — DSR-z 2.10 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.298944)
  id=e9c2d285112d1a5c  gen=139  by=evo_mutate  nodes=6
```
**#17 · `58233c33043ebf60` — DSR-z 2.09 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=58233c33043ebf60  gen=187  by=evo_mutate  nodes=6
```
**#18 · `b2b22a197c72b51a` — DSR-z 2.08 · died at `G8_orthogonality` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=66)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.7446705606517607, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=b2b22a197c72b51a  gen=248  by=evo_mutate  nodes=6
```
**#19 · `98608bfaf3fa9ea4` — DSR-z 2.08 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.18045218177412267, gross=1.2771138515752631, per_name_cap=0.13936442095981705)
  risk:     horizon_hold(horizon=47, cost_stress=1.298944)
  id=98608bfaf3fa9ea4  gen=138  by=evo_crossover  nodes=6
```
**#20 · `b90757e9fa877bda` — DSR-z 2.07 · died at `ADMITTED` · families: breakout, liquidity, microstructure, pattern, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68)
  sizing:   rank_bucket(top_frac=0.2018593855204894, gross=1.2771138515752631, per_name_cap=0.0921862561511815)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=b90757e9fa877bda  gen=186  by=evo_mutate  nodes=6
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 71,878 | 45.4% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 46,146 | 29.1% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 19,441 | 12.3% | did not produce a valid backtest |
| `GS_screen` | 15,463 | 9.8% | — |
| `ADMITTED` | 3,631 | 2.3% | **cleared every gate** |
| `G3_cpcv_pbo` | 1,753 | 1.1% | parameter tuning overfit (high PBO) |
| `G8_orthogonality` | 147 | 0.1% | duplicates an existing archive member |
| `G2_oos` | 6 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 53298 | 1524 | 2.35 | ██████████████████ |
| `fx` | 53264 | 304 | 0.97 | ███████████······· |
| `xau` | 51903 | 1803 | 0.26 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 137539 | 3631 | 2.35 | ██████████████████ |
| `directional` | 20926 | 0 | -0.10 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 81830 | 3626 | 2.35 | ██████████████████ |
| `llm` | 1314 | 2 | -0.07 | ·················· |
| `random` | 35303 | 0 | -0.10 | ·················· |
| `template` | 28248 | 1 | -0.87 | ·················· |
| `miner` | 11770 | 2 | -1.53 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 52562 | 1614 | 2.35 | ██████████████████ |
| `low_vol` | 29969 | 10 | 0.87 | ██████████········ |
| `trend` | 29521 | 9 | 0.73 | ████████·········· |
| `chop` | 26758 | 1992 | 0.26 | ███··············· |
| `high_vol` | 19655 | 6 | 0.26 | ███··············· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 98811 | 3437 | 2.35 | ██████████████████ |
| `vol_target` | 29185 | 185 | 0.97 | ███████████······· |
| `fixed_fractional` | 13979 | 0 | -0.10 | ·················· |
| `atr_scaled` | 6930 | 0 | -1.32 | ·················· |
| `kelly_fraction` | 9560 | 9 | -1.38 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `volatility` | 31298 | 1820 | 2.35 | ██████████████████ |
| `pattern` | 17281 | 2184 | 2.35 | ██████████████████ |
| `breakout` | 12237 | 1492 | 2.35 | ██████████████████ |
| `microstructure` | 12165 | 1308 | 2.35 | ██████████████████ |
| `liquidity` | 8168 | 1285 | 2.35 | ██████████████████ |
| `trend` | 21402 | 2122 | 1.71 | ██████████████████ |
| `auction_market_theory` | 28263 | 1883 | 1.70 | ██████████████████ |
| `volume` | 14851 | 815 | 1.70 | ██████████████████ |
| `volume_profile` | 7069 | 1194 | 1.63 | ██████████████████ |
| `momentum` | 28010 | 1870 | 1.37 | ███████████████··· |
| `order_flow` | 11152 | 548 | 1.21 | █████████████····· |
| `market_profile` | 9336 | 245 | 1.11 | ████████████······ |
| `statistical` | 26008 | 1302 | 1.09 | ████████████······ |
| `oscillator` | 20277 | 1175 | 1.04 | ███████████······· |
| `macro` | 17424 | 473 | 0.97 | ███████████······· |
| `sentiment` | 8732 | 194 | 0.97 | ███████████······· |
| `ict` | 4317 | 580 | 0.26 | ███··············· |
| `smc` | 4317 | 580 | 0.26 | ███··············· |
| `event` | 3683 | 279 | 0.25 | ███··············· |
| `calendar` | 1759 | 227 | 0.25 | ███··············· |
| `rates` | 5253 | 52 | 0.18 | ██················ |
| `mean_reversion` | 12965 | 292 | -0.07 | ·················· |
| `cross_asset` | 1865 | 5 | -0.07 | ·················· |
| `positioning` | 1934 | 8 | -0.20 | ·················· |
| `persistence` | 3283 | 26 | -0.85 | ·················· |
| `regime` | 5875 | 0 | -1.33 | ·················· |
| `mixed` | 35575 | 0 | -2.42 | ·················· |
| `ml_derived` | 2564 | 0 | -2.45 | ·················· |
| `intermarket` | 1109 | 0 | -2.67 | ·················· |
| `crypto` | 848 | 0 | -3.10 | ·················· |
| `funding` | 848 | 0 | -3.10 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `delta_divergence` | 2 | +6.129 | **carries signal** |
| `intx_28e8ed9a` | 2 | +2.857 | **carries signal** |
| `amihud_illiquidity` | 5772 | +0.896 | **carries signal** |
| `momentum` | 2127 | +0.805 | **carries signal** |
| `atr_expansion` | 4868 | +0.699 | **carries signal** |
| `rotation_factor` | 1495 | +0.596 | **carries signal** |
| `tsmom_blend` | 3104 | +0.521 | **carries signal** |
| `macd` | 2473 | +0.487 | **carries signal** |
| `williams_r` | 2 | +0.436 | **carries signal** |
| `order_block_strength` | 509 | +0.386 | **carries signal** |
| `news_sentiment` | 2173 | +0.327 | **carries signal** |
| `breakout` | 5316 | +0.271 | **carries signal** |
| `fed_repricing` | 137 | +0.224 | **carries signal** |
| `fvg_gap` | 1206 | +0.204 | **carries signal** |
| `adx` | 1484 | +0.186 | **carries signal** |

---

## 5 · Archive (26 niches)

| niche | market | fitness |
|---|---|---:|
| `xau:swing:low:long:chop` | xau | 0.848 |
| `crypto:position:med:neutral:all` | crypto | 0.657 |
| `crypto:position:high:neutral:all` | crypto | 0.596 |
| `xau:swing:low:neutral:chop` | xau | 0.485 |
| `crypto:position:high:neutral:low_vol` | crypto | 0.402 |
| `crypto:position:low:neutral:all` | crypto | 0.352 |
| `fx:position:low:neutral:all` | fx | 0.334 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.297 |
| `crypto:position:med:neutral:trend` | crypto | 0.270 |
| `crypto:position:med:neutral:high_vol` | crypto | 0.263 |
| `crypto:position:med:neutral:chop` | crypto | 0.223 |
| `xau:intraday:low:neutral:chop` | xau | 0.221 |
| `xau:swing:low:long:high_vol` | xau | 0.220 |
| `fx:intraday:low:long:chop` | fx | 0.155 |
| `crypto:swing:med:neutral:all` | crypto | 0.133 |
| `crypto:swing:med:long:chop` | crypto | 0.092 |
| `xau:intraday:low:long:chop` | xau | 0.075 |
| `crypto:swing:low:neutral:all` | crypto | 0.026 |
| `crypto:swing:high:neutral:all` | crypto | -0.016 |
| `xau:intraday:low:neutral:all` | xau | -0.022 |
| `crypto:intraday:low:neutral:all` | crypto | -0.030 |
| `xau:position:low:long:chop` | xau | -0.054 |
| `crypto:swing:med:neutral:low_vol` | crypto | -0.075 |
| `xau:intraday:trade:long:chop` | xau | -0.097 |
| `crypto:intraday:med:neutral:all` | crypto | -0.213 |

## 6 · Lessons library (18,906)

- ×13 — [GS_screen] breakout+macro+momentum+oscillator+pattern+sentiment+statistical+trend+volatility+volume (cross_sectional) — r
- ×10 — [PASS] momentum+oscillator+pattern+statistical+trend+volatility on a cross_sectional book promoted to the candidate p
- ×7 — [PASS] macro+momentum+pattern+sentiment+statistical+trend+volatility+volume on a cross_sectional book promoted to the
- ×6 — [PASS] auction_market_theory+macro+momentum+oscillator+pattern+sentiment+statistical+trend+volume_profile on a cross_
- ×5 — [PASS] auction_market_theory+breakout+liquidity+market_profile+microstructure+pattern+volatility+volume_profile on a 
- ×5 — [GS_screen] liquidity+microstructure (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_singl
- ×5 — [PASS] momentum+oscillator on a cross_sectional book promoted to the candidate pool
- ×4 — [GS_screen] mean_reversion+statistical+volatility (cross_sectional) — raw predictive strength too weak to clear the FDR sc
- ×4 — [PASS] statistical on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] macro+momentum+pattern+sentiment+trend+volatility+volume on a cross_sectional book promoted to the candidate p
- ×4 — [PASS] breakout+liquidity+microstructure+pattern+volatility on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] breakout+liquidity+microstructure+momentum+pattern+trend on a cross_sectional book promoted to the candidate p
- ×4 — [PASS] auction_market_theory+trend+volatility+volume_profile on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] momentum+oscillator+statistical on a cross_sectional book promoted to the candidate pool
- ×4 — [GS_screen] macro+momentum+oscillator+pattern+sentiment+statistical+trend+volatility+volume (cross_sectional) — raw predic

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*