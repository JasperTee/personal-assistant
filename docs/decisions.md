# Decisions (ADR)

Each decision: context → options → chosen → why → trade-offs. Never delete an old decision; if you change your mind, add a new one and mark the old one "Superseded by ADR-xx".

| ID | Decision | Status | Date |
| --- | --- | --- | --- |
| ADR-01 | Build our own instead of using OpenClaw | Accepted | 2026-11-09 |
| ADR-02 | Python | Accepted | 2026-11-09 |
| ADR-03 | Use LLM APIs, don't run models locally | Accepted | 2026-11-09 |
| ADR-04 | Telegram is the first channel | Accepted | 2026-11-09 |
| ADR-05 | 5-layer architecture + 7-step pipeline | Accepted | 2026-11-09 |
| ADR-06 | Policy layer in code, RiskLevel classification | Accepted | 2026-11-09 |
| ADR-07 | Routing before the agent loop | Accepted | 2026-11-09 |
| ADR-08 | Secretary + specialist bots (hub-and-spoke) | Accepted | 2026-11-09 |
| ADR-09 | One database: SQLite → PostgreSQL | Superseded by ADR-25 (one database per service) | 2026-11-09 |
| ADR-10 | Write our own agent loop, no framework yet | Accepted | 2026-11-09 |
| ADR-11 | Run locally during development, AWS VPS once stable | Accepted | 2026-11-09 |
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
| ADR-25 | Microservices split by business area: assistant, rental, market, finance | Accepted; reminders and to-dos moved by ADR-28, retention changed by ADR-27 | 2026-11-18 |
| ADR-26 | Monorepo with one folder per service under `services/` | Accepted; `assistant` moved to `apps/` by ADR-30 | 2026-11-18 |
| ADR-27 | Rental keeps readings and bills for 12 months, meter-book photos for 3 | Accepted | 2026-11-18 |
| ADR-28 | The planner belongs to the study app (own repository, .NET); the assistant is its client | Accepted | 2026-11-18 |
| ADR-29 | Telegram webhook in every environment, ready for several replicas | Accepted | 2026-11-18 |
| ADR-30 | Apps in `apps/`, business services in `services/` | Accepted | 2026-11-19 |

---

## ADR-01 — Build our own instead of using OpenClaw

- **Context:** OpenClaw is an open-source assistant with multi-channel support, memory and skills out of the box.
- **Options:** (a) install OpenClaw; (b) build our own, borrowing ideas from OpenClaw's architecture.
- **Chosen:** (b).
- **Why:** the goal is learning and a CV project; OpenClaw has a worrying security history (instances exposed to the internet, malicious skills on ClawHub) while this agent will read mail and tenant data; the custom needs (rent calculation, market) have to be written by hand anyway.
- **Trade-offs:** time spent building the scaffolding OpenClaw already has.

## ADR-02 — Python

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
