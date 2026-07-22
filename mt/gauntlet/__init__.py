"""mt.gauntlet — the overfitting immune system (docs/05).

Every other subsystem *produces* candidates; this one exists to *destroy* them. What
survives is not "good" — it is "not yet disproven". The thin slice enforces G1 (sanity),
G4 (Deflated Sharpe, the multiple-testing firewall, using the honest ledger trial count)
and G5 (stationary-bootstrap robustness) with CC_Trading's REAL implementations; G2/G3/
G6/G7/G8 are recorded as deferred, not silently skipped.
"""
from mt.gauntlet.runner import Gauntlet, GauntletReport, GauntletContext
from mt.gauntlet.gates import GateResult

__all__ = ["Gauntlet", "GauntletReport", "GauntletContext", "GateResult"]
