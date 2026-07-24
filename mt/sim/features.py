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


# ─── regime classifier (the conditioning axis, docs/06) ──────────────────
# Turns "feature X" into "feature X *when* regime Y" — the highest-leverage way an
# unconditional-noise signal becomes a conditional edge. Pure trailing OHLCV ⇒ PIT-safe.
REGIMES = ("all", "low_vol", "high_vol", "trend", "chop")


def regime_mask(panel: NormPanel, tf: str, regime: str) -> Optional[pd.DataFrame]:
    """Boolean [time × symbol] mask (True = bar is IN the named regime), or None for 'all'.
    Percentile-ranked against each symbol's own trailing history, so it is self-calibrating."""
    if regime in (None, "", "all"):
        return None
    close = _close(panel, tf)
    if close.empty:
        return None
    rv = close.pct_change().rolling(48, min_periods=12).std()
    if regime in ("low_vol", "high_vol"):
        pct = rv.rolling(200, min_periods=50).rank(pct=True)
        return (pct < 0.40) if regime == "low_vol" else (pct > 0.60)
    if regime in ("trend", "chop"):
        mom = close.pct_change().rolling(20, min_periods=6).mean()
        strength = (mom.abs() / rv.replace(0, np.nan))          # |drift| in vol units → trendiness
        pct = strength.rolling(200, min_periods=50).rank(pct=True)
        return (pct > 0.55) if regime == "trend" else (pct < 0.45)
    return None


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


# ─── Auction Market Theory & order-flow proxies (docs/11 §3.15) ──────────
# Bar-derivable proxies; the true footprint versions activate once trades/aggTrades
# are in the lake (docs/12 §3). Not privileged — they compete in the Gauntlet like any op.

def _clv_delta(panel: NormPanel, tf: str) -> pd.DataFrame:
    """Per-bar signed volume via close-location value in [-1,1] × volume (delta proxy)."""
    close = _close(panel, tf)
    high = panel.field_matrix("high", tf).reindex_like(close)
    low = panel.field_matrix("low", tf).reindex_like(close)
    vol = panel.field_matrix("volume", tf).reindex_like(close)
    rng = (high - low).replace(0, np.nan)
    clv = (2 * (close - low) / rng - 1.0)          # +1 close-on-high, -1 close-on-low
    return clv * vol


# ─── real Market Profile: developing POC + Value Area (Steidlmayer/Dalton) ─
def _volume_profile_core(close, volume, w, levels):
    """Rolling volume-at-price profile → (POC price, value-area low, value-area high) per bar.
    POC = price level with the most volume over the trailing window; Value Area = the contiguous
    price band holding 70% of volume around the POC. Pure-numeric so Numba JITs it."""
    n = len(close)
    poc = np.full(n, np.nan); va_lo = np.full(n, np.nan); va_hi = np.full(n, np.nan)
    for t in range(w - 1, n):
        lo = close[t - w + 1]; hi = lo
        for j in range(t - w + 1, t + 1):
            cj = close[j]
            if cj < lo:
                lo = cj
            if cj > hi:
                hi = cj
        if not (hi > lo):
            continue
        binw = (hi - lo) / levels
        vp = np.zeros(levels)
        for j in range(t - w + 1, t + 1):
            b = int((close[j] - lo) / binw)
            if b >= levels:
                b = levels - 1
            elif b < 0:
                b = 0
            vp[b] += volume[j]
        pk = 0
        for b in range(1, levels):
            if vp[b] > vp[pk]:
                pk = b
        poc[t] = lo + (pk + 0.5) * binw
        total = 0.0
        for b in range(levels):
            total += vp[b]
        target = 0.7 * total
        acc = vp[pk]; lob = pk; hib = pk
        while acc < target and (lob > 0 or hib < levels - 1):
            up = vp[hib + 1] if hib < levels - 1 else -1.0
            dn = vp[lob - 1] if lob > 0 else -1.0
            if up >= dn and hib < levels - 1:
                hib += 1; acc += vp[hib]
            elif lob > 0:
                lob -= 1; acc += vp[lob]
            else:
                break
        va_lo[t] = lo + lob * binw; va_hi[t] = lo + (hib + 1) * binw
    return poc, va_lo, va_hi


try:                                                          # JIT when available; identical fallback
    from numba import njit as _njit
    _profile_core = _njit(cache=True)(_volume_profile_core)
except Exception:                                             # pragma: no cover
    _profile_core = _volume_profile_core


