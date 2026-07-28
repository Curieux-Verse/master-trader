# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-28 14:05 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **217,098** |
| Deflated-Sharpe trial count (raw N) | **413,616** *(evals 296,296 + 117,320 screened)* |
| **Effective** independent trials (N_eff) | **234,430** *(ρ̄=0.10333362306699923 — the bar the DSR actually uses)* |
| Admitted to archive | **22052** |
| Rejected | **195,046** (89.8%) |
| Distinct families explored | **31** |
| Lessons accumulated | **56,773** |
| Best DSR-z | **+2.714** vs bar 1.645 — ✅ **cleared the bar** |

**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); **`1.645` = statistically significant at p<0.05.** Higher is better; it is the single number that says how close the search is to a genuine edge.

---

## 2 · 🏆 Top 20 candidates (closest to a real edge)

| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |
|--:|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `756f4b4cb0215305` | fx | **2.71** ✅ | 1.5512 | 10.48 | 0.000 | cross_sectional | all | `ADMITTED` |
| 2 | `f565adc2296dd0c5` | fx | **2.71** ✅ | 1.5512 | 10.48 | 0.000 | cross_sectional | all | `G8_orthogonality` |
| 3 | `4b0a1c225b39b8a9` | fx | **2.70** ✅ | 1.5512 | 10.48 | 0.000 | cross_sectional | all | `G8_orthogonality` |
| 4 | `62329a6764ad97f2` | fx | **2.66** ✅ | 1.5313 | 10.34 | 0.000 | cross_sectional | all | `ADMITTED` |
| 5 | `c9d0b80b4cfe4d4b` | fx | **2.47** ✅ | 1.4777 | 9.98 | 0.000 | cross_sectional | all | `ADMITTED` |
| 6 | `496721e576443bea` | fx | **2.47** ✅ | 1.4777 | 9.98 | 0.000 | cross_sectional | all | `G8_orthogonality` |
| 7 | `d975c1a4d38e2758` | fx | **2.45** ✅ | 1.5289 | 10.33 | 0.000 | cross_sectional | all | `ADMITTED` |
| 8 | `9f5e3668764a1557` | fx | **2.43** ✅ | 1.5403 | 10.40 | 0.000 | cross_sectional | all | `ADMITTED` |
| 9 | `829a32f9b7de3f76` | fx | **2.42** ✅ | 1.5719 | 10.62 | 0.000 | cross_sectional | all | `ADMITTED` |
| 10 | `4f508d1ef6104389` | crypto | **2.41** ✅ | 1.0790 | 7.37 | 0.040 | cross_sectional | all | `ADMITTED` |
| 11 | `af9c2944588a6691` | crypto | **2.40** ✅ | 1.0791 | 7.37 | 0.044 | cross_sectional | all | `ADMITTED` |
| 12 | `eae09a8bcdefa330` | fx | **2.39** ✅ | 1.5403 | 10.40 | 0.000 | cross_sectional | all | `ADMITTED` |
| 13 | `3898f7908cfceda7` | fx | **2.39** ✅ | 1.5403 | 10.40 | 0.000 | cross_sectional | all | `ADMITTED` |
| 14 | `f2d2e3c981201bb9` | fx | **2.39** ✅ | 1.5403 | 10.40 | 0.000 | cross_sectional | all | `ADMITTED` |
| 15 | `8790576b67b2ba16` | fx | **2.39** ✅ | 1.5148 | 10.23 | 0.000 | cross_sectional | all | `ADMITTED` |
| 16 | `769376c9f4686bc4` | fx | **2.39** ✅ | 1.7051 | 11.52 | 0.000 | cross_sectional | all | `ADMITTED` |
| 17 | `55b80bbeb1b15234` | fx | **2.38** ✅ | 1.7493 | 11.82 | 0.001 | cross_sectional | all | `G8_orthogonality` |
| 18 | `e41648aa5c632f0e` | fx | **2.38** ✅ | 1.6054 | 10.84 | 0.000 | cross_sectional | all | `ADMITTED` |
| 19 | `1910a2f4ddd61623` | fx | **2.38** ✅ | 1.7664 | 11.93 | 0.000 | cross_sectional | all | `ADMITTED` |
| 20 | `62dce1e8bc85b432` | fx | **2.37** ✅ | 1.7051 | 11.52 | 0.000 | cross_sectional | all | `ADMITTED` |

