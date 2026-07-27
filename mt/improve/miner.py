"""mt.improve.miner — the Factor Miner (Engine C, docs/03 §4).

Data-first: searches feature (op, args) configurations for raw predictive power against
forward returns, measured by the Information Coefficient (rank correlation) — the exact
metric CC_Trading's xsec/ic_report.py uses. High-IC single features seed new genomes, and
high-IC *interactions* of two features are MINTED as brand-new computable primitives through
the registry's §1 gate — the vocabulary literally grows from the data.

Discipline (docs/03 §4): the miner is the most overfitting-prone engine, so every mined
factor is still charged to the Deflated-Sharpe trial count and must clear the same Gauntlet
as any random expression.
"""
from __future__ import annotations

import hashlib
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from mt.data.panel import NormPanel
from mt.genome.registry import REGISTRY, OpSpec, ArgSpec, Pit, register, computable_feature_ops
from mt.genome.schema import FeatureNode
from mt.sim import features as F


def _pooled_ic(feat: pd.DataFrame, fwd: pd.DataFrame, sample: int = 4000, seed: int = 0) -> float:
    """Pooled rank IC of a feature vs forward returns over all (time, symbol) points."""
    a = feat.to_numpy().ravel(); b = fwd.to_numpy().ravel()
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 50:
        return 0.0
    if len(a) > sample:
        idx = np.random.default_rng(seed).choice(len(a), sample, replace=False)
        a, b = a[idx], b[idx]
    ar = pd.Series(a).rank().to_numpy(); br = pd.Series(b).rank().to_numpy()
    if ar.std() == 0 or br.std() == 0:
        return 0.0
    return float(np.corrcoef(ar, br)[0, 1])


def _forward(panel: NormPanel, horizon: int = 4) -> pd.DataFrame:
    close = panel.close_matrix()
    return close.shift(-horizon) / close - 1.0


def mine_features(panel: NormPanel, n_candidates: int, rng: np.random.Generator,
                  top: int = 3, horizon: int = 4) -> List[Tuple[FeatureNode, float]]:
    """Return the top-|IC| candidate feature nodes discovered on this panel."""
    fwd = _forward(panel, horizon)
    ops = [op for op in computable_feature_ops()
           if all(d in ("ohlcv", "funding_rate") for d in op.data_requires)]
    scored: List[Tuple[FeatureNode, float]] = []
    for _ in range(n_candidates):
        op = ops[int(rng.integers(len(ops)))]
        args = op.sample_args(rng)
        try:
            mat = F.compute(op.name, panel, args, panel.primary_tf).reindex_like(fwd)
            ic = _pooled_ic(F.zscore_rows(mat), fwd, seed=int(rng.integers(1 << 30)))
        except Exception:
            continue
        scored.append((FeatureNode("f1", op.name, args), abs(ic)))
    scored.sort(key=lambda x: -x[1])
    return scored[:top]


def register_minted(name: str, recipe: dict, ic: float = 0.0) -> bool:
    """(Re)build a minted `intx_*` primitive from its stored recipe and register it.

    Called at startup for every op in the `minted_ops` table. Without this the vocabulary lived
    only in the process that minted it: on the next marathon the op was gone from the REGISTRY, so
    every hall-of-fame genome built on it failed `typecheck` and was silently skipped by
    warm-start — the deepest, most-evolved part of the search was discarded every run while
    best-z still reported its score (docs/15 §3.4)."""
    if name in REGISTRY:
        return False
    a, aa = recipe["a"], recipe["a_args"]
    b, ab = recipe["b"], recipe["b_args"]

    def _builder(p, args, tfx, _a=a, _aa=aa, _b=b, _ab=ab):
        za_ = F.zscore_rows(F.compute(_a, p, _aa, tfx))
        zb_ = F.zscore_rows(F.compute(_b, p, _ab, tfx))
        return za_ * zb_

    F.BUILDERS[name] = _builder
    register(OpSpec(name, "feature", {}, output="Series[zscore]", cost_class="medium",
                    tags=("mined", "interaction", a, b), computable=True,
                    pit=Pit(lookback="max(components)"),
                    provenance={"source": "factor_miner", "version": "1.0.0", "ic": round(ic, 4)},
                    doc=f"mined interaction {a}×{b} (IC={ic:.3f})"))
    return True


def restore_minted(store) -> int:
    """Rebuild the whole persisted vocabulary. Returns how many ops were re-registered."""
    n = 0
    for name, recipe, ic in store.minted_ops():
        try:
            if register_minted(name, recipe, ic or 0.0):
                n += 1
        except Exception:
            continue
    return n


def mint_interaction(panel: NormPanel, rng: np.random.Generator, min_ic: float = 0.03,
                     store=None, market: str = "") -> Optional[str]:
    """Mint a new `intx_*` primitive = product of two standardized features, if it clears an
    IC bar. Registers it (typed, PIT-safe, bounded) so every generator can use it immediately,
    and PERSISTS the recipe so it survives the process."""
    fwd = _forward(panel)
    ops = [op for op in computable_feature_ops()
           if all(d in ("ohlcv", "funding_rate") for d in op.data_requires)]
    a, b = ops[int(rng.integers(len(ops)))], ops[int(rng.integers(len(ops)))]
    aa, ab = a.sample_args(rng), b.sample_args(rng)
    tf = panel.primary_tf
    try:
        za = F.zscore_rows(F.compute(a.name, panel, aa, tf).reindex_like(fwd))
        zb = F.zscore_rows(F.compute(b.name, panel, ab, tf).reindex_like(fwd))
        prod = za * zb
        ic = _pooled_ic(prod, fwd, seed=int(rng.integers(1 << 30)))
    except Exception:
        return None
    if abs(ic) < min_ic:
        return None
    key = hashlib.sha256(f"{a.name}{aa}{b.name}{ab}".encode()).hexdigest()[:8]
    name = f"intx_{key}"
    if name in REGISTRY:
        return name
    recipe = {"a": a.name, "a_args": aa, "b": b.name, "b_args": ab}
    register_minted(name, recipe, ic)
    if store is not None:
        try:
            store.save_minted_op(name, market, recipe, ic)
        except Exception:
            pass
    return name
