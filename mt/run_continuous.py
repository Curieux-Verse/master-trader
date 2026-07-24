"""mt.run_continuous — the unattended, scaled discovery loop (docs/06 §7, docs/09).

run_system is a short sprint that resets the DB; this is the marathon. It builds the panels
once, then runs discovery generation after generation into a PERSISTENT store (archive +
lessons + ledger accumulate), leaning the engine budget toward the directed generators
(evo/miner/llm) so N is spent on aimed bets rather than blind random. Every `--report-every`
generations it prints a digest with the DSR-z convergence steer — the diagnostic that says
whether the search is LEARNING (scale on) or FLAT (the space is efficient; feed it new
data/conditioning). Ctrl-C writes a final report and exits cleanly. No capital is ever placed.

    python -m mt.run_continuous --source lake --snapshot-id real --generations 100
    python -m mt.run_continuous --source lake --generations 0        # 0 = run until Ctrl-C
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime, timezone

import numpy as np

from mt.config import DB_PATH, RUNS_DIR, DEFAULT_SEED
from mt.store import MTStore
from mt.improve import DiscoveryLoop
from mt.run_system import _build_panels, _convergence, _pretty_lessons
from mt.live.report import format_system_report, format_telegram_report, send_telegram


def run(markets, generations, batch_size, seed, source, snapshot_id, structure,
        report_every=10, explore_floor=None, use_ollama=False, reset=False, max_minutes=0):
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if reset:
        from mt.run_system import _reset_db
        _reset_db()
    store = MTStore()
    floor = explore_floor if explore_floor is not None else {"evo": 0.3, "miner": 0.2}

    print("=" * 72)
    print(" MASTER TRADER — CONTINUOUS DISCOVERY  (unattended, accumulating, targeted)")
    print("=" * 72)
    print(f"  targeted-engine floor: {floor}   report every {report_every} gens   "
          f"{'until Ctrl-C' if generations <= 0 else str(generations)+' gens'}")

    loops, active = {}, []
    for m in markets:
        panels = _build_panels(m, source, snapshot_id, seed, structure)
        if panels is None:
            print(f"  [{m}] no lake data for '{snapshot_id}' — skipping.")
            continue
        panel, holdout, _live = panels
        loops[m] = DiscoveryLoop(store, m, panel, holdout, seed=seed,
                                 use_ollama=use_ollama, explore_floor=floor)
        active.append(m)
        print(f"  [{m}] {len(panel.symbols)} symbols × {panel.close_matrix().shape[0]} train bars")
    if not active:
        print("  No markets have data — run mt.run_ingest first.")
        store.close(); return
    markets = active

    t0 = time.time()
    z_trend = []
    fam_all, pheno_all = Counter(), Counter()
    gen = 0
    try:
        while generations <= 0 or gen < generations:
            if max_minutes and (time.time() - t0) / 60.0 >= max_minutes:
                print(f"\n  ⏱  reached --max-minutes={max_minutes} — stopping cleanly (state saved).")
                break
            gen += 1
            gen_e, gen_zbest = [], []
            for m in markets:
                st = loops[m].run_generation(batch_size=batch_size)
                fam_all.update(st["families_tested"]); pheno_all.update(st["phenotypes_tested"])
                if st.get("edge_t_median") is not None:
                    gen_e.append(st["edge_t_median"])
                if st.get("dsr_z_best") is not None:
                    gen_zbest.append(st["dsr_z_best"])
            z_trend.append({"gen": gen, "edge_t_median": (float(np.median(gen_e)) if gen_e else None),
                            "z_best": (max(gen_zbest) if gen_zbest else None)})
            arch = sum(loops[m].archive.coverage() for m in markets)
            admitted = store.conn.execute("SELECT COUNT(*) FROM gauntlet_reports WHERE passed=1").fetchone()[0]
            if gen % report_every == 0 or (generations > 0 and gen == generations):
                _digest(store, markets, z_trend, fam_all, pheno_all, gen, arch, admitted, t0,
                        bandit=loops[markets[0]].bandit.weights())
            else:
                et = z_trend[-1]["edge_t_median"]; zb = z_trend[-1]["z_best"]
                print(f"  gen {gen:4}: archive={arch:3} admitted={admitted:3} N={store.trial_count():6} "
                      f"lessons={store.lesson_count():3}  edge-t̃={_f(et)}  best-z={_f(zb)}")
    except KeyboardInterrupt:
        print("\n  ⏹  interrupted — writing final report…")

    _digest(store, markets, z_trend, fam_all, pheno_all, gen, arch, admitted, t0, final=True,
            bandit=loops[markets[0]].bandit.weights())
    store.close()


def _f(x):
    return "—" if x is None else f"{x:+.2f}"


def _digest(store, markets, z_trend, fam_all, pheno_all, gen, arch, admitted, t0, final=False, bandit=None):
    gr = store.conn.execute("SELECT passed, COUNT(*) FROM gauntlet_reports GROUP BY passed").fetchall()
    passed = sum(c for p, c in gr if p); rejected = sum(c for p, c in gr if not p)
    rho = store.avg_trial_corr()
    rep = {
        "started": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": round(time.time() - t0, 1), "markets": markets,
        "discovery": {"generations": gen, "evaluated": store.trial_count(),
                      "admitted": passed, "rejected": rejected,
                      "reject_rate": rejected / max(1, passed + rejected),
                      "n_families": len(fam_all), "phenotypes": dict(pheno_all),
                      "trial_corr": None if rho is None else round(rho, 4),
                      "effective_trials": store.effective_trial_count(None, rho),
                      "bandit": {k: round(v, 3) for k, v in (bandit or {}).items()},
                      **_convergence(z_trend)},
        "archive": {"coverage": arch, "elites": [{"niche": r["niche_key"], "fit": r["scalar_fit"],
                    "market": r["market"]} for r in store.archive_rows()[:8]]},
        "paper": {}, "lessons": store.lesson_count(),
        "recent_lessons": _pretty_lessons(store.recent_lessons(4)),
    }
    print("\n" + format_system_report(rep))
    send_telegram(format_telegram_report(rep))          # phone ping for the unattended marathon
    tag = "final" if final else f"gen{gen}"
    out = RUNS_DIR / f"continuous_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{tag}.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"  saved: {out}  ({rep['elapsed_s']}s, {gen} gens)\n")


def main():
    ap = argparse.ArgumentParser(description="Master Trader — continuous unattended discovery.")
    ap.add_argument("--markets", default="crypto,fx,xau")
    ap.add_argument("--generations", type=int, default=100, help="0 = run until Ctrl-C")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--source", choices=["synthetic", "lake"], default="lake")
    ap.add_argument("--snapshot-id", default="real")
    ap.add_argument("--structure", type=float, default=0.8, help="synthetic only")
    ap.add_argument("--report-every", type=int, default=10)
    ap.add_argument("--max-minutes", type=float, default=0,
                    help="wall-clock budget; stop cleanly after N minutes (0 = no limit). Use in CI "
                         "to finish and persist state before the runner's hard job cap.")
    ap.add_argument("--evo-floor", type=float, default=0.3)
    ap.add_argument("--miner-floor", type=float, default=0.2)
    ap.add_argument("--reset", action="store_true", help="wipe the DB before starting (fresh archive)")
    ap.add_argument("--ollama", action="store_true")
    args = ap.parse_args()
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    run(markets, args.generations, args.batch_size, args.seed, args.source, args.snapshot_id,
        args.structure, report_every=args.report_every,
        explore_floor={"evo": args.evo_floor, "miner": args.miner_floor},
        use_ollama=args.ollama, reset=args.reset, max_minutes=args.max_minutes)


if __name__ == "__main__":
    main()
