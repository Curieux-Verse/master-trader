"""mt.selftest_gauntlet — the critical go/no-go (docs/09 Phase 2).

Two experiments, both essential:

  (A) OVERFIT TRAP — on edgeless (random-walk) data, pick the best backtest out of many
      random genomes (classic selection overfitting) and confirm the gauntlet REJECTS it
      once the honest trial count deflates the Sharpe / PBO flags the tuning. If the
      gauntlet cannot catch a strategy we overfit on purpose, nothing downstream is
      trustworthy.

  (B) REAL-EDGE CONTROL — on data with a *genuine* injected momentum edge and a small
      trial count, confirm a momentum genome clears the significance gate (G4). This proves
      the gauntlet is a discriminator, not merely a rejection machine — it must let a real
      edge through, or the whole enterprise is pointless.

    python -m mt.selftest_gauntlet
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd

from mt.data.panel import NormPanel
from mt.genome.schema import Genome, Meta, FeatureNode, SignalSpec, SizingSpec, RiskSpec
from mt.generators import TemplateSampler
from mt.sim import evaluate
from mt.gauntlet import Gauntlet, GauntletContext


def make_panel(edge: bool, n_sym: int = 10, bars: int = 900, seed: int = 0) -> NormPanel:
    rng = np.random.default_rng(seed)
    end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    times = pd.to_datetime([end - timedelta(hours=4) * (bars - 1 - i) for i in range(bars)], utc=True)
    # persistent per-symbol drift ⇒ a genuine, capturable CROSS-SECTIONAL momentum edge
    mu = rng.normal(0, 0.0025, n_sym) if edge else np.zeros(n_sym)
    frames = {}
    for s in range(n_sym):
        e = rng.normal(0, 0.012, bars)
        r = (mu[s] + e) if edge else rng.normal(0, 0.02, bars)   # drift+noise vs pure random walk
        close = 100 * np.exp(np.cumsum(r))
        high = close * (1 + np.abs(rng.normal(0, 0.004, bars)))
        low = close * (1 - np.abs(rng.normal(0, 0.004, bars)))
        df = pd.DataFrame({
            "datetime": times, "open": close, "high": high, "low": low, "close": close,
            "volume": rng.lognormal(10, 1, bars),
            "atr_14": pd.Series(np.abs(close * 0.01)).rolling(14, min_periods=1).mean().to_numpy(),
            "funding_rate": rng.normal(0.0001, 0.0004, bars),
        })
        frames[f"S{s}"] = {"4h": df}
    return NormPanel(market="crypto", asof=end, snapshot_id="selftest",
                     symbols=list(frames), frames=frames, timeframes={"htf": "4h"})


def momentum_genome(lookback: int = 20, horizon: int = 2) -> Genome:
    return Genome(
        meta=Meta(market="crypto", htf="4h"),
        features=[FeatureNode("f1", "momentum", {"lookback": lookback, "skip": 1})],
        signal=SignalSpec("weighted_blend", {"direction": "neutral"}),
        sizing=SizingSpec("rank_bucket", {"top_frac": 0.25, "gross": 1.0, "per_name_cap": 0.2}),
        risk=RiskSpec("horizon_hold", {"horizon": horizon, "cost_stress": 1.0}),
    )


def experiment_overfit_trap(seed: int = 1, k: int = 40) -> dict:
    import statistics
    panel = make_panel(edge=False, seed=seed)
    sampler = TemplateSampler(seed=seed)
    gauntlet = Gauntlet()

    best, best_res, best_sh = None, None, -np.inf
    spps = []
    for _ in range(k):
        g = sampler._random("crypto")
        res = evaluate(g, panel, seed)
        if res.ok and np.isfinite(res.summary.get("net_sharpe", np.nan)):
            spp = res.summary.get("sharpe_pp")
            if spp is not None and np.isfinite(spp):
                spps.append(float(spp))                       # per-observation Sharpe of each trial
            if res.summary["net_sharpe"] > best_sh:
                best, best_res, best_sh = g, res, res.summary["net_sharpe"]

    # The cross-trial Sharpe dispersion σ_SR the PRODUCTION Result Ledger computes from these N
    # trials (store.sr_trial_std). It is the correct scale for DSR's E[max SR] deflation. WITHOUT
    # it, G4 falls back to the candidate's own SE and under-deflates ~4× → the best-of-N selection
    # overfit slips through G4 (the true multiple-testing firewall). Passing it makes the self-test
    # exercise the gauntlet exactly as the marathon does, so the trap is caught by G4 — not by an
    # incidental G3 behaviour (docs/05 §3, DSR Appendix 3).
    sigma_sr = statistics.pstdev(spps) if len(spps) >= 8 else None
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel, seed=seed,
                          sr_trial_std=sigma_sr)
    report = gauntlet.run(best, best_res, trial_count=k, ctx=ctx)     # honest N = k tried
    return {"is_sharpe": best_sh, "passed": report.passed, "failed_gate": report.failed_gate,
            "gates": report.gates, "sigma_sr": sigma_sr}


def experiment_real_edge(seed: int = 2) -> dict:
    """A genuine edge must clear BOTH stages: the Stage-A FDR screen and the confirmatory G4.

    The screen is exercised against a realistic trial population (random genomes on the same
    panel), because a threshold of None trivially rejects everything — the screen has to be shown
    admitting a real edge out of a crowd, which is the whole point of a discriminator."""
    from mt.gauntlet.multipletest import bhy_threshold, sharpe_pvalue
    from mt.gauntlet.runner import STAGE_EXPLORE, STAGE_CONFIRM
    panel = make_panel(edge=True, seed=seed)
    sampler = TemplateSampler(seed=seed)
    pvals = []
    for _ in range(24):                                   # the surrounding trial population
        r = evaluate(sampler._random("crypto"), panel, seed)
        if r.ok:
            p = sharpe_pvalue(r.summary.get("sharpe_pp"), r.summary.get("n_periods"))
            if p is not None:
                pvals.append(p)
    g = momentum_genome()
    res = evaluate(g, panel, seed)
    p_edge = sharpe_pvalue(res.summary.get("sharpe_pp"), res.summary.get("n_periods"))
    if p_edge is not None:
        pvals.append(p_edge)
    thr = bhy_threshold(pvals, q=0.10)
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel, seed=seed,
                          fdr_threshold=thr)
    gauntlet = Gauntlet()
    rep_a = gauntlet.run(g, res, trial_count=3, ctx=ctx, stage=STAGE_EXPLORE)
    rep_b = gauntlet.run(g, res, trial_count=3, ctx=ctx, stage=STAGE_CONFIRM)   # small honest N
    g4 = rep_b.gates.get("G4_deflated_sharpe", {})
    return {"is_sharpe": res.summary.get("net_sharpe"), "passed": rep_b.passed,
            "promoted": rep_a.promoted, "stage_a_gate": rep_a.failed_gate,
            "failed_gate": rep_b.failed_gate, "g4_significant": g4.get("is_significant"),
            "raw_sharpe": g4.get("raw_sharpe"), "dsr_p": g4.get("dsr_pvalue"),
            "screen_p": p_edge, "fdr_threshold": thr,
            "pbo": rep_b.gates.get("G3_cpcv_pbo", {}).get("pbo")}


def experiment_effective_n(seed: int = 5, k: int = 30) -> dict:
    """EFFECTIVE trial count over the REAL ledger path: a family of genomes that are structurally
    distinct but whose P&L moves together must collapse to few independent trials, while a
    genuinely diverse set must not (López de Prado, DSR Appendix 3).

    The near-duplicate family is built from 30 DIFFERENT lookbacks rather than repeats of one
    genome. That is both the honest real-world case — production's top-20 were parameter jitter on
    a single idea, each a distinct genome — and now the only expressible one, since the ledger
    refuses to charge a second trial for a genome it has already evaluated (experiment G)."""
    import os
    import tempfile
    from mt.store import MTStore
    panel = make_panel(edge=True, n_sym=8, bars=600, seed=seed)
    ops = ["momentum", "rsi", "breakout", "macd", "bb_position", "obv", "cci", "adx",
           "atr_expansion", "vwap_distance", "volume_zscore", "autocorr", "slope", "roc",
           "stoch", "williams_r", "cmf", "mfi", "trix", "kama", "donchian_position",
           "keltner_position", "ulcer_index", "zscore", "rank_momentum", "skewness",
           "kurtosis", "volatility", "range_ratio", "gap_ratio"]

    def build(dupe: bool) -> tuple:
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
        store = MTStore(db_path=tmp.name)
        n_ok = 0
        for i in range(k):
            if dupe:                                  # 30 DISTINCT genomes, near-identical P&L
                g = momentum_genome(lookback=20 + i, horizon=2)
            else:
                from mt.genome.registry import REGISTRY
                op = ops[i % len(ops)]
                if op not in REGISTRY:
                    op = ops[i % 8]
                g = Genome(Meta(market="crypto", htf="4h"), [FeatureNode("f1", op, {})],
                           SignalSpec("weighted_blend", {"direction": ("long_bias", "short_bias", "neutral")[i % 3]}),
                           SizingSpec("rank_bucket", {"top_frac": 0.2, "gross": 1.0, "per_name_cap": 0.15}),
                           RiskSpec("horizon_hold", {"horizon": 2 + i % 6, "cost_stress": 1.0}))
            if not g.typecheck()[0]:
                continue
            _eid, is_new = store.record_eval(evaluate(g, panel, seed))
            n_ok += int(is_new)
        out = (store.trial_count("crypto"), store.avg_trial_corr("crypto"),
               store.effective_trial_count("crypto"))
        store.close()
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
        return out

    dup = build(True); div = build(False)
    return {"dup_raw": dup[0], "dup_rho": dup[1], "dup_neff": dup[2],
            "div_raw": div[0], "div_rho": div[1], "div_neff": div[2]}


def experiment_directional_cpcv() -> dict:
    """Directional CPCV must align variant returns by TIME, not by trade position (docs/14 review).
    Three 'variants' realize returns on DIFFERENT bars (like directional trades at different times).
    Time-alignment (the fix) yields the UNION calendar with flat bars = 0; the old position-tail
    alignment would take the MIN length and mix different calendar times across columns. We assert
    the union shape and exact flat-bar zeros — a check position-alignment cannot pass."""
    from mt.gauntlet import cpcv
    from mt.sim.evalresult import EvalResult
    t = pd.date_range("2026-01-01", periods=100, freq="4h", tz="UTC")
    canned = {0: pd.Series(0.010, index=t[::2]),     # trades on even bars (50)
              1: pd.Series(0.010, index=t[1::2]),    # trades on odd bars  (50)
              2: pd.Series(-0.005, index=t[::3])}    # every third bar      (34)
    variants = list(canned)                          # 0,1,2 as opaque "variants"
    def ev(v, _panel):
        r = EvalResult(genome_id=str(v), market="crypto")
        r.net_returns = canned[v]
        return r
    mat = cpcv.returns_matrix(variants, None, ev)
    ok_shape = mat is not None and mat.shape == (100, 3)         # union calendar (NOT min=34)
    # bar t[0] (even & divisible-by-3): var0 trades, var1 FLAT=0, var2 trades
    row0_ok = ok_shape and np.allclose(mat[0], [0.010, 0.0, -0.005])
    # bar t[1] (odd): var0 FLAT=0, var1 trades, var2 FLAT=0 (1 % 3 != 0)
    row1_ok = ok_shape and np.allclose(mat[1], [0.0, 0.010, 0.0])
    pbo = None if mat is None else cpcv.cscv_pbo(mat, n_groups=6)
    return {"matrix_shape": None if mat is None else mat.shape,
            "time_aligned": bool(row0_ok and row1_ok), "pbo_runs": pbo is not None}


def experiment_gate_robustness() -> dict:
    """Degenerate & ruinous return series must not slip through (docs/14 gate review). A (near-)
    constant series has a float-noise std → an astronomical spurious Sharpe that must be rejected at
    G1 (else it passes G4b/G4); a bootstrap path with a ≤−100% bar must yield a drawdown in [0,1],
    not NaN or >1. Regression guard so these robustness fixes can't silently rot."""
    from mt.gauntlet import gates as G
    from mt.adapters.cclib import bootstrap_drawdown
    const_reject = G.g1_sanity(pd.Series(np.full(200, 0.001))).status == "fail"
    near_reject = G.g1_sanity(pd.Series(0.001 + np.random.default_rng(0).normal(0, 1e-9, 200))).status == "fail"
    ruin = np.r_[np.random.default_rng(1).normal(0.001, 0.02, 150), [-1.5, -1.0],
                 np.random.default_rng(2).normal(0.001, 0.02, 48)]
    dd = bootstrap_drawdown(ruin.tolist(), n_sims=400, seed=1).get("max_dd_95")
    dd_ok = dd is not None and np.isfinite(dd) and 0.0 <= dd <= 1.0

    # σ_SR must survive a CONTAMINATED ledger. The ledger is written before the gauntlet runs, so
    # degenerate genomes (near-constant returns → float-noise std → absurd Sharpe) are stored even
    # though G1 rejects them. The real production brain holds sharpe_pp up to 38,026, which made
    # the plain std 2,497 against a true value of ~0.23 — and since the deflation is σ_SR·E[max N],
    # that alone drove every candidate's z to minus infinity. A robust estimator is not a nicety
    # here; without it nothing can ever clear the bar regardless of the strategies.
    import os, tempfile, sqlite3
    from mt.store import MTStore
    tmpc = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmpc.close()
    st = MTStore(db_path=tmpc.name)
    rng2 = np.random.default_rng(3)
    clean = list(rng2.normal(0.0, 0.22, 200))                 # plausible per-bar Sharpes
    junk = [38026.5, -421.2, 17201.9, 9999.0, 5000.0] * 4      # numerical degenerates (~9%)
    for i, v in enumerate(clean + junk):
        st.conn.execute("INSERT INTO result_ledger(genome_id,market,sharpe_pp,n_periods,created_at)"
                        " VALUES(?,?,?,?,0)", (f"c{i}", "crypto", float(v), 300))
    st.conn.commit()
    sigma = st.sr_trial_std("crypto")
    st.close()
    try:
        os.unlink(tmpc.name)
    except OSError:
        pass
    sigma_ok = sigma is not None and 0.05 < sigma < 1.0        # true value ≈0.22, not thousands
    return {"const_reject": const_reject, "near_reject": near_reject, "ruin_dd": dd, "dd_ok": dd_ok,
            "sigma_contaminated": None if sigma is None else round(sigma, 4), "sigma_ok": sigma_ok}


