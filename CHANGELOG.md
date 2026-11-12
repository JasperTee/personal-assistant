# Changelog

Record every finished phase or significant change. Newest first.

## [Unreleased]

### Added
- Project skeleton: 5-layer folder structure, docs in `docs/`, Secretary persona config.
- Project text (docs, config, prompts, docstrings) translated to English.
- Branch and pull request workflow with a protected `main` (ADR-18) and a PR template.
- CI: GitHub Actions runs `ruff check .`, `lint-imports` and `pytest` on every PR; required to merge.
- Telegram echo through the pipeline (controller → `Pipeline` → `FakeLLMProvider` → presenter); answers only the owner.

### Changed
- Use cases moved into `application/` (pipeline steps, `policy/`, `tools/`); a second import-linter contract checks the order inside it (ADR-19).
