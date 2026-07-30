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

import numpy as np

from mt.config import DB_PATH, RUNS_DIR, MARKETS, DEFAULT_SEED
from mt.adapters import MarketAdapter
from mt.data.lake import read_lake_panel, lake_has_data, snapshot_info
from mt.store import MTStore
from mt.improve import DiscoveryLoop
from mt.live import PaperBook
from mt.live.report import format_system_report, format_telegram_report, send_telegram


# Point-in-time split of real history, as (start_frac, end_frac). Named so the invariant below is
# machine-checkable: the self-test asserts holdout_width >= train_width, because the moment the
# TRAIN window becomes the longer one, the search can promote horizons the confirmation stage
# cannot test (see the reasoning in _build_panels).
TRAIN_SPAN = (0.0, 0.40)
HOLDOUT_SPAN = (0.42, 0.84)
LIVE_SPAN = (0.86, 1.0)


def span_width(span) -> float:
    return float(span[1] - span[0])


def _build_panels(market, source, snapshot_id, seed, structure):
    """Return (train, holdout, live) panels. Real data is split by TIME (point-in-time);
    synthetic data uses independent seeded realizations."""
    if source == "lake":
        if not lake_has_data(market, snapshot_id):
            return None
        # ~2% EMBARGO GAPS are dropped between splits: adjacent bars are serially correlated, so an
        # unembargoed holdout/live isn't truly out-of-sample (López de Prado purge/embargo).
        #
        # THE HOLDOUT IS DELIBERATELY THE LONGER WINDOW (0.42 vs 0.40), and that inequality is the
        # invariant, not a tuning choice.
        #
        # A genome needs T ≥ MIN_PERIODS observations to be judged at all, and T = bars/horizon, so
        # each window imposes a horizon ceiling of bars/MIN_PERIODS. If the training window is the
        # longer one, its ceiling is HIGHER, and the gap between the two ceilings is a band of
        # horizons the search can promote but the confirmation stage is structurally incapable of
        # testing. Measured on the 2026-07-29 marathon under the old 0.53/0.25 split: fx and xau
        # trained on ~794 bars and held out ~375, admitting horizons to 39 while confirming at most
        # 18 — a dead band at 19–39 that killed 12 of 21 finalists at G1, several with POSITIVE
        # out-of-sample Sharpe.
        #
        # Making the holdout the longer window closes that band BY CONSTRUCTION rather than
        # shrinking it: holdout ≥ train ⇒ ceiling_holdout ≥ ceiling_train ⇒ nothing promotable is
        # unconfirmable, at every market and every history length. Equal fractions would leave a
        # residual band wherever rounding on the union calendar makes the holdout a few bars
        # shorter (measured at 30–31 for fx/xau when the split was 0.42/0.40).
        #
        # It also buys power where it is scarcest. The confirmatory bar falls as 1/√T, so this cuts
        # the required per-period Sharpe by ~21% (crypto ~998 → ~1600 observations, fx/xau ~375 →
        # ~600). Stage B is the binding constraint — 0 cleared with crypto's book at p=0.055 — so
        # history is worth more there than in a search that already had 2000 bars. Discovery pays
        # ~13% of its t-statistic for it, the right trade while confirmation is what fails.
        #
        # The holdout cap matches the train cap on purpose: a smaller one (it was 1200) would
        # silently reintroduce the asymmetry on any market with deep enough history.
        train = read_lake_panel(market, snapshot_id, *TRAIN_SPAN, max_bars=2000)     # discovery
        holdout = read_lake_panel(market, snapshot_id, *HOLDOUT_SPAN, max_bars=2000)  # transfer (G6)
        live = read_lake_panel(market, snapshot_id, *LIVE_SPAN, max_bars=400)       # recent → paper
        return train, holdout, live
    a = MarketAdapter(market)
    return (a.build_panel(bars=440, seed=seed, structure=structure, snapshot_id=f"sys_{market}"),
            a.build_panel(bars=440, seed=seed + 1, structure=structure, snapshot_id=f"sysho_{market}"),
            a.build_panel(bars=440, seed=seed + 2, structure=structure, snapshot_id=f"syslive_{market}"))


def _reset_db():
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB_PATH) + suffix)
        if p.exists():
            p.unlink()


