"""mt.ingest.binance_dumps — deep history from Binance public bulk dumps (docs/08 §1).

The REST baseline gives ~1500 recent bars; the DSR needs more for statistical power. The
free monthly klines dumps (data.binance.vision) extend HTF history to years — and they carry
**taker-buy volume + trade count**, so real bar-level order flow (CVD / delta / aggressor
ratio / OFI / intensity) comes for free across all of it. Tick-level aggTrades (for footprint
imbalance/absorption) are downloaded separately and only for a bounded validation window,
since a single month can be ~700 MB.
"""
from __future__ import annotations

import io
import zipfile
from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.ingest.http import session
from mt.ingest.binance import to_binance_symbol, fetch_klines

DATA = "https://data.binance.vision/data/futures/um"
_KCOLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
          "qav", "count", "tbav", "tbqav", "ignore"]


def recent_months(n: int) -> List[str]:
    """The n completed calendar months before the current one, as 'YYYY-MM' (oldest first)."""
    y, m = date.today().year, date.today().month
    out = []
    for _ in range(n):
        m -= 1
        if m == 0:
            m = 12; y -= 1
        out.append(f"{y:04d}-{m:02d}")
    return list(reversed(out))


def _parse_klines_csv(raw: bytes) -> pd.DataFrame:
    if b"open_time" in raw[:64]:                             # newer dumps ship a header row
        df = pd.read_csv(io.BytesIO(raw))
        tb_col, cnt_col = "taker_buy_volume", "count"
    else:
        df = pd.read_csv(io.BytesIO(raw), header=None, names=_KCOLS)
        tb_col, cnt_col = "tbav", "count"
    for c in ("open", "high", "low", "close", "volume"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    ot = pd.to_numeric(df["open_time"], errors="coerce")     # ms or µs depending on vintage
    unit = "us" if ot.iloc[-1] > 1e15 else "ms"
    df["datetime"] = pd.to_datetime(ot, unit=unit, utc=True)
    df["taker_buy_volume"] = pd.to_numeric(df[tb_col], errors="coerce")
    df["trade_count"] = pd.to_numeric(df[cnt_col], errors="coerce")
    return df[["datetime", "open", "high", "low", "close", "volume", "taker_buy_volume", "trade_count"]]


def download_monthly_klines(symbol: str, interval: str, month: str) -> Optional[pd.DataFrame]:
    sym = to_binance_symbol(symbol)
    url = f"{DATA}/monthly/klines/{sym}/{interval}/{sym}-{interval}-{month}.zip"
    try:
        r = session().get(url, timeout=90)
        if r.status_code != 200:
            return None
        z = zipfile.ZipFile(io.BytesIO(r.content))
        return _parse_klines_csv(z.read(z.namelist()[0]))
    except Exception:
        return None


def build_deep_klines(symbol: str, interval: str, months: int = 24) -> pd.DataFrame:
    """Concatenate `months` of monthly dumps + the current partial month via REST; dedup."""
    parts = []
    for mo in recent_months(months):
        df = download_monthly_klines(symbol, interval, mo)
        if df is not None and len(df):
            parts.append(df)
    tail = fetch_klines(symbol, interval, limit=1500)          # current (incomplete) month
    if len(tail):
        parts.append(tail)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out = out.dropna(subset=["close"]).drop_duplicates("datetime").sort_values("datetime")
    return out.reset_index(drop=True)
