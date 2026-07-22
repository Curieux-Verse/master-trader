# 12 — Primitive Library Implementation Plan

> How the vast, no-privilege vocabulary of [11 — Primitive Catalog](11_PRIMITIVE_CATALOG.md) actually gets built, and what each family *demands* of every phase. The catalog says *what* the generators may wire; this doc says *when it becomes real, where its data comes from, which existing code seeds it, and what it costs.* It is the bridge from "test everything, privilege nothing" to a concrete, phased build.

The headline: the registry is not a Phase-1 checkbox — it is a **cross-phase workstream** whose data requirements *reshape* Phase 0, and whose expansion hooks (miner + LLM authoring primitives) *are* Phases 3–4. Under-scoping it was the gap this document closes.

## 1. Three mechanisms make unbounded breadth safe (and where they live)

Breadth is only legitimate when paired with rigor ([README principle 3](../README.md)). Four pieces enforce that, mapped to code:

| Mechanism | Catalog ref | What it guarantees | Lands in |
|---|---|---|---|
| **Primitive declaration contract** | [11 §1](11_PRIMITIVE_CATALOG.md) | typed I/O, bounded args, PIT metadata, `data_requires`, cost class, provenance | `mt/genome/registry.py` (P1) |
| **Type system** | [11 §2](11_PRIMITIVE_CATALOG.md) | random wiring still type-checks (an op only connects to a compatible output) | `mt/genome/registry.py` + `schema.typecheck` (P1) |
| **Registration gate** | [11 §8](11_PRIMITIVE_CATALOG.md) | rejects leaky (`uses_future`), unbounded, untyped, or unsatisfiable primitives at the door | `registry.register()` (P1) |
| **Validation Gauntlet** | [05](05_VALIDATION_GAUNTLET.md) | trial-count-honest pruning of whatever the breadth produces | `mt/gauntlet/` (P2) |

The contract + gate are *front-door* filters (keep the space valid); the Gauntlet is the *back-door* filter (keep conclusions honest). Both are required before mass generation (P3).

## 2. Family → data → seed code → cost → phase (the master map)

Every feature family from [11 §3](11_PRIMITIVE_CATALOG.md), plus the operator stages. **Wave** = the registry build-order (§5). "Seed code" is the *first* implementation to wrap, never the ceiling.

| Family | `data_requires` | Seed code (wrap first) | cost | Wave / Phase |
|---|---|---|---|---|
| 3.1 Price & return | ohlcv | new (trivial) | cheap | W1 / P1 |
| 3.2 MA & trend | ohlcv | new; `adx` etc. | cheap | W1 / P1 |
| 3.3 Momentum & oscillators | ohlcv | `xsec/factors/momentum.py` | cheap | W1 / P1 |
| 3.4 Volatility | ohlcv | `atr_pct` (have); GARCH heavy | cheap–heavy | W1 / P1 (GARCH P3) |
| 3.5 Volume & participation | ohlcv (+quote vol) | `xsec/factors/flow.py` | cheap | W1 / P1 |
| 3.6 Microstructure & order flow | **trades, funding, oi** | `flow.py`, `carry.py`, `basis.py` | medium | W3 / P0-data + P3 |
| 3.7 Statistical & econometric | ohlcv | new (scipy/statsmodels) | med–heavy | W2 / P1 (coint/pca/hurst P3) |
| 3.8 Pattern & shape | ohlcv | `candlestick` (pandas_ta); DTW heavy | med | W2 / P1 (shapelet P3) |
| 3.9 SMC / ICT | ohlcv (+atr) | **`concepts/*` via `xsec/factors/smc.compute_smc_features`** | medium | W2 / P1 |
| 3.10 Cross-asset & intermarket | **multi-symbol, macro** | `Macro_Compass` gauge; multi-market join | medium | W3 / P0-data + P3 |
| 3.11 Cross-sectional | panel (multi-symbol) | `xsec/neutralize.py`, `combine.py` | cheap–med | W2 / P1 |
| 3.12 Regime, latent & ML-derived | ohlcv + **models** | `xsec/regime.py`, `SMC_ML` predictor | heavy | W4 / P4 |
| 3.13 Seasonality & calendar | datetime, **calendar** | `concepts/smc_sessions.py`; scanner `calendar_feed` | cheap | W2 (time) / P1; event P3 |
| 3.14 Macro / sentiment / positioning | **FRED, COT, GDELT, Finnhub** | Sentiment-Scanner `ingestion/*`; `Macro_Compass` | medium | W3 / P0-data + P3 |
| 3.15 **Auction Market Theory & order flow** | ohlcv (proxies) / **trades** (footprint) | new; `flow.cvd` as delta base | med–heavy | W2 (proxy) + W3 (footprint) / P1 + P3 |
| 3.16 Transform & combinator glue | — (polymorphic) | new | cheap | **W1 / P1 (early)** |
| §4 Signal ops | — | `combine.py`; `SMC_ML` learned head | cheap–med | P1 (basic); learned/regime P3–P4 |
| §5 Sizing ops | — | `xsec/portfolio.py` | cheap | P1 (basic); risk-parity live P5 |
| §6 Risk overlays | — | `trading/smc_trade.py`, `smc_tracker.py` | cheap | P1 (caps/horizon); `triple_barrier` P2; breakers P5 |
| §7 Meta genes | universe/regime feeds | `Past_Trading` (survivorship), `xsec/regime.py` | — | P0 (universe); `regime_filter` P4 |

