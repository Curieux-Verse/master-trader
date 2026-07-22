"""Fast, deterministic smoke tests for the thin slice (no subprocess / no network).

Fabricates a NormPanel directly so the genome→sim→gauntlet→archive path is covered in
milliseconds. The subprocess-isolation path is exercised by mt.run_demo, not here.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd
import pytest

from mt.data.panel import NormPanel
from mt.genome.schema import Genome, Meta, FeatureNode, SignalSpec, SizingSpec, RiskSpec
from mt.genome.registry import (
    REGISTRY, ops_for_stage, computable_feature_ops, register, OpSpec, ArgSpec, Pit, RegistrationError,
)
from mt.sim import features as F
from mt.genome.ops import mutate, crossover, distance
from mt.sim import Tier1Executor
from mt.gauntlet import Gauntlet
from mt.gauntlet.gates import g1_sanity, g4_deflated_sharpe
from mt.store import MTStore
from mt.archive import MapElites


def _panel(n_symbols=6, bars=200, seed=1) -> NormPanel:
    rng = np.random.default_rng(seed)
    end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    times = pd.to_datetime([end - timedelta(hours=4) * (bars - 1 - i) for i in range(bars)], utc=True)
    frames = {}
    for s in range(n_symbols):
        rets = rng.normal(0, 0.02, bars)
        close = 100 * np.exp(np.cumsum(rets))
        df = pd.DataFrame({
            "datetime": times, "open": close, "high": close * 1.01, "low": close * 0.99,
            "close": close, "volume": rng.lognormal(10, 1, bars),
            "atr_14": pd.Series(np.abs(close * 0.01)).rolling(14, min_periods=1).mean().to_numpy(),
            "funding_rate": rng.normal(0.0001, 0.0004, bars),
        })
        frames[f"SYM{s}"] = {"4h": df}
    return NormPanel(market="crypto", asof=end, snapshot_id="test",
                     symbols=list(frames), frames=frames, timeframes={"htf": "4h"})


def _genome() -> Genome:
    return Genome(
        meta=Meta(market="crypto", htf="4h"),
        features=[FeatureNode("f1", "momentum", {"lookback": 40, "skip": 1}),
                  FeatureNode("f2", "reversion", {"lookback": 3})],
        signal=SignalSpec("weighted_blend", {"direction": "neutral"}),
        sizing=SizingSpec("rank_bucket", {"top_frac": 0.2, "gross": 1.0, "per_name_cap": 0.15}),
        risk=RiskSpec("horizon_hold", {"horizon": 6, "cost_stress": 1.0}),
    )


def test_genome_hash_stable_and_roundtrips():
    g = _genome()
    assert g.genome_id == Genome.from_dict(g.to_dict()).genome_id
    ok, issues = g.typecheck()
    assert ok and not issues


def test_typecheck_rejects_bad_op():
    g = _genome()
    g.features[0].op = "not_a_real_op"
    ok, issues = g.typecheck()
    assert not ok and any("unknown" in i for i in issues)


def test_registry_sampling_is_valid():
    rng = np.random.default_rng(0)
    for op in ops_for_stage("feature"):
        args = op.sample_args(rng)
        assert set(args) == set(op.args)


def test_mutation_and_crossover_stay_valid():
    rng = np.random.default_rng(0)
    g = _genome()
    for _ in range(20):
        child = mutate(g, rng)
        assert child.typecheck()[0]
        assert child.parents == [g.genome_id]
    child2 = crossover(g, mutate(g, rng), rng)
    assert child2.typecheck()[0]
    assert 0.0 <= distance(g, child2) <= 1.0


def test_executor_produces_evalresult():
    res = Tier1Executor(seed=7).evaluate(_genome(), _panel())
    assert res.ok
    assert res.summary["n_periods"] > 0
    assert set(("hold_bucket", "turnover_bucket", "exposure_bucket")) <= set(res.behavioral_descriptor)


def test_gauntlet_rejects_noise():
    res = Tier1Executor(seed=7).evaluate(_genome(), _panel())
    report = Gauntlet().run(_genome(), res, trial_count=50)
    # random-walk data has no edge → must be rejected (immune system working)
    assert not report.passed
    assert report.failed_gate is not None


def test_g1_catches_single_period_dominance():
    net = pd.Series([0.001] * 40 + [5.0])   # one period dwarfs all others
    assert g1_sanity(net).status == "fail"


def test_g4_deflates_with_trials():
    # more trials ⇒ higher deflated p-value (harder to be significant)
    net = pd.Series(np.random.default_rng(0).normal(0.01, 0.02, 120))
    p_lax = g4_deflated_sharpe(net, trial_count=1).stats.get("dsr_pvalue")
    p_strict = g4_deflated_sharpe(net, trial_count=5000).stats.get("dsr_pvalue")
    assert p_lax is not None and p_strict is not None
    assert p_strict >= p_lax - 1e-9


def test_store_dedup_and_ledger(tmp_path):
    store = MTStore(db_path=tmp_path / "t.db")
    g = _genome()
    assert store.register_genome(g) is True
    assert store.register_genome(g) is False        # dedup by content hash
    res = Tier1Executor().evaluate(g, _panel())
    store.record_eval(res)
    assert store.trial_count() == 1
    store.close()


def test_archive_occupy_replace_keep(tmp_path):
    store = MTStore(db_path=tmp_path / "t.db")
    assert store.upsert_archive("n1", "a", "crypto", {}, {}, scalar_fit=1.0) == "occupy"
    assert store.upsert_archive("n1", "b", "crypto", {}, {}, scalar_fit=2.0) == "replace"
    assert store.upsert_archive("n1", "c", "crypto", {}, {}, scalar_fit=0.5) == "keep"
    store.close()


def test_every_computable_feature_has_a_builder():
    # the contract's promise: computable=True ⇒ mt.sim.features can actually compute it
    for op in computable_feature_ops():
        assert op.name in F.BUILDERS, f"{op.name} marked computable but has no builder"


def test_registration_gate_rejects_leaky_and_unbounded():
    with pytest.raises(RegistrationError):
        register(OpSpec("leaky_op", "feature", {}, pit=Pit(uses_future=True)))
    with pytest.raises(RegistrationError):
        register(OpSpec("unbounded_op", "feature", {"w": ArgSpec("float", 1.0, 1.0)}))
    with pytest.raises(RegistrationError):
        register(OpSpec("mistyped_op", "feature", {}, output="NotAType"))


def test_amt_primitives_flow_through_executor():
    # Auction Market Theory proxies must compute and drive a real backtest end-to-end
    g = Genome(
        meta=Meta(market="crypto", htf="4h"),
        features=[FeatureNode("f1", "dist_to_poc", {"window": 60}),
                  FeatureNode("f2", "cumulative_delta", {"window": 48}),
                  FeatureNode("f3", "value_area_position", {"window": 60})],
        signal=SignalSpec("weighted_blend", {"direction": "neutral"}),
        sizing=SizingSpec("rank_bucket", {"top_frac": 0.2, "gross": 1.0, "per_name_cap": 0.15}),
        risk=RiskSpec("horizon_hold", {"horizon": 6, "cost_stress": 1.0}),
    )
    assert g.typecheck()[0]
    res = Tier1Executor(seed=7).evaluate(g, _panel())
    assert res.ok and res.summary["n_periods"] > 0


def test_data_gated_primitives_wired_but_not_sampled():
    from mt.generators.templates import TemplateSampler
    ops_used = set()
    for g in TemplateSampler(seed=1).sample("crypto", n_random=20):
        ops_used.update(f.op for f in g.features)
    # footprint is fully wired (computable, has a builder) but data-gated on `trades`
    # (not in default feeds) → never wired into a genome until aggTrades are ingested
    assert "stacked_imbalance" not in ops_used and "absorption" not in ops_used
    assert REGISTRY["stacked_imbalance"].computable is True
    assert "trades" in REGISTRY["stacked_imbalance"].data_requires


def test_gauntlet_is_trustworthy():
    # the critical go/no-go (docs/09 P2): catches an overfit AND admits a real edge
    from mt.selftest_gauntlet import run
    r = run(verbose=False)
    assert r["trap_ok"], "gauntlet failed to catch a deliberately-overfit strategy"
    assert r["edge_ok"], "gauntlet rejected a genuine injected edge"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
