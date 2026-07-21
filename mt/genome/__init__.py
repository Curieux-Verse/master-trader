"""mt.genome — the keystone: strategies as typed, searchable data.

A genome is a small typed pipeline (features -> signal -> sizing -> risk, governed by
meta) drawn from a vetted primitive REGISTRY. Because it is data, the system can hash,
mutate, cross, diff, describe, and dedup it — none of which is tractable with free-form
code. See docs/02.
"""
from mt.genome.schema import (
    Genome, FeatureNode, SignalSpec, SizingSpec, RiskSpec, Meta,
)
from mt.genome.registry import REGISTRY, OpSpec, ArgSpec, ops_for_stage

__all__ = [
    "Genome", "FeatureNode", "SignalSpec", "SizingSpec", "RiskSpec", "Meta",
    "REGISTRY", "OpSpec", "ArgSpec", "ops_for_stage",
]
