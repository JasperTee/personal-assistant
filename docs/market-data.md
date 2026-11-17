# Market data model

How the Market persona stores, grades and uses data so that an analysis is a chain of evidence, not a guess. Decision: [ADR-21](decisions.md#adr-21--five-axis-data-model-for-market-evidence). Tables: [data-dictionary.md](data-dictionary.md#market-tables--mvp--per-persona-market).

## Goal

A deep answer links many kinds of facts (company figures, the commodity or sector, the supply and demand chain, macro data, weather and seasons) into a **causal chain** where every link has a number, a source and a date. A vague answer jumps from the first link to the conclusion.

Example — a Vietnamese hydropower stock:

```text
La Niña -> more rain in the north and centre -> full reservoirs
-> more hydro output, lower spot power price
-> hydro revenue up, coal power down
-> compared with what the share price already expects?
```

## The five axes

Every piece of data is graded on five **independent** axes. Never merge two axes into one score.

| # | Axis | Values | Question it answers | Source of the idea |
| --- | --- | --- | --- | --- |
| 1 | Relevance tier | 0–4 | How many causal steps from the subject? | Supply-chain return predictability; financial knowledge graphs |
| 2 | Source reliability | A–F | How good is this source's track record for this kind of claim? | Admiralty Code (NATO AJP-2.1) |
| 3 | Information credibility | 1–6 | Is this specific item confirmed by independent sources? | Admiralty Code (NATO AJP-2.1) |
| 4 | Processing layer | bronze, silver, gold | How far has the data been cleaned and turned into evidence? | Medallion architecture |
| 5 | Time | period, published_at, ingested_at, lag | What period is it about, when did it become public, how long until it affects the subject? | Nowcasting with ragged-edge data |

### 1. Relevance tier (graph, not list)

| Tier | Meaning | Mining company (iron ore) | Consumer retailer |
| --- | --- | --- | --- |
| 0 | The subject itself | output, cash cost, reserves, debt | same-store sales, margin, inventory |
| 1 | Its product, commodity or sector | iron ore price, port stockpiles | sector retail sales |
| 2 | Supply and demand chain | Chinese steel output, housing starts | household income, consumer confidence |
| 3 | Macro | USD, interest rates, Chinese stimulus | interest rates, unemployment, inflation |
| 4 | Exogenous | cyclones in the Pilbara | weather anomalies, Tết / Christmas |

- The five tiers are the same for every sector; only the content changes, so the content lives in config (`services/market/config/factor_maps/<sector>.yaml`), not in code.
- The factor map is a **graph**: nodes are factors, edges are causal links (`supplies_to`, `demand_driver`, `cost_input`, `substitute`, ...). The tier of a node is computed by code as the number of edges on the shortest path to the subject; the YAML does not declare it.
- Evidence from tier 2 or higher is only used if it carries a **path** of edges down to tier 0.

### 2–3. Reliability and credibility (two separate grades)

| Source reliability | | Information credibility | |
| --- | --- | --- | --- |
| A | Completely reliable | 1 | Confirmed by other independent sources |
| B | Usually reliable | 2 | Probably true |
| C | Fairly reliable | 3 | Possibly true |
| D | Not usually reliable | 4 | Doubtful |
| E | Unreliable | 5 | Improbable |
| F | Cannot be judged (new source) | 6 | Cannot be judged |

- Reliability is graded **per source and per kind of claim** (an official statistics office is A for its own figures, not for forecasts), from its track record in `source_ratings`. A new source starts at F, and F is not the same as E.
- Credibility is graded per item from corroboration: the same figure from two independent sources raises it; one unconfirmed news story stays at 3 or below.

### 4. Processing layers

```text
bronze  raw_records    exactly what the API returned; never changed
silver  observations   parsed, typed, units and time zones normalised, deduplicated
gold    evidence       one statement about one factor, graded on all five axes, ready for the LLM
```

The LLM only ever reads **gold**. Bronze is kept so silver and gold can be rebuilt when a parser is fixed.

### 5. Time

- `period_start_on` / `period_end_on`: the period the number describes (e.g. Q3 2026).
- `published_at`: when it became public. `ingested_at`: when the bot fetched it.
- `lag_days` (on factor-map edges): how long until the factor affects the next node.
- **Point-in-time rule:** an analysis "as of T" may only use data with `published_at <= T`. This makes old analyses reproducible and keeps backtests honest.
- Seasonal and weather data are stored as **deviation from the seasonal norm** (`value_vs_norm`), not only as a raw value: studies find that unusual weather shifts spending between months, with effects that are non-linear and differ by season.

## Rules for an analysis

1. **Numbers come from tools.** Every number in a reply must appear in a cited `evidence` row; code checks this in post-processing.
2. **Every claim cites evidence.** A claim without an evidence id is dropped.
3. **Paths to tier 0.** Tier ≥ 2 evidence without a path is dropped.
4. **Conflicts:** prefer higher credibility, then higher reliability, then lower tier. Never average an A source with an E source.
5. **Depth by mode:** quick mode uses tiers 0–1 (cheap model); deep mode uses tiers 0–4 (strong model).
6. **"Not enough data" is a valid answer.**
7. **Every forecast is logged** in `forecasts` and scored when its horizon passes. Only forecasts made after the LLM's training cut-off count: LLMs score well on past periods they have memorised, and that advantage disappears after the cut-off.

## Sentiment and panic (ADR-22)

Panic moves prices away from fundamentals for a while; the analysis must tell the two apart. "Is this drop caused by worse fundamentals (tier 0–3 evidence) or by fear?" is the main question this section answers.

### What the research says

| Finding | Source | Consequence here |
| --- | --- | --- |
| Waves of sentiment can be measured and have regular effects; hard-to-value stocks are hit hardest | Baker & Wurgler (2006, 2007) | Sentiment weighs more for small, speculative stocks |
| Media pessimism predicts a price drop **followed by reversion**; extreme pessimism predicts high volume | Tetlock (2007) | Panic is a short-term, mean-reverting signal, not a new fundamental |
| Household searches for "recession", "bankruptcy"… measure fear daily | Da, Engelberg & Gao (2015), FEARS | Search attention is a cheap fear gauge |
| "Twitter mood predicts the market" failed to replicate; the fund built on it closed | Lachanski & Pav (2017) | Never trust a single mood index without out-of-sample tests |
| Social sentiment moves **with** returns; it predicts intraday (novice traders) but not daily large-cap returns | Renault (2017, 2020); StockTwits studies | Short `lag_days`; strongest within the day |
| Negative sentiment matters more than positive | StockTwits study (LSE Business Review) | Treat fear and euphoria asymmetrically |
| Up to 71% of authors of suspicious stock tweets were bots (cashtag piggybacking) | Cresci et al. (2019) | Bot and coordination filter before any counting |
| Trades made on high social-media attention lose money for retail investors | Eliner & Kobilov (2023); Warkulat & Pelster (2024) | High attention = risk flag, not a buy signal |
| Sentiment raises the chance of a crash within a year but does not time the turning point | Zouaoui et al. (2011) | Report risk level, never "the bottom is in" |
| Vietnam: retail investors are the large majority of trading; Facebook sentiment had no effect on returns while online newspapers did | Tạp chí Ngân hàng; Thang Long University (2024) | In Vietnam, weight press above Facebook until our own data says otherwise |

### Three families of fear signals

| Family | Examples | Source reliability | Why |
| --- | --- | --- | --- |
| Market-based | ready-made gauges where they exist: implied volatility (Cboe VIX for the US, S&P/ASX 200 VIX for Australia), CNN Fear & Greed (US), St. Louis Fed Financial Stress Index (weekly); otherwise computed by us: price drop vs. its own volatility, realised volatility, volume spike, breadth (share of stocks falling), foreign net selling, margin pressure | A–B | Hard data, hard to fake |
| Attention | search volume for fear words (Vietnamese and English), news count | B | Aggregated, little manipulation |
| Text | news pessimism, social posts and comments | press C, social **F** by default, credibility ≤ 3 | Noisy, can be manipulated |

- Every signal is stored as **deviation from its own recent baseline** (`value_vs_norm`), not as a level.
- **Panic state** = at least two families cross their thresholds at the same time (thresholds in `services/market/config/sentiment.yaml`, tuned on real data, not guessed). Text alone never declares panic.
- In the factor graph, sentiment links to the subject's **price**, not to its revenue or costs, with a short `lag_days`.

### Social data pipeline

```text
bronze: posts fetched through official APIs or public pages the platform allows
silver: language detection, dedupe of near-identical posts, bot and coordination filter
        (new accounts, bursts of copies, one author posting many tickers)
gold:   aggregated snapshot per subject and time window: post count vs. baseline,
        share negative / positive (cheap model, batch), top themes
```

- Only **aggregates** reach gold and the LLM. Raw posts are personal data: keep them only as long as needed to rebuild a snapshot (`retention.social_posts_days`), never store names or profiles.
- No scraping that breaks a platform's terms of use; if a source has no allowed access, it is not used.

### How the analysis uses it

1. Fundamental chain first (tiers 0–4).
2. Then the market state: is there a panic or euphoria state, and since when?
3. Verdict per move: "driven by fundamentals", "driven by sentiment", or "both", with the evidence for each.
4. If sentiment-driven: say that research shows such moves tend to revert, give the risk, and say what would change the view; never a buy or sell instruction.

## Quantitative layer (ADR-23)

Statistics and machine learning handle what repeats in past data; agents handle what past data cannot say. Models run in code on the owner's machine, so they cost no tokens.

| Job | Done by | Why |
| --- | --- | --- |
| Measure past relationships (e.g. how bank stocks reacted to rate rises) | Statistics: regression, event studies | Cheap, reproducible, testable |
| Probabilistic forecasts from recurring patterns | ML: penalised regression, trees, gradient boosting | Catches non-linear patterns |
| Volatility and risk | Volatility models, the fear signals of ADR-22 | A numbers problem; LLMs are weak at it |
| Read news and reports, explain, build causal chains | Agents | Language and context |
| **Challenge the models** ("trained on a low-rate era — is now different?") | Agents | Judgement about regime and novelty |
| Events with no history | Agents | Models know nothing about what never happened |

Rules:

1. **Baseline first.** Start with a simple model (historical average, linear regression). A complex model is used only if it beats the baseline out of sample. Research finds real but small predictability (out-of-sample R² around 0.26% a month in Gu, Kelly & Xiu after regularisation; an unpenalised model with 900+ predictors overfits badly).
2. **Walk-forward validation only** on point-in-time data: train on the past, test on the next period, roll forward. A single hold-out set is not trusted for investment backtests (Bailey et al.).
3. **Count the trials.** Every model and setting tried is logged; the more tried, the higher the bar.
4. **Model output is evidence, not truth.** Each result becomes an `evidence` row with `kind = model` and its validation figures (out-of-sample error, training period, sample size) so agents can weigh and challenge it.
5. **Small data is fine.** Macro series and financial statements are small; "big data" is not a goal.

## Indicator trust (ADR-24)

Each indicator and model gets a **trust score that changes over time and by market regime**, earned from its own past results. It extends axis 2 (source reliability) from sources to indicators and models.

- **Regimes** are set in code from data, few on purpose (e.g. volatility high / normal; rates rising / falling). Too many regimes leave too few scored forecasts in each.
- **Score from track record:** every indicator's past calls are scored (e.g. Brier score for probabilities) per regime and horizon; recent results weigh more (exponential decay with a half-life in config).
- **Shrink toward equal weights.** Estimated "optimal" weights are noisy, and equal weights often beat them (the forecast combination puzzle). Trust = blend of the indicator's own record and the average, moving away from the average only as the number of scored calls grows. A new indicator starts at the average, like a new source starts at F.
- **Agents see the trust score and the sample size behind it**, and may challenge it ("high score, but from 6 calls, in a regime never seen before").
- All of this is code: no tokens.

## Output of a deep analysis

Thesis · causal chain(s) · evidence table (statement, value, source, grade, date) · counter-evidence · 2–3 scenarios with probabilities · signals to watch · what would prove the thesis wrong · confidence.

## Not decided yet

- Scope: **the whole world** (Huy, 2026-11-13), grown desk by desk; first sector: **financials**. Still open: which desks come first (a global macro desk plus one market's financials desk is the suggested start).
- How many analyst sub-agents and how they debate (TradingAgents-style bull/bear vs. one critic) — a later ADR, once the data layer exists.
- Budget: deep runs use the strong model several times per run; see ADR-20.

## References

- Cohen & Frazzini (2008), *Economic Links and Predictable Returns*, Journal of Finance 63(4) — customer returns predict supplier returns because investors react late to linked firms.
- Menzly & Ozbas (2010) — supplier and customer industries cross-predict each other's returns.
- Ding et al. (2026), *TRACE: Temporal Rule-Anchored Chain-of-Evidence on Knowledge Graphs* (arXiv:2603.12500) — LLM + temporal knowledge graph with explicit evidence chains.
- NATO AJP-2.1 / STANAG 2511 (Admiralty Code) — source reliability A–F and information credibility 1–6, graded independently.
- Databricks, *Medallion architecture* — bronze (raw), silver (validated), gold (enriched).
- Marcellino & Schumacher (2008), *Factor-MIDAS for Now- and Forecasting with Ragged-Edge Data* — indicators arrive at different frequencies and delays.
- Sandqvist & Siliverstovs (2021), Empirical Economics 61 — weather deviations from seasonal norms shift consumer spending.
- Badorf & Hoberg (2020), Journal of Retailing and Consumer Services 52 — weather effects on sales are non-linear.
- Xiao et al. (2024), *TradingAgents* (arXiv:2412.20138) — analyst team + bull/bear researchers + risk management.
- Gao, Jiang & Yan (2025), *Detecting Lookahead Bias in LLM Forecasts* (arXiv:2512.23847) — forecast accuracy is inflated before the training cut-off.
- Baker & Wurgler (2006), Journal of Finance 61(4); (2007), Journal of Economic Perspectives 21(2) — investor sentiment and the cross-section of returns.
- Tetlock (2007), *Giving Content to Investor Sentiment*, Journal of Finance 62(3) — media pessimism, price pressure and reversion.
- Da, Engelberg & Gao (2015), *The Sum of All FEARS*, Review of Financial Studies 28(1) — search-based fear index.
- Lachanski & Pav (2017), Econ Journal Watch 14(3) — failed replication of "Twitter Mood Predicts the Stock Market".
- Renault (2017), Journal of Banking & Finance 84 — intraday StockTwits sentiment; Renault (2020), Digital Finance — no daily prediction for large caps.
- Cresci et al. (2019), *Cashtag Piggybacking*, ACM Transactions on the Web 13(2) — bots in stock microblogs.
- Eliner & Kobilov (2023), *To the Moon or Bust*; Warkulat & Pelster (2024), International Review of Financial Analysis — losses from social-media-driven trades.
- Zouaoui, Nouyrigat & Beer (2011), Financial Review 46 — sentiment and the probability of stock market crises.
- Lopez-Lira & Tang (2023–2025), *Can ChatGPT Forecast Stock Price Movements?* (arXiv:2304.07619) — LLM news scores and the initial market reaction.
- Nguyễn Thu Hoài, Thang Long University (2024) — Facebook vs. online-newspaper sentiment in Vietnam.
- Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning*, Review of Financial Studies — ML return prediction: small R², real economic value.
- Bailey, Borwein, López de Prado & Zhu (2017), *The Probability of Backtest Overfitting*, Journal of Computational Finance.
- Bates & Granger (1969); Stock & Watson (2004) — forecast combination, time-varying and inverse-MSE weights, instability of predictors.
- Smith & Wallis (2009), Oxford Bulletin of Economics and Statistics 71(3) — the forecast combination puzzle.
- Ravazzolo, van Dijk & Verbeek — time-varying model weights for S&P 500 forecasts with economic gains.
