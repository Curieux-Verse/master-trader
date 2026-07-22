"""mt.run_demo — the thin end-to-end slice, exercised across crypto + FX + XAU.

Proves the whole loop wires together on isolated, clashing market stacks:

    generate → register (dedup) → simulate (Tier 1) → Result Ledger → gauntlet → archive

Honesty note (docs/00 §2): the demo runs on deterministic *synthetic* data with no real
edge, so the correct outcome is that the gauntlet REJECTS almost everything — "far more
rejections than discoveries" is the immune system succeeding, not failing. The archive
occupy/replace logic is additionally proven with an explicit, clearly-labeled mechanism
check so that code path is demonstrated regardless of the (honest) rejection rate.

    python -m mt.run_demo --reset --bars 600
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from mt.config import DB_PATH, RUNS_DIR, MARKETS, DATA_SNAPSHOT_ID, DEFAULT_SEED
from mt.adapters import MarketAdapter
from mt.genome.ops import mutate
from mt.generators import TemplateSampler
from mt.sim import evaluate
from mt.gauntlet import Gauntlet, GauntletContext
from mt.archive import MapElites
from mt.store import MTStore


def _reset_db():
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB_PATH) + suffix)
        if p.exists():
            p.unlink()


def run(markets, bars: int, seed: int, reset: bool) -> dict:
    try:                                   # Windows consoles default to cp1252
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if reset:
        _reset_db()
    store = MTStore()
    gauntlet = Gauntlet()
    archive = MapElites(store)
    sampler = TemplateSampler(seed=seed)
    rng = np.random.default_rng(seed)

    run_report = {"started": datetime.now(timezone.utc).isoformat(), "snapshot_id": DATA_SNAPSHOT_ID,
                  "markets": {}, "isolation": {}}
    t0 = time.time()

    print("=" * 78)
    print(" MASTER TRADER — thin end-to-end slice  (generate→sim→ledger→gauntlet→archive)")
    print("=" * 78)

    for market in markets:
        print(f"\n### MARKET: {market}  (root: {MARKETS[market].root.name})")
        panel = MarketAdapter(market).build_panel(bars=bars, seed=seed)
        core_file = _core_file(market)
        run_report["isolation"][market] = core_file
        print(f"  worker imported core from: {core_file}")
        print(f"  panel: {len(panel.symbols)} symbols × {panel.close_matrix().shape[0]} bars @ {panel.primary_tf}")

        ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel, seed=seed)

        genomes = sampler.sample(market, n_random=6)
        # add one mutation to exercise the evolutionary operator + lineage
        genomes.append(mutate(genomes[0], rng))

        stats = {"generated": len(genomes), "new": 0, "dup": 0, "evaluated": 0,
                 "rejected": 0, "admitted": 0, "verdicts": []}

        for g in genomes:
            newly = store.register_genome(g)
            stats["new" if newly else "dup"] += 1

            res = evaluate(g, panel, seed)
            store.record_eval(res)                       # EVERY eval → ledger (honest N)
            stats["evaluated"] += 1

            n_trials = store.trial_count()               # deflate for everything tried so far
            report = gauntlet.run(g, res, trial_count=n_trials, ctx=ctx)
            store.record_gauntlet(g.genome_id, market, report.passed, report.failed_gate,
                                  report.gates, report.fitness)

            if report.passed:
                outcome = archive.insert(g, res, report)
                stats["admitted"] += 1
                verdict = f"ADMIT→{outcome.action}({outcome.niche})"
            else:
                stats["rejected"] += 1
                verdict = f"REJECT@{report.failed_gate}"
            stats["verdicts"].append({"genome": g.genome_id, "generator": g.generator, "verdict": verdict})
            print(f"    {g.genome_id} {g.generator:18} {verdict:30} "
                  f"sharpe={_fmt(res.summary.get('net_sharpe'))} "
                  f"dsr_p={_fmt(report.gates.get('G4_deflated_sharpe',{}).get('dsr_pvalue'))}")

        run_report["markets"][market] = stats
        print(f"  -> generated {stats['generated']} ({stats['new']} new / {stats['dup']} dup), "
              f"rejected {stats['rejected']}, admitted {stats['admitted']}")

    _archive_mechanism_check(store)

    elapsed = time.time() - t0
    run_report["elapsed_s"] = round(elapsed, 2)
    run_report["ledger_trial_count"] = store.trial_count()
    run_report["genome_registry_count"] = store.genome_count()
    run_report["archive_coverage"] = archive.coverage()

    _print_summary(run_report, store)
    _save(run_report)
    store.close()
    return run_report


def _core_file(market: str) -> str:
    man = Path(str(DATA_SNAPSHOT_ID)).name
    from mt.config import LAKE_DIR
    p = LAKE_DIR / DATA_SNAPSHOT_ID / market / "_manifest.json"
    if p.exists():
        return json.loads(p.read_text())["market_core_file"]
    return "?"


def _archive_mechanism_check(store: MTStore):
    """Prove the MAP-Elites occupy/replace logic deterministically (labeled; not a discovery)."""
    print("\n### ARCHIVE MECHANISM CHECK  [synthetic elites — proves niche occupy/replace]")
    a = store.upsert_archive("crypto:swing:low:neutral", "deadbeef00000001", "crypto",
                             {"deflated_sharpe": 1.2}, {"hold_bucket": "swing"}, scalar_fit=1.2)
    b = store.upsert_archive("crypto:swing:low:neutral", "deadbeef00000002", "crypto",
                             {"deflated_sharpe": 1.8}, {"hold_bucket": "swing"}, scalar_fit=1.8)
    c = store.upsert_archive("crypto:swing:low:neutral", "deadbeef00000003", "crypto",
                             {"deflated_sharpe": 0.4}, {"hold_bucket": "swing"}, scalar_fit=0.4)
    print(f"  first insert (empty niche)     -> {a}   (expect: occupy)")
    print(f"  fitter challenger              -> {b}   (expect: replace)")
    print(f"  weaker challenger              -> {c}   (expect: keep)")


def _print_summary(rep: dict, store: MTStore):
    print("\n" + "=" * 78)
    print(" RUN SUMMARY")
    print("=" * 78)
    print(f"  isolation proof (each market resolved its OWN core in a separate process):")
    for m, cf in rep["isolation"].items():
        print(f"     {m:7} -> {cf}")
    print(f"\n  genome registry : {rep['genome_registry_count']} unique genomes")
    print(f"  result ledger   : {rep['ledger_trial_count']} evaluations (the honest DSR trial count N)")
    natural = max(0, rep['archive_coverage'] - 1)   # the mechanism check occupies exactly 1 labeled niche
    print(f"  archive niches  : {rep['archive_coverage']} occupied "
          f"({natural} natural + 1 labeled mechanism-check niche)")
    tot_rej = sum(s["rejected"] for s in rep["markets"].values())
    tot_adm = sum(s["admitted"] for s in rep["markets"].values())
    tot_gen = sum(s["generated"] for s in rep["markets"].values())
    print(f"  verdicts        : {tot_gen} genomes → {tot_rej} rejected / {tot_adm} admitted "
          f"({tot_rej/max(1,tot_gen):.0%} rejection rate)")
    print(f"  elapsed         : {rep['elapsed_s']}s")
    print("\n  On edgeless synthetic data a high rejection rate is the immune system WORKING")
    print("  (docs/00 §2). Real Binance/OANDA history + the full G2/G3/G6/G7/G8 gates come next.")
    print("=" * 78)


def _save(rep: dict):
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out = RUNS_DIR / f"demo_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\n  run artifact saved: {out}")


def _fmt(v):
    try:
        return f"{float(v):+.3f}"
    except (TypeError, ValueError):
        return "  n/a "


def main():
    ap = argparse.ArgumentParser(description="Master Trader thin end-to-end demo.")
    ap.add_argument("--markets", default="crypto,fx,xau")
    ap.add_argument("--bars", type=int, default=600)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--no-reset", action="store_true", help="accumulate into the existing ledger")
    args = ap.parse_args()
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    run(markets, bars=args.bars, seed=args.seed, reset=not args.no_reset)


if __name__ == "__main__":
    main()
