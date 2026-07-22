"""mt.ingest.binance — real crypto OHLCV + funding from Binance USD-M futures (no auth).

Uses the public REST endpoints (klines up to 1500/call, fundingRate history). The current
forming candle is dropped (closed-bar rule). Funding is aligned to bars with a backward
as-of merge (funding accrues on the position held into each bar).
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

FAPI = "https://fapi.binance.com/fapi/v1"


def to_binance_symbol(symbol: str) -> str:
    """ccxt-style 'BTC/USDT:USDT' → Binance 'BTCUSDT'."""
    return symbol.split(":")[0].replace("/", "").replace("-", "")


def to_ccxt_symbol(binance_symbol: str) -> str:
    """Binance 'BTCUSDT' → ccxt-style 'BTC/USDT:USDT' (USDT-margined perp)."""
    base = binance_symbol[:-4] if binance_symbol.endswith("USDT") else binance_symbol
    return f"{base}/USDT:USDT"


@lru_cache(maxsize=1)
def _coin_perp_symbols() -> frozenset:
    """USDT-margined perps whose underlying is actually a COIN (excludes the tokenized
    EQUITY/COMMODITY 'TradFi' perps Binance now lists) and is TRADING."""
    info = get_json(f"{FAPI}/exchangeInfo")
    return frozenset(
        s["symbol"] for s in info.get("symbols", [])
        if s.get("underlyingType") == "COIN" and s.get("contractType") == "PERPETUAL"
        and s.get("status") == "TRADING" and s["symbol"].endswith("USDT")
    )


def top_symbols_by_volume(n: int = 50, coin_only: bool = True) -> List[str]:
    """Top-N USDT perps by 24h quote (dollar) volume, in ccxt symbol format.

    coin_only (default) restricts to real crypto — the venue's top-volume list otherwise
    includes tokenized stocks/commodities (SNDK, SOXL, XAUUSDT, …). Survivorship-safe by
    construction: it reflects what is *currently* liquid; delisted names simply aren't here."""
    tickers = get_json(f"{FAPI}/ticker/24hr")
    valid = _coin_perp_symbols() if coin_only else None
    rows = [(t["symbol"], float(t.get("quoteVolume", 0.0))) for t in tickers
            if t["symbol"].endswith("USDT") and (valid is None or t["symbol"] in valid)]
    rows.sort(key=lambda x: x[1], reverse=True)
    return [to_ccxt_symbol(sym) for sym, _ in rows[:max(1, n)]]


def fetch_klines(symbol: str, interval: str, limit: int = 1500) -> pd.DataFrame:
    raw = get_json(f"{FAPI}/klines",
                   params={"symbol": to_binance_symbol(symbol), "interval": interval, "limit": min(limit, 1500)})
    if not raw:
        return pd.DataFrame()
    df = pd.DataFrame(raw, columns=["open_time", "open", "high", "low", "close", "volume",
                                    "close_time", "qav", "trades", "tbav", "tqav", "ignore"])
    for c in ("open", "high", "low", "close", "volume", "tbav"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["trade_count"] = pd.to_numeric(df["trades"], errors="coerce")
    df["taker_buy_volume"] = df["tbav"]                      # aggressive-buy base volume → real order flow
    df["datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    now_ms = pd.Timestamp.utcnow().value // 1_000_000
    df = df[df["close_time"] <= now_ms]                      # drop the still-forming candle
    return df[["datetime", "open", "high", "low", "close", "volume",
               "taker_buy_volume", "trade_count"]].reset_index(drop=True)


def fetch_funding(symbol: str, limit: int = 1000) -> pd.DataFrame:
    try:
        raw = get_json(f"{FAPI}/fundingRate",
                       params={"symbol": to_binance_symbol(symbol), "limit": min(limit, 1000)})
    except Exception:
        return pd.DataFrame(columns=["datetime", "funding_rate"])
    if not raw:
        return pd.DataFrame(columns=["datetime", "funding_rate"])
    df = pd.DataFrame(raw)
    df["datetime"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
    df["funding_rate"] = pd.to_numeric(df["fundingRate"], errors="coerce")
    return df[["datetime", "funding_rate"]].sort_values("datetime").reset_index(drop=True)


def build_frame(symbol: str, interval: str, limit: int = 1500, with_funding: bool = True) -> pd.DataFrame:
    df = fetch_klines(symbol, interval, limit)
    if df.empty:
        return df
    if with_funding:
        fr = fetch_funding(symbol)
        if not fr.empty:
            df = pd.merge_asof(df.sort_values("datetime"), fr, on="datetime", direction="backward")
    if "funding_rate" not in df.columns:
        df["funding_rate"] = np.nan
    return df
