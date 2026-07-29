# 🧬 Master Trader — Genome Population Report

*Generated 2026-07-29 04:02 UTC · source `/home/runner/work/master-trader/master-trader/var/mt.db`*

## 1 · Executive summary

| | |
|---|---|
| Genomes generated & tested | **122,634** |
| Deflated-Sharpe trial count (raw N) | **256,680** *(evals 122,697 + 133,983 screened)* |
| **Effective** independent trials (N_eff) | **357,558** *(ρ̄=0.029761285433194683 — the bar the DSR actually uses)* |
| Admitted to archive | **15977** |
| Rejected | **106,657** (87.0%) |
| Distinct families explored | **31** |
| Lessons accumulated | **82,768** |
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
| `—` | 82,602 | 67.4% | — |
| `ADMITTED` | 15,977 | 13.0% | **cleared every gate** |
| `GS_screen` | 11,440 | 9.3% | — |
| `G1_sanity` | 5,603 | 4.6% | degenerate / too few periods, or one period dominates P&L |
| `G3_cpcv_pbo` | 3,883 | 3.2% | parameter tuning overfit (high PBO) |
| `G4_deflated_sharpe` | 2,026 | 1.7% | edge indistinguishable from luck after trial correction |
| `G8_orthogonality` | 698 | 0.6% | duplicates an existing archive member |
| `G0_eval` | 358 | 0.3% | did not produce a valid backtest |
| `G2_oos` | 47 | 0.0% | shines in-sample, decays out-of-sample |

---

## 4 · Categorized breakdown

*`best DSR-z` per category is the meaningful column — it shows **where the search is finding signal**, not merely where it spent effort.*

### 4.1 By market
**Market**

| market | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `fx` | 40510 | 3371 | 2.71 | ██████████████████ |
| `crypto` | 42631 | 7213 | 2.41 | ██████████████████ |
| `xau` | 39493 | 5393 | 0.26 | ███··············· |

### 4.2 By phenotype
**Execution style**

| phenotype | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `cross_sectional` | 121053 | 15977 | 2.71 | ██████████████████ |
| `directional` | 1581 | 0 | -0.10 | ·················· |

### 4.3 By generation engine
**Engine**

| engine | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `evo` | 115856 | 15966 | 2.71 | ██████████████████ |
| `llm` | 1304 | 1 | -0.07 | ·················· |
| `random` | 1746 | 0 | -0.10 | ·················· |
| `template` | 2321 | 0 | -1.59 | ·················· |
| `miner` | 1407 | 10 | -5.33 | ·················· |

### 4.4 By regime conditioning
**Regime**

| regime | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `all` | 63060 | 10105 | 2.71 | ██████████████████ |
| `low_vol` | 1908 | 34 | 1.02 | ███████████······· |
| `trend` | 2958 | 26 | 0.73 | ████████·········· |
| `chop` | 41847 | 5273 | 0.26 | ███··············· |
| `high_vol` | 12861 | 539 | 0.26 | ███··············· |

### 4.5 By position sizing
**Sizing**

| sizing op | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `rank_bucket` | 115189 | 15852 | 2.71 | ██████████████████ |
| `vol_target` | 4696 | 119 | 0.97 | ███████████······· |
| `fixed_fractional` | 1246 | 0 | -0.10 | ·················· |
| `kelly_fraction` | 1169 | 6 | -1.38 | ·················· |
| `atr_scaled` | 334 | 0 | -4.07 | ·················· |

### 4.6 By strategy family — all 31 explored
**Family (ranked by best DSR-z)**

| family | genomes | admitted | best DSR-z | vs bar (1.645) |
|---|---:|---:|---:|---|
| `trend` | 43670 | 8233 | 2.71 | ██████████████████ |
| `volatility` | 41902 | 8385 | 2.71 | ██████████████████ |
| `pattern` | 38309 | 7945 | 2.71 | ██████████████████ |
| `statistical` | 37181 | 5672 | 2.71 | ██████████████████ |
| `momentum` | 35167 | 5485 | 2.71 | ██████████████████ |
| `oscillator` | 22217 | 2850 | 2.71 | ██████████████████ |
| `volume` | 25758 | 3980 | 2.43 | ██████████████████ |
| `macro` | 21556 | 2365 | 2.43 | ██████████████████ |
| `sentiment` | 8387 | 1017 | 2.43 | ██████████████████ |
| `microstructure` | 24679 | 5816 | 2.41 | ██████████████████ |
| `liquidity` | 23545 | 5790 | 2.41 | ██████████████████ |
| `breakout` | 17749 | 4204 | 2.41 | ██████████████████ |
| `positioning` | 5386 | 460 | 2.38 | ██████████████████ |
| `auction_market_theory` | 33152 | 4179 | 2.38 | ██████████████████ |
| `mean_reversion` | 4306 | 558 | 1.70 | ██████████████████ |
| `cross_asset` | 1303 | 119 | 1.70 | ██████████████████ |
| `volume_profile` | 9926 | 1808 | 1.63 | ██████████████████ |
| `order_flow` | 6403 | 689 | 1.21 | █████████████····· |
| `market_profile` | 6836 | 890 | 1.11 | ████████████······ |
| `ict` | 7872 | 1215 | 0.26 | ███··············· |
| `smc` | 7872 | 1215 | 0.26 | ███··············· |
| `event` | 8616 | 1090 | 0.22 | ██················ |
| `calendar` | 3178 | 390 | 0.22 | ██················ |
| `rates` | 7069 | 880 | 0.18 | ██················ |
| `persistence` | 762 | 65 | -0.85 | ·················· |
| `regime` | 271 | 0 | -1.47 | ·················· |
| `mixed` | 3476 | 108 | -1.72 | ·················· |
| `ml_derived` | 247 | 0 | -4.46 | ·················· |
| `intermarket` | 51 | 0 | -7.63 | ·················· |
| `crypto` | 9 | 0 | -25.42 | ·················· |
| `funding` | 9 | 0 | -25.42 | ·················· |

