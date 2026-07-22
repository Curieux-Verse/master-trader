"""Network-free tests for the lake read/slice path (fabricates a tiny lake on disk)."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd

from mt.config import LAKE_DIR
from mt.data.panel import write_frame
from mt.data.lake import read_lake_panel, lake_has_data, snapshot_info


def _fake_lake(snap: str, market: str = "crypto", n_sym: int = 5, bars: int = 200):
    end = datetime.now(timezone.utc)
    times = pd.to_datetime([end - timedelta(hours=4) * (bars - 1 - i) for i in range(bars)], utc=True)
    frames_meta = []
    syms = [f"C{s}/USDT:USDT" for s in range(n_sym)]
    for s, sym in enumerate(syms):
        close = 100 + np.cumsum(np.random.default_rng(s).normal(0, 1, bars))
        df = pd.DataFrame({"datetime": times, "open": close, "high": close + 1, "low": close - 1,
                           "close": close, "volume": np.ones(bars), "atr_14": np.ones(bars),
                           "funding_rate": np.nan})
        p = write_frame(LAKE_DIR, snap, market, sym, "4h", df)
        frames_meta.append({"symbol": sym, "tf": "4h", "path": str(p), "rows": bars})
    d = LAKE_DIR / snap / market
    d.mkdir(parents=True, exist_ok=True)
    (d / "_snapshot.json").write_text(json.dumps({
        "market": market, "snapshot_id": snap, "source": "test", "asof": end.isoformat(),
        "timeframes": {"htf": "4h", "mtf": "1h", "ltf": "15m"}, "symbols": syms,
        "content_hash": "deadbeef", "total_rows": n_sym * bars, "frames": frames_meta,
    }))
    return syms


def test_lake_read_and_time_split():
    snap = "pytest_probe"
    try:
        _fake_lake(snap)
        assert lake_has_data("crypto", snap)
        assert snapshot_info("crypto", snap)["content_hash"] == "deadbeef"

        full = read_lake_panel("crypto", snap)
        assert full.close_matrix().shape == (200, 5)

        train = read_lake_panel("crypto", snap, 0.0, 0.6)
        holdout = read_lake_panel("crypto", snap, 0.6, 1.0)
        assert train.close_matrix().shape[0] == 120
        assert holdout.close_matrix().shape[0] == 80
        # the split is contiguous in time (no overlap)
        assert train.frames[full.symbols[0]]["4h"]["datetime"].iloc[-1] <= \
               holdout.frames[full.symbols[0]]["4h"]["datetime"].iloc[0]
    finally:
        shutil.rmtree(LAKE_DIR / snap, ignore_errors=True)
