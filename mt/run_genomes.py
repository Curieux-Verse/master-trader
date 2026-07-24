"""mt.run_genomes — the categorized Genome Population Report (Markdown).

A curated, readable window into the live population rather than a raw dump: an executive
summary, the TOP CANDIDATES ranked by how close they came to clearing the Deflated Sharpe
(with their full typed DSL and the gate that actually killed them), the gate-failure funnel,
and complete categorical coverage — by market, phenotype, engine, regime, sizing and family.

Read-only; it just streams var/mt.db.

    python -m mt.run_genomes                     # → var/runs/genomes_current.md
    python -m mt.run_genomes --top 30            # more headline candidates
    python -m mt.run_genomes --full              # + exhaustive one-line index of every genome
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone

from mt.config import DB_PATH, RUNS_DIR, MARKETS
from mt.genome.schema import Genome
from mt.improve.bandit import engine_of
from mt.improve.critic import families

Z_PASS = 1.645          # DSR z a candidate must clear to be "not luck" at p<0.05


# ─── helpers ─────────────────────────────────────────────────────────────
def _f(x, nd=3):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, (int, float)) else str(x))


def _bar(frac, width=18):
    n = 0 if frac is None else max(0, min(width, int(round(frac * width))))
    return "█" * n + "·" * (width - n)


class Agg:
    """One category's rollup: how many, and how close its best came to the bar."""
    __slots__ = ("n", "best_z", "best_id", "passed")

    def __init__(self):
        self.n = 0; self.best_z = None; self.best_id = None; self.passed = 0

    def add(self, z, gid, passed):
        self.n += 1
        self.passed += 1 if passed else 0
        if z is not None and (self.best_z is None or z > self.best_z):
            self.best_z, self.best_id = z, gid


def _table(title, agg_map, limit=None, label="category"):
    rows = sorted(agg_map.items(), key=lambda kv: (-(kv[1].best_z if kv[1].best_z is not None else -9e9), -kv[1].n))
    if limit:
        rows = rows[:limit]
    L = [f"**{title}**", "",
         f"| {label} | genomes | admitted | best DSR-z | vs bar (1.645) |",
         "|---|---:|---:|---:|---|"]
    for k, a in rows:
        frac = None if a.best_z is None else a.best_z / Z_PASS
        L.append(f"| `{k}` | {a.n} | {a.passed} | {_f(a.best_z, 2)} | {_bar(frac)} |")
    L.append("")
    return L


