"""mt.run_ingest — build the real data lake (docs/08).

    python -m mt.run_ingest --markets crypto,fx,xau --bars 1500 --snapshot-id real

Crypto → Binance USD-M futures REST (no auth). FX/XAU → OANDA v20 practice (key from
FX_Trading/.env). Writes content-hashed Parquet under var/lake/<snapshot-id>/<market>/.
Run once; the system then reads Parquet, never the API.
"""
from __future__ import annotations

import argparse

from mt.config import MARKETS
from mt.ingest import ingest_market
from mt.ingest.oanda import available as oanda_available


def main():
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Build the Master Trader real data lake.")
    ap.add_argument("--markets", default="crypto,fx,xau")
    ap.add_argument("--bars", type=int, default=1500)
    ap.add_argument("--snapshot-id", default="real")
    ap.add_argument("--top-n", type=int, default=50,
                    help="crypto: number of top-volume perps to ingest (dynamic universe)")
    ap.add_argument("--deep-months", type=int, default=0,
                    help="crypto: extend HTF history via N months of bulk dumps (0 = REST only)")
    ap.add_argument("--flow-days", type=int, default=0,
                    help="crypto: enrich recent HTF bars with real aggTrades footprint (0 = off)")
    ap.add_argument("--flow-symbols", type=int, default=8, help="how many top symbols to footprint-enrich")
    args = ap.parse_args()
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]

    print("=" * 70)
    print(f" MASTER TRADER — data lake ingestion  (snapshot '{args.snapshot_id}')")
    print("=" * 70)
    if any(MARKETS[m].kind != "crypto" for m in markets) and not oanda_available():
        print("  ⚠ OANDA_API_KEY not found — FX/XAU will be skipped (crypto still ingests).")

    results = []
    for m in markets:
        if MARKETS[m].kind != "crypto" and not oanda_available():
            print(f"\n[{m}] skipped (no OANDA key).")
            continue
        scope = (f"top {args.top_n} by 24h volume" if MARKETS[m].kind == "crypto"
                 else f"{len(MARKETS[m].universe)} instruments")
        print(f"\n[{m}] ingesting {scope} × 3 timeframes "
              f"({'Binance' if MARKETS[m].kind=='crypto' else 'OANDA'})…")
        res = ingest_market(m, bars=args.bars, snapshot_id=args.snapshot_id, top_n=args.top_n,
                            deep_months=(args.deep_months if MARKETS[m].kind == "crypto" else 0))
        results.append(res)
        print(f"   → {len(res.symbols)} symbols kept, {res.frames} frames, "
              f"{res.total_rows} bars, content_hash={res.content_hash}")

    if args.flow_days > 0 and "crypto" in markets:
        from mt.ingest.lake import enrich_footprint
        print(f"\n[crypto] enriching top {args.flow_symbols} symbols with real aggTrades footprint "
              f"({args.flow_days}d)…")
        n = enrich_footprint("crypto", snapshot_id=args.snapshot_id, days=args.flow_days, top_k=args.flow_symbols)
        print(f"   → footprint attached to {n} symbol frames")

    print("\n" + "=" * 70)
    print(" LAKE READY")
    for r in results:
        print(f"   {r.market:7} [{r.source:12}] {len(r.symbols):2} symbols  {r.total_rows:6} bars  #{r.content_hash}")
    print("=" * 70)
    print(f"\n  Run the system on real data:")
    print(f"    python -m mt.run_system --source lake --snapshot-id {args.snapshot_id} --markets {args.markets}")


if __name__ == "__main__":
    main()