def experiment_keff_duplicates(seed: int = 11) -> dict:
    """K_eff must COLLAPSE when the search produces near-clones, and must not when it doesn't.

    This is the estimator's whole reason for existing. The equicorrelation formula it replaces
    reads only the shape of the correlation spectrum, not its scale, so in production it reported
    ρ̄=0.00998 → N_eff=100 out of 46,843 trials while the top-20 candidates were parameter jitter
    on a single obv×vwap_distance idea. The mixed case below is the one that distinguishes them:
    25 clones plus 5 genuinely different strategies is 6 independent trials, and an estimator that
    answers 1 (equicorrelation) or 30 (raw) is unusable for deflation."""
    from mt.gauntlet.multipletest import effective_trials
    rng = np.random.default_rng(seed)
    base = rng.standard_normal(24)
    dup = [base + rng.normal(0, 0.01, 24) for _ in range(30)]
    div = [rng.standard_normal(24) for _ in range(30)]
    mixed = dup[:25] + div[:5]
    d = effective_trials(30, dup)["n_eff"]
    v = effective_trials(30, div)["n_eff"]
    m = effective_trials(30, mixed)["n_eff"]
    return {"dup_neff": d, "div_neff": v, "mixed_neff": m,
            "ok": bool(d <= 3 and v >= 20 and 3 <= m <= 12)}


