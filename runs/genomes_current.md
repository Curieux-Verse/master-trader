# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-24 09:44 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **28,453** |
| Deflated-Sharpe trial count (N) | **85,636** *(evals 56,030 + 29,606 screened)* |
| Admitted to archive | **0** |
| Rejected | **28,453** (100.0%) |
| Distinct families explored | **29** |
| Lessons accumulated | **1,594** |
| Best DSR-z | **+0.878** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `095e9e792d801987` | crypto | **0.88** | 0.4529 | 3.09 | 0.058 | cross_sectional | all | `G4_deflated_sharpe` |
| 2 | `41807f4b7abf7276` | crypto | **0.77** | 0.4315 | 2.95 | 0.042 | cross_sectional | all | `G4_deflated_sharpe` |
| 3 | `1d10a75cdd7ec411` | crypto | **0.76** | 0.5572 | 3.80 | 0.035 | cross_sectional | all | `G4_deflated_sharpe` |
| 4 | `5a9d333510aa56e2` | crypto | **0.74** | 0.3999 | 2.73 | 0.044 | cross_sectional | all | `G4_deflated_sharpe` |
| 5 | `fe6a2e669df48420` | crypto | **0.65** | 0.4315 | 2.95 | 0.042 | cross_sectional | all | `G4_deflated_sharpe` |
| 6 | `252c276825939106` | crypto | **0.56** | 0.4503 | 3.07 | 0.053 | cross_sectional | all | `G4_deflated_sharpe` |
| 7 | `08b43a8632c3ba89` | crypto | **0.55** | 0.4315 | 2.95 | 0.042 | cross_sectional | all | `G4_deflated_sharpe` |
| 8 | `90fb7bd8c883b6b7` | crypto | **0.51** | 0.4976 | 5.65 | 0.005 | cross_sectional | trend | `G1_sanity` |
| 9 | `204155540db75dd3` | crypto | **0.30** | 0.4306 | 2.94 | 0.062 | cross_sectional | all | `G4_deflated_sharpe` |
| 10 | `d480d0f51dea6782` | crypto | **0.20** | 0.4328 | 2.95 | 0.033 | cross_sectional | all | `G4_deflated_sharpe` |
| 11 | `6ef132c837e5e1b0` | crypto | **0.06** | 0.5572 | 3.80 | 0.035 | cross_sectional | all | `G4_deflated_sharpe` |
| 12 | `9fd814278a2f4dec` | crypto | **0.06** | 0.4326 | 2.95 | 0.053 | cross_sectional | all | `G4_deflated_sharpe` |
| 13 | `58b81da46c63fa26` | crypto | **0.03** | 0.3047 | 2.38 | 0.262 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 14 | `ebe79fe71d097fef` | crypto | **-0.07** | 0.5477 | 3.74 | 0.025 | cross_sectional | all | `G4_deflated_sharpe` |
| 15 | `790cffb06750b808` | crypto | **-0.07** | 0.3558 | 2.43 | 0.031 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 16 | `4bd4828f55ecfabd` | crypto | **-0.07** | 0.3971 | 2.71 | 0.044 | cross_sectional | all | `G4_deflated_sharpe` |
| 17 | `7192752f098897e9` | crypto | **-0.11** | 0.3913 | 2.67 | 0.044 | cross_sectional | all | `G4_deflated_sharpe` |
| 18 | `005f2710858c1cd8` | crypto | **-0.14** | 0.5031 | 3.43 | 0.037 | cross_sectional | all | `G4_deflated_sharpe` |
| 19 | `d0297eda88e76f31` | crypto | **-0.15** | 0.4179 | 2.85 | 0.053 | cross_sectional | all | `G4_deflated_sharpe` |
| 20 | `fc59ed084cb3d399` | crypto | **-0.30** | 0.2676 | 1.83 | 0.031 | cross_sectional | low_vol | `G4_deflated_sharpe` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `095e9e792d801987` — DSR-z 0.88 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8142971844026982, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=095e9e792d801987  gen=6  by=evo_mutate  nodes=5
```
**#2 · `41807f4b7abf7276` — DSR-z 0.77 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=41807f4b7abf7276  gen=5  by=evo_mutate  nodes=5
```
**#3 · `1d10a75cdd7ec411` — DSR-z 0.76 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (long_bias) on 4h
  features: intx_9484f370(); sma_dist(window=51)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8142971844026982, per_name_cap=0.02)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=1d10a75cdd7ec411  gen=12  by=evo_mutate  nodes=5
