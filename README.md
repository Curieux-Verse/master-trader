# Master Trader

**An autonomous, self-improving strategy-discovery system for crypto, FX, and gold — built entirely on free-tier data and compute.**

Master Trader is not a trading strategy. It is a *factory that manufactures, tests, kills, and refines trading strategies* around the clock, with the discipline of a quantitative research desk and the tirelessness of a machine. It sits one level of abstraction *above* the strategies you already run (`CC_Trading`, `FX_Trading`, the sentiment scanners) and treats each of them as one member of an evolving population.

The design goal, stated plainly: **make the *research process* the edge — not any single idea.** This is the Renaissance Technologies insight restated. Individual signals decay; a machine that can *find and validate new signals faster than they decay*, while ruthlessly rejecting the ones that are only luck, is the durable asset.

---

## Read these documents in order

| # | Document | What it answers |
|---|----------|-----------------|
| 00 | [Vision & Reality](docs/00_VISION_AND_REALITY.md) | What we are building, what is achievable, and the honest limits. **Read this first.** |
| 01 | [System Architecture](docs/01_SYSTEM_ARCHITECTURE.md) | The whole machine on one page, then subsystem by subsystem. |
| 02 | [Strategy Genome DSL](docs/02_STRATEGY_GENOME_DSL.md) | How a strategy is represented as *data* so it can be generated, mutated, and searched. |
| 03 | [Generation Engines](docs/03_GENERATION_ENGINES.md) | The four idea sources: evolutionary, LLM-critic, factor-mining, template. |
| 04 | [Backtest Simulator](docs/04_BACKTEST_SIMULATOR.md) | The multi-fidelity, cost-aware, tick-level simulation loop. |
| 05 | [Validation Gauntlet](docs/05_VALIDATION_GAUNTLET.md) | The overfitting immune system: CPCV, PBO, Deflated Sharpe, regime & OOS gates. |
| 06 | [Self-Improvement Loop](docs/06_SELF_IMPROVEMENT_LOOP.md) | How the system reflects on *why* a strategy won or lost and gets better. |
| 07 | [Live Adaptation & Portfolio](docs/07_LIVE_ADAPTATION_AND_PORTFOLIO.md) | The paper→live ladder, regime-aware allocator, drift detection, kill switches. |
| 08 | [Infrastructure & Data](docs/08_INFRASTRUCTURE_AND_DATA.md) | The zero-cost stack: data feeds, storage, orchestration, compute. |
| 09 | [Research Roadmap](docs/09_RESEARCH_ROADMAP.md) | Phased build plan with milestones and go/no-go gates. |
| 10 | [Integration Map](docs/10_INTEGRATION_MAP.md) | Exactly how this reuses your existing CC_Trading / xsec / SMC_ML / scanners. |
| 11 | [Primitive Catalog](docs/11_PRIMITIVE_CATALOG.md) | The full open-ended registry of features/indicators/operators the generators pull from — ~16 families incl. Auction Market Theory. |
| 12 | [Primitive Implementation Plan](docs/12_PRIMITIVE_IMPLEMENTATION_PLAN.md) | How the catalog gets built: every family → data → seed code → cost → phase. |
| — | [References](docs/REFERENCES.md) | Papers and the specific claims each one backs. |

---

## The one-paragraph version

A pool of **Generation Engines** continuously proposes candidate strategies, each expressed in a common **Strategy Genome** (a typed, serializable spec — not free-form code). Every candidate is dropped into a **multi-fidelity Backtest Simulator**: cheap vectorized screening for the thousands, expensive tick-level simulation for the survivors. Survivors then face the **Validation Gauntlet**, a battery of anti-overfitting statistical tests whose entire job is to *disprove* the strategy. What survives is not called "good" — it is called "not yet rejected," and it earns a place in a **Quality-Diversity Archive** that deliberately keeps a *diverse* stable of specialists rather than one over-tuned champion. A **Self-Improvement Loop** (evolutionary search + an LLM critic that reads trade-level post-mortems + a bandit meta-controller) mutates the archive toward better, more robust regions. Finally, a **Live Adaptation** layer promotes strategies up a ladder — backtest → paper/shadow → incubation → live sleeve — with a regime-aware allocator distributing risk and hair-trigger kill switches pulling capital the moment live behavior diverges from the backtest.

---

## Running it

**Install**
```bash
pip install -r requirements.txt        # + optional: pip install numba  (JITs the hot loop ~100x)
```

**Locally**
```bash
python -m mt.selftest_gauntlet         # go/no-go: rejects a planted overfit, admits a planted edge
python -m mt.run_ingest --top-n 100 --deep-months 12 --macro --calendar   # build the real data lake
python -m mt.run_system --source lake --snapshot-id real --generations 4   # a bounded sprint (resets each run)
python -m mt.run_continuous --source lake --generations 0                  # the marathon (accumulates; Ctrl-C to stop)
python -m mt.run_genomes               # dump the live population → var/runs/genomes_current.md
```