def experiment_ledger_dedup(seed: int = 12) -> dict:
    """Re-evaluating the SAME genome on the SAME data must not charge a second trial.

    It is deterministic, so it yields a bit-identical result and represents no new hypothesis —
    yet it used to raise the significance bar for every other candidate (measured: 25% of the
    production ledger, one genome evaluated 12 times returning one distinct answer)."""
    import os, tempfile
    from mt.store import MTStore
    panel = make_panel(edge=True, n_sym=6, bars=400, seed=seed)
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
    store = MTStore(db_path=tmp.name)
    g = momentum_genome()
    firsts = []
    for _ in range(5):
        res = evaluate(g, panel, seed)
        _eid, is_new = store.record_eval(res)
        firsts.append(is_new)
    n = store.trial_count("crypto")
    store.close()
    try:
        os.unlink(tmp.name)
    except OSError:
        pass
    return {"is_new_flags": firsts, "trial_count": n,
            "ok": bool(firsts[0] and not any(firsts[1:]) and n == 1)}


def experiment_two_stage(seed: int = 13, k: int = 40) -> dict:
    """The two-stage protocol must be STRICTER at confirmation, not looser.

    Two things are asserted. (1) On edgeless data, the best-of-k overfit still dies — moving the
    screen to FDR must not open a hole. (2) Stage A must never read the holdout: G6 is the transfer
    gate, and if it appears in an exploration report the seal is broken (the previous design ran it
    on all 23,030 genomes, turning the 'unseen' panel into a selection surface)."""
    import statistics
    from mt.gauntlet.runner import STAGE_EXPLORE, STAGE_CONFIRM
    from mt.gauntlet.multipletest import bhy_threshold, sharpe_pvalue
    panel = make_panel(edge=False, seed=seed)
    holdout = make_panel(edge=False, seed=seed + 500)
    sampler = TemplateSampler(seed=seed)
    gauntlet = Gauntlet()
    best, best_res, best_sh, spps, pvals = None, None, -np.inf, [], []
    for _ in range(k):
        g = sampler._random("crypto")
        res = evaluate(g, panel, seed)
        if res.ok and np.isfinite(res.summary.get("net_sharpe", np.nan)):
            spp = res.summary.get("sharpe_pp")
            if spp is not None and np.isfinite(spp):
                spps.append(float(spp))
                p = sharpe_pvalue(spp, res.summary.get("n_periods"))
                if p is not None:
                    pvals.append(p)
            if res.summary["net_sharpe"] > best_sh:
                best, best_res, best_sh = g, res, res.summary["net_sharpe"]
    sigma_sr = statistics.pstdev(spps) if len(spps) >= 8 else None
    thr = bhy_threshold(pvals, q=0.10)
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel,
                          holdout_panel=holdout, seed=seed, sr_trial_std=sigma_sr,
                          fdr_threshold=thr)
    a = gauntlet.run(best, best_res, trial_count=k, ctx=ctx, stage=STAGE_EXPLORE)
    b = gauntlet.run(best, best_res, trial_count=k, ctx=ctx, stage=STAGE_CONFIRM)
    holdout_leak = "G6_transfer" in a.gates
    return {"stage_a_promoted": a.promoted, "stage_a_gate": a.failed_gate,
            "stage_b_cleared": b.cleared, "stage_b_gate": b.failed_gate,
            "fdr_threshold": thr, "holdout_leak": holdout_leak,
            "ok": bool((not b.cleared) and (not holdout_leak))}