# ─── main ────────────────────────────────────────────────────────────────
def dump(db_path=None, out_path=None, top_n=20, full=False) -> str:
    conn = sqlite3.connect(str(db_path or DB_PATH))
    conn.row_factory = sqlite3.Row

    sql = """
    SELECT g.genome_id, g.market, g.generator, g.complexity, g.body, g.prose,
           r.passed AS passed, r.failed_gate AS failed_gate, r.gates AS gates,
           l.net_sharpe AS net_sharpe, l.sharpe_pp AS sharpe_pp, l.max_dd AS max_dd, l.n_periods AS n_periods
    FROM genomes g
    LEFT JOIN (SELECT genome_id, passed, failed_gate, gates,
                      ROW_NUMBER() OVER (PARTITION BY genome_id ORDER BY report_id DESC) rn
               FROM gauntlet_reports) r ON r.genome_id = g.genome_id AND r.rn = 1
    LEFT JOIN (SELECT genome_id, net_sharpe, sharpe_pp, max_dd, n_periods,
                      ROW_NUMBER() OVER (PARTITION BY genome_id ORDER BY eval_id DESC) rn
               FROM result_ledger) l ON l.genome_id = g.genome_id AND l.rn = 1
    """

    by_market, by_engine, by_pheno = defaultdict(Agg), defaultdict(Agg), defaultdict(Agg)
    by_regime, by_sizing, by_family = defaultdict(Agg), defaultdict(Agg), defaultdict(Agg)
    gate_funnel = Counter()
    top: list = []                      # [(z, row-dict)] kept small
    total = admitted = 0
    compact: list = []

    for row in conn.execute(sql):
        total += 1
        try:
            g = Genome.from_dict(json.loads(row["body"]))
        except Exception:
            continue
        z = None
        if row["gates"]:
            try:
                z = (json.loads(row["gates"]).get("G4_deflated_sharpe", {}) or {}).get("dsr_z")
            except Exception:
                z = None
        z = float(z) if isinstance(z, (int, float)) else None
        passed = bool(row["passed"])
        admitted += 1 if passed else 0
        gate_funnel[row["failed_gate"] or ("ADMITTED" if passed else "—")] += 1

        eng = engine_of(row["generator"]); pheno = g.meta.execution
        regime = g.signal.args.get("regime", "all"); sizing = g.sizing.op
        fams = families(g)
        gid = row["genome_id"]
        for m, k in ((by_market, row["market"]), (by_engine, eng), (by_pheno, pheno),
                     (by_regime, regime), (by_sizing, sizing)):
            m[k].add(z, gid, passed)
        for t in fams:
            by_family[t].add(z, gid, passed)

        rec = {"id": gid, "market": row["market"], "engine": eng, "pheno": pheno,
               "regime": regime, "sizing": sizing, "fams": fams, "z": z,
               "sharpe_pp": row["sharpe_pp"], "net_sharpe": row["net_sharpe"],
               "max_dd": row["max_dd"], "n_periods": row["n_periods"],
               "gate": row["failed_gate"], "passed": passed, "prose": row["prose"]}
        if z is not None:
            top.append((z, rec))
            if len(top) > 4000:                       # bound memory; keep the strongest
                top.sort(key=lambda t: -t[0]); top = top[:top_n * 4]
        if full:
            compact.append(rec)

    lessons = [r[0] for r in conn.execute("SELECT text FROM lessons ORDER BY id DESC LIMIT 400").fetchall()]
    n_lessons = conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    n_trials = conn.execute("SELECT COUNT(*) FROM result_ledger").fetchone()[0]
    scr = conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger").fetchone()[0] or 0
    arch = conn.execute("SELECT niche_key, market, scalar_fit FROM archive ORDER BY scalar_fit DESC").fetchall()
    from mt.store.db import MTStore
    store = MTStore(db_path=db_path or DB_PATH)
    rho = store.avg_trial_corr()
    n_eff = store.effective_trial_count(None, rho)
    attributions = store.top_feature_attributions(None, limit=15)
    store.close()
    conn.close()

    top.sort(key=lambda t: -t[0])
    best = top[0][1] if top else None

    # ── render ───────────────────────────────────────────────────────────
    L = []
    L.append("# 🧬 Master Trader — Genome Population Report")
    L.append("")
    L.append(f"*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
             f"source `{(db_path or DB_PATH)}`*")
    L.append("")

    # 1 — executive summary
    L.append("## 1 · Executive summary")
    L.append("")
    L.append("| | |")
    L.append("|---|---|")
    L.append(f"| Genomes generated & tested | **{total:,}** |")
    L.append(f"| Deflated-Sharpe trial count (raw N) | **{n_trials + scr:,}** *(evals {n_trials:,} + {scr:,} screened)* |")
    if n_eff is not None:
        L.append(f"| **Effective** independent trials (N_eff) | **{n_eff:,}** *(ρ̄={rho} — the bar the DSR actually uses)* |")
    L.append(f"| Admitted to archive | **{admitted}** |")
    L.append(f"| Rejected | **{total - admitted:,}** ({(total-admitted)/max(1,total):.1%}) |")
    L.append(f"| Distinct families explored | **{len(by_family)}** |")
    L.append(f"| Lessons accumulated | **{n_lessons:,}** |")
    if best:
        cleared = "✅ **cleared the bar**" if best["z"] >= Z_PASS else "below the bar"
        L.append(f"| Best DSR-z | **{best['z']:+.3f}** vs bar {Z_PASS} — {cleared} |")
    L.append("")
    if best and best["z"] >= Z_PASS and admitted == 0:
        L.append(f"> ### ⚠️ Headline: a candidate cleared the significance bar — and was still rejected")
        L.append(f"> Genome `{best['id']}` reached **DSR-z {best['z']:+.2f}** (> {Z_PASS}), i.e. its edge is *not* "
                 f"explainable by luck across {n_trials + scr:,} trials. It was nonetheless killed at "
                 f"**`{best['gate']}`** — a *later*, independent gate. This is the layered gauntlet working as "
                 f"designed: clearing multiple-testing is necessary, not sufficient.")
        L.append("")
    L.append("**How to read `DSR-z`:** `0` = the luck bar (what the best of N random trials would score); "
             f"**`{Z_PASS}` = statistically significant at p<0.05.** Higher is better; it is the single "
             "number that says how close the search is to a genuine edge.")
    L.append("")
    L.append("---")

    # 2 — top candidates
    L.append("")
    L.append(f"## 2 · 🏆 Top {min(top_n, len(top))} candidates (closest to a real edge)")
    L.append("")
    L.append("| # | genome | market | DSR-z | sharpe/obs | net sharpe | max DD | phenotype | regime | died at |")
    L.append("|--:|---|---|---:|---:|---:|---:|---|---|---|")
    for i, (_, r) in enumerate(top[:top_n], 1):
        flag = " ✅" if r["z"] is not None and r["z"] >= Z_PASS else ""
        L.append(f"| {i} | `{r['id']}` | {r['market']} | **{_f(r['z'],2)}**{flag} | {_f(r['sharpe_pp'],4)} "
                 f"| {_f(r['net_sharpe'],2)} | {_f(r['max_dd'],3)} | {r['pheno']} | {r['regime']} "
                 f"| `{r['gate'] or 'ADMITTED'}` |")
    L.append("")
    L.append("<details><summary><b>Full DSL recipes for the top candidates</b></summary>")
    L.append("")
    for i, (_, r) in enumerate(top[:top_n], 1):
        L.append(f"**#{i} · `{r['id']}` — DSR-z {_f(r['z'],2)} · died at `{r['gate'] or 'ADMITTED'}` · "
                 f"families: {', '.join(r['fams'])}**")
        L.append("```")
        L.append((r["prose"] or "").rstrip())
        L.append("```")
    L.append("</details>")
    L.append("")
    L.append("---")

    # 3 — gate funnel
    L.append("")
    L.append("## 3 · Where genomes die — the gate funnel")
    L.append("")
    L.append("Each candidate is killed by the **first** gate it fails. Cheap gates run first.")
    L.append("")
    L.append("| gate | genomes killed | share | what it means |")
    L.append("|---|---:|---:|---|")
    meaning = {
        "G0_eval": "did not produce a valid backtest",
        "G1_sanity": "degenerate / too few periods, or one period dominates P&L",
        "G4_deflated_sharpe": "edge indistinguishable from luck after trial correction",
        "G4b_reality_check": "not significant under stationary-block bootstrap (non-parametric)",
        "G5_robustness": "bootstrap tail drawdown too large",
        "G2_oos": "shines in-sample, decays out-of-sample",
        "G7_capacity": "edge evaporates under 2× costs",
        "G8_orthogonality": "duplicates an existing archive member",
        "G3_cpcv_pbo": "parameter tuning overfit (high PBO)",
        "G6_transfer": "does not transfer to the held-out period",
        "ADMITTED": "**cleared every gate**",
    }
    for gate, cnt in gate_funnel.most_common():
        L.append(f"| `{gate}` | {cnt:,} | {cnt/max(1,total):.1%} | {meaning.get(gate,'—')} |")
    L.append("")
    L.append("---")

    # 4 — categorized breakdowns
    L.append("")
    L.append("## 4 · Categorized breakdown")
    L.append("")
    L.append("*`best DSR-z` per category is the meaningful column — it shows **where the search is finding "
             "signal**, not merely where it spent effort.*")
    L.append("")
    L.append("### 4.1 By market"); L += _table("Market", by_market, label="market")
    L.append("### 4.2 By phenotype"); L += _table("Execution style", by_pheno, label="phenotype")
    L.append("### 4.3 By generation engine"); L += _table("Engine", by_engine, label="engine")
    L.append("### 4.4 By regime conditioning"); L += _table("Regime", by_regime, label="regime")
    L.append("### 4.5 By position sizing"); L += _table("Sizing", by_sizing, label="sizing op")
    L.append(f"### 4.6 By strategy family — all {len(by_family)} explored")
    L += _table("Family (ranked by best DSR-z)", by_family, label="family")
    L.append("---")

    # 4.7 — measured feature attribution
    if attributions:
        L.append("")
        L.append("### 4.7 Feature attribution — which primitives *measurably* carry signal")
        L.append("")
        L.append("*Leave-one-out ΔDSR-z on near-miss genomes: how much **dropping** each feature lowered the "
                 "Deflated-Sharpe z. Positive ⇒ the feature carried edge; ≤0 ⇒ it was inert or noise. This is "
                 "measured contribution, not the family it's tagged under.*")
        L.append("")
        L.append("| feature | times measured | mean ΔDSR-z | verdict |")
        L.append("|---|---:|---:|---|")
        for op, nm, dz in attributions:
            verdict = "**carries signal**" if dz > 0.05 else ("inert / noise" if dz <= 0 else "marginal")
            L.append(f"| `{op}` | {nm} | {dz:+.3f} | {verdict} |")
        L.append("")
    L.append("---")

    # 5 — archive + lessons
    L.append("")
    L.append(f"## 5 · Archive ({len(arch)} niches)")
    L.append("")
    if arch:
        L.append("| niche | market | fitness |"); L.append("|---|---|---:|")
        for a in arch[:25]:
            L.append(f"| `{a['niche_key']}` | {a['market']} | {a['scalar_fit']:.3f} |")
    else:
        L.append("*Empty — nothing has cleared all eight gates. Honest: no genuine edge yet.*")
    L.append("")
    L.append(f"## 6 · Lessons library ({n_lessons:,})")
    L.append("")
    lc = Counter()
    for t in lessons:
        try:
            d = json.loads(t); lc[f"[{d.get('gate','')}] {d.get('general_lesson','')[:110]}"] += 1
        except Exception:
            lc[t[:110]] += 1
    for txt, c in lc.most_common(15):
        L.append(f"- ×{c} — {txt}")
    L.append("")

    if full and compact:
        L.append("---")
        L.append("")
        L.append(f"## 7 · Appendix — every genome ({len(compact):,})")
        L.append("")
        L.append("| genome | market | engine | phenotype | regime | sizing | DSR-z | died at |")
        L.append("|---|---|---|---|---|---|---:|---|")
        for r in sorted(compact, key=lambda r: -(r["z"] if r["z"] is not None else -9e9)):
            L.append(f"| `{r['id']}` | {r['market']} | {r['engine']} | {r['pheno']} | {r['regime']} "
                     f"| {r['sizing']} | {_f(r['z'],2)} | `{r['gate'] or 'ADMITTED'}` |")
        L.append("")

    L.append("---")
    L.append("")
    L.append("🔒 *Paper/research only — no live-capital action is taken or authorized. "
             "A genome in this report is a **candidate**, never a recommendation to trade.*")

    text = "\n".join(L)
    out = out_path or (RUNS_DIR / "genomes_current.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    return str(out)


def main():
    ap = argparse.ArgumentParser(description="Categorized genome population report.")
    ap.add_argument("--out", default=None)
    ap.add_argument("--db", default=None)
    ap.add_argument("--top", type=int, default=20, help="headline candidates shown in full")
    ap.add_argument("--full", action="store_true", help="append a one-line index of EVERY genome")
    args = ap.parse_args()
    path = dump(db_path=args.db, out_path=args.out, top_n=args.top, full=args.full)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
