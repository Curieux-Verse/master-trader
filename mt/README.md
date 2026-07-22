# `mt/` — Master Trader implementation

The meta-layer factory that manufactures, simulates, validates, archives, and (later)
self-improves trading strategies expressed as typed **genomes**. It sits *above* the
existing per-market stacks and reuses their battle-tested pure functions — it does not
rewrite them.

This is the **thin end-to-end slice** (per the approved plan): every stage of the loop is
wired and runs across **crypto + FX + XAU** in one process, with the deepest new pieces
stubbed and clearly labeled. The point of a thin slice is to prove the integration —
especially the hardest risk, the package-namespace isolation — before deepening any stage.

## Run it

```bash
# THE COMPLETE SYSTEM: inner discovery loop (×gens ×markets) + outer paper loop + report
python -m mt.run_system --generations 4 --markets crypto,fx,xau --structure 0.8

# the critical go/no-go: proves the gauntlet catches an overfit AND admits a real edge
python -m mt.selftest_gauntlet

# the thin single-pass demo (generate → sim → ledger → gauntlet → archive, one batch/market)
python -m mt.run_demo --bars 600

# test suite (22 tests incl. the trustworthiness gate and a full-loop smoke)
python -m pytest tests/ -q
```

`--structure 0` runs on pure random walks (honest baseline — the archive stays empty, which
is the immune system working). `--structure > 0` injects a *labeled* synthetic edge so the
discovery machinery has genuine planted structure to find, validate, archive, and paper-trade.

Runtime deps are already in the base env (pandas / numpy / scipy / pyarrow + stdlib sqlite3).
The heavier stack (`ccxt`, `duckdb`, `polars`, `deap`, `gplearn`, `faiss`) is only needed for
real-data ingestion and is added per `../requirements.txt`.

## How the reuse works (the crux)

`CC_Trading`, `FX_Trading`, and `XAU_Trading` each define identically-named top-level
packages (`core`, `xsec`, `backtest`, `concepts`), so **only one may be on a process's
`sys.path` at a time.** Two mechanisms resolve this:

- **Subprocess isolation** (`mt/adapters/_market_worker.py` + `market.py`) — each market's
  data is built inside its own process with that stack's root on `PYTHONPATH`; the worker
  ships a compact result back. This is the *only* safe way to touch >1 stack per run, and
  it matches the "one CLI job per market" pattern the scanners already use.
- **One in-process library boundary** (`mt/adapters/cclib.py`) — CC_Trading is the
  "library" market; its pure cost model, stationary bootstrap, and Deflated Sharpe are
  imported in-process (the only place a market root joins `mt`'s `sys.path`). FX/XAU are
  *never* imported in-process, which keeps the clash impossible.

## The loop, module by module

| Stage | Module | Status |
|---|---|---|
| Data (normalized panel + Parquet lake, isolated workers) | `mt/data/` + `mt/adapters/` | ✅ isolated/synthetic (labeled edge knob); real ingestion deferred |
| Genome DSL + full primitive contract + registration gate | `mt/genome/` | ✅ typed I/O, PIT, data_requires, cost, provenance |
| Primitive registry (~16 families, incl. Auction Market Theory) | `mt/genome/registry.py` + `mt/sim/features.py` | ✅ 50+ primitives; ~40 computable across all major families |
| Simulator — Tier-1 cross-sectional + Tier-2 directional (triple-barrier) | `mt/sim/` | ✅ both phenotypes; Tier-3 tick deferred |
| Gauntlet — G1/G2/G3(CPCV→PBO)/G4(correct DSR)/G5/G6/G7/G8 | `mt/gauntlet/` | ✅ all enforced (cheap→expensive); regime-slice pending labels |
| Registries — Genome Registry + Result Ledger (+ σ_SR) | `mt/store/` | ✅ SQLite `var/mt.db` |
| MAP-Elites archive (behavioral niching) | `mt/archive/` | ✅ occupy/replace |
| Generators — templates + random + evolution + factor miner + critic | `mt/generators/` + `mt/improve/` | ✅ Engines A/B/C/D |
| Self-improvement — NSGA-II + bandit + critic + Lesson Library | `mt/improve/` | ✅ inner discovery loop |
| Live/paper — shadow + regime allocator + drift + circuit breakers | `mt/live/` | ✅ R1 paper only (no capital) |
| Drivers — complete system, thin demo, gauntlet self-test | `mt/run_system.py`, `mt/run_demo.py`, `mt/selftest_gauntlet.py` | ✅ end-to-end |

## What is real vs. deferred (no hidden magic)

**Real (runs end-to-end today):** subprocess isolation across 3 markets · content-hashed
genome dedup · the full **primitive declaration contract** + registration gate · a
no-privilege registry spanning ~16 families (trend/oscillator/volatility/volume/statistical/
pattern/**Auction Market Theory**/microstructure) with ~40 computable primitives · **both
phenotypes** (cross-sectional rank book + directional triple-barrier) · the **full gauntlet**
G1–G8 including the genuinely-new **CPCV→PBO** and a **corrected Deflated Sharpe** (mt's own —
CC_Trading's was ~30× too strict for a return series) fed by the ledger's honest trial count
and cross-trial σ_SR · **CC_Trading's actual stationary bootstrap** · MAP-Elites archive ·
**self-improvement** (NSGA-II evolution + IC factor-miner that mints new primitives + a critic
that writes lessons and targeted fixes + a Thompson bandit that learns which engine to fund) ·
**paper/shadow** with a regime-aware Hedge allocator, Page-Hinkley + rolling-PSR drift, and
circuit breakers · a daily written report. The **gauntlet self-test proves it catches a
deliberately-overfit strategy AND admits a genuine injected edge.**

**Deferred (labeled in code):** real Binance/OANDA ingestion incl. **trades/aggTrades**
(currently synthetic; trades unlock microstructure + AMT footprint — docs/12 §3) · declared-
only families (SMC via `compute_smc_features`, cross-asset, macro/COT/news, ML-derived)
awaiting their data/wrappers · Tier-3 tick simulator · regime-sliced G5 (needs regime labels)
· R2/R3 live capital (a deliberate human decision, never the machine's).

On the current **synthetic, edgeless** data the correct outcome is that the gauntlet
rejects ~everything — "far more rejections than discoveries" is the immune system working
(docs/00 §2), not a failure.

## Next deepening steps (in order)

1. **Real data lake (expanded scope, per docs/12 §3)** — wire CC_Trading's ccxt fetch +
   OANDA REST into the workers **and add trades/aggTrades ingestion** (Binance bulk dumps),
   which unlocks the microstructure + Auction-Market-Theory *footprint* families; write
   content-hashed Parquet snapshots; re-derive the survivorship universe.
2. **P1 reproduction gate** — cross-check the Tier-1 executor against `backtest/engine.py`
   on crypto; encode 3–5 known SMC strategies as genomes and match their backtests.
3. **P2 gauntlet** — implement **CPCV → PBO** and wire `purged_cv.py` (G2), regime slicing
   (G5), transfer (G6), capacity (G7), orthogonality (G8); prove it flags a deliberately
   overfit genome (the critical go/no-go).
