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
    """Cheap persistence proxy in ~[0,1]: 0.5 + 0.5·lag-1 autocorrelation of returns."""
    w = int(args.get("window", 120))
    return 0.5 + 0.5 * autocorr(panel, {"lag": 1, "window": w}, tf)


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
    "cumulative_delta": cumulative_delta, "delta_divergence": delta_divergence, "rotation_factor": rotation_factor,
    "order_flow_imbalance": order_flow_imbalance, "aggressor_ratio": aggressor_ratio,
    "trade_intensity": trade_intensity,
    # trend
    "sma_dist": sma_dist, "ma_cross": ma_cross, "slope": slope, "adx": adx,
    # oscillators
    "macd": macd, "stoch": stoch, "cci": cci, "williams_r": williams_r, "roc": roc,
    # volatility
    "bb_position": bb_position, "atr_expansion": atr_expansion, "vol_of_vol": vol_of_vol,
    # volume
    "obv": obv, "vwap_distance": vwap_distance, "rel_volume": rel_volume, "volume_zscore": volume_zscore,
    # statistical
    "autocorr": autocorr, "variance_ratio": variance_ratio, "rolling_skew": rolling_skew,
    "rolling_kurt": rolling_kurt, "hurst": hurst, "price_zscore": price_zscore,
    # pattern
    "consolidation_score": consolidation_score,
    # cross-asset + SMC/ICT (lightweight computable proxies)
    "rolling_corr": rolling_corr,
    "structure_break": structure_break, "fvg_gap": fvg_gap, "liquidity_sweep": liquidity_sweep,
    # tick footprint (real aggTrades)
    "stacked_imbalance": stacked_imbalance, "absorption": absorption,
    # the last five: pattern / SMC OB / vol-regime / COT / news
    "candlestick_pattern": candlestick_pattern, "order_block_strength": order_block_strength,
    "vol_regime_tag": vol_regime_tag, "cot_zscore": cot_zscore, "news_sentiment": news_sentiment,
    "event_surprise": event_surprise,
}


def compute(op: str, panel: NormPanel, args: dict, tf: str) -> pd.DataFrame:
    fn = BUILDERS.get(op)
    if fn is None:
        raise KeyError(f"no feature builder for op {op!r}")
    return fn(panel, args, tf)