def experiment_archive_and_book(seed: int = 14) -> dict:
    """Three structural guarantees the search depends on.

    (1) The archive must admit by behavioural NICHE, not by clearing the bar — the old pass-gated
        admission left it permanently empty, which disabled elite breeding, novelty targets and the
        G8 reference series all at once.
    (2) A book of decorrelated members must beat its best single member, and must be charged for
        the combinations examined while selecting them.
    (3) The decisive control: a book assembled from PURE NOISE must NOT look significant. If
        combining junk produced a significant portfolio, the portfolio route would just be a new
        place for selection bias to hide — this is the assertion that makes the book trustworthy
        rather than merely convenient."""
    from mt.improve.book import build_book, select_members
    T = 400
    rng = np.random.default_rng(seed)
    series = {f"g{i}": pd.Series(rng.normal(0.0006, 0.01, T)) for i in range(12)}
    members, trials = select_members(series)
    b = build_book(series, n_books_tried=0)
    gain = b.get("diversification_gain") if b else None

    # null control across several seeds — noise books must sit below the significance bar
    null_z, edge_z = [], []
    for s in range(6):
        r0 = np.random.default_rng(500 + s)
        nb = build_book({f"g{i}": pd.Series(r0.normal(0.0, 0.01, T)) for i in range(12)},
                        n_books_tried=0)
        if nb and nb["book_dsr_z"] is not None:
            null_z.append(float(nb["book_dsr_z"]))
        r1 = np.random.default_rng(900 + s)
        eb = build_book({f"g{i}": pd.Series(r1.normal(0.0006, 0.01, T)) for i in range(12)},
                        n_books_tried=0)
        if eb and eb["book_dsr_z"] is not None:
            edge_z.append(float(eb["book_dsr_z"]))
    null_ok = bool(null_z) and max(null_z) < 1.645
    edge_ok_ = bool(edge_z) and sum(1 for z in edge_z if z > 1.645) >= len(edge_z) - 1
    return {"n_members": None if not b else b["n_members"],
            "selection_trials": trials,
            "book_sharpe": None if not b else b["book_sharpe_pp"],
            "best_member": None if not b else b["best_member_sharpe_pp"], "gain": gain,
            "family_charged": None if not b else b["n_books_tried"],
            "sigma_source": None if not b else b.get("sigma_source"),
            "null_max_z": None if not null_z else round(max(null_z), 2),
            "edge_hits": f"{sum(1 for z in edge_z if z > 1.645)}/{len(edge_z)}",
            "ok": bool(b and trials > 1 and gain is not None and gain > 1.0
                       and b["n_books_tried"] > 1 and null_ok and edge_ok_)}


