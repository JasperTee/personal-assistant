# CLAUDE.md

Read this first. It tells Claude Code how this repository works and how to work with its owner.

## The project

A personal AI assistant on Telegram, being rebuilt in C# .NET 10 (ADR-33).

- A **Secretary** bot routes each request to specialist bots (life, housing, finance, market, …) that hold the tools (ADR-32).
- All bots live in one app, `apps/assistant`. Each business area is its own service under `services/` with its own database. Apps call services over gRPC; services never call apps (ADR-34).
- `services/market` is Python. Everything else is C#.
- Scope is personal only. **The architecture is frozen (ADR-35)**: put new ideas in `docs/ideas.md` and don't redesign.

## Roles: who does what

The project is a learning and CV piece. The owner must be able to explain every line in an interview.

- **The owner** writes all code in `src/`, all tests and `Program.cs` (DI). They run every `git` and `dotnet` command themselves.
- **Claude** writes the following:
  - config: `.csproj`/`.slnx`, `Directory.Build.props`, `.editorconfig`, CI, `.gitignore`, appsettings skeletons. Explain each part briefly.
  - docs: ADRs, README, CHANGELOG, `docs/`.
- **Claude also reviews and guides.** Don't write `src/` code unless asked.
  - When the owner is stuck on design, use a hint ladder: point to where to look first, give a stronger hint next, and give the answer only when asked.
  - When they're stuck on syntax, show the syntax frame or a small example directly.
  - Don't ask obvious questions.
- **Language:**
  - Chat in Vietnamese.
  - Everything written into the repository is English: code, comments, docs, config, prompts (ADR-14).
  - Eval inputs stay Vietnamese on purpose.

## Layout (`apps/assistant`)

Clean Architecture. Project references enforce the rings: a project may reference only the rings inside it.

```text
Assistant.Bot             composition root (Program.cs), Telegram, scheduler   → Application, Infrastructure
Assistant.Infrastructure  adapters: database, LLM, logs, service clients        → Application
Assistant.Application     pipeline, agent loop, Policy/, Tools/<Area>/          → Domain
Assistant.Domain          Models/, Ports/ — references nothing
tests/                    one xUnit project per ring
```

The pipeline (README, "Architecture at a glance") has 7 steps:

1. Receive, then clean the input in code (ADR-17).
2. Check access and budget.
3. Normalize and route, then build the context.
4. Run the agent loop. The Guard checks each tool call's `RiskLevel` before it runs.
5. Post-process the reply.
6. Send it.
7. Store it and log the run.

## Commands

Run these from `apps/assistant`. They are the same checks CI runs (`.github/workflows/checks.yml`).

```bash
dotnet format --verify-no-changes
dotnet build
dotnet test
```

- `dotnet format` (without `--verify-no-changes`) fixes whitespace and final newlines.
- Warnings are errors (`Directory.Build.props`).
- For `services/market`, run `ruff check .`, `lint-imports` and `pytest` in its virtualenv.

## Rules that always apply

- **Git flow** (ADR-18):
  - Branch, then commit with Conventional Commits, open a PR, wait for CI, and use **Rebase and merge**. Never commit to `main`.
  - Give each git command in its own code block.
  - Use single quotes for commit messages that contain `!`, because zsh expands it.
- **Attribution:**
  - When a commit contains work Claude did (docs, config, reviews that shaped the code), end the commit message with `Co-Authored-By: Claude <noreply@anthropic.com>`.
  - Commits of the owner's own code have no trailer.
- **Secrets:**
  - Never show, ask for or type tokens, keys or passwords.
  - `.env` is gitignored and Claude does not edit it. Secrets on the laptop go in `dotnet user-secrets`.
- **Never `git add ops/`.** It holds the owner's untracked server scripts.
- **Don't commit tuned market config.**
- **Sensitive data:** ID-card (CCCD) photos and numbers are never sent to an LLM or Telegram. They are reachable only through an owner-only `housing` endpoint (ADR-34).
- **Tests use fake data only.**
- **Naming and style** follow `docs/conventions.md`. Check it in every example and review.

## Where to look

| Question | File |
| --- | --- |
| Why was X decided? | `docs/decisions.md` (ADRs) |
| How do I name or structure X? | `docs/conventions.md` |
| What does a table hold? | `docs/data-dictionary.md` |
| Which tools does each bot have? | `docs/tools.md` |
| Threats and mitigations | `docs/threat-model.md` |
| Run, deploy, emergency shutdown | `docs/runbook.md` |
| Problems that changed direction | `docs/devlog.md` |
| Ideas for later | `docs/ideas.md` |
