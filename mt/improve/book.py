"""mt.improve.book — portfolio-level significance (docs/15 §5).

The system spent its whole life asking "is there a SINGLE genome whose Sharpe survives deflation
for every trial we ever ran?". That is the hardest possible question, and the measured answer was
that three candidates in 23,030 cleared the z bar and all three then died on robustness.

Institutional alpha factories do not ask it. WorldQuant has produced >20 million alphas while
deliberately hunting *ever weaker* signals, and scores submissions as BASKETS whose members have
strong-but-uncorrelated returns; AlphaGen makes this explicit by optimizing the combined IC of an
alpha SET rather than each alpha alone, and found that even mutually-correlated alphas can be
synergistic. The arithmetic is the point: k decorrelated strategies each worth t ≈ 0.4 combine to
t ≈ 0.4·√k, so twenty of them reach ≈1.8 — above the significance bar that none of them can reach
alone. The hall of fame already holds genomes at exactly that individual strength.

This module builds that basket honestly:
  • members come only from the archive (behaviourally distinct niches),
  • selection is GREEDY ON MARGINAL CONTRIBUTION with a correlation cap, so adding a near-clone
    cannot inflate the count,
  • the book's own Deflated Sharpe is charged a family size equal to the number of BOOKS
    considered — not one, and not the genome ledger. Building a portfolio is itself a selection,
    and pretending otherwise would reintroduce the bias this whole subsystem exists to control.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

MAX_MEMBER_CORR = 0.60          # above this a candidate adds risk, not diversification
MIN_MEMBERS = 3
MAX_MEMBERS = 24


def _align(series_by_id: Dict[str, pd.Series]) -> pd.DataFrame:
    """Union calendar, flat (0.0) where a member did not trade — the same time-alignment rule the
    CPCV matrix uses, so a member that trades rarely cannot silently shorten the book.

    Duplicate index labels are collapsed FIRST. A member whose return series carries a repeated
    timestamp (the cross-sectional executor indexes by rebalance bar, and a panel with a repeated
    bar produces one) made `pd.DataFrame({...})` raise "cannot reindex on an axis with duplicate
    labels". In Stage B that exception was swallowed by the caller's try/except and reported as
    "confirmation skipped" — a silent loss of the entire confirmation round."""
    if not series_by_id:
        return pd.DataFrame()
    clean = {}
    for k, v in series_by_id.items():
        s = pd.Series(v).astype(float)
        if s.index.has_duplicates:
            s = s.groupby(level=0).mean()
        clean[k] = s
    df = pd.DataFrame(clean)
    return df.sort_index().fillna(0.0)


def _sharpe(x: np.ndarray) -> float:
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size < 2:
        return float("nan")
    sd = x.std(ddof=1)
    return float(x.mean() / sd) if sd > 0 else float("nan")


def select_members(series_by_id: Dict[str, pd.Series], max_members: int = MAX_MEMBERS,
                   max_corr: float = MAX_MEMBER_CORR) -> Tuple[List[str], int]:
    """Greedy max-marginal-Sharpe selection under a pairwise correlation cap.

    Starts from the strongest single member, then repeatedly adds whichever remaining candidate
    most improves the EQUAL-WEIGHT book Sharpe, refusing any candidate correlated above the cap
    with something already in. Greedy-on-the-book (not top-k-by-own-Sharpe) is what makes this a
    portfolio rather than a leaderboard: a mediocre member that zigs when the others zag will be
    taken ahead of a strong member that duplicates the book.

    Returns `(members, n_selection_trials)`. The second value is the number of distinct candidate
    books whose Sharpe was actually examined during selection, and it is NOT bookkeeping trivia:
    assembling a portfolio is itself a search, so reporting the winning combination without
    charging the combinations that lost is precisely the selection bias this system exists to
    control. It flows straight into the book's own Deflated-Sharpe family size."""
    df = _align(series_by_id)
    if df.shape[1] == 0 or df.shape[0] < 20:
        return [], 0
    cols = list(df.columns)
    solo = {c: _sharpe(df[c].to_numpy()) for c in cols}
    cols = [c for c in cols if np.isfinite(solo[c])]
    if not cols:
        return [], 0
    corr = df[cols].corr().fillna(0.0)
    chosen = [max(cols, key=lambda c: solo[c])]
    trials = len(cols)                       # every solo Sharpe we looked at to pick the seed
    while len(chosen) < min(max_members, len(cols)):
        best, best_sh = None, _sharpe(df[chosen].mean(axis=1).to_numpy())
        for c in cols:
            if c in chosen:
                continue
            if max(abs(float(corr.loc[c, o])) for o in chosen) > max_corr:
                continue
            trials += 1                      # one more candidate book examined
            sh = _sharpe(df[chosen + [c]].mean(axis=1).to_numpy())
            if np.isfinite(sh) and sh > best_sh:
                best, best_sh = c, sh
        if best is None:
            break
        chosen.append(best)
    return chosen, trials


