"""mt.ingest — the real, zero-cost data lake (docs/08).

Pulls real market history into the same NormPanel Parquet contract the synthetic worker
writes, so everything downstream (genome executor, gauntlet, archive, paper) runs unchanged
on real data. Free sources, no ccxt:

  • crypto  — Binance USD-M futures REST (klines + funding), no auth (data is public).
  • FX/XAU  — OANDA v20 practice candles (key read from FX_Trading/.env).

"One download, many reads" (docs/08 §6): history lands as content-hashed Parquet; backtests
read Parquet, never the API. Bulk daily/monthly dumps (deep history + survivorship) are the
natural next extension on top of this REST baseline.
"""
from mt.ingest.lake import ingest_market, IngestResult

__all__ = ["ingest_market", "IngestResult"]
