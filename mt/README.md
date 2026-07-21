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
# full loop across all three markets (generate → sim → ledger → gauntlet → archive)
python -m mt.run_demo --bars 600

# fast unit smoke tests (no subprocess / no network)
python -m pytest tests/ -q
```

Runtime deps for the demo are already in the base env (pandas / numpy / scipy / pyarrow +
stdlib sqlite3). The heavier stack (`ccxt`, `duckdb`, `polars`, `deap`, `gplearn`, `faiss`)
is added per phase — see `../requirements.txt`.

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
| Data (normalized panel + Parquet lake) | `mt/data/` + `mt/adapters/` | ✅ synthetic/isolated; real ingestion deferred |
| Genome DSL (typed, hash, mutate/crossover, to_prose) | `mt/genome/` | ✅ seed vocabulary |
| Tier-1 simulator (genome-driven, cost-aware) | `mt/sim/` | ✅ Tier 1; Tier 2/3 deferred |
| Gauntlet (G1 + real G4 DSR + real G5 bootstrap) | `mt/gauntlet/` | ✅ G1/G4/G5; G2/G3/G6/G7/G8 deferred |
| Registries (Genome Registry + Result Ledger) | `mt/store/` | ✅ SQLite `var/mt.db` |
| MAP-Elites archive | `mt/archive/` | ✅ niche occupy/replace |
| Generators (templates + fully-random) | `mt/generators/` | ✅ Engine D; A/B/C deferred |
| Driver | `mt/run_demo.py` | ✅ end-to-end |

## What is real vs. deferred (no hidden magic)

**Real:** subprocess isolation across 3 markets · content-hashed genome dedup · the honest
Result-Ledger trial count feeding **CC_Trading's actual Deflated-Sharpe** (Bailey & López
de Prado) · **CC_Trading's actual stationary bootstrap** · MAP-Elites occupy/replace.

**Deferred (labeled in code):** real Binance/OANDA ingestion (currently deterministic
synthetic data) · gauntlet gates **G2** purged-WF, **G3 CPCV→PBO** (the genuinely-new
piece), **G6** transfer, **G7** capacity, **G8** orthogonality · Tier 2/3 simulators · the
per-symbol/directional executor (Shape B, needed for single-instrument books) · Engines
A/B/C · self-improvement loop · live/paper layer.

On the current **synthetic, edgeless** data the correct outcome is that the gauntlet
rejects ~everything — "far more rejections than discoveries" is the immune system working
(docs/00 §2), not a failure.

## Next deepening steps (in order)

1. **Real data lake** — wire CC_Trading's ccxt fetch + OANDA REST into the workers; write
   content-hashed Parquet snapshots; re-derive the survivorship universe.
2. **P1 reproduction gate** — cross-check the Tier-1 executor against `backtest/engine.py`
   on crypto; encode 3–5 known SMC strategies as genomes and match their backtests.
3. **P2 gauntlet** — implement **CPCV → PBO** and wire `purged_cv.py` (G2), regime slicing
   (G5), transfer (G6), capacity (G7), orthogonality (G8); prove it flags a deliberately
   overfit genome (the critical go/no-go).
