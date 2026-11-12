# Personal Assistant Agent

A personal AI assistant that talks over Telegram. A **Secretary** bot coordinates the specialist bots (Market, Email, Research, …); they all share one program and one database.

- Design document (architecture, pipeline, roadmap; in Vietnamese): [AI Agent design process](https://claude.ai/artifact/6PJohVCM9wezexxfhSLyz3)
- Detailed docs: [`docs/`](docs/README.md)

## Architecture at a glance

Clean Architecture for the whole system; MVC only at the edge (channel controllers and presenters). A 7-step pipeline; each step belongs to one layer:

| Step | Layer | Where |
| --- | --- | --- |
| 1 Receive | Channel (controller) | `channels/<channel>/controller.py` |
| 2 Check access, budget | Application (policy) | `application/policy/access.py`, `application/policy/budget.py` |
| 3 Context, 4 Loop, 5 Post-process | Application | `application/` |
| 4 Approve tool calls | Application (policy) | `application/policy/guard.py` |
| 4 Run tools | Application (tools) | `application/tools/<area>/<verb>.py` |
| 6 Send | Channel (presenter) | `channels/<channel>/presenter.py` |
| 7 Store & observe | Infrastructure | `infrastructure/` |

Dependency rule (ADR-16, ADR-19, checked by `lint-imports`): a layer imports only the layers below it.

```text
main.py                          composition root — wires concrete classes
channels/  |  infrastructure/    adapters: Telegram, scheduler | DB, LLM, config, logs
application/                     use cases: pipeline → router, context, agent loop → policy | tools
domain/                          data contracts, ports, business rules — imports nothing
```

## Folder structure

```text
personal-assistant/
├── config/                 # personas, prompts, settings — no secrets
├── docs/                   # docs that live with the code
├── migrations/             # Alembic
├── data/                   # SQLite file when running locally (not committed)
├── src/assistant/
│   ├── domain/             # models.py, ports.py, rental/ (business rules)
│   ├── channels/           # telegram/, scheduler/ — controller.py, presenter.py
│   ├── application/        # use cases: pipeline, router, context_builder, agent_loop, postprocess
│   │   ├── policy/         # access.py, budget.py, guard.py
│   │   └── tools/          # registry.py + <area>/<verb>.py (reminders/create.py)
│   ├── infrastructure/     # config.py, run_logger.py, db/, llm/
│   └── main.py             # composition root
└── tests/                  # mirrors src/ (tests/application/policy/test_guard.py) + evals.yaml
```

## Running locally

1. Python 3.12+; create a virtualenv: `uv venv`.
2. Install dependencies: `uv pip install -e ".[dev]"`.
3. Copy `.env.example` to `.env` and fill in tokens and API keys.
4. Start the bot: `python -m assistant.main` (phase 1 echoes your messages; Ctrl+C stops it).
5. Before every commit: `ruff check .`, `lint-imports`, `pytest`.

Step-by-step details, deployment and the **emergency shutdown**: [`docs/runbook.md`](docs/runbook.md).

## Status

Currently in **phase 1 — Foundations**. Change history: [`CHANGELOG.md`](CHANGELOG.md).
