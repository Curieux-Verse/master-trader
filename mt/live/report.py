"""mt.live.report — the daily written report (docs/07 §5, docs/08 §5).

The critic's daily digest: what the machine tested, promoted, quarantined, and learned.
Formatting only; delivery reuses the scanners' raw-requests Telegram pattern (best-effort,
silently skipped without a token). No financial action is ever taken from here.
"""
from __future__ import annotations

import os
from typing import Dict


def format_system_report(rep: Dict) -> str:
    L = []
    L.append("═" * 60)
    L.append(" MASTER TRADER — daily research digest")
    L.append("═" * 60)
    disc = rep.get("discovery", {})
    L.append(f"\n▸ DISCOVERY  ({disc.get('generations', 0)} generations × {len(rep.get('markets', []))} markets)")
    L.append(f"   genomes evaluated : {disc.get('evaluated', 0)}  (ledger trial count N)")
    L.append(f"   admitted to archive: {disc.get('admitted', 0)}   rejected: {disc.get('rejected', 0)} "
             f"({disc.get('reject_rate', 0):.0%})")
    L.append(f"   families tested    : {disc.get('n_families', 0)}   phenotypes: {disc.get('phenotypes', {})}")
    L.append(f"   engine mix (bandit): {disc.get('bandit', {})}")

    arch = rep.get("archive", {})
    L.append(f"\n▸ ARCHIVE  ({arch.get('coverage', 0)} diverse niches)")
    for e in arch.get("elites", [])[:8]:
        L.append(f"   {e.get('niche',''):32} fit={e.get('fit',0):.3f}  [{e.get('market','')}]")

    paper = rep.get("paper", {})
    if paper:
        L.append(f"\n▸ PAPER / SHADOW  (R1 — no capital)")
        L.append(f"   book sharpe (paper): {paper.get('book_sharpe')}   days: {paper.get('days', 0)}")
        tracked = paper.get("tracked", 0); total = paper.get("n_strategies", 0)
        L.append(f"   live≈backtest      : {tracked}/{total} strategies tracking expectation")
        for ev in paper.get("events", [])[:6]:
            L.append(f"   ⚠ {ev}")

    L.append(f"\n▸ LESSONS LIBRARY  ({rep.get('lessons', 0)} accumulated)")
    for lz in rep.get("recent_lessons", [])[:4]:
        L.append(f"   • {lz}")

    L.append(f"\n▸ GOVERNANCE")
    L.append("   No live-capital action taken or authorized. Promotions are recommendations only.")
    L.append("═" * 60)
    return "\n".join(L)


def send_telegram(text: str, token: str = None, chat_id: str = None, timeout: float = 10.0) -> bool:
    """Best-effort delivery (reuses the scanners' raw Bot API pattern). Silent no-op without creds."""
    token = token or os.environ.get("SMC_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("SMC_CHAT_ID")
    if not token or not chat_id:
        return False
    try:
        import requests
        for i in range(0, len(text), 3900):
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat_id, "text": text[i:i + 3900]}, timeout=timeout)
        return True
    except Exception:
        return False
