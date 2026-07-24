"""mt.ingest.lake — build the content-hashed Parquet lake from real feeds.

Writes the SAME NormPanel frame contract the synthetic worker uses, plus a `_snapshot.json`
manifest with a content hash, so any backtest is reproducible against a named snapshot
(docs/08 §4). Reading needs no market stack (it's just Parquet), so panels load in-process
with no isolation dance — the subprocess isolation only mattered for importing a market's
code, which ingestion here sidesteps by going straight to the public endpoints.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import numpy as np
import pandas as pd

from mt.config import LAKE_DIR, MARKETS
from mt.data.panel import write_frame, FRAME_COLS
from mt.ingest import binance, oanda, binance_dumps


@dataclass
class IngestResult:
    market: str
    snapshot_id: str
    source: str
    symbols: List[str]
    timeframes: dict
    total_rows: int
    content_hash: str
    frames: int


def _us(series) -> pd.Series:
    """Normalize a datetime series to UTC microsecond resolution (merge_asof needs matching units)."""
    return pd.to_datetime(series, utc=True).dt.as_unit("us")


def _tf_minutes(tf: str) -> int:
    tf = tf.strip()
    unit, val = (tf[-1].lower(), int(tf[:-1])) if tf[0].isdigit() else (tf[0].lower(), int(tf[1:] or 1))
    return {"m": 1, "h": 60, "d": 1440}[unit] * val


def enrich_footprint(market: str, snapshot_id: str = "real", symbols: Optional[List[str]] = None,
                     days: int = 5, top_k: int = 8, log=print) -> int:
    """Attach REAL tick footprint (fp_stacked, fp_absorption) to recent HTF bars via aggTrades.

    Bounded by design (daily aggTrades are 2–20 MB): enriches the top-`top_k` symbols for the
    last `days` days. Older bars keep NaN footprint (the feature is skipped there)."""
    import json
    from mt.ingest import agg_trades
    m = MARKETS[market]
    if m.kind != "crypto":
        log(f"    [{market}] footprint is Binance-only — skipping."); return 0
    man_path = LAKE_DIR / snapshot_id / market / "_snapshot.json"
    if not man_path.exists():
        log(f"    [{market}] no lake snapshot — ingest first."); return 0
    manifest = json.loads(man_path.read_text())
    tf_min = _tf_minutes(m.htf)
    syms = symbols or manifest.get("symbols", [])[:top_k]
    enriched = 0
    for f in manifest.get("frames", []):
        if f["tf"] != m.htf or f["symbol"] not in syms:
            continue
        fp = agg_trades.bar_footprint_frame(f["symbol"], tf_min, days=days)
        if fp.empty:
            continue
        df = pd.read_parquet(f["path"])
        df["datetime"] = _us(df["datetime"])
        df = df.drop(columns=[c for c in ("fp_stacked", "fp_absorption") if c in df.columns], errors="ignore")
        fpm = fp.rename(columns={"stacked_imbalance": "fp_stacked", "absorption": "fp_absorption"})
        fpm["datetime"] = _us(fpm["datetime"])
        merged = pd.merge_asof(df.sort_values("datetime"),
                               fpm[["datetime", "fp_stacked", "fp_absorption"]].sort_values("datetime"),
                               on="datetime", direction="backward", tolerance=pd.Timedelta(minutes=tf_min))
        for c in FRAME_COLS:
            if c not in merged.columns:
                merged[c] = np.nan
        merged[FRAME_COLS].to_parquet(f["path"], index=False)
        enriched += 1
        log(f"    [{market}] {f['symbol']}: footprint on {int(fpm['fp_stacked'].notna().sum())} recent bars")
    return enriched


def enrich_macro(market: str, snapshot_id: str = "real", symbols: Optional[List[str]] = None,
                 months: int = 18, do_cot: bool = True, do_news: bool = True, log=print) -> int:
    """Attach CFTC COT positioning (cot_z) + GDELT news tone (news_tone) to HTF bars of the
    mapped symbols, over deep history. Unmapped symbols keep NaN (feature skipped there)."""
    import json
    from mt.ingest import cot as cot_mod, news as news_mod
    m = MARKETS[market]
    man_path = LAKE_DIR / snapshot_id / market / "_snapshot.json"
    if not man_path.exists():
        log(f"    [{market}] no lake snapshot."); return 0
    manifest = json.loads(man_path.read_text())
    syms = symbols or manifest.get("symbols", [])
    enriched = 0
    for f in manifest.get("frames", []):
        if f["tf"] != m.htf or f["symbol"] not in syms:
            continue
        try:
            cotdf = cot_mod.fetch_cot_z(f["symbol"]) if do_cot else None
            newsdf = news_mod.fetch_news_tone(f["symbol"], months) if do_news else None
            if cotdf is None and newsdf is None:
                continue
            df = pd.read_parquet(f["path"])
            df["datetime"] = _us(df["datetime"])
            df = df.drop(columns=[c for c in ("cot_z", "news_tone") if c in df.columns],
                         errors="ignore").sort_values("datetime")
            if cotdf is not None:
                cotdf = cotdf.copy(); cotdf["datetime"] = _us(cotdf["datetime"])
                df = pd.merge_asof(df, cotdf.sort_values("datetime"), on="datetime", direction="backward")
            if newsdf is not None:
                newsdf = newsdf.copy(); newsdf["datetime"] = _us(newsdf["datetime"])
                df = pd.merge_asof(df, newsdf.sort_values("datetime"), on="datetime", direction="backward")
            for c in FRAME_COLS:
                if c not in df.columns:
                    df[c] = np.nan
            df[FRAME_COLS].to_parquet(f["path"], index=False)
            enriched += 1
        except Exception as e:
            log(f"    [{market}] {f['symbol']}: macro enrich error ({type(e).__name__}: {str(e)[:60]})")
            continue
        tags = []
        if cotdf is not None and "cot_z" in df:
            tags.append(f"cot({int(df['cot_z'].notna().sum())})")
        if newsdf is not None and "news_tone" in df:
            tags.append(f"news({int(df['news_tone'].notna().sum())})")
        log(f"    [{market}] {f['symbol']}: {' '.join(tags) or 'no macro'}")
    return enriched


def enrich_calendar(market: str, snapshot_id: str = "real", symbols: Optional[List[str]] = None,
                    log=print) -> int:
    """Attach FairEconomy event surprise (cal_surprise) to recent HTF bars. Source is fetched
    once per market (ForexFactory/MetalsMine/CryptoCraft); events persist up to 3 days."""
    import json
    from mt.ingest import calendar as cal_mod
    m = MARKETS[market]
    man_path = LAKE_DIR / snapshot_id / market / "_snapshot.json"
    if not man_path.exists():
        log(f"    [{market}] no lake snapshot."); return 0
    manifest = json.loads(man_path.read_text())
    events = cal_mod.fetch_source(m.kind)
    if events is None or events.empty:
        log(f"    [{market}] no calendar events for source."); return 0
    syms = symbols or manifest.get("symbols", [])
    enriched = 0
    for f in manifest.get("frames", []):
        if f["tf"] != m.htf or f["symbol"] not in syms:
            continue
        try:
            sig = cal_mod.signal_from_events(events, f["symbol"], m.kind)
            if sig is None or sig.empty:
                continue
            df = pd.read_parquet(f["path"])
            df["datetime"] = _us(df["datetime"])
            df = df.drop(columns=[c for c in ("cal_surprise",) if c in df.columns], errors="ignore").sort_values("datetime")
            sig = sig.copy(); sig["datetime"] = _us(sig["datetime"])
            df = pd.merge_asof(df, sig.sort_values("datetime"), on="datetime", direction="backward",
                               tolerance=pd.Timedelta(days=3))
            for c in FRAME_COLS:
                if c not in df.columns:
                    df[c] = np.nan
            df[FRAME_COLS].to_parquet(f["path"], index=False)
            enriched += 1
            log(f"    [{market}] {f['symbol']}: cal_surprise on {int(df['cal_surprise'].notna().sum())} bars")
        except Exception as e:
            log(f"    [{market}] {f['symbol']}: calendar error ({type(e).__name__}: {str(e)[:50]})")
            continue
    return enriched


def _atr(df: pd.DataFrame, window: int = 14) -> np.ndarray:
    high, low, close = df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy()
    prev = np.concatenate([[close[0]], close[:-1]])
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev), np.abs(low - prev)))
    return pd.Series(tr).rolling(window, min_periods=1).mean().to_numpy()


_BENCHMARK = {"crypto": "BTC/USDT:USDT", "fx": "XAU_USD", "xau": "XAU_USD"}   # cross-asset ref


def _fetch(market: str, symbol: str, tf: str, bars: int, deep_months: int = 0,
           is_htf: bool = False) -> pd.DataFrame:
    if MARKETS[market].kind == "crypto":
        if deep_months:                                      # deep history via bulk dumps (CDN, geo-safe)
            if not is_htf:
                return pd.DataFrame()                        # mtf/ltf unused by the sim + REST is geo-blocked
            df = binance_dumps.build_deep_klines(symbol, tf, months=deep_months)
            if df is None or df.empty:
                return df
            fr = binance_dumps.fetch_funding_dumps(symbol, months=deep_months)   # funding via dumps (API blocked)
            if not fr.empty:
                df = pd.merge_asof(df.sort_values("datetime"), fr.sort_values("datetime"),
                                   on="datetime", direction="backward")
            return df
        return binance.build_frame(symbol, tf, limit=bars, with_funding=True)   # REST (local only)
    return oanda.build_frame(symbol, tf, count=bars)          # fx / metal → OANDA


def ingest_market(market: str, *, bars: int = 1500, snapshot_id: str = "real",
                  symbols: Optional[List[str]] = None, top_n: int = 50, deep_months: int = 0,
                  min_bars: int = 120, log=print) -> IngestResult:
    m = MARKETS[market]
    tfs = {"htf": m.htf, "mtf": m.mtf, "ltf": m.ltf}
    if symbols is None and m.kind == "crypto":
        try:
            symbols = binance.top_symbols_by_volume(top_n, coin_only=True)   # dynamic universe by 24h $volume
            log(f"    [{market}] universe: top {len(symbols)} crypto perps by 24h volume (API)")
        except Exception as e:
            log(f"    [{market}] 24h-volume API unavailable ({type(e).__name__}) — ranking via dump CDN…")
            try:
                symbols = binance_dumps.top_symbols_by_dump_volume(top_n)    # geo-safe fallback
                log(f"    [{market}] universe: top {len(symbols)} perps by dump quote-volume")
            except Exception as e2:
                log(f"    [{market}] dump ranking failed ({type(e2).__name__}); using config universe")
                symbols = m.universe
    syms = symbols or m.universe
    source = "binance_fapi" if m.kind == "crypto" else "oanda_v20"
    if deep_months:
        source += f"+dumps{deep_months}mo"

    # cross-asset benchmark (BTC for crypto, gold for FX/XAU) → ref_close on every frame
    bench_ref = None
    bench_sym = _BENCHMARK.get(market)
    if bench_sym:
        try:
            bdf = _fetch(market, bench_sym, m.htf, bars, deep_months, is_htf=True)
            if bdf is not None and len(bdf):
                bench_ref = bdf[["datetime", "close"]].rename(columns={"close": "ref_close"}).sort_values("datetime")
        except Exception as e:
            log(f"    [{market}] benchmark {bench_sym} fetch failed ({type(e).__name__})")

    frames_meta = []
    hasher = hashlib.sha256()
    total_rows = 0
    kept: List[str] = []
    for sym in syms:
        sym_ok = False
        for role, tf in tfs.items():
            try:
                df = _fetch(market, sym, tf, bars, deep_months, is_htf=(role == "htf"))
            except Exception as e:
                log(f"    [{market}] {sym} {tf}: fetch error ({type(e).__name__}: {str(e)[:60]})")
                continue
            if df is None or len(df) < min_bars:
                continue
            df = df.copy()
            df["atr_14"] = _atr(df, 14)
            if bench_ref is not None:
                df = pd.merge_asof(df.sort_values("datetime"), bench_ref, on="datetime", direction="backward")
            for c in FRAME_COLS:
                if c not in df.columns:
                    df[c] = np.nan
            path = write_frame(LAKE_DIR, snapshot_id, market, sym, tf, df)
            n = int(len(df))
            total_rows += n
            sym_ok = True
            last = df.iloc[-1]
            hasher.update(f"{sym}|{tf}|{n}|{df['datetime'].iloc[0]}|{df['datetime'].iloc[-1]}|"
                          f"{round(float(last['close']), 6)}".encode())
            frames_meta.append({"symbol": sym, "tf": tf, "path": str(path), "rows": n})
        if sym_ok:
            kept.append(sym)
        log(f"    [{market}] {sym}: {'ok' if sym_ok else 'skipped (insufficient data)'}")

    content_hash = hasher.hexdigest()[:16]
    manifest = {
        "market": market, "snapshot_id": snapshot_id, "source": source,
        "asof": datetime.now(timezone.utc).isoformat(), "timeframes": tfs,
        "symbols": kept, "total_rows": total_rows, "content_hash": content_hash,
        "frames": frames_meta,
    }
    out_dir = LAKE_DIR / snapshot_id / market
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_snapshot.json").write_text(json.dumps(manifest, indent=2))
    return IngestResult(market, snapshot_id, source, kept, tfs, total_rows, content_hash, len(frames_meta))
