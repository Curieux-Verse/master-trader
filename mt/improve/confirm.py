"""mt.improve.confirm — Stage B, the confirmatory stage (docs/15 §4).

Exploration and confirmation are different statistical regimes. Stage A screens under an
FDR-controlled, N-independent rule so the search has a stable signal to learn from. Stage B is
where a candidate becomes a *claim*, and it is deliberately STRICTER than anything the system did
before:

  1. **Pre-registration.** The finalist list is content-hashed and timestamped BEFORE the sealed
     holdout is read. Stage B may only confirm a list that already exists in the
     `preregistration` table. Without this artifact a two-stage protocol is p-hacking with extra
     steps — you could quietly redraw the finalists after a disappointing holdout.

  2. **The holdout is genuinely sealed.** This is the only code path allowed to evaluate on it,
     and every access is counted in `holdout_ledger`. The previous design had no budget at all:
     the last production run evaluated the G6 transfer gate on all 23,030 genomes, which turned
     the "unseen" panel into a selection surface. A holdout looked at 23,030 times is not a
     holdout.

  3. **A small, honest family.** Because the confirmation is performed on data that played no
     part in selection, the multiplicity that applies is the number of hypotheses CARRIED FORWARD
     — the finalists — not the exploratory ledger. This is the standard sample-splitting argument,
     and it is paid for with fresh data, not by relabelling. The family size is still deflated to
     effectively-independent trials (K_eff) before the Deflated Sharpe sees it.

No gate is relaxed here. A genome must survive Stage A, be written down, and then clear the FULL
gauntlet — G4 included, plus CPCV and the transfer gate — on data it has never touched.
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np

from mt.gauntlet import Gauntlet, GauntletContext
from mt.gauntlet.runner import STAGE_CONFIRM
from mt.sim import evaluate


def finalists(store, market: str, limit: int = 12) -> List[str]:
    """The Stage-A survivors that are eligible for confirmation.

    Drawn from archive elites that were PROMOTED (cleared the exploratory screen), ranked by
    scalar fitness. Behavioural niching already guarantees they are not all the same idea."""
    rows = [r for r in store.archive_rows(market) if r["promoted"]]
    rows.sort(key=lambda r: (r["scalar_fit"] if r["scalar_fit"] is not None else float("-inf")),
              reverse=True)
    return [r["genome_id"] for r in rows[:limit]]


def confirm(store, market: str, holdout_panel, seed: int = 4242,
            limit: int = 12) -> Optional[Dict]:
    """Run one confirmation round. Returns a summary, or None when there is nothing to confirm.

    Order of operations is the whole point and must not be rearranged:
        select finalists → PRE-REGISTER (hash + timestamp) → only then touch the holdout.
    """
    if holdout_panel is None:
        return None
    ids = finalists(store, market, limit=limit)
    if not ids:
        return None

    # ── the confirmatory family: the finalists, deflated to independent trials ──
    # K_eff must be measured on the FINALISTS' OWN return signatures. It used to be computed from
    # `store.trial_signatures(market)` — the market-wide trial population — and then applied to the
    # finalist count. The finalists come from distinct MAP-Elites niches, so they are far less
    # mutually correlated than the general population; borrowing the population's ratio understated
    # N_eff and made the confirmatory family too small, i.e. the bar too easy.
    from mt.gauntlet.multipletest import effective_trials
    sigs = store.trial_signatures(market, genome_ids=ids)
    if len(sigs) < 3:                                  # not enough signatures to estimate ρ
        sigs = store.trial_signatures(market)
    keff = effective_trials(len(ids), sigs)
    n_eff = int(keff["n_eff"])

    # ── SEAL THE LIST. Nothing below may change what is being tested. ──
    prereg_id, list_hash = store.preregister(market, ids, n_eff, keff["method"])

    gauntlet = Gauntlet()
    sr_std = store.sr_trial_std(market) or store.sr_trial_std(None)
    # `fresh_sigma` makes G4 derive the deflation spread from each finalist's OWN holdout series
    # instead of the exploratory ledger (see runner.run). `sr_trial_std` stays as the fallback for
    # any series too short to estimate a standard error from.
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=holdout_panel,
                          holdout_panel=holdout_panel, archive_returns={}, seed=seed,
                          sr_trial_std=sr_std, fresh_sigma=True)

    results, cleared = [], []
    oos_returns: Dict[str, object] = {}
    for gid in ids:
        g = store.get_genome(gid)
        if g is None or not g.typecheck()[0]:
            continue
        store.record_holdout_access(market, gid, "stage_b_confirm", prereg_id)
        try:
            res = evaluate(g, holdout_panel, seed)        # sealed data; NEVER written to the ledger
        except Exception:
            continue
        if not res.ok:
            continue
        oos_returns[gid] = res.net_returns
        rep = gauntlet.run(g, res, trial_count=n_eff, ctx=ctx, stage=STAGE_CONFIRM)
        g4 = rep.gates.get("G4_deflated_sharpe", {}) or {}
        row = {"genome_id": gid, "cleared": bool(rep.cleared), "failed_gate": rep.failed_gate,
               "oos_sharpe": res.summary.get("net_sharpe"), "oos_dsr_z": g4.get("dsr_z")}
        results.append(row)
        if rep.cleared:
            cleared.append(gid)
            # mark the archive incumbent as confirmed — the ONLY route to a tradeable flag
            for r in store.archive_rows(market):
                if r["genome_id"] == gid:
                    store.upsert_archive(r["niche_key"], gid, market,
                                         _loads(r["fitness"]), _loads(r["descriptor"]),
                                         float(r["scalar_fit"] or 0.0) + 1e-9,
                                         promoted=True, cleared=True)
                    break

    # ── the BOOK is a candidate too, and is confirmed the same way ──
    # Membership is FIXED to the pre-registered finalists, so no selection happens on holdout data
    # and the book is charged only for the rounds of assembly that preceded it. Scoring the book
    # on the same panel that chose its members would be an in-sample number wearing a portfolio
    # costume (docs/15 §5).
    book = None
    if len(oos_returns) >= 3:
        from mt.improve.book import build_book
        # The book does not get the holdout to itself: this round put `n_eff` finalist hypotheses
        # plus the book in front of the same sealed panel, and earlier rounds spent it too. Charge
        # all of them, so a portfolio cannot be quietly cheaper to confirm than its members.
        b = build_book(oos_returns, n_books_tried=n_eff + 1 + store.prereg_count(market),
                       sr_trial_std=sr_std, members=list(oos_returns), fresh_sigma=True)
        if b:
            book = {k: v for k, v in b.items() if k != "returns"}
            store.record_book(market, b["members"], None, None,
                              b["book_sharpe_pp"], b["book_dsr_z"])

    store.mark_confirmed(prereg_id)
    # WHY a round failed is the single most useful line in the digest. Without it "→ 0 cleared" is
    # indistinguishable from a bug, and diagnosing the 2026-07-28 rounds needed a forensic audit of
    # the brain rather than a glance at the report.
    from collections import Counter
    rejected = Counter(r["failed_gate"] or "?" for r in results if not r["cleared"])
    zs = [r["oos_dsr_z"] for r in results if r.get("oos_dsr_z") is not None]
    shp = [r["oos_sharpe"] for r in results if r.get("oos_sharpe") is not None]
    return {
        "prereg_id": prereg_id, "list_hash": list_hash, "market": market,
        "family_size": len(ids), "n_eff": n_eff, "keff_method": keff["method"],
        "n_tested": len(results), "n_cleared": len(cleared), "cleared": cleared,
        "results": results, "book_oos": book,
        "rejected_by": dict(rejected.most_common()),
        "best_oos_z": (max(zs) if zs else None),
        "median_oos_sharpe": (float(np.median(shp)) if shp else None),
        "holdout_accesses_total": store.holdout_access_count(market),
    }


def _loads(s):
    import json
    try:
        return json.loads(s) if s else {}
    except Exception:
        return {}
