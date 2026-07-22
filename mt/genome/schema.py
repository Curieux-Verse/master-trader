"""mt.genome.schema — the typed genome and its canonical content hash.

The genome hash is SHA-256 over the canonicalized *body* only (meta+features+signal+
sizing+risk) — deliberately excluding lineage/generator — so two engines that invent the
same idea dedup to one ledger entry (docs/02 §5, docs/01 §5). Floats are rounded before
hashing so structurally-identical genomes are byte-identical.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from mt.genome.registry import REGISTRY

_FLOAT_NDIGITS = 6


def _round(obj):
    if isinstance(obj, float):
        return round(obj, _FLOAT_NDIGITS)
    if isinstance(obj, dict):
        return {k: _round(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round(v) for v in obj]
    return obj


@dataclass
class Meta:
    market: str
    htf: str
    mtf: str = ""
    ltf: str = ""
    rebalance: str = ""
    cost_profile: str = "default"
    execution: str = "cross_sectional"   # "cross_sectional" (rank book) | "directional" (per-symbol)

    def to_dict(self) -> dict:
        return {"market": self.market, "htf": self.htf, "mtf": self.mtf, "ltf": self.ltf,
                "rebalance": self.rebalance, "cost_profile": self.cost_profile, "execution": self.execution}


@dataclass
class FeatureNode:
    id: str
    op: str
    args: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"id": self.id, "op": self.op, "args": self.args}


@dataclass
class SignalSpec:
    op: str
    args: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"op": self.op, "args": self.args}


@dataclass
class SizingSpec:
    op: str
    args: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"op": self.op, "args": self.args}


@dataclass
class RiskSpec:
    op: str
    args: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"op": self.op, "args": self.args}


@dataclass
class Genome:
    meta: Meta
    features: List[FeatureNode]
    signal: SignalSpec
    sizing: SizingSpec
    risk: RiskSpec
    generator: str = "template"
    parents: List[str] = field(default_factory=list)
    generation: int = 0

    # ─── canonical body + hash ───────────────────────────────────────────
    def body(self) -> dict:
        return _round({
            "meta": self.meta.to_dict(),
            "features": [f.to_dict() for f in self.features],
            "signal": self.signal.to_dict(),
            "sizing": self.sizing.to_dict(),
            "risk": self.risk.to_dict(),
        })

    @property
    def genome_id(self) -> str:
        canonical = json.dumps(self.body(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]

    def complexity(self) -> int:
        """Node count — the Occam axis / overfitting penalty (docs/02 §7)."""
        return len(self.features) + 3  # features + signal + sizing + risk

    # ─── serialization ───────────────────────────────────────────────────
    def to_dict(self) -> dict:
        d = self.body()
        d.update({"genome_id": self.genome_id, "generator": self.generator,
                  "parents": list(self.parents), "generation": self.generation})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Genome":
        return cls(
            meta=Meta(**d["meta"]),
            features=[FeatureNode(**f) for f in d["features"]],
            signal=SignalSpec(**d["signal"]),
            sizing=SizingSpec(**d["sizing"]),
            risk=RiskSpec(**d["risk"]),
            generator=d.get("generator", "template"),
            parents=list(d.get("parents", [])),
            generation=int(d.get("generation", 0)),
        )

    # ─── validation (the pre-sim gate) ───────────────────────────────────
    def typecheck(self) -> Tuple[bool, List[str]]:
        issues: List[str] = []
        if not self.features:
            issues.append("no feature nodes")
        for f in self.features:
            spec = REGISTRY.get(f.op)
            if spec is None:
                issues.append(f"unknown feature op {f.op!r}")
            elif spec.stage != "feature":
                issues.append(f"op {f.op!r} is not a feature op")
        for stage, node in (("signal", self.signal), ("sizing", self.sizing), ("risk", self.risk)):
            spec = REGISTRY.get(node.op)
            if spec is None:
                issues.append(f"unknown {stage} op {node.op!r}")
            elif spec.stage != stage:
                issues.append(f"op {node.op!r} is not a {stage} op")
        # data-requirement check (e.g. funding features on a non-funding market)
        return (len(issues) == 0), issues

    def data_warnings(self, has_funding: bool) -> List[str]:
        """Non-fatal: features whose data the market lacks contribute nothing."""
        warns = []
        for f in self.features:
            spec = REGISTRY.get(f.op)
            if spec and "funding_rate" in spec.needs and not has_funding:
                warns.append(f"{f.op}: market has no funding_rate; feature will be inert")
        return warns

    # ─── human/LLM-readable description ───────────────────────────────────
    def to_prose(self) -> str:
        feat = "; ".join(
            f"{f.op}(" + ", ".join(f"{k}={v}" for k, v in f.args.items()) + ")"
            for f in self.features
        )
        direction = self.signal.args.get("direction", "neutral")
        lines = [
            f"[{self.meta.market}] {self.signal.op} ({direction}) on {self.meta.htf}",
            f"  features: {feat or '(none)'}",
            f"  sizing:   {self.sizing.op}(" +
            ", ".join(f"{k}={v}" for k, v in self.sizing.args.items()) + ")",
            f"  risk:     {self.risk.op}(" +
            ", ".join(f"{k}={v}" for k, v in self.risk.args.items()) + ")",
            f"  id={self.genome_id}  gen={self.generation}  by={self.generator}  nodes={self.complexity()}",
        ]
        return "\n".join(lines)
