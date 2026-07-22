"""mt.ingest.http — one shared HTTP client with exponential backoff + jitter (docs/08 §6).

Free feeds have rate limits; treat them as design constraints. Every GET retries on 429/5xx
with capped exponential backoff and jitter, so a burst of ingestion never trips the abuse
radar and a transient blip doesn't abort a lake build.
"""
from __future__ import annotations

import random
import time
from typing import Optional

import requests

_SESSION: Optional[requests.Session] = None


def session() -> requests.Session:
    global _SESSION
    if _SESSION is None:
        s = requests.Session()
        s.headers.update({"User-Agent": "master-trader-lake/0.1"})
        _SESSION = s
    return _SESSION


def get_json(url: str, *, params: dict = None, headers: dict = None, timeout: float = 25.0,
             max_retries: int = 5):
    delay = 1.0
    last = None
    for attempt in range(max_retries):
        try:
            r = session().get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (418, 429) or r.status_code >= 500:
                last = f"HTTP {r.status_code}"
            else:
                r.raise_for_status()
        except requests.RequestException as e:
            last = f"{type(e).__name__}: {str(e)[:80]}"
        time.sleep(delay + random.uniform(0, 0.5 * delay))
        delay = min(delay * 2, 20.0)
    raise RuntimeError(f"GET failed after {max_retries} retries ({last}): {url}")
