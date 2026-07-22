"""mt.ingest.lake — build the content-hashed Parquet lake from real feeds.

Writes the SAME NormPanel frame contract the synthetic worker uses, plus a `_snapshot.json`
manifest with a content hash, so any backtest is reproducible against a named snapshot
(docs/08 §4). Reading needs no market stack (it's just Parquet), so panels load in-process
with no isolation dance — the subprocess isolation only mattered for importing a market's
code, which ingestion here sidesteps by going straight to the public endpoints.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.config import LAKE_DIR, MARKETS
from mt.data.panel import write_frame, FRAME_COLS
from mt.ingest import binance, oanda


@dataclass
class IngestResult:
    market: str
    snapshot_id: str
    source: str
    symbols: List[str]
    timeframes: dict
    total_rows: int
    content_hash: str
    frames: int


def _atr(df: pd.DataFrame, window: int = 14) -> np.ndarray:
    high, low, close = df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy()
    prev = np.concatenate([[close[0]], close[:-1]])
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev), np.abs(low - prev)))
    return pd.Series(tr).rolling(window, min_periods=1).mean().to_numpy()


def _fetch(market: str, symbol: str, tf: str, bars: int) -> pd.DataFrame:
    if MARKETS[market].kind == "crypto":
        return binance.build_frame(symbol, tf, limit=bars, with_funding=True)
    return oanda.build_frame(symbol, tf, count=bars)          # fx / metal → OANDA


def ingest_market(market: str, *, bars: int = 1500, snapshot_id: str = "real",
                  symbols: Optional[List[str]] = None, min_bars: int = 120,
                  log=print) -> IngestResult:
    m = MARKETS[market]
    tfs = {"htf": m.htf, "mtf": m.mtf, "ltf": m.ltf}
    syms = symbols or m.universe
    source = "binance_fapi" if m.kind == "crypto" else "oanda_v20"

    frames_meta = []
    hasher = hashlib.sha256()
    total_rows = 0
    kept: List[str] = []
    for sym in syms:
        sym_ok = False
        for tf in tfs.values():
            try:
                df = _fetch(market, sym, tf, bars)
            except Exception as e:
                log(f"    [{market}] {sym} {tf}: fetch error ({type(e).__name__}: {str(e)[:60]})")
                continue
            if df is None or len(df) < min_bars:
                continue
            df = df.copy()
            df["atr_14"] = _atr(df, 14)
            for c in FRAME_COLS:
                if c not in df.columns:
                    df[c] = np.nan
            path = write_frame(LAKE_DIR, snapshot_id, market, sym, tf, df)
            n = int(len(df))
            total_rows += n
            sym_ok = True
            last = df.iloc[-1]
            hasher.update(f"{sym}|{tf}|{n}|{df['datetime'].iloc[0]}|{df['datetime'].iloc[-1]}|"
                          f"{round(float(last['close']), 6)}".encode())
            frames_meta.append({"symbol": sym, "tf": tf, "path": str(path), "rows": n})
        if sym_ok:
            kept.append(sym)
        log(f"    [{market}] {sym}: {'ok' if sym_ok else 'skipped (insufficient data)'}")

    content_hash = hasher.hexdigest()[:16]
    manifest = {
        "market": market, "snapshot_id": snapshot_id, "source": source,
        "asof": datetime.now(timezone.utc).isoformat(), "timeframes": tfs,
        "symbols": kept, "total_rows": total_rows, "content_hash": content_hash,
        "frames": frames_meta,
    }
    out_dir = LAKE_DIR / snapshot_id / market
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_snapshot.json").write_text(json.dumps(manifest, indent=2))
    return IngestResult(market, snapshot_id, source, kept, tfs, total_rows, content_hash, len(frames_meta))
