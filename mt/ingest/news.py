"""mt.ingest.news — GDELT news tone timeline (docs/08, docs/11 §3.14).

Average article tone per day from GDELT's free DOC 2.0 API (the feed the sentiment scanners
use). GDELT rate-limits to one request / 5 s, so requests are spaced; the backoff in
mt.ingest.http also treats 429 as retryable. Tone history goes back years, so it aligns to
deep history for the mapped assets; unmapped symbols are left NaN (feature skipped).
"""
from __future__ import annotations

import time
from typing import Optional

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

GDELT = "https://api.gdeltproject.org/api/v2/doc/doc"

_NEWS_QUERY = {
    "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "XRP": "ripple xrp", "DOGE": "dogecoin",
    "BNB": "binance coin", "ADA": "cardano", "LINK": "chainlink", "AVAX": "avalanche crypto",
    "XAU": "gold price", "XAG": "silver price", "XPT": "platinum price", "XPD": "palladium price",
    "EUR": "euro dollar exchange", "GBP": "british pound sterling", "JPY": "japanese yen",
    "AUD": "australian dollar", "CAD": "canadian dollar", "CHF": "swiss franc", "NZD": "new zealand dollar",
}


def news_key(symbol: str) -> str:
    s = symbol.split("/")[0].split(":")[0]
    if "_" in s:
        parts = s.split("_")
        non_usd = [p for p in parts if p != "USD"]
        return non_usd[0] if non_usd else parts[0]
    return s


def fetch_news_tone(symbol: str, months: int = 18, polite_delay: float = 5.5) -> Optional[pd.DataFrame]:
    """Daily (datetime, news_tone) average article tone; None if the asset is unmapped."""
    q = _NEWS_QUERY.get(news_key(symbol))
    if not q:
        return None
    time.sleep(polite_delay)                                    # GDELT: 1 request / 5 s
    params = {"query": q, "mode": "timelinetone", "timespan": f"{int(months) * 30}d", "format": "json"}
    try:
        j = get_json(GDELT, params=params)
    except Exception:
        return None
    tl = j.get("timeline", []) if isinstance(j, dict) else []
    pts = tl[0].get("data", []) if tl else []
    if not pts:
        return None
    df = pd.DataFrame(pts)
    # GDELT stamps each daily tone point at the day boundary, but the value aggregates ALL of
    # that day's articles (incl. ones published later in the day). Lag by one day so an intraday
    # bar never sees tone built from articles that were still in its own future (PIT).
    df["datetime"] = pd.to_datetime(df["date"], utc=True, errors="coerce") + pd.Timedelta(days=1)
    df["news_tone"] = pd.to_numeric(df["value"], errors="coerce")
    out = df[["datetime", "news_tone"]].dropna()
    return out if len(out) else None
