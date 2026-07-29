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
from typing import Callable, Dict, List, Optional

import numpy as np
import pandas as pd

from mt.genome.registry import REGISTRY
from mt.genome.schema import Genome


def _perturb(op_name: str, args: dict, rng: np.random.Generator) -> int:
    """Perturb the NUMERIC (int/float) args of one op in-place; return how many were changed.
    `mutate` is a no-op for choice/bool kinds, so only tunable numerics move."""
    spec = REGISTRY.get(op_name)
    if not spec:
        return 0
    n = 0
    for k, aspec in spec.args.items():
        if aspec.kind in ("int", "float") and k in args:
            args[k] = aspec.mutate(args[k], rng)
            n += 1
    return n


def param_variants(genome: Genome, m: int, rng: np.random.Generator) -> List[Genome]:
    """m genomes: the original + (m-1) with perturbed numeric args across the WHOLE genome —
    feature AND signal/sizing/risk (horizon, top_frac, thresholds, sl/tp mults, …). Perturbing
    only *feature* args (the old behaviour) meant a genome whose features expose no int/float
    args (e.g. order_block_strength, fvg_gap, atr_pct, candlestick_pattern) produced m IDENTICAL
    variants → CSCV scored PBO=1.0 and G3 rejected it deterministically, a false reject unrelated
    to overfitting. Widening to all tunable numerics gives such genomes a genuine parameter
    neighbourhood (they still share the rebalance grid). If a genome has NO tunable numeric arg
    anywhere, the variants stay identical and `returns_matrix` returns None → G3 DEFERS (never
    auto-fails)."""
    variants = [genome]
    for _ in range(m - 1):
        v = copy.deepcopy(genome)
        for f in v.features:
            _perturb(f.op, f.args, rng)
        _perturb(v.signal.op, v.signal.args, rng)
        _perturb(v.sizing.op, v.sizing.args, rng)
        _perturb(v.risk.op, v.risk.args, rng)
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
        s = r if isinstance(r, pd.Series) else pd.Series(r)
        # collapse duplicate timestamps (directional: several per-symbol exits close on one bar) so
        # the index is unique and variants can align on a COMMON CALENDAR rather than by trade order.
        series.append(s.groupby(level=0).sum())
    # Align columns on the UNION of timestamps; a bar where a variant held no position contributes 0
    # (flat). THIS is what makes the CSCV time-split + purge/embargo valid for DIRECTIONAL genomes
    # (and for cross-sectional variants whose perturbed horizon changes the rebalance grid). Position
    # tail-alignment mixed different calendar times across columns → an invalid PBO (docs/05 G3, docs/14).
    df = pd.concat(series, axis=1).sort_index().fillna(0.0)
    if df.shape[0] < 20 or df.shape[1] < 2:
        return None
    mat = df.to_numpy(dtype=float)
    # PBO is undefined without ≥2 DISTINCT configurations: identical columns make the IS-best the
    # arbitrary first column and force PBO→1.0, a false reject. When the genome could not be
    # perturbed into distinct variants, return None so G3 DEFERS instead of auto-failing.
    if len({tuple(np.round(mat[:, j], 12)) for j in range(mat.shape[1])}) < 2:
        return None
    return mat