def experiment_minted_vocab_persists(seed: int = 15) -> dict:
    """A hall-of-fame genome built on a MINTED primitive must still typecheck after a restart.

    Minted intx_* ops used to live only in the process that created them, so on the next marathon
    every elite built on one failed `typecheck` and was silently dropped by warm-start — the
    deepest part of the search was discarded every run while best-z kept reporting its score."""
    import os, tempfile
    from mt.store import MTStore
    from mt.improve import miner as M
    from mt.genome.registry import REGISTRY
    from mt.genome.schema import FeatureNode
    # make_panel (not MarketAdapter): the self-test must run on a bare CI runner, where the
    # CC_Trading/FX_Trading roots the subprocess workers need do not exist. Every other experiment
    # here already builds its panel in-process for exactly this reason.
    panel = make_panel(edge=True, n_sym=8, bars=600, seed=seed)
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
    store = MTStore(db_path=tmp.name)
    rng = np.random.default_rng(seed)
    name = None
    for _ in range(40):
        name = M.mint_interaction(panel, rng, store=store, market="crypto")
        if name:
            break
    ok_persisted = restored = False
    if name:
        g = momentum_genome()
        g.features = [FeatureNode("f1", name, {})]
        ok_before = g.typecheck()[0]
        del REGISTRY[name]                      # simulate a fresh process
        gone = not g.typecheck()[0]
        n = M.restore_minted(store)             # what DiscoveryLoop does at startup
        restored = n >= 1
        ok_persisted = bool(ok_before and gone and g.typecheck()[0])
    store.close()
    try:
        os.unlink(tmp.name)
    except OSError:
        pass
    return {"minted": name, "restored": restored, "ok": bool(name and ok_persisted and restored)}


