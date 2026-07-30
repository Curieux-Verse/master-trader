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
-- Denormalized per-(genome, family-tag) facts. This is the CYCLE-LEVEL tier of the research
-- memory: it is what lets "which families keep dying at which gate" be a cheap GROUP BY instead
-- of a re-parse of every genome body. Written once per gauntlet verdict (docs/15 §3).
CREATE TABLE IF NOT EXISTS trial_facts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    genome_id   TEXT,
    market      TEXT,
    tag         TEXT,
    phenotype   TEXT,
    regime      TEXT,
    sizing      TEXT,
    gate        TEXT,
    promoted    INTEGER,
    dsr_z       REAL,
    edge_t      REAL,
    created_at  REAL
);
CREATE INDEX IF NOT EXISTS ix_facts_market_tag ON trial_facts(market, tag);
CREATE INDEX IF NOT EXISTS ix_facts_gate ON trial_facts(market, gate);
-- The miner MINTS new primitives at run time (intx_*). Without persistence the vocabulary dies
-- with the process, and every hall-of-fame genome built on a minted op fails `typecheck` on the
-- next marathon and is silently dropped from warm-start — i.e. the deepest part of the search
-- was being forgotten every run. Store the recipe (the two component ops + their args) so the
-- op can be rebuilt and registered at startup (docs/15 §3.4).
CREATE TABLE IF NOT EXISTS minted_ops (
    name        TEXT PRIMARY KEY,
    market      TEXT,
    recipe      TEXT,
    ic          REAL,
    created_at  REAL
);
-- Stage-A → Stage-B boundary. A finalist list is content-hashed and timestamped BEFORE the
-- holdout is touched; Stage B may only ever confirm a list that already exists here. This is the
-- artifact that makes "we did not redraw the finalists after peeking" checkable (docs/15 §4).
-- Monotonic all-time counters. The Deflated-Sharpe family size N must survive retention: if it
-- were recomputed from surviving ledger rows, pruning would lower the significance bar for every
-- future candidate — manufacturing significance by forgetting trials that were already paid for.
CREATE TABLE IF NOT EXISTS counters (
    k TEXT PRIMARY KEY,
    v INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS preregistration (
    prereg_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    list_hash   TEXT,
    genome_ids  TEXT,
    family_size INTEGER,
    n_eff       INTEGER,
    method      TEXT,
    created_at  REAL,
    confirmed_at REAL
);
CREATE INDEX IF NOT EXISTS ix_prereg_market ON preregistration(market, created_at);
-- Every read of the sealed holdout, counted. An unbudgeted holdout stops being out-of-sample:
-- the last production run evaluated G6 transfer on all 23,030 genomes, which silently turned the
-- "unseen" panel into a selection surface (docs/15 §4).
CREATE TABLE IF NOT EXISTS holdout_ledger (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    genome_id   TEXT,
    purpose     TEXT,
    prereg_id   INTEGER,
    created_at  REAL
);
CREATE INDEX IF NOT EXISTS ix_holdout_market ON holdout_ledger(market);
-- Book (portfolio) certification track: the combination of decorrelated candidates, which is the
-- object that can realistically clear significance when no single genome does (docs/15 §5).
CREATE TABLE IF NOT EXISTS book_track (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    market      TEXT,
    members     TEXT,
    n_members   INTEGER,
    book_sharpe REAL,
    book_dsr_z  REAL,
    oos_sharpe  REAL,
    oos_dsr_z   REAL,
    created_at  REAL
);
CREATE INDEX IF NOT EXISTS ix_book_market ON book_track(market, created_at);
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
    """Rank a genome exactly as the gauntlet does. Delegates to the ONE implementation in
    mt.gauntlet.runner (imported lazily to avoid a store→runner cycle at module load) — the two
    used to be hand-copied, which is a silent-drift hazard now that the scalarization carries a
    similarity discount."""
    if not fitness:
        return float("-inf")
    from mt.gauntlet.runner import scalarize
    return scalarize(fitness)


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
        for table, col, decl in (("result_ledger", "ret_sig", "TEXT"),
                                 ("archive", "promoted", "INTEGER DEFAULT 0"),
                                 ("archive", "cleared", "INTEGER DEFAULT 0"),
                                 ("hall_of_fame", "curiosity", "REAL DEFAULT 0"),
                                 ("hall_of_fame", "edge_t", "REAL")):
            try:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
            except sqlite3.OperationalError:
                pass
        # Dedup index on the ledger identity. A trial is a distinct HYPOTHESIS; re-evaluating the
        # same genome on the same data with the same seed is deterministic and returns a
        # bit-identical result, so charging it again inflates the family size for zero information
        # (measured: 25% of the production ledger). Created as a plain index, not UNIQUE, so an
        # already-accumulated brain with historical duplicates still opens (docs/15 §1).
        try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS ix_ledger_identity "
                              "ON result_ledger(genome_id, seed, snapshot_id)")
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
    def find_eval(self, genome_id: str, seed: int, snapshot_id: str):
        """The existing ledger row for this exact (genome, seed, snapshot), if any."""
        return self.conn.execute(
            "SELECT eval_id, sharpe_pp, n_periods FROM result_ledger "
            "WHERE genome_id=? AND seed=? AND snapshot_id=? ORDER BY eval_id DESC LIMIT 1",
            (genome_id, int(seed), snapshot_id or "")).fetchone()

    def record_eval(self, res: EvalResult, dedup: bool = True) -> tuple:
        """Append a trial to the ledger. Returns (eval_id, is_new_trial).

        `dedup=True` refuses to charge a SECOND trial for an identical (genome_id, seed,
        snapshot_id): that combination is deterministic, so the re-run yields the same numbers and
        represents no new hypothesis. The Deflated Sharpe deflates for the number of *distinct
        things tried*; counting a repeat raises the significance bar for every other candidate in
        exchange for nothing. The codebase already asserts this principle for warm-start parents
        and champion re-validation — this makes the main loop obey it too (docs/15 §1)."""
        if dedup:
            prior = self.find_eval(res.genome_id, res.seed, res.snapshot_id)
            if prior is not None:
                return int(prior["eval_id"]), False
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
        self.bump_trials(res.market, 1)          # all-time N, immune to retention
        return cur.lastrowid, True

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

    def last_n_periods(self, genome_id: str) -> Optional[int]:
        """Observations this genome produced on the SEARCH panel, from its most recent trial.

        Used to predict how many it will produce on the holdout before that panel is touched:
        observation counts scale with panel length, so the ratio is knowable in advance and a
        genome that cannot reach MIN_PERIODS there must not be pre-registered (docs/15 §4)."""
        row = self.conn.execute(
            "SELECT n_periods FROM result_ledger WHERE genome_id=? AND n_periods IS NOT NULL "
            "ORDER BY eval_id DESC LIMIT 1", (genome_id,)).fetchone()
        return int(row[0]) if row and row[0] is not None else None

    def trial_signatures(self, market: Optional[str] = None, sample: int = 400,
                         genome_ids: Optional[List[str]] = None) -> List:
        """The most recent parsed P&L-path signatures — raw material for K_eff.

        `genome_ids` restricts the sample to a named set. Stage B needs this: the confirmatory
        family must be deflated by how correlated the FINALISTS are with each other, not by how
        correlated the market's general trial population is (docs/15 §4)."""
        q = "SELECT ret_sig FROM result_ledger WHERE ret_sig IS NOT NULL AND ret_sig!=''"
        params: tuple = ()
        if market:
            q += " AND market=?"; params = (market,)
        if genome_ids:
            ids = list(dict.fromkeys(genome_ids))       # de-dup, order-stable
            q += " AND genome_id IN (%s)" % ",".join("?" * len(ids))
            params = params + tuple(ids)
        q += " ORDER BY eval_id DESC LIMIT ?"
        import numpy as np
        out = []
        for (s,) in self.conn.execute(q, params + (int(sample),)).fetchall():
            try:
                v = np.array([float(x) for x in s.split(",")], dtype=float)
            except Exception:
                continue
            if v.size >= 8 and np.isfinite(v).all() and v.std() > 0:
                out.append(v)
        return out

    def effective_trials(self, market: Optional[str] = None, rho: Optional[float] = None) -> dict:
        """Full K_eff report: {n_eff, method, ...}. Primary estimator is the extreme-value
        inversion over the measured trial-correlation matrix (mt.gauntlet.multipletest), which —
        unlike the equicorrelation formula it replaces — actually collapses when the search starts
        producing near-clones. Equicorrelation remains the fallback for a cold ledger."""
        from mt.gauntlet.multipletest import effective_trials as _eff
        n = self.trial_count(market)
        if rho is None:
            rho = self.avg_trial_corr(market)
        return _eff(n, self.trial_signatures(market), rho=rho)

    def effective_trial_count(self, market: Optional[str] = None, rho: Optional[float] = None) -> int:
        """Raw trial count deflated to effectively-independent trials (K_eff). Scalar convenience
        wrapper over `effective_trials`."""
        return int(self.effective_trials(market, rho)["n_eff"])

    def recent_pvalues(self, market: Optional[str] = None, sample: int = 500) -> List[float]:
        """One-sided single-strategy p-values (SR·√T) for the most recent trials.

        These carry NO multiple-testing penalty by construction, which is the point: the Stage-A
        FDR threshold has to be computed from a distribution that does not itself move as the
        ledger grows, or the screen would drift exactly like the bar it replaces."""
        from mt.gauntlet.multipletest import sharpe_pvalue
        q = ("SELECT sharpe_pp, n_periods FROM result_ledger WHERE sharpe_pp IS NOT NULL"
             + (" AND market=?" if market else "") + " ORDER BY eval_id DESC LIMIT ?")
        params = ((market, int(sample)) if market else (int(sample),))
        out = []
        for spp, npd in self.conn.execute(q, params).fetchall():
            p = sharpe_pvalue(spp, npd)
            if p is not None:
                out.append(p)
        return out

    def sr_trial_std(self, market: Optional[str] = None) -> Optional[float]:
        """ROBUST dispersion of per-observation Sharpes across trials — the σ_SR that scales the
        entire Deflated-Sharpe deflation (docs/05 §3). None until enough finite trials exist.

        This must be robust, because the ledger is written BEFORE the gauntlet runs: a genome whose
        returns are near-constant has a float-noise standard deviation and therefore an absurd
        per-bar Sharpe, and G1 rejects it only AFTER `record_eval` has already stored it. The real
        production brain shows exactly that — `sharpe_pp` ranging to 38,026 (and −421), with 10% of
        all trials above |10|, a value that is physically impossible for a per-observation Sharpe.

        The plain standard deviation over that ledger is 2,497.5 versus 0.2253 for the sane 82%.
        Since the deflation term is σ_SR·E[max of N], a contaminated σ makes E[max SR] ≈ 10,000
        Sharpe units and drives EVERY candidate's z to minus infinity — nothing can ever clear the
        bar, for reasons that have nothing to do with the strategies.

        Fixed two ways: drop values the gates already consider numerically degenerate, then use a
        median-absolute-deviation estimator (×1.4826 for normal consistency) so that any remaining
        outlier cannot move the scale. Falls back to the plain std only if the MAD degenerates."""
        from mt.adapters.cclib import MAX_SANE_SR_PP
        q = "SELECT sharpe_pp FROM result_ledger WHERE sharpe_pp IS NOT NULL"
        params: tuple = ()
        if market:
            q += " AND market=?"; params = (market,)
        vals = [r[0] for r in self.conn.execute(q, params).fetchall() if r[0] is not None]
        import math
        import statistics
        vals = [v for v in vals if math.isfinite(v) and abs(v) <= MAX_SANE_SR_PP]
        if len(vals) < 8:
            return None
        med = statistics.median(vals)
        mad = statistics.median([abs(v - med) for v in vals])
        s = 1.4826 * mad
        if not (s > 0 and math.isfinite(s)):
            s = statistics.pstdev(vals)
        return float(s) if s > 0 and math.isfinite(s) else None

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

    # ─── Research memory: cycle-level facts and archetype-level cues (docs/15 §3) ──
    def record_trial_facts(self, genome_id: str, market: str, tags: List[str], phenotype: str,
                           regime: str, sizing: str, gate: Optional[str], promoted: bool,
                           dsr_z: Optional[float], edge_t: Optional[float]) -> None:
        """One row per (genome, family tag) — the substrate the archetype cues are computed from.

        This exists because the old lesson library stored PROSE. Prose cannot be aggregated: 1,123
        stored lessons contained exactly 3 distinct prescriptions and no numbers, so nothing could
        ever consume them. Facts can be grouped, ranked, and turned into a sampling prior."""
        now = time.time()
        rows = [(genome_id, market, t, phenotype, regime, sizing, gate or "", int(bool(promoted)),
                 dsr_z, edge_t, now) for t in (tags or ["mixed"])]
        self.conn.executemany(
            "INSERT INTO trial_facts(genome_id,market,tag,phenotype,regime,sizing,gate,promoted,"
            "dsr_z,edge_t,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", rows)
        self.conn.commit()

    def family_priors(self, market: Optional[str] = None, min_n: int = 12) -> List[tuple]:
        """(tag, n, promote_rate, mean_edge_t) per strategy family — the ARCHETYPE-LEVEL cue.

        Ranked by mean edge-t, which is N-INDEPENDENT: it measures whether the family produces raw
        predictive strength, not whether it survived a bar that moves as the ledger grows. That is
        what makes this prior stable enough to steer generation over weeks."""
        q = ("SELECT tag, COUNT(*), AVG(promoted), AVG(edge_t) FROM trial_facts "
             "WHERE edge_t IS NOT NULL" + (" AND market=?" if market else "") +
             " GROUP BY tag HAVING COUNT(*) >= ? ORDER BY AVG(edge_t) DESC")
        params = ((market, int(min_n)) if market else (int(min_n),))
        return [(r[0], int(r[1]), float(r[2] or 0.0), float(r[3] or 0.0))
                for r in self.conn.execute(q, params).fetchall()]

    def gate_profile(self, market: Optional[str] = None) -> List[tuple]:
        """(tag, gate, n) — which families die at which gate. The critic's evidence pack."""
        q = ("SELECT tag, gate, COUNT(*) FROM trial_facts WHERE gate != ''"
             + (" AND market=?" if market else "") + " GROUP BY tag, gate ORDER BY COUNT(*) DESC")
        params = ((market,) if market else ())
        return [(r[0], r[1], int(r[2])) for r in self.conn.execute(q, params).fetchall()]

    def feature_op_weights(self, market: Optional[str] = None, floor: float = 0.25,
                           temperature: float = 1.0) -> dict:
        """{feature_op: relative sampling weight} from MEASURED leave-one-out ΔDSR-z.

        This is the wire that was missing: attribution was computed, stored, rendered in a markdown
        report, and then ignored by every generator, which kept sampling primitives uniformly. A
        softmax over mean Δz (floored, so nothing is ever fully starved and the search cannot
        collapse onto last week's winner) turns that measurement into search direction."""
        rows = self.top_feature_attributions(market, limit=500)
        if not rows:
            return {}
        import math as _m
        vals = {op: dz for op, _n, dz in rows}
        mx = max(vals.values())
        raw = {op: _m.exp((dz - mx) / max(1e-6, temperature)) for op, dz in vals.items()}
        tot = sum(raw.values()) or 1.0
        n = len(raw)
        # blend toward uniform by `floor` so measured evidence tilts the search without owning it
        return {op: (1.0 - floor) * (w / tot) + floor * (1.0 / n) for op, w in raw.items()}

    # ─── Minted vocabulary (so the miner's primitives survive a restart) ──
    def save_minted_op(self, name: str, market: str, recipe: dict, ic: float) -> None:
        self.conn.execute(
            "INSERT INTO minted_ops(name,market,recipe,ic,created_at) VALUES(?,?,?,?,?) "
            "ON CONFLICT(name) DO NOTHING",
            (name, market, json.dumps(recipe), float(ic), time.time()))
        self.conn.commit()

    def minted_ops(self) -> List[tuple]:
        return [(r["name"], json.loads(r["recipe"]), r["ic"])
                for r in self.conn.execute("SELECT name, recipe, ic FROM minted_ops")]

    # ─── Holdout budget + pre-registration (docs/15 §4) ──
    def record_holdout_access(self, market: str, genome_id: str, purpose: str,
                              prereg_id: Optional[int] = None) -> None:
        self.conn.execute(
            "INSERT INTO holdout_ledger(market,genome_id,purpose,prereg_id,created_at)"
            " VALUES(?,?,?,?,?)", (market, genome_id, purpose, prereg_id, time.time()))
        self.conn.commit()

    def holdout_access_count(self, market: Optional[str] = None,
                             purpose: Optional[str] = None) -> int:
        q = "SELECT COUNT(*) FROM holdout_ledger"
        where, args = [], []
        if market:
            where.append("market=?"); args.append(market)
        if purpose:
            where.append("purpose=?"); args.append(purpose)
        if where:
            q += " WHERE " + " AND ".join(where)
        return int(self.conn.execute(q, tuple(args)).fetchone()[0])

    def holdout_access_breakdown(self, market: Optional[str] = None) -> dict:
        """Accesses split BY PURPOSE.

        A single total is no longer interpretable now that G10 calibrates its bar on the sealed
        panel: 40 of those reads are random genomes that are never promoted and can create no
        selection bias, and lumping them in with candidate reads would make the budget line look
        alarming for the one kind of access that is actually harmless. Both still get counted —
        the discipline is that every read is recorded, not that some reads are exempt."""
        q = "SELECT COALESCE(purpose,'?') p, COUNT(*) n FROM holdout_ledger"
        args: tuple = ()
        if market:
            q += " WHERE market=?"; args = (market,)
        q += " GROUP BY p ORDER BY n DESC"
        return {r[0]: int(r[1]) for r in self.conn.execute(q, args)}

    def preregister(self, market: str, genome_ids: List[str], n_eff: int, method: str) -> tuple:
        """Seal a Stage-B finalist list BEFORE the holdout is read. Returns (prereg_id, hash).

        The hash is over the sorted genome ids, so the list that gets confirmed is provably the
        list that was written down. Without this artifact a two-stage protocol is just p-hacking
        with extra steps — the finalists could be redrawn after a disappointing holdout."""
        import hashlib
        ids = sorted(set(genome_ids))
        h = hashlib.sha256("|".join(ids).encode()).hexdigest()[:16]
        cur = self.conn.execute(
            "INSERT INTO preregistration(market,list_hash,genome_ids,family_size,n_eff,method,"
            "created_at,confirmed_at) VALUES(?,?,?,?,?,?,?,NULL)",
            (market, h, json.dumps(ids), len(ids), int(n_eff), method, time.time()))
        self.conn.commit()
        return int(cur.lastrowid), h

    def mark_confirmed(self, prereg_id: int) -> None:
        self.conn.execute("UPDATE preregistration SET confirmed_at=? WHERE prereg_id=?",
                          (time.time(), int(prereg_id)))
        self.conn.commit()

    def prereg_count(self, market: Optional[str] = None) -> int:
        q = "SELECT COUNT(*) FROM preregistration" + (" WHERE market=?" if market else "")
        return int(self.conn.execute(q, ((market,) if market else ())).fetchone()[0])

    def record_book(self, market: str, members: List[str], book_sharpe, book_dsr_z,
                    oos_sharpe, oos_dsr_z) -> None:
        self.conn.execute(
            "INSERT INTO book_track(market,members,n_members,book_sharpe,book_dsr_z,oos_sharpe,"
            "oos_dsr_z,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (market, json.dumps(list(members)), len(members), book_sharpe, book_dsr_z,
             oos_sharpe, oos_dsr_z, time.time()))
        self.conn.commit()

    def best_book(self, market: Optional[str] = None):
        q = "SELECT * FROM book_track" + (" WHERE market=?" if market else "")
        q += " ORDER BY book_dsr_z DESC LIMIT 1"
        return self.conn.execute(q, ((market,) if market else ())).fetchone()

    def record_screening(self, market: str, n: int, kind: str = "miner_ic") -> None:
        """Charge N *hidden* selection trials (e.g. IC-screened miner candidates that were
        looked at but never separately backtested) to the Deflated-Sharpe family size, so G4 is
        not silently under-deflated for the most overfitting-prone engine (docs/05 §3)."""
        if n and n > 0:
            self.conn.execute("INSERT INTO screening_ledger(market,n,kind,created_at) VALUES(?,?,?,?)",
                              (market, int(n), kind, time.time()))
            self.conn.commit()
            self.bump_trials(market, int(n))      # all-time N, immune to retention

    def trial_count(self, market: Optional[str] = None) -> int:
        """The Deflated-Sharpe family size N: every eval ever recorded PLUS hidden screening
        trials (docs/05 §3). Both counts are scoped the same way as the σ_SR dispersion the DSR
        pairs with — per-market when a market is given — so N and σ_SR describe one trial set.

        N is the MONOTONIC counter, never a live COUNT(*) alone. Retention prunes old ledger rows
        to keep the brain a workable size, and if N were derived from surviving rows then pruning
        would silently shrink the family and lower the significance bar for every future candidate
        — buying "significance" by forgetting the trials that were paid for. `trial_counter` holds
        the all-time total; the row count is only a floor for a brain written before it existed."""
        key = f"trials:{market}" if market else "trials:*"
        row = self.conn.execute("SELECT v FROM counters WHERE k=?", (key,)).fetchone()
        counted = int(row["v"]) if row else 0
        if market:
            n_eval = self.conn.execute("SELECT COUNT(*) FROM result_ledger WHERE market=?", (market,)).fetchone()[0]
            n_scr = self.conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger WHERE market=?",
                                      (market,)).fetchone()[0]
        else:
            n_eval = self.conn.execute("SELECT COUNT(*) FROM result_ledger").fetchone()[0]
            n_scr = self.conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger").fetchone()[0]
        return max(counted, int(n_eval) + int(n_scr))

    def bump_trials(self, market: Optional[str], n: int = 1) -> None:
        """Advance the monotonic trial counter (all-time N), per market and globally."""
        if n <= 0:
            return
        for key in ({f"trials:{market}", "trials:*"} if market else {"trials:*"}):
            self.conn.execute(
                "INSERT INTO counters(k,v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=v+?",
                (key, int(n), int(n)))
        self.conn.commit()

    def backfill_counters(self) -> None:
        """One-time: seed the monotonic counters from the rows an existing brain already holds, so
        migrating a pre-retention database cannot momentarily drop N."""
        if self.conn.execute("SELECT 1 FROM counters WHERE k='trials:*'").fetchone():
            return
        markets = [r[0] for r in self.conn.execute("SELECT DISTINCT market FROM result_ledger")]
        total = 0
        for m in markets:
            n = self.conn.execute("SELECT COUNT(*) FROM result_ledger WHERE market=?", (m,)).fetchone()[0]
            s = self.conn.execute("SELECT COALESCE(SUM(n),0) FROM screening_ledger WHERE market=?",
                                  (m,)).fetchone()[0]
            self.conn.execute("INSERT OR REPLACE INTO counters(k,v) VALUES(?,?)",
                              (f"trials:{m}", int(n) + int(s)))
            total += int(n) + int(s)
        self.conn.execute("INSERT OR REPLACE INTO counters(k,v) VALUES('trials:*',?)", (int(total),))
        self.conn.commit()

    # ─── retention: keep the brain a workable size ───────────────────────
    def prune(self, keep_reports: int = 40000, keep_hof: int = 3000,
              keep_ledger: int = 120000) -> dict:
        """Bound the three tables that dominate the file, WITHOUT losing anything load-bearing.

        Measured on the 2026-07-28 production brain (528 MB raw, growing ~30 MB compressed per
        marathon): gauntlet_reports 248k rows ≈158 MB, genomes 158k ≈145 MB, result_ledger 238k
        ≈62 MB, hall_of_fame 92,879 rows ≈36 MB. `gauntlet_reports` is read only for COUNT(*) and
        a one-time hall-of-fame backfill, and `hall_of_fame` had no cap at all — it was a copy of
        every promoted genome rather than a hall of fame.

        Anything referenced by the archive, a champion, a book, a pre-registration or the retained
        hall-of-fame is kept in full: those are the objects warm-start, G8 and Stage B read back."""
        protected = set()
        for q in ("SELECT genome_id FROM archive",
                  "SELECT genome_id FROM champion_track",
                  "SELECT genome_id FROM holdout_ledger"):
            try:
                protected.update(r[0] for r in self.conn.execute(q))
            except Exception:
                pass
        try:
            for (members,) in self.conn.execute("SELECT members FROM book_track"):
                protected.update(json.loads(members or "[]"))
        except Exception:
            pass
        before = self._page_bytes()

        # hall of fame: keep the best of each ordering the selectors actually use
        for col in ("dsr_z", "curiosity", "edge_t"):
            for (m,) in self.conn.execute("SELECT DISTINCT market FROM hall_of_fame"):
                protected.update(r[0] for r in self.conn.execute(
                    f"SELECT genome_id FROM hall_of_fame WHERE market=? "
                    f"ORDER BY COALESCE({col},-1e18) DESC LIMIT ?", (m, keep_hof)))
        ph = ",".join("?" * len(protected)) if protected else "''"
        args = tuple(protected)
        n_hof = self.conn.execute(
            f"DELETE FROM hall_of_fame WHERE genome_id NOT IN ({ph})", args).rowcount
        n_rep = self.conn.execute(
            f"DELETE FROM gauntlet_reports WHERE genome_id NOT IN ({ph}) AND report_id NOT IN "
            f"(SELECT report_id FROM gauntlet_reports ORDER BY report_id DESC LIMIT ?)",
            args + (keep_reports,)).rowcount
        n_led = self.conn.execute(
            f"DELETE FROM result_ledger WHERE genome_id NOT IN ({ph}) AND eval_id NOT IN "
            f"(SELECT eval_id FROM result_ledger ORDER BY eval_id DESC LIMIT ?)",
            args + (keep_ledger,)).rowcount
        n_gen = self.conn.execute(
            f"DELETE FROM genomes WHERE genome_id NOT IN ({ph}) AND genome_id NOT IN "
            f"(SELECT genome_id FROM result_ledger)", args).rowcount
        self.conn.commit()
        self.conn.execute("VACUUM")
        return {"hall_of_fame": n_hof, "gauntlet_reports": n_rep, "result_ledger": n_led,
                "genomes": n_gen, "bytes_before": before, "bytes_after": self._page_bytes()}

    def _page_bytes(self) -> int:
        try:
            pc = self.conn.execute("PRAGMA page_count").fetchone()[0]
            ps = self.conn.execute("PRAGMA page_size").fetchone()[0]
            return int(pc) * int(ps)
        except Exception:
            return 0

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
                       fitness: dict, descriptor: dict, scalar_fit: float,
                       promoted: bool = False, cleared: bool = False) -> str:
        """Occupy an empty niche or replace a less-fit incumbent. Returns the action.

        `cleared` records whether this elite ever cleared the full confirmatory gauntlet — kept as
        a FLAG rather than an admission condition. Canonical MAP-Elites admits the best solution
        per behavioural cell with no global quality bar; requiring a gauntlet pass (as this did)
        left the archive permanently empty, which in turn disabled every mechanism keyed on it:
        no elites to breed from, no reference series for the G8 orthogonality gate, no novelty
        targets. The bar still governs what is TRADEABLE — it just no longer governs what the
        search is allowed to remember (docs/15 §2)."""
        cur = self.conn.execute("SELECT scalar_fit FROM archive WHERE niche_key=?", (niche_key,))
        row = cur.fetchone()
        if row is None:
            action = "occupy"
        elif scalar_fit > row["scalar_fit"]:
            action = "replace"
        else:
            return "keep"
        self.conn.execute(
            "INSERT INTO archive(niche_key,genome_id,market,fitness,descriptor,scalar_fit,"
            "promoted,cleared,updated_at) VALUES(?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(niche_key) DO UPDATE SET "
            "genome_id=excluded.genome_id, market=excluded.market, fitness=excluded.fitness, "
            "descriptor=excluded.descriptor, scalar_fit=excluded.scalar_fit, "
            "promoted=excluded.promoted, cleared=excluded.cleared, updated_at=excluded.updated_at",
            (niche_key, genome_id, market, json.dumps(fitness), json.dumps(descriptor),
             scalar_fit, int(bool(promoted)), int(bool(cleared)), time.time()),
        )
        self.conn.commit()
        return action

    def archive_rows(self, market: Optional[str] = None, cleared_only: bool = False) -> List[sqlite3.Row]:
        q = "SELECT * FROM archive"
        where, params = [], []
        if market:
            where.append("market=?"); params.append(market)
        if cleared_only:
            where.append("cleared=1")
        if where:
            q += " WHERE " + " AND ".join(where)
        return list(self.conn.execute(q + " ORDER BY scalar_fit DESC", tuple(params)))

    def qd_score(self, market: Optional[str] = None) -> float:
        """Σ fitness over occupied niches — the quality-DIVERSITY progress metric.

        best-z alone is a single-point statistic: it can sit still while the search quietly
        collapses onto clones of one idea (measured: the production top-20 were near-duplicates of
        one obv×vwap_distance strategy). QD-score only rises by filling a NEW behavioural cell or
        improving an existing one, so it is the number that actually detects mode collapse.

        Contributions are floored at zero. Summing SIGNED fitness would let a negative-fitness
        niche cancel a positive one (observed: +0.116 and −0.116 reported as a QD-score of +0.00
        for a two-niche archive), which breaks the one property the metric must have — filling a
        cell can never make the score go down."""
        rows = self.archive_rows(market)
        import math
        return float(sum(max(0.0, r["scalar_fit"]) for r in rows
                         if r["scalar_fit"] is not None and math.isfinite(r["scalar_fit"])))

    # ─── Hall of Fame (persistent best-ever memory, independent of the pass bar) ──
    def bump_curiosity(self, genome_id: str, delta: float) -> None:
        """Reward/penalise a parent for what its offspring did (Monte Carlo Elites).

        +1 when a child lands in the archive, −0.5 when it does not. Parent selection then favours
        genomes that have historically been productive STEPPING STONES rather than genomes that
        merely score well — which is the documented fix for a search that improves the population
        mean while never extending the tail, exactly the pathology measured here (best dsr_z at
        lineage depth 0 was never beaten at depth ≥2)."""
        self.conn.execute("UPDATE hall_of_fame SET curiosity = COALESCE(curiosity,0) + ? "
                          "WHERE genome_id=?", (float(delta), genome_id))
        self.conn.commit()

    def upsert_hof(self, genome_id: str, market: str, dsr_z: Optional[float], scalar_fit: float,
                   passed: bool, fitness: dict, sharpe_pp: Optional[float] = None,
                   edge_t: Optional[float] = None) -> str:
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
                "edge_t,curiosity,first_seen,updated_at) VALUES(?,?,?,?,?,?,?,?,0,?,?)",
                (genome_id, market, z, float(scalar_fit), int(bool(passed)), json.dumps(fitness),
                 sharpe_pp, edge_t, now, now))
            self.conn.commit()
            return "occupy"
        if z > (row["dsr_z"] if row["dsr_z"] is not None else float("-inf")):
            self.conn.execute(
                "UPDATE hall_of_fame SET dsr_z=?, scalar_fit=?, passed=?, fitness=?, sharpe_pp=?, "
                "edge_t=?, updated_at=? WHERE genome_id=?",
                (z, float(scalar_fit), int(bool(passed)), json.dumps(fitness), sharpe_pp,
                 edge_t, now, genome_id))
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

    def hof_top(self, market: Optional[str] = None, limit: int = 12,
                order: str = "z") -> List[sqlite3.Row]:
        """Top-K hall-of-fame rows. `order`: 'z' (best-ever Deflated-Sharpe z — the challenger
        pool), 'curiosity' (most productive stepping stones — the warm-start pool), or 'edge_t'
        (raw N-independent predictive strength).

        NOTE the caller is expected to apply a STRUCTURAL diversity filter on top of this for
        warm-start: ordering by z alone returned 12 near-identical genomes in production, so the
        'compounding' mechanism was reseeding each marathon with 12 copies of one idea."""
        col = {"z": "dsr_z", "curiosity": "COALESCE(curiosity,0)", "edge_t": "edge_t"}.get(order, "dsr_z")
        q = ("SELECT genome_id, market, dsr_z, scalar_fit, passed, fitness, sharpe_pp, "
             "COALESCE(curiosity,0) AS curiosity, edge_t FROM hall_of_fame")
        params: tuple = ()
        if market:
            q += " WHERE market=?"; params = (market,)
        q += f" ORDER BY {col} DESC LIMIT ?"
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