def book_sigma_sr(series_by_id: Dict[str, pd.Series], n_members: int,
                  n_samples: int = 200, seed: int = 17) -> Optional[float]:
    """Dispersion of Sharpe ACROSS CANDIDATE BOOKS of the same size.

    This is the σ_SR the book's Deflated Sharpe needs, and it is emphatically not the ledger's
    genome-level σ_SR. The DSR deflation term is σ_SR·E[max of N], so σ_SR must describe the
    dispersion of the *object being selected*. Feeding it the spread of individual genome Sharpes
    (≈0.24) while the object is an equal-weight book (whose Sharpe spread is far smaller, because
    averaging decorrelated members shrinks variance) over-deflates enormously — measured as a book
    z of −49.6, which is not a conservative answer, it is a meaningless one.

    Estimated by resampling random member subsets of the same size from the same candidate pool:
    literally the null distribution of "a book of this size assembled from these candidates"."""
    ids = [k for k in series_by_id if series_by_id[k] is not None]
    if len(ids) <= n_members or n_members < 1:
        return None
    df = _align(series_by_id)
    if df.shape[0] < 20:
        return None
    rng = np.random.default_rng(seed)
    sh = []
    for _ in range(int(n_samples)):
        pick = rng.choice(len(ids), size=n_members, replace=False)
        s = _sharpe(df[[ids[i] for i in pick]].mean(axis=1).to_numpy())
        if np.isfinite(s):
            sh.append(float(s))
    if len(sh) < 8:
        return None
    sd = float(np.std(sh))
    return sd if sd > 0 else None


def build_book(series_by_id: Dict[str, pd.Series], n_books_tried: int = 0,
               sr_trial_std: Optional[float] = None,
               max_members: int = MAX_MEMBERS,
               members: Optional[List[str]] = None,
               fresh_sigma: bool = False) -> Optional[dict]:
    """Assemble the equal-weight book and test ITS Deflated Sharpe.

    The family size charged is `n_books_tried` (books assembled in previous rounds) PLUS the
    combinations examined inside this round's greedy selection. It is deliberately not the genome
    trial count — the hypothesis under test is "this combination has an edge", and few such
    hypotheses exist — but equally deliberately not 1, because picking the members was a search.

    Pass `members` to score a FIXED, pre-registered membership (Stage-B confirmation): no
    selection happens, so no selection trials are charged."""
    from mt.adapters.cclib import deflated_sharpe, sharpe_std_error
    if members is None:
        members, sel_trials = select_members(series_by_id, max_members=max_members)
    else:
        members = [m for m in members if m in series_by_id]
        sel_trials = 0                        # membership was fixed in advance — nothing searched
    if len(members) < MIN_MEMBERS:
        return None
    n_books_tried = max(1, int(n_books_tried) + int(sel_trials))
    df = _align({k: series_by_id[k] for k in members})
    book = df.mean(axis=1)                                  # equal weight: no fitted weights, no
    r = book.to_numpy(float)                                # extra parameters to overfit
    if r.size < 20:
        return None
    corr = df.corr().to_numpy(float)
    iu = np.triu_indices_from(corr, k=1)
    mean_corr = float(np.nanmean(corr[iu])) if corr.shape[0] > 1 else 0.0
    # σ_SR must describe the dispersion of BOOKS, not of genomes (see book_sigma_sr).
    #
    # `fresh_sigma` is the Stage-B case: membership was pre-registered and the panel is sealed, so
    # nothing was selected on this data and the null spread is simply the book's own Sharpe
    # standard error. Resampling subsets would be meaningless there anyway — Stage B passes the
    # finalists as BOTH the pool and the membership, so `book_sigma_sr`'s `len(ids) <= n_members`
    # guard returned None on every single call and the code silently fell back to the genome-level
    # ledger σ_SR: the exact category error this function exists to prevent, ~10× too large.
    resampled = None if fresh_sigma else book_sigma_sr(series_by_id, len(members))
    sigma = resampled
    sigma_source = "book_resample"
    if sigma is None and fresh_sigma:
        sigma = sharpe_std_error(r.tolist())
        sigma_source = "book_sr_se"
    if sigma is None:
        sigma = sr_trial_std
        sigma_source = "fallback"
    d = deflated_sharpe(book.tolist(), n_trials=max(1, int(n_books_tried)), sr_trial_std=sigma)
    solo = [_sharpe(df[c].to_numpy()) for c in df.columns]
    solo = [s for s in solo if np.isfinite(s)]
    return {
        "members": members,
        "n_members": len(members),
        "book_sharpe_pp": round(_sharpe(r), 5),
        "book_edge_t": round(float(_sharpe(r) * np.sqrt(r.size)), 4),
        "best_member_sharpe_pp": round(max(solo), 5) if solo else None,
        "mean_member_corr": round(mean_corr, 4),
        "diversification_gain": (round(_sharpe(r) / max(solo), 3) if solo and max(solo) > 0 else None),
        "book_dsr_z": d.get("dsr_z_score"),
        "book_dsr_p": d.get("dsr_pvalue"),
        "book_reliable": d.get("reliable"),
        "book_sigma_sr": None if sigma is None else round(float(sigma), 6),
        "sigma_source": sigma_source,
        "n_books_tried": int(n_books_tried),
        "selection_trials": int(sel_trials),
        "returns": book,
    }
