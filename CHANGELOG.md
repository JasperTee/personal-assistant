# Changelog

Record every finished phase or significant change. Newest first.

## [Unreleased]

### Changed
- The code restarts in C# .NET (ADR-33): the Python code of `assistant`, `rental` and `finance` is removed; `apps/assistant` is a .NET solution with `Assistant.Domain`, `.Application`, `.Infrastructure`, `.Bot` and two test projects. `services/market` stays Python.
- Shared .NET build settings (`Directory.Build.props`: .NET 10, nullable, warnings as errors, recommended analyzers), SDK pinned in `global.json`, code style in `.editorconfig`, LF line endings in `.gitattributes`.
- CI builds, checks formatting and tests each .NET solution, and keeps the Python checks for `market`; `checks` stays the required job.
- README, conventions (C# naming, tests, doc comments), runbook, PR template and data dictionary updated for .NET.
- The Life bot is written into the plan (ADR-32): requirements get a Life area and LIFE-01 to LIFE-04 (moved from SEC-02, 03, 04, 08), the MVP lists Life, and SEC-06 `ask_specialist` becomes Must. New `life` persona and prompt; the Secretary persona keeps only `ask_specialist`.
- `CLAUDE.md`: project rules for Claude Code.
- Work and pay in Finance (FIN-09 to 14): shifts at one job, with hours up to a cap per period paid to the bank and hours over it paid in cash, each method with its own rate and pay delay from `pay.yaml`, total pay not yet received (on request, no alerts), hours per week and fortnight, payslip checks, and a tax estimate for the financial year that includes cash wages; `work_shifts`, `pay_lines` and `payslips` tables; `pay.yaml` is gitignored.
- Runbook: file storage on the home server (one folder per service, files named by id, sensitive files encrypted) and 3-2-1 backups with `restic` (USB disk + encrypted cloud copy, 12-month limit, quarterly restore test); the deploy section now targets the home server instead of AWS.

### Decided
- Email and Documents merge into Life (MAIL, DOC IDs kept); each specialist sends its own report at its own pace (Life and Learning daily, Market every trading day, Housing and Finance monthly), never an empty one (REPORT-01 to 05), and the Secretary's combined brief is dropped; Life keeps one file store (`documents` table) and each area keeps its own summaries, e.g. Learning's lecture summaries per course (DOC-06); housing files stay in `housing` (ADR-39).
- Research merges into Learning, which now covers study, science and career; new SCI-06 daily science digest (at most 5 items, never sent twice); the `research` persona, prompt and token are removed (ADR-38).
- Life owns everything with a date: study deadlines and study schedule move from Learning (LIFE-05, 06); Learning keeps lectures, PTE and applications. `rental` is renamed `housing` (Huy's own rent is only a `finance` expense category): persona, prompt, tools, token, service and `housing-web` (ADR-37).
- No link to the study app (ADR-36, supersedes ADR-28): reminders, to-dos, calendar and study deadlines live in `assistant` under the Life and Learning bots; reminders and to-dos are back in the MVP. Every study-app reference is removed from docs and config.
- C# .NET is the main language and the code restarts from scratch in this repository (ADR-33, supersedes ADR-02); Python stays only for `market`.
- Two tiers of bots (ADR-32, amends ADR-08): the Secretary only routes through `ask_specialist`; specialists (life, rental, finance, market) hold the tools and are their own Telegram bots.
- Service boundaries (ADR-34): microservices stay; data only through APIs, no shared database or copies; ID-card data only through an owner-only Rental endpoint, never through AI or Telegram; no identity service; rules for where an LLM may run and which formats go between parts.
- Personal scope, home server instead of AWS (supersedes ADR-11), and an architecture freeze until the bot answers with Claude and rent is billed once (ADR-35). Parked ideas go to `docs/ideas.md`.

### Added
- Project skeleton: 5-layer folder structure, docs in `docs/`, Secretary persona config.
- Project text (docs, config, prompts, docstrings) translated to English.
- Branch and pull request workflow with a protected `main` (ADR-18) and a PR template.
- CI: GitHub Actions runs `ruff check .`, `lint-imports` and `pytest` on every PR; required to merge.
- Telegram echo through the pipeline (controller → `Pipeline` → `FakeLLMProvider` → presenter); answers only the owner.
- Market in the MVP (ADR-20) and its data model (ADR-21): `docs/market-data.md`, market tables in the data dictionary, factor-map template, `domain/market/` stubs.
- Sentiment and panic signal design (ADR-22): three signal families, social-data pipeline with bot filter, `sentiment_snapshots` table.
- Proposed quantitative layer (ADR-23) and time- and regime-dependent indicator trust (ADR-24): `model_runs`, `indicator_ratings`, `evidence.kind`.

### Changed
- Folder layout (ADR-30): `assistant` moved to `apps/assistant/`; `services/` keeps the business areas (`rental`, `market`, `finance`). CI runs one job per app and service.
- Telegram stays on long polling (ADR-31, supersedes ADR-29 before it was built): no public URL, tunnel or webhook settings; a dev bot on the laptop, the real bot on the server.
- Rental retention (ADR-27): readings, invoices and calculations kept 12 months, meter-book photos 3 months; settings moved to `services/rental/config/settings.yaml`.
- Planner (reminders, to-dos, study deadlines) belongs to the study app, in its own repository (ADR-28); SEC-02 and SEC-03 leave the assistant MVP.
- Monorepo of services (ADR-25, ADR-26): code moved to `services/assistant/`; new `services/rental/`, `services/market/` and `services/finance/` with their domain stubs; one CI job per service plus the required `checks` job; `channels/` renamed `entrypoints/` so every service has the same rings.
- Owner-only access moved from the Telegram filter into `AccessPolicy`, checked first in `Pipeline.run()`; strangers get no reply.
- Use cases moved into `application/` (pipeline steps, `policy/`, `tools/`); a second import-linter contract checks the order inside it (ADR-19).