def run_system(markets, generations: int, batch_size: int, seed: int, structure: float,
               paper_days: int, reset: bool = True, use_ollama: bool = False,
               source: str = "synthetic", snapshot_id: str = "real") -> dict:
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

    # ── build panels per market (real lake = time-split; synthetic = seeded) ──
    print(f"\n  DATA SOURCE: {'REAL LAKE (' + snapshot_id + ')' if source == 'lake' else 'synthetic (structure=' + str(structure) + ')'}")
    loops = {}
    live_panels = {}
    active = []
    for m in markets:
        panels = _build_panels(m, source, snapshot_id, seed, structure)
        if panels is None:
            print(f"  [{m}] no lake data for snapshot '{snapshot_id}' — skipping (run mt.run_ingest first).")
            continue
        panel, holdout, live_panels[m] = panels
        if source == "lake":
            info = snapshot_info(m, snapshot_id) or {}
            print(f"  [{m}] REAL {info.get('source','')}: {len(panel.symbols)} symbols × "
                  f"{panel.close_matrix().shape[0]} train bars @ {panel.primary_tf}  #{info.get('content_hash','')}")
        else:
            print(f"  [{m}] synthetic (worker in {MARKETS[m].root.name}): {len(panel.symbols)} symbols")
        loops[m] = DiscoveryLoop(store, m, panel, holdout, seed=seed, use_ollama=use_ollama)
        active.append(m)
    markets = active
    if not markets:
        print("\n  No markets have data. Run: python -m mt.run_ingest --markets crypto,fx,xau")
        store.close()
        return {"error": "no_data"}

    # ── INNER LOOP: discovery across all markets, generation by generation ──
    print(f"\n{'─'*72}\n INNER LOOP — {generations} generations × {len(markets)} markets\n{'─'*72}")
    fam_all: Counter = Counter(); pheno_all: Counter = Counter(); last_bandit = {}
    z_trend = []                        # per-gen: N-independent edge_t (learning) + best DSR-z (distance)
    for gen in range(generations):
        line = []; gen_e = []; gen_zbest = []
        for m in markets:
            st = loops[m].run_generation(batch_size=batch_size)
            fam_all.update(st["families_tested"]); pheno_all.update(st["phenotypes_tested"])
            last_bandit[m] = st["bandit_weights"]
            if st.get("edge_t_median") is not None:
                gen_e.append(st["edge_t_median"])
            if st.get("dsr_z_best") is not None:
                gen_zbest.append(st["dsr_z_best"])
            et = st.get("edge_t_median")
            line.append(f"{m}:arch{st['archive_coverage']}" + ("" if et is None else f"(t̃{et:+.2f})"))
        emed = float(np.median(gen_e)) if gen_e else None
        zbest = max(gen_zbest) if gen_zbest else None
        z_trend.append({"gen": gen + 1, "edge_t_median": emed, "z_best": zbest})
        print(f"  gen {gen+1:2}: " + "  ".join(line) +
              f"   | ledger N={store.trial_count()}  lessons={store.lesson_count()}")

    # ── discovery aggregate ──
    gr = store.conn.execute("SELECT passed, COUNT(*) FROM gauntlet_reports GROUP BY passed").fetchall()
    passed = sum(c for p, c in gr if p); rejected = sum(c for p, c in gr if not p)
    evaluated = store.trial_count()
    rho = store.avg_trial_corr()
    discovery = {
        "generations": generations, "evaluated": evaluated, "admitted": passed, "rejected": rejected,
        "reject_rate": rejected / max(1, passed + rejected), "n_families": len(fam_all),
        "phenotypes": dict(pheno_all), "bandit": last_bandit.get(markets[0], {}),
        "trial_corr": None if rho is None else round(rho, 4),
        "effective_trials": store.effective_trial_count(None, rho),
        **_convergence(z_trend),
    }

    # ── archive snapshot ──
    elites_rows = store.archive_rows()
    archive = {"coverage": len(elites_rows), "qd_score": round(store.qd_score(), 4),
               "cleared": len(store.archive_rows(cleared_only=True)),
               "elites": [{"niche": r["niche_key"], "fit": r["scalar_fit"], "market": r["market"],
                           "cleared": bool(r["cleared"])} for r in elites_rows]}

    # ── OUTER LOOP: promote elites → paper/shadow per market ──
    print(f"\n{'─'*72}\n OUTER LOOP — promote archive → paper/shadow (R1, no capital)\n{'─'*72}")
    paper_agg = {"days": paper_days, "events": [], "n_strategies": 0, "tracked": 0, "book_sharpes": []}
    for m in markets:
        # ONLY Stage-B–confirmed members are eligible for paper. The archive now admits by
        # behavioural niche (canonical MAP-Elites), so membership means "worth remembering", NOT
        # "worth trading" — papering a merely-promoted candidate would quietly undo the whole
        # point of separating exploration from confirmation (docs/15 §4).
        rows = [r for r in elites_rows if r["market"] == m and r["cleared"]]
        elites = []
        for r in rows:
            g = store.get_genome(r["genome_id"])
            if g is not None:
                elites.append((g, store.genome_sharpe_pp(r["genome_id"])))
        if not elites:
            n_prom = sum(1 for r in elites_rows if r["market"] == m and r["promoted"])
            print(f"  [{m}] no CONFIRMED elites to paper-trade "
                  f"({n_prom} promoted candidates awaiting Stage-B confirmation).")
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
    send_telegram(format_telegram_report(rep))          # clean, emoji, mobile-first HTML digest
    out = RUNS_DIR / f"system_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\n  full report saved: {out}\n  elapsed: {rep['elapsed_s']}s")
    store.close()
    return rep