<details><summary><b>Full DSL recipes for the top candidates</b></summary>

**#1 · `756f4b4cb0215305` — DSR-z 2.71 · died at `ADMITTED` · families: momentum, oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: macd(fast=7, slow=23, signal=19); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.18225207774899146, gross=1.0, per_name_cap=0.04687803515421096)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=756f4b4cb0215305  gen=108  by=evo_mutate  nodes=9
```
**#2 · `f565adc2296dd0c5` — DSR-z 2.71 · died at `G8_orthogonality` · families: momentum, oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: macd(fast=7, slow=23, signal=19); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.17412637810828982, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=f565adc2296dd0c5  gen=111  by=evo_mutate  nodes=9
```
**#3 · `4b0a1c225b39b8a9` — DSR-z 2.70 · died at `G8_orthogonality` · families: momentum, oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: macd(fast=7, slow=23, signal=19); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=4b0a1c225b39b8a9  gen=110  by=evo_mutate  nodes=9
```
**#4 · `62329a6764ad97f2` — DSR-z 2.66 · died at `ADMITTED` · families: momentum, oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: macd(fast=7, slow=23, signal=19); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.14029229848303446)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=62329a6764ad97f2  gen=112  by=evo_crossover  nodes=9
```
**#5 · `c9d0b80b4cfe4d4b` — DSR-z 2.47 · died at `ADMITTED` · families: oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: ma_cross(fast=4, slow=14); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.18225207774899146, gross=1.0, per_name_cap=0.04687803515421096)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=c9d0b80b4cfe4d4b  gen=109  by=evo_mutate  nodes=9
```
**#6 · `496721e576443bea` — DSR-z 2.47 · died at `G8_orthogonality` · families: oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: ma_cross(fast=4, slow=14); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=496721e576443bea  gen=110  by=evo_crossover  nodes=9
```
**#7 · `d975c1a4d38e2758` — DSR-z 2.45 · died at `ADMITTED` · families: oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: ema_dist(window=15); cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=d975c1a4d38e2758  gen=146  by=evo_mutate  nodes=9
```
**#8 · `9f5e3668764a1557` — DSR-z 2.43 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); news_sentiment(window=20); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.07297557077671206)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=9f5e3668764a1557  gen=194  by=evo_mutate  nodes=8
```
**#9 · `829a32f9b7de3f76` — DSR-z 2.42 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); news_sentiment(window=20); rel_volume(window=135); news_sentiment(window=8)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.14029229848303446)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=829a32f9b7de3f76  gen=191  by=evo_mutate  nodes=9
```
**#10 · `4f508d1ef6104389` — DSR-z 2.41 · died at `ADMITTED` · families: breakout, liquidity, microstructure, momentum, pattern, trend, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68); amihud_illiquidity(window=250); tsmom_blend(short=38, med=59, long=63)
  sizing:   rank_bucket(top_frac=0.180452, gross=1.4835195432578485, per_name_cap=0.10539243851958019)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=4f508d1ef6104389  gen=113  by=evo_mutate  nodes=8
```
**#11 · `af9c2944588a6691` — DSR-z 2.40 · died at `ADMITTED` · families: breakout, liquidity, microstructure, momentum, pattern, trend, volatility**
```
[crypto] weighted_blend (neutral) on 4h
  features: amihud_illiquidity(window=182); breakout(window=14); atr_expansion(window=68); amihud_illiquidity(window=250); tsmom_blend(short=38, med=59, long=63)
  sizing:   rank_bucket(top_frac=0.180452, gross=1.6136995382452015, per_name_cap=0.11544998622470065)
  risk:     horizon_hold(horizon=47, cost_stress=1.0)
  id=af9c2944588a6691  gen=113  by=evo_mutate  nodes=8
```
**#12 · `eae09a8bcdefa330` — DSR-z 2.39 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); news_sentiment(window=20); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.19425064002768988, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=eae09a8bcdefa330  gen=218  by=evo_mutate  nodes=8
```
**#13 · `3898f7908cfceda7` — DSR-z 2.39 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); news_sentiment(window=20); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=3898f7908cfceda7  gen=186  by=evo_crossover  nodes=8
```
**#14 · `f2d2e3c981201bb9` — DSR-z 2.39 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); news_sentiment(window=20); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.19128067206115637, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=f2d2e3c981201bb9  gen=210  by=evo_mutate  nodes=8
```
**#15 · `8790576b67b2ba16` — DSR-z 2.39 · died at `ADMITTED` · families: momentum, oscillator, pattern, statistical, trend, volatility**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); ema_dist(window=184); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rsi(window=10)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=8790576b67b2ba16  gen=112  by=evo_mutate  nodes=9
```
**#16 · `769376c9f4686bc4` — DSR-z 2.39 · died at `ADMITTED` · families: oscillator, pattern, statistical, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.21, gross=1.177697134096235, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=769376c9f4686bc4  gen=149  by=evo_mutate  nodes=8
```
**#17 · `55b80bbeb1b15234` — DSR-z 2.38 · died at `G8_orthogonality` · families: macro, oscillator, pattern, positioning, statistical, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rel_volume(window=135); cot_index(window=13)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.14029229848303446)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=55b80bbeb1b15234  gen=115  by=evo_mutate  nodes=9
```
**#18 · `e41648aa5c632f0e` — DSR-z 2.38 · died at `ADMITTED` · families: auction_market_theory, pattern, statistical, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: rotation_factor(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.09511358859730075)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=e41648aa5c632f0e  gen=315  by=evo_mutate  nodes=8
```
**#19 · `1910a2f4ddd61623` — DSR-z 2.38 · died at `ADMITTED` · families: macro, oscillator, pattern, sentiment, statistical, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rel_volume(window=135); news_sentiment(window=11)
  sizing:   rank_bucket(top_frac=0.21, gross=0.8824190586852465, per_name_cap=0.1488698459729555)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=1910a2f4ddd61623  gen=260  by=evo_mutate  nodes=9
```
**#20 · `62dce1e8bc85b432` — DSR-z 2.37 · died at `ADMITTED` · families: oscillator, pattern, statistical, volatility, volume**
```
[fx] gated_or (long_bias) on H4
  features: cci(window=5); realized_vol(window=16); candlestick_pattern(pattern=pin); variance_ratio(window=43, q=7); rel_volume(window=135)
  sizing:   rank_bucket(top_frac=0.21, gross=1.0, per_name_cap=0.10667879121072119)
  risk:     horizon_hold(horizon=48, cost_stress=1.0)
  id=62dce1e8bc85b432  gen=175  by=evo_mutate  nodes=8
```
</details>