def _col_sharpe(mat: np.ndarray) -> np.ndarray:
    mu = np.nanmean(mat, axis=0)
    sd = np.nanstd(mat, axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(sd > 0, mu / sd, np.nan)


def cscv_pbo(mat: np.ndarray, n_groups: int = 8, embargo_frac: float = 0.02) -> Optional[float]:
    """Probability of Backtest Overfitting via CSCV. mat is [T × K] (K ≥ 2 configs).

    `embargo_frac` implements López de Prado's purge/embargo: the trailing fraction of each
    contiguous time-group is dropped so two temporally-adjacent observations never end up split
    across the IS/OOS boundary (serial-correlation / overlapping-label leakage). This is what
    makes the "Purged" in CPCV real — without it, directional triple-barrier trades whose labels
    span a group boundary leak their outcome into the out-of-sample fold and deflate PBO."""
    if mat is None:
        return None
    T, K = mat.shape
    if K < 2 or T < 2 * n_groups:
        n_groups = max(2, min(n_groups, T // 2))
        if K < 2 or T < 2 * n_groups:
            return None
    groups = np.array_split(np.arange(T), n_groups)
    emb = max(1, int(round(embargo_frac * T))) if embargo_frac > 0 else 0
    if emb:                                                     # purge each group's trailing edge
        groups = [g[:-emb] if len(g) > emb + 1 else g[:max(1, len(g) // 2)] for g in groups]
    half = n_groups // 2
    logits = []
    oos_best = []                                              # OOS Sharpe of the IS-best config, per split
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
        oos_best.append(float(oos_sh[n_star]) if np.isfinite(oos_sh[n_star]) else np.nan)
    if not logits:
        return None
    return float(np.mean(np.array(logits) <= 0.0))             # P(IS-best below OOS median)


def cscv_stats(mat: np.ndarray, n_groups: int = 8, embargo_frac: float = 0.02) -> Optional[Dict]:
    """CSCV → {pbo, oos_sharpe_median, prob_oos_positive}. Beyond the scalar PBO, CPCV yields a
    whole DISTRIBUTION of out-of-sample Sharpes for the in-sample-best config (its key advantage
    over a single overfit estimate); we surface the median OOS Sharpe and the probability it is
    positive as extra, honest robustness signals (docs/05 G3)."""
    if mat is None:
        return None
    T, K = mat.shape
    ng = n_groups
    if K < 2 or T < 2 * ng:
        ng = max(2, min(ng, T // 2))
        if K < 2 or T < 2 * ng:
            return None
    groups = np.array_split(np.arange(T), ng)
    emb = max(1, int(round(embargo_frac * T))) if embargo_frac > 0 else 0
    if emb:
        groups = [g[:-emb] if len(g) > emb + 1 else g[:max(1, len(g) // 2)] for g in groups]
    half = ng // 2
    logits, oos_best = [], []
    for comb in combinations(range(ng), half):
        is_idx = np.concatenate([groups[i] for i in comb])
        oos_idx = np.concatenate([groups[i] for i in range(ng) if i not in comb])
        is_sh = _col_sharpe(mat[is_idx]); oos_sh = _col_sharpe(mat[oos_idx])
        if np.all(np.isnan(is_sh)) or np.all(np.isnan(oos_sh)):
            continue
        n_star = int(np.nanargmax(is_sh))
        ranks = np.argsort(np.argsort(np.nan_to_num(oos_sh, nan=-1e9)))
        w = min(max((ranks[n_star] + 1) / (K + 1), 1e-6), 1 - 1e-6)
        logits.append(np.log(w / (1 - w)))
        oos_best.append(float(oos_sh[n_star]) if np.isfinite(oos_sh[n_star]) else np.nan)
    if not logits:
        return None
    ob = np.array(oos_best, dtype=float); ob = ob[np.isfinite(ob)]
    return {
        "pbo": float(np.mean(np.array(logits) <= 0.0)),
        "oos_sharpe_median": float(np.median(ob)) if len(ob) else None,
        "prob_oos_positive": float(np.mean(ob > 0)) if len(ob) else None,
    }


def plateau_stats(mat: Optional[np.ndarray], retain: float = 0.5) -> Optional[Dict]:
    """Is this genome sitting on a PLATEAU in parameter space, or balanced on a spike?

    PBO and the plateau statistic are two different questions asked of the same neighbourhood,
    which is why this reads the matrix CSCV already built and costs no extra backtests:

      • PBO asks a SELECTION question — if I pick the best variant in-sample, does it stay good
        out-of-sample? It is about how the tuning was chosen.
      • The plateau asks a STABILITY question — do the genome's NEIGHBOURS still work at all?
        A strategy whose edge evaporates when its windows move by a few bars has been fitted to
        the noise of one particular parameterisation, and it will not survive contact with a
        slightly different market.

    A genome can pass one and fail the other. A flat, mediocre neighbourhood scores a low PBO
    (nothing to overfit to) while a sharp peak surrounded by dead variants scores a high plateau
    only if the peak itself is the centre — hence both are enforced.

    Column 0 of `mat` is the unperturbed genome (see `param_variants`); the rest are its
    neighbours. Returns the fraction of NEIGHBOURS that keep a positive edge and retain at least
    `retain` of the centre's t-statistic.

    These evaluations are NOT charged to the trial ledger. A neighbour is never promoted and is
    never compared against its siblings to pick a winner — the statistic is the *fraction that
    survive*, not the maximum. Charging them would inflate N for a robustness measurement,
    exactly the confusion the ledger-dedup rule exists to prevent."""
    if mat is None or mat.ndim != 2 or mat.shape[1] < 3 or mat.shape[0] < 20:
        return None
    T, K = mat.shape
    t = _col_sharpe(mat) * np.sqrt(T)            # per-column t-stat, N-independent
    centre = float(t[0])
    nb = t[1:]
    nb = nb[np.isfinite(nb)]
    if nb.size == 0 or not np.isfinite(centre):
        return None
    if centre <= 0:
        # a centre with no edge has no plateau to stand on; report it rather than dividing by it
        return {"plateau_pass_pct": 0.0, "plateau_n": int(nb.size), "centre_t": round(centre, 4),
                "neighbour_t_median": round(float(np.median(nb)), 4)}
    keep = (nb > 0) & (nb >= retain * centre)
    return {
        "plateau_pass_pct": round(float(np.mean(keep)) * 100.0, 2),
        "plateau_n": int(nb.size),
        "centre_t": round(centre, 4),
        "neighbour_t_median": round(float(np.median(nb)), 4),
        "retain_frac": retain,
    }
