# Changelog

Record every finished phase or significant change. Newest first.

## [Unreleased]

### Changed
- The code restarts in C# .NET (ADR-33): the Python code of `assistant`, `rental` and `finance` is removed; `apps/assistant` is a .NET solution with `Assistant.Domain`, `.Application`, `.Infrastructure`, `.Bot` and two test projects. `services/market` stays Python.
- Shared .NET build settings (`Directory.Build.props`: .NET 10, nullable, warnings as errors, recommended analyzers), SDK pinned in `global.json`, code style in `.editorconfig`, LF line endings in `.gitattributes`.
- CI builds, checks formatting and tests each .NET solution, and keeps the Python checks for `market`; `checks` stays the required job.
- README, conventions (C# naming, tests, doc comments), runbook, PR template and data dictionary updated for .NET.

### Decided
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
