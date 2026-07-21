"""mt.data — the normalized panel contract and the Parquet feature lake.

Everything downstream (genome executor, gauntlet, archive) consumes a NormPanel: a
point-in-time, market-agnostic view of OHLCV(+funding) frames. Each per-market worker
writes this contract into the lake; the mt process reads it back identically regardless
of which stack produced it — the "one feature store" invariant from docs/01 §4.
"""