---

## 3 · Where genomes die — the gate funnel

Each candidate is killed by the **first** gate it fails. Cheap gates run first.

| gate | genomes killed | share | what it means |
|---|---:|---:|---|
| `G4_deflated_sharpe` | 71,878 | 33.1% | edge indistinguishable from luck after trial correction |
| `G1_sanity` | 54,746 | 25.2% | degenerate / too few periods, or one period dominates P&L |
| `GS_screen` | 37,792 | 17.4% | — |
| `ADMITTED` | 22,052 | 10.2% | **cleared every gate** |
| `G0_eval` | 19,638 | 9.0% | did not produce a valid backtest |
| `G3_cpcv_pbo` | 10,333 | 4.8% | parameter tuning overfit (high PBO) |
| `G8_orthogonality` | 529 | 0.2% | duplicates an existing archive member |
| `G2_oos` | 130 | 0.1% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `fx` | 71750 | 4590 | 2.71 | ██████████████████ |
| `crypto` | 74087 | 9817 | 2.41 | ██████████████████ |
| `xau` | 71261 | 7645 | 0.26 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 196172 | 22052 | 2.71 | ██████████████████ |
| `directional` | 20926 | 0 | -0.10 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 140463 | 22048 | 2.71 | ██████████████████ |
| `llm` | 1314 | 1 | -0.07 | ·················· |
| `random` | 35303 | 0 | -0.10 | ·················· |
| `template` | 28248 | 1 | -0.87 | ·················· |
| `miner` | 11770 | 2 | -1.53 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 84582 | 13312 | 2.71 | ██████████████████ |
| `low_vol` | 30593 | 75 | 1.02 | ███████████······· |
| `trend` | 30094 | 66 | 0.73 | ████████·········· |
| `chop` | 45828 | 7714 | 0.26 | ███··············· |
| `high_vol` | 26001 | 885 | 0.26 | ███··············· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 156331 | 21864 | 2.71 | ██████████████████ |
| `vol_target` | 30298 | 179 | 0.97 | ███████████······· |
| `fixed_fractional` | 13979 | 0 | -0.10 | ·················· |
| `atr_scaled` | 6930 | 0 | -1.32 | ·················· |
| `kelly_fraction` | 9560 | 9 | -1.38 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `volatility` | 52916 | 11241 | 2.71 | ██████████████████ |
| `statistical` | 45695 | 8213 | 2.71 | ██████████████████ |
| `trend` | 45442 | 11769 | 2.71 | ██████████████████ |
| `momentum` | 44729 | 7915 | 2.71 | ██████████████████ |
| `pattern` | 36530 | 10767 | 2.71 | ██████████████████ |
| `oscillator` | 31267 | 4484 | 2.71 | ██████████████████ |
| `macro` | 29150 | 4154 | 2.43 | ██████████████████ |
| `volume` | 27918 | 5654 | 2.43 | ██████████████████ |
| `sentiment` | 13172 | 1638 | 2.43 | ██████████████████ |
| `microstructure` | 24582 | 7828 | 2.41 | ██████████████████ |
| `breakout` | 20349 | 5904 | 2.41 | ██████████████████ |
| `liquidity` | 19941 | 7733 | 2.41 | ██████████████████ |
| `positioning` | 4434 | 562 | 2.38 | ██████████████████ |
| `auction_market_theory` | 44264 | 6963 | 2.38 | ██████████████████ |
| `mean_reversion` | 14716 | 892 | 1.70 | ██████████████████ |
| `cross_asset` | 2599 | 207 | 1.70 | ██████████████████ |
| `volume_profile` | 10291 | 2436 | 1.63 | ██████████████████ |
| `order_flow` | 14388 | 1602 | 1.21 | █████████████····· |
| `market_profile` | 12877 | 1248 | 1.11 | ████████████······ |
| `ict` | 8338 | 1969 | 0.26 | ███··············· |
| `smc` | 8338 | 1969 | 0.26 | ███··············· |
| `event` | 9072 | 2249 | 0.25 | ███··············· |
| `calendar` | 3516 | 834 | 0.25 | ███··············· |
| `rates` | 9959 | 1788 | 0.18 | ██················ |
| `persistence` | 3604 | 125 | -0.85 | ·················· |
| `regime` | 5875 | 0 | -1.33 | ·················· |
| `mixed` | 36189 | 100 | -1.71 | ·················· |
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
| `amihud_illiquidity` | 32609 | +0.974 | **carries signal** |
| `atr_expansion` | 19832 | +0.966 | **carries signal** |
| `autocorr` | 8129 | +0.713 | **carries signal** |
| `rel_volume` | 9086 | +0.698 | **carries signal** |
| `variance_ratio` | 14038 | +0.693 | **carries signal** |
| `tsmom_blend` | 12610 | +0.466 | **carries signal** |
| `breakout` | 17431 | +0.442 | **carries signal** |
| `williams_r` | 2 | +0.436 | **carries signal** |
| `candlestick_pattern` | 24249 | +0.383 | **carries signal** |
| `realized_vol` | 11019 | +0.377 | **carries signal** |
| `ma_cross` | 11345 | +0.265 | **carries signal** |
| `momentum` | 4735 | +0.247 | **carries signal** |
| `cci` | 7574 | +0.207 | **carries signal** |