```
**#4 · `5a9d333510aa56e2` — DSR-z 0.74 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: stoch(window=32)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=5a9d333510aa56e2  gen=0  by=random  nodes=4
```
**#5 · `fe6a2e669df48420` — DSR-z 0.65 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (neutral) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=fe6a2e669df48420  gen=6  by=evo_mutate  nodes=5
```
**#6 · `252c276825939106` — DSR-z 0.56 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (neutral) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.7461942915028619, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=252c276825939106  gen=7  by=evo_mutate  nodes=5
```
**#7 · `08b43a8632c3ba89` — DSR-z 0.55 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (neutral) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=08b43a8632c3ba89  gen=9  by=evo_crossover  nodes=5
```
**#8 · `90fb7bd8c883b6b7` — DSR-z 0.51 · died at `G1_sanity` · families: auction_market_theory, microstructure, order_flow**
```
[crypto] gated_and (short_bias, regime=trend) on 4h
  features: intx_ed7e0d30(); aggressor_ratio(window=62)
  sizing:   vol_target(target_ann_vol=0.06536386631794155, top_frac=0.19681159606613513, per_name_cap=0.08189515638351134)
  risk:     horizon_hold(horizon=17, cost_stress=1.622099689647165)
  id=90fb7bd8c883b6b7  gen=1  by=evo_mutate  nodes=5
```
**#9 · `204155540db75dd3` — DSR-z 0.30 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] weighted_blend (neutral) on 4h
  features: value_area_position(window=160); cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.7461942915028619, per_name_cap=0.07826297839616754)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=204155540db75dd3  gen=8  by=evo_mutate  nodes=5
```
**#10 · `d480d0f51dea6782` — DSR-z 0.20 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: stoch(window=32)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.03617004460348221)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=d480d0f51dea6782  gen=1  by=evo_mutate  nodes=4
```
**#11 · `6ef132c837e5e1b0` — DSR-z 0.06 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: intx_9484f370(); sma_dist(window=51)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8142971844026982, per_name_cap=0.02)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=6ef132c837e5e1b0  gen=14  by=evo_crossover  nodes=5
```
**#12 · `9fd814278a2f4dec` — DSR-z 0.06 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: stoch(window=32)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8142971844026982, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.9110708743108724)
  id=9fd814278a2f4dec  gen=10  by=evo_mutate  nodes=4
```
**#13 · `58b81da46c63fa26` — DSR-z 0.03 · died at `G4_deflated_sharpe` · families: macro, positioning, trend**
```
[crypto] weighted_blend (long_bias, regime=low_vol) on 4h
  features: cot_zscore(window=14); slope(window=22)
  sizing:   rank_bucket(top_frac=0.12912108396145083, gross=1.652500223569648, per_name_cap=0.1833077589149296)
  risk:     horizon_hold(horizon=36, cost_stress=1.591788816720003)
  id=58b81da46c63fa26  gen=0  by=random  nodes=5
```
**#14 · `ebe79fe71d097fef` — DSR-z -0.07 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: sma_dist(window=51)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8142971844026982, per_name_cap=0.02)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=ebe79fe71d097fef  gen=17  by=evo_mutate  nodes=4
```
**#15 · `790cffb06750b808` — DSR-z -0.07 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, oscillator**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: stoch(window=46); value_area_position(window=104)
  sizing:   vol_target(target_ann_vol=0.11028235786754201, top_frac=0.25410145991133576, per_name_cap=0.03182153790149175)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=790cffb06750b808  gen=6  by=evo_mutate  nodes=5
```
**#16 · `4bd4828f55ecfabd` — DSR-z -0.07 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: stoch(window=32)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=4bd4828f55ecfabd  gen=1  by=evo_mutate  nodes=4
```
**#17 · `7192752f098897e9` — DSR-z -0.11 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: stoch(window=32)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=2.0)
  id=7192752f098897e9  gen=1  by=evo_mutate  nodes=4
