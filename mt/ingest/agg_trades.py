"""mt.ingest.agg_trades — tick-level footprint from Binance aggTrades (docs/11 §3.15).

The one family that genuinely needs trades, not bars: price-level footprint imbalance and
absorption. Daily aggTrades dumps are 2–20 MB each (a month is ~700 MB), so this is a
BOUNDED enrichment — fetch recent days for a few symbols, reconstruct per-bar footprint, and
write footprint columns onto those bars. Older bars keep NaN footprint (the feature is inert
there and simply skipped), so it lights up the family for recent/live analysis without a
multi-GB backfill.
"""
from __future__ import annotations

import io
import zipfile
from datetime import date, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.ingest.http import session
from mt.ingest.binance import to_binance_symbol

DATA = "https://data.binance.vision/data/futures/um"
_ACOLS = ["agg_id", "price", "qty", "first_id", "last_id", "transact_time", "is_buyer_maker"]


def download_daily_aggtrades(symbol: str, day: date) -> Optional[pd.DataFrame]:
    sym = to_binance_symbol(symbol)
    url = f"{DATA}/daily/aggTrades/{sym}/{sym}-aggTrades-{day.isoformat()}.zip"
    try:
        r = session().get(url, timeout=180)
        if r.status_code != 200:
            return None
        z = zipfile.ZipFile(io.BytesIO(r.content))
        raw = z.read(z.namelist()[0])
        has_header = b"agg_trade_id" in raw[:64] or b"transact_time" in raw[:200]
        df = pd.read_csv(io.BytesIO(raw)) if has_header else pd.read_csv(io.BytesIO(raw), header=None, names=_ACOLS)
        df.columns = _ACOLS[:len(df.columns)]
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
        tt = pd.to_numeric(df["transact_time"], errors="coerce")
        df["datetime"] = pd.to_datetime(tt, unit="us" if tt.iloc[-1] > 1e15 else "ms", utc=True)
        df["is_buyer_maker"] = df["is_buyer_maker"].astype(str).str.lower().isin(["true", "1"])
        return df[["datetime", "price", "qty", "is_buyer_maker"]]
    except Exception:
        return None


def _bar_footprint(trades: pd.DataFrame, levels: int = 12) -> dict:
    """Per-bar footprint stats from one bar's trades. is_buyer_maker=False ⇒ aggressive buy."""
    if trades.empty:
        return {"delta": np.nan, "stacked_imbalance": np.nan, "absorption": np.nan}
    buy = np.where(~trades["is_buyer_maker"], trades["qty"], 0.0)
    sell = np.where(trades["is_buyer_maker"], trades["qty"], 0.0)
    delta = float(buy.sum() - sell.sum())
    total = float(buy.sum() + sell.sum())
    # price-level footprint: bin trades, per-level imbalance, longest lopsided run
    p = trades["price"].to_numpy()
    lo, hi = p.min(), p.max()
    stacked = 0
    if hi > lo:
        idx = np.clip(((p - lo) / (hi - lo) * (levels - 1)).astype(int), 0, levels - 1)
        run = 0
        for lv in range(levels):
            m = idx == lv
            b, s = buy[m].sum(), sell[m].sum()
            imb = (b - s) / (b + s) if (b + s) > 0 else 0.0
            if abs(imb) > 0.6:
                run += 1; stacked = max(stacked, run)
            else:
                run = 0
    # absorption: a lot of aggressive volume that barely moved price (into a passive wall)
    rng = (hi - lo) / p[-1] if p[-1] else 0.0
    absorption = float(abs(delta) / total) if (total > 0 and rng < 0.002) else 0.0
    return {"delta": delta, "stacked_imbalance": float(stacked), "absorption": absorption}


def bar_footprint_frame(symbol: str, tf_minutes: int, days: int = 5, levels: int = 12) -> pd.DataFrame:
    """Per-bar footprint (real_delta, stacked_imbalance, absorption) for the last `days` days."""
    parts = []
    for d in range(days, 0, -1):
        day = date.today() - timedelta(days=d)
        at = download_daily_aggtrades(symbol, day)
        if at is not None and len(at):
            parts.append(at)
    if not parts:
        return pd.DataFrame(columns=["datetime", "real_delta", "stacked_imbalance", "absorption"])
    trades = pd.concat(parts, ignore_index=True).sort_values("datetime")
    freq = f"{tf_minutes}min"
    rows = []
    for bar_time, grp in trades.groupby(trades["datetime"].dt.floor(freq)):
        fp = _bar_footprint(grp, levels)
        rows.append({"datetime": bar_time, "real_delta": fp["delta"],
                     "stacked_imbalance": fp["stacked_imbalance"], "absorption": fp["absorption"]})
    return pd.DataFrame(rows)
