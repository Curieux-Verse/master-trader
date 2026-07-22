"""mt.gauntlet.cpcv — Combinatorial Purged Cross-Validation → PBO (docs/05 G3).

The genuinely-new gate. Given a small family of parameter variants of a genome, CSCV
(Bailey & López de Prado) forms many combinatorial in-sample/out-of-sample partitions and
asks: how often does the configuration that looks best in-sample end up *below the median*
out-of-sample? That fraction is the **Probability of Backtest Overfitting**. A high PBO
means the selection was likely luck. We reject PBO > 0.5.

The "configurations" are the genome's own parameter neighbours — so PBO here measures how
overfit the *tuning* of this strategy is (it complements the population-level Deflated
Sharpe, which corrects for how many genomes were tried).
"""
from __future__ import annotations

import copy
from itertools import combinations
from typing import Callable, List, Optional

import numpy as np
import pandas as pd

from mt.genome.registry import REGISTRY
from mt.genome.schema import Genome


def param_variants(genome: Genome, m: int, rng: np.random.Generator) -> List[Genome]:
    """m genomes: the original + (m-1) with perturbed *numeric feature* args only, so all
    variants share the same rebalance grid and their return series stay alignable."""
    variants = [genome]
    for _ in range(m - 1):
        v = copy.deepcopy(genome)
        for f in v.features:
            spec = REGISTRY.get(f.op)
            if not spec:
                continue
            for k, aspec in spec.args.items():
                if aspec.kind in ("int", "float") and k in f.args:
                    f.args[k] = aspec.mutate(f.args[k], rng)
        v.generator = "cpcv_variant"
        variants.append(v)
    return variants


def returns_matrix(variants: List[Genome], panel, eval_fn: Callable) -> Optional[np.ndarray]:
    """[T × K] net-return matrix across the K variants, aligned by tail length.

    Cross-sectional variants share the rebalance grid (tail = full alignment); directional
    variants may have different trade counts (and duplicate exit timestamps), so position-
    based tail alignment is used uniformly — robust to both phenotypes."""
    series = []
    for v in variants:
        r = eval_fn(v, panel).net_returns
        if r is None or len(r) < 20:
            return None
        series.append(np.asarray(r.to_numpy(), dtype=float))
    m = min(len(a) for a in series)
    if m < 20:
        return None
    return np.column_stack([a[-m:] for a in series])


def _col_sharpe(mat: np.ndarray) -> np.ndarray:
    mu = np.nanmean(mat, axis=0)
    sd = np.nanstd(mat, axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(sd > 0, mu / sd, np.nan)


def cscv_pbo(mat: np.ndarray, n_groups: int = 8) -> Optional[float]:
    """Probability of Backtest Overfitting via CSCV. mat is [T × K] (K ≥ 2 configs)."""
    if mat is None:
        return None
    T, K = mat.shape
    if K < 2 or T < 2 * n_groups:
        n_groups = max(2, min(n_groups, T // 2))
        if K < 2 or T < 2 * n_groups:
            return None
    groups = np.array_split(np.arange(T), n_groups)
    half = n_groups // 2
    logits = []
    for comb in combinations(range(n_groups), half):
        is_idx = np.concatenate([groups[i] for i in comb])
        oos_idx = np.concatenate([groups[i] for i in range(n_groups) if i not in comb])
        is_sh = _col_sharpe(mat[is_idx]); oos_sh = _col_sharpe(mat[oos_idx])
        if np.all(np.isnan(is_sh)) or np.all(np.isnan(oos_sh)):
            continue
        n_star = int(np.nanargmax(is_sh))                      # in-sample-best config
        ranks = np.argsort(np.argsort(np.nan_to_num(oos_sh, nan=-1e9)))
        w = (ranks[n_star] + 1) / (K + 1)                      # its OOS relative rank
        w = min(max(w, 1e-6), 1 - 1e-6)
        logits.append(np.log(w / (1 - w)))
    if not logits:
        return None
    return float(np.mean(np.array(logits) <= 0.0))             # P(IS-best below OOS median)
