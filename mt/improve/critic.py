"""mt.improve.critic — the reflective critic (Engine B, docs/06 §3).

Attribution first, opinion second: given a finished gauntlet verdict, it writes a structured
post-mortem (exploits / breaks_when / single_fix / general_lesson / confidence), appends it
to the Lesson Library, and proposes ONE targeted mutation implementing the fix — closing the
analyze→tweak→re-test loop. Adversarial by role: its job is to find *why this will fail
live*, not to celebrate the backtest. Runs on a deterministic heuristic by default (free,
reproducible); an optional local ollama pass refines the prose when available.
"""
from __future__ import annotations

import copy
import json
from typing import Dict, List, Optional

import numpy as np

from mt.genome.registry import REGISTRY
from mt.genome.schema import Genome
from mt.genome.ops import mutate

# gate → (what it means, how to fix it)
GATE_LESSONS = {
    "G0_eval": ("did not produce a valid backtest", "check data sufficiency / feature validity"),
    "G1_sanity": ("degenerate or too few trades", "loosen entry threshold or lengthen the sample"),
    "G4_deflated_sharpe": ("edge indistinguishable from luck after trial correction",
                           "signal too weak — combine an orthogonal family or drop it"),
    "G5_robustness": ("tail drawdown too large under bootstrap", "add a stop / vol-target / cut gross"),
    "G2_oos": ("shines in-sample, decays out-of-sample", "add a regime filter or simplify"),
    "G7_capacity": ("edge evaporates under 2× costs — turnover too high", "lengthen the holding horizon"),
    "G8_orthogonality": ("duplicates an existing archive member", "explore a different family/niche"),
    "G3_cpcv_pbo": ("parameter tuning is overfit (high PBO)", "reduce complexity / prefer parameter plateaus"),
    "G6_transfer": ("does not transfer to held-out data", "likely data-mined; demand an economic rationale"),
}


def families(genome: Genome) -> List[str]:
    tags: set = set()
    for f in genome.features:
        spec = REGISTRY.get(f.op)
        if spec:
            tags.update(t for t in spec.tags if t not in ("classical_ta",))
    return sorted(tags) or ["mixed"]


def critique(genome: Genome, report, res, store, rng: np.random.Generator,
             use_ollama: bool = False) -> Dict:
    fam = families(genome)
    if report.passed:
        lesson = {
            "exploits": fam, "breaks_when": "regime change / edge decay",
            "single_fix": "promote to paper and monitor drift",
            "general_lesson": f"{'+'.join(fam)} on a {genome.meta.execution} book cleared the full gauntlet — a candidate edge",
            "confidence": 0.6, "gate": "PASS",
        }
        fix = None
    else:
        gate = report.failed_gate or "unknown"
        breaks_when, fixhint = GATE_LESSONS.get(gate, ("failed a gate", "revise the hypothesis"))
        lesson = {
            "exploits": fam, "breaks_when": breaks_when, "single_fix": fixhint,
            "general_lesson": f"{'+'.join(fam)} ({genome.meta.execution}) — {breaks_when}",
            "confidence": 0.5, "gate": gate,
        }
        fix = _targeted_fix(genome, gate, rng)

    if use_ollama:
        refined = _ollama_refine(lesson)
        if refined:
            lesson = refined

    store.add_lesson(json.dumps(lesson, sort_keys=True), tags=lesson["gate"])
    return {"lesson": lesson, "suggested_mutation": fix}


def _targeted_fix(genome: Genome, gate: str, rng: np.random.Generator) -> Optional[Genome]:
    child = copy.deepcopy(genome)
    child.generator = "llm_critic"
    child.parents = [genome.genome_id]
    child.generation = genome.generation + 1
    try:
        if gate == "G7_capacity":                       # too much turnover → hold longer
            if child.risk.op == "horizon_hold":
                child.risk.args["horizon"] = min(48, int(child.risk.args.get("horizon", 6) * 1.7) + 1)
            elif child.risk.op == "triple_barrier":
                child.risk.args["max_bars"] = min(48, int(child.risk.args.get("max_bars", 16) * 1.6) + 1)
            return child
        if gate == "G3_cpcv_pbo" and len(child.features) > 1:   # overfit tuning → simplify
            del child.features[int(rng.integers(len(child.features)))]
            return child
        if gate in ("G8_orthogonality", "G2_oos"):      # duplicate/unstable → swap a family in
            return mutate(genome, rng)
        if gate == "G4_deflated_sharpe":                # weak → add an orthogonal feature
            return mutate(genome, rng)
    except Exception:
        pass
    return mutate(genome, rng)


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
