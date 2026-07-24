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
import re
import zipfile
from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.ingest.http import session
from mt.ingest.binance import to_binance_symbol, to_ccxt_symbol, fetch_klines

DATA = "https://data.binance.vision/data/futures/um"
# The dump CDN is reachable from geo-blocked hosts (US GitHub runners) where the trading API
# returns HTTP 451; the S3 bucket also serves the symbol listing, so the whole crypto pipeline
# — universe, volume ranking, deep klines, funding — can run entirely off dumps.
S3_LIST = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
_KCOLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
          "qav", "count", "tbav", "tbqav", "ignore"]
_METAL_PERPS = frozenset({"XAUUSDT", "XAGUSDT", "XPTUSDT", "XPDUSDT"})   # traded separately as XAU market


def list_um_perp_symbols(quote: str = "USDT") -> List[str]:
    """All USD-M perpetual symbols, from the dump bucket's S3 listing (no trading API)."""
    prefix = "data/futures/um/monthly/klines/"
    out: List[str] = []
    token = None
    for _ in range(20):                                        # paginate via continuation-token
        params = {"delimiter": "/", "prefix": prefix, "list-type": "2"}
        if token:
            params["continuation-token"] = token
        try:
            r = session().get(S3_LIST, params=params, timeout=45)
        except Exception:
            break
        if r.status_code != 200:
            break
        out += re.findall(r"<Prefix>" + re.escape(prefix) + r"([^/]+)/</Prefix>", r.text)
        m = re.search(r"<NextContinuationToken>([^<]+)</NextContinuationToken>", r.text)
        if not m:
            break
        token = m.group(1)
    return [s for s in dict.fromkeys(out) if s.endswith(quote)]


def top_symbols_by_dump_volume(n: int = 100, exclude=_METAL_PERPS) -> List[str]:
    """Top-N USDT perps by recent QUOTE volume (≈ close·volume summed over the latest 1d dump),
    in ccxt symbol format. Geo-independent and less noisy than a 24h ticker snapshot. Falls back
    to nothing (caller uses config universe) only if the listing itself is unreachable."""
    syms = [s for s in list_um_perp_symbols("USDT") if s not in exclude]
    months = recent_months(2)                                 # oldest→newest; try newest first
    scored: List = []
    for s in syms:
        for mo in reversed(months):
            df = download_monthly_klines(s, "1d", mo)
            if df is not None and len(df):
                qv = float((df["close"] * df["volume"]).sum())
                if np.isfinite(qv) and qv > 0:
                    scored.append((s, qv))
                break
    scored.sort(key=lambda x: -x[1])
    return [to_ccxt_symbol(s) for s, _ in scored[:max(1, n)]]


def fetch_funding_dumps(symbol: str, months: int = 12) -> pd.DataFrame:
    """Funding-rate history from monthly fundingRate dumps (the trading API is geo-blocked)."""
    sym = to_binance_symbol(symbol)
    parts = []
    for mo in recent_months(months):
        url = f"{DATA}/monthly/fundingRate/{sym}/{sym}-fundingRate-{mo}.zip"
        try:
            r = session().get(url, timeout=60)
            if r.status_code != 200:
                continue
            z = zipfile.ZipFile(io.BytesIO(r.content))
            raw = z.read(z.namelist()[0])
            has_header = b"calc_time" in raw[:64] or b"funding" in raw[:64]
            df = pd.read_csv(io.BytesIO(raw)) if has_header else pd.read_csv(
                io.BytesIO(raw), header=None, names=["calc_time", "funding_interval_hours", "last_funding_rate"])
            tcol = next((c for c in df.columns if "time" in str(c).lower()), df.columns[0])
            rcol = next((c for c in df.columns if "rate" in str(c).lower()), df.columns[-1])
            t = pd.to_numeric(df[tcol], errors="coerce")
            out = pd.DataFrame({
                "datetime": pd.to_datetime(t, unit="us" if t.iloc[-1] > 1e15 else "ms", utc=True),
                "funding_rate": pd.to_numeric(df[rcol], errors="coerce")})
            parts.append(out.dropna())
        except Exception:
            continue
    if not parts:
        return pd.DataFrame(columns=["datetime", "funding_rate"])
    return pd.concat(parts, ignore_index=True).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)


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
    try:                                                       # current (incomplete) month via REST
        tail = fetch_klines(symbol, interval, limit=1500)      # geo-blocked (451) on US runners →
        if len(tail):                                          # best-effort: dumps alone are enough
            parts.append(tail)
    except Exception:
        pass
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out = out.dropna(subset=["close"]).drop_duplicates("datetime").sort_values("datetime")
    return out.reset_index(drop=True)