---

### 4.7 Feature attribution — which primitives *measurably* carry signal

*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is measured contribution, not the family it's tagged under.*

| feature | times measured | mean ΔDSR-z | verdict |
|---|---:|---:|---|
| `delta_divergence` | 2 | +6.129 | **carries signal** |
| `intx_fb03f296` | 2 | +2.663 | **carries signal** |
| `intx_70120704` | 18 | +2.409 | **carries signal** |
| `intx_d24a257d` | 32 | +2.170 | **carries signal** |
| `intx_d52ec380` | 57 | +2.163 | **carries signal** |
| `intx_bbf4a4e3` | 2 | +2.147 | **carries signal** |
| `intx_4a0c40e9` | 4 | +1.891 | **carries signal** |
| `vol_regime_tag` | 174 | +1.691 | **carries signal** |
| `value_area_real` | 5 | +1.460 | **carries signal** |
| `intx_039d3ebd` | 240 | +1.231 | **carries signal** |
| `intx_db6df9da` | 9 | +1.190 | **carries signal** |
| `intx_17709675` | 2 | +1.188 | **carries signal** |
| `variance_ratio` | 21048 | +1.072 | **carries signal** |
| `amihud_illiquidity` | 53846 | +0.981 | **carries signal** |
| `atr_expansion` | 27469 | +0.929 | **carries signal** |

---

## 5 · Archive (37 niches)

| niche | market | fitness |
|---|---|---:|
| `fx:position:low:long:all` | fx | 1.388 |
| `fx:position:med:long:all` | fx | 1.314 |
| `xau:swing:low:long:chop` | xau | 0.971 |
| `xau:swing:low:neutral:chop` | xau | 0.876 |
| `crypto:position:med:neutral:all` | crypto | 0.723 |
| `crypto:position:high:neutral:all` | crypto | 0.660 |
| `xau:swing:low:long:trend` | xau | 0.642 |
| `fx:position:low:neutral:all` | fx | 0.556 |
| `xau:swing:low:long:all` | xau | 0.524 |
| `crypto:position:med:neutral:high_vol` | crypto | 0.503 |
| `xau:swing:low:long:high_vol` | xau | 0.482 |
| `xau:position:low:long:chop` | xau | 0.466 |
| `xau:swing:low:neutral:high_vol` | xau | 0.450 |
| `crypto:position:med:neutral:low_vol` | crypto | 0.422 |
| `crypto:position:high:neutral:low_vol` | crypto | 0.402 |
| `xau:swing:low:neutral:all` | xau | 0.374 |
| `crypto:position:low:neutral:all` | crypto | 0.369 |
| `crypto:position:med:neutral:chop` | crypto | 0.361 |
| `crypto:position:low:neutral:high_vol` | crypto | 0.334 |
| `crypto:position:med:neutral:trend` | crypto | 0.320 |
| `xau:intraday:low:neutral:chop` | xau | 0.221 |
| `fx:intraday:low:long:chop` | fx | 0.155 |
| `crypto:swing:med:neutral:all` | crypto | 0.133 |
| `crypto:swing:med:long:chop` | crypto | 0.092 |
| `crypto:position:high:neutral:trend` | crypto | 0.089 |

## 6 · Lessons library (82,768)

- ×24 — [PASS] breakout+liquidity+microstructure+momentum+pattern+trend+volatility on a cross_sectional book promoted to the 
- ×11 — [PASS] mean_reversion+statistical on a cross_sectional book promoted to the candidate pool
- ×8 — [PASS] interaction+mined+pattern+poc_distance_real+roc+trend on a cross_sectional book promoted to the candidate pool
- ×7 — [PASS] breakout+liquidity+microstructure+momentum+pattern+trend on a cross_sectional book promoted to the candidate p
- ×7 — [PASS] pattern+trend on a cross_sectional book promoted to the candidate pool
- ×6 — [GS_screen] atr_pct+interaction+mined+range_vol (cross_sectional) — raw predictive strength too weak to clear the FDR scre
- ×6 — [PASS] auction_market_theory+liquidity+microstructure+volatility+volume on a cross_sectional book promoted to the can
- ×6 — [PASS] momentum on a cross_sectional book promoted to the candidate pool
- ×5 — [PASS] breakout+liquidity+microstructure+pattern+trend+volatility on a cross_sectional book promoted to the candidate
- ×5 — [PASS] liquidity+microstructure+volatility on a cross_sectional book promoted to the candidate pool
- ×5 — [GS_screen] atr_expansion+har_vol+interaction+mined (cross_sectional) — raw predictive strength too weak to clear the FDR 
- ×4 — [PASS] liquidity+microstructure+trend+volatility on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] momentum+trend on a cross_sectional book promoted to the candidate pool
- ×4 — [PASS] volume on a cross_sectional book promoted to the candidate pool
- ×4 — [GS_screen] dist_to_poc+interaction+intx_81239c57+mined (cross_sectional) — raw predictive strength too weak to clear the 

---

🔒 *Paper/research only — no live-capital action is taken or authorized. A genome in this report is a **candidate**, never a recommendation to trade.*