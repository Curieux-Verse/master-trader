"""mt.store.db — the SQLite spine (Genome Registry, Result Ledger, Archive, Lessons).

Deliberately a NEW database (var/mt.db); the existing smc_signals.db is never touched.
The Result Ledger is sacred: it records EVERY evaluation — including genomes the
generators would otherwise discard quietly — because each is a "trial" that inflates the
best backtest by luck, and the Deflated Sharpe (G4) deflates for exactly that count.
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Optional

from mt.config import DB_PATH
from mt.genome.schema import Genome
from mt.sim.evalresult import EvalResult

_SCHEMA = """
CREATE TABLE IF NOT EXISTS genomes (
    genome_id   TEXT PRIMARY KEY,
    market      TEXT,
    generator   TEXT,
    generation  INTEGER,
    parents     TEXT,
    body        TEXT,
    prose       TEXT,
    complexity  INTEGER,
    created_at  REAL
);
CREATE TABLE IF NOT EXISTS result_ledger (
    eval_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    genome_id    TEXT,
    market       TEXT,
    fidelity     TEXT,
    seed         INTEGER,
    snapshot_id  TEXT,
    n_periods    INTEGER,
    net_sharpe   REAL,
    sharpe_pp    REAL,
    ann_return   REAL,
    max_dd       REAL,
    hit_rate     REAL,
    avg_turnover REAL,
    error        TEXT,
    created_at   REAL
);
CREATE INDEX IF NOT EXISTS ix_ledger_market ON result_ledger(market);
CREATE TABLE IF NOT EXISTS gauntlet_reports (
    report_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    genome_id    TEXT,
    market       TEXT,
    passed       INTEGER,
    failed_gate  TEXT,
    gates        TEXT,
    fitness      TEXT,
    created_at   REAL
);
CREATE TABLE IF NOT EXISTS archive (
    niche_key   TEXT PRIMARY KEY,
    genome_id   TEXT,
    market      TEXT,
    fitness     TEXT,
    descriptor  TEXT,
    scalar_fit  REAL,
    updated_at  REAL
);
CREATE TABLE IF NOT EXISTS lessons (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    text        TEXT,
    tags        TEXT,
    created_at  REAL
);
"""


class MTStore:
    def __init__(self, db_path: Optional[Path] = None):
        self.path = Path(db_path or DB_PATH)
        self.conn = sqlite3.connect(str(self.path), timeout=5)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ─── Genome Registry (dedup by content hash) ─────────────────────────
    def register_genome(self, g: Genome) -> bool:
        """Insert if new. Returns True if newly registered, False if already known."""
        gid = g.genome_id
        cur = self.conn.execute("SELECT 1 FROM genomes WHERE genome_id=?", (gid,))
        if cur.fetchone():
            return False
        self.conn.execute(
            "INSERT INTO genomes(genome_id,market,generator,generation,parents,body,prose,complexity,created_at)"
            " VALUES(?,?,?,?,?,?,?,?,?)",
            (gid, g.meta.market, g.generator, g.generation, json.dumps(g.parents),
             json.dumps(g.body()), g.to_prose(), g.complexity(), time.time()),
        )
        self.conn.commit()
        return True

    def genome_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM genomes").fetchone()[0]

    # ─── Result Ledger (the honest trial count) ──────────────────────────
    def record_eval(self, res: EvalResult) -> int:
        row = res.to_ledger_row()
        cur = self.conn.execute(
            "INSERT INTO result_ledger(genome_id,market,fidelity,seed,snapshot_id,n_periods,"
            "net_sharpe,sharpe_pp,ann_return,max_dd,hit_rate,avg_turnover,error,created_at)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (row["genome_id"], row["market"], row["fidelity"], row["seed"], row["snapshot_id"],
             row["n_periods"], row["net_sharpe"], row.get("sharpe_pp"), row["ann_return"], row["max_dd"],
             row["hit_rate"], row["avg_turnover"], row["error"], time.time()),
        )
        self.conn.commit()
        return cur.lastrowid

    def sr_trial_std(self, market: Optional[str] = None) -> Optional[float]:
        """Std of per-observation Sharpes across trials — the σ_SR that scales the Deflated
        Sharpe deflation (docs/05 §3). None until enough finite trials exist."""
        q = "SELECT sharpe_pp FROM result_ledger WHERE sharpe_pp IS NOT NULL"
        params: tuple = ()
        if market:
            q += " AND market=?"; params = (market,)
        vals = [r[0] for r in self.conn.execute(q, params).fetchall() if r[0] is not None]
        import math
        vals = [v for v in vals if math.isfinite(v)]
        if len(vals) < 8:
            return None
        import statistics
        s = statistics.pstdev(vals)
        return float(s) if s > 0 else None

    def trial_count(self, market: Optional[str] = None) -> int:
        """The Deflated-Sharpe family size N: every eval ever recorded (docs/05 §3)."""
        if market:
            return self.conn.execute("SELECT COUNT(*) FROM result_ledger WHERE market=?", (market,)).fetchone()[0]
        return self.conn.execute("SELECT COUNT(*) FROM result_ledger").fetchone()[0]

    # ─── Gauntlet reports ────────────────────────────────────────────────
    def record_gauntlet(self, genome_id: str, market: str, passed: bool,
                        failed_gate: Optional[str], gates: dict, fitness: dict) -> None:
        self.conn.execute(
            "INSERT INTO gauntlet_reports(genome_id,market,passed,failed_gate,gates,fitness,created_at)"
            " VALUES(?,?,?,?,?,?,?)",
            (genome_id, market, int(passed), failed_gate or "", json.dumps(gates),
             json.dumps(fitness), time.time()),
        )
        self.conn.commit()

    # ─── QD Archive ──────────────────────────────────────────────────────
    def upsert_archive(self, niche_key: str, genome_id: str, market: str,
                       fitness: dict, descriptor: dict, scalar_fit: float) -> str:
        """Occupy an empty niche or replace a less-fit incumbent. Returns the action."""
        cur = self.conn.execute("SELECT scalar_fit FROM archive WHERE niche_key=?", (niche_key,))
        row = cur.fetchone()
        if row is None:
            action = "occupy"
        elif scalar_fit > row["scalar_fit"]:
            action = "replace"
        else:
            return "keep"
        self.conn.execute(
            "INSERT INTO archive(niche_key,genome_id,market,fitness,descriptor,scalar_fit,updated_at)"
            " VALUES(?,?,?,?,?,?,?) ON CONFLICT(niche_key) DO UPDATE SET "
            "genome_id=excluded.genome_id, market=excluded.market, fitness=excluded.fitness, "
            "descriptor=excluded.descriptor, scalar_fit=excluded.scalar_fit, updated_at=excluded.updated_at",
            (niche_key, genome_id, market, json.dumps(fitness), json.dumps(descriptor),
             scalar_fit, time.time()),
        )
        self.conn.commit()
        return action

    def archive_rows(self) -> List[sqlite3.Row]:
        return list(self.conn.execute("SELECT * FROM archive ORDER BY scalar_fit DESC"))

    # ─── Lessons (thin) ──────────────────────────────────────────────────
    def add_lesson(self, text: str, tags: str = "") -> bool:
        """Append a lesson, deduplicated by exact text. Returns True if newly added."""
        if self.conn.execute("SELECT 1 FROM lessons WHERE text=?", (text,)).fetchone():
            return False
        self.conn.execute("INSERT INTO lessons(text,tags,created_at) VALUES(?,?,?)",
                          (text, tags, time.time()))
        self.conn.commit()
        return True

    def lesson_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]

    def recent_lessons(self, limit: int = 8) -> List[str]:
        rows = self.conn.execute("SELECT text FROM lessons ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [r[0] for r in rows]
