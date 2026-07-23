"""mt.run_genomes — dump every genome in the store to a human-readable Markdown file.

A window into the live population: what the discovery loop has actually generated and tested
per market, which engine minted each, its phenotype/family, its full typed DSL definition, and
how it fared in the Gauntlet (the honest verdict). Read-only — it just reads var/mt.db.

    python -m mt.run_genomes                       # → var/runs/genomes_current.md
    python -m mt.run_genomes --out somewhere.md    # custom path
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone

from mt.config import DB_PATH, RUNS_DIR, MARKETS
from mt.genome.schema import Genome
from mt.improve.bandit import engine_of
from mt.improve.critic import families


def _latest_ledger(conn, gid):
    r = conn.execute("SELECT net_sharpe, sharpe_pp, max_dd, n_periods, error FROM result_ledger "
                     "WHERE genome_id=? ORDER BY eval_id DESC LIMIT 1", (gid,)).fetchone()
    return r


def _latest_report(conn, gid):
    r = conn.execute("SELECT passed, failed_gate, gates FROM gauntlet_reports "
                     "WHERE genome_id=? ORDER BY report_id DESC LIMIT 1", (gid,)).fetchone()
    return r


def _fmt(x, nd=3):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, (int, float)) else str(x))


def dump(db_path=None, out_path=None) -> str:
    conn = sqlite3.connect(str(db_path or DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT genome_id, market, generator, generation, complexity, body, prose "
                        "FROM genomes ORDER BY market, generator").fetchall()

    by_market = {}
    for r in rows:
        by_market.setdefault(r["market"], []).append(r)

    L = []
    L.append(f"# Master Trader — live genome population")
    L.append("")
    L.append(f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} from "
             f"`{(db_path or DB_PATH)}` — {len(rows)} unique genomes (deduped by content hash)._")
    L.append("")
    L.append("Every genome the discovery loop has generated and tested, grouped by market. "
             "**Verdict** is the Gauntlet outcome: `ADMITTED` cleared all G1–G8, otherwise the "
             "first gate it failed. `sharpe_pp` is the per-observation Sharpe (what the Deflated "
             "Sharpe deflates); `DSR p` is the multiple-testing p-value.")
    L.append("")

    # ── global summary ───────────────────────────────────────────────────
    eng_tally, pheno_tally = {}, {}
    for r in rows:
        eng_tally[engine_of(r["generator"])] = eng_tally.get(engine_of(r["generator"]), 0) + 1
        g = Genome.from_dict(json.loads(r["body"]))
        pheno_tally[g.meta.execution] = pheno_tally.get(g.meta.execution, 0) + 1
    L.append(f"**Totals** — {len(rows)} genomes · engines "
             + ", ".join(f"{k}:{v}" for k, v in sorted(eng_tally.items(), key=lambda x: -x[1]))
             + " · phenotypes " + ", ".join(f"{k}:{v}" for k, v in pheno_tally.items()))
    L.append("")
    L.append("---")

    for market in [m for m in MARKETS if m in by_market] + [m for m in by_market if m not in MARKETS]:
        mrows = by_market[market]
        mk = MARKETS.get(market)
        fam_set, phenos = set(), {}
        parsed = []
        for r in mrows:
            g = Genome.from_dict(json.loads(r["body"]))
            fam = families(g)
            fam_set.update(fam)
            phenos[g.meta.execution] = phenos.get(g.meta.execution, 0) + 1
            parsed.append((r, g, fam))

        L.append("")
        L.append(f"## {market.upper()}  ({len(mrows)} genomes)")
        if mk:
            L.append(f"_{mk.kind} · htf {mk.htf} · universe { '/'.join(mk.universe[:6]) }"
                     + (f" … (+{len(mk.universe)-6})_" if len(mk.universe) > 6 else "_"))
        L.append(f"- phenotypes: " + ", ".join(f"{k} {v}" for k, v in phenos.items()))
        L.append(f"- families in play ({len(fam_set)}): " + ", ".join(sorted(fam_set)))
        L.append("")
        L.append("| # | id | engine | phenotype | sizing | families | sharpe_pp | net_sharpe | DSR p | verdict |")
        L.append("|--:|----|--------|-----------|--------|----------|----------:|-----------:|------:|---------|")
        for i, (r, g, fam) in enumerate(parsed, 1):
            lg = _latest_ledger(conn, r["genome_id"])
            rep = _latest_report(conn, r["genome_id"])
            dsr_p = None
            if rep and rep["gates"]:
                dsr_p = (json.loads(rep["gates"]).get("G4_deflated_sharpe", {}) or {}).get("dsr_pvalue")
            verdict = "**ADMITTED**" if (rep and rep["passed"]) else (rep["failed_gate"] if rep else "—")
            L.append(f"| {i} | `{r['genome_id']}` | {engine_of(r['generator'])} | {g.meta.execution} "
                     f"| {g.sizing.op} | {'+'.join(fam[:3])}{'…' if len(fam) > 3 else ''} "
                     f"| {_fmt(lg['sharpe_pp'] if lg else None)} | {_fmt(lg['net_sharpe'] if lg else None)} "
                     f"| {_fmt(dsr_p, 4)} | {verdict} |")

        # ── full definitions ─────────────────────────────────────────────
        L.append("")
        L.append(f"<details><summary><b>Full DSL definitions ({len(mrows)})</b></summary>")
        L.append("")
        for i, (r, g, fam) in enumerate(parsed, 1):
            L.append("```")
            L.append(r["prose"].rstrip())
            L.append("```")
        L.append("")
        L.append("</details>")
        L.append("")
        L.append("---")

    conn.close()
    text = "\n".join(L)
    out = out_path or (RUNS_DIR / "genomes_current.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    return str(out)


def main():
    ap = argparse.ArgumentParser(description="Dump the genome store to a readable Markdown file.")
    ap.add_argument("--out", default=None, help="output path (default var/runs/genomes_current.md)")
    ap.add_argument("--db", default=None, help="sqlite path (default var/mt.db)")
    args = ap.parse_args()
    path = dump(db_path=args.db, out_path=args.out)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
