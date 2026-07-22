"""Phase G — end-to-end smoke: discovery loop + paper book + report (no workers, fast-ish)."""
from __future__ import annotations

from mt.store import MTStore
from mt.improve import DiscoveryLoop
from mt.live import PaperBook
from mt.live.report import format_system_report
from mt.selftest_gauntlet import make_panel


def test_full_loop_discovers_and_papers(tmp_path):
    panel = make_panel(edge=True, n_sym=6, bars=320, seed=3)
    holdout = make_panel(edge=True, n_sym=6, bars=320, seed=4)
    live = make_panel(edge=True, n_sym=6, bars=320, seed=5)

    store = MTStore(db_path=tmp_path / "s.db")
    loop = DiscoveryLoop(store, "crypto", panel, holdout, seed=3)
    st = None
    for _ in range(2):
        st = loop.run_generation(batch_size=8)

    # the loop actually ran the whole pipeline
    assert store.trial_count() >= 8
    assert store.genome_count() >= 1
    assert len(st["families_tested"]) >= 3          # breadth: many families tested
    assert set(st["bandit_weights"]) == {"template", "random", "evo", "miner", "llm"}

    # promote whatever cleared the gauntlet → paper (exercise the outer loop if non-empty)
    rows = store.archive_rows()
    elites = [(store.get_genome(r["genome_id"]), store.genome_sharpe_pp(r["genome_id"])) for r in rows]
    if elites:
        pr = PaperBook("crypto", elites, seed=3).run(live, n_days=8)
        assert "daily" in pr and len(pr["daily"]) >= 1
        assert "live_vs_backtest" in pr

    rep = {
        "markets": ["crypto"],
        "discovery": {"generations": 2, "evaluated": store.trial_count(), "admitted": len(rows),
                      "rejected": 0, "reject_rate": 0.0, "n_families": len(st["families_tested"]),
                      "phenotypes": st["phenotypes_tested"], "bandit": st["bandit_weights"]},
        "archive": {"coverage": len(rows), "elites": []}, "paper": {},
        "lessons": store.lesson_count(), "recent_lessons": [],
    }
    assert "MASTER TRADER" in format_system_report(rep)
    store.close()
