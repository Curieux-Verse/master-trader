# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-24 04:36 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **24,882** |
| Deflated-Sharpe trial count (N) | **54,238** *(evals 35,488 + 18,750 screened)* |
| Admitted to archive | **0** |
| Rejected | **24,882** (100.0%) |
| Distinct families explored | **26** |
| Lessons accumulated | **1,469** |
| Best DSR-z | **+1.272** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 25 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `2e2ca90e42e81cfe` | xau | **1.27** | 1.3198 | 21.84 | 0.000 | cross_sectional | high_vol | `G1_sanity` |
| 2 | `98431349e8c387c1` | fx | **0.54** | 0.5964 | 10.55 | 0.000 | cross_sectional | chop | `G1_sanity` |
| 3 | `879fdd9314ea85c3` | fx | **0.23** | 0.6486 | 11.47 | 0.000 | cross_sectional | chop | `G1_sanity` |
| 4 | `e414adcdbb3e8617` | fx | **0.10** | 0.5334 | 9.43 | 0.002 | cross_sectional | chop | `G4_deflated_sharpe` |
| 5 | `e2449e035c64fdac` | xau | **-0.23** | 0.4546 | 15.04 | 0.002 | cross_sectional | all | `G1_sanity` |
| 6 | `5ce62af05581097d` | fx | **-0.26** | 0.4167 | 7.37 | 0.001 | cross_sectional | chop | `G1_sanity` |
| 7 | `ac994394aeda46eb` | fx | **-0.29** | 0.7510 | 13.28 | 0.000 | cross_sectional | chop | `G1_sanity` |
| 8 | `f9c9dc0720ae5abc` | fx | **-0.54** | 0.1054 | 2.01 | 0.007 | cross_sectional | all | `G4_deflated_sharpe` |
| 9 | `eb7c17be95df5a2a` | fx | **-0.66** | 0.3946 | 9.23 | 0.001 | cross_sectional | chop | `G4_deflated_sharpe` |
| 10 | `a8fc5a8e6af8a1bd` | fx | **-0.67** | 0.3946 | 9.23 | 0.001 | cross_sectional | chop | `G4_deflated_sharpe` |
| 11 | `16ef1cdec82a913b` | xau | **-0.71** | 0.4546 | 15.04 | 0.002 | cross_sectional | all | `G1_sanity` |
| 12 | `a931d42df65895ab` | fx | **-0.78** | 0.1560 | 2.58 | 0.002 | cross_sectional | low_vol | `G1_sanity` |
| 13 | `d83564849b21b185` | fx | **-0.88** | 0.2524 | 2.86 | 0.003 | cross_sectional | low_vol | `G1_sanity` |
| 14 | `258950d1ffec3d76` | fx | **-0.91** | 0.5334 | 9.43 | 0.002 | cross_sectional | chop | `G4_deflated_sharpe` |
| 15 | `54998203c23a7bab` | fx | **-0.91** | 0.5334 | 9.43 | 0.002 | cross_sectional | chop | `G4_deflated_sharpe` |
| 16 | `8c35d732adff54d5` | fx | **-0.94** | 0.3976 | 3.06 | 0.002 | cross_sectional | all | `G1_sanity` |
| 17 | `6107f60d6622af8a` | fx | **-0.98** | 1.2860 | 9.64 | 0.001 | cross_sectional | high_vol | `G1_sanity` |
| 18 | `9c3cccb9be0ed07a` | fx | **-1.10** | 0.3240 | 7.58 | 0.002 | cross_sectional | chop | `G4_deflated_sharpe` |
| 19 | `f9c2618b4b00481a` | fx | **-1.11** | 0.7986 | 7.33 | 0.000 | cross_sectional | low_vol | `G1_sanity` |
| 20 | `883f984137f92a43` | fx | **-1.14** | 0.3976 | 3.06 | 0.002 | cross_sectional | all | `G1_sanity` |
| 21 | `bfe6eea79154df97` | fx | **-1.16** | 0.2018 | 4.22 | 0.004 | cross_sectional | chop | `G4_deflated_sharpe` |
| 22 | `bf9f21c13adac03b` | fx | **-1.17** | 0.2048 | 4.79 | 0.001 | cross_sectional | chop | `G1_sanity` |
| 23 | `82764e4a8d580a2d` | xau | **-1.20** | 0.1677 | 1.67 | 0.365 | directional | low_vol | `G4_deflated_sharpe` |
| 24 | `55912c31faf20e24` | fx | **-1.24** | 0.2107 | 2.97 | 0.004 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 25 | `6f5d46bb872e5298` | xau | **-1.31** | 0.0860 | 1.41 | 0.438 | directional | chop | `G4_deflated_sharpe` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `2e2ca90e42e81cfe` — DSR-z 1.27 · died at `G1_sanity` · families: breakout, ict, pattern, smc, trend**
```
[xau] gated_and (long_bias, regime=high_vol) on H4
  features: order_block_strength(); breakout(window=109); adx(window=36)
  sizing:   rank_bucket(top_frac=0.2919297460151009, gross=1.204018723184618, per_name_cap=0.09124210572221594)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=2e2ca90e42e81cfe  gen=5  by=evo_mutate  nodes=6
```
**#2 · `98431349e8c387c1` — DSR-z 0.54 · died at `G1_sanity` · families: persistence, statistical, volume**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: volume_zscore(window=14); hurst(window=126)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.07072289407683964, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=98431349e8c387c1  gen=7  by=evo_mutate  nodes=5
```
**#3 · `879fdd9314ea85c3` — DSR-z 0.23 · died at `G1_sanity` · families: momentum, oscillator, volume**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=17, slow=37, signal=9); obv(window=33)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.07072289407683964, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=879fdd9314ea85c3  gen=9  by=evo_mutate  nodes=5
```
**#4 · `e414adcdbb3e8617` — DSR-z 0.10 · died at `G4_deflated_sharpe` · families: momentum, oscillator**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=17, slow=37, signal=9)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.05, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=e414adcdbb3e8617  gen=11  by=evo_mutate  nodes=4
```
**#5 · `e2449e035c64fdac` — DSR-z -0.23 · died at `G1_sanity` · families: breakout, ict, pattern, smc, trend**
```
[xau] gated_and (long_bias) on H4
  features: order_block_strength(); breakout(window=109); adx(window=36)
  sizing:   rank_bucket(top_frac=0.2919297460151009, gross=1.3933806431970668, per_name_cap=0.09124210572221594)
  risk:     horizon_hold(horizon=2, cost_stress=1.2774250504091818)
  id=e2449e035c64fdac  gen=0  by=random  nodes=6