def experiment_failure_memory(seed: int = 16) -> dict:
    """Failures must produce AGGREGATABLE facts and a gate-specific repair.

    The old critic wrote prose: 1,123 stored lessons contained 3 distinct prescriptions, all at a
    hard-coded confidence of 0.5, and 8 of its 10 gate branches fell through to a uniform random
    mutation — so 'targeted fix' was random ~100% of the time and nothing could ever be queried."""
    import os, tempfile
    from mt.store import MTStore
    from mt.improve.critic import _targeted_fix
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
    store = MTStore(db_path=tmp.name)
    for i in range(30):
        store.record_trial_facts(f"g{i}", "crypto", ["momentum", "trend"], "cross_sectional",
                                 "all", "rank_bucket", "GS_screen", False, -1.0, 0.2 + i * 0.01)
    for i in range(30, 60):
        store.record_trial_facts(f"g{i}", "crypto", ["carry"], "cross_sectional",
                                 "all", "rank_bucket", None, True, 0.5, 3.0 + i * 0.01)
    priors = store.family_priors("crypto")
    ranked = [t for t, _n, _p, _e in priors]
    prior_ok = bool(ranked and ranked[0] == "carry")     # the productive family ranks first
    profile_ok = any(g == "GS_screen" for _t, g, _n in store.gate_profile("crypto"))

    g = momentum_genome(horizon=4)
    rng = np.random.default_rng(seed)
    fixes, labelled = {}, True
    for gate in ("G1_sanity", "G7_capacity", "G5_robustness", "G3_cpcv_pbo", "GS_screen"):
        c = _targeted_fix(g, gate, rng)
        fixes[gate] = None if c is None else c.generator
        if c is None or c.generator != "llm_critic":
            labelled = False
    # G1 = P&L concentrated in one bar → the repair must actually slow the book down
    g1_child = _targeted_fix(g, "G1_sanity", rng)
    g1_ok = bool(g1_child and g1_child.risk.args.get("horizon", 0) > g.risk.args.get("horizon", 0))
    store.close()
    try:
        os.unlink(tmp.name)
    except OSError:
        pass
    return {"family_priors": priors[:2], "prior_ok": prior_ok, "profile_ok": profile_ok,
            "fix_labels": fixes, "g1_lengthens_horizon": g1_ok,
            "ok": bool(prior_ok and profile_ok and labelled and g1_ok)}