The marathon is **stateful and resumable** — archive, lessons, minted vocabulary and bandit
learning all accumulate in `var/mt.db`, so discovery **compounds across sessions**. No machine
needs to stay on 24/7; it just learns whenever it runs.

**Unattended & free, on GitHub Actions** (this repo is public → unlimited Actions minutes)

| Workflow | Trigger | What it does |
|---|---|---|
| [`tests`](.github/workflows/tests.yml) | every push | unit suite + gauntlet self-test |
| [`ingest-lake`](.github/workflows/ingest.yml) | manual + weekly | builds the data lake, caches it |
| [`marathon`](.github/workflows/marathon.yml) | manual + every 6h | restores lake + brain, runs discovery ~5h, saves the brain, commits a digest to [`runs/`](runs/), pings Telegram |

The marathon restores/saves `var/mt.db` (the "brain") from the Actions cache each run, so it
compounds continuously without any always-on server. **First-time setup:**
1. Add repo **Secrets** (Settings → Secrets → Actions): `OANDA_API_KEY` (FX/gold ingest — crypto needs none), and optionally `SMC_BOT_TOKEN` + `SMC_CHAT_ID` for the Telegram digest.
2. Run the **`ingest-lake`** workflow once (Actions tab → Run workflow) to build the lake.
3. Run **`marathon`** (or wait for the 6-hourly cron). Watch it learn via the digest's **best-z** climbing toward the significance bar.

> **Governance:** every run is paper/shadow only. The machine never self-authorizes a
> live-capital action — promotions are recommendations for a human to act on.

---

## Non-negotiable principles

1. **The null hypothesis is "this strategy is worthless."** Everything is built to reject, not to confirm. A backtest that looks good is a *suspect*, not a *result*.
2. **Every trial is counted.** The more strategies you test, the higher your best backtest will look by pure luck. We track the trial count and deflate every performance metric for it (Deflated Sharpe). This single discipline is what separates a research lab from a slot machine.
3. **Expand first; no privileged priors.** The search space is deliberately vast and agnostic — classical TA, statistics, microstructure, cross-asset relationships, SMC/ICT, and fully random combinations all compete on equal footing. We do *not* narrow to a favored school of thought up front. We wire everything together, including in ways no human would think to try, and let the data decide. **The catch that makes this safe:** a bigger search space means more chances to get lucky, so a wide search is only legitimate when paired with honest trial-counting (principle 2) and the Deflated-Sharpe / PBO gauntlet ([05](docs/05_VALIDATION_GAUNTLET.md)). Expansion and rigor are two halves of one method — expansion finds candidates, rigor keeps you from believing the lucky ones.
4. **Diversity over optimization.** We do not search for *the* best strategy. We maintain a *portfolio* of uncorrelated, regime-specialised strategies. A single global optimum is almost always an overfit artifact.
5. **Costs are modeled before profits are believed.** Fees, funding, spread, slippage, and market impact are charged in the *screening* tier, not bolted on later.
6. **Paper before pennies. Pennies before dollars.** No strategy touches real capital until it has survived the gauntlet *and* a live paper-trading incubation that confirms the backtest was not a fiction.
7. **Reproducibility is law.** Seeded RNG, content-hashed genomes, point-in-time data snapshots. Any result must be regenerable byte-for-byte or it does not count.

---

## What this is **not**

- It is **not** a promise of profit. See [00_VISION_AND_REALITY](docs/00_VISION_AND_REALITY.md). No architecture guarantees returns; markets are adversarial and largely efficient. What this design maximizes is the *rate and rigor of honest discovery*, and it minimizes the single largest cause of blown retail algo accounts: self-deception through overfitting.
- It is **not** a high-frequency system. Free-tier data and retail latency make sub-second edges inaccessible. The target is the seconds-to-days horizon where your existing SMC and factor work already lives.
- It is **not** a black box. Every promoted strategy has a human-readable genome, an attribution report, and a written LLM post-mortem explaining what it exploits and when it should fail.

---

*Status: **working implementation, running on real data.** The complete system (discovery → gauntlet → archive → self-improvement → paper) runs end-to-end across crypto/FX/XAU on a real, content-hashed data lake — Binance USD-M (deep history + real order flow), OANDA v20 (FX/gold), CFTC COT, GDELT tone, and FairEconomy event calendars — with regime-conditioned search, a purged/embargoed CPCV + Deflated-Sharpe + bootstrap-Reality-Check gauntlet, and a convergence instrument (best-z) that shows whether the search is actually learning. Runs unattended and free on GitHub Actions. Markets: crypto (Binance), FX + XAU (OANDA). Paper only — no live-capital automation.*
