"""mt.data.lake — read real NormPanels from the content-hashed Parquet lake.

Reading needs no market stack (just Parquet), so it happens in-process. Fractional slicing
gives an honest point-in-time split of real history: train on the early fraction, lock a
holdout in the middle (G6 transfer), and paper-trade the most recent fraction (R1) — no
look-ahead, no synthetic seeds.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from mt.config import LAKE_DIR, MARKETS
from mt.data.panel import NormPanel, load_norm_panel, build_snapshot_from_frames


def market_dir(snapshot_id: str, market: str) -> Path:
    return LAKE_DIR / snapshot_id / market


def lake_has_data(market: str, snapshot_id: str) -> bool:
    man = market_dir(snapshot_id, market) / "_snapshot.json"
    if not man.exists():
        return False
    try:
        return len(json.loads(man.read_text()).get("frames", [])) > 0
    except Exception:
        return False


def snapshot_info(market: str, snapshot_id: str) -> Optional[dict]:
    man = market_dir(snapshot_id, market) / "_snapshot.json"
    if not man.exists():
        return None
    d = json.loads(man.read_text())
    return {k: d.get(k) for k in ("market", "source", "content_hash", "total_rows", "symbols", "asof")}


def read_lake_panel(market: str, snapshot_id: str, start_frac: float = 0.0,
                    end_frac: float = 1.0, max_bars: int = None) -> NormPanel:
    """Load a NormPanel from the lake, sliced to a time fraction [start,end) and optionally
    capped to the most recent `max_bars` bars per frame (keeps feature/backtest cost bounded
    while staying real and point-in-time)."""
    man_path = market_dir(snapshot_id, market) / "_snapshot.json"
    if not man_path.exists():
        raise FileNotFoundError(f"no lake snapshot for {market}/{snapshot_id}")
    manifest = json.loads(man_path.read_text())
    m = MARKETS[market]
    tfs = {"htf": m.htf, "mtf": m.mtf, "ltf": m.ltf}
    panel = load_norm_panel(manifest, tfs)
    panel.snapshot_id = snapshot_id

    if start_frac > 0.0 or end_frac < 1.0 or max_bars:
        for sym, tfd in panel.frames.items():
            for tf, df in list(tfd.items()):
                n = len(df)
                lo, hi = int(start_frac * n), int(end_frac * n)
                sliced = df.iloc[lo:hi]
                if max_bars and len(sliced) > max_bars:
                    sliced = sliced.iloc[-max_bars:]
                tfd[tf] = sliced.reset_index(drop=True)
        primary = panel.primary_tf
        if primary:
            panel.snapshot = build_snapshot_from_frames(panel.frames, primary)
        panel.symbols = sorted(panel.frames)
        panel.invalidate_cache()
    return panel
