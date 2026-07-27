# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-27 07:02 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **52,636** |
| Deflated-Sharpe trial count (raw N) | **128,493** *(evals 84,048 + 44,445 screened)* |
| **Effective** independent trials (N_eff) | **287** *(ρ̄=0.003482315396987971 — the bar the DSR actually uses)* |
| Admitted to archive | **0** |
| Rejected | **52,636** (100.0%) |
| Distinct families explored | **31** |
| Lessons accumulated | **3,172** |
| Best DSR-z | **+1.093** vs bar 1.645 — below the bar |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `52702f9fc2f14605` | crypto | **1.09** | 0.4498 | 4.59 | 0.025 | cross_sectional | all | `G4_deflated_sharpe` |
| 2 | `53147ae58ac6750e` | crypto | **0.55** | 0.4150 | 5.19 | 0.026 | cross_sectional | all | `G4_deflated_sharpe` |
| 3 | `36d9f954dca0d83a` | crypto | **0.43** | 0.3876 | 4.85 | 0.034 | cross_sectional | trend | `G4_deflated_sharpe` |
| 4 | `7ba7253e5ef4a020` | crypto | **0.42** | 0.3869 | 4.84 | 0.034 | cross_sectional | trend | `G4_deflated_sharpe` |
| 5 | `a77a2fe504a44cfb` | crypto | **0.37** | 0.3636 | 3.71 | 0.037 | cross_sectional | all | `G4_deflated_sharpe` |
| 6 | `939e4c1831b9203d` | fx | **-0.00** | 0.3210 | 2.29 | 0.004 | cross_sectional | all | `G4_deflated_sharpe` |
| 7 | `bfd937441caac98b` | fx | **-0.10** | 0.3011 | 4.53 | 0.014 | directional | low_vol | `G4_deflated_sharpe` |
| 8 | `7a08185ab1583242` | crypto | **-0.45** | 0.2872 | 3.59 | 0.018 | cross_sectional | all | `G4_deflated_sharpe` |
| 9 | `ae8e7630a0bb18c0` | crypto | **-0.55** | 0.2785 | 3.16 | 0.080 | cross_sectional | all | `G4_deflated_sharpe` |
| 10 | `57078272babd4349` | crypto | **-0.55** | 0.1552 | 2.10 | 0.198 | cross_sectional | all | `G4_deflated_sharpe` |
| 11 | `4e44a91561b4ff9d` | xau | **-0.56** | 0.2582 | 4.27 | 0.012 | cross_sectional | high_vol | `G4_deflated_sharpe` |
| 12 | `6a10cb27be3c816e` | crypto | **-0.65** | 0.2365 | 1.60 | 0.285 | cross_sectional | all | `G4_deflated_sharpe` |
| 13 | `f0e77520848bf1cc` | crypto | **-0.72** | 0.0522 | 0.86 | 0.323 | cross_sectional | high_vol | `G4_deflated_sharpe` |
| 14 | `64d6965aedcb3205` | crypto | **-0.77** | 0.0612 | 0.91 | 0.279 | cross_sectional | high_vol | `G4_deflated_sharpe` |
| 15 | `6cb81bdd8b97e983` | xau | **-0.78** | 0.2655 | 3.75 | 0.026 | cross_sectional | trend | `G4_deflated_sharpe` |
| 16 | `bd700d5a382c9f29` | xau | **-0.81** | 0.2955 | 4.89 | 0.021 | cross_sectional | trend | `G4_deflated_sharpe` |
| 17 | `8c03edf89d88ded3` | fx | **-0.82** | 0.1883 | 1.97 | 0.009 | cross_sectional | all | `G4_deflated_sharpe` |
| 18 | `dc3fd5b337d662c8` | fx | **-0.85** | 0.1883 | 1.97 | 0.009 | cross_sectional | all | `G4_deflated_sharpe` |
| 19 | `94ac92ba3cf7ce9a` | fx | **-0.85** | 0.1883 | 1.97 | 0.009 | cross_sectional | all | `G4_deflated_sharpe` |
| 20 | `8a4085d64e83b2b0` | crypto | **-0.87** | 0.0342 | 0.72 | 0.539 | cross_sectional | all | `G4_deflated_sharpe` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `52702f9fc2f14605` — DSR-z 1.09 · died at `G4_deflated_sharpe` · families: auction_market_theory, statistical**
```
[crypto] gated_and (long_bias) on 4h
  features: rolling_kurt(window=71); rotation_factor(window=31)
  sizing:   rank_bucket(top_frac=0.2159875356881487, gross=1.5820119993219797, per_name_cap=0.07789291227666356)
  risk:     horizon_hold(horizon=21, cost_stress=1.6320938700249077)
  id=52702f9fc2f14605  gen=3  by=evo_mutate  nodes=5
```
**#2 · `53147ae58ac6750e` — DSR-z 0.55 · died at `G4_deflated_sharpe` · families: calendar, event, macro, volatility, volume**
```
[crypto] gated_and (short_bias) on 4h
  features: obv(window=34); cesi_surprise(window=26); range_vol(window=42)
  sizing:   vol_target(target_ann_vol=0.14253913331184145, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=53147ae58ac6750e  gen=1  by=evo_mutate  nodes=6
```
**#3 · `36d9f954dca0d83a` — DSR-z 0.43 · died at `G4_deflated_sharpe` · families: calendar, event, macro, volatility, volume**
```
[crypto] gated_and (short_bias, regime=trend) on 4h
  features: obv(window=34); cesi_surprise(window=26); range_vol(window=42)
  sizing:   vol_target(target_ann_vol=0.13987297876382396, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=36d9f954dca0d83a  gen=5  by=evo_mutate  nodes=6
```
**#4 · `7ba7253e5ef4a020` — DSR-z 0.42 · died at `G4_deflated_sharpe` · families: calendar, event, macro, volatility, volume**
```
[crypto] gated_and (short_bias, regime=trend) on 4h
  features: obv(window=34); cesi_surprise(window=26); range_vol(window=42)
  sizing:   vol_target(target_ann_vol=0.14253913331184145, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=7ba7253e5ef4a020  gen=4  by=evo_mutate  nodes=6
```
**#5 · `a77a2fe504a44cfb` — DSR-z 0.37 · died at `G4_deflated_sharpe` · families: auction_market_theory, statistical**
```
[crypto] gated_and (long_bias) on 4h
  features: rolling_kurt(window=71); rotation_factor(window=21)
  sizing:   rank_bucket(top_frac=0.2159875356881487, gross=1.5820119993219797, per_name_cap=0.07789291227666356)
  risk:     horizon_hold(horizon=21, cost_stress=1.6320938700249077)
  id=a77a2fe504a44cfb  gen=2  by=evo_crossover  nodes=5
```
**#6 · `939e4c1831b9203d` — DSR-z -0.00 · died at `G4_deflated_sharpe` · families: macro, mean_reversion, positioning, statistical**
```
[fx] weighted_blend (long_bias) on H4
  features: cot_index(window=7); mean_reversion_halflife(window=23)
  sizing:   kelly_fraction(kelly_frac=0.35288141119085553, max_leverage=2.991053424485564, top_frac=0.1711302888078569, gross=1.296064831524862, per_name_cap=0.04649308290159507)
  risk:     horizon_hold(horizon=43, cost_stress=1.072342218882366)
  id=939e4c1831b9203d  gen=2  by=evo_mutate  nodes=5
```
**#7 · `bfd937441caac98b` — DSR-z -0.10 · died at `G4_deflated_sharpe` · families: auction_market_theory, breakout, market_profile, pattern, volatility**
```
[fx] gated_and (long_bias, regime=low_vol) on H4
  features: realized_vol(window=66); breakout(window=15); value_area_position(window=25)
  sizing:   fixed_fractional(f=0.061306406715798636)
  risk:     triple_barrier(entry_thr=0.6557941688966837, sl_mult=2.6633774947616438, tp_mult=3.732239271917572, max_bars=16, cost_stress=1.3334322802286227)
  id=bfd937441caac98b  gen=0  by=random  nodes=6
```
**#8 · `7a08185ab1583242` — DSR-z -0.45 · died at `G4_deflated_sharpe` · families: calendar, event, macro, trend, volume**
```
[crypto] gated_and (long_bias) on 4h
  features: obv(window=34); cesi_surprise(window=26); ma_cross(fast=20, slow=185)
  sizing:   vol_target(target_ann_vol=0.14253913331184145, top_frac=0.05782709615838198, per_name_cap=0.06769232130025979)
  risk:     horizon_hold(horizon=14, cost_stress=1.7975401320743511)
  id=7a08185ab1583242  gen=1  by=evo_mutate  nodes=6
```
**#9 · `ae8e7630a0bb18c0` — DSR-z -0.55 · died at `G4_deflated_sharpe` · families: liquidity, microstructure**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=34)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=17, cost_stress=1.0)
  id=ae8e7630a0bb18c0  gen=3  by=evo_crossover  nodes=4
