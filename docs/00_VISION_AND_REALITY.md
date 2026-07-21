# 00 — Vision & Reality

> Read this before anything else. A brilliant architecture pointed at the wrong belief is how quant desks blow up.

## 1. The vision

Build a machine that does, autonomously and continuously, what a disciplined quant research team does: form hypotheses, express them as testable strategies, simulate them honestly against history, subject the survivors to statistical cross-examination, allocate capital to the ones that keep earning their keep, and retire the ones that stop. It should generate *dozens of concurrent candidate strategies*, backtest them at high speed, reflect on *why* each one succeeded or failed, mutate them toward improvement, and graduate the best from simulation to paper trading — adapting as regimes change.

That is precisely what you asked for, and it is buildable at zero cost. The rest of these documents specify exactly how.

## 2. The reality — stated by your Principal Quant, not sugar-coated

You asked for something "extremely profitable in a brief time" and "that nobody can even imagine." I owe you honesty over hype, because the fastest way to lose money in this field is to believe the hype.

**Three things are true at once:**

1. **The architecture below is genuinely at the research frontier.** The combination it proposes — a strategy-genome DSL, quality-diversity evolutionary search, an LLM critic that reads trade-level post-mortems, and a CPCV/PBO/Deflated-Sharpe validation gauntlet, all on free infrastructure — mirrors what the newest 2025–2026 literature (QuantEvolve, MadEvolve, QuantaAlpha, AlphaEvolve) is only now formalizing. You are not behind. You are early.

2. **No architecture can guarantee profit, and anyone who tells you otherwise is selling something.** Markets are adaptive and adversarial. Most published edges are already arbitraged or were never real. The base rate for retail automated strategies is *negative* after costs. This system does not repeal that base rate — it gives you a disciplined machine for finding the rare exceptions and, just as importantly, for *proving to yourself which of your ideas are not exceptions* before they cost you money.

3. **"Extremely profitable in a brief time" is the exact mindset the system is engineered to protect you from.** The pressure to find a big edge fast is what makes people p-hack their backtests, over-fit parameters, and skip out-of-sample discipline. The edge here is *slow-compounding process rigor*, not a lightning strike. Renaissance did not win with one magic trade; they won with a decades-long machine for compounding many tiny, well-validated, well-hedged edges. This blueprint is built in that spirit.

**What "success" realistically looks like** for a zero-cost, retail-latency system on liquid crypto/FX/gold:

- A *stable of* modest, low-correlation edges — think Sharpe in the low single digits *per strategy on paper*, degrading meaningfully live — that combine into a portfolio smoother than any one of them.
- Far more *rejections* than discoveries. If the gauntlet is working, it will kill 95%+ of candidates that "looked great." That is the system succeeding, not failing.
- Most of the value in year one is **negative knowledge**: a machine that reliably tells you what does *not* work is worth more than a hunch that feels like it does.

If, after reading that, you still want to build it — good. That level-headedness is itself an edge. Let's build it properly.

## 3. The adversaries (design each subsystem to defeat these)

| Adversary | What it does to you | Which document defends against it |
|---|---|---|
| **Overfitting / backtest overfitting** | The #1 killer. More trials → a better-looking best backtest by pure luck. | [05 Validation Gauntlet](05_VALIDATION_GAUNTLET.md) — PBO, Deflated Sharpe, CPCV |
| **Look-ahead / leakage** | Using information the strategy could not have had; inflates everything. | [04 Simulator](04_BACKTEST_SIMULATOR.md) point-in-time discipline; purge/embargo |
| **Transaction costs & slippage** | Turns paper winners into live losers. | [04 Simulator](04_BACKTEST_SIMULATOR.md) cost model (reuses your `backtest/costs.py`) |
| **Regime change / non-stationarity** | The market that trained your model is gone. | [07 Live Adaptation](07_LIVE_ADAPTATION_AND_PORTFOLIO.md) drift detection, regime allocator |
| **Capacity & liquidity** | Edge exists but vanishes at any size that matters. | [05](05_VALIDATION_GAUNTLET.md) capacity test; [04](04_BACKTEST_SIMULATOR.md) impact model |
| **Survivorship & selection bias** | Testing only on coins/pairs that still exist. | [08 Data](08_INFRASTRUCTURE_AND_DATA.md) delisted-symbol inclusion |
| **Multiple-testing inflation** | 1,000 random strategies → ~50 look "significant" at p<0.05. | [05](05_VALIDATION_GAUNTLET.md) family-wise trial accounting |
| **Human / LLM confirmation bias** | The generator falls in love with a pattern. | [06 Self-Improvement](06_SELF_IMPROVEMENT_LOOP.md) adversarial critic role |

**Design maxim:** *every* subsystem's primary job is to make it harder to fool yourself. The profit is a residual left over after all the ways to be wrong have been subtracted.

## 4. Scope boundaries

- **Horizon:** seconds-to-days. No sub-second HFT — free data and retail latency make that a fantasy.
- **Markets:** Binance (crypto perps/spot), OANDA (FX majors + XAUUSD). All support free data + free paper trading.
- **Capital path:** research → paper → *optional* tiny live incubation. This deliverable stops at paper; live sizing is a business decision for you, not the machine.
- **Cost ceiling:** $0. Every component in [08](08_INFRASTRUCTURE_AND_DATA.md) has a free tier that is sufficient for this scale.

## 5. Definition of done (for the whole program)

The Master Trader is "working" when it can, unattended for a week:
1. generate ≥ dozens of new candidate genomes per day,
2. screen and validate them through the full gauntlet with correct trial accounting,
3. maintain a quality-diversity archive of surviving, low-correlation strategies,
4. run the archive in paper/shadow mode across crypto + FX + XAU,
5. produce a daily written report (via the LLM critic) of what it learned, what it promoted, and what it killed — and
6. never once take a live-capital action without an explicit human gate.

Everything that follows is in service of that definition.
