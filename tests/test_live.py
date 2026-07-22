"""Fast, deterministic tests for the live/paper adaptation layer (Phase E)."""
from __future__ import annotations

from mt.live.allocator import HedgeAllocator
from mt.live.drift import PageHinkley, DriftMonitor, probabilistic_sharpe_ratio, circuit_breaker


def test_page_hinkley_detects_downward_drift():
    ph = PageHinkley(delta=0.001, lam=0.03)
    changed = False
    for x in [0.01] * 25 + [-0.05] * 25:
        changed = ph.update(x) or changed
    assert changed


def test_allocator_normalizes_and_favors_winners():
    a = HedgeAllocator(["x", "y"], eta=3.0)
    for _ in range(5):
        a.update({"x": 0.02, "y": -0.02})
    w = a.weights()
    assert abs(sum(w.values()) - 1.0) < 1e-9
    assert w["x"] > w["y"]


def test_allocator_drop_and_throttle():
    a = HedgeAllocator(["x", "y", "z"])
    a.drop("z")
    assert a.weights()["z"] == 0.0
    before = a.weights()["x"]
    a.throttle("x", 0.5)
    assert a.weights()["x"] < before


def test_psr_discriminates():
    import numpy as np
    rng = np.random.default_rng(0)
    assert probabilistic_sharpe_ratio(list(rng.normal(0.01, 0.004, 60))) > 0.9
    assert probabilistic_sharpe_ratio(list(rng.normal(-0.01, 0.004, 60))) < 0.1


def test_circuit_breaker_halts_on_drawdown():
    assert circuit_breaker([1.0, 1.1, 1.2, 0.8]) == "halt"     # >25% DD from peak
    assert circuit_breaker([1.0, 1.001, 1.002]) == "ok"


def test_drift_monitor_quarantines_on_collapse():
    mon = DriftMonitor(backtest_sr_pp=0.4)
    resp = "ok"
    for x in [0.01] * 12 + [-0.08] * 12:
        resp = mon.update(x)
    assert mon.quarantined