```
**#10 · `57078272babd4349` — DSR-z -0.55 · died at `G4_deflated_sharpe` · families: auction_market_theory, market_profile, order_flow, volume_profile**
```
[crypto] weighted_blend (neutral) on 4h
  features: dist_to_poc(window=104); value_area_position(window=45); cumulative_delta(window=58)
  sizing:   rank_bucket(top_frac=0.17, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=12, cost_stress=1.0)
  id=57078272babd4349  gen=2  by=evo_crossover  nodes=6
```
**#11 · `4e44a91561b4ff9d` — DSR-z -0.56 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[xau] gated_and (long_bias, regime=high_vol) on H4
  features: atr_expansion(window=71); breakout(window=46)
  sizing:   rank_bucket(top_frac=0.15, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=4e44a91561b4ff9d  gen=0  by=template:volexp  nodes=5
```
**#12 · `6a10cb27be3c816e` — DSR-z -0.65 · died at `G4_deflated_sharpe` · families: volatility**
```
[crypto] gated_or (long_bias) on 4h
  features: bb_position(window=19, mult=1.824268544576922)
  sizing:   kelly_fraction(kelly_frac=0.7017885073579699, max_leverage=4.864670761728196, top_frac=0.16035288259389402, gross=1.2468186870025852, per_name_cap=0.1917504326857068)
  risk:     horizon_hold(horizon=48, cost_stress=1.2989442673410005)
  id=6a10cb27be3c816e  gen=0  by=random  nodes=4
```
**#13 · `f0e77520848bf1cc` — DSR-z -0.72 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[crypto] gated_and (long_bias, regime=high_vol) on 4h
  features: atr_expansion(window=71); breakout(window=46)
  sizing:   rank_bucket(top_frac=0.15, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=f0e77520848bf1cc  gen=0  by=template:volexp  nodes=5
```
**#14 · `64d6965aedcb3205` — DSR-z -0.77 · died at `G4_deflated_sharpe` · families: trend**
```
[crypto] weighted_blend (neutral, regime=high_vol) on 4h
  features: sma_dist(window=174)
  sizing:   rank_bucket(top_frac=0.0855216497031606, gross=1.031306603909702, per_name_cap=0.19418941713087268)
  risk:     horizon_hold(horizon=10, cost_stress=1.3957894762345329)
  id=64d6965aedcb3205  gen=0  by=random  nodes=4
```
**#15 · `6cb81bdd8b97e983` — DSR-z -0.78 · died at `G4_deflated_sharpe` · families: momentum, oscillator, volatility**
```
[xau] gated_and (long_bias, regime=trend) on H4
  features: atr_expansion(window=63); macd(fast=10, slow=59, signal=16)
  sizing:   rank_bucket(top_frac=0.22, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=11, cost_stress=1.0)
  id=6cb81bdd8b97e983  gen=1  by=evo_mutate  nodes=5
```
**#16 · `bd700d5a382c9f29` — DSR-z -0.81 · died at `G4_deflated_sharpe` · families: breakout, pattern, volatility**
```
[xau] gated_and (long_bias, regime=trend) on H4
  features: atr_expansion(window=71); breakout(window=46)
  sizing:   rank_bucket(top_frac=0.15, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=8, cost_stress=1.0)
  id=bd700d5a382c9f29  gen=2  by=evo_mutate  nodes=5
```
**#17 · `8c03edf89d88ded3` — DSR-z -0.82 · died at `G4_deflated_sharpe` · families: statistical**
```
[fx] gated_and (long_bias) on H4
  features: autocorr(lag=6, window=91)
  sizing:   rank_bucket(top_frac=0.2, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=20, cost_stress=1.0)
  id=8c03edf89d88ded3  gen=7  by=evo_mutate  nodes=4
```
**#18 · `dc3fd5b337d662c8` — DSR-z -0.85 · died at `G4_deflated_sharpe` · families: statistical**
```
[fx] gated_and (long_bias) on H4
  features: autocorr(lag=6, window=91)
  sizing:   rank_bucket(top_frac=0.12936081428670365, gross=1.0, per_name_cap=0.15519042777345052)
  risk:     horizon_hold(horizon=20, cost_stress=1.0)
  id=dc3fd5b337d662c8  gen=10  by=evo_mutate  nodes=4
```
**#19 · `94ac92ba3cf7ce9a` — DSR-z -0.85 · died at `G4_deflated_sharpe` · families: statistical**
```
[fx] gated_and (long_bias) on H4
  features: autocorr(lag=6, window=91)
  sizing:   rank_bucket(top_frac=0.2, gross=1.1373937916998094, per_name_cap=0.15519042777345052)
  risk:     horizon_hold(horizon=20, cost_stress=1.0)
  id=94ac92ba3cf7ce9a  gen=10  by=evo_mutate  nodes=4
```
**#20 · `8a4085d64e83b2b0` — DSR-z -0.87 · died at `G4_deflated_sharpe` · families: momentum, oscillator, trend**
```
[crypto] gated_or (long_bias) on 4h
  features: macd(fast=12, slow=26, signal=9); ma_cross(fast=9, slow=36)
  sizing:   rank_bucket(top_frac=0.18, gross=1.0, per_name_cap=0.15)
  risk:     horizon_hold(horizon=5, cost_stress=1.0)
  id=8a4085d64e83b2b0  gen=0  by=template:macd_trend  nodes=5
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 29,108 | 55.3% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 15,654 | 29.7% | degenerate / too few periods, or one period dominates P&L |
| `G0_eval` | 7,874 | 15.0% | did not produce a valid backtest |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `crypto` | 18297 | 0 | 1.09 | ████████████······ |
| `fx` | 17313 | 0 | -0.00 | ·················· |
| `xau` | 17026 | 0 | -0.56 | ·················· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 44846 | 0 | 1.09 | ████████████······ |
| `directional` | 7790 | 0 | -0.10 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 23663 | 0 | 1.09 | ████████████······ |
| `random` | 13378 | 0 | -0.10 | ·················· |
| `template` | 10767 | 0 | -0.56 | ·················· |
| `miner` | 4828 | 0 | -1.53 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 16878 | 0 | 1.09 | ████████████······ |
| `trend` | 13782 | 0 | 0.43 | █████············· |
| `low_vol` | 9989 | 0 | -0.10 | ·················· |
| `high_vol` | 5571 | 0 | -0.56 | ·················· |
| `chop` | 6416 | 0 | -1.15 | ·················· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 35879 | 0 | 1.09 | ████████████······ |
| `vol_target` | 5675 | 0 | 0.55 | ██████············ |
| `kelly_fraction` | 3292 | 0 | -0.00 | ·················· |
| `fixed_fractional` | 5243 | 0 | -0.10 | ·················· |
| `atr_scaled` | 2547 | 0 | -2.32 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `auction_market_theory` | 7668 | 0 | 1.09 | ████████████······ |
| `statistical` | 6871 | 0 | 1.09 | ████████████······ |
| `volatility` | 10281 | 0 | 0.55 | ██████············ |
| `volume` | 4162 | 0 | 0.55 | ██████············ |
| `macro` | 2061 | 0 | 0.55 | ██████············ |
| `event` | 1162 | 0 | 0.55 | ██████············ |
| `calendar` | 410 | 0 | 0.55 | ██████············ |
| `mean_reversion` | 3728 | 0 | -0.00 | ·················· |
| `positioning` | 404 | 0 | -0.00 | ·················· |
| `pattern` | 3836 | 0 | -0.10 | ·················· |
| `breakout` | 2907 | 0 | -0.10 | ·················· |
| `market_profile` | 1555 | 0 | -0.10 | ·················· |
| `trend` | 4200 | 0 | -0.45 | ·················· |
| `microstructure` | 3527 | 0 | -0.55 | ·················· |
| `liquidity` | 2105 | 0 | -0.55 | ·················· |
| `order_flow` | 4690 | 0 | -0.55 | ·················· |
| `volume_profile` | 1466 | 0 | -0.55 | ·················· |
| `momentum` | 6486 | 0 | -0.78 | ·················· |
| `oscillator` | 4899 | 0 | -0.78 | ·················· |
| `sentiment` | 327 | 0 | -1.18 | ·················· |
| `regime` | 1465 | 0 | -1.33 | ·················· |
| `rates` | 975 | 0 | -1.33 | ·················· |
| `ml_derived` | 1251 | 0 | -1.35 | ·················· |
| `persistence` | 1171 | 0 | -1.59 | ·················· |
| `ict` | 870 | 0 | -1.67 | ·················· |
| `smc` | 870 | 0 | -1.67 | ·················· |
| `mixed` | 14890 | 0 | -2.42 | ·················· |
| `cross_asset` | 622 | 0 | -2.67 | ·················· |
| `intermarket` | 386 | 0 | -2.67 | ·················· |
| `crypto` | 352 | 0 | -3.10 | ·················· |
| `funding` | 352 | 0 | -3.10 | ·················· |

---
---

## 5 · Archive (0 niches)

*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*

## 6 · Lessons library (3,172)

- ×1 — [G4_deflated_sharpe] interaction+intx_1dc0b040+intx_97267b90+mined+persistence+statistical (cross_sectional) — edge indistinguishab
- ×1 — [G0_eval] consolidation_score+interaction+intx_3d943c0f+intx_490ae0e7+intx_a605c3a9+intx_a7330ab8+intx_f4086f90+mined (c
- ×1 — [G4_deflated_sharpe] interaction+intx_1982d8fe+intx_42f6d136+intx_a27acb9f+intx_f0c615e8+mined+obv+order_block_strength (cross_sect
- ×1 — [G4_deflated_sharpe] interaction+intx_888ccf05+intx_9103e174+intx_924d5801+intx_e191f15c+mined (cross_sectional) — edge indistingui
- ×1 — [G0_eval] momentum+pattern+trend (cross_sectional) — did not produce a valid backtest
- ×1 — [G0_eval] hurst+interaction+intx_03f84a0d+intx_61b45e5f+intx_68f31ba6+intx_81426b05+intx_fd877997+mined (directional) — 
- ×1 — [G0_eval] interaction+intx_0a3a9b14+intx_2ec8aa70+intx_6fed863d+intx_c52263c1+mined+volatility (cross_sectional) — did n
- ×1 — [G0_eval] interaction+intx_65b3deb2+intx_e98a7020+macro+mined+sentiment (cross_sectional) — did not produce a valid back
- ×1 — [G1_sanity] interaction+intx_1dc0b040+intx_47366be9+intx_794714f9+intx_93c55220+intx_a7330ab8+intx_fa0d218b+mined (cross_s
- ×1 — [G0_eval] auction_market_theory+interaction+intx_1982d8fe+mined+order_flow+statistical+variance_ratio (cross_sectional) 
- ×1 — [G0_eval] interaction+intx_8f5045f5+intx_b21d0c2e+intx_bbd086ed+mined+rolling_kurt (directional) — did not produce a val
- ×1 — [G4_deflated_sharpe] interaction+liquidity_sweep+ma_cross+mined+rotation_factor+slope (cross_sectional) — edge indistinguishable fr
- ×1 — [G4_deflated_sharpe] interaction+intx_2b5b6e1f+mined+rolling_skew (directional) — edge indistinguishable from luck after trial corr
- ×1 — [G4_deflated_sharpe] interaction+intx_ab8150cc+intx_fe13d173+mined (cross_sectional) — edge indistinguishable from luck after trial
- ×1 — [G4_deflated_sharpe] interaction+intx_348c41cb+intx_37b2c0dc+intx_a1e5145d+intx_bbd086ed+mined+volume (cross_sectional) — edge indi

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*