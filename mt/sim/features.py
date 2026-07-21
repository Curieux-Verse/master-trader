"""mt.sim.features — feature-op → [time × symbol] matrix builders.

Each function turns a NormPanel into a cross-sectional feature matrix (rows = closed-bar
times, cols = symbols) using only closed bars. These are the point-in-time-safe primitives
the genome's feature nodes reference. This seed set is pure OHLCV(+funding); the richer
SMC/statistical/microstructure families (docs/02 §2) attach here as they are wrapped.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd

from mt.data.panel import NormPanel


def zscore_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional (per-row) z-score — the standardization used before blending."""
    mu = df.mean(axis=1)
    sd = df.std(axis=1).replace(0, np.nan)
    return df.sub(mu, axis=0).div(sd, axis=0)


def _close(panel: NormPanel, tf: Optional[str]) -> pd.DataFrame:
    return panel.close_matrix(tf)


def momentum(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    lb = int(args.get("lookback", 84)); skip = int(args.get("skip", 1))
    close = _close(panel, tf)
    if close.empty:
        return close
    shifted = close.shift(skip)
    mom = shifted / shifted.shift(lb) - 1.0
    vol = close.pct_change().rolling(lb, min_periods=max(3, lb // 3)).std()
    return mom / vol.replace(0, np.nan)


def reversion(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    lb = int(args.get("lookback", 3))
    close = _close(panel, tf)
    return -(close / close.shift(lb) - 1.0) if not close.empty else close


def ema_dist(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    w = int(args.get("window", 50))
    close = _close(panel, tf)
    atr = panel.field_matrix("atr_14", tf).reindex_like(close)
    ema = close.ewm(span=w, min_periods=max(3, w // 3)).mean()
    return (close - ema) / atr.replace(0, np.nan)


def rsi(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    w = int(args.get("window", 14))
    close = _close(panel, tf)
    delta = close.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / w, min_periods=w).mean()
    down = (-delta.clip(upper=0)).ewm(alpha=1 / w, min_periods=w).mean()
    rs = up / down.replace(0, np.nan)
    val = 100 - 100 / (1 + rs)
    return (val - 50.0) / 50.0            # center to [-1, 1]


def realized_vol(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    w = int(args.get("window", 48))
    close = _close(panel, tf)
    rv = close.pct_change().rolling(w, min_periods=max(3, w // 3)).std()
    return -rv                            # prefer calmer names (negated)


def breakout(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    w = int(args.get("window", 55))
    close = _close(panel, tf)
    atr = panel.field_matrix("atr_14", tf).reindex_like(close)
    hh = close.rolling(w, min_periods=max(3, w // 3)).max()
    return (close - hh) / atr.replace(0, np.nan)   # 0 at new high, negative below


def atr_pct(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    close = _close(panel, tf)
    atr = panel.field_matrix("atr_14", tf).reindex_like(close)
    return -(atr / close.replace(0, np.nan))       # negated: low-vol tilt


def funding_z(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    w = int(args.get("window", 72))
    fr = panel.field_matrix("funding_rate", tf)
    if fr.empty or fr.isna().all().all():
        return _close(panel, tf) * np.nan          # inert on non-funding markets
    mu = fr.rolling(w, min_periods=max(3, w // 3)).mean()
    sd = fr.rolling(w, min_periods=max(3, w // 3)).std().replace(0, np.nan)
    return -((fr - mu) / sd)                        # contrarian to crowded funding


BUILDERS: Dict[str, Callable[[NormPanel, dict, str], pd.DataFrame]] = {
    "momentum": momentum, "reversion": reversion, "ema_dist": ema_dist, "rsi": rsi,
    "realized_vol": realized_vol, "breakout": breakout, "atr_pct": atr_pct, "funding_z": funding_z,
}


def compute(op: str, panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    fn = BUILDERS.get(op)
    if fn is None:
        raise KeyError(f"no feature builder for op {op!r}")
    return fn(panel, args, tf)
