# Personal Assistant Agent

A personal AI assistant that talks over Telegram. A **Secretary** bot routes each request to specialist bots (life, rental, finance, market, …) that hold the tools; Huy can also talk to each specialist directly. The bots share one app (`apps/assistant`); each business area is its own service with its own database. Being rebuilt in C# .NET (ADR-33).

- Design document (architecture, pipeline, roadmap; in Vietnamese): [AI Agent design process](https://claude.ai/artifact/6PJohVCM9wezexxfhSLyz3)
- Detailed docs: [`docs/`](docs/README.md)

## Architecture at a glance

Clean Architecture for the whole system; MVC only at the edge (channel controllers and presenters). A 7-step pipeline; each step belongs to one ring (paths under `apps/assistant/src/`):

| Step | Ring | Where |
| --- | --- | --- |
| 1 Receive | Entry point (controller) | `Assistant.Bot/Telegram/TelegramController.cs` |
| 2 Check access, budget | Application (policy) | `Assistant.Application/Policy/` |
| 3 Context, 4 Loop, 5 Post-process | Application | `Assistant.Application/` |
| 4 Approve tool calls | Application (policy) | `Assistant.Application/Policy/Guard.cs` |
| 4 Run tools | Application (tools) | `Assistant.Application/Tools/<Area>/` |
| 6 Send | Entry point (presenter) | `Assistant.Bot/Telegram/TelegramPresenter.cs` |
| 7 Store & observe | Infrastructure | `Assistant.Infrastructure/` |

Dependency rule (ADR-16, ADR-19, ADR-33): a project references only the rings inside it, so the compiler blocks a wrong dependency.

```text
Assistant.Bot             composition root (Program.cs) + Telegram, scheduler
Assistant.Infrastructure  adapters: database, LLM, config, logs, other services' clients
Assistant.Application     use cases: pipeline → router, context, agent loop → policy | tools
Assistant.Domain          data contracts, ports, business rules — references nothing
```

## Folder structure

Monorepo of apps and services (ADR-26, ADR-30, ADR-34). `apps/` holds what people use (the Telegram bots, later `rental-web`); `services/` holds the business areas the apps call over gRPC. Each one has its own solution (or `pyproject.toml` for `market`), code, tests and config, and builds alone. Apps call services; services never call apps.

```text
personal-assistant/
├── apps/                          # what people use; calls the services
│   └── assistant/                 # all Telegram bots: Secretary + specialists (ADR-32)
│       ├── Assistant.slnx         # the solution: lists the projects below
│       ├── config/                # personas, prompts — no secrets
│       ├── src/
│       │   ├── Assistant.Domain/          # Models/, Ports/
│       │   ├── Assistant.Application/     # Pipeline, AgentLoop, Policy/, Tools/<Area>/
│       │   ├── Assistant.Infrastructure/  # Llm/, Database/, logs
│       │   └── Assistant.Bot/             # Program.cs, Telegram/, Scheduler/
│       └── tests/                 # one test project per ring, mirrors src/
├── services/                      # business areas; never call apps
│   └── market/                    # Python (ADR-33): market data, evidence, forecasts
│                                  # rental/ and finance/ return as .NET solutions
├── docs/                          # docs that live with the code
├── Directory.Build.props          # build settings shared by every .NET project
├── global.json                    # the .NET SDK version
├── .editorconfig                  # code style; the build checks it
└── .github/workflows/             # CI: one job per solution + market + the required `checks` job
```

## Running locally

1. Install the .NET SDK 10 (`dotnet --version` should print 10.0.x; `global.json` picks the version).
2. Build and test the assistant: `cd apps/assistant`, then `dotnet build` and `dotnet test`.
3. Secrets on the laptop go in .NET user secrets, never in a file in the repository: `dotnet user-secrets set "<Section>:<Key>" "<value>" --project src/Assistant.Bot` (the keys arrive with the code that reads them).
4. Start the bot: `dotnet run --project src/Assistant.Bot` (Ctrl+C stops it).
5. Before every commit, in the solution folder: `dotnet format --verify-no-changes`, `dotnet build`, `dotnet test`. For `services/market`: `ruff check .`, `lint-imports`, `pytest` in a Python virtualenv.

Step-by-step details, deployment and the **emergency shutdown**: [`docs/runbook.md`](docs/runbook.md).

## Status

Currently in **phase 1 — Foundations**. Change history: [`CHANGELOG.md`](CHANGELOG.md).
