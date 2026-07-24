"""mt.live.report — the daily written report (docs/07 §5, docs/08 §5).

The critic's daily digest: what the machine tested, promoted, quarantined, and learned.
Formatting only; delivery reuses the scanners' raw-requests Telegram pattern (best-effort,
silently skipped without a token). No financial action is ever taken from here.
"""
from __future__ import annotations

import html
import os
from typing import Dict


def format_system_report(rep: Dict) -> str:
    L = []
    L.append("═" * 60)
    L.append(" MASTER TRADER — daily research digest")
    L.append("═" * 60)
    disc = rep.get("discovery", {})
    L.append(f"\n▸ DISCOVERY  ({disc.get('generations', 0)} generations × {len(rep.get('markets', []))} markets)")
    eff = disc.get("effective_trials"); rho = disc.get("trial_corr")
    L.append(f"   genomes evaluated : {disc.get('evaluated', 0)}  (raw N)"
             + (f"  →  N_eff={eff}  (ρ̄={rho}, effective independent trials)" if eff is not None else ""))
    L.append(f"   admitted to archive: {disc.get('admitted', 0)}   rejected: {disc.get('rejected', 0)} "
             f"({disc.get('reject_rate', 0):.0%})")
    L.append(f"   families tested    : {disc.get('n_families', 0)}   phenotypes: {disc.get('phenotypes', {})}")
    L.append(f"   engine mix (bandit): {disc.get('bandit', {})}")
    if disc.get("convergence"):
        best = disc.get("dsr_z_best"); gap = disc.get("dsr_gap_to_significance")
        br = disc.get("best_z_recent"); be = disc.get("best_z_early")
        L.append(f"   discovery (best-z) : best z={('—' if best is None else f'{best:+.2f}')}"
                 f"   gap to G4={('—' if gap is None else f'{gap:+.2f}')}"
                 f"   (z=0 luck bar; pass needs z≳1.64)")
        if be is not None and br is not None:
            L.append(f"     best-z early→recent: {be:+.2f} → {br:+.2f}   (this is the signal that matters)")
        L.append(f"   exploration floor  : {disc['convergence']}")

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


# ─── Telegram: a decluttered, emoji, mobile-first digest (HTML parse mode) ──
def _gauge(best_z, width: int = 10) -> str:
    """A progress bar for best-z's climb from the luck bar (z=0) to the pass bar (z≈1.64)."""
    if best_z is None:
        return "⬜" * width + "  —"
    frac = max(0.0, min(1.0, best_z / 1.645))
    filled = int(round(frac * width))
    if filled == 0 and frac > 0:                             # tiny-but-positive → a visible sliver
        return "🟨" + "⬜" * (width - 1) + f"  {frac*100:.0f}%"
    if 0 < filled < width:                                   # leading edge in amber
        return "🟩" * (filled - 1) + "🟨" + "⬜" * (width - filled) + f"  {frac*100:.0f}%"
    return "🟩" * filled + "⬜" * (width - filled) + f"  {frac*100:.0f}%"


def _conv_tag(conv: str) -> str:
    c = (conv or "").upper()
    if "LEARNING" in c:
        return "🧭 Learning — search is improving, scale compute"
    if "SOFTENING" in c:
        return "🧭 Median easing (usually noise) — watch best-z"
    if "FLOOR" in c or "FLAT" in c:
        return "🧭 At the noise floor — feed it new data / conditioning"
    if "WARMING" in c:
        return "🧭 Warming up — needs more generations to call a trend"
    return "🧭 " + (conv or "")


def format_telegram_report(rep: Dict) -> str:
    """A clean, scannable Telegram message (HTML). Leads with the verdict and the one signal that
    matters — best-z — then the essentials, decluttered so it reads at a glance on a phone."""
    disc = rep.get("discovery", {}); arch = rep.get("archive", {}); paper = rep.get("paper", {})
    when = str(rep.get("started", ""))[:16].replace("T", " ")
    mkts = rep.get("markets", [])
    adm = disc.get("admitted", 0); rej = disc.get("rejected", 0); ev = disc.get("evaluated", 0)
    ph = disc.get("phenotypes", {}) or {}
    bz = disc.get("dsr_z_best"); gap = disc.get("dsr_gap_to_significance")
    L = []

    L.append("🤖 <b>Master Trader</b> · research digest")
    L.append(f"<i>{html.escape(when)} · {len(mkts)} markets · {rep.get('elapsed_s', '?')}s</i>")
    L.append("")

    if adm > 0:
        L.append(f"🎉 <b>{adm} candidate{'s' if adm != 1 else ''} cleared the gauntlet!</b>")
    else:
        L.append("🛡️ <b>Nothing cleared</b> — the machine held the line")
        L.append("<i>honest: no genuine edge yet, not a bug</i>")
    L.append("")

    if bz is not None:
        L.append("🎯 <b>Closest to an edge</b>")
        L.append(_gauge(bz))
        L.append(f"best-z <b>{bz:+.2f}</b> · needs <b>+1.64</b> · gap <b>{gap:+.2f}</b>")
        L.append("<i>z 0 = luck · above 1.64 = real edge</i>")
        L.append("")

    L.append("🔬 <b>Discovery</b>")
    eff = disc.get("effective_trials")
    trials_line = f"🧬 <b>{ev}</b> trials"
    if eff is not None:
        trials_line += f" → <b>{eff}</b> effective (ρ̄ {disc.get('trial_corr')})"
    L.append(trials_line + f" · <b>{disc.get('n_families', 0)}</b> families")
    L.append(f"📈 {ph.get('cross_sectional', 0)} cross-sectional · 🎯 {ph.get('directional', 0)} directional")
    L.append(f"❌ {rej} rejected ({disc.get('reject_rate', 0):.0%})")
    if disc.get("convergence"):
        L.append(_conv_tag(disc["convergence"]))
    L.append("")

    L.append(f"🗄️ <b>Archive</b> · {arch.get('coverage', 0)} diverse niches")
    for e in arch.get("elites", [])[:3]:
        L.append(f"   • <code>{html.escape(str(e.get('niche', '')))}</code> "
                 f"fit {e.get('fit', 0):.2f}")
    if paper:
        bs = paper.get("book_sharpe")
        tracked = paper.get("tracked", 0); total = paper.get("n_strategies", 0)
        L.append(f"📝 <b>Paper</b> · " + (f"book sharpe {bs} · {tracked}/{total} tracking"
                                          if bs is not None else "nothing promoted"))
    L.append("")

    lessons = rep.get("recent_lessons", [])
    if lessons:
        L.append(f"💡 <b>Lessons</b> ({rep.get('lessons', 0)})")
        for lz in lessons[:3]:
            txt = lz.split("] ", 1)[-1] if "]" in lz else lz
            L.append(f"   • {html.escape(txt[:95])}")
        L.append("")

    L.append("🔒 <i>Paper only — no capital acted or authorized.</i>")
    return "\n".join(L)


def send_telegram(text: str, token: str = None, chat_id: str = None, timeout: float = 10.0,
                  parse_mode: str = "HTML") -> bool:
    """Best-effort delivery (reuses the scanners' raw Bot API pattern). Silent no-op without creds."""
    token = token or os.environ.get("SMC_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("SMC_CHAT_ID")
    if not token or not chat_id:
        return False
    try:
        import requests
        for i in range(0, len(text), 3900):
            payload = {"chat_id": chat_id, "text": text[i:i + 3900],
                       "disable_web_page_preview": True}
            if parse_mode:
                payload["parse_mode"] = parse_mode
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json=payload, timeout=timeout)
        return True
    except Exception:
        return False
