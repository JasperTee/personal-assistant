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
| ADR-09 | One database: SQLite → PostgreSQL | Accepted | 2026-11-09 |
| ADR-10 | Write our own agent loop, no framework yet | Accepted | 2026-11-09 |
| ADR-11 | Run locally during development, AWS VPS once stable | Accepted | 2026-11-09 |
| ADR-12 | Invoices are only exported to a folder, not sent via Zalo | Accepted | 2026-11-11 |
| ADR-13 | Detailed rental data is kept for 3 months only | Accepted | 2026-11-11 |
| ADR-14 | English for all project text | Accepted | 2026-11-11 |
| ADR-15 | Scheduled runs: read → select → verify → dedupe → send → confirm → commit | Proposed (phase 5) | 2026-11-11 |
| ADR-16 | Clean Architecture for the system, MVC only in channels; folders by layer, then area | Accepted | 2026-11-11 |

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

