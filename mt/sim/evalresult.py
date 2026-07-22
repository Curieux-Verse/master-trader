"""mt.sim.evalresult — the standard evaluation contract (simulator → gauntlet → archive).

Every genome, at every fidelity and from every generator, speaks this one shape so the
gauntlet and archive treat them uniformly (docs/04 §5). The `net_returns` series is the
canonical, post-cost object the whole validation stack consumes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


@dataclass
class EvalResult:
    genome_id: str
    market: str
    fidelity: str = "tier1"
    seed: int = 4242
    snapshot_id: str = ""
    net_returns: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))
    turnover: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))
    summary: Dict = field(default_factory=dict)
    behavioral_descriptor: Dict = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and not self.net_returns.empty

    def descriptor_vector(self) -> List:
        d = self.behavioral_descriptor
        return [d.get("hold_bucket"), d.get("turnover_bucket"), d.get("exposure_bucket")]

    def to_ledger_row(self) -> dict:
        return {
            "genome_id": self.genome_id,
            "market": self.market,
            "fidelity": self.fidelity,
            "seed": self.seed,
            "snapshot_id": self.snapshot_id,
            "n_periods": int(self.summary.get("n_periods", 0)),
            "net_sharpe": _f(self.summary.get("net_sharpe")),
            "sharpe_pp": _f(self.summary.get("sharpe_pp")),
            "ann_return": _f(self.summary.get("ann_return")),
            "max_dd": _f(self.summary.get("max_dd")),
            "hit_rate": _f(self.summary.get("hit_rate")),
            "avg_turnover": _f(self.summary.get("avg_turnover")),
            "error": self.error or "",
        }


def _f(v):
    try:
        v = float(v)
        return v if np.isfinite(v) else None
    except (TypeError, ValueError):
        return None
