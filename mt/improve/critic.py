"""mt.improve.critic — the reflective critic (Engine B, docs/06 §3, reworked in docs/15 §3).

Given a finished gauntlet verdict it writes a structured, QUANTIFIED post-mortem and proposes a
mutation that addresses the specific statistic that failed — closing the analyze→tweak→re-test
loop the requirement asks for.

What changed, and why it mattered:

  • **It now receives evidence.** The old critic saw only `report.failed_gate` and the genome's
    family tags, so 76% of all failures collapsed into one undifferentiated bucket. Across 1,123
    stored lessons the entire library contained THREE distinct prescriptions, every one at a
    hard-coded confidence of 0.5. It now reads the failing gate's actual statistics plus the
    store's measured feature attribution and family priors.

  • **The fixes are real fixes.** Previously eight of the ten gate branches fell through to
    `mutate(genome, rng)` — a uniform random single-node perturbation, i.e. exactly what blind
    evolution already does. Only G3 and G7 had targeted repairs, and those two gates fired 2 and 0
    times in 23,030 genomes, so in practice the "targeted fix" was random ~100% of the time. Every
    gate that actually fires now has a repair aimed at the statistic that killed the candidate.

  • **Children are labelled honestly.** `_targeted_fix` used to build a child tagged `llm_critic`
    and then discard it in favour of `mutate()`'s `evo_mutate` child on most paths, so critic work
    was invisible in the ledger and the engine bandit could never learn whether it was working.
"""
from __future__ import annotations

import copy
import json
from typing import Dict, List, Optional

import numpy as np

from mt.genome.registry import REGISTRY
from mt.genome.schema import Genome
from mt.genome.ops import mutate, novelty_mutate

# gate → (what the failure means, the repair that addresses it)
GATE_LESSONS = {
    "G0_eval": ("did not produce a valid backtest", "simplify — drop a feature the data can't serve"),
    "G1_sanity": ("degenerate P&L — too few trades, or one bar dominates the result",
                  "spread the book: hold longer and cap per-name weight"),
    "GS_screen": ("raw predictive strength too weak to clear the FDR screen",
                  "add an orthogonal, measurably-contributing feature"),
    "G4_deflated_sharpe": ("edge indistinguishable from luck after trial correction",
                           "signal too weak — combine an orthogonal family or drop it"),
    "G4b_reality_check": ("Sharpe not significant under block resampling — a few lucky runs",
                          "lengthen the holding horizon so P&L is not block-concentrated"),
    "G5_robustness": ("tail drawdown too large under bootstrap", "cut gross and cap per-name size"),
    "G2_oos": ("shines in-sample, decays out-of-sample", "add a regime filter or simplify"),
    "G7_capacity": ("edge evaporates under 2× costs — turnover too high", "lengthen the holding horizon"),
    "G8_orthogonality": ("duplicates an existing archive member", "explore a different family/niche"),
    "G3_cpcv_pbo": ("parameter tuning is overfit (high PBO)", "reduce complexity / prefer parameter plateaus"),
    "G6_transfer": ("does not transfer to held-out data", "likely data-mined; demand an economic rationale"),
}

_EVIDENCE_KEYS = ("dsr_z", "raw_sharpe", "dsr_pvalue", "p_single", "edge_t", "fdr_threshold",
                  "pbo", "max_dd_95", "sharpe_2x_cost", "max_corr", "single_period_share",
                  "n_periods", "oos_mean", "is_mean", "holdout_sharpe", "p_fwer")


def families(genome: Genome) -> List[str]:
    tags: set = set()
    for f in genome.features:
        spec = REGISTRY.get(f.op)
        if spec:
            tags.update(t for t in spec.tags if t not in ("classical_ta",))
    return sorted(tags) or ["mixed"]


def _evidence(report, gate: str) -> Dict:
    """The numbers that actually decided the verdict — the critic reasons over these, not vibes."""
    stats = report.gates.get(gate, {}) or {}
    out = {k: stats[k] for k in _EVIDENCE_KEYS if k in stats and stats[k] is not None}
    gs = report.gates.get("GS_screen", {}) or {}
    if "edge_t" in gs and gs["edge_t"] is not None:
        out.setdefault("edge_t", gs["edge_t"])
    return out


