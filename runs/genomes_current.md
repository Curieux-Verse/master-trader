# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-27 14:02 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **115,328** |
| Deflated-Sharpe trial count (raw N) | **283,393** *(evals 185,424 + 97,969 screened)* |
| **Effective** independent trials (N_eff) | **540** *(ρ̄=0.0018486934978747178 — the bar the DSR actually uses)* |
| Admitted to archive | **0** |
| Rejected | **115,328** (100.0%) |
| Distinct families explored | **31** |
| Lessons accumulated | **6,951** |
| Best DSR-z | **+1.093** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `52702f9fc2f14605` | crypto | **1.09** | 0.4498 | 4.59 | 0.025 | cross_sectional | all | `G4_deflated_sharpe` |
| 2 | `36d9f954dca0d83a` | crypto | **0.43** | 0.3876 | 4.85 | 0.034 | cross_sectional | trend | `G4_deflated_sharpe` |
| 3 | `939e4c1831b9203d` | fx | **-0.00** | 0.3210 | 2.29 | 0.004 | cross_sectional | all | `G4_deflated_sharpe` |
| 4 | `bfd937441caac98b` | fx | **-0.10** | 0.3011 | 4.53 | 0.014 | directional | low_vol | `G4_deflated_sharpe` |
| 5 | `7a08185ab1583242` | crypto | **-0.45** | 0.2872 | 3.59 | 0.018 | cross_sectional | all | `G4_deflated_sharpe` |
| 6 | `6a10cb27be3c816e` | crypto | **-0.65** | 0.2365 | 1.60 | 0.285 | cross_sectional | all | `G4_deflated_sharpe` |
| 7 | `6cb81bdd8b97e983` | xau | **-0.78** | 0.2655 | 3.75 | 0.026 | cross_sectional | trend | `G4_deflated_sharpe` |
| 8 | `bd700d5a382c9f29` | xau | **-0.81** | 0.2955 | 4.89 | 0.021 | cross_sectional | trend | `G4_deflated_sharpe` |
| 9 | `94ac92ba3cf7ce9a` | fx | **-0.85** | 0.1883 | 1.97 | 0.009 | cross_sectional | all | `G4_deflated_sharpe` |
| 10 | `34271b4b9fa507c6` | fx | **-0.87** | 0.0829 | 1.23 | 0.003 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 11 | `ea54d8b480042ce4` | xau | **-0.95** | 0.2582 | 4.27 | 0.012 | cross_sectional | high_vol | `G4_deflated_sharpe` |
| 12 | `139ef8f4f9adeaf9` | crypto | **-0.98** | -0.0230 | -0.36 | 0.034 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 13 | `b3e4b8b5fdb0e19e` | fx | **-1.00** | 0.1726 | 2.33 | 0.009 | cross_sectional | low_vol | `G4_deflated_sharpe` |
| 14 | `19bcfe0b80881caa` | crypto | **-1.02** | 0.2179 | 2.47 | 0.232 | cross_sectional | all | `G4_deflated_sharpe` |
| 15 | `e008a006979de73f` | crypto | **-1.04** | 0.1195 | 1.77 | 0.243 | cross_sectional | all | `G4_deflated_sharpe` |
| 16 | `d29065d4ece3b433` | crypto | **-1.07** | 0.2215 | 2.51 | 0.232 | cross_sectional | all | `G4_deflated_sharpe` |
| 17 | `e75de6d651160e99` | xau | **-1.08** | 0.3290 | 4.77 | 0.231 | directional | high_vol | `G4_deflated_sharpe` |
| 18 | `d6b54344a0822f6c` | fx | **-1.11** | 0.1078 | 0.74 | 0.006 | cross_sectional | all | `G4_deflated_sharpe` |
| 19 | `803dac91c7a1ffa8` | crypto | **-1.15** | 0.0682 | 0.70 | 0.093 | cross_sectional | chop | `G4_deflated_sharpe` |
| 20 | `271f5fbd7a589233` | crypto | **-1.17** | 0.1180 | 1.84 | 0.148 | cross_sectional | chop | `G4_deflated_sharpe` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `52702f9fc2f14605` — DSR-z 1.09 · died at `G4_deflated_sharpe` · families: auction_market_theory, statistical**
```
[crypto] gated_and (long_bias) on 4h
  features: rolling_kurt(window=71); rotation_factor(window=31)
  sizing:   rank_bucket(top_frac=0.2159875356881487, gross=1.5820119993219797, per_name_cap=0.07789291227666356)
  risk:     horizon_hold(horizon=21, cost_stress=1.6320938700249077)
  id=52702f9fc2f14605  gen=3  by=evo_mutate  nodes=5
```
**#2 · `36d9f954dca0d83a` — DSR-z 0.43 · died at `G4_deflated_sharpe` · families: calendar, event, macro, volatility, volume**
```
[crypto] gated_and (short_bias, regime=trend) on 4h
  features: obv(window=34); cesi_surprise(window=26); range_vol(window=42)
  sizing:   vol_target(target_ann_vol=0.13987297876382396, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=36d9f954dca0d83a  gen=5  by=evo_mutate  nodes=6
```
**#3 · `939e4c1831b9203d` — DSR-z -0.00 · died at `G4_deflated_sharpe` · families: macro, mean_reversion, positioning, statistical**
```
[fx] weighted_blend (long_bias) on H4
  features: cot_index(window=7); mean_reversion_halflife(window=23)
  sizing:   kelly_fraction(kelly_frac=0.35288141119085553, max_leverage=2.991053424485564, top_frac=0.1711302888078569, gross=1.296064831524862, per_name_cap=0.04649308290159507)
  risk:     horizon_hold(horizon=43, cost_stress=1.072342218882366)
  id=939e4c1831b9203d  gen=2  by=evo_mutate  nodes=5
```
**#4 · `bfd937441caac98b` — DSR-z -0.10 · died at `G4_deflated_sharpe` · families: auction_market_theory, breakout, market_profile, pattern, volatility**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: realized_vol(window=66); breakout(window=15); value_area_position(window=25)
  sizing:   fixed_fractional(f=0.061306406715798636)
  risk:     triple_barrier(entry_thr=0.6557941688966837, sl_mult=2.6633774947616438, tp_mult=3.732239271917572, max_bars=16, cost_stress=1.3334322802286227)
  id=bfd937441caac98b  gen=0  by=random  nodes=6