---

## 5 · Archive (34 niches)

| niche | market | fitness |
|---|---|---:|
| `fx:position:low:long:all` | fx | 1.388 |
| `fx:position:med:long:all` | fx | 1.314 |
| `xau:swing:low:long:chop` | xau | 0.848 |
| `xau:swing:low:neutral:chop` | xau | 0.757 |
| `crypto:position:med:neutral:all` | crypto | 0.679 |
| `crypto:position:high:neutral:all` | crypto | 0.660 |
| `crypto:position:med:neutral:high_vol` | crypto | 0.432 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.404 |
| `crypto:position:high:neutral:low_vol` | crypto | 0.402 |
| `xau:swing:low:long:high_vol` | xau | 0.374 |
| `xau:swing:low:long:trend` | xau | 0.366 |
| `crypto:position:med:neutral:chop` | crypto | 0.361 |
| `crypto:position:low:neutral:all` | crypto | 0.352 |
| `fx:position:low:neutral:all` | fx | 0.334 |
| `crypto:position:low:neutral:high_vol` | crypto | 0.334 |
| `crypto:position:med:neutral:trend` | crypto | 0.320 |
| `xau:swing:low:long:all` | xau | 0.240 |
| `xau:intraday:low:neutral:chop` | xau | 0.221 |
| `fx:intraday:low:long:chop` | fx | 0.155 |
| `crypto:swing:med:neutral:all` | crypto | 0.133 |
| `xau:position:low:long:chop` | xau | 0.111 |
| `crypto:swing:med:long:chop` | crypto | 0.092 |
| `crypto:position:high:neutral:trend` | crypto | 0.089 |
| `xau:intraday:low:long:chop` | xau | 0.075 |
| `xau:swing:low:neutral:all` | xau | 0.044 |

