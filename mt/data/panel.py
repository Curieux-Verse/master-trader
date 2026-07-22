"""mt.data.panel — the normalized, market-agnostic panel contract.

A NormPanel is the single working form every market resolves to. It deliberately
mirrors CC_Trading's xsec.panel.Panel shape (per-symbol multi-timeframe frames + a
cross-sectional snapshot indexed by symbol) so the mt Tier-1 executor can cross-check
against the native engine, but it is produced identically for crypto / FX / XAU.

On disk (the lake):
    var/lake/<snapshot_id>/<market>/<SYMBOL>__<tf>.parquet
with a per-market manifest.json listing the frames. Symbols are filename-escaped
(``/`` and ``:`` → ``-``) so ccxt-style ``BTC/USDT:USDT`` round-trips safely.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

FRAME_COLS = ["datetime", "open", "high", "low", "close", "volume", "atr_14", "funding_rate",
              "taker_buy_volume", "trade_count",   # → real bar-level order flow (Binance)
              "ref_close",                          # benchmark close (BTC / gold) → cross-asset
              "fp_stacked", "fp_absorption"]        # tick footprint (aggTrades) → stacked imbalance / absorption
SNAPSHOT_COLS = ["close", "ret_1", "atr_pct", "quote_volume_usd", "funding_rate"]


def escape_symbol(symbol: str) -> str:
    """Filesystem-safe symbol token (ccxt 'BTC/USDT:USDT' -> 'BTC-USDT-USDT')."""
    return symbol.replace("/", "-").replace(":", "-")


@dataclass
class NormPanel:
    """As-known-at-`asof` normalized market view."""
    market: str
    asof: datetime
    snapshot_id: str
    symbols: List[str] = field(default_factory=list)
    frames: Dict[str, Dict[str, pd.DataFrame]] = field(default_factory=dict)  # symbol -> {tf: OHLCV df}
    snapshot: pd.DataFrame = field(default_factory=pd.DataFrame)               # index=symbol, cols=SNAPSHOT_COLS
    timeframes: Dict[str, str] = field(default_factory=dict)                   # {"htf","mtf","ltf"} -> tf label
    _mat_cache: Dict = field(default_factory=dict, repr=False, compare=False)  # (field, tf) -> matrix

    @property
    def primary_tf(self) -> Optional[str]:
        return self.timeframes.get("htf")

    def invalidate_cache(self) -> None:
        self._mat_cache.clear()

    def close_matrix(self, tf: Optional[str] = None) -> pd.DataFrame:
        """[time x symbol] close matrix at a timeframe — the Tier-1 working form (cached)."""
        return self.field_matrix("close", tf)

    def field_matrix(self, field_name: str, tf: Optional[str] = None) -> pd.DataFrame:
        """[time x symbol] matrix for one OHLCV field (cached — built once per panel).

        The panel is read-only during a run, so caching turns the ~dozen matrix rebuilds a
        single genome triggers (and every CPCV variant's) into one construction each."""
        tf = tf or self.primary_tf
        key = (field_name, tf)
        cached = self._mat_cache.get(key)
        if cached is not None:
            return cached
        cols = {}
        for sym, tfs in self.frames.items():
            df = tfs.get(tf)
            if df is None or df.empty or field_name not in df.columns:
                continue
            cols[sym] = pd.Series(df[field_name].to_numpy(), index=pd.to_datetime(df["datetime"]))
        mat = pd.DataFrame(cols).sort_index() if cols else pd.DataFrame()
        self._mat_cache[key] = mat
        return mat


# ─── lake IO ─────────────────────────────────────────────────────────────


def frame_path(lake_dir: Path, snapshot_id: str, market: str, symbol: str, tf: str) -> Path:
    return lake_dir / snapshot_id / market / f"{escape_symbol(symbol)}__{tf}.parquet"


def write_frame(lake_dir: Path, snapshot_id: str, market: str, symbol: str, tf: str, df: pd.DataFrame) -> Path:
    p = frame_path(lake_dir, snapshot_id, market, symbol, tf)
    p.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    for c in FRAME_COLS:
        if c not in out.columns:
            out[c] = np.nan
    out = out[FRAME_COLS]
    out.to_parquet(p, index=False)
    return p


def read_frame(path: str | Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    return df


def build_snapshot_from_frames(frames: Dict[str, Dict[str, pd.DataFrame]], primary_tf: str) -> pd.DataFrame:
    """Cross-sectional snapshot (index=symbol) from the latest closed bar of each symbol."""
    rows: Dict[str, dict] = {}
    for sym, tfs in frames.items():
        df = tfs.get(primary_tf)
        if df is None or len(df) < 2:
            continue
        last = df.iloc[-1]
        prev = df.iloc[-2]
        close = float(last["close"])
        prev_close = float(prev["close"])
        atr = float(last.get("atr_14", np.nan))
        rows[sym] = {
            "close": close,
            "ret_1": (close / prev_close - 1.0) if prev_close > 0 else np.nan,
            "atr_pct": (atr / close) if (close > 0 and np.isfinite(atr)) else np.nan,
            "quote_volume_usd": float(last.get("volume", np.nan)) * close,
            "funding_rate": float(last.get("funding_rate", np.nan)),
        }
    snap = pd.DataFrame.from_dict(rows, orient="index").reindex(columns=SNAPSHOT_COLS)
    snap.index.name = "symbol"
    return snap


def load_norm_panel(manifest: dict, timeframes: Dict[str, str]) -> NormPanel:
    """Reconstruct a NormPanel from a worker manifest (see mt.adapters)."""
    frames: Dict[str, Dict[str, pd.DataFrame]] = {}
    for f in manifest.get("frames", []):
        frames.setdefault(f["symbol"], {})[f["tf"]] = read_frame(f["path"])
    primary = timeframes.get("htf")
    snap = build_snapshot_from_frames(frames, primary) if primary else pd.DataFrame()
    asof = manifest.get("asof")
    asof_dt = pd.to_datetime(asof, utc=True).to_pydatetime() if asof else datetime.now(timezone.utc)
    return NormPanel(
        market=manifest["market"],
        asof=asof_dt,
        snapshot_id=manifest["snapshot_id"],
        symbols=sorted(frames.keys()),
        frames=frames,
        snapshot=snap,
        timeframes=timeframes,
    )
