"""mt.ingest.cot — CFTC Commitments of Traders positioning (docs/08, docs/11 §3.14).

Weekly net non-commercial (large-spec) positioning from the CFTC Socrata public API — the
same free feed the FX/XAU sentiment scanners use. Available for years, so it aligns to deep
history. Mapped to the liquid futures markets (BTC, ETH, gold, silver, the FX majors);
symbols with no COT market are left NaN (the feature is skipped there).
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

COT_URL = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"

# base-asset → distinctive substring of the CFTC market_and_exchange_names
_COT_MARKET = {
    "BTC": "BITCOIN - CHICAGO", "ETH": "ETHER", "XAU": "GOLD - COMMODITY", "XAG": "SILVER - COMMODITY",
    "XPT": "PLATINUM", "XPD": "PALLADIUM",
    "EUR": "EURO FX", "GBP": "BRITISH POUND", "JPY": "JAPANESE YEN", "AUD": "AUSTRALIAN DOLLAR",
    "CAD": "CANADIAN DOLLAR", "CHF": "SWISS FRANC", "NZD": "NEW ZEALAND",
}


def cot_key(symbol: str) -> str:
    """Symbol → base asset for COT lookup (crypto BTC/USDT:USDT→BTC; FX EUR_USD/USD_JPY→non-USD leg)."""
    s = symbol.split("/")[0].split(":")[0]
    if "_" in s:
        parts = s.split("_")
        non_usd = [p for p in parts if p != "USD"]
        return non_usd[0] if non_usd else parts[0]
    return s


def fetch_cot_z(symbol: str, limit: int = 500) -> Optional[pd.DataFrame]:
    """Weekly (datetime, cot_z) — z-scored net non-commercial positioning; None if unmapped."""
    sub = _COT_MARKET.get(cot_key(symbol))
    if not sub:
        return None
    params = {
        "$where": f"upper(market_and_exchange_names) like '%{sub}%'",
        "$select": "report_date_as_yyyy_mm_dd,market_and_exchange_names,"
                   "noncomm_positions_long_all,noncomm_positions_short_all",
        "$order": "report_date_as_yyyy_mm_dd DESC", "$limit": limit,   # most-recent weeks
    }
    try:
        data = get_json(COT_URL, params=params)
    except Exception:
        return None
    if not data:
        return None
    df = pd.DataFrame(data)
    if "market_and_exchange_names" in df and df["market_and_exchange_names"].nunique() > 1:
        main = df["market_and_exchange_names"].value_counts().idxmax()      # the primary contract
        df = df[df["market_and_exchange_names"] == main]
    df["datetime"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"], utc=True)
    for c in ("noncomm_positions_long_all", "noncomm_positions_short_all"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.sort_values("datetime")
    net = df["noncomm_positions_long_all"] - df["noncomm_positions_short_all"]
    z = (net - net.rolling(52, min_periods=8).mean()) / net.rolling(52, min_periods=8).std()
    out = pd.DataFrame({"datetime": df["datetime"].to_numpy(), "cot_z": z.to_numpy()}).dropna()
    return out if len(out) else None