```
**#6 · `5ce62af05581097d` — DSR-z -0.26 · died at `G1_sanity` · families: breakout, ict, pattern, smc**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: structure_break(window=8); breakout(window=47)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.12151157999722831, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=5ce62af05581097d  gen=8  by=evo_mutate  nodes=5
```
**#7 · `ac994394aeda46eb` — DSR-z -0.29 · died at `G1_sanity` · families: momentum, oscillator**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=17, slow=37, signal=9); williams_r(window=6)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.07072289407683964, per_name_cap=0.14596563241920293)
  risk:     horizon_hold(horizon=7, cost_stress=1.0428827303327532)
  id=ac994394aeda46eb  gen=14  by=evo_mutate  nodes=5
```
**#8 · `f9c9dc0720ae5abc` — DSR-z -0.54 · died at `G4_deflated_sharpe` · families: statistical**
```
[fx] weighted_blend (neutral) on H4
  features: autocorr(lag=4, window=184)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=6, cost_stress=1.0)
  id=f9c9dc0720ae5abc  gen=0  by=miner  nodes=4
```
**#9 · `eb7c17be95df5a2a` — DSR-z -0.66 · died at `G4_deflated_sharpe` · families: mean_reversion, statistical, volatility**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: price_zscore(window=156); atr_expansion(window=17)
  sizing:   kelly_fraction(kelly_frac=0.6155747612733246, max_leverage=4.4930693941677555, top_frac=0.22411269517993931, gross=1.7412563236316623, per_name_cap=0.06226091096755838)
  risk:     horizon_hold(horizon=4, cost_stress=1.0078728914041917)
  id=eb7c17be95df5a2a  gen=1  by=evo_mutate  nodes=5
```
**#10 · `a8fc5a8e6af8a1bd` — DSR-z -0.67 · died at `G4_deflated_sharpe` · families: mean_reversion, statistical, volatility**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: price_zscore(window=156); atr_expansion(window=17)
  sizing:   kelly_fraction(kelly_frac=0.6573318246740214, max_leverage=4.300029018026736, top_frac=0.22411269517993931, gross=1.7412563236316623, per_name_cap=0.06226091096755838)
  risk:     horizon_hold(horizon=4, cost_stress=1.0078728914041917)
  id=a8fc5a8e6af8a1bd  gen=1  by=evo_mutate  nodes=5