def _confidence(report, gate: str) -> float:
    """How strongly the evidence supports the diagnosis, instead of a hard-coded 0.5.

    Anchored on how far the deciding statistic sat from its threshold: a candidate that missed by
    a hair teaches something different from one that missed by a mile, and the lesson library was
    unable to express that distinction at all."""
    ev = _evidence(report, gate)
    if gate == "GS_screen" and ev.get("p_single") is not None and ev.get("fdr_threshold"):
        ratio = float(ev["p_single"]) / max(1e-9, float(ev["fdr_threshold"]))
        return round(float(np.clip(0.35 + 0.15 * np.log10(max(ratio, 1e-3)), 0.3, 0.95)), 2)
    if gate == "G4_deflated_sharpe" and ev.get("dsr_z") is not None:
        return round(float(np.clip(0.5 + 0.25 * abs(float(ev["dsr_z"])) / 1.645, 0.3, 0.95)), 2)
    if gate == "G1_sanity" and ev.get("single_period_share") is not None:
        return round(float(np.clip(float(ev["single_period_share"]), 0.3, 0.95)), 2)
    if gate == "G3_cpcv_pbo" and ev.get("pbo") is not None:
        return round(float(np.clip(float(ev["pbo"]), 0.3, 0.95)), 2)
    # Fallback on edge_t, which is ALWAYS available and never None. Without this the common case —
    # a screen failure while no BHY discovery exists in the batch, so `fdr_threshold` is None —
    # fell through to a constant 0.5, which is how the old library ended up with a single
    # confidence value across all 1,123 entries. "Nowhere near" and "missed by a hair" have to be
    # distinguishable or the field carries no information.
    if ev.get("edge_t") is not None:
        return round(float(np.clip(0.30 + 0.30 * abs(float(ev["edge_t"])) / 1.645, 0.3, 0.95)), 2)
    return 0.5


def critique(genome: Genome, report, res, store, rng: np.random.Generator,
             use_ollama: bool = False, op_weights: Optional[Dict] = None,
             avoid: Optional[List[Genome]] = None) -> Dict:
    fam = families(genome)
    if report.passed:
        stage = "promoted to the candidate pool" if report.promoted else "cleared confirmation"
        lesson = {
            "exploits": fam, "breaks_when": "regime change / edge decay",
            "single_fix": "hold in the archive and re-challenge on the sealed holdout",
            "general_lesson": f"{'+'.join(fam)} on a {genome.meta.execution} book {stage}",
            "confidence": 0.6, "gate": "PASS", "evidence": _evidence(report, "GS_screen"),
        }
        fix = None
    else:
        gate = report.failed_gate or "unknown"
        breaks_when, fixhint = GATE_LESSONS.get(gate, ("failed a gate", "revise the hypothesis"))
        ev = _evidence(report, gate)
        ev_txt = ", ".join(f"{k}={v}" for k, v in list(ev.items())[:4])
        lesson = {
            "exploits": fam, "breaks_when": breaks_when, "single_fix": fixhint,
            "general_lesson": f"{'+'.join(fam)} ({genome.meta.execution}) — {breaks_when}"
                              + (f" [{ev_txt}]" if ev_txt else ""),
            "confidence": _confidence(report, gate), "gate": gate, "evidence": ev,
        }
        fix = _targeted_fix(genome, gate, rng, report, op_weights=op_weights, avoid=avoid)

    if use_ollama:
        refined = _ollama_refine(lesson)
        if refined:
            lesson = refined

    store.add_lesson(json.dumps(lesson, sort_keys=True), tags=lesson["gate"])
    return {"lesson": lesson, "suggested_mutation": fix}


def _child_of(genome: Genome) -> Genome:
    child = copy.deepcopy(genome)
    child.generator = "llm_critic"
    child.parents = [genome.genome_id]
    child.generation = genome.generation + 1
    return child