## 6 · Lessons library (56,773)

- ×11 — [PASS] statistical on a cross_sectional book promoted to the candidate pool
- ×11 — [PASS] auction_market_theory+liquidity+microstructure+volatility+volume on a cross_sectional book promoted to the can
- ×11 — [PASS] liquidity+microstructure+momentum+trend+volatility on a cross_sectional book promoted to the candidate pool
- ×11 — [PASS] breakout+liquidity+microstructure+momentum+pattern+trend+volatility on a cross_sectional book promoted to the 
- ×7 — [PASS] auction_market_theory+market_profile+volatility on a cross_sectional book promoted to the candidate pool
- ×7 — [PASS] statistical+volatility on a cross_sectional book promoted to the candidate pool
- ×7 — [PASS] liquidity+microstructure+momentum+trend+volatility+volume on a cross_sectional book promoted to the candidate 
- ×6 — [PASS] interaction+mined+obv+range_vol+statistical+trend+volatility on a cross_sectional book promoted to the candida
- ×6 — [GS_screen] auction_market_theory+volume (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_s
- ×6 — [G3_cpcv_pbo] liquidity+microstructure+momentum+trend+volatility (cross_sectional) — parameter tuning is overfit (high PBO) 
- ×6 — [GS_screen] event+macro+pattern+rates+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [
- ×6 — [GS_screen] momentum+oscillator+trend (cross_sectional) — raw predictive strength too weak to clear the FDR screen [p_sing
- ×4 — [PASS] liquidity+microstructure+trend on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] volatility on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] liquidity+microstructure+momentum+oscillator+trend+volatility on a cross_sectional book promoted to the candid

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*