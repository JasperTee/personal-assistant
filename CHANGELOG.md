# Changelog

Record every finished phase or significant change. Newest first.

## [Unreleased]

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
- Monorepo of services (ADR-25, ADR-26): code moved to `services/assistant/`; new `services/rental/`, `services/market/` and `services/finance/` with their domain stubs; one CI job per service plus the required `checks` job; `channels/` renamed `entrypoints/` so every service has the same rings.
- Owner-only access moved from the Telegram filter into `AccessPolicy`, checked first in `Pipeline.run()`; strangers get no reply.
- Use cases moved into `application/` (pipeline steps, `policy/`, `tools/`); a second import-linter contract checks the order inside it (ADR-19).