```
**#18 · `005f2710858c1cd8` — DSR-z -0.14 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias) on 4h
  features: cci(window=73)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.8209565475302393, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=005f2710858c1cd8  gen=11  by=evo_mutate  nodes=4
```
**#19 · `d0297eda88e76f31` — DSR-z -0.15 · died at `G4_deflated_sharpe` · families: trend, volatility**
```
[crypto] weighted_blend (long_bias) on 4h
  features: intx_9484f370(); sma_dist(window=51); atr_expansion(window=193)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.03617004460348221)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=d0297eda88e76f31  gen=14  by=evo_mutate  nodes=6
```
**#20 · `fc59ed084cb3d399` — DSR-z -0.30 · died at `G4_deflated_sharpe` · families: oscillator**
```
[crypto] weighted_blend (long_bias, regime=low_vol) on 4h
  features: stoch(window=35)
  sizing:   rank_bucket(top_frac=0.24367176087697412, gross=0.5131672689664204, per_name_cap=0.053123450593053526)
  risk:     horizon_hold(horizon=47, cost_stress=1.834832613529229)
  id=fc59ed084cb3d399  gen=2  by=evo_mutate  nodes=4
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 18,238 | 64.1% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 7,316 | 25.7% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 2,898 | 10.2% | did not produce a valid backtest |
| `—` | 1 | 0.0% | — |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 1299 | 0 | 0.88 | ██████████········ |
| `xau` | 13332 | 0 | -184.90 | ·················· |
| `fx` | 13822 | 0 | -224.47 | ·················· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 24391 | 0 | 0.88 | ██████████········ |
| `directional` | 4062 | 0 | -2.29 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 13843 | 0 | 0.88 | ██████████········ |
| `random` | 6518 | 0 | 0.74 | ████████·········· |
| `template` | 5053 | 0 | -0.72 | ·················· |
| `miner` | 3039 | 0 | -1.52 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 9912 | 0 | 0.88 | ██████████········ |
| `trend` | 5585 | 0 | 0.51 | ██████············ |
| `low_vol` | 3823 | 0 | 0.03 | ·················· |
| `high_vol` | 3314 | 0 | -0.72 | ·················· |
| `chop` | 5819 | 0 | -1.17 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 19479 | 0 | 0.88 | ██████████········ |
| `vol_target` | 2262 | 0 | 0.51 | ██████············ |
| `kelly_fraction` | 2646 | 0 | -1.31 | ·················· |
| `atr_scaled` | 1325 | 0 | -2.29 | ·················· |
| `fixed_fractional` | 2741 | 0 | -3.04 | ·················· |

### 4.6 By strategy family — all 29 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `oscillator` | 5054 | 0 | 0.88 | ██████████········ |
| `auction_market_theory` | 3020 | 0 | 0.88 | ██████████········ |
| `market_profile` | 886 | 0 | 0.88 | ██████████········ |
| `trend` | 5076 | 0 | 0.76 | ████████·········· |
| `order_flow` | 1062 | 0 | 0.51 | ██████············ |
| `microstructure` | 137 | 0 | 0.51 | ██████············ |
| `macro` | 885 | 0 | 0.03 | ·················· |
| `positioning` | 193 | 0 | 0.03 | ·················· |
| `volatility` | 5001 | 0 | -0.15 | ·················· |
| `pattern` | 4793 | 0 | -0.72 | ·················· |
| `breakout` | 4199 | 0 | -0.72 | ·················· |
| `volume` | 1981 | 0 | -0.96 | ·················· |
| `calendar` | 497 | 0 | -0.96 | ·················· |
| `event` | 497 | 0 | -0.96 | ·················· |
| `statistical` | 5345 | 0 | -0.97 | ·················· |
| `volume_profile` | 1069 | 0 | -1.14 | ·················· |
| `momentum` | 5289 | 0 | -1.21 | ·················· |
| `mean_reversion` | 1798 | 0 | -1.31 | ·················· |
| `crypto` | 45 | 0 | -1.31 | ·················· |
| `funding` | 45 | 0 | -1.31 | ·················· |
| `ict` | 4259 | 0 | -1.71 | ·················· |
| `smc` | 4259 | 0 | -1.71 | ·················· |
| `ml_derived` | 203 | 0 | -1.98 | ·················· |
| `regime` | 203 | 0 | -1.98 | ·················· |
| `cross_asset` | 183 | 0 | -2.02 | ·················· |
| `intermarket` | 183 | 0 | -2.02 | ·················· |
| `sentiment` | 201 | 0 | -2.03 | ·················· |
| `mixed` | 5135 | 0 | -2.14 | ·················· |
| `persistence` | 772 | 0 | -2.17 | ·················· |

---

## 5 · Archive (0 niches)

*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*

## 6 · Lessons library (1,594)

- ×1 — [G4_deflated_sharpe] auction_market_theory+ema_dist+interaction+macd+mined+order_flow (directional) — edge indistinguishable from l
- ×1 — [G1_sanity] interaction+mined+realized_vol+trend+variance_ratio (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] ema_dist+interaction+macd+mean_reversion+mined (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] interaction+intx_d1eaed84+intx_ed7e0d30+mined+price_zscore+stoch+trend (cross_sectional) — edge indistinguisha
- ×1 — [G4_deflated_sharpe] ema_dist+interaction+macd+mined+volume (cross_sectional) — edge indistinguishable from luck after trial correc
- ×1 — [G4_deflated_sharpe] auction_market_theory+microstructure (directional) — edge indistinguishable from luck after trial correction
- ×1 — [G1_sanity] interaction+intx_2b43a6c9+mined+structure_break (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] breakout+ict+interaction+intx_ed7e0d30+mined+pattern+smc+stoch (cross_sectional) — edge indistinguishable from
- ×1 — [G4_deflated_sharpe] breakout+interaction+mined+pattern+realized_vol+variance_ratio (directional) — edge indistinguishable from luc
- ×1 — [G1_sanity] ema_dist+interaction+macd+mined+ml_derived+regime+statistical (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] ema_dist+interaction+intx_7e0dea0f+mined+realized_vol+variance_ratio (cross_sectional) — degenerate or too few
- ×1 — [G4_deflated_sharpe] interaction+microstructure+mined+order_flow+realized_vol+variance_ratio (cross_sectional) — edge indistinguish
- ×1 — [G1_sanity] oscillator+volume (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] interaction+mined+sma_dist+vol_of_vol (directional) — edge indistinguishable from luck after trial correction
- ×1 — [G4_deflated_sharpe] cross_asset+ema_dist+interaction+intermarket+intx_7e0dea0f+mined+volatility (cross_sectional) — edge indisting

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*