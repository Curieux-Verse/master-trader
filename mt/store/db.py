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
    ret_sig      TEXT,
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
CREATE TABLE IF NOT EXISTS screening_ledger (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    n           INTEGER,
    kind        TEXT,
    created_at  REAL
);
CREATE TABLE IF NOT EXISTS attributions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    feature_op  TEXT,
    delta_z     REAL,
    created_at  REAL
);
CREATE TABLE IF NOT EXISTS hall_of_fame (
    genome_id   TEXT PRIMARY KEY,
    market      TEXT,
    dsr_z       REAL,
    scalar_fit  REAL,
    passed      INTEGER,
    fitness     TEXT,
    sharpe_pp   REAL,
    first_seen  REAL,
    updated_at  REAL
);
CREATE INDEX IF NOT EXISTS ix_hof_z ON hall_of_fame(dsr_z);
CREATE INDEX IF NOT EXISTS ix_hof_market_z ON hall_of_fame(market, dsr_z);
CREATE TABLE IF NOT EXISTS bandit_state (
    market      TEXT,
    engine      TEXT,
    alpha       REAL,
    beta        REAL,
    updated_at  REAL,
    PRIMARY KEY (market, engine)
);
CREATE TABLE IF NOT EXISTS champion_track (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    genome_id   TEXT,
    dsr_z       REAL,
    oos_sharpe  REAL,
    oos_dsr_z   REAL,
    runs_held   INTEGER,
    created_at  REAL
);
CREATE INDEX IF NOT EXISTS ix_champion_market ON champion_track(market, created_at);
"""


def _hof_scalarize(fitness: dict) -> float:
    """The Gauntlet's scalarization, replicated here (avoids a store→runner import cycle) so the
    hall-of-fame and the backfill agree with mt.gauntlet.runner._scalarize on a genome's rank."""
    if not fitness:
        return float("-inf")
    ds = fitness.get("deflated_sharpe")
    if ds is None:
        ds = fitness.get("net_sharpe")
    if ds is None:
        ds = 0.0
    base = float(ds)
    omp = fitness.get("one_minus_pbo")
    if omp is not None:
        base *= max(0.0, float(omp))
    return base - 0.05 * abs(float(fitness.get("neg_complexity", 0) or 0))


class MTStore:
    def __init__(self, db_path: Optional[Path] = None):
        self.path = Path(db_path or DB_PATH)
        self.conn = sqlite3.connect(str(self.path), timeout=5)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.executescript(_SCHEMA)
        self._migrate()
        self.conn.commit()

    def _migrate(self) -> None:
        """Additive migrations for brains created before a column existed (the cached marathon
        DB predates ret_sig). Each ALTER is best-effort — a duplicate-column error means done."""
        for table, col, decl in (("result_ledger", "ret_sig", "TEXT"),):
            try:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
            except sqlite3.OperationalError:
                pass

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

    def get_genome(self, genome_id: str):
        row = self.conn.execute("SELECT body FROM genomes WHERE genome_id=?", (genome_id,)).fetchone()
        if not row:
            return None
        from mt.genome.schema import Genome
        return Genome.from_dict(json.loads(row["body"]))

    def genome_sharpe_pp(self, genome_id: str):
        r = self.conn.execute(
            "SELECT sharpe_pp FROM result_ledger WHERE genome_id=? AND sharpe_pp IS NOT NULL "
            "ORDER BY eval_id DESC LIMIT 1", (genome_id,)).fetchone()
        return r[0] if r else None

    # ─── Result Ledger (the honest trial count) ──────────────────────────
    def record_eval(self, res: EvalResult) -> int:
        row = res.to_ledger_row()
        cur = self.conn.execute(
            "INSERT INTO result_ledger(genome_id,market,fidelity,seed,snapshot_id,n_periods,"
            "net_sharpe,sharpe_pp,ann_return,max_dd,hit_rate,avg_turnover,error,ret_sig,created_at)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (row["genome_id"], row["market"], row["fidelity"], row["seed"], row["snapshot_id"],
             row["n_periods"], row["net_sharpe"], row.get("sharpe_pp"), row["ann_return"], row["max_dd"],
             row["hit_rate"], row["avg_turnover"], row["error"], row.get("ret_sig", ""), time.time()),
        )
        self.conn.commit()
        return cur.lastrowid

    def avg_trial_corr(self, market: Optional[str] = None, sample: int = 400) -> Optional[float]:
        """Average pairwise correlation of trial P&L signatures — the equicorrelation ρ̄ used to
        deflate the RAW trial count to an EFFECTIVE independent count. Genomes share features, so
        their trials are correlated; treating N as fully independent over-deflates the Sharpe and
        can manufacture a false 100% rejection (López de Prado, DSR Appendix 3)."""
        q = "SELECT ret_sig FROM result_ledger WHERE ret_sig IS NOT NULL AND ret_sig!=''"
        params: tuple = ()
        if market:
            q += " AND market=?"; params = (market,)
        q += " ORDER BY eval_id DESC LIMIT ?"
        rows = [r[0] for r in self.conn.execute(q, params + (int(sample),)).fetchall()]
        import numpy as np
        sigs = []
        for s in rows:
            try:
                v = np.array([float(x) for x in s.split(",")], dtype=float)
                if v.size >= 8 and np.isfinite(v).all():
                    sigs.append(v)
            except Exception:
                continue
        if len(sigs) < 8:
            return None
        k = min(v.size for v in sigs)
        C = np.corrcoef(np.vstack([v[:k] for v in sigs]))
        iu = np.triu_indices_from(C, k=1)
        rho = float(np.nanmean(C[iu]))                    # signed: positive co-movement reduces independence
        return None if not np.isfinite(rho) else float(min(max(rho, 0.0), 0.99))

    def effective_trial_count(self, market: Optional[str] = None, rho: Optional[float] = None) -> int:
        """Raw trial count deflated to effectively-independent trials via the equicorrelation
        N_eff = N / (1 + (N−1)·ρ̄). Falls back to raw N when ρ̄ is unknown."""
        n = self.trial_count(market)
        if rho is None:
            rho = self.avg_trial_corr(market)
        if not rho or rho <= 0 or n <= 1:
            return n
        return max(1, int(round(n / (1.0 + (n - 1) * rho))))

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

    def record_attribution(self, market: str, feature_op: str, delta_z: float) -> None:
        """Store one leave-one-out ΔDSR-z: how much DROPPING this feature hurt a near-miss genome's
        Deflated Sharpe (positive ⇒ the feature carried signal). Turns 26 families of guesswork into
        measured per-primitive contribution (docs/13 attribution)."""
        import math
        if delta_z is None or not math.isfinite(delta_z):
            return
        self.conn.execute("INSERT INTO attributions(market,feature_op,delta_z,created_at) VALUES(?,?,?,?)",
                          (market, feature_op, float(delta_z), time.time()))
        self.conn.commit()

    def top_feature_attributions(self, market: Optional[str] = None, limit: int = 20) -> List[tuple]:
        """(feature_op, n, mean ΔDSR-z) ranked by mean contribution — which primitives carry signal."""
        q = ("SELECT feature_op, COUNT(*), AVG(delta_z) FROM attributions "
             + ("WHERE market=? " if market else "") + "GROUP BY feature_op "
             "HAVING COUNT(*) >= 2 ORDER BY AVG(delta_z) DESC LIMIT ?")
        params = ((market, limit) if market else (limit,))
        return [(r[0], int(r[1]), float(r[2])) for r in self.conn.execute(q, params).fetchall()]

    def record_screening(self, market: str, n: int, kind: str = "miner_ic") -> None:
        """Charge N *hidden* selection trials (e.g. IC-screened miner candidates that were
        looked at but never separately backtested) to the Deflated-Sharpe family size, so G4 is
        not silently under-deflated for the most overfitting-prone engine (docs/05 §3)."""
        if n and n > 0:
            self.conn.execute("INSERT INTO screening_ledger(market,n,kind,created_at) VALUES(?,?,?,?)",
                              (market, int(n), kind, time.time()))
            self.conn.commit()

    def trial_count(self, market: Optional[str] = None) -> int:
        """The Deflated-Sharpe family size N: every eval ever recorded PLUS hidden screening
        trials (docs/05 §3). Both counts are scoped the same way as the σ_SR dispersion the DSR
        pairs with — per-market when a market is given — so N and σ_SR describe one trial set."""
        if market:
            n_eval = self.conn.execute("SELECT COUNT(*) FROM result_ledger WHERE market=?", (market,)).fetchone()[0]
            n_scr = self.conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger WHERE market=?",
                                      (market,)).fetchone()[0]
        else:
            n_eval = self.conn.execute("SELECT COUNT(*) FROM result_ledger").fetchone()[0]
            n_scr = self.conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger").fetchone()[0]
        return int(n_eval) + int(n_scr)

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

    # ─── Hall of Fame (persistent best-ever memory, independent of the pass bar) ──
    def upsert_hof(self, genome_id: str, market: str, dsr_z: Optional[float], scalar_fit: float,
                   passed: bool, fitness: dict, sharpe_pp: Optional[float] = None) -> str:
        """Retain a genome's BEST-ever Deflated-Sharpe z. Unlike the archive (which admits only
        gauntlet PASSERS and so stays empty until an edge clears), the hall-of-fame keeps the
        search's closest approaches too — so best-z is an ALL-TIME high-water mark that ratchets
        across marathons, and warm-start has elites to breed from. This is a search-memory /
        reporting device; it does NOT relax any gate (tradeable still requires clearing G4)."""
        import math
        if dsr_z is None or not math.isfinite(float(dsr_z)):
            return "skip"
        z = float(dsr_z); now = time.time()
        row = self.conn.execute("SELECT dsr_z FROM hall_of_fame WHERE genome_id=?", (genome_id,)).fetchone()
        if row is None:
            self.conn.execute(
                "INSERT INTO hall_of_fame(genome_id,market,dsr_z,scalar_fit,passed,fitness,sharpe_pp,"
                "first_seen,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
                (genome_id, market, z, float(scalar_fit), int(bool(passed)), json.dumps(fitness),
                 sharpe_pp, now, now))
            self.conn.commit()
            return "occupy"
        if z > (row["dsr_z"] if row["dsr_z"] is not None else float("-inf")):
            self.conn.execute(
                "UPDATE hall_of_fame SET dsr_z=?, scalar_fit=?, passed=?, fitness=?, sharpe_pp=?, "
                "updated_at=? WHERE genome_id=?",
                (z, float(scalar_fit), int(bool(passed)), json.dumps(fitness), sharpe_pp, now, genome_id))
            self.conn.commit()
            return "replace"
        return "keep"

    def best_z_alltime(self, market: Optional[str] = None) -> Optional[float]:
        """The all-time high-water mark of Deflated-Sharpe z — the honest cross-marathon progress
        metric (the per-run z_trend resets each run; this does not)."""
        q = "SELECT MAX(dsr_z) FROM hall_of_fame"
        params: tuple = ()
        if market:
            q += " WHERE market=?"; params = (market,)
        r = self.conn.execute(q, params).fetchone()
        return None if (r is None or r[0] is None) else float(r[0])

    def hof_top(self, market: Optional[str] = None, limit: int = 12) -> List[sqlite3.Row]:
        """Top-K genomes by best-ever dsr_z — the challenger pool and the warm-start seed set."""
        q = "SELECT genome_id, market, dsr_z, scalar_fit, passed, fitness, sharpe_pp FROM hall_of_fame"
        params: tuple = ()
        if market:
            q += " WHERE market=?"; params = (market,)
        q += " ORDER BY dsr_z DESC LIMIT ?"
        return list(self.conn.execute(q, params + (int(limit),)))

    def backfill_hof(self) -> int:
        """One-time seed of the hall-of-fame from historical gauntlet_reports (dsr_z lives in the
        gates JSON, fitness in its own column). Lets an already-accumulated brain surface its
        best-ever genomes immediately, instead of building the HoF only from post-upgrade evals.
        Idempotent: no-ops once the HoF has any row."""
        if self.conn.execute("SELECT 1 FROM hall_of_fame LIMIT 1").fetchone():
            return 0
        n = 0
        cur = self.conn.execute("SELECT genome_id, market, passed, gates, fitness FROM gauntlet_reports")
        for row in cur.fetchall():
            try:
                gates = json.loads(row["gates"]) if row["gates"] else {}
                fit = json.loads(row["fitness"]) if row["fitness"] else {}
            except Exception:
                continue
            z = (gates.get("G4_deflated_sharpe", {}) or {}).get("dsr_z")
            if z is None:
                continue
            self.upsert_hof(row["genome_id"], row["market"], z, _hof_scalarize(fit),
                            bool(row["passed"]), fit, fit.get("net_sharpe"))
            n += 1
        return n

    # ─── Engine bandit state (so the meta-controller compounds across marathons) ──
    def save_bandit(self, market: str, alpha: dict, beta: dict) -> None:
        now = time.time()
        for e in alpha:
            self.conn.execute(
                "INSERT INTO bandit_state(market,engine,alpha,beta,updated_at) VALUES(?,?,?,?,?) "
                "ON CONFLICT(market,engine) DO UPDATE SET alpha=excluded.alpha, beta=excluded.beta, "
                "updated_at=excluded.updated_at",
                (market, e, float(alpha[e]), float(beta.get(e, 1.0)), now))
        self.conn.commit()

    def load_bandit(self, market: str) -> Optional[dict]:
        rows = self.conn.execute(
            "SELECT engine, alpha, beta FROM bandit_state WHERE market=?", (market,)).fetchall()
        if not rows:
            return None
        return {r["engine"]: (float(r["alpha"]), float(r["beta"])) for r in rows}

    # ─── Champion / challenger track (OOS certification over weeks; NOT the trial ledger) ──
    def record_champion(self, market: str, genome_id: str, dsr_z: Optional[float],
                        oos_sharpe: Optional[float], oos_dsr_z: Optional[float], runs_held: int) -> None:
        self.conn.execute(
            "INSERT INTO champion_track(market,genome_id,dsr_z,oos_sharpe,oos_dsr_z,runs_held,created_at)"
            " VALUES(?,?,?,?,?,?,?)",
            (market, genome_id, dsr_z, oos_sharpe, oos_dsr_z, int(runs_held), time.time()))
        self.conn.commit()

    def champion_reign(self, market: str, genome_id: str) -> int:
        """How many consecutive digests this genome has been the standing champion (its reign)."""
        rows = self.conn.execute(
            "SELECT genome_id FROM champion_track WHERE market=? ORDER BY created_at DESC LIMIT 200",
            (market,)).fetchall()
        reign = 0
        for r in rows:
            if r["genome_id"] == genome_id:
                reign += 1
            else:
                break
        return reign

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