Two structural notes that fall out of this table:
- **§3.16 glue must land in Phase 1, early.** It is the type-polymorphic connective tissue every generator leans on to interlink families "in ways no human enumerated" ([11 §3.16](11_PRIMITIVE_CATALOG.md)). Without it, breadth is a pile of disconnected features.
- **§3.9 SMC and §3.11 cross-sectional are nearly free** — they wrap existing, tested code (`compute_smc_features`, `neutralize.py`). They are early wins that also validate the "wrap, don't rewrite" boundary.

## 3. What the catalog demands of the data lake (the big Phase-0 expansion)

This is the "lot of it." My original P0 scoped OHLCV only; the catalog needs **six data classes**, each a free feed with a known adapter. Microstructure (§3.6) and AMT footprint (§3.15) in particular require **trade-level data**, which the thin slice does not yet ingest.

| Data class | Unlocks families | Free source | Adapter / seed code | Status |
|---|---|---|---|---|
| OHLCV bars | 3.1–3.5, 3.7–3.9, 3.11, AMT proxies | Binance dumps · OANDA v20 | `mt/adapters` workers | ✅ thin (synthetic) |
| **Trades / aggTrades** | 3.6, **3.15 footprint** | Binance aggTrades bulk dumps | new worker op → footprint/delta reconstruct | ⬜ P0 deepen |
| Funding + OI | 3.6 (`funding_z`, `oi_change`) | ccxt (Binance/Bybit) | `core/smc_data.py` (partial) | ◻ partial |
| Cross-asset levels | 3.10, `dollar_regime` | yfinance · OANDA · FRED · MEXC | `Macro_Compass` + multi-market join | ⬜ P0 deepen / P3 |
| Macro / positioning / news | 3.14 | FRED · CFTC COT · GDELT · Finnhub | Sentiment-Scanner `ingestion/*` | ⬜ P3 |
| Economic calendar | 3.13 `event_proximity` | scanner `calendar_feed` | Sentiment-Scanner | ⬜ P3 |

**Consequence:** trade/aggTrades ingestion moves *up* into P0 deepening, because it gates two whole families (microstructure + AMT footprint) and both are high-value. Everything is still survivorship-safe and content-hash-snapshotted per [08](08_INFRASTRUCTURE_AND_DATA.md).

## 4. Cross-phase dependencies (loops the catalog creates)

