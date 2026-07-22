"""mt.adapters._market_worker — the isolated per-market subprocess entry point.

This script is executed *inside a market's stack root* (PYTHONPATH = CC_Trading or
FX_Trading), so its ``import core...`` resolves to THAT market's packages. It must NOT
import anything from ``mt`` — the whole point is process isolation from the namespace
clash. It speaks a tiny JSON protocol:

    python _market_worker.py <task.json>   ->   prints one line of JSON manifest to stdout

Task:  {"op","market","symbols","timeframes","bars","seed","out_dir","has_funding"}
Manifest: {"ok","market","snapshot_id","asof","market_core_file","frames":[...]}

For the thin slice the data is deterministic synthetic OHLCV (ccxt-free, network-free),
so the demo is byte-reproducible today; the ``cached``/live sources are the P0 deepening
step. Even so, the worker really does import each market's ``core`` — proving the
subprocess-isolation architecture end to end.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd


def _seed_int(*parts) -> int:
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:16], 16)


def _tf_minutes(tf: str) -> int:
    """Parse ccxt ('4h','15m','1d') and OANDA ('H4','M15','D') timeframes to minutes."""
    tf = tf.strip()
    if tf and tf[0].isdigit():                      # ccxt style: 4h, 15m, 1d
        unit, val = tf[-1].lower(), int(tf[:-1])
    else:                                            # OANDA style: H4, M15, D
        unit, val = tf[0].lower(), int(tf[1:] or 1)
    return {"m": 1, "h": 60, "d": 1440}[unit] * val


def _base_price(market_kind: str, symbol: str) -> float:
    r = _seed_int(symbol) % 1000 / 1000.0
    if market_kind == "crypto":
        return float(10 ** (1 + 4 * r))              # ~10 .. 100000
    if market_kind == "metal":
        return 1800.0 + 800.0 * r                    # gold ~1800..2600
    return 0.8 + 1.0 * r                             # fx ~0.8..1.8


def _synth_frame(symbol: str, tf: str, bars: int, seed: int, kind: str, has_funding: bool,
                 structure: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(_seed_int(seed, symbol, tf))
    minutes = _tf_minutes(tf)
    # per-bar vol scaled from an ~annual vol so different tfs are self-consistent
    ann_vol = {"crypto": 0.8, "metal": 0.15, "fx": 0.08}.get(kind, 0.3)
    bars_per_year = 525600.0 / minutes
    sigma = ann_vol / np.sqrt(bars_per_year)
    drift = -0.5 * sigma ** 2
    noise = rng.normal(0.0, sigma, size=bars)
    if structure > 0.0:
        # LABELED synthetic edge: persistent per-symbol drift + mild momentum (AR on noise),
        # so the discovery machine has genuine (planted) structure to find and validate.
        srng = np.random.default_rng(_seed_int(seed, symbol, "structure"))
        mu = float(srng.normal(0.0, 0.30 * structure * sigma))   # persistent drift, scaled to σ
        phi = 0.18 * structure                                    # momentum (AR on noise)
        rets = np.empty(bars)
        prev = 0.0
        for t in range(bars):
            rets[t] = drift + mu + phi * prev + noise[t]
            prev = noise[t]
    else:
        rets = drift + noise
    price = _base_price(kind, symbol) * np.exp(np.cumsum(rets))

    # OHLC around the close path
    close = price
    open_ = np.empty(bars)
    open_[0] = close[0] / (1 + rets[0]) if (1 + rets[0]) != 0 else close[0]
    open_[1:] = close[:-1]
    wig = np.abs(rng.normal(0, sigma, size=bars)) * close
    high = np.maximum(open_, close) + wig
    low = np.minimum(open_, close) - wig
    volume = rng.lognormal(mean=10.0, sigma=1.0, size=bars)

    end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    step = timedelta(minutes=minutes)
    times = [end - step * (bars - 1 - i) for i in range(bars)]

    df = pd.DataFrame({
        "datetime": pd.to_datetime(times, utc=True),
        "open": open_, "high": high, "low": low, "close": close, "volume": volume,
    })
    df["atr_14"] = _atr(df, 14)
    # synthetic order flow: aggressive-buy share correlated with the bar's return
    ret = np.concatenate([[0.0], np.diff(close) / np.where(close[:-1] == 0, np.nan, close[:-1])])
    buy_frac = np.clip(0.5 + 6.0 * ret + rng.normal(0, 0.05, bars), 0.05, 0.95)
    df["taker_buy_volume"] = volume * buy_frac
    df["trade_count"] = np.maximum(1.0, volume / max(np.median(volume), 1e-9) * 80.0)
    if has_funding:
        # small mean-reverting funding series (crypto perps)
        fr = rng.normal(0.0001, 0.0004, size=bars)
        df["funding_rate"] = pd.Series(fr).ewm(span=8).mean().to_numpy()
    else:
        df["funding_rate"] = np.nan
    return df


def _atr(df: pd.DataFrame, window: int) -> np.ndarray:
    high, low, close = df["high"].to_numpy(), df["low"].to_numpy(), df["close"].to_numpy()
    prev_close = np.concatenate([[close[0]], close[:-1]])
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    return pd.Series(tr).rolling(window, min_periods=1).mean().to_numpy()


def _escape(symbol: str) -> str:
    return symbol.replace("/", "-").replace(":", "-")


def main() -> None:
    task = json.loads(open(sys.argv[1], "r", encoding="utf-8").read())

    # Prove we are running inside the target market's stack (ccxt-free import).
    market_core_file = None
    try:
        import core.smc_config as _cfg  # noqa: F401 — resolves to THIS market's package
        market_core_file = getattr(_cfg, "__file__", None)
    except Exception as e:                # keep the worker robust if a stack is partial
        market_core_file = f"<import core failed: {type(e).__name__}: {e}>"

    market = task["market"]
    kind = task.get("kind", "crypto")
    tfs = list(task["timeframes"].values())
    out_dir = task["out_dir"]
    import os
    os.makedirs(out_dir, exist_ok=True)

    frames_meta = []
    for sym in task["symbols"]:
        for tf in tfs:
            df = _synth_frame(sym, tf, int(task.get("bars", 400)), int(task.get("seed", 4242)),
                              kind, bool(task.get("has_funding", False)),
                              structure=float(task.get("structure", 0.0)))
            path = os.path.join(out_dir, f"{_escape(sym)}__{tf}.parquet")
            df.to_parquet(path, index=False)
            frames_meta.append({"symbol": sym, "tf": tf, "path": os.path.abspath(path), "rows": int(len(df))})

    manifest = {
        "ok": True,
        "op": task["op"],
        "market": market,
        "snapshot_id": task.get("snapshot_id", "synthetic"),
        "asof": datetime.now(timezone.utc).isoformat(),
        "source": "synthetic",
        "market_core_file": market_core_file,
        "frames": frames_meta,
    }
    # Write to a file (authoritative — immune to stray stdout from the market's imports),
    # and also echo to stdout for interactive debugging.
    with open(os.path.join(out_dir, "_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)
    sys.stdout.write(json.dumps(manifest))


if __name__ == "__main__":
    main()
