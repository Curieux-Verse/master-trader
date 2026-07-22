"""mt.run_system — the COMPLETE system: inner discovery loop + outer paper loop.

Ties everything together across crypto + FX + XAU:

  INNER (discovery):  generate (bandit-split across engines) → simulate (Tier 1/2) →
                      Result Ledger → gauntlet (G1..G8, honest DSR) → MAP-Elites archive →
                      critic (lessons + targeted fixes) → bandit reallocation.  [× generations]

  OUTER (deployment): promote archive elites → paper/shadow on a live continuation feed
                      through the SAME simulator → regime-aware allocator + drift monitors +
                      circuit breakers → daily written report.

Governance: paper only. The machine NEVER self-authorizes a live-capital action (docs/07 §6).

    python -m mt.run_system --generations 4 --markets crypto,fx,xau --structure 0.8
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from mt.config import DB_PATH, RUNS_DIR, MARKETS, DEFAULT_SEED
from mt.adapters import MarketAdapter
from mt.store import MTStore
from mt.improve import DiscoveryLoop
from mt.live import PaperBook
from mt.live.report import format_system_report, send_telegram


def _reset_db():
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB_PATH) + suffix)
        if p.exists():
            p.unlink()


def run_system(markets, generations: int, batch_size: int, seed: int, structure: float,
               paper_days: int, reset: bool = True, use_ollama: bool = False) -> dict:
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if reset:
        _reset_db()
    store = MTStore()
    t0 = time.time()

    print("=" * 72)
    print(" MASTER TRADER — COMPLETE SYSTEM RUN  (inner discovery + outer paper loop)")
    print("=" * 72)

    # ── build isolated, structured panels per market (+ unseen holdout/live) ──
    loops = {}
    live_panels = {}
    for m in markets:
        print(f"\n[{m}] building isolated panels (structured synthetic; worker in {MARKETS[m].root.name})…")
        panel = MarketAdapter(m).build_panel(bars=440, seed=seed, structure=structure, snapshot_id=f"sys_{m}")
        holdout = MarketAdapter(m).build_panel(bars=440, seed=seed + 1, structure=structure, snapshot_id=f"sysho_{m}")
        live_panels[m] = MarketAdapter(m).build_panel(bars=440, seed=seed + 2, structure=structure, snapshot_id=f"syslive_{m}")
        loops[m] = DiscoveryLoop(store, m, panel, holdout, seed=seed, use_ollama=use_ollama)

    # ── INNER LOOP: discovery across all markets, generation by generation ──
    print(f"\n{'─'*72}\n INNER LOOP — {generations} generations × {len(markets)} markets\n{'─'*72}")
    fam_all: Counter = Counter(); pheno_all: Counter = Counter(); last_bandit = {}
    for gen in range(generations):
        line = []
        for m in markets:
            st = loops[m].run_generation(batch_size=batch_size)
            fam_all.update(st["families_tested"]); pheno_all.update(st["phenotypes_tested"])
            last_bandit[m] = st["bandit_weights"]
            line.append(f"{m}:arch{st['archive_coverage']}")
        print(f"  gen {gen+1:2}: " + "  ".join(line) +
              f"   | ledger N={store.trial_count()}  lessons={store.lesson_count()}")

    # ── discovery aggregate ──
    gr = store.conn.execute("SELECT passed, COUNT(*) FROM gauntlet_reports GROUP BY passed").fetchall()
    passed = sum(c for p, c in gr if p); rejected = sum(c for p, c in gr if not p)
    evaluated = store.trial_count()
    discovery = {
        "generations": generations, "evaluated": evaluated, "admitted": passed, "rejected": rejected,
        "reject_rate": rejected / max(1, passed + rejected), "n_families": len(fam_all),
        "phenotypes": dict(pheno_all), "bandit": last_bandit.get(markets[0], {}),
    }

    # ── archive snapshot ──
    elites_rows = store.archive_rows()
    archive = {"coverage": len(elites_rows),
               "elites": [{"niche": r["niche_key"], "fit": r["scalar_fit"], "market": r["market"]}
                          for r in elites_rows]}

    # ── OUTER LOOP: promote elites → paper/shadow per market ──
    print(f"\n{'─'*72}\n OUTER LOOP — promote archive → paper/shadow (R1, no capital)\n{'─'*72}")
    paper_agg = {"days": paper_days, "events": [], "n_strategies": 0, "tracked": 0, "book_sharpes": []}
    for m in markets:
        rows = [r for r in elites_rows if r["market"] == m]
        elites = []
        for r in rows:
            g = store.get_genome(r["genome_id"])
            if g is not None:
                elites.append((g, store.genome_sharpe_pp(r["genome_id"])))
        if not elites:
            print(f"  [{m}] no archive elites to paper-trade (honest: nothing cleared the gauntlet).")
            continue
        book = PaperBook(m, elites, seed=seed)
        pr = book.run(live_panels[m], n_days=paper_days)
        tracked = sum(1 for v in pr["live_vs_backtest"].values() if v["tracks_backtest"])
        paper_agg["n_strategies"] += len(elites); paper_agg["tracked"] += tracked
        paper_agg["events"] += [f"[{m}] {e}" for e in pr["events"]]
        if pr.get("book_sharpe") == pr.get("book_sharpe"):   # not NaN
            paper_agg["book_sharpes"].append(pr["book_sharpe"])
        print(f"  [{m}] papered {len(elites)} elites {paper_days}d → book_sharpe={pr['book_sharpe']} "
              f"| live≈backtest {tracked}/{len(elites)} | events={len(pr['events'])}")

    paper_agg["book_sharpe"] = (round(sum(paper_agg["book_sharpes"]) / len(paper_agg["book_sharpes"]), 3)
                                if paper_agg["book_sharpes"] else None)

    # ── assemble + emit report ──
    rep = {
        "started": datetime.now(timezone.utc).isoformat(), "elapsed_s": round(time.time() - t0, 1),
        "markets": markets, "discovery": discovery, "archive": archive, "paper": paper_agg,
        "lessons": store.lesson_count(), "recent_lessons": _pretty_lessons(store.recent_lessons(4)),
    }
    text = format_system_report(rep)
    print("\n" + text)
    send_telegram(text)
    out = RUNS_DIR / f"system_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\n  full report saved: {out}\n  elapsed: {rep['elapsed_s']}s")
    store.close()
    return rep


def _pretty_lessons(raw):
    out = []
    for t in raw:
        try:
            d = json.loads(t)
            out.append(f"[{d.get('gate','')}] {d.get('general_lesson','')}")
        except Exception:
            out.append(t[:120])
    return out


def main():
    ap = argparse.ArgumentParser(description="Master Trader — complete system run.")
    ap.add_argument("--markets", default="crypto,fx,xau")
    ap.add_argument("--generations", type=int, default=4)
    ap.add_argument("--batch-size", type=int, default=12)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--structure", type=float, default=0.8,
                    help="0=pure random (honest, empty archive); >0 injects a labeled synthetic edge to discover")
    ap.add_argument("--paper-days", type=int, default=12)
    ap.add_argument("--ollama", action="store_true", help="use local ollama to refine critic lessons")
    args = ap.parse_args()
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    run_system(markets, args.generations, args.batch_size, args.seed, args.structure,
               args.paper_days, use_ollama=args.ollama)


if __name__ == "__main__":
    main()
