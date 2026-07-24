"""mt.ingest.fedwatch — CME-FedWatch-style Fed policy expectation from FRED (docs/08, docs/11 §3.14).

The CME FedWatch Tool publishes the market-implied probability of a rate move at the next FOMC
meeting, derived inside CME's own widget from 30-Day Fed Funds futures (ZQ). CME exposes neither
those probabilities nor ZQ prices through a free API, so we reproduce the SAME signal — the rates
market's expected policy move — from free FRED data:

    fed_expectation = DGS1  −  target_mid           (percent → basis points ×100)

where DGS1 is the 1-Year Treasury yield (the market's expected AVERAGE fed-funds rate over the next
year, i.e. the expected policy path) and target_mid is the current FOMC target midpoint
((DFEDTARU+DFEDTARL)/2, or the pre-2008 single-point DFEDTAR). A positive value means the market is
pricing HIKES (yield above the current target); negative means CUTS — directionally identical to
FedWatch, which is what a regime/risk feature needs. It is a single GLOBAL macro series, so it is
broadcast to every symbol (unlike COT/calendar, which are per-symbol / per-currency).

Uses the official FRED JSON API (free api_key, stored like OANDA_API_KEY). PIT-aligned: H.15 daily
series publish the NEXT business day (~16:15 ET), so each observation is stamped to its release
instant so a same-day bar never sees a value that was not yet public.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
# FRED_API_KEY is reused from the sibling stacks that already hold it (borrow, don't duplicate).
_ENV_CANDIDATES = [
    Path("c:/Users/Curieux/FX Sentiment Scanner/.env"),
    Path("c:/Users/Curieux/Second_Brain/.env"),
    Path("c:/Users/Curieux/Macro_Compass/.env"),
    Path("c:/Users/Curieux/Trading/FX_Trading/.env"),
]


@lru_cache(maxsize=1)
def _api_key() -> Optional[str]:
    import os
    if os.environ.get("FRED_API_KEY"):
        return os.environ["FRED_API_KEY"]
    for p in _ENV_CANDIDATES:
        if p.exists():
            for ln in p.read_text(errors="ignore").splitlines():
                if ln.strip().startswith("#") or "=" not in ln:
                    continue
                k, v = ln.split("=", 1)
                if k.strip() == "FRED_API_KEY":
                    return v.strip().strip('"').strip("'")
    return None


def available() -> bool:
    return bool(_api_key())


def _fetch_series(series_id: str, start: str = "2015-01-01") -> Optional[pd.Series]:
    """One FRED series → Series[date → float] (numeric, missing '.' dropped); None on failure."""
    key = _api_key()
    if not key:
        return None
    params = {"series_id": series_id, "api_key": key, "file_type": "json",
              "observation_start": start}
    try:
        data = get_json(FRED_BASE, params=params)
    except Exception:
        return None
    obs = (data or {}).get("observations")
    if not obs:
        return None
    dates = pd.to_datetime([o["date"] for o in obs], utc=True)
    vals = pd.to_numeric([o.get("value") for o in obs], errors="coerce")   # FRED marks missing as "."
    s = pd.Series(vals, index=dates).dropna()
    return s if len(s) else None


def _target_mid(start: str) -> Optional[pd.Series]:
    """FOMC target midpoint: (DFEDTARU+DFEDTARL)/2 (post-2008 band), else single-point DFEDTAR."""
    up = _fetch_series("DFEDTARU", start)
    lo = _fetch_series("DFEDTARL", start)
    if up is not None and lo is not None:
        mid = (up.add(lo, fill_value=np.nan)) / 2.0
        mid = mid.dropna()
        if len(mid):
            return mid
    return _fetch_series("DFEDTAR", start)                    # pre-2008 fallback (single target)


def fetch_fed_expectation(start: str = "2015-01-01") -> Optional[pd.DataFrame]:
    """Daily (datetime, fed_expectation) — expected policy move in basis points (1Y yield − target
    midpoint), PIT-aligned to the next-business-day H.15 release. None if FRED is unavailable."""
    y1 = _fetch_series("DGS1", start)                         # 1Y Treasury = expected avg policy path
    mid = _target_mid(start)
    if y1 is None or mid is None:
        return None
    # forward-fill the (near-constant) target onto the daily yield grid, then take the gap in bps
    both = pd.DataFrame({"y1": y1}).join(pd.DataFrame({"mid": mid}), how="outer").sort_index()
    both["mid"] = both["mid"].ffill()
    both = both.dropna(subset=["y1", "mid"])
    if both.empty:
        return None
    bps = (both["y1"] - both["mid"]) * 100.0
    # H.15 daily series are released ~16:15 ET the NEXT business day; stamp to the release instant so
    # a bar on day D cannot see the value FRED first published on D+1 (PIT, mirrors the COT lag).
    dt = both.index + pd.Timedelta(days=1, hours=22)
    out = pd.DataFrame({"datetime": dt, "fed_expectation": bps.to_numpy()}).dropna()
    return out if len(out) else None
