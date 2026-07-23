"""mt.ingest.calendar — economic-event surprise from Fair Economy calendars (docs/11 §3.14).

Reuses the same free JSON feeds your FX/XAU/Crypto sentiment scanners consume, one curated
source per market:
  • ForexFactory  (ff) → FX     — events filtered to the pair's two currencies
  • MetalsMine    (mm) → metals — the metals-relevant event set
  • CryptoCraft   (cc) → crypto — the crypto-relevant event set

Each event carries impact (High/Medium/Low) and actual-vs-forecast, so we derive an
impact-weighted *surprise* signal per bar. The feeds cover ~2 weeks (thisweek+nextweek), so
this enriches recent bars (older bars keep NaN → the feature is skipped there), exactly like
the tick footprint.
"""
from __future__ import annotations

import re
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

FAIRECONOMY = "https://nfs.faireconomy.media"
SOURCE_BY_KIND = {"fx": "ff", "metal": "mm", "crypto": "cc"}
_IMPACT_W = {"High": 3.0, "Medium": 2.0, "Low": 1.0, "Holiday": 0.0, "": 0.5}
_VALUE_RE = re.compile(r"^\s*([<>])?\s*([+-]?)\s*([0-9,]+\.?[0-9]*)\s*([KMBT%])?\s*$", re.IGNORECASE)
_MULT = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}


def _parse_value(val) -> Optional[float]:
    if val is None:
        return None
    s = str(val).strip().strip('"').strip("'")
    if not s:
        return None
    m = _VALUE_RE.match(s)
    if not m:
        return None
    try:
        num = float(m.group(3).replace(",", ""))
    except ValueError:
        return None
    if m.group(2) == "-":
        num = -num
    suf = (m.group(4) or "").upper()
    return num * _MULT[suf] if suf in _MULT else num


def _fetch_events(source: str) -> pd.DataFrame:
    rows = []
    for period in ("thisweek", "nextweek"):
        try:
            data = get_json(f"{FAIRECONOMY}/{source}_calendar_{period}.json")
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for e in data:
            try:
                dt = pd.to_datetime(e.get("date"), utc=True)
            except Exception:
                continue
            if pd.isna(dt):
                continue
            fc, act = _parse_value(e.get("forecast")), _parse_value(e.get("actual"))
            surprise = ((act - fc) / abs(fc)) if (act is not None and fc not in (None, 0)) else 0.0
            rows.append({
                "datetime": dt, "country": str(e.get("country", "")).upper(),
                "impact": _IMPACT_W.get(e.get("impact", ""), 0.5),
                "surprise": float(np.clip(surprise, -3.0, 3.0)),
            })
    return pd.DataFrame(rows).drop_duplicates(["datetime", "country"]) if rows else pd.DataFrame()


def _relevant_currencies(symbol: str, kind: str) -> Optional[set]:
    """FX filters to the pair's two legs; metals/crypto use the whole curated source."""
    if kind == "fx":
        legs = [p for p in symbol.split("/")[0].split(":")[0].split("_") if p]
        return set(legs) or None
    return None                                                # mm/cc are already curated


def fetch_source(kind: str) -> pd.DataFrame:
    """All events for the market's curated source (fetch once per market, reuse per symbol)."""
    source = SOURCE_BY_KIND.get(kind)
    return _fetch_events(source) if source else pd.DataFrame()


def signal_from_events(events: pd.DataFrame, symbol: str, kind: str) -> Optional[pd.DataFrame]:
    """Per-event (datetime, cal_surprise)=impact×surprise for one symbol, from pre-fetched events."""
    if events is None or events.empty:
        return None
    df = events
    cur = _relevant_currencies(symbol, kind)
    if cur:
        df = df[df["country"].isin(cur)]
    if df.empty:
        return None
    out = df.assign(cal_surprise=df["impact"] * df["surprise"])
    return out.groupby("datetime", as_index=False)["cal_surprise"].sum().sort_values("datetime")


def calendar_signal(symbol: str, kind: str) -> Optional[pd.DataFrame]:
    """Convenience: fetch + filter for one symbol (fetches the source each call)."""
    return signal_from_events(fetch_source(kind), symbol, kind)
