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
    panel = make_panel(edge=True, seed=seed)
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel, seed=seed)
    gauntlet = Gauntlet()
    g = momentum_genome()
    res = evaluate(g, panel, seed)
    report = gauntlet.run(g, res, trial_count=3, ctx=ctx)            # small honest N
    g4 = report.gates.get("G4_deflated_sharpe", {})
    return {"is_sharpe": res.summary.get("net_sharpe"), "passed": report.passed,
            "failed_gate": report.failed_gate, "g4_significant": g4.get("is_significant"),
            "raw_sharpe": g4.get("raw_sharpe"), "dsr_p": g4.get("dsr_pvalue"),
            "pbo": report.gates.get("G3_cpcv_pbo", {}).get("pbo")}


def experiment_effective_n(seed: int = 5, k: int = 30) -> dict:
    """EFFECTIVE trial count: a family of near-duplicate genomes must collapse to ≈1 independent
    trial, while a diverse set must stay near k — else the Deflated Sharpe over-deflates on the
    correlated genomes it actually generates (López de Prado, DSR Appendix 3)."""
    import os
    import tempfile
    from mt.store import MTStore
    panel = make_panel(edge=True, n_sym=8, bars=600, seed=seed)
    rng = np.random.default_rng(seed)
    ops = ["momentum", "rsi", "breakout", "macd", "bb_position", "obv", "cci", "adx"]

    def build(dupe: bool) -> tuple:
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False); tmp.close()
        store = MTStore(db_path=tmp.name)
        for i in range(k):
            if dupe:
                g = momentum_genome(lookback=20 + int(rng.integers(-2, 3)), horizon=2)
            else:
                g = Genome(Meta(market="crypto", htf="4h"), [FeatureNode("f1", ops[i % len(ops)], {})],
                           SignalSpec("weighted_blend", {"direction": ("long_bias", "short_bias", "neutral")[i % 3]}),
                           SizingSpec("rank_bucket", {"top_frac": 0.2, "gross": 1.0, "per_name_cap": 0.15}),
                           RiskSpec("horizon_hold", {"horizon": 2 + i % 6, "cost_stress": 1.0}))
            store.record_eval(evaluate(g, panel, seed))
        out = (store.trial_count("crypto"), store.avg_trial_corr("crypto"), store.effective_trial_count("crypto"))
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
    trap_ok = not a["passed"]                       # the overfit winner MUST be rejected
    edge_ok = bool(b["g4_significant"])             # the real edge MUST clear significance
    # correlated trials collapse (N_eff ≪ raw) AND diverse trials do not
    neff_ok = (c["dup_neff"] <= max(3, c["dup_raw"] // 3)) and (c["div_neff"] >= c["div_raw"] // 2)
    dir_ok = bool(d["time_aligned"] and d["pbo_runs"])   # directional CPCV aligns by TIME, not position
    if verbose:
        print("=" * 72)
        print(" GAUNTLET SELF-TEST — the critical go/no-go (docs/09 P2)")
        print("=" * 72)
        print(f"\n(A) Overfit trap: best-of-40 on RANDOM data looked like Sharpe {a['is_sharpe']:.2f} in-sample")
        print(f"    verdict: {'REJECTED at ' + str(a['failed_gate']) if not a['passed'] else 'ADMITTED (!!)'}"
              f"   -> {'PASS ✓ (caught the overfit)' if trap_ok else 'FAIL ✗ (let overfit through)'}")
        print(f"\n(B) Real-edge control: momentum genome on data WITH an injected edge")
        print(f"    raw_sharpe={b['raw_sharpe']}, dsr_p={b['dsr_p']}, PBO={b['pbo']}, "
              f"full_pass={b['passed']}")
        print(f"    -> {'PASS ✓ (admitted the real edge at G4)' if edge_ok else 'FAIL ✗ (rejected a real edge)'}")
        print(f"\n(C) Effective trial count: 30 near-duplicate genomes vs 30 diverse ones")
        print(f"    duplicates: ρ̄={c['dup_rho']}  N_eff={c['dup_neff']}/{c['dup_raw']}   "
              f"diverse: ρ̄={c['div_rho']}  N_eff={c['div_neff']}/{c['div_raw']}")
        print(f"    -> {'PASS ✓ (correlated trials collapse, diverse ones do not)' if neff_ok else 'FAIL ✗'}")
        print(f"\n(D) Directional CPCV alignment: 3 variants trading on different bars → matrix {d['matrix_shape']}")
        print(f"    -> {'PASS ✓ (aligned by TIME on the union calendar, flat bars = 0)' if dir_ok else 'FAIL ✗ (position-aligned / misaligned)'}")
        ok = trap_ok and edge_ok and neff_ok and dir_ok
        verdict = "TRUSTWORTHY" if ok else "NOT TRUSTWORTHY — DO NOT PROCEED"
        print("\n" + "=" * 72)
        print(f" RESULT: gauntlet is {verdict}")
        print("=" * 72)
    return {"trap_ok": trap_ok, "edge_ok": edge_ok, "neff_ok": neff_ok, "dir_ok": dir_ok,
            "overfit": a, "edge": b, "neff": c, "directional": d}


if __name__ == "__main__":
    import sys
    r = run()
    sys.exit(0 if (r["trap_ok"] and r["edge_ok"] and r["neff_ok"] and r["dir_ok"]) else 1)
