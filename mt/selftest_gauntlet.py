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
    panel = make_panel(edge=False, seed=seed)
    sampler = TemplateSampler(seed=seed)
    ctx = GauntletContext(eval_fn=lambda g, p: evaluate(g, p, seed), panel=panel, seed=seed)
    gauntlet = Gauntlet()

    best, best_res, best_sh = None, None, -np.inf
    for _ in range(k):
        g = sampler._random("crypto")
        res = evaluate(g, panel, seed)
        if res.ok and np.isfinite(res.summary.get("net_sharpe", np.nan)):
            if res.summary["net_sharpe"] > best_sh:
                best, best_res, best_sh = g, res, res.summary["net_sharpe"]

    report = gauntlet.run(best, best_res, trial_count=k, ctx=ctx)     # honest N = k tried
    return {"is_sharpe": best_sh, "passed": report.passed, "failed_gate": report.failed_gate,
            "gates": report.gates}


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


def run(verbose: bool = True) -> dict:
    a = experiment_overfit_trap()
    b = experiment_real_edge()
    trap_ok = not a["passed"]                       # the overfit winner MUST be rejected
    edge_ok = bool(b["g4_significant"])             # the real edge MUST clear significance
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
        verdict = "TRUSTWORTHY" if (trap_ok and edge_ok) else "NOT TRUSTWORTHY — DO NOT PROCEED"
        print("\n" + "=" * 72)
        print(f" RESULT: gauntlet is {verdict}")
        print("=" * 72)
    return {"trap_ok": trap_ok, "edge_ok": edge_ok, "overfit": a, "edge": b}


if __name__ == "__main__":
    import sys
    r = run()
    sys.exit(0 if (r["trap_ok"] and r["edge_ok"]) else 1)