- **The model→feature loop (§3.12).** `hmm_regime`, `lgbm_prob`, `autoencoder_embed` are features *produced by* models that themselves consume features. So the regime classifier (`xsec/regime.py`) and `SMC_ML` predictor must exist (P4) before these primitives register — and once they do, genomes can wire a model's output as an input, feeding the next round of discovery. This is intended, and it is why P4 (self-improvement) is where the registry gets its most powerful members.
- **Meta genes need infrastructure (§7).** `universe` needs the survivorship-safe set (`Past_Trading`, P0); `regime_filter` needs the regime classifier (P4). Until then those genes take safe defaults.
- **Order-flow proxies now, footprint later (§3.15).** The proxy subset (bar-derivable) registers in P1; the footprint subset flips from `declared` to `computable` the moment aggTrades are in the lake — no genome rewrites, just newly-satisfiable `data_requires`.

## 5. Registry build-order (four waves)

Sequence the ~200-primitive target by *data availability*, not by family preference — no school of thought goes first:

1. **Wave 1 — OHLCV-cheap + glue (P1):** price/return, MA/trend, momentum, volatility, volume, **combinator glue (§3.16)**, basic signal/sizing/risk. Gets the generators wiring immediately.
2. **Wave 2 — OHLCV-rich (P1):** SMC/ICT (wrap `compute_smc_features`), cross-sectional (wrap `neutralize`/`combine`), statistical-lite, pattern-lite, **AMT proxies (§3.15 volume-profile/auction-state)**, session/time seasonality.
3. **Wave 3 — data-gated (P3, after P0 lake expansion):** microstructure on trades, **AMT footprint/delta**, cross-asset/intermarket, macro/COT/news/calendar. Also where the **Factor Miner** and **LLM** begin *authoring* new primitives through the §1 gate.
4. **Wave 4 — model-derived (P4):** regime/HMM/kmeans tags, ML win-prob, autoencoder embeddings — the model→feature loop, plus **novelty-targeted** sampling that biases the generators toward under-used families and **cost-class scheduling** in the simulator.

## 6. Per-phase deltas (what each phase now must include for the registry)

- **P0** — expand the lake to trades/aggTrades + funding/OI + cross-asset + macro/COT/news snapshots; content-hash each; build the survivorship universe (feeds meta `universe`).
- **P1** — implement the **primitive contract + type system + registration gate**; land Waves 1–2 (incl. SMC via `compute_smc_features` and **AMT proxies**); land the **combinator glue early**; seed signal/sizing/risk/meta ops.
- **P2** — add `triple_barrier` (risk + labeling); wire regime slicing (G5) using regime tags; the Gauntlet now prunes a *large* space — this is precisely why the referee is built before the tournament.
- **P3** — Wave 3 comes online with the data; the **Factor Miner mints IC-positive primitives** and the **LLM authors primitives from lessons**, both through the §1 gate; each mined/authored primitive is charged to the [trial count](05_VALIDATION_GAUNTLET.md#3-the-trial-count-ledger-the-honesty-backbone) and "no-story" ones get stricter OOS.
- **P4** — Wave 4 (model-derived features); **novelty targeting** biases primitive selection toward empty niches; **cost-class** drives simulator scheduling.
- **P5** — live risk overlays (`dd_circuit_breaker`, `corr_throttle`, `session_filter`) activate on the paper book.
- **P6** — continuous primitive addition + periodic population-level audits over the whole registry.

## 7. Status snapshot (thin slice → target)

| | Now (thin slice) | This change | Target |
|---|---|---|---|
| Contract | toy `OpSpec` (name/stage/args) | **full contract** (types, PIT, `data_requires`, cost_class, tags, provenance) + registration gate | [11 §1](11_PRIMITIVE_CATALOG.md) |
| Feature ops | 8 (momentum, reversion, ema_dist, rsi, realized_vol, breakout, atr_pct, funding_z) | +5 **AMT computable** (dist_to_poc, value_area_position, cumulative_delta, delta_divergence, rotation_factor) + declared family stubs | ~200, all families |
| Data | OHLCV synthetic | (unchanged this pass) | 6 data classes, real |
| Generator | samples all feature ops | **samples only computable + data-satisfiable** ops | type-directed + novelty-targeted |

The thin slice deliberately registers the AMT *proxy* subset as real compute (proving the family flows end-to-end through sim→gauntlet), declares the footprint subset as `data_requires: [trades]` pending the P0 lake expansion, and enforces the full contract so every future primitive — human, mined, or LLM-authored — enters through one honest door.
