"""mt.store — the system's durable memory (SQLite, WAL), separate from smc_signals.db.

Four registries make results honest and reproducible (docs/01 §5):
  • Genome Registry  — every genome ever seen, content-hashed, deduplicated, with lineage.
  • Result Ledger    — every evaluation of every genome; this is what the Deflated Sharpe
                       trial count literally counts (docs/05 §3). Under-count N and you fool
                       yourself; the ledger exists so you cannot.
  • QD Archive       — the current elite map (best genome per behavioral niche).
  • Lesson Library   — the critic's accumulating, human-readable wisdom (thin for now).
"""
from mt.store.db import MTStore

__all__ = ["MTStore"]
