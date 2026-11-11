# Personal Assistant Agent

A personal AI assistant that talks over Telegram. A **Secretary** bot coordinates the specialist bots (Market, Email, Research, …); they all share one program and one database.

- Design document (architecture, pipeline, roadmap; in Vietnamese): [AI Agent design process](https://claude.ai/artifact/6PJohVCM9wezexxfhSLyz3)
- Detailed docs: [`docs/`](docs/README.md)

## Architecture at a glance

A 7-step pipeline; each step belongs to one layer:

| Step | Layer | Folder |
| --- | --- | --- |
| 1 Receive, 6 Send | Channel | `src/assistant/channels/` |
| 2 Check access | Policy | `src/assistant/policy/access.py` |
| 3 Context, 4 Loop, 5 Post-process | Orchestration | `src/assistant/orchestration/` |
| 4 Approve tool calls | Policy | `src/assistant/policy/guard.py` |
| 4 Run tools | Capability | `src/assistant/tools/` |
| 7 Store & observe | Infrastructure | `src/assistant/infrastructure/` |

Dependency rule: `domain/` imports nothing; every other folder imports only `domain/` and the layer directly below it; only `main.py` wires concrete classes together.

## Folder structure

```text
personal-assistant/
├── config/            # personas, prompts, settings — no secrets
├── docs/              # docs that live with the code
├── migrations/        # Alembic
├── data/              # SQLite file when running locally (not committed)
├── src/assistant/
│   ├── domain/        # data contracts + interfaces
│   ├── channels/      # Telegram, scheduler
│   ├── policy/        # allowlist, roles, guard by RiskLevel
│   ├── orchestration/ # router, context, agent loop, post-processing, pipeline
│   ├── tools/         # one file per tool
│   ├── infrastructure/# LLM, DB, logging
│   └── main.py        # composition root
└── tests/             # unit tests + evals.yaml
```

## Running locally

1. Python 3.12+; create a virtualenv: `uv venv`.
2. Install dependencies: `uv pip install -e ".[dev]"`.
3. Copy `.env.example` to `.env` and fill in tokens and API keys.
4. Run the migrations, then run `src/assistant/main.py`.

Step-by-step details, deployment and the **emergency shutdown**: [`docs/runbook.md`](docs/runbook.md).

## Status

Currently in **phase 1 — Foundations**. Change history: [`CHANGELOG.md`](CHANGELOG.md).
