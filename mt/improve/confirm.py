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

from typing import Dict, List, Optional, Tuple

import numpy as np

from mt.gauntlet import Gauntlet, GauntletContext
from mt.gauntlet.runner import STAGE_CONFIRM
from mt.sim import evaluate

# G10's reference size is DERIVED, not chosen. A permutation p-value over n draws cannot go below
# 1/(n+1), so to test at α/k the reference needs n ≥ ceil(k/α) − 1. A 40-draw reference resolves
# only to p=0.024 while k=6 finalists demand 0.0083 — it would abstain, and 40 holdout reads would
# be spent for a gate that then declines to speak. Capped because confirmations are the one place
# holdout compute is spent, and this runs once per marathon (final digest only).
MAX_HOLDOUT_REFERENCE = 200


def predicted_holdout_periods(store, genome_id: str, holdout_bars: int,
                              train_bars: Optional[int] = None) -> Optional[float]:
    """How many return observations will this genome produce on the holdout?

    Knowable WITHOUT touching the holdout, which is what makes it usable for pre-registration:
    it depends only on the genome's own structure and on how many bars each panel contains — a
    shape, not an outcome.

    Cross-sectional genomes are exact. The executor rebalances on `range(0, n - horizon, horizon)`,
    so the observation count is (bars − horizon) // horizon. Directional genomes produce one
    observation per TRADE, which cannot be derived from the horizon, so their training count is
    scaled by the ratio of panel lengths — trade counts grow with the length of the history."""
    g = store.get_genome(genome_id)
    if g is None or not holdout_bars:
        return None
    if getattr(g.meta, "execution", "") == "cross_sectional" and g.risk.op == "horizon_hold":
        h = max(1, int(g.risk.args.get("horizon", 1) or 1))
        return float(max(0, (int(holdout_bars) - h) // h))
    n_train = store.last_n_periods(genome_id)
    if n_train and train_bars:
        return float(n_train) * float(holdout_bars) / float(train_bars)
    return None


def finalists(store, market: str, limit: int = 12, holdout_bars: Optional[int] = None,
              train_bars: Optional[int] = None) -> Tuple[List[str], List[dict]]:
    """The Stage-A survivors that are eligible for confirmation, and those ruled ineligible.

    Drawn from archive elites that were PROMOTED (cleared the exploratory screen), ranked by
    scalar fitness. Behavioural niching already guarantees they are not all the same idea.

    A genome is only eligible if it can produce at least MIN_PERIODS observations on the holdout.
    Because T = bars/horizon and the train and holdout panels are DIFFERENT LENGTHS, G1's
    20-observation floor admits genomes during the search that it must then reject at
    confirmation. Measured on the 2026-07-29 marathon: 12 of 21 finalists died at G1 on the
    holdout — several with POSITIVE out-of-sample Sharpe (+3.35, +3.25) — because fx and xau
    train on ~794 bars but hold out only ~375, so anything with a horizon between 19 and 39 is
    promotable yet structurally unconfirmable.

    Filtering them here rather than letting them fail matters twice over. They stop burning
    pre-registration slots and holdout reads, and — the part that actually costs discoveries —
    they stop inflating the confirmatory family. That run pre-registered 7/9/7 finalists when only
    4/3/2 were testable, so the survivors were deflated for hypotheses that were never tested,
    right as crypto's book came within p=0.055 of significance."""
    from mt.gauntlet.gates import MIN_PERIODS
    rows = [r for r in store.archive_rows(market) if r["promoted"]]
    rows.sort(key=lambda r: (r["scalar_fit"] if r["scalar_fit"] is not None else float("-inf")),
              reverse=True)
    eligible: List[str] = []
    skipped: List[dict] = []
    for r in rows:
        gid = r["genome_id"]
        if holdout_bars:
            n = predicted_holdout_periods(store, gid, holdout_bars, train_bars)
            if n is not None and n < MIN_PERIODS:
                skipped.append({"genome_id": gid, "predicted_holdout_periods": round(n, 1),
                                "min_periods": MIN_PERIODS})
                continue
        eligible.append(gid)
        if len(eligible) >= limit:
            break
    return eligible, skipped


def confirm(store, market: str, holdout_panel, seed: int = 4242,
            limit: int = 12, train_bars: Optional[int] = None) -> Optional[Dict]:
    """Run one confirmation round. Returns a summary, or None when there is nothing to confirm.

    Order of operations is the whole point and must not be rearranged:
        select finalists → PRE-REGISTER (hash + timestamp) → only then touch the holdout.
    """
    if holdout_panel is None:
        return None
    # Panel LENGTH only — a shape, not an outcome. Reading how many bars exist is not reading
    # what happened in them, so this is safe to consult before the list is sealed.
    try:
        holdout_bars = int(holdout_panel.close_matrix().shape[0])
    except Exception:
        holdout_bars = 0
    ids, ineligible = finalists(store, market, limit=limit,
                                holdout_bars=holdout_bars, train_bars=train_bars)
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

    # ── G10's reference distribution, rebuilt ON THE HOLDOUT ──
    # The exploratory reference describes the training panel and cannot be reused here: a bar
    # calibrated on one dataset says nothing about performance on another. Random genomes are not
    # candidates and are never promoted, so they create no selection bias — but they ARE reads of
    # the sealed panel, so every one is counted under its own purpose. This gives Stage B a
    # confirmation cross-check that involves no σ_SR at all, which matters because σ_SR is the
    # component we found to be most fragile.
    random_ref: List[float] = []
    try:
        import math as _math
        from mt.generators import TemplateSampler
        from mt.gauntlet.gates import BEAT_RANDOM_ALPHA
        n_ref = min(MAX_HOLDOUT_REFERENCE,
                    int(_math.ceil(max(1, n_eff) / BEAT_RANDOM_ALPHA)) - 1)
        sampler = TemplateSampler(seed=seed + 77)
        for _ in range(n_ref):
            rg = sampler._random(market)
            if not rg.typecheck()[0]:
                continue
            store.record_holdout_access(market, rg.genome_id, "g10_reference", prereg_id)
            try:
                rr = evaluate(rg, holdout_panel, seed)
            except Exception:
                continue
            if not rr.ok:
                continue
            spp = rr.summary.get("sharpe_pp"); npd = int(rr.summary.get("n_periods", 0) or 0)
            if spp is None or not np.isfinite(spp) or npd < 2:
                continue
            random_ref.append(float(spp) * float(np.sqrt(npd)))
    except Exception:
        random_ref = []
    # `fresh_sigma` makes G4 derive the deflation spread from each finalist's OWN holdout series
    # instead of the exploratory ledger (see runner.run). `sr_trial_std` stays as the fallback for
    # any series too short to estimate a standard error from.
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=holdout_panel,
                          holdout_panel=holdout_panel, archive_returns={}, seed=seed,
                          sr_trial_std=sr_std, fresh_sigma=True,
                          random_ref=random_ref, random_ref_k=max(1, n_eff))

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
        "holdout_bars": holdout_bars,
        "n_ineligible": len(ineligible),
        "ineligible": ineligible[:8],
        "holdout_accesses_total": store.holdout_access_count(market),
    }


def _loads(s):
    import json
    try:
        return json.loads(s) if s else {}
    except Exception:
        return {}