```
**#11 · `16ef1cdec82a913b` — DSR-z -0.71 · died at `G1_sanity` · families: breakout, ict, pattern, smc, trend**
```
[xau] gated_and (long_bias) on H4
  features: order_block_strength(); breakout(window=109); adx(window=36)
  sizing:   rank_bucket(top_frac=0.2919297460151009, gross=1.035477616960832, per_name_cap=0.09124210572221594)
  risk:     horizon_hold(horizon=2, cost_stress=1.2774250504091818)
  id=16ef1cdec82a913b  gen=1  by=evo_mutate  nodes=6
```
**#12 · `a931d42df65895ab` — DSR-z -0.78 · died at `G1_sanity` · families: volume**
```
[fx] gated_or (long_bias, regime=low_vol) on H4
  features: obv(window=35)
  sizing:   vol_target(target_ann_vol=0.32080577477514427, top_frac=0.2544090445555388, per_name_cap=0.13212478016618595)
  risk:     horizon_hold(horizon=8, cost_stress=1.699456305732376)
  id=a931d42df65895ab  gen=0  by=random  nodes=4
```
**#13 · `d83564849b21b185` — DSR-z -0.88 · died at `G1_sanity` · families: statistical**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: autocorr(lag=4, window=184)
  sizing:   rank_bucket(top_frac=0.06604306837922404, gross=1.8287875597839103, per_name_cap=0.1594436678314214)
  risk:     horizon_hold(horizon=17, cost_stress=1.0)
  id=d83564849b21b185  gen=7  by=evo_mutate  nodes=4
```
**#14 · `258950d1ffec3d76` — DSR-z -0.91 · died at `G4_deflated_sharpe` · families: momentum, oscillator**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=17, slow=37, signal=9)
  sizing:   vol_target(target_ann_vol=0.2275491497416184, top_frac=0.05, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=258950d1ffec3d76  gen=12  by=evo_mutate  nodes=4
```
**#15 · `54998203c23a7bab` — DSR-z -0.91 · died at `G4_deflated_sharpe` · families: momentum, oscillator**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=17, slow=37, signal=9)
  sizing:   vol_target(target_ann_vol=0.23014239313709395, top_frac=0.07072289407683964, per_name_cap=0.1432430748406647)
  risk:     horizon_hold(horizon=7, cost_stress=1.1533330926996905)
  id=54998203c23a7bab  gen=8  by=evo_mutate  nodes=4
```
**#16 · `8c35d732adff54d5` — DSR-z -0.94 · died at `G1_sanity` · families: pattern**
```
[fx] weighted_blend (long_bias) on H4
  features: candlestick_pattern(pattern=inside)
  sizing:   vol_target(target_ann_vol=0.2333101236913866, top_frac=0.22257746154144298, per_name_cap=0.08351520052098306)
  risk:     horizon_hold(horizon=37, cost_stress=1.8418649868704366)
  id=8c35d732adff54d5  gen=6  by=evo_crossover  nodes=4
```
**#17 · `6107f60d6622af8a` — DSR-z -0.98 · died at `G1_sanity` · families: statistical**
```
[fx] gated_and (long_bias, regime=high_vol) on H4
  features: autocorr(lag=4, window=184)
  sizing:   vol_target(target_ann_vol=0.256552118550725, top_frac=0.22257746154144298, per_name_cap=0.08351520052098306)
  risk:     horizon_hold(horizon=39, cost_stress=1.8418649868704366)
  id=6107f60d6622af8a  gen=20  by=evo_mutate  nodes=4
```
**#18 · `9c3cccb9be0ed07a` — DSR-z -1.10 · died at `G4_deflated_sharpe` · families: mean_reversion, statistical, volatility**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: price_zscore(window=156); atr_expansion(window=10)
  sizing:   kelly_fraction(kelly_frac=0.798913634022707, max_leverage=4.4930693941677555, top_frac=0.22411269517993931, gross=1.7412563236316623, per_name_cap=0.06226091096755838)
  risk:     horizon_hold(horizon=4, cost_stress=1.0078728914041917)
  id=9c3cccb9be0ed07a  gen=2  by=evo_mutate  nodes=5
```
**#19 · `f9c2618b4b00481a` — DSR-z -1.11 · died at `G1_sanity` · families: breakout, pattern**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: intx_56ca4ba2(); breakout(window=29); intx_05504a39()
  sizing:   vol_target(target_ann_vol=0.32032358127346006, top_frac=0.18966790409371548, per_name_cap=0.052831004770890116)
  risk:     horizon_hold(horizon=26, cost_stress=1.1808098683890738)
  id=f9c2618b4b00481a  gen=2  by=evo_mutate  nodes=6
```
**#20 · `883f984137f92a43` — DSR-z -1.14 · died at `G1_sanity` · families: pattern**
```
[fx] weighted_blend (long_bias) on H4
  features: candlestick_pattern(pattern=inside)
  sizing:   vol_target(target_ann_vol=0.15742364904377587, top_frac=0.22257746154144298, per_name_cap=0.08351520052098306)
  risk:     horizon_hold(horizon=37, cost_stress=1.8418649868704366)
  id=883f984137f92a43  gen=13  by=evo_crossover  nodes=4
```
**#21 · `bfe6eea79154df97` — DSR-z -1.16 · died at `G4_deflated_sharpe` · families: momentum, oscillator**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: macd(fast=12, slow=26, signal=9)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=5, cost_stress=1.0)
  id=bfe6eea79154df97  gen=3  by=evo_mutate  nodes=4
```
**#22 · `bf9f21c13adac03b` — DSR-z -1.17 · died at `G1_sanity` · families: trend**
```
[fx] gated_and (long_bias, regime=chop) on H4
  features: ma_cross(fast=33, slow=53); intx_4d4ac75b()
  sizing:   kelly_fraction(kelly_frac=0.6573318246740214, max_leverage=4.4930693941677555, top_frac=0.22411269517993931, gross=1.7412563236316623, per_name_cap=0.06226091096755838)
  risk:     horizon_hold(horizon=4, cost_stress=1.1372197958791914)
  id=bf9f21c13adac03b  gen=3  by=evo_mutate  nodes=5
```
**#23 · `82764e4a8d580a2d` — DSR-z -1.20 · died at `G4_deflated_sharpe` · families: momentum, oscillator**
```
[xau] gated_and (short_bias, regime=low_vol) on H4
  features: macd(fast=16, slow=34, signal=13)
  sizing:   atr_scaled(atr_mult=2.859659839421881)
  risk:     triple_barrier(entry_thr=0.9855272047727897, sl_mult=2.5715300349362433, tp_mult=4.822049010689032, max_bars=47, cost_stress=1.6395737689775474)
  id=82764e4a8d580a2d  gen=0  by=random  nodes=4
```
**#24 · `55912c31faf20e24` — DSR-z -1.24 · died at `G4_deflated_sharpe` · families: ict, smc**
```
[fx] weighted_blend (long_bias, regime=low_vol) on H4
  features: liquidity_sweep(window=24)
  sizing:   vol_target(target_ann_vol=0.298554404165175, top_frac=0.1259500586833423, per_name_cap=0.10372280595902203)
  risk:     horizon_hold(horizon=11, cost_stress=1.0678494297786747)
  id=55912c31faf20e24  gen=0  by=random  nodes=4
```
**#25 · `6f5d46bb872e5298` — DSR-z -1.31 · died at `G4_deflated_sharpe` · families: trend, volume**
```
[xau] weighted_blend (long_bias, regime=chop) on H4
  features: volume_zscore(window=25); adx(window=11); adx(window=46)
  sizing:   atr_scaled(atr_mult=1.8242140184374653)
  risk:     triple_barrier(entry_thr=0.5613267689828192, sl_mult=2.909529584673182, tp_mult=1.2692406874162594, max_bars=28, cost_stress=1.4981286887151628)
  id=6f5d46bb872e5298  gen=0  by=random  nodes=6
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 15,429 | 62.0% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 6,806 | 27.4% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 2,647 | 10.6% | did not produce a valid backtest |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `xau` | 12216 | 0 | 1.27 | ██████████████···· |
| `fx` | 12666 | 0 | 0.54 | ██████············ |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 21290 | 0 | 1.27 | ██████████████···· |
| `directional` | 3592 | 0 | -1.20 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 12211 | 0 | 1.27 | ██████████████···· |
| `random` | 5742 | 0 | -0.23 | ·················· |
| `miner` | 2437 | 0 | -0.54 | ·················· |
| `template` | 4492 | 0 | -1.33 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `high_vol` | 2869 | 0 | 1.27 | ██████████████···· |
| `chop` | 5301 | 0 | 0.54 | ██████············ |
| `all` | 8197 | 0 | -0.23 | ·················· |
| `low_vol` | 3354 | 0 | -0.78 | ·················· |
| `trend` | 5161 | 0 | -1.33 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 17064 | 0 | 1.27 | ██████████████···· |
| `vol_target` | 1825 | 0 | 0.54 | ██████············ |
| `kelly_fraction` | 2405 | 0 | -0.66 | ·················· |
| `atr_scaled` | 1172 | 0 | -1.20 | ·················· |
| `fixed_fractional` | 2416 | 0 | -2.13 | ·················· |

### 4.6 By strategy family — all 26 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `trend` | 4525 | 0 | 1.27 | ██████████████···· |
| `pattern` | 4377 | 0 | 1.27 | ██████████████···· |
| `breakout` | 3942 | 0 | 1.27 | ██████████████···· |
| `ict` | 3910 | 0 | 1.27 | ██████████████···· |
| `smc` | 3910 | 0 | 1.27 | ██████████████···· |
| `statistical` | 4795 | 0 | 0.54 | ██████············ |
| `volume` | 1608 | 0 | 0.54 | ██████············ |
| `persistence` | 686 | 0 | 0.54 | ██████············ |
| `momentum` | 4697 | 0 | 0.23 | ███··············· |
| `oscillator` | 4496 | 0 | 0.23 | ███··············· |
| `volatility` | 4296 | 0 | -0.66 | ·················· |
| `mean_reversion` | 1639 | 0 | -0.66 | ·················· |
| `auction_market_theory` | 2394 | 0 | -1.33 | ·················· |
| `volume_profile` | 870 | 0 | -1.33 | ·················· |
| `order_flow` | 814 | 0 | -1.33 | ·················· |
| `market_profile` | 687 | 0 | -1.33 | ·················· |
| `mixed` | 4943 | 0 | -1.73 | ·················· |
| `macro` | 715 | 0 | -2.45 | ·················· |
| `positioning` | 139 | 0 | -2.45 | ·················· |
| `cross_asset` | 130 | 0 | -2.55 | ·················· |
| `intermarket` | 130 | 0 | -2.55 | ·················· |
| `sentiment` | 154 | 0 | -2.70 | ·················· |
| `calendar` | 427 | 0 | -3.30 | ·················· |
| `event` | 427 | 0 | -3.30 | ·················· |
| `ml_derived` | 135 | 0 | -3.63 | ·················· |
| `regime` | 135 | 0 | -3.63 | ·················· |

---

## 5 · Archive (0 niches)

*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*

## 6 · Lessons library (1,469)

- ×1 — [G1_sanity] interaction+intx_75f06f75+intx_ababbe5b+mined+volatility (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] auction_market_theory+ict+oscillator+smc+volume_profile (cross_sectional) — degenerate or too few trades
- ×1 — [G0_eval] interaction+intx_329bb2d8+intx_75788444+intx_7914bacd+intx_8cbb1c71+mined+volatility (cross_sectional) — did n
- ×1 — [G0_eval] breakout+ict+interaction+intx_75788444+intx_dc41da51+mined+pattern+smc+statistical+trend (cross_sectional) — d
- ×1 — [G1_sanity] cci+interaction+intx_84f0ed00+mean_reversion+mined+statistical+volatility (cross_sectional) — degenerate or to
- ×1 — [G4_deflated_sharpe] interaction+intx_f7b593db+mined+variance_ratio (cross_sectional) — edge indistinguishable from luck after tria
- ×1 — [G4_deflated_sharpe] interaction+intx_a7d08786+intx_f9b6cfe6+mined+momentum+trend (directional) — edge indistinguishable from luck 
- ×1 — [G1_sanity] hurst+interaction+intx_0c6d78df+mined+pattern (cross_sectional) — degenerate or too few trades
- ×1 — [G0_eval] interaction+intx_56ca4ba2+intx_74e8f45e+intx_75788444+intx_8cbb1c71+intx_9cb1dcaa+mined+realized_vol (cross_se
- ×1 — [G1_sanity] interaction+intx_af44e407+intx_d2abaaa2+mined (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] interaction+intx_489542c2+intx_4d4ac75b+intx_811d244c+intx_95714be5+mined (cross_sectional) — degenerate or to
- ×1 — [G4_deflated_sharpe] interaction+intx_0c6d78df+intx_df14f57a+intx_f9b6cfe6+macd+mined+value_area_position+williams_r (cross_section
- ×1 — [G1_sanity] atr_pct+interaction+intx_9cb1dcaa+mined+momentum+oscillator (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] interaction+intx_489542c2+intx_811d244c+mined (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] macro+ml_derived+positioning+regime (directional) — edge indistinguishable from luck after trial correction

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*