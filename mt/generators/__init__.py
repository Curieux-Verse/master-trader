"""mt.generators — the idea sources that feed the shared genome pool (docs/03).

Thin slice: the Template Sampler (Engine D) — parameterized archetypes PLUS fully-random
genomes that wire arbitrary primitives together with no archetype at all. The random stream
matters as much as the named archetypes: it is how the system discovers structure it was
never told to look for. Engines A (evolution), B (LLM), C (factor miner) attach at the same
pool in Phase 3.
"""
from mt.generators.templates import TemplateSampler

__all__ = ["TemplateSampler"]
