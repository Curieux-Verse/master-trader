# References

The specific claim each source backs. This is a research blueprint; these are the shoulders it stands on.

## Overfitting, validation, and the honesty machinery (the core discipline)

- **Bailey, Borwein, López de Prado, Zhu — "The Probability of Backtest Overfitting" (PBO / CSCV).** Backs [05 G3](05_VALIDATION_GAUNTLET.md): PBO = probability the in-sample-best strategy underperforms out-of-sample; combinatorially-symmetric cross-validation to estimate it. `davidhbailey.com/dhbpapers/backtest-prob.pdf`
- **Bailey & López de Prado — "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality."** Backs [05 G4](05_VALIDATION_GAUNTLET.md) and the trial-count ledger: deflate Sharpe for number of trials, sample length, skew/kurtosis.
- **López de Prado — *Advances in Financial Machine Learning*.** Backs the whole gauntlet philosophy: purged/embargoed CV, **CPCV**, meta-labeling, the "backtest is a research tool, not a discovery" stance. Your `backtest/purged_cv.py` already ports the purge/embargo idea.
- **Recent comparative study (2024, ScienceDirect) — out-of-sample testing methods in a synthetic controlled environment.** Backs [05](05_VALIDATION_GAUNTLET.md): **CPCV shows lower PBO and superior DSR** vs. k-fold and single walk-forward. `sciencedirect.com/science/article/abs/pii/S0950705124011110`
- **White — "A Reality Check for Data Snooping"; Hansen — "Superior Predictive Ability (SPA) test."** Back [05 §3](05_VALIDATION_GAUNTLET.md) population-level audits: is the *best* strategy better than a data-snooping null?

## LLM-driven + evolutionary strategy discovery (the frontier this design tracks)

- **QuantEvolve (2025).** Backs [03](03_GENERATION_ENGINES.md)/[06](06_SELF_IMPROVEMENT_LOOP.md): multi-agent MAP-Elites + island models + hypothesis-driven LLM mutation evolving complete strategies as executable specs.
- **MadEvolve — "Evolutionary Optimization of Trading Systems with LLMs" (arXiv 2605.23007).** Backs the MAP-Elites behavioral grid (complexity × diversity × performance axes) used in [06 §2](06_SELF_IMPROVEMENT_LOOP.md).
- **QuantaAlpha — "An Evolutionary Framework for LLM-Driven Alpha Mining" (arXiv 2602.07085).** Backs [03 §4](03_GENERATION_ENGINES.md): symbolic factor representation, redundancy-aware evolution, constraint-aware synthesis for more stable/generalizable factors.
- **AlphaEvolve / CodeEvolve (arXiv 2510.14150).** Back [03](03_GENERATION_ENGINES.md)/[06](06_SELF_IMPROVEMENT_LOOP.md): LLM-ensemble evolutionary program discovery with MAP-Elites population management, migration, archive updates.
- **"Cognitive Alpha Mining via LLM-Driven Code-Based Evolution" (arXiv 2511.18850).** Backs the LLM-critic-plus-evolution division of labor.

## Quality-diversity & the "diverse stable, not one champion" thesis

- **Mouret & Clune — "Illuminating search spaces by mapping elites" (MAP-Elites).** Backs [06 §2](06_SELF_IMPROVEMENT_LOOP.md): fill a behavioral grid with the best occupant per niche → diversity as a first-class objective.
- **Lehman & Stanley — Novelty Search / Quality-Diversity.** Backs the novelty-pressure generation bias ([03 §6](03_GENERATION_ENGINES.md)).

## Self-reflection / accumulating-lesson agents

- **Shinn et al. — "Reflexion: Language Agents with Verbal Reinforcement Learning."** Backs [06 §3](06_SELF_IMPROVEMENT_LOOP.md): verbal self-critique + episodic memory to improve without gradient updates.
- **Wang et al. — "Voyager: An Open-Ended Embodied Agent with LLMs."** Backs the **Lesson Library / skill library** pattern — a growing, retrievable store of learned competencies.

## Multi-objective & sequential-decision machinery

- **Deb et al. — NSGA-II.** Backs [05 §4](05_VALIDATION_GAUNTLET.md)/[03 §2](03_GENERATION_ENGINES.md): fast non-dominated sorting for the Pareto-front fitness (return, robustness, capacity, simplicity, orthogonality).
- **Auer et al. — bandits (UCB/EXP3); Thompson sampling.** Back the meta-controller ([06 §4](06_SELF_IMPROVEMENT_LOOP.md)) and online allocator ([07 §3](07_LIVE_ADAPTATION_AND_PORTFOLIO.md)).
- **Schulman et al. — PPO.** Backs the *optional* execution-layer RL track ([06 §5](06_SELF_IMPROVEMENT_LOOP.md)), consistent with your `SMC_ML` Phase-4 plan.

## Concept drift (live monitoring)

- **Page — CUSUM; Page-Hinkley test; Bifet & Gavaldà — ADWIN.** Back [07 §4](07_LIVE_ADAPTATION_AND_PORTFOLIO.md): change-point detection on live return streams.
- **Bailey & López de Prado — Probabilistic Sharpe Ratio (PSR).** Backs the rolling live-vs-backtest edge-decay monitor ([07 §4](07_LIVE_ADAPTATION_AND_PORTFOLIO.md)).

## Costs, capacity, impact

- **Almgren-Chriss / square-root market-impact law.** Backs [04 §3](04_BACKTEST_SIMULATOR.md) and [05 G7](05_VALIDATION_GAUNTLET.md): impact ∝ √(size/ADV); the capacity test.

## Free data & infrastructure (verified July 2026)

- **Binance public data** — free bulk klines/trades/aggTrades dumps. `github.com/binance/binance-public-data`. ⚠️ v1 klines/aggTrades REST endpoints deprecated, retiring **2026-03-25** — use v3.
- **Binance Spot API docs.** `developers.binance.com/docs/binance-spot-api-docs`. Rate limit ~2400 request-weight/min; klines ≤1000/call.
- **OANDA v20 REST** — free practice account, historical candles + live pricing for FX majors and XAUUSD; rate-limited, practice rates differ slightly from live.
- **FRED, CFTC COT (Socrata), GDELT, Finnhub free tier** — the macro/positioning/news feeds your sentiment scanners already use.

---

*Note on citations: paper identifiers and dates were current as of the July 2026 research pass. Where an arXiv id is given, verify the latest version at build time — preprints revise. The methodological claims (PBO, DSR, CPCV, MAP-Elites, Reflexion) are well-established; the 2025–2026 LLM-evolution papers are fast-moving and worth re-checking for successors before you implement.*
