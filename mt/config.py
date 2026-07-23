"""mt.config — paths, the market registry, and shared constants.

The market registry is the heart of the reuse strategy: each market names the
*root* of an existing stack (CC_Trading / FX_Trading) whose pure functions we call
inside an isolated subprocess. Because CC_Trading, FX_Trading and XAU_Trading each
define identically-named top-level packages (core/xsec/backtest/concepts), only one
root may ever be on a process's sys.path — hence one worker process per market.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# ─── repo + runtime paths ────────────────────────────────────────────────
MT_ROOT = Path(__file__).resolve().parent.parent          # c:/Users/Curieux/Master_Trader
PKG_ROOT = MT_ROOT / "mt"
VAR_DIR = MT_ROOT / "var"                                   # git-ignored runtime state
LAKE_DIR = VAR_DIR / "lake"                                 # Parquet feature lake
RUNS_DIR = VAR_DIR / "runs"                                 # per-run artifacts / reports
DB_PATH = VAR_DIR / "mt.db"                                 # registries + ledger + archive + lessons

for _d in (VAR_DIR, LAKE_DIR, RUNS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ─── the market registry ─────────────────────────────────────────────────
_TRADING = Path("c:/Users/Curieux/Trading")


@dataclass(frozen=True)
class Market:
    """A logical market and the isolated stack that provides its data/primitives."""
    name: str
    root: Path                     # sys.path root for the worker subprocess (has its own core/xsec/...)
    kind: str                      # "crypto" | "fx" | "metal"
    universe: List[str] = field(default_factory=list)
    htf: str = "4h"
    mtf: str = "1h"
    ltf: str = "15m"
    # cost defaults for costs.round_trip_cost (bps). Crypto has funding; OANDA is spread-as-fee.
    fee_bps_per_side: float = 5.0
    half_spread_bps: float = 2.0
    has_funding: bool = True


MARKETS: Dict[str, Market] = {
    # Crypto — CC_Trading is the "library" market: its pure costs/engine/gauntlet tooling
    # is imported directly into the mt process (it is the most complete stack).
    "crypto": Market(
        name="crypto",
        root=_TRADING / "CC_Trading",
        kind="crypto",
        universe=["BTC/USDT:USDT", "ETH/USDT:USDT", "SOL/USDT:USDT", "BNB/USDT:USDT",
                  "XRP/USDT:USDT", "DOGE/USDT:USDT", "ADA/USDT:USDT", "AVAX/USDT:USDT",
                  "LINK/USDT:USDT", "POL/USDT:USDT", "DOT/USDT:USDT", "LTC/USDT:USDT"],   # POL (ex-MATIC)
        fee_bps_per_side=5.0, half_spread_bps=2.0, has_funding=True,
    ),
    # FX — FX_Trading (OANDA REST, no ccxt). No cross-sectional engine of its own; the
    # mt Tier-1 executor + CC_Trading's cost model serve it. Symbols use OANDA underscores.
    "fx": Market(
        name="fx",
        root=_TRADING / "FX_Trading",
        kind="fx",
        universe=["EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD", "USD_CHF",
                  "NZD_USD", "EUR_JPY", "GBP_JPY", "EUR_GBP"],
        htf="H4", mtf="H1", ltf="M15",
        fee_bps_per_side=0.0, half_spread_bps=1.0, has_funding=False,
    ),
    # XAU — gold via OANDA (FX_Trading root, gold universe). XAU_Trading exists but is
    # incomplete; OANDA's XAU_USD is served by the same practice API.
    "xau": Market(
        name="xau",
        root=_TRADING / "FX_Trading",
        kind="metal",
        # A precious-metals cross-section (all real OANDA CFDs) so the Tier-1 book can form.
        # A single-instrument XAU book instead needs the per-symbol directional executor (Shape B).
        universe=["XAU_USD", "XAG_USD", "XPT_USD", "XPD_USD"],
        htf="H4", mtf="H1", ltf="M15",
        fee_bps_per_side=0.0, half_spread_bps=3.0, has_funding=False,
    ),
}

def available_feeds(market: str) -> set:
    """Data feeds a market can currently satisfy — the single source of truth shared by the
    template sampler AND the mutation operators, so no generator (template, random, OR evo)
    can attach a feature whose data the market lacks (which would compute all-NaN, waste the
    complexity budget, and over-report family coverage)."""
    feeds = {"ohlcv"}
    m = MARKETS[market]
    if m.has_funding:
        feeds.add("funding_rate")
    if m.kind == "crypto":
        feeds.add("taker_buy")               # Binance klines carry taker-buy volume + trade count
    feeds.add("cross_asset")                 # ingest attaches a benchmark ref_close (BTC / gold)
    feeds.update({"cot", "news", "calendar"})   # COT + GDELT + FairEconomy calendars
    return feeds


# CC_Trading is the stack whose pure libraries mt links directly (in-process).
LIBRARY_MARKET = "crypto"
LIBRARY_ROOT = MARKETS[LIBRARY_MARKET].root

# ─── reproducibility ─────────────────────────────────────────────────────
DEFAULT_SEED = 4242
DATA_SNAPSHOT_ID = "thin_slice_synthetic_v1"   # content-hash of a real lake in later phases
