"""mt.ingest.oanda — real FX + XAU candles from OANDA v20 practice (docs/08).

Reuses the OANDA practice endpoint and the OANDA_API_KEY the FX_Trading stack already holds
(read from its .env — the meta-layer borrows the credential, it does not duplicate the
account). Only COMPLETE candles are kept (closed-bar rule); OANDA `volume` is a tick count,
so it is a participation proxy, not traded size.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from mt.ingest.http import get_json

OANDA_BASE = "https://api-fxpractice.oanda.com"
_ENV_CANDIDATES = [
    Path("c:/Users/Curieux/Trading/FX_Trading/.env"),
    Path("c:/Users/Curieux/FX Sentiment Scanner/.env"),
]


@lru_cache(maxsize=1)
def _api_key() -> Optional[str]:
    import os
    if os.environ.get("OANDA_API_KEY"):
        return os.environ["OANDA_API_KEY"]
    for p in _ENV_CANDIDATES:
        if p.exists():
            for ln in p.read_text(errors="ignore").splitlines():
                if ln.strip().startswith("#") or "=" not in ln:
                    continue
                k, v = ln.split("=", 1)
                if k.strip() == "OANDA_API_KEY":
                    return v.strip().strip('"').strip("'")
    return None


def available() -> bool:
    return bool(_api_key())


def build_frame(instrument: str, granularity: str, count: int = 1500) -> pd.DataFrame:
    key = _api_key()
    if not key:
        return pd.DataFrame()
    data = get_json(f"{OANDA_BASE}/v3/instruments/{instrument}/candles",
                    params={"granularity": granularity, "count": min(count, 5000), "price": "M"},
                    headers={"Authorization": f"Bearer {key}"})
    candles = [c for c in data.get("candles", []) if c.get("complete")]   # closed bars only
    if not candles:
        return pd.DataFrame()
    rows = []
    for c in candles:
        m = c["mid"]
        rows.append({
            "datetime": pd.to_datetime(c["time"], utc=True),
            "open": float(m["o"]), "high": float(m["h"]), "low": float(m["l"]), "close": float(m["c"]),
            "volume": float(c.get("volume", 0.0)), "funding_rate": np.nan,
        })
    return pd.DataFrame(rows).sort_values("datetime").reset_index(drop=True)