def _profile(panel: NormPanel, tf: str, w: int, levels: int = 24):
    close, _, _, vol, _ = _mats(panel, tf)
    poc, vlo, vhi = {}, {}, {}
    for sym in close.columns:
        c = np.ascontiguousarray(close[sym].to_numpy(), dtype=np.float64)
        v = np.ascontiguousarray(vol[sym].to_numpy(), dtype=np.float64)
        v = np.where(np.isfinite(v), v, 0.0)
        p, lo, hi = _profile_core(c, v, int(w), int(levels))
        poc[sym] = p; vlo[sym] = lo; vhi[sym] = hi
    idx = close.index
    return (pd.DataFrame(poc, index=idx), pd.DataFrame(vlo, index=idx), pd.DataFrame(vhi, index=idx))


def poc_distance_real(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Distance from price to the REAL developing Point of Control (volume mode), in ATR — the
    genuine Market Profile POC (Steidlmayer/Dalton), not the VWAP-mean proxy."""
    w = int(args.get("window", 60)); levels = int(args.get("levels", 24))
    close, _, _, _, atr = _mats(panel, tf)
    poc, _, _ = _profile(panel, tf, w, levels)
    return (close - poc) / atr


def value_area_real(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """+1 above / 0 inside / −1 below the REAL developing Value Area (the contiguous 70%-volume
    band around the POC) — the actual Market Profile construction."""
    w = int(args.get("window", 60)); levels = int(args.get("levels", 24))
    close = _close(panel, tf)
    _, vlo, vhi = _profile(panel, tf, w, levels)
    return (close > vhi).astype(float) - (close < vlo).astype(float)


def dist_to_poc(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Distance of price to the developing volume Point of Control, in ATR (proxy: VWAP)."""
    w = int(args.get("window", 60))
    close = _close(panel, tf)
    vol = panel.field_matrix("volume", tf).reindex_like(close)
    atr = panel.field_matrix("atr_14", tf).reindex_like(close)
    num = (close * vol).rolling(w, min_periods=max(3, w // 3)).sum()
    den = vol.rolling(w, min_periods=max(3, w // 3)).sum().replace(0, np.nan)
    poc = num / den
    return (close - poc) / atr.replace(0, np.nan)


def value_area_position(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Above (+1) / inside (0) / below (-1) the developing value area (proxy: VWAP±1σ)."""
    w = int(args.get("window", 60))
    close = _close(panel, tf)
    vol = panel.field_matrix("volume", tf).reindex_like(close)
    num = (close * vol).rolling(w, min_periods=max(3, w // 3)).sum()
    den = vol.rolling(w, min_periods=max(3, w // 3)).sum().replace(0, np.nan)
    vwap = num / den
    sd = close.rolling(w, min_periods=max(3, w // 3)).std().replace(0, np.nan)
    pos = (close - vwap) / sd
    return pos.clip(-1, 1).where(pos.abs() > 1, 0.0).apply(np.sign)


def _has_flow(panel: NormPanel, tf: str) -> bool:
    tbv = panel.field_matrix("taker_buy_volume", tf)
    return not tbv.empty and bool(tbv.notna().any().any())


def _real_delta(panel: NormPanel, tf: str):
    """REAL net aggressor volume (2·taker_buy − volume) from Binance klines, else None."""
    if not _has_flow(panel, tf):
        return None, None
    tbv = panel.field_matrix("taker_buy_volume", tf)
    vol = panel.field_matrix("volume", tf).reindex_like(tbv)
    return (2.0 * tbv - vol), vol


def cumulative_delta(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Normalized cumulative volume delta over a window, in [-1,1]. Uses REAL taker-buy
    aggressor flow (Binance klines) when present, else the OHLCV close-location proxy."""
    w = int(args.get("window", 48))
    delta, vol = _real_delta(panel, tf)
    if delta is None:
        delta = _clv_delta(panel, tf)
        vol = panel.field_matrix("volume", tf).reindex_like(delta)
    ds = delta.rolling(w, min_periods=max(3, w // 3)).sum()
    vs = vol.rolling(w, min_periods=max(3, w // 3)).sum().replace(0, np.nan)
    return ds / vs


# ─── real bar-level order flow (Binance taker-buy + trade count) ─────────
def order_flow_imbalance(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Net aggressor fraction (real buy−sell / volume), rolling — the order-flow imbalance."""
    w = int(args.get("window", 48))
    delta, vol = _real_delta(panel, tf)
    if delta is None:
        return _close(panel, tf) * np.nan                 # inert where taker-buy is absent (OANDA)
    return (delta / vol.replace(0, np.nan)).rolling(w, min_periods=max(3, w // 3)).mean()


def aggressor_ratio(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Market-buy share vs market-sell, centered to [-1,1] (real taker-buy fraction)."""
    w = int(args.get("window", 48))
    if not _has_flow(panel, tf):
        return _close(panel, tf) * np.nan
    tbv = panel.field_matrix("taker_buy_volume", tf)
    vol = panel.field_matrix("volume", tf).reindex_like(tbv)
    return (2.0 * tbv / vol.replace(0, np.nan) - 1.0).rolling(w, min_periods=max(3, w // 3)).mean()


def trade_intensity(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Auction speed: z-score of trades-per-bar vs its trailing mean (real trade count)."""
    w = int(args.get("window", 48))
    tc = panel.field_matrix("trade_count", tf)
    if tc.empty or not tc.notna().any().any():
        return _close(panel, tf) * np.nan
    mu = tc.rolling(w, min_periods=max(3, w // 3)).mean()
    sd = tc.rolling(w, min_periods=max(3, w // 3)).std().replace(0, np.nan)
    return (tc - mu) / sd


def vpin(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """VPIN — order-flow *toxicity* (Easley, López de Prado & O'Hara 2012): rolling ABSOLUTE
    imbalance Σ|buy−sell| / Σvolume ∈ [0,1]. Unsigned (distinct from order-flow imbalance) —
    high VPIN flags informed/one-sided flow that precedes volatility. Real taker-buy; our exact
    buy/sell beats the paper's bulk-volume classification. Inert where taker-buy is absent."""
    w = int(args.get("window", 48))
    delta, vol = _real_delta(panel, tf)                       # delta = buy − sell = 2·taker_buy − volume
    if delta is None:
        return _close(panel, tf) * np.nan
    num = delta.abs().rolling(w, min_periods=_mp(w)).sum()
    den = vol.rolling(w, min_periods=_mp(w)).sum().replace(0, np.nan)
    return num / den


def kyle_lambda(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Kyle's λ (1985) — price impact per unit of (normalized) signed order flow, estimated as a
    rolling cov(return, flow)/var(flow). Dimensionless (return per unit imbalance-fraction) so it
    is comparable across symbols. High λ = illiquid / fragile. Real taker-buy flow."""
    w = int(args.get("window", 48))
    delta, vol = _real_delta(panel, tf)
    if delta is None:
        return _close(panel, tf) * np.nan
    ret = _close(panel, tf).pct_change()
    x = delta / vol.replace(0, np.nan)                        # normalized signed flow ∈ [−1,1]
    mp = _mp(w)
    mx = x.rolling(w, min_periods=mp).mean(); my = ret.rolling(w, min_periods=mp).mean()
    cov = (x * ret).rolling(w, min_periods=mp).mean() - mx * my
    var = x.rolling(w, min_periods=mp).var().replace(0, np.nan)
    return cov / var


def amihud_illiquidity(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Amihud (2002) illiquidity: rolling mean of |return| / dollar-volume — how much price moves
    per dollar traded. Higher = less liquid; a well-evidenced cross-sectional premium. OHLCV-only,
    so it works on every market (not just crypto)."""
    w = int(args.get("window", 48))
    close, _, _, vol, _ = _mats(panel, tf)
    ret = close.pct_change().abs()
    dollar = (close * vol).replace(0, np.nan)
    return (ret / dollar).rolling(w, min_periods=_mp(w)).mean()


def delta_divergence(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Price up while delta down (or vice-versa) → absorption warning (proxy)."""
    w = int(args.get("window", 14))
    close = _close(panel, tf)
    cd = cumulative_delta(panel, {"window": w}, tf)
    pc = close.diff(w)
    return -(np.sign(pc) * cd)                      # +ve when price and delta disagree


def rotation_factor(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """TPO up/down rotation proxy over a window, normalized to [-1,1]."""
    w = int(args.get("window", 20))
    close = _close(panel, tf)
    up = (close.diff() > 0).astype(float)
    down = (close.diff() < 0).astype(float)
    return (up.rolling(w, min_periods=max(3, w // 3)).sum()
            - down.rolling(w, min_periods=max(3, w // 3)).sum()) / w


# ─── extended families (breadth: no school of thought privileged, docs/11) ─
def _mats(panel: NormPanel, tf: str):
    close = _close(panel, tf)
    high = panel.field_matrix("high", tf).reindex_like(close)
    low = panel.field_matrix("low", tf).reindex_like(close)
    vol = panel.field_matrix("volume", tf).reindex_like(close)
    atr = panel.field_matrix("atr_14", tf).reindex_like(close).replace(0, np.nan)
    return close, high, low, vol, atr


def _mp(w):
    return max(3, w // 3)


# — trend —
def sma_dist(panel, args, tf):
    w = int(args.get("window", 50)); close, _, _, _, atr = _mats(panel, tf)
    return (close - close.rolling(w, min_periods=_mp(w)).mean()) / atr


def ma_cross(panel, args, tf):
    fast = int(args.get("fast", 12)); slow = int(args.get("slow", 48))
    close, _, _, _, atr = _mats(panel, tf)
    return (close.ewm(span=fast, min_periods=_mp(fast)).mean()
            - close.ewm(span=slow, min_periods=_mp(slow)).mean()) / atr


def slope(panel, args, tf):
    w = int(args.get("window", 20)); close, _, _, _, atr = _mats(panel, tf)
    return close.diff().rolling(w, min_periods=_mp(w)).mean() / atr


def tsmom_blend(panel, args, tf):
    """Multi-horizon time-series momentum (AQR 'Trends Everywhere'; Moskowitz-Ooi-Pedersen 2012):
    the average of vol-scaled momentum at short / medium / long lookbacks — one feature capturing
    the horizon blend a real trend desk runs, instead of the search rediscovering it."""
    close = _close(panel, tf); r = close.pct_change()
    acc = None; n = 0
    for lb in (int(args.get("short", 20)), int(args.get("med", 60)), int(args.get("long", 120))):
        vol = r.rolling(lb, min_periods=max(3, lb // 3)).std().replace(0, np.nan)
        comp = (close / close.shift(lb) - 1.0) / vol
        acc = comp if acc is None else acc + comp; n += 1
    return acc / max(1, n)


def adx(panel, args, tf):
    w = int(args.get("window", 14)); close, high, low, _, _ = _mats(panel, tf)
    up = high.diff(); dn = -low.diff()
    plus_dm = up.where((up > dn) & (up > 0), 0.0)
    minus_dm = dn.where((dn > up) & (dn > 0), 0.0)
    prev_close = close.shift(1)
    tr = np.maximum(np.maximum((high - low).abs(), (high - prev_close).abs()), (low - prev_close).abs())
    mp = _mp(w)                                          # rolling mean ≈ Wilder, ~10× faster than ewm here
    atr_ = tr.rolling(w, min_periods=mp).mean().replace(0, np.nan)
    plus_di = 100 * plus_dm.rolling(w, min_periods=mp).mean() / atr_
    minus_di = 100 * minus_dm.rolling(w, min_periods=mp).mean() / atr_
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return (dx.rolling(w, min_periods=mp).mean() - 20.0) / 20.0


# — oscillators —
def macd(panel, args, tf):
    f = int(args.get("fast", 12)); s = int(args.get("slow", 26)); sig = int(args.get("signal", 9))
    close, _, _, _, atr = _mats(panel, tf)
    line = close.ewm(span=f, min_periods=_mp(f)).mean() - close.ewm(span=s, min_periods=_mp(s)).mean()
    return (line - line.ewm(span=sig, min_periods=_mp(sig)).mean()) / atr


def stoch(panel, args, tf):
    w = int(args.get("window", 14)); close, high, low, _, _ = _mats(panel, tf)
    ll = low.rolling(w, min_periods=_mp(w)).min(); hh = high.rolling(w, min_periods=_mp(w)).max()
    return (2 * (close - ll) / (hh - ll).replace(0, np.nan) - 1.0)


def cci(panel, args, tf):
    w = int(args.get("window", 20)); close, high, low, _, _ = _mats(panel, tf)
    tp = (high + low + close) / 3.0
    ma = tp.rolling(w, min_periods=_mp(w)).mean()
    md = (tp - ma).abs().rolling(w, min_periods=_mp(w)).mean().replace(0, np.nan)
    return ((tp - ma) / (0.015 * md)).clip(-300, 300) / 100.0


def williams_r(panel, args, tf):
    w = int(args.get("window", 14)); close, high, low, _, _ = _mats(panel, tf)
    hh = high.rolling(w, min_periods=_mp(w)).max(); ll = low.rolling(w, min_periods=_mp(w)).min()
    return (2 * (close - ll) / (hh - ll).replace(0, np.nan) - 1.0)


def roc(panel, args, tf):
    w = int(args.get("window", 12)); return _close(panel, tf).pct_change(w)


# — volatility —
def bb_position(panel, args, tf):
    w = int(args.get("window", 20)); mult = float(args.get("mult", 2.0))
    close, _, _, _, _ = _mats(panel, tf)
    ma = close.rolling(w, min_periods=_mp(w)).mean(); sd = close.rolling(w, min_periods=_mp(w)).std()
    return (close - ma) / (mult * sd).replace(0, np.nan)


def atr_expansion(panel, args, tf):
    w = int(args.get("window", 48)); _, _, _, _, atr = _mats(panel, tf)
    return atr / atr.rolling(w, min_periods=_mp(w)).mean() - 1.0


def vol_of_vol(panel, args, tf):
    w = int(args.get("window", 48)); close = _close(panel, tf)
    rv = close.pct_change().rolling(w, min_periods=_mp(w)).std()
    return -rv.rolling(w, min_periods=_mp(w)).std()


def har_vol(panel, args, tf):
    """HAR-RV vol term-structure (Corsi 2009): short-horizon realized vol relative to long-horizon
    realized vol. >0 ⇒ vol expanding vs its longer-run level — a principled atr_expansion."""
    short = int(args.get("short", 6)); long_ = int(args.get("long", 132))
    r = _close(panel, tf).pct_change()
    rv_s = r.rolling(short, min_periods=max(2, short // 2)).std()
    rv_l = r.rolling(long_, min_periods=max(5, long_ // 3)).std().replace(0, np.nan)
    return rv_s / rv_l - 1.0


def range_vol(panel, args, tf):
    """Yang-Zhang (2000) OHLC range volatility — the most efficient close-to-close alternative,
    combining overnight, open-close and Rogers-Satchell terms. Same window, far less noise, using
    OHLC we already store. Negated (low-vol tilt, like realized_vol)."""
    w = int(args.get("window", 48)); close, high, low, _, _ = _mats(panel, tf)
    open_ = panel.field_matrix("open", tf).reindex_like(close); mp = _mp(w)
    o = np.log(open_ / close.shift(1)); c = np.log(close / open_)
    rs = np.log(high / close) * np.log(high / open_) + np.log(low / close) * np.log(low / open_)
    k = 0.34 / (1.34 + (w + 1) / (w - 1))
    yz = (o.rolling(w, min_periods=mp).var() + k * c.rolling(w, min_periods=mp).var()
          + (1 - k) * rs.rolling(w, min_periods=mp).mean())
    return -np.sqrt(yz.clip(lower=0))


# — volume —
def obv(panel, args, tf):
    w = int(args.get("window", 48)); close, _, _, vol, _ = _mats(panel, tf)
    o = (np.sign(close.diff()) * vol).cumsum()
    return (o - o.rolling(w, min_periods=_mp(w)).mean()) / o.rolling(w, min_periods=_mp(w)).std().replace(0, np.nan)


def vwap_distance(panel, args, tf):
    w = int(args.get("window", 48)); close, _, _, vol, atr = _mats(panel, tf)
    vwap = (close * vol).rolling(w, min_periods=_mp(w)).sum() / vol.rolling(w, min_periods=_mp(w)).sum().replace(0, np.nan)
    return (close - vwap) / atr


def rel_volume(panel, args, tf):
    w = int(args.get("window", 48)); _, _, _, vol, _ = _mats(panel, tf)
    return vol / vol.rolling(w, min_periods=_mp(w)).mean().replace(0, np.nan) - 1.0


def volume_zscore(panel, args, tf):
    w = int(args.get("window", 48)); _, _, _, vol, _ = _mats(panel, tf)
    return (vol - vol.rolling(w, min_periods=_mp(w)).mean()) / vol.rolling(w, min_periods=_mp(w)).std().replace(0, np.nan)


# — statistical / econometric —
def autocorr(panel, args, tf):
    lag = int(args.get("lag", 1)); w = int(args.get("window", 48))
    r = _close(panel, tf).pct_change(); y = r.shift(lag)
    mx = r.rolling(w, min_periods=_mp(w)).mean(); my = y.rolling(w, min_periods=_mp(w)).mean()
    cov = (r * y).rolling(w, min_periods=_mp(w)).mean() - mx * my
    return cov / (r.rolling(w, min_periods=_mp(w)).std() * y.rolling(w, min_periods=_mp(w)).std()).replace(0, np.nan)


def variance_ratio(panel, args, tf):
    w = int(args.get("window", 96)); q = int(args.get("q", 4))
    close = _close(panel, tf)
    v1 = close.pct_change().rolling(w, min_periods=_mp(w)).var()
    vq = close.pct_change(q).rolling(w, min_periods=_mp(w)).var()
    return vq / (q * v1).replace(0, np.nan) - 1.0            # >0 trending, <0 mean-reverting


def rolling_skew(panel, args, tf):
    w = int(args.get("window", 48)); return _close(panel, tf).pct_change().rolling(w, min_periods=_mp(w)).skew()


def rolling_kurt(panel, args, tf):
    w = int(args.get("window", 48)); return _close(panel, tf).pct_change().rolling(w, min_periods=_mp(w)).kurt()


def hurst(panel, args, tf):
    """Hurst exponent via the aggregated-variance method: Var(k-period return) ∝ k^(2H), so the
    slope of log Var(k) on log k across scales is 2H. Returns H−0.5 (>0 persistent/trending, <0
    anti-persistent/mean-reverting, 0 random walk) — a faithful replacement for the old
    0.5+0.5·autocorr proxy (Chan, Algorithmic Trading)."""
    w = int(args.get("window", 120))
    close = _close(panel, tf); mp = _mp(w)
    lags = (1, 2, 4, 8, 16)
    logk = np.log(np.array(lags, dtype=float)); xbar = logk.mean()
    sxx = float(((logk - xbar) ** 2).sum())
    logvar = [np.log(close.pct_change(k).rolling(w, min_periods=mp).var().replace(0, np.nan)) for k in lags]
    slope = sum((logk[i] - xbar) * logvar[i] for i in range(len(lags))) / sxx   # = 2H
    return 0.5 * slope - 0.5


def mean_reversion_halflife(panel, args, tf):
    """Ornstein-Uhlenbeck mean-reversion signal (Chan): fit a rolling AR(1) on log price
    (Δy = λ·y₋₁+…), λ<0 ⇒ mean-reverting with half-life −ln2/λ. Returns the deviation-from-
    equilibrium (in σ) *scaled by the reversion speed* → a real MR alpha that is strong only
    where the series actually reverts, and inert where it trends."""
    w = int(args.get("window", 60))
    close = _close(panel, tf); mp = _mp(w)
    y = np.log(close.replace(0, np.nan)); dy = y.diff(); ylag = y.shift(1)
    mx = ylag.rolling(w, min_periods=mp).mean(); md = dy.rolling(w, min_periods=mp).mean()
    cov = (ylag * dy).rolling(w, min_periods=mp).mean() - mx * md
    var = ylag.rolling(w, min_periods=mp).var().replace(0, np.nan)
    lam = cov / var                                          # AR(1) drift coefficient
    speed = (-lam).clip(lower=0.0)                           # reversion speed (0 if trending)
    dev = (y - y.rolling(w, min_periods=mp).mean()) / y.rolling(w, min_periods=mp).std().replace(0, np.nan)
    return -(dev) * speed                                    # short rich / long cheap, weighted by speed


def coint_zscore(panel, args, tf):
    """Cointegration-residual z-score vs the benchmark (Engle-Granger / Chan pairs): rolling hedge
    ratio β = cov(y,x)/var(x) on log prices, spread = y − β·x, z-scored. A genuine stat-arb signal
    (revert to the cointegrating relationship) rather than plain correlation."""
    w = int(args.get("window", 90))
    close = _close(panel, tf); mp = _mp(w)
    ref = panel.field_matrix("ref_close", tf).reindex_like(close)
    if ref.empty or not ref.notna().any().any():
        return close * np.nan
    y = np.log(close.replace(0, np.nan)); x = np.log(ref.replace(0, np.nan))
    mx = x.rolling(w, min_periods=mp).mean(); my = y.rolling(w, min_periods=mp).mean()
    cov = (x * y).rolling(w, min_periods=mp).mean() - mx * my
    beta = cov / x.rolling(w, min_periods=mp).var().replace(0, np.nan)
    resid = y - beta * x
    z = (resid - resid.rolling(w, min_periods=mp).mean()) / resid.rolling(w, min_periods=mp).std().replace(0, np.nan)
    return -z                                                # revert to the cointegration


def price_zscore(panel, args, tf):
    w = int(args.get("window", 48)); close = _close(panel, tf)
    return (close - close.rolling(w, min_periods=_mp(w)).mean()) / close.rolling(w, min_periods=_mp(w)).std().replace(0, np.nan)


# — pattern / shape —
def consolidation_score(panel, args, tf):
    w = int(args.get("window", 20)); close, high, low, _, _ = _mats(panel, tf)
    rng = high.rolling(w, min_periods=_mp(w)).max() - low.rolling(w, min_periods=_mp(w)).min()
    longer = high.rolling(3 * w, min_periods=_mp(w)).max() - low.rolling(3 * w, min_periods=_mp(w)).min()
    return 1.0 - rng / longer.replace(0, np.nan)             # high ⇒ tight consolidation


# ─── cross-asset / intermarket (benchmark = BTC for crypto, gold for FX/XAU) ─
def rolling_corr(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Rolling correlation of each symbol's returns with the benchmark's — intermarket beta."""
    w = int(args.get("window", 60))
    close = _close(panel, tf)
    ref = panel.field_matrix("ref_close", tf).reindex_like(close)
    if ref.empty or not ref.notna().any().any():
        return close * np.nan
    sr = close.pct_change(); rr = ref.pct_change()
    ms = sr.rolling(w, min_periods=_mp(w)).mean(); mr = rr.rolling(w, min_periods=_mp(w)).mean()
    cov = (sr * rr).rolling(w, min_periods=_mp(w)).mean() - ms * mr
    denom = (sr.rolling(w, min_periods=_mp(w)).std() * rr.rolling(w, min_periods=_mp(w)).std()).replace(0, np.nan)
    return cov / denom


# ─── SMC / ICT — lightweight VECTORIZED time-series proxies (docs/11 §3.9) ─
# Not the full concepts/* detectors (those are snapshot-oriented); these capture the same
# ideas as cheap per-bar series so the family competes in the cross-sectional/directional book.
def structure_break(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """+1 break of structure up / −1 down (close beyond the prior N-bar swing extreme)."""
    w = int(args.get("window", 20)); close, high, low, _, _ = _mats(panel, tf)
    hh = high.rolling(w, min_periods=_mp(w)).max().shift(1)
    ll = low.rolling(w, min_periods=_mp(w)).min().shift(1)
    return (close > hh).astype(float) - (close < ll).astype(float)


def fvg_gap(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Signed fair-value-gap size in ATR: bullish 3-bar gap (low>high[-2]) minus bearish."""
    _, high, low, _, atr = _mats(panel, tf)
    bull = (low - high.shift(2)) / atr
    bear = (low.shift(2) - high) / atr
    return bull.where(bull > 0, 0.0) - bear.where(bear > 0, 0.0)


def liquidity_sweep(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """+1 swept-low-then-reclaim (bullish) / −1 swept-high-then-reject (bearish)."""
    w = int(args.get("window", 20)); close, high, low, _, _ = _mats(panel, tf)
    hh = high.rolling(w, min_periods=_mp(w)).max().shift(1)
    ll = low.rolling(w, min_periods=_mp(w)).min().shift(1)
    swept_high = ((high > hh) & (close < hh)).astype(float)
    swept_low = ((low < ll) & (close > ll)).astype(float)
    return swept_low - swept_high


# ─── tick footprint (real, from aggTrades; inert where not ingested) ─────
def stacked_imbalance(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Consecutive lopsided footprint levels — the institutional signature (real aggTrades)."""
    fp = panel.field_matrix("fp_stacked", tf)
    if fp.empty or not fp.notna().any().any():
        return _close(panel, tf) * np.nan
    return fp.rolling(3, min_periods=1).max()


def absorption(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Aggressive volume that failed to move price (absorbed at a level) — real aggTrades."""
    fp = panel.field_matrix("fp_absorption", tf)
    if fp.empty or not fp.notna().any().any():
        return _close(panel, tf) * np.nan
    return fp.rolling(3, min_periods=1).mean()


# ─── the last five (docs/11): pattern, SMC OB, vol-regime ─────────────────
def candlestick_pattern(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Signed candlestick pattern flag (engulfing / pin / doji / inside)."""
    pat = str(args.get("pattern", "engulfing"))
    close, high, low, _, _ = _mats(panel, tf)
    open_ = panel.field_matrix("open", tf).reindex_like(close)
    body = close - open_
    rng = (high - low).replace(0, np.nan)
    if pat == "engulfing":
        po, pc = open_.shift(1), close.shift(1)
        bull = (close > open_) & (pc < po) & (close >= po) & (open_ <= pc)
        bear = (close < open_) & (pc > po) & (close <= po) & (open_ >= pc)
        return bull.astype(float) - bear.astype(float)
    if pat == "pin":
        upper = high - np.maximum(close, open_); lower = np.minimum(close, open_) - low; b = body.abs()
        return ((lower > 2 * b) & (upper < b)).astype(float) - ((upper > 2 * b) & (lower < b)).astype(float)
    if pat == "doji":
        return (body.abs() < 0.1 * rng).astype(float)
    return ((high < high.shift(1)) & (low > low.shift(1))).astype(float)   # inside bar


def order_block_strength(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """SMC order block: net recent displacement-after-opposite-candle pressure, in ATR.
    A lightweight vectorized proxy for the concepts/ detector (which is snapshot-only)."""
    close, high, low, _, atr = _mats(panel, tf)
    open_ = panel.field_matrix("open", tf).reindex_like(close)
    body = (close - open_) / atr
    displacement = body.where(body.abs() > 1.5, 0.0)                       # institutional candle
    prior_opposite = np.sign(body) != np.sign(body.shift(1))              # preceded by an opposite candle
    ob = displacement.where(prior_opposite, 0.0)
    return ob.rolling(10, min_periods=1).sum()


def vol_regime_tag(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Volatility regime in [-1,1]: percentile of current realized vol vs its trailing history
    (calm → −1, extreme → +1). A model-free version of the risk-grid's vol tier."""
    close = _close(panel, tf)
    rv = close.pct_change().rolling(48, min_periods=12).std()
    pct = rv.rolling(200, min_periods=50).rank(pct=True)
    return 2.0 * pct - 1.0


# ─── macro feed-based (COT positioning, news tone) — read enriched columns ─
def cot_zscore(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """CFTC COT net-positioning z-score (asset-mgr/large-spec), from the enriched cot_z column."""
    w = int(args.get("window", 26))
    cz = panel.field_matrix("cot_z", tf)
    if cz.empty or not cz.notna().any().any():
        return _close(panel, tf) * np.nan
    return cz.rolling(w, min_periods=1).mean()


def cot_index(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Williams COT Index: the %-range (stochastic) of net positioning over a lookback, in [-1,1].
    Extremes are contrarian (Larry Williams, *Secrets of the COT Report*). Built from cot_z."""
    w = int(args.get("window", 26))
    cz = panel.field_matrix("cot_z", tf)
    if cz.empty or not cz.notna().any().any():
        return _close(panel, tf) * np.nan
    mp = max(3, w // 3)
    lo = cz.rolling(w, min_periods=mp).min(); hi = cz.rolling(w, min_periods=mp).max()
    idx = (cz - lo) / (hi - lo).replace(0, np.nan)            # 0..1 within the lookback range
    return 2.0 * idx - 1.0                                    # −1 (min positioning) .. +1 (max)


def news_sentiment(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """News tone (GDELT) rolling average, from the enriched news_tone column."""
    w = int(args.get("window", 24))
    nt = panel.field_matrix("news_tone", tf)
    if nt.empty or not nt.notna().any().any():
        return _close(panel, tf) * np.nan
    return nt.rolling(w, min_periods=1).mean()


def event_surprise(panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    """Economic-event surprise (impact-weighted actual-vs-forecast) from the FairEconomy
    calendars (ForexFactory / MetalsMine / CryptoCraft), via the enriched cal_surprise column."""
    w = int(args.get("window", 12))
    cs = panel.field_matrix("cal_surprise", tf)
    if cs.empty or not cs.notna().any().any():
        return _close(panel, tf) * np.nan
    return cs.rolling(w, min_periods=1).mean()


BUILDERS: Dict[str, Callable[[NormPanel, dict, str], pd.DataFrame]] = {
    # classical
    "momentum": momentum, "reversion": reversion, "ema_dist": ema_dist, "rsi": rsi,
    "realized_vol": realized_vol, "breakout": breakout, "atr_pct": atr_pct, "funding_z": funding_z,
    # AMT / order-flow proxies + REAL bar-level order flow (Binance taker-buy)
    "dist_to_poc": dist_to_poc, "value_area_position": value_area_position,
    "poc_distance_real": poc_distance_real, "value_area_real": value_area_real,
    "cumulative_delta": cumulative_delta, "delta_divergence": delta_divergence, "rotation_factor": rotation_factor,
    "order_flow_imbalance": order_flow_imbalance, "aggressor_ratio": aggressor_ratio,
    "trade_intensity": trade_intensity,
    # microstructure (real order flow): Kyle's λ, VPIN toxicity, Amihud illiquidity
    "vpin": vpin, "kyle_lambda": kyle_lambda, "amihud_illiquidity": amihud_illiquidity,
    # trend
    "sma_dist": sma_dist, "ma_cross": ma_cross, "slope": slope, "adx": adx, "tsmom_blend": tsmom_blend,
    # oscillators
    "macd": macd, "stoch": stoch, "cci": cci, "williams_r": williams_r, "roc": roc,
    # volatility
    "bb_position": bb_position, "atr_expansion": atr_expansion, "vol_of_vol": vol_of_vol,
    "har_vol": har_vol, "range_vol": range_vol,
    # volume
    "obv": obv, "vwap_distance": vwap_distance, "rel_volume": rel_volume, "volume_zscore": volume_zscore,
    # statistical
    "autocorr": autocorr, "variance_ratio": variance_ratio, "rolling_skew": rolling_skew,
    "rolling_kurt": rolling_kurt, "hurst": hurst, "price_zscore": price_zscore,
    "mean_reversion_halflife": mean_reversion_halflife, "coint_zscore": coint_zscore,
    # pattern
    "consolidation_score": consolidation_score,
    # cross-asset + SMC/ICT (lightweight computable proxies)
    "rolling_corr": rolling_corr,
    "structure_break": structure_break, "fvg_gap": fvg_gap, "liquidity_sweep": liquidity_sweep,
    # tick footprint (real aggTrades)
    "stacked_imbalance": stacked_imbalance, "absorption": absorption,
    # the last five: pattern / SMC OB / vol-regime / COT / news
    "candlestick_pattern": candlestick_pattern, "order_block_strength": order_block_strength,
    "vol_regime_tag": vol_regime_tag, "cot_zscore": cot_zscore, "cot_index": cot_index,
    "news_sentiment": news_sentiment, "event_surprise": event_surprise,
}


def compute(op: str, panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    fn = BUILDERS.get(op)
    if fn is None:
        raise KeyError(f"no feature builder for op {op!r}")
    return fn(panel, args, tf)