def run(verbose: bool = True) -> dict:
    try:                                        # Windows consoles default to cp1252; the report has ✓/✗
        import sys
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    a = experiment_overfit_trap()
    b = experiment_real_edge()
    c = experiment_effective_n()
    d = experiment_directional_cpcv()
    e = experiment_gate_robustness()
    f = experiment_keff_duplicates()
    h = experiment_ledger_dedup()
    i = experiment_two_stage()
    j = experiment_archive_and_book()
    k_ = experiment_minted_vocab_persists()
    l = experiment_failure_memory()
    trap_ok = not a["passed"]                       # the overfit winner MUST be rejected
    # the real edge MUST survive the exploratory screen AND clear confirmatory significance
    edge_ok = bool(b["g4_significant"]) and bool(b["promoted"])
    # correlated trials collapse (N_eff ≪ raw) AND diverse trials do not
    neff_ok = (c["dup_neff"] <= max(3, c["dup_raw"] // 3)) and (c["div_neff"] >= c["div_raw"] // 2)
    dir_ok = bool(d["time_aligned"] and d["pbo_runs"])   # directional CPCV aligns by TIME, not position
    robust_ok = bool(e["const_reject"] and e["near_reject"] and e["dd_ok"] and e["sigma_ok"])
    keff_ok = bool(f["ok"])                         # K_eff collapses on clones, holds on diversity
    dedup_ok = bool(h["ok"])                        # a repeat evaluation charges no new trial
    stage_ok = bool(i["ok"])                        # confirmation still rejects; holdout not leaked
    book_ok = bool(j["ok"])                         # portfolio beats its best member, honestly charged
    vocab_ok = bool(k_["ok"])                       # minted primitives survive a restart
    memory_ok = bool(l["ok"])                       # failures aggregate + repairs are gate-specific
    if verbose:
        print("=" * 72)
        print(" GAUNTLET SELF-TEST — the critical go/no-go (docs/09 P2)")
        print("=" * 72)
        print(f"\n(A) Overfit trap: best-of-40 on RANDOM data looked like Sharpe {a['is_sharpe']:.2f} in-sample")
        print(f"    verdict: {'REJECTED at ' + str(a['failed_gate']) if not a['passed'] else 'ADMITTED (!!)'}"
              f"   -> {'PASS ✓ (caught the overfit)' if trap_ok else 'FAIL ✗ (let overfit through)'}")
        print(f"\n(B) Real-edge control: momentum genome on data WITH an injected edge")
        print(f"    Stage A: p={b['screen_p']} vs BHY threshold {b['fdr_threshold']} → "
              f"promoted={b['promoted']}")
        print(f"    Stage B: raw_sharpe={b['raw_sharpe']}, dsr_p={b['dsr_p']}, PBO={b['pbo']}, "
              f"full_pass={b['passed']}")
        print(f"    -> {'PASS ✓ (real edge survives the screen AND clears G4)' if edge_ok else 'FAIL ✗ (rejected a real edge)'}")
        print(f"\n(C) Effective trial count: 30 near-duplicate genomes vs 30 diverse ones")
        print(f"    duplicates: ρ̄={c['dup_rho']}  N_eff={c['dup_neff']}/{c['dup_raw']}   "
              f"diverse: ρ̄={c['div_rho']}  N_eff={c['div_neff']}/{c['div_raw']}")
        print(f"    -> {'PASS ✓ (correlated trials collapse, diverse ones do not)' if neff_ok else 'FAIL ✗'}")
        print(f"\n(D) Directional CPCV alignment: 3 variants trading on different bars → matrix {d['matrix_shape']}")
        print(f"    -> {'PASS ✓ (aligned by TIME on the union calendar, flat bars = 0)' if dir_ok else 'FAIL ✗ (position-aligned / misaligned)'}")
        print(f"\n(E) Gate robustness: (near-)constant series rejected, ruin drawdown={e['ruin_dd']}")
        print(f"    σ_SR on a ledger contaminated with degenerate Sharpes = {e['sigma_contaminated']}"
              f"   (true ≈0.22; a plain std would read ~2500 and drive every z to −∞)")
        print(f"    -> {'PASS ✓ (degenerate Sharpe rejected at G1; DD in [0,1]; σ_SR stays robust)' if robust_ok else 'FAIL ✗ (degenerate/ruin/contamination slipped through)'}")
        print(f"\n(F) K_eff vs duplication: 30 clones→{f['dup_neff']}, 30 diverse→{f['div_neff']}, "
              f"25 clones+5 diverse→{f['mixed_neff']} (truth 6)")
        print(f"    -> {'PASS ✓ (family size collapses on clones, holds on real diversity)' if keff_ok else 'FAIL ✗'}")
        print(f"\n(G) Ledger dedup: same genome evaluated 5× → trial_count={h['trial_count']}")
        print(f"    -> {'PASS ✓ (a repeat is not a new hypothesis)' if dedup_ok else 'FAIL ✗ (duplicates still inflate N)'}")
        print(f"\n(H) Two-stage protocol: overfit best-of-40 at Stage B → "
              f"{'REJECTED at ' + str(i['stage_b_gate']) if not i['stage_b_cleared'] else 'CLEARED (!!)'}; "
              f"holdout leaked into Stage A = {i['holdout_leak']}")
        print(f"    -> {'PASS ✓ (confirmation still rejects; the seal holds)' if stage_ok else 'FAIL ✗'}")
        print(f"\n(I) Archive + book: {j['n_members']} decorrelated members, "
              f"book sharpe {j['book_sharpe']} vs best single {j['best_member']} (×{j['gain']}), "
              f"charged family={j['family_charged']} from {j['selection_trials']} selection trials")
        print(f"    null control: max book-z on pure noise = {j['null_max_z']} (must be < 1.645);  "
              f"real edge detected {j['edge_hits']};  σ_SR from {j['sigma_source']}")
        print(f"    -> {'PASS ✓ (portfolio beats its best member, pays for the search, and noise stays insignificant)' if book_ok else 'FAIL ✗'}")
        print(f"\n(J) Minted vocabulary: {k_['minted']} survives a simulated restart")
        print(f"    -> {'PASS ✓ (elites built on mined primitives are not silently dropped)' if vocab_ok else 'FAIL ✗'}")
        print(f"\n(K) Failure memory: top family prior={l['family_priors'][:1]}, "
              f"G1 repair lengthens horizon={l['g1_lengthens_horizon']}")
        print(f"    -> {'PASS ✓ (failures aggregate; repairs target the failing statistic)' if memory_ok else 'FAIL ✗'}")
        ok = all([trap_ok, edge_ok, neff_ok, dir_ok, robust_ok, keff_ok, dedup_ok,
                  stage_ok, book_ok, vocab_ok, memory_ok])
        verdict = "TRUSTWORTHY" if ok else "NOT TRUSTWORTHY — DO NOT PROCEED"
        print("\n" + "=" * 72)
        print(f" RESULT: gauntlet is {verdict}")
        print("=" * 72)
    return {"trap_ok": trap_ok, "edge_ok": edge_ok, "neff_ok": neff_ok, "dir_ok": dir_ok,
            "robust_ok": robust_ok, "keff_ok": keff_ok, "dedup_ok": dedup_ok, "stage_ok": stage_ok,
            "book_ok": book_ok, "vocab_ok": vocab_ok, "memory_ok": memory_ok,
            "overfit": a, "edge": b, "neff": c, "directional": d, "robustness": e,
            "keff": f, "dedup": h, "two_stage": i, "book": j, "vocab": k_, "memory": l}


if __name__ == "__main__":
    import sys
    r = run()
    sys.exit(0 if all(r[k] for k in ("trap_ok", "edge_ok", "neff_ok", "dir_ok", "robust_ok",
                                     "keff_ok", "dedup_ok", "stage_ok", "book_ok", "vocab_ok",
                                     "memory_ok")) else 1)