```
**#5 · `7a08185ab1583242` — DSR-z -0.45 · died at `G4_deflated_sharpe` · families: calendar, event, macro, trend, volume**
```
[crypto] gated_and (long_bias) on 4h
  features: obv(window=34); cesi_surprise(window=26); ma_cross(fast=20, slow=185)
  sizing:   vol_target(target_ann_vol=0.14253913331184145, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=7a08185ab1583242  gen=1  by=evo_mutate  nodes=6
```
**#6 · `6a10cb27be3c816e` — DSR-z -0.65 · died at `G4_deflated_sharpe` · families: volatility**
```
[crypto] gated_or (long_bias) on 4h
  features: bb_position(window=19, mult=1.824268544576922)
  sizing:   kelly_fraction(kelly_frac=0.7017885073579699, max_leverage=4.864670761728196, top_frac=0.16035288259389402, gross=1.2468186870025852, per_name_cap=0.1917504326857068)
  risk:     horizon_hold(horizon=48, cost_stress=1.2989442673410005)
  id=6a10cb27be3c816e  gen=0  by=random  nodes=4
```
**#7 · `6cb81bdd8b97e983` — DSR-z -0.78 · died at `G4_deflated_sharpe` · families: momentum, oscillator, volatility**
```
[xau] gated_and (long_bias, regime=trend) on H4
  features: atr_expansion(window=63); macd(fast=10, slow=59, signal=16)
  sizing:   rank_bucket(top_frac=0.22, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=11, cost_stress=1.0)
  id=6cb81bdd8b97e983  gen=1  by=evo_mutate  nodes=5
```
**#8 · `bd700d5a382c9f29` — DSR-z -0.81 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[xau] gated_and (long_bias, regime=trend) on H4
  features: atr_expansion(window=71); breakout(window=46)
  sizing:   rank_bucket(top_frac=0.15, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=bd700d5a382c9f29  gen=2  by=evo_mutate  nodes=5
```
**#9 · `94ac92ba3cf7ce9a` — DSR-z -0.85 · died at `G4_deflated_sharpe` · families: statistical**
```
[fx] gated_and (long_bias) on H4
  features: autocorr(lag=6, window=91)
  sizing:   rank_bucket(top_frac=0.2, gross=1.1373937916998094, per_name_cap=0.15519042777345052)
  risk:     horizon_hold(horizon=20, cost_stress=1.0)
  id=94ac92ba3cf7ce9a  gen=10  by=evo_mutate  nodes=4
```
**#10 · `34271b4b9fa507c6` — DSR-z -0.87 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: breakout(window=72); atr_expansion(window=21)
  sizing:   rank_bucket(top_frac=0.18, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=10, cost_stress=1.0)
  id=34271b4b9fa507c6  gen=0  by=template:breakout  nodes=5
```
**#11 · `ea54d8b480042ce4` — DSR-z -0.95 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[xau] gated_and (long_bias, regime=high_vol) on H4
  features: atr_expansion(window=71); breakout(window=46)
  sizing:   rank_bucket(top_frac=0.13084176860234142, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=ea54d8b480042ce4  gen=1  by=evo_mutate  nodes=5
```
**#12 · `139ef8f4f9adeaf9` — DSR-z -0.98 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[crypto] gated_and (long_bias, regime=low_vol) on 4h
  features: breakout(window=76); atr_expansion(window=20)
  sizing:   vol_target(target_ann_vol=0.10617591155464799, top_frac=0.2698092645445984, per_name_cap=0.05626721661929569)
  risk:     horizon_hold(horizon=9, cost_stress=1.0)
  id=139ef8f4f9adeaf9  gen=2  by=evo_crossover  nodes=5
```
**#13 · `b3e4b8b5fdb0e19e` — DSR-z -1.00 · died at `G4_deflated_sharpe` · families: trend**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: ma_cross(fast=18, slow=15)
  sizing:   vol_target(target_ann_vol=0.2584554834126489, top_frac=0.14894736905863326, per_name_cap=0.05309815073019125)
  risk:     horizon_hold(horizon=12, cost_stress=1.0)
  id=b3e4b8b5fdb0e19e  gen=5  by=evo_crossover  nodes=4
```
**#14 · `19bcfe0b80881caa` — DSR-z -1.02 · died at `G4_deflated_sharpe` · families: momentum, trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: tsmom_blend(short=8, med=153, long=184)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0028499629190382, per_name_cap=0.15)
  risk:     horizon_hold(horizon=17, cost_stress=1.0)
  id=19bcfe0b80881caa  gen=2  by=evo_mutate  nodes=4
```
**#15 · `e008a006979de73f` — DSR-z -1.04 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: sma_dist(window=126)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=10, cost_stress=1.5541021393093686)
  id=e008a006979de73f  gen=5  by=evo_crossover  nodes=4
```
**#16 · `d29065d4ece3b433` — DSR-z -1.07 · died at `G4_deflated_sharpe` · families: momentum, trend**
```
[crypto] weighted_blend (neutral) on 4h
  features: tsmom_blend(short=8, med=153, long=184)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0028499629190382, per_name_cap=0.1786815960381712)
  risk:     horizon_hold(horizon=17, cost_stress=1.0)
  id=d29065d4ece3b433  gen=3  by=evo_mutate  nodes=4
```
**#17 · `e75de6d651160e99` — DSR-z -1.08 · died at `G4_deflated_sharpe` · families: auction_market_theory, momentum, trend, volume_profile**
```
[xau] weighted_blend (long_bias, regime=high_vol) on H4
  features: tsmom_blend(short=6, med=33, long=194); poc_distance_real(window=123, levels=12)
  sizing:   fixed_fractional(f=0.2176450279140734)
  risk:     triple_barrier(entry_thr=0.5751215520275685, sl_mult=1.095959632864601, tp_mult=4.259961589399703, max_bars=34, cost_stress=1.224332824705363)
  id=e75de6d651160e99  gen=0  by=random  nodes=5
```
**#18 · `d6b54344a0822f6c` — DSR-z -1.11 · died at `G4_deflated_sharpe` · families: auction_market_theory, oscillator**
```
[fx] gated_or (long_bias) on H4
  features: intx_e0e9215c(); rotation_factor(window=44); cci(window=89)
  sizing:   rank_bucket(top_frac=0.24103323556321582, gross=0.958011489402528, per_name_cap=0.15149712926154243)
  risk:     horizon_hold(horizon=46, cost_stress=1.9231863125377213)
  id=d6b54344a0822f6c  gen=0  by=random  nodes=6
```
**#19 · `803dac91c7a1ffa8` — DSR-z -1.15 · died at `G4_deflated_sharpe` · families: auction_market_theory, volatility**
```
[crypto] gated_and (short_bias, regime=chop) on 4h
  features: realized_vol(window=14); rotation_factor(window=21)
  sizing:   rank_bucket(top_frac=0.2159875356881487, gross=1.5820119993219797, per_name_cap=0.07463769819903499)
  risk:     horizon_hold(horizon=21, cost_stress=1.6320938700249077)
  id=803dac91c7a1ffa8  gen=1  by=evo_mutate  nodes=5
```
**#20 · `271f5fbd7a589233` — DSR-z -1.17 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[crypto] gated_and (long_bias, regime=chop) on 4h
  features: breakout(window=69); atr_expansion(window=20)
  sizing:   rank_bucket(top_frac=0.14, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=9, cost_stress=1.0)
  id=271f5fbd7a589233  gen=1  by=evo_mutate  nodes=5
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 63,344 | 54.9% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 35,455 | 30.7% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 16,529 | 14.3% | did not produce a valid backtest |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 38629 | 0 | 1.09 | ████████████······ |
| `fx` | 39090 | 0 | -0.00 | ·················· |
| `xau` | 37609 | 0 | -0.78 | ·················· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 97828 | 0 | 1.09 | ████████████······ |
| `directional` | 17500 | 0 | -0.10 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 52701 | 0 | 1.09 | ████████████······ |
| `random` | 29759 | 0 | -0.10 | ·················· |
| `template` | 23563 | 0 | -0.87 | ·················· |
| `miner` | 9305 | 0 | -1.53 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 35247 | 0 | 1.09 | ████████████······ |
| `trend` | 25108 | 0 | 0.43 | █████············· |
| `low_vol` | 24895 | 0 | -0.10 | ·················· |
| `high_vol` | 16549 | 0 | -0.95 | ·················· |
| `chop` | 13529 | 0 | -1.15 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 70968 | 0 | 1.09 | ████████████······ |
| `vol_target` | 19476 | 0 | 0.43 | █████············· |
| `kelly_fraction` | 7386 | 0 | -0.00 | ·················· |
| `fixed_fractional` | 11636 | 0 | -0.10 | ·················· |
| `atr_scaled` | 5862 | 0 | -2.32 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `statistical` | 17430 | 0 | 1.09 | ████████████······ |
| `auction_market_theory` | 17400 | 0 | 1.09 | ████████████······ |
| `volatility` | 19151 | 0 | 0.43 | █████············· |
| `macro` | 10848 | 0 | 0.43 | █████············· |
| `volume` | 8803 | 0 | 0.43 | █████············· |
| `event` | 1883 | 0 | 0.43 | █████············· |
| `calendar` | 884 | 0 | 0.43 | █████············· |
| `mean_reversion` | 10629 | 0 | -0.00 | ·················· |
| `positioning` | 1469 | 0 | -0.00 | ·················· |
| `pattern` | 7803 | 0 | -0.10 | ·················· |
| `market_profile` | 7094 | 0 | -0.10 | ·················· |
| `breakout` | 6372 | 0 | -0.10 | ·················· |
| `trend` | 9505 | 0 | -0.45 | ·················· |
| `momentum` | 14287 | 0 | -0.78 | ·················· |
| `oscillator` | 10510 | 0 | -0.78 | ·················· |
| `volume_profile` | 3105 | 0 | -1.08 | ·················· |
| `regime` | 4628 | 0 | -1.33 | ·················· |
| `rates` | 4161 | 0 | -1.33 | ·················· |
| `microstructure` | 5915 | 0 | -1.35 | ·················· |
| `ml_derived` | 1473 | 0 | -1.35 | ·················· |
| `order_flow` | 7719 | 0 | -1.54 | ·················· |
| `persistence` | 2529 | 0 | -1.59 | ·················· |
| `ict` | 1903 | 0 | -1.67 | ·················· |
| `smc` | 1903 | 0 | -1.67 | ·················· |
| `liquidity` | 2598 | 0 | -1.94 | ·················· |
| `sentiment` | 4473 | 0 | -2.12 | ·················· |
| `mixed` | 33220 | 0 | -2.42 | ·················· |
| `cross_asset` | 1259 | 0 | -2.67 | ·················· |
| `intermarket` | 807 | 0 | -2.67 | ·················· |
| `crypto` | 746 | 0 | -3.10 | ·················· |
| `funding` | 746 | 0 | -3.10 | ·················· |

---
---

## 5 · Archive (0 niches)

*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*

## 6 · Lessons library (6,951)

- ×1 — [G4_deflated_sharpe] auction_market_theory+cci+interaction+market_profile+mined+order_block_strength+order_flow+volume_profile (cro
- ×1 — [G1_sanity] interaction+intx_f6adbb90+intx_f7747515+mined (cross_sectional) — degenerate or too few trades
- ×1 — [G1_sanity] interaction+intx_68931c03+intx_fc94f5be+macro+mined+sentiment (cross_sectional) — degenerate or too few trades
- ×1 — [G4_deflated_sharpe] atr_pct+fvg_gap+interaction+intx_276c7415+intx_73f6ed76+intx_96c8aab4+intx_f9b6ac5a+mined (cross_sectional) — 
- ×1 — [G4_deflated_sharpe] interaction+intx_6affe237+intx_ffecaa50+mined (cross_sectional) — edge indistinguishable from luck after trial
- ×1 — [G1_sanity] interaction+intx_b4431afc+intx_c202425b+mined (cross_sectional) — degenerate or too few trades
- ×1 — [G0_eval] interaction+intx_6420cf41+intx_8ed6b659+mined (cross_sectional) — did not produce a valid backtest
- ×1 — [G4_deflated_sharpe] interaction+intx_21424c7d+mined+trend+tsmom_blend (cross_sectional) — edge indistinguishable from luck after t
- ×1 — [G0_eval] interaction+intx_2b95f478+intx_33362112+intx_523cb487+intx_8d319905+mined (directional) — did not produce a va
- ×1 — [G0_eval] interaction+intx_2b95f478+intx_31ec7dbf+intx_33362112+intx_84c4eb09+intx_d7cdc91d+intx_ec71eb00+mined (directi
- ×1 — [G0_eval] interaction+intx_7bc00ae2+intx_96c8aab4+mined (directional) — did not produce a valid backtest
- ×1 — [G1_sanity] interaction+intx_0d9dfed7+intx_f587c01d+mean_reversion+mined+statistical (cross_sectional) — degenerate or too
- ×1 — [G1_sanity] interaction+intx_2b89b972+intx_79808473+intx_8293ade8+intx_f46b61d4+mined (cross_sectional) — degenerate or to
- ×1 — [G4_deflated_sharpe] atr_pct+interaction+intx_89fe53eb+intx_e0f99a11+mined+reversion (cross_sectional) — edge indistinguishable fro
- ×1 — [G4_deflated_sharpe] interaction+intx_6b2acdbc+intx_c0b28d4f+mined (cross_sectional) — edge indistinguishable from luck after trial

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*