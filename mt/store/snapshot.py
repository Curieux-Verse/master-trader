"""mt.store.snapshot — durable, integrity-checked snapshots of the accumulating brain (docs/14).

The brain (var/mt.db) — QD archive, hall-of-fame, lessons, ledger, bandit, minted vocabulary —
lives in the GitHub Actions cache, which GitHub EVICTS after 7 days of no access (and LRU past
~10 GB). Running every 8h keeps it warm, but a pause longer than a week would silently wipe weeks
of compounding: an UNINTENDED fresh start (see [[mt-brain-compounding]]). Now that the hall-of-fame
makes the brain the crown jewels, that risk is unacceptable.

This module is the belt-and-suspenders layer: a compressed, integrity-checked snapshot the marathon
commits to a long-lived `state` branch (and/or uploads as a 90-day artifact), and restores from on a
cache miss. It uses SQLite's Online Backup API, so the copy is consistent even if taken mid-write
(WAL journal). No capital is touched — only bytes.

    python -m mt.store.snapshot save     [--db var/mt.db] [--out var/mt.db.gz]
    python -m mt.store.snapshot restore  [--in var/mt.db.gz] [--db var/mt.db]   # only if integrity ok
"""
from __future__ import annotations

import argparse
import gzip
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path
from typing import Optional

from mt.config import DB_PATH, VAR_DIR

DEFAULT_SNAPSHOT = VAR_DIR / "mt.db.gz"


def save_snapshot(db_path=DB_PATH, dest_gz=DEFAULT_SNAPSHOT) -> Optional[str]:
    """Consistent, gzipped snapshot of the DB via the SQLite Online Backup API. Returns the path,
    or None if the source DB doesn't exist yet (nothing to snapshot)."""
    db_path = Path(db_path); dest_gz = Path(dest_gz)
    if not db_path.exists():
        return None
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
    src = sqlite3.connect(str(db_path)); dst = sqlite3.connect(tmp.name)
    try:
        with dst:
            src.backup(dst)                     # snapshots a live WAL DB into a single clean file
    finally:
        dst.close(); src.close()
    dest_gz.parent.mkdir(parents=True, exist_ok=True)
    with open(tmp.name, "rb") as f_in, gzip.open(dest_gz, "wb", compresslevel=6) as f_out:
        shutil.copyfileobj(f_in, f_out)
    try:
        os.unlink(tmp.name)
    except OSError:
        pass
    return str(dest_gz)


def restore_snapshot(src_gz=DEFAULT_SNAPSHOT, db_path=DB_PATH) -> bool:
    """Restore the DB from a snapshot ONLY if it passes PRAGMA integrity_check — a corrupt snapshot
    must never overwrite a good brain. Removes stale -wal/-shm sidecars so the restored file is
    authoritative. Returns True on success, False if missing/corrupt."""
    src_gz = Path(src_gz); db_path = Path(db_path)
    if not src_gz.exists():
        return False
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
    with gzip.open(src_gz, "rb") as f_in, open(tmp.name, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    try:
        conn = sqlite3.connect(tmp.name)
        ok = conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        conn.close()
    except sqlite3.DatabaseError:
        ok = False
    if not ok:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
        return False
    db_path.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("", "-wal", "-shm"):
        try:
            os.remove(str(db_path) + ext)
        except OSError:
            pass
    shutil.move(tmp.name, str(db_path))
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Durable brain snapshot save/restore (docs/14).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sv = sub.add_parser("save"); sv.add_argument("--db", default=str(DB_PATH)); sv.add_argument("--out", default=str(DEFAULT_SNAPSHOT))
    rs = sub.add_parser("restore"); rs.add_argument("--in", dest="inp", default=str(DEFAULT_SNAPSHOT)); rs.add_argument("--db", default=str(DB_PATH))
    args = ap.parse_args()
    if args.cmd == "save":
        out = save_snapshot(args.db, args.out)
        if out:
            mb = os.path.getsize(out) / 1e6
            print(f"snapshot saved: {out} ({mb:.2f} MB)"); return 0
        print("no DB to snapshot (skipped)"); return 0
    ok = restore_snapshot(args.inp, args.db)
    print(f"restore {'OK' if ok else 'SKIPPED (missing or failed integrity_check)'}: {args.db}")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