_MIN_GENS_FOR_TREND = 8


def _convergence(z_trend: list, best_z_floor: float = None) -> dict:
    """Steering verdict — WHICH wall are we on? Two signals, and the DISTINCTION matters:

      • best-z (the DISCOVERY signal): how close the single best genome is to clearing G4. This is
        the tail we actually care about (z=0 is the luck bar; a pass needs z ≳ 1.64).
      • median edge-t (the EXPLORATION FLOOR): the *typical* genome's single-strategy t-stat. Most
        genomes are random/exploratory, so this sits near zero *by construction* on an efficient
        market — it is NOT a quality score, and a few noisy points must not be read as a trend.

    `best_z_floor` is the ALL-TIME hall-of-fame high-water mark (docs/14). The per-run z_trend
    resets every marathon, so on its own best-z spuriously "regresses" when a short/cold run hasn't
    re-climbed yet; flooring the headline best-z with the persisted best makes it a true
    cross-marathon progress metric that ratchets and never drops. `this_run_best_z` keeps the raw
    within-run climb visible alongside it.

    So the verdict needs ≥8 generations and a noise-aware dead-band; below that we refuse to call
    it. The median is judged by a least-squares slope vs its own scatter, never a 2-point delta."""
    pts = [(t["gen"], t["edge_t_median"]) for t in z_trend if t.get("edge_t_median") is not None]
    run_best_z = max((t["z_best"] for t in z_trend if t.get("z_best") is not None), default=None)
    # headline best-z = max(this run's climb, all-time hall-of-fame high-water mark)
    if best_z_floor is not None:
        best_z = best_z_floor if run_best_z is None else max(run_best_z, float(best_z_floor))
    else:
        best_z = run_best_z
    # is the BEST improving? compare the best-z of the recent half vs the early half
    zb = [t["z_best"] for t in z_trend if t.get("z_best") is not None]
    best_recent = max(zb[len(zb) // 2:], default=None) if zb else None
    best_early = max(zb[:len(zb) // 2], default=None) if len(zb) > 1 else None
    out = {"trend": z_trend, "dsr_z_best": best_z, "this_run_best_z": run_best_z,
           "dsr_gap_to_significance": None if best_z is None else round(1.645 - best_z, 3),
           "best_z_recent": best_recent, "best_z_early": best_early}
    if len(pts) < _MIN_GENS_FOR_TREND:
        out["convergence"] = (f"warming up ({len(pts)} gen) — too few to call a trend (per-gen medians "
                              f"are noisy); watch best-z, and run mt.run_continuous for many generations")
        return out
    gens = np.array([g for g, _ in pts], float); vals = np.array([v for _, v in pts], float)
    slope = float(np.polyfit(gens, vals, 1)[0])
    span = slope * (gens[-1] - gens[0])                       # total drift the fit implies
    band = max(0.15, 0.6 * float(vals.std()))                # dead-band scaled to the scatter
    out["edge_t_slope_per_gen"] = round(slope, 4)
    if abs(span) < band:
        out["convergence"] = ("FLOOR STEADY — median edge sits at the noise floor (expected on an "
                              "efficient space); judge progress by best-z, and feed new data/conditioning")
    elif span > 0:
        out["convergence"] = (f"LEARNING — median edge rising ({span:+.2f} over {len(pts)} gens); "
                              f"generation is improving, scale compute")
    else:
        out["convergence"] = (f"SOFTENING — median edge easing ({span:+.2f}); usually just exploration "
                              f"noise — judge by best-z, not the median")
    return out


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
                    help="synthetic only: 0=pure random (honest, empty archive); >0 injects a labeled edge")
    ap.add_argument("--paper-days", type=int, default=12)
    ap.add_argument("--ollama", action="store_true", help="use local ollama to refine critic lessons")
    ap.add_argument("--source", choices=["synthetic", "lake"], default="synthetic",
                    help="'lake' = REAL data ingested by mt.run_ingest; 'synthetic' = isolated workers")
    ap.add_argument("--snapshot-id", default="real", help="lake snapshot to read (with --source lake)")
    args = ap.parse_args()
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    run_system(markets, args.generations, args.batch_size, args.seed, args.structure,
               args.paper_days, use_ollama=args.ollama, source=args.source, snapshot_id=args.snapshot_id)


if __name__ == "__main__":
    main()
