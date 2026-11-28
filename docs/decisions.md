# Decisions (ADR)

Each decision: context → options → chosen → why → trade-offs. Never delete an old decision; if you change your mind, add a new one and mark the old one "Superseded by ADR-xx".

| ID | Decision | Status | Date |
| --- | --- | --- | --- |
| ADR-01 | Build our own instead of using OpenClaw | Accepted | 2026-11-09 |
| ADR-02 | Python | Superseded by ADR-33 (C# .NET main) | 2026-11-09 |
| ADR-03 | Use LLM APIs, don't run models locally | Accepted | 2026-11-09 |
| ADR-04 | Telegram is the first channel | Accepted | 2026-11-09 |
| ADR-05 | 5-layer architecture + 7-step pipeline | Accepted | 2026-11-09 |
| ADR-06 | Policy layer in code, RiskLevel classification | Accepted | 2026-11-09 |
| ADR-07 | Routing before the agent loop | Accepted | 2026-11-09 |
| ADR-08 | Secretary + specialist bots (hub-and-spoke) | Accepted; amended by ADR-32 (two tiers) | 2026-11-09 |
| ADR-09 | One database: SQLite → PostgreSQL | Superseded by ADR-25 (one database per service) | 2026-11-09 |
| ADR-10 | Write our own agent loop, no framework yet | Accepted | 2026-11-09 |
| ADR-11 | Run locally during development, AWS VPS once stable | Superseded by ADR-35 (home server) | 2026-11-09 |
| ADR-12 | Invoices are only exported to a folder, not sent via Zalo | Accepted | 2026-11-11 |
| ADR-13 | Detailed rental data is kept for 3 months only | Superseded by ADR-27 | 2026-11-11 |
| ADR-14 | English for all project text | Accepted | 2026-11-11 |
| ADR-15 | Scheduled runs: read → select → verify → dedupe → send → confirm → commit | Proposed (phase 5) | 2026-11-11 |
| ADR-16 | Clean Architecture for the system, MVC only in channels; folders by layer, then area | Accepted | 2026-11-11 |
| ADR-17 | LLM input preprocessing (normalised + original text); verify with evals | Accepted | 2026-11-12 |
| ADR-18 | Branches, pull requests and a protected `main` | Accepted | 2026-11-12 |
| ADR-19 | Use cases live in `application/` | Accepted; folder name `channels/` superseded by ADR-26 (`entrypoints/`) | 2026-11-12 |
| ADR-20 | Market analysis joins the MVP (Secretary + Rental + Market) | Accepted | 2026-11-13 |
| ADR-21 | Five-axis data model for market evidence | Accepted | 2026-11-13 |
| ADR-22 | Sentiment and panic as a separate market-state signal | Accepted | 2026-11-13 |
| ADR-23 | Quantitative layer: statistics and ML on past data, agents interpret and challenge | Proposed | 2026-11-13 |
| ADR-24 | Indicator trust that changes over time and by regime, earned from past results | Proposed | 2026-11-13 |
| ADR-25 | Microservices split by business area: assistant, rental, market, finance | Accepted; reminders and to-dos moved by ADR-28 and back by ADR-36, retention changed by ADR-27, identity and LLM rules changed by ADR-34, `rental` renamed `housing` by ADR-37 | 2026-11-18 |
| ADR-26 | Monorepo with one folder per service under `services/` | Accepted; `assistant` moved to `apps/` by ADR-30, Python tooling replaced by ADR-33 | 2026-11-18 |
| ADR-27 | Rental keeps readings and bills for 12 months, meter-book photos for 3 | Accepted | 2026-11-18 |
| ADR-28 | The planner belongs to the study app (own repository, .NET); the assistant is its client | Superseded by ADR-36 (no link to the study app) | 2026-11-18 |
| ADR-29 | Telegram webhook in every environment, ready for several replicas | Superseded by ADR-31 | 2026-11-18 |
| ADR-30 | Apps in `apps/`, business services in `services/` | Accepted | 2026-11-19 |
| ADR-31 | Telegram stays on long polling; one owner, one process | Accepted | 2026-11-19 |
| ADR-32 | Two tiers of bots: a Secretary that routes, specialists that hold the tools | Accepted | 2026-11-27 |
| ADR-33 | C# .NET is the main language; the code restarts from scratch | Accepted | 2026-11-27 |
| ADR-34 | Service boundaries: data only through APIs, sensitive data away from AI | Accepted | 2026-11-27 |
| ADR-35 | Personal scope, home server, architecture freeze | Accepted | 2026-11-27 |
| ADR-36 | No link to the study app; the planner lives in `assistant` under the Life bot | Accepted; study deadlines moved to Life by ADR-37 | 2026-11-28 |
| ADR-37 | Life owns everything with a date; `rental` is renamed `housing` | Accepted | 2026-11-28 |
| ADR-38 | Research merges into Learning; a daily science digest | Accepted | 2026-11-28 |
| ADR-39 | Email and Documents merge into Life; each specialist sends its own report at its own pace, only when there is news; one file store, summaries kept by each area | Accepted | 2026-11-28 |

---

## ADR-01 — Build our own instead of using OpenClaw

- **Context:** OpenClaw is an open-source assistant with multi-channel support, memory and skills out of the box.
- **Options:** (a) install OpenClaw; (b) build our own, borrowing ideas from OpenClaw's architecture.
- **Chosen:** (b).
- **Why:** the goal is learning and a CV project; OpenClaw has a worrying security history (instances exposed to the internet, malicious skills on ClawHub) while this agent will read mail and tenant data; the custom needs (rent calculation, market) have to be written by hand anyway.
- **Trade-offs:** time spent building the scaffolding OpenClaw already has.

## ADR-02 — Python

> **Superseded by ADR-33** (2026-11-27): C# .NET is the main language; Python only for `market`.

- **Options:** Python, C#.
- **Chosen:** Python.
- **Why:** the strongest AI/agent/bot ecosystem; reusable for the stock-analysis project.
- **Trade-offs:** C# (.NET), which is being studied at university, doesn't get practised in this project.

## ADR-03 — Use LLM APIs, don't run models locally

- **Options:** API (Claude/OpenAI); a local model on the Mac or a GPU PC.
- **Chosen:** API.
- **Why:** the strongest models for tool use; no hardware or electricity cost for running 24/7; GPU prices in Australia are very high.
- **Trade-offs:** vendor dependency, pay per token. Mitigated by the `LLMProvider` interface, which lets us switch vendors or move to a local model later.

## ADR-04 — Telegram is the first channel

- **Options:** Telegram, Zalo, Messenger, WhatsApp.
- **Chosen:** Telegram.
- **Why:** free bots via BotFather, a clear API, inline buttons (used for approvals), no business account needed.
- **Trade-offs:** tenants use Zalo — deferred to phase 7.

## ADR-05 — 5-layer architecture + 7-step pipeline

- **Chosen:** Channel · Orchestration · Policy · Capability · Infrastructure; data flows one way through 7 steps with fixed data contracts.
- **Why:** easy to control, each layer can be replaced without touching the others, each step can be tested, reusable for future agents.
- **Trade-offs:** more files than a simple script.

## ADR-06 — Policy layer in code, RiskLevel classification

- **Chosen:** every `ToolCall` goes through Policy; each tool declares READ / WRITE_SELF / EXTERNAL / FORBIDDEN; EXTERNAL needs approval; actual values are checked too.
- **Why:** rules in a prompt can be ignored or bypassed by prompt injection; code can't.
- **Trade-offs:** mail and outgoing messages need a tap to approve.

## ADR-07 — Routing before the agent loop

- **Chosen:** a cheap model or code classifies intent; structured tasks take a fixed path, open-ended messages go into the loop.
- **Why:** cheaper, faster and fewer errors for repetitive daily tasks (following Anthropic's "Building effective agents" guide).
- **Trade-offs:** an intent list to maintain; the router can misclassify → there is a fallback path into the loop.

## ADR-08 — Secretary + specialist bots (hub-and-spoke)

> **Amended by ADR-32** (2026-11-27): the Secretary has no domain tools; specialists answer through `ask_specialist`, not an `events` table.

- **Options:** (a) one bot does everything; (b) many independent bots; (c) a Secretary that drives specialist bots over shared data.
- **Chosen:** (c), split out gradually.
- **Why:** each area gets its own chat and its own notifications (market alerts don't get buried); the Secretary still controls everything via `ask_specialist`.
- **Rule:** flat hierarchy — only the Secretary calls other bots; specialist bots report back through the `events` table.
- **Trade-offs:** more tokens and config to manage; each call to a specialist costs an extra LLM turn.

## ADR-09 — One database: SQLite → PostgreSQL

- **Chosen:** SQLite in phases 1–4; PostgreSQL + pgvector once on a server and RAG is needed.
- **Why:** SQLite needs no server; the `Repository` interface allows switching without changing the upper layers.
- **Trade-offs:** migrations must be written carefully to move the data.

## ADR-10 — Write our own agent loop, no framework yet

- **Options:** write our own; LangGraph; OpenAI Agents SDK; Claude Agent SDK.
- **Chosen:** write our own.
- **Why:** to understand how it really works; a basic loop is only a few hundred lines; the framework isn't the bottleneck.
- **Revisit:** when building the multi-agent forecasting project.

## ADR-11 — Run locally during development, AWS VPS once stable

> **Superseded by ADR-35** (2026-11-27): production runs on the home server.

- **Chosen:** the Mac during development; a 1–2 GB RAM VPS on AWS once phase 3 is stable.
- **Why:** the bot only needs a few hundred MB of RAM because the LLM runs via API; practise AWS skills.
- **Trade-offs:** a monthly VPS cost; the server has to be managed by hand.

## ADR-12 — Invoices are only exported to a folder, not sent via Zalo

- **Context:** tenants use Zalo. Sending automatically by phone number needs a verified Zalo OA + ZNS (approved templates, paid per message). Automating a personal Zalo account risks getting it banned.
- **Options:** (a) ZNS; (b) semi-automatic via `zalo.me` links; (c) export files only, Huy sends them.
- **Chosen:** (c).
- **Why:** the MVP focuses on the most valuable part — calculating rent correctly; it removes all the risk and paperwork of a Zalo integration.
- **Trade-offs:** Huy sends ~50 invoices by hand each month.
- **Revisit:** once invoices have been consistently correct for 2–3 months. With a business registration + ID, ZNS is feasible: only a sending adapter is needed, the billing part stays the same.

## ADR-13 — Detailed rental data is kept for 3 months only

> Superseded by ADR-27.

- **Chosen:** invoice files, meter-book photos, readings and detailed calculation results older than 3 months are deleted automatically at the start of each month.
- **Why:** tidy, and less of other people's sensitive data to protect; 3 months is enough to check back when a tenant has a question.
- **Kept:** tenant info, rooms, unit prices; the latest month's readings (used as the "previous reading" next month).
- **How:** a scheduler job in plain code that logs how many files were deleted; the LLM has no delete tool (FORBIDDEN).
- **Trade-offs:** invoices older than 3 months can't be looked up. If they must be kept longer (tax, disputes), increase `retention.rental_months` in `settings.yaml`.

## ADR-14 — English for all project text

- **Context:** the docs, config, prompts and docstrings were written in Vietnamese.
- **Options:** (a) keep Vietnamese; (b) English for code only; (c) English for everything in the repo.
- **Chosen:** (c).
- **Why:** English is the norm for code and docs; the repo is readable by employers and other developers, which matters for a CV project; LLMs follow English prompts at least as well.
- **Not affected:** the bot still replies in the language Huy writes in (rule in `config/prompts/rules.md`); eval messages stay in Vietnamese because that's how Huy talks to the bot.
- **Trade-offs:** the external design document is still in Vietnamese.

## ADR-15 — Scheduled runs: read → select → verify → dedupe → send → confirm → commit

- **Status:** Proposed — finalise before phase 5 (morning brief, SEC-05) and phase 6 (market alerts, MKT-02; important-mail alerts, MAIL-01).
- **Context:** chat runs are triggered by Huy and answered once. Scheduled runs are different: nobody is watching, they read several sources, and they must neither miss an item nor report it twice. Reference: Anthropic's "Building effective agent automations" (claude.dev/blog/building-effective-agent-automations) and an independent summary map of it.
- **Chosen — the scheduled run loop:**
  1. **Read** — load preferences (config, read-only, always fresh), state, and each source from its bookmark.
  2. **Select** — keep only items that need attention or change a decision; skip items already in the ledger.
  3. **Verify** — re-check each item against the live source right before sending (deadline moved? mail already answered?); drop items that are resolved or can't be confirmed, and log them.
  4. **Dedupe** — look up today's titles in the ledger; never send the same item twice.
  5. **Send** — mark the delivery `posting`, then send to Telegram.
  6. **Confirm** — require Telegram's success response and message id.
     - Success → **commit**: mark the delivery `sent`, advance the bookmarks of the sources that were read successfully.
     - No / unclear answer → mark `held` (maybe posted); keep the ledger and bookmarks unchanged so the next run can retry safely.
- **Rules:**
  - **A failed read is not "nothing new".** If a source fails, report it in the brief ("Gmail could not be read"), keep its bookmark, and continue with the other sources.
  - **Read window overlaps** the previous run by 10 minutes, so items arriving at the boundary are not lost; the ledger removes the overlap duplicates. First run looks back 24 hours.
  - **Commit only when safe:** bookmarks and ledger change only after a confirmed send.
  - **Deliberate silence:** if nothing passes Select/Verify, send nothing (unless preferences ask for an "all clear"), but still commit the bookmarks.
  - Keep source links in the brief; don't reopen topics Huy has marked done.
- **Data:** `source_bookmarks` and `deliveries` tables (see data-dictionary.md, phase 5). `events.is_read_by_secretary` and `alerts_sent` fold into `deliveries`.
- **Why:** scheduled runs fail silently; without bookmarks, a ledger and confirm-before-commit, failures turn into missed or duplicate messages that nobody notices.
- **Trade-offs:** two extra tables and a more complex scheduled path than the chat pipeline.

## ADR-16 — Clean Architecture for the system, MVC only in channels; folders by layer, then area

- **Context:** files were flat inside each layer (`tools/reminders.py` held several tools, `postprocess.py` mixed formatting with business logic), tests were flat, and the dependency rule was only written in the README. Huy also wanted to combine MVC with Clean Architecture.
- **Options:** (a) top-level `models/ views/ controllers/` (web-framework MVC); (b) Clean Architecture layers, with MVC roles inside the channel layer only; (c) keep the flat layout.
- **Chosen:** (b).
- **Mapping to the Clean Architecture rings:**
  - Entities: `domain/` (contracts, ports, pure business rules such as `domain/rental/billing.py`).
  - Use cases: `orchestration/`, `policy/`, `tools/`.
  - Interface adapters: `channels/<channel>/controller.py` (MVC controller: raw input → `IncomingMessage` → pipeline), `channels/<channel>/presenter.py` (MVC view: `AgentReply` → channel message), and the port implementations in `infrastructure/`.
  - Frameworks & drivers: python-telegram-bot, SQLAlchemy, the Anthropic SDK; wired only in `main.py`.
  - MVC model = `domain/`.
- **Rules:**
  - Folders go **layer first, then area**: `tools/reminders/create.py` is the tool `reminders.create`; `domain/rental/` holds rental rules.
  - `postprocess.py` only stores pending actions; formatting, splitting and buttons belong to the presenter.
  - A layer imports only the layers below it (`main` → `channels | infrastructure` → `orchestration` → `policy | tools` → `domain`); `|` sides don't import each other. Inner layers never import telegram, sqlalchemy, alembic, yaml or dotenv. Checked by import-linter (`lint-imports`, config in `pyproject.toml`).
  - `tests/` mirrors `src/assistant/`; tests are grouped in `Test<ClassName>` classes; pytest runs with `--import-mode=importlib` so same-named test files can live in different folders.
- **Why:** the path tells you what a file is and which layer it belongs to; one file, one responsibility; the dependency rule is enforced by a tool instead of memory; MVC where it fits (input/output) without a second `models/` next to `domain/models.py`.
- **Trade-offs:** more small files and folders; one more dev tool.
- **Update:** the use-case folders moved into `application/` (ADR-19).

## ADR-17 — LLM input preprocessing (normalised + original text); verify with evals

- **Context:** most messages are Vietnamese with teencode ("ko", "nhma", "t"), missing diacritics and typos. Idea: a cheap model first translates to English, expands teencode, fixes spelling and rewrites the message in a standard form, so the strong model routes and decides more accurately with fewer tokens.
- **Options:**
  - (a) strong model gets the normalised English **and** the original text;
  - (b) strong model gets only the normalised English;
  - (c) no LLM preprocessing: the router and the strong model get the original text.
- **Evidence:**
  - Anthropic, "Building effective agents": use the simplest solution and add steps only when they demonstrably improve results; chaining model calls trades latency for accuracy.
  - Claude docs, "Multilingual support": strong models keep roughly 97–99% of their English score in other languages; cheap models drop more on low-resource languages. Vietnamese is not in the table, and no benchmark covers Vietnamese teencode. The docs do not recommend translating to English first; they recommend stating the reply language in the system prompt.
  - Etxaniz et al. 2023 ("Do Multilingual Language Models Think Better in English?"): translating to English first helped 2023-era models. Liu et al., NAACL 2025 ("Is Translation All You Need?"): translation is a strong baseline but not always best; native-language prompts keep cultural and language nuance.
  - Token cost: the user's message is under 1% of a strong-model call (system prompt, tool definitions and history dominate), so translating saves almost nothing.
  - Risk: a mistranslation ("1tr2", "mai" as a name instead of "tomorrow") propagates; in (b) the strong model can't detect it.
- **Chosen:** (a), with a switch `preprocessing.is_enabled` in `settings.yaml` (default `true`) so (c) can be compared on the same eval suite.
  - One cheap-model call, merged with the router (no extra call): returns the normalised English text, the intent and the entities.
  - The original text is always kept and sent to the strong model next to the normalised text (about +1% tokens).
  - Code checks that amounts, dates and room numbers in the normalised text match the original; on a mismatch the bot asks back instead of guessing.
  - The bot still replies in the language Huy writes in.
- **Not affected:** code-level cleaning still happens without an LLM: Unicode NFC normalisation, trimming, length limit, duplicate Telegram updates, time zone conversion.
- **Why (a) before measuring:** nothing can be measured yet (no router, agent loop or tools exist). Huy writes mostly teencode, and the router runs on a cheap model, which loses more accuracy outside English; keeping the original text removes the main risk of (b). The evidence above says the gain may be small, so this is verified, not assumed.
- **Verification rule (after phase 2):** run the `normalize` and `routing` eval groups with the switch on and off. Turn preprocessing **off** (option c) if the switch-off run is within 2 percentage points of the switch-on run; it is simpler and cheaper. Keep it on otherwise.
- **Trade-offs:** one more structured output to build and test in the router; a little more latency and cost per message until the evals show whether it is needed.


## ADR-18 — Branches, pull requests and a protected `main`

- **Context:** commits went straight to `main`. The project should follow the same process as a large company's team, both to learn it and so the history shows reviewed, checked changes.
- **Options:** (a) commit to `main` (fast, no review); (b) GitHub flow: short-lived branch per change, pull request, merge to a protected `main`; (c) Git flow with `develop` and `release/*` branches.
- **Chosen:** (b) GitHub flow.
  - Branch name `<type>/<short-description>`, same types as Conventional Commits.
  - Every change is merged through a PR that uses `.github/pull_request_template.md`.
  - `main` is protected on GitHub: PR required, no force-push, no deletion, rules apply to admins too.
  - Merge method: rebase and merge only, so every Conventional Commit stays on a linear `main`; branches are deleted after merging.
  - Next: CI (GitHub Actions) runs `ruff check .`, `lint-imports` and `pytest` on every PR and becomes a required check.
- **Why:** (b) is what most product teams use with continuous delivery; (c) adds release branches this project doesn't need.
- **Trade-offs:** a few more commands per change; a solo owner can't get a second approver, so the review is the owner reading the PR diff (and Claude reviewing it).
- **Rules:** docs/conventions.md §13.

## ADR-19 — Use cases live in `application/`

- **Context:** the use-case ring was split across three top-level folders (`orchestration/`, `policy/`, `tools/`). `orchestration` is not a name Clean Architecture readers recognise, and the top level mixed rings with parts of a ring.
- **Options:** (a) keep the three folders; (b) rename `orchestration/` to `application/` only; (c) one `application/` folder holding the pipeline steps, `policy/` and `tools/`.
- **Chosen:** (c). The top level of `src/assistant/` now shows exactly the rings: `domain/` (entities), `application/` (use cases), `channels/` and `infrastructure/` (interface adapters), `main.py` (composition root).
  - A second import-linter contract keeps the order inside `application/`: `pipeline` → `agent_loop | context_builder | postprocess | router` → `policy | tools`.
  - `tests/` follows: `tests/application/`, `tests/application/policy/`, `tests/application/tools/`.
  - `channels/` keeps its name: "channel" is the chatbot industry's word for Telegram, Teams, Slack, and the folder also holds the scheduler, so `presentation/` or `web/` would be wrong.
- **Why:** `application/` is the name used by the common .NET and Python Clean Architecture templates (`Domain / Application / Infrastructure / Web`); a reader sees the four rings at a glance.
- **Trade-offs:** one level deeper for tools (`application/tools/reminders/create.py`); every import of the moved modules changed once.

## ADR-20 — Market analysis joins the MVP (Secretary + Rental + Market)

- **Context:** Market was a "Could" area planned for phase 6. Huy decided that deep market analysis is a core goal of the project: answers that combine company figures, sector and supply-chain data, macro data, weather and seasons into a causal chain, not a single data point and a vague conclusion.
- **Options:** (a) keep Market in phase 6; (b) Market replaces Rental in the MVP; (c) Market is added to the MVP next to Secretary and Rental.
- **Chosen:** (c). New use case MKT-07 (deep multi-factor analysis) and MKT-08 (forecast log and scoring) are **Must**.
- **Why:** it is the part of the project Huy cares most about and the strongest CV piece; Rental stays because it solves a real monthly job.
- **Trade-offs:**
  - The MVP is bigger; Market needs a data layer (ADR-21) and source tools before any analysis is useful.
  - **Budget (open):** the MVP limit of $15/month was set without Market. A deep run calls the strong model several times; the limit must be re-checked once the first deep run is measured (`run_logs.cost_usd`).
- **Data model:** ADR-21, docs/market-data.md.

## ADR-21 — Five-axis data model for market evidence

- **Context:** to avoid shallow analysis, the agent must know how close each fact is to the subject, how far it can be trusted and whether it was public at the time. A single "quality" label mixes these up.
- **Options:** (a) store raw text and let the LLM judge relevance and quality; (b) one relevance tier + one quality grade; (c) five independent axes, computed or graded in code.
- **Chosen:** (c), described in docs/market-data.md:
  1. **Relevance tier 0–4**, computed from a factor-map **graph** (`config/market/factor_maps/<sector>.yaml`) as the shortest path to the subject; tier ≥ 2 evidence needs a path to tier 0.
  2. **Source reliability A–F** and 3. **information credibility 1–6**, graded separately (Admiralty Code).
  4. **Processing layer** bronze (`raw_records`) → silver (`observations`) → gold (`evidence`); the LLM reads gold only.
  5. **Time:** period, `published_at`, `ingested_at`, edge `lag_days`; point-in-time rule `published_at <= as_of`; seasonal data stored as deviation from the seasonal norm.
  - Every forecast goes into `forecasts` and is scored later; only forecasts after the LLM's training cut-off count.
- **Why:** customer–supplier links carry predictable information (Cohen & Frazzini 2008) and are best modelled as a graph; intelligence analysis grades source and information independently because merging them makes unconfirmed claims look confirmed; point-in-time data is the only way to test forecasts honestly, and LLM forecasts are inflated on periods inside their training data.
- **Trade-offs:** more tables and a factor map to write per sector; grading sources takes a track record that does not exist yet (new sources start at F).
- **Code:** `domain/market/` (`models.py`, `factor_graph.py`, `evidence_rules.py`) — pure rules, no I/O; loading YAML and fetching data belong in `infrastructure/`.


## ADR-22 — Sentiment and panic as a separate market-state signal

- **Context:** Huy wants the Market persona to recognise market panic, including from social-media posts and comments, so a deep analysis can say whether a move comes from fundamentals or from fear.
- **Options:** (a) LLM reads posts and judges the mood; (b) one social-media sentiment score as a factor like any other; (c) a market-state signal built from three families (market data, search attention, text), stored as deviation from baseline, linked to price only.
- **Chosen:** (c), described in docs/market-data.md "Sentiment and panic":
  - panic is declared only when at least two families cross their thresholds together; text alone never declares it;
  - social sources start at reliability F, credibility ≤ 3; a bot and coordination filter runs before counting;
  - only aggregates reach the LLM; raw posts are deleted after `retention.social_posts_days`; no scraping against a platform's terms;
  - output is a risk statement ("sentiment-driven, tends to revert"), never a buy or sell instruction.
- **Why:** the best-known social-mood result did not replicate; social sentiment predicts at most intraday moves; a large share of stock-tweet authors can be bots; media pessimism predicts a drop followed by reversion. Market data is harder to fake and anchors the signal.
- **Trade-offs:** thresholds need real data before they mean anything; social APIs may cost money or be unavailable for Vietnamese forums, in which case that family relies on the press and search data.
- **Threat model:** coordinated posts trying to steer the bot are a new attack path (add to threat-model.md before the first social source).

## ADR-23 — Quantitative layer: statistics and ML on past data, agents interpret and challenge

- **Context:** LLM calls are the main cost, LLMs are weak at numbers, and LLM forecasts on past periods are inflated by memorised outcomes. Huy proposed analysing past data with statistics and machine learning and keeping agents for interpretation and challenge.
- **Options:** (a) agents do everything; (b) models only, no agents; (c) models for what repeats in past data, agents for reading text, explaining, challenging models and handling events with no history ("quantamental").
- **Chosen:** (c), docs/market-data.md "Quantitative layer": baseline first, walk-forward validation on point-in-time data, every trial logged, model output stored as `evidence` (`kind = model`) with its validation figures.
- **Why:** models run free on the owner's machine and give reproducible numbers; ML return predictability is small but has real economic value (Gu, Kelly & Xiu); agents add what models cannot know.
- **Trade-offs:** a second skill set (statistics, ML) to learn and test; backtest overfitting is the main risk (Bailey et al.), hence the validation rules.
- **Code (later):** pure scoring rules in `domain/market/`; model fitting with statistics/ML libraries behind a port in `infrastructure/`.
- **Status:** Proposed — Huy is still evaluating the Market direction; Rental comes first.

## ADR-24 — Indicator trust that changes over time and by regime, earned from past results

- **Context:** an indicator that is reliable in one period may not be in another; Huy wants each indicator to carry a trust score based on its past results, so one indicator can be trusted more now and another more at a different time.
- **Options:** (a) fixed trust per indicator; (b) "optimal" weights re-estimated from recent errors; (c) time- and regime-dependent trust from scored past calls, shrunk toward equal weights by sample size.
- **Chosen:** (c), docs/market-data.md "Indicator trust": few code-defined regimes, scores per regime and horizon with exponential decay, shrinkage toward the average, sample size shown next to every score.
- **Why:** forecasting relations are unstable over time (Stock & Watson), and time-varying weights improved S&P 500 forecasts with economic gains (Ravazzolo et al.); but estimated weights are noisy and equal weights often win (forecast combination puzzle, Smith & Wallis), so trust must be earned slowly.
- **Trade-offs:** needs many scored calls before scores mean much; regime definitions are a judgement that must stay small and fixed in advance.
- **Status:** Proposed — same reason as ADR-23.

## ADR-25 — Microservices split by business area: assistant, rental, market, finance

- **Context:** everything lived in one `assistant` package. Huy wants Rental (and later Market and Finance) to stand on their own: usable from other clients such as a billing website, able to scale on their own, and able to join a bigger system instead of being one closed app. He also wants a strong business-logic structure to show in interviews.
- **Options:** (a) keep one app; (b) a modular monolith, split later; (c) microservices now.
- **Chosen:** (c). Claude advised (b) first; Huy chose (c), knowing the extra work.
  - **Split by business area, not by layer.** `assistant`: Telegram, pipeline, LLM, personas, policy, chat memory, API cost, and at first reminders and to-dos (moved to the study app by ADR-28). `rental`: rooms, tenants, meter readings, bills, invoices, the retention clean-up (ADR-13, changed to 12 months by ADR-27). `market`: market data, graded evidence, forecasts and scores (ADR-20 to ADR-24). `finance`: expenses, budgets, reports (FIN-*). Later: `rental-web` (website for billing), `identity` (sign-in).
  - **When something becomes a service:** it has its own data, its own business rules, and a reason to stand alone (another client, its own scaling or schedule). Otherwise it stays a module in `assistant`; this is why reminders and to-dos first stayed there (later ADR-28).
  - **One-way calls:** `assistant` calls the other services; they never call `assistant`. No service imports another service's code (import-linter contracts in every `pyproject.toml`).
  - **One database per service:** one PostgreSQL server later, with its own database and user per service; no joins across services, ids are UUIDs. This replaces the single database of ADR-09.
  - **Between services: gRPC** with versioned contracts in `proto/` (rules in a later ADR); REST/JSON only at the edge (websites).
  - **The LLM stays in `assistant`:** for example the meter photo (RENT-01) is read by the assistant's LLM; `rental` only receives the table of numbers.
- **Why:** it matches Huy's goal (independent, integrable services) and makes each area's business rules stand alone and easy to test.
- **Trade-offs:** network calls that can fail or time out, several processes to run and deploy, contracts to version, data spread over several databases, and more set-up before the first feature works.

## ADR-26 — Monorepo with one folder per service under `services/`

- **Context:** ADR-25 needs a place for several services.
- **Options:** (a) one repository per service; (b) one repository (monorepo) with a folder per service.
- **Chosen:** (b).
  - `services/<name>/` holds that service's `pyproject.toml`, `src/<name>/`, `tests/`, and if it has them `config/`, `data/`, `migrations/`, `.env.example` (later its `Dockerfile`). `docs/` and `.github/` stay at the root; `proto/` is added at the root with the first contract.
  - `assistant` keeps Clean Architecture inside (ADR-16, ADR-19). `rental`, `market` and `finance` follow Domain-Driven Design ("Architecture Patterns with Python"): `domain/` first, then `application/`, `infrastructure/`, `entrypoints/` as they are written; their layer contracts are added together with `application/`.
  - Paths moved: `src/assistant/` → `services/assistant/src/assistant/`; `domain/rental/` → `services/rental/src/rental/domain/`; `domain/market/` and `config/market/` → `services/market/`. Older ADRs keep the old paths as history.
  - **CI:** one job per service (matrix) runs `ruff check .`, `lint-imports` and `pytest` inside its folder; a summary job keeps the name `checks`, the required check on `main` (ADR-18). Later: run only the services a PR changes.
  - **Same rings everywhere:** `domain/`, `application/`, `infrastructure/`, `entrypoints/`, `main.py` in every Python service, mapped one to one to `<App>.Domain / .Application / .Infrastructure / .Api|.Web / Program.cs` in the .NET study app (docs/conventions.md §9). So `assistant`'s `channels/` is renamed `entrypoints/` (`entrypoints/telegram/`, `entrypoints/scheduler/`); this replaces the folder-name choice in ADR-19, and "channel" stays the word for Telegram, Teams and the scheduler inside it.
  - **Local:** one `.venv` at the root with every service installed in editable mode; run the tools inside the service folder.
- **Why:** one PR can change a contract and both sides at once, one CI file, simple for a solo owner, and the history stays in one place. A service can still be split into its own repository later (`git filter-repo`).
- **Trade-offs:** CI runs every service on every PR until path filters are added; keeping services apart depends on the import-linter contracts, not on separate repositories.

## ADR-27 — Rental keeps readings and bills for 12 months, meter-book photos for 3

- **Context:** ADR-13 deleted every detail older than 3 months. Leases run 6 to 12 months, so a deposit question at move-out can need readings from much earlier; RENT-10 (income by quarter and year) and year-end records need a full year; and the meter-book photos are the most personal part of the data.
- **Options:** (a) keep 3 months for everything (ADR-13); (b) keep 12 months for everything; (c) 12 months for readings, invoices and calculation results, 3 months for meter-book photos.
- **Chosen:** (c).
  - Kept 12 months: invoice files, confirmed readings, detailed calculation results.
  - Kept 3 months: meter-book photos. Once Huy has confirmed the table of numbers (RENT-01), the confirmed readings are the record; the photo is only a backup check.
  - Never deleted by this rule: tenant details, rooms, unit prices, and the latest month's readings (the "previous reading" for next month).
  - Run by the `rental` service (ADR-25) as a scheduled job in plain code at the start of each month; it logs how many rows and files it deleted. The LLM has no delete tool (FORBIDDEN).
  - Settings: `retention.details_months: 12` and `retention.meter_photos_months: 3` in `services/rental/config/settings.yaml`.
  - Backups follow the same limit: a backup is deleted after at most 12 months, so data removed from the database does not live on in old backups.
- **Why:** a full year covers a whole lease and a whole tax year; photos go early because they carry the most personal detail and are no longer needed once the numbers are confirmed.
- **Trade-offs:** four times as long a window of tenants' data to protect (access rules, encryption at rest when deployed); a dispute about a photo older than 3 months can only be checked against the confirmed numbers.

## ADR-28 — The planner belongs to the study app (own repository, .NET); the assistant is its client

- **Context:** reminders, to-dos, calendar, study deadlines, exams and habits ("the planner") were planned inside `assistant` (SEC-02, 03, 04, 08; EDU-01, 02). Huy's second project, a study web app (.NET, many users, deployed on AWS), has deadlines, exams and an AI study schedule as its MVP, and will grow into managing a student's life. Both would need the same planner data.
- **Options:** (a) keep the planner as a module in `assistant`; (b) `services/planner/` in this monorepo; (c) the study app owns the planner, in its own repository, and `assistant` calls it.
- **Chosen:** (c).
  - The study app is a separate product (its own users, sign-in, .NET tooling, security scans, AWS deployment), so it gets its own repository; the four services here stay in this monorepo (ADR-26).
  - The study app owns the planner data and its gRPC contract (`.proto`); `assistant` copies the contract and keeps thin tools (`reminders.*`, later `todos.*`, `deadlines.*`) that call it.
  - Calls go one way: `assistant` → study app. When a reminder is due, the study app publishes an event (or, at first, `assistant` asks every minute for due reminders) and `assistant` sends the Telegram message.
  - `assistant` acts on Huy's behalf in the study app through its sign-in (OAuth, designed with the identity work); every planner row has a `user_id` from day one because the study app has many users.
  - Both repositories follow the same structure and naming (docs/conventions.md §9).
  - **MVP:** reminders and to-dos (SEC-02, 03) leave the assistant MVP; they arrive when the study app's planner exists. The assistant MVP is SEC-01, 07 + Rental + Market.
- **Why:** one planner for the bot and the web app instead of two copies of the same data; the study app's MVP already covers it; a Python bot calling a .NET service in another repository through a versioned contract is the integration Huy wants to show.
- **Trade-offs:** no reminders in the bot until the study app's planner is built; a change that needs both sides takes two pull requests (server first, then client); the bot depends on the study app being up, so the tools must fail gracefully ("can't reach the planner, try again later").

## ADR-29 — Telegram webhook in every environment, ready for several replicas

> **Superseded by ADR-31** (2026-11-19): the bot keeps long polling. Never implemented.

- **Context:** the bot asks Telegram for new messages (`run_polling()`). Only one process can poll a bot, so `assistant` could never run more than one copy, and the server setup (tunnel, HTTPS) would first be tested only at deployment.
- **Options:** (a) keep polling; (b) polling on the laptop, webhook on the server, chosen by a setting; (c) webhook everywhere.
- **Chosen:** (c). Telegram sends each update as an HTTPS POST to the bot (`run_webhook()` of python-telegram-bot, `python-telegram-bot[webhooks]`).
  - **One path per bot:** `/telegram/<persona>` (e.g. `/telegram/secretary`), on one port; the public base URL comes from `TELEGRAM_WEBHOOK_BASE_URL`.
  - **Secret header:** the webhook is registered with `TELEGRAM_WEBHOOK_SECRET`; Telegram sends it in `X-Telegram-Bot-Api-Secret-Token` and any request without it is rejected, so nobody can pretend to be Telegram.
  - **Laptop:** a temporary tunnel gives a public HTTPS URL (`cloudflared tunnel --url http://localhost:8080`, no account needed); a separate **dev bot** from BotFather, because a bot with a webhook cannot be polled and the real bot must not receive test traffic.
  - **Server:** the same code behind the server's tunnel and HTTPS; only `.env` differs.
- **Ready for several replicas** (rules for the code that follows):
  - no conversation state in memory: history, memory and pending actions live in the database;
  - **idempotent updates:** Telegram can send an update again, so the processed `update_id`s are stored and a repeat is skipped;
  - **one scheduler:** scheduled jobs take a database lock so only one replica runs each job (ADR-15);
  - answer Telegram quickly (within seconds); long work continues after the reply is acknowledged.
- **Why:** dev and server run the same way (dev/prod parity), webhook problems show up on the laptop, and the bot can scale out behind a load balancer.
- **Trade-offs:** a tunnel must be running for every local run; two bots to manage; the bot is reachable from the internet, so the secret header and the owner check (`AccessPolicy`) both matter.

## ADR-30 — Apps in `apps/`, business services in `services/`

- **Context:** ADR-26 put all four parts side by side under `services/`. They do different jobs: `assistant` is what people talk to (Telegram channels, the agent, personas, policy) and owns no business data of rental, market or finance; it only calls them. Huy found the flat list misleading, and more front ends are coming (`rental-web`, maybe Zalo as another channel of `assistant`).
- **Options:** (a) keep everything in `services/` and write the roles down; (b) group by role: `apps/` for what people use, `services/` for business areas; (c) the JavaScript-monorepo style `apps/` + `libs/`, where every deployable (services too) is an app.
- **Chosen:** (b).
  - `apps/<name>/`: what people use; calls services over gRPC (ADR-25). Now `assistant`; later `rental-web`. A new chat channel (e.g. Zalo) is not a new app: it is another `entrypoints/<channel>/` inside `assistant`.
  - `services/<name>/`: one business area each, with its own data; candidates to move to their own repository one day. Now `rental`, `market`, `finance`.
  - **Direction:** apps → services, never back; services never import or call apps; nothing imports across folders (import-linter in every package).
  - Everything else from ADR-26 stays: each folder has its own `pyproject.toml`, `src/<name>/`, `tests/`, config and later `Dockerfile`; `docs/`, `.github/` and later `proto/` stay at the root. CI runs one job per app and service.
  - Paths moved: `services/assistant/` → `apps/assistant/`. Older ADRs keep the old path as history.
- **Why:** the tree shows the dependency direction at a glance; front ends have an obvious home; the services that could become their own product or repository are the ones under `services/`.
- **Trade-offs:** two top-level folders instead of one; the move touched CI, README and docs once; each local virtualenv must reinstall `assistant` from its new path. Option (c) was rejected because there every service would also be an "app", which hides the difference this ADR is about.

## ADR-31 — Telegram stays on long polling; one owner, one process

- **Context:** ADR-29 chose webhooks so `assistant` could run several copies. The bot has one user (Huy, owner-only through `AccessPolicy`) and one channel (Telegram); there will be no tenant chat or other channels. One process handles that load easily, and the server is a home machine behind a router, not a load-balanced cloud host.
- **Options:** (a) long polling everywhere; (b) polling on the laptop, webhook on the server; (c) webhook everywhere (ADR-29).
- **Chosen:** (a). `Application.run_polling()` from python-telegram-bot, on the laptop and on the server.
  - **One process per bot token:** Telegram allows only one poller per token, so the laptop uses a separate **dev bot** from BotFather while the server runs the real one.
  - No public URL, tunnel, inbound port or webhook secret; `TELEGRAM_WEBHOOK_*` and the `telegram.webhook_*` settings are removed.
  - Conversation state still lives in the database, not in memory, so a restart loses nothing.
- **Why:** the reasons for ADR-29 (replicas, serverless, load balancer) do not apply to a single-owner bot. Polling needs only outgoing HTTPS, so the home server opens no port to the internet: less to configure and less to attack. Long polling holds the request open until a message arrives, so replies are just as fast.
- **Trade-offs:** `assistant` cannot run more than one copy per bot; if that is ever needed, a new ADR brings webhooks back (ADR-29 has the design). Two bots to manage (dev and real). Each poll is an open outgoing connection that the server keeps up.

## ADR-32 — Two tiers of bots: a Secretary that routes, specialists that hold the tools

- **Context:** in ADR-08 the Secretary had its own tools (reminders, tasks, calendar) and could also call specialists. More areas are coming (life, rental, finance, market, later more), and a bot that holds every tool gets a long tool list: more tokens per call and a worse choice of tool. Huy also wants to talk to each specialist directly, like asking the right department instead of the front desk.
- **Options:** (a) keep ADR-08 as it is; (b) one bot with every tool, and the router picks a subset per message; (c) two tiers: a Secretary with no domain tools, and specialists that own the tools.
- **Chosen:** (c). This amends ADR-08.
  - **Orchestrator tier, the Secretary:** no domain tools. It has a directory of specialists (name and what each one handles) and one tool, `ask_specialist`. It splits a request that spans several areas, asks each specialist, and combines the answers.
  - **Specialist tier:** `life`, `rental`, `finance`, `market`, and more later. Each one holds the tools of its area and is its own Telegram bot, so Huy can chat with it directly.
  - **All bots live in `apps/assistant`:** one bot = one persona file (`config/personas/<name>`) + one bot token. One codebase; one process per bot token (ADR-31). A new bot needs no new app.
  - **Tool rules:**
    - a **write** tool only acts on the specialist's own service (the rental bot writes to `rental`, never to `finance`);
    - **read-only** tools on other services are allowed, the fast path (the finance bot may read rent income from `rental`);
    - specialists never call each other; work across areas goes through the Secretary.
  - A specialist's answer goes back to the Secretary as the result of `ask_specialist`. This replaces ADR-08's rule that specialists report back through an `events` table.
- **Why:** each bot sees a short, relevant tool list, so tool choice stays good as areas grow; each area's tools stay apart; Huy can go straight to the right bot.
- **Trade-offs:** a question that goes through the Secretary costs at least two LLM calls; one token per bot (plus a dev bot each) to manage; the directory descriptions must stay accurate or the Secretary asks the wrong specialist.

## ADR-33 — C# .NET is the main language; the code restarts from scratch

- **Context:** ADR-02 chose Python. Huy studies C# at university and is aiming for jobs in Australia where .NET is widely used. He can read the Python code but found it hard to write new code in it, most commits so far reshaped the structure, and most of the code is still `TODO` stubs. The study app (ADR-28) is already .NET.
- **Options:** (a) keep Python; (b) C# only for new parts, Python stays; (c) C# for everything except where Python clearly wins, and restart the code.
- **Chosen:** (c). This supersedes ADR-02.
  - **C#:** `apps/assistant`, `services/rental`, `services/finance`, later `apps/rental-web`.
  - **Python:** only `services/market` (data, statistics, machine learning; ADR-23). Any other Python part needs a new ADR.
  - **Restart in this repository:** the Python code of `assistant`, `rental` and `finance` is removed in one commit; git history keeps it. Older ADRs stay as history; their Python paths, libraries and tools (Pydantic, import-linter, ruff, python-telegram-bot) are historical.
  - **Design that stays:** the 7-step pipeline (ADR-05), Policy and `RiskLevel` (ADR-06), routing before the loop (ADR-07), our own agent loop (ADR-10), Clean Architecture rings (ADR-16, ADR-19), the monorepo (ADR-26), `apps/` and `services/` (ADR-30), long polling (ADR-31).
  - **.NET layout:** each app and service has its own solution so it builds alone, with one project per ring (`<Name>.Domain`, `<Name>.Application`, `<Name>.Infrastructure`, and an entry point such as `<Name>.Bot` or `<Name>.Api`) plus test projects. Project references enforce the rings (Domain references nothing; nothing references the entry point), replacing import-linter. Details are written with the skeleton.
  - **Main libraries:** the official Anthropic C# SDK, Telegram.Bot, EF Core, Grpc.AspNetCore, xUnit.
  - **Who writes what:** Huy writes all code in `src/`, the tests and `Program.cs`, and runs git and `dotnet` commands; Claude writes config, CI and docs, explains them, and reviews.
- **Why:** practise the language of university and the job market; go deep in one ecosystem instead of shallow in two; types catch mistakes at build time; the same stack as the study app.
- **Trade-offs:** the Python work is thrown away and the first working bot comes later; .NET has fewer ready-made AI agent libraries than Python, which matters little because we write our own loop (ADR-10); two languages in one repository means two toolchains in CI.

## ADR-34 — Service boundaries: data only through APIs, sensitive data away from AI

- **Context:** two tiers of bots (ADR-32) and several services raised new questions: may services call each other, should there be a shared database or copies of data, where do ID-card numbers go, where may an LLM run, which format goes between parts, and is a sign-in service needed. The choice of microservices was also questioned again.
- **Chosen:**
  - **Microservices stay (ADR-25).** Each app and service has its own process, database, database user (granted only on its own database), build and deploy, so one can be changed, built or broken without breaking the others. A modular monolith was considered again and rejected for this reason.
  - **Calls:** gRPC with contracts in `proto/`. Apps call services. A service may call another service's **read** API directly; writes go only through the service that owns the data; no call cycles.
  - **Data:** a service's database is internal. Shared data leaves only through its API. No shared database and no copies: Finance reads rent income from Rental's API when it needs it, so retention (ADR-27, 12 months) lives in one place.
  - **Sensitive data** (ID-card numbers and photos):
    - only through an owner-only endpoint in `rental`, used only by `rental-web`;
    - every read is logged (audit);
    - numbers are masked by default and shown in full only on request;
    - stored encrypted;
    - never in a prompt, LLM call, tool result, Telegram message or log.
  - **No identity service:** sign-in lives in `apps/rental-web` (ASP.NET Core Identity) when it is built. This drops the `identity` service planned in ADR-25.
  - **Where AI runs:**
    - agents (an LLM with tools in a loop) live only in `apps/assistant`;
    - a bot uses the LLM to turn messy input (a photo, free text) into structured data before it calls a tool;
    - a service may call an LLM as a plain function in a background job (for example market sentiment, ADR-22), behind a port, with its own budget, and never with sensitive data.
    This refines ADR-25's "the LLM stays in `assistant`".
  - **Formats:**
    - the LLM returns JSON that is checked against a schema (tool use or structured output);
    - services exchange protobuf over gRPC;
    - files (photos, invoices) are stored by the service that owns them and passed by id;
    - plain text is only for people.
    Data made by AI carries `confidence`, `source` and `confirmed` (false until Huy confirms).
- **Why:** each part builds, deploys and fails alone; one owner per piece of data, so no copies drift apart; the most personal data never reaches a third party or a chat app.
- **Trade-offs:** when a service is down, reads from it fail, so tools must say so ("can't reach rental, try again later"); no joins across services; the owner-only endpoint, audit and encryption are extra work.

## ADR-35 — Personal scope, home server, architecture freeze

- **Context:** discussions drifted to selling the rental part to other landlords, a company brand and app stores. ADR-11 planned an AWS VPS, but Huy now has a home server. Many commits reshaped the structure before any feature worked.
- **Chosen:**
  - **Personal only:** one owner (Huy); family members later through `rental-web`. No preparation for other users (no `landlord_id`), no SaaS, no app stores. A rental product for other people would be a separate app in a separate repository.
  - **Home server:** apps and services run on the home server (an ASUS TUF laptop with Ubuntu). Long polling needs only outgoing HTTPS (ADR-31), so no port is opened to the internet. This supersedes ADR-11. AWS practice moves to the study app (ADR-28).
  - **Architecture freeze:** no new structure decisions until (1) a bot answers a real Telegram message with Claude and (2) rent is billed once from start to finish. New ideas go to [ideas.md](ideas.md). Choices inside the design (a library, a table, a tool) are still made as they come.
- **Why:** a clear scope stops design work that serves no real need; the home server costs nothing per month; the freeze turns effort into working features.
- **Trade-offs:** the home server is a single point of failure (power, internet, disk), so backups and a restart plan in the runbook matter; ideas that need a structure change wait until the freeze ends.

## ADR-36 — No link to the study app; the planner lives in `assistant` under the Life bot

- **Context:** ADR-28 gave the planner (reminders, to-dos, calendar, study deadlines) to Huy's separate study app, and the assistant would call it. Huy decided the two projects stay completely apart: this project never depends on the study app. ADR-28 also left the bot without reminders until another product was built.
- **Options:** (a) the planner is a module in `assistant`, owned by the Life bot; (b) a new `services/planner/`; (c) keep ADR-28.
- **Chosen:** (a). This supersedes ADR-28.
  - Reminders, to-dos and calendar (LIFE-01 to LIFE-03) and study deadlines (EDU-01, 02) are tools inside `assistant`, with their tables in the assistant's own database. The Life bot owns reminders, to-dos and calendar; the Learning bot owns study deadlines.
  - It stays a module, not a service, by ADR-25's rule: no other client needs this data, so there is no reason for it to stand alone.
  - No `user_id` for many users, no OAuth into another app, no shared `.proto`: one owner (ADR-35).
  - Nothing in this repository refers to the study app any more. The study app may copy these conventions, but this repository does not keep them in step.
  - **Architecture freeze (ADR-35):** this removes an integration instead of adding one, so it is allowed during the freeze.
- **Why:** the project builds and runs alone; reminders no longer wait for another product; less to build (no cross-repository contract, no sign-in between apps).
- **Trade-offs:** if the study app later needs the same planner data, the two hold separate copies, and that is accepted. The "C# bot calls a .NET service in another repository" integration is no longer shown here; `rental` and `finance` over gRPC still show it inside the monorepo.

## ADR-37 — Life owns everything with a date; `rental` is renamed `housing`

- **Context:**
  - Daily-life work was split across bots: reminders and calendar in Life, study deadlines and study schedule in Learning (ADR-36). Huy thinks of all of it as "my life": one place for what is due and when.
  - Huy wants the area named by what it is about, housing, rather than by one activity.
- **Options for Life:**
  - (a) Life takes everything about learning as well;
  - (b) Life takes everything that has a date or a to-do, and Learning keeps the teaching;
  - (c) keep ADR-36.
- **Chosen:** (b), and the rename.
  - **Life** owns reminders, to-dos, calendar, study deadlines and study schedule (EDU-01, 02 become LIFE-05, 06), and workouts. One `deadlines` list for every kind of deadline.
  - **Learning** keeps the teaching and career work: explaining lectures, PTE practice, flashcards, internship applications (EDU-03 to 05, CAR-*). Its own deadlines go to Life through the Secretary.
  - **`rental` becomes `housing`:** the service (`services/housing`), the bot and persona (`housing`), the tools (`housing.*`), the token (`TELEGRAM_TOKEN_HOUSING`) and the future website (`housing-web`).
    - It covers the rooms Huy rents out. RENT-01 to RENT-10 keep their IDs, so older ADRs still point to them.
    - The rent Huy pays for his own room, and his household bills, are only expense categories in `finance` (FIN-01). Housing holds no data about Huy's own home, so his own payments never mix with rent income or with the tenants' data.
  - The ID-card endpoint of ADR-34 is now a `housing` endpoint; the rule does not change.
  - **Architecture freeze (ADR-35):** no new ring, service or integration, only names and which bot holds which tools. That is allowed during the freeze.
  - Older ADRs keep the word `rental` as history.
- **Why:**
  - One bot answers "what's due this week?", whatever the deadline is about.
  - Learning's tool list stays short and its prompt stays a teacher's (ADR-32). Option (a) would give Life a long tool list and two jobs.
  - `housing` names the area by what it covers, not by one activity inside it.
- **Trade-offs:**
  - Life's tool list grows: about 6 groups. If tool choice gets worse, split it again.
  - A rename across docs and config now; cheap because the C# code for `housing` does not exist yet.

## ADR-38 — Research merges into Learning; a daily science digest

- **Context:** the Research bot (Scientist) explained papers and scientific terms, learned new topics and sent new papers weekly. The Learning bot explains lectures and runs PTE practice. Both do the same job: help Huy understand and learn. Huy also wants science updates every day, not only every week.
- **Options:**
  - (a) keep two bots;
  - (b) merge Research into Learning;
  - (c) merge both into Life.
- **Chosen:** (b).
  - The **Learning** bot covers study, science and career: lectures, PTE, flashcards, scientific papers and terms, new topics, notes, and internship applications. SCI-01 to 05 keep their IDs.
  - It takes Research's tools: `papers.*`, `web.search`, `notes.save` and `research.subagent`.
  - **SCI-06, new:** a morning science newspaper: what the world discovered or invented, written for a general reader like a news page, not a list of papers.
    - At most 5 stories a day, each a headline, 2–3 plain sentences and its source.
    - Under each story the bot offers Telegram buttons: summarise it, explain the science, go deeper. Huy picks one, and the bot answers in the same chat.
    - It is a scheduled run (ADR-15): read the sources, pick, check, drop what was already sent, then send.
    - The weekly papers (SCI-04) stay.
  - The `research` persona, prompt and Telegram token are removed.
  - **Architecture freeze (ADR-35):** this removes a bot instead of adding one, so it is allowed during the freeze.
- **Why:** one bot for "explain this to me", whether the question comes from a lecture or a paper; one notes store for both; one bot fewer to run. Option (c) would mix a teacher's job into the life manager (ADR-37).
- **Trade-offs:**
  - Learning's tool list grows to about 8 groups. If tool choice gets worse, use tool search (`docs/ideas.md`) or split it again.
  - The daily digest costs about 7 times as much as the weekly one. The 5-item cap and a cheap model for picking keep it small; `run_logs` shows the real cost.

## ADR-39 — Email and Documents merge into Life; each specialist sends its own report at its own pace, only when there is news; one file store, summaries kept by each area

- **Context:**
  - Mail and files are part of Huy's daily life, and mail often holds the dates Life already tracks.
  - Huy wants each specialist to report on its own area, at the pace of that area, not one combined brief from the Secretary. Areas that change slowly, like housing, report once a month, and no bot sends a report with nothing in it.
  - Huy wants one place that keeps every document, while each area still owns what the documents mean. For example, Learning summarises lectures and keeps those summaries itself.
- **Chosen:**
  - **Life takes Email and Documents.** MAIL-01 to 04 and DOC-01 to 05 keep their IDs. The `email` and `documents` personas, prompts and tokens are removed.
    - Sending mail stays EXTERNAL: every mail waits for Huy's approval (ADR-06).
    - Mail content is data, not instructions (threat model T-01).
  - **Reports, one per specialist:**
    - Each specialist sends its own report in its own chat, on the schedule set in its persona (`report.every`, `report.at`).
    - **Nothing to report, nothing sent:** a report with no items is skipped, never sent as "nothing new".
    - Each report is a scheduled run (ADR-15), so nothing is missed or sent twice.
    - Each report can be turned off on its own.
    - Something urgent (a lease about to expire, a budget overrun, a big market move) is still sent when it happens, as an alert, without waiting for the report.
    - Pace and contents:
      - **Life, daily:** today's plan, reminders, deadlines, important mail.
      - **Learning, daily:** the morning science newspaper (SCI-06) and what is due to study.
      - **Market, every trading day:** the market report (MKT-01).
      - **Housing, monthly:** rent collected and still owed, leases expiring next month, open repairs.
      - **Finance, monthly:** last month's spending against budget and cash flow (FIN-04).
    - The Secretary's combined morning brief (SEC-05) is dropped, and the Secretary sends nothing on a schedule.
  - **One file store, summaries by area:**
    - Life keeps one store for every file Huy sends (DOC-01): the original file once, plus its type, its area tag and the course or topic.
    - The specialist of that area reads the file, summarises it and keeps the summary in its own tables. For example, Learning writes lecture summaries per course to `learning_notes`.
    - Other bots find files through read-only `docs.search` and `docs.ask` (ADR-32).
  - **Exception:** housing files (meter photos, invoices, leases, ID cards) stay in the `housing` service and never enter the shared store (ADR-34). Identity, visa and bank documents in the store keep only their metadata; their content never goes to the LLM.
  - **Architecture freeze (ADR-35):** this removes two bots and a combined brief; the store and the summary tables are tables inside `assistant`. That is allowed during the freeze.
- **Why:**
  - Mail, files and dates sit with one bot.
  - Each report comes from the bot that knows the area, so Huy can reply to it in the same chat. A pace per area and no empty reports keep the messages few and worth reading.
  - A file is stored once, but its summary lives where it is used.
- **Trade-offs:**
  - Life's tool list grows to about 9 groups. If tool choice gets worse, use tool search (`docs/ideas.md`) or split Email out again.
  - Up to 3 messages on a normal morning and 2 more at the start of the month, instead of one brief; each report can be turned off. A skipped report could hide a bot that stopped working, so `run_logs` records every report run, sent or skipped.
  - A summary can go stale if the file is replaced, so every summary keeps its `document_id`.