def _targeted_fix(genome: Genome, gate: str, rng: np.random.Generator, report=None,
                  op_weights: Optional[Dict] = None,
                  avoid: Optional[List[Genome]] = None) -> Optional[Genome]:
    """One concrete repair aimed at the statistic that failed.

    Every branch that returns a hand-built child labels it `llm_critic` so the bandit can learn
    whether directed repair beats blind mutation. Branches that genuinely need a structural change
    delegate to `novelty_mutate`, which at least steers AWAY from what the archive already holds
    instead of perturbing at random."""
    avoid = list(avoid or [])
    try:
        if gate == "G1_sanity":
            # P&L concentrated in one bar, or too few trades. Both are fixed by making the book
            # wider and slower. This is the gate that killed the single best candidate the system
            # has ever produced (z=+1.96, net sharpe 12.82 from essentially one bar) — and the old
            # critic answered it with a random perturbation.
            child = _child_of(genome)
            if child.risk.op == "horizon_hold":
                child.risk.args["horizon"] = min(48, int(child.risk.args.get("horizon", 6) * 2) + 2)
            elif child.risk.op == "triple_barrier":
                child.risk.args["max_bars"] = min(48, int(child.risk.args.get("max_bars", 16) * 2) + 2)
            if child.sizing.op == "rank_bucket":
                child.sizing.args["top_frac"] = float(min(0.6, child.sizing.args.get("top_frac", 0.2) * 1.8))
                child.sizing.args["per_name_cap"] = float(min(0.25, child.sizing.args.get("per_name_cap", 0.15)))
            return child
        if gate in ("G7_capacity", "G4b_reality_check"):     # turnover / block-concentrated P&L
            child = _child_of(genome)
            if child.risk.op == "horizon_hold":
                child.risk.args["horizon"] = min(48, int(child.risk.args.get("horizon", 6) * 1.7) + 1)
            elif child.risk.op == "triple_barrier":
                child.risk.args["max_bars"] = min(48, int(child.risk.args.get("max_bars", 16) * 1.6) + 1)
            return child
        if gate == "G5_robustness":                          # tail drawdown → cut risk
            child = _child_of(genome)
            if child.sizing.op == "rank_bucket":
                child.sizing.args["gross"] = float(max(0.3, child.sizing.args.get("gross", 1.0) * 0.6))
                child.sizing.args["per_name_cap"] = float(max(0.03, child.sizing.args.get("per_name_cap", 0.15) * 0.6))
            return child
        if gate in ("G3_cpcv_pbo", "G0_eval") and len(genome.features) > 1:   # overfit / invalid → simplify
            child = _child_of(genome)
            del child.features[int(rng.integers(len(child.features)))]
            return child
        if gate == "G2_oos":                                 # unstable → condition on regime
            child = _child_of(genome)
            spec = REGISTRY.get(child.signal.op)
            if spec and "regime" in spec.args:
                child.signal.args["regime"] = spec.args["regime"].sample(rng)
                return child
            return _critic_mutate(genome, rng, avoid, op_weights)
        if gate in ("GS_screen", "G4_deflated_sharpe"):
            # Too weak. Add a primitive with MEASURED contribution rather than a random one — this
            # is where the attribution table earns its keep.
            child = _child_of(genome)
            from mt.genome.ops import _feature_ops_for, _pick_op, _new_feature_id
            from mt.genome.schema import FeatureNode
            have = {f.op for f in child.features}
            pool = [o for o in _feature_ops_for(child.meta.market) if o.name not in have]
            if pool and len(child.features) < 6:
                op = _pick_op(pool, rng, op_weights)
                child.features.append(FeatureNode(_new_feature_id(child.features), op.name,
                                                  op.sample_args(rng)))
                return child
            return _critic_mutate(genome, rng, avoid, op_weights)
        if gate == "G8_orthogonality":                       # duplicate → move away structurally
            return _critic_mutate(genome, rng, avoid, op_weights)
    except Exception:
        pass
    return _critic_mutate(genome, rng, avoid, op_weights)


def _critic_mutate(genome: Genome, rng: np.random.Generator, avoid: List[Genome],
                   op_weights: Optional[Dict]) -> Genome:
    """Structural repair, but ATTRIBUTED to the critic.

    `novelty_mutate` stamps its output `evo_mutate`; leaving that in place is how the critic's
    work became invisible — the production report showed the `llm` engine having produced 1 genome
    out of 23,030 because only two rarely-reached gate branches ever returned a labelled child.
    Re-stamping means the bandit's reward signal and the population report finally attribute
    directed repair to the engine that performed it."""
    child = novelty_mutate(genome, rng, avoid, op_weights=op_weights)
    child.generator = "llm_critic"
    child.parents = [genome.genome_id]
    child.generation = genome.generation + 1
    return child


def _ollama_refine(lesson: Dict, model: str = "qwen2.5:3b", timeout: float = 20.0) -> Optional[Dict]:
    """Best-effort local-LLM refinement (free, offline). Silent fallback if unavailable."""
    try:
        import subprocess
        prompt = ("Rewrite as one crisp, adversarial trading-desk lesson (<=30 words), no preamble:\n"
                  + lesson["general_lesson"])
        out = subprocess.run(["ollama", "run", model], input=prompt,
                             capture_output=True, text=True, timeout=timeout)
        text = (out.stdout or "").strip()
        if text:
            refined = dict(lesson)
            refined["general_lesson"] = text[:300]
            refined["source"] = "ollama"
            return refined
    except Exception:
        return None
    return None
