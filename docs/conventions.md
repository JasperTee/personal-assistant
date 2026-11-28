# Naming conventions

One name for one idea, everywhere: code, database, config, docs. If two names mean the same thing, one of them is wrong.
C# code follows the [.NET naming guidelines](https://learn.microsoft.com/dotnet/standard/design-guidelines/naming-guidelines); the rules in the root `.editorconfig` make the build fail when a name breaks them. Python in `services/market` follows PEP 8 (Ruff). The project-specific rules below are checked in code review.

## 1. Case

| What | Style | Example |
| --- | --- | --- |
| Class, record, struct, enum, namespace | `PascalCase` | `ToolCall`, `RiskLevel`, `Assistant.Domain` |
| Interface | `I` + `PascalCase` | `ILlmProvider` |
| Method, property, event, public constant | `PascalCase` | `BuildContext`, `ReceivedAt`, `MaxIterations` |
| Enum member | `PascalCase` | `RiskLevel.WriteSelf` |
| Parameter, local variable | `camelCase` | `toolCall`, `receivedAt` |
| Private field | `_camelCase` | `_client`, `_maxTokens` |
| File | the type it holds, one public type per file | `ToolCall.cs`, `ClaudeLlmProvider.cs` |
| Project | `<App>.<Ring>` | `Assistant.Application` |
| DB table | `snake_case`, plural | `messages`, `run_logs` |
| DB column, `.proto` field, YAML key | `snake_case`, same words as the C# property | `received_at` ↔ `ReceivedAt` |
| JSON at the edge (REST, web) | `camelCase` | `receivedAt` |
| Environment variable | .NET configuration path, `__` between sections | `Anthropic__ApiKey` |
| Tool name | `<area>.<verb>`, lowercase | `reminders.create`, `expenses.summary` |
| Persona id | lowercase, one word | `secretary`, `housing` |

Acronyms longer than two letters are written like words: `LlmProvider`, `HttpClient`, `SqliteRepository` (not `LLMProvider`); two-letter ones stay upper case: `IO`.

## 2. Identifiers (ids)

- An object's **own** id is always `Id` (`id` in the database and `.proto`).
- A **reference** to another object is `<Object>Id`, where `<Object>` is that class's name: `ToolCallId` (`tool_call_id`).
- Never `ID`, `ToolId`, or a bare `CallId` when the class is `ToolCall`.

| Class | Own id | References |
| --- | --- | --- |
| `ToolCall` | `Id` | — |
| `ToolResult` | — | `ToolCallId` (→ `ToolCall.Id`) |
| `IncomingMessage` | — | `SenderId` (→ the user who sent it), `RunId` |
| DB `messages` | `id` | `user_id` (→ `users.id`), `run_id` |

Exception: an id that comes from an outside system keeps its source in the name: `TelegramId`.

## 3. Suffixes that carry meaning

| Kind of value | C# type | Suffix | Example |
| --- | --- | --- | --- |
| Moment in time | `DateTimeOffset` (stored in UTC) | `At` | `ReceivedAt`, `RemindAt`, `ExpiresAt` |
| Calendar date | `DateOnly` | `On` | `SpentOn`, `DueOn` |
| Duration | `TimeSpan`, or a number with its unit | unit | `Timeout`, `DurationMs`, `CooldownHours` |
| Money | `decimal` (`long` cents in `.proto`) | currency | `AmountAud`, `CostUsd`, `TotalCents` |
| Count | `int` | `Count` | `RetryCount` |

A number without a unit (`Timeout` as an `int`, `Amount`) is not allowed when the value has one. Never `double` for money.

## 4. Booleans

Read as a yes/no question: `Is`, `Has`, `Can`, `Should`.
`IsError`, `IsEnabled`, `HasAttachments` — not `Error`, `Enabled`, `Ok`.

Exception: on/off switches under `proactive:` in persona YAML are feature names (`morning_brief: true`).

## 5. Collections

Plural noun: `ToolCalls`, `Messages`, `AllowedTools`. A dictionary from keys to values: `<Value>By<Key>`, e.g. `PersonaByToken`. Data contracts expose read-only collections (`IReadOnlyList<T>`).

## 6. Methods

Start with a verb. The same verb always means the same thing:

| Verb | Meaning | Returns |
| --- | --- | --- |
| `Get` | Fetch one; it must exist | the object, throws if missing |
| `Find` | Look for one | the object or `null` |
| `List` | Fetch many | a list (may be empty) |
| `Create` / `Save` | Insert new / insert-or-update | the stored object |
| `Update` | Change an existing one | the updated object |
| `Delete` | Remove | nothing |
| `Build` | Assemble an object in memory, no I/O | the object |
| `Parse` | Turn raw data into a model | the model |
| `To` | Convert to another format | the converted value |
| `Check` / `Validate` | Verify, throw on failure | nothing |
| `Load` | Read config or files from disk at start-up | the typed object |
| `Generate` | Ask an LLM to produce something | the LLM's response |
| `Send` | Deliver something outside (a chat message) | nothing |
| `Handle` | Entry point a framework calls for an event | nothing |

Methods that return `Task` end in `Async` (`GenerateAsync`, `SendAsync`) and take a `CancellationToken` as the last parameter.

## 7. Classes

- Models (data) are nouns, written as immutable `record`s: `ToolCall`, `AgentReply`.
- Interfaces (ports) are `I` + the role: `ILlmProvider`, `IRepository`, `IChannel`.
- Implementations are `<Technology><Role>`: `ClaudeLlmProvider`, `FakeLlmProvider`, `SqliteRepository`, `TelegramChannel`.
- No `Manager`, `Helper`, `Utils`, `Data`, `Info` suffixes — they say nothing.

## 8. Words

- English only (ADR-14), no abbreviations except well-known ones: `id`, `url`, `db`, `llm`, `ms`.
- Use the project's words consistently: **persona** (not bot/agent in code), **tool** (not function/skill), **run** (one pass through the pipeline), **owner** (Huy), **tenant**.

## 9. Structure (ADR-16, ADR-19, ADR-30, ADR-33)

Apps and services first: `apps/<name>/` for what people use (`assistant`, later `housing-web`), `services/<name>/` for business areas (`housing`, `market`, `finance`). Each has its own solution and builds alone; none references another's projects. Apps call services, services never call apps.

Inside `apps/assistant/`: one project per ring, then folders by kind and area. The path tells you the ring and the job:

| What | Path (under `src/`) | Example |
| --- | --- | --- |
| Data contract shared by all | `Assistant.Domain/Models/` | `ToolCall.cs` |
| Interface (port) | `Assistant.Domain/Ports/` | `ILlmProvider.cs` |
| Business rules of another area | its own service | `services/housing/src/Housing.Domain/` |
| Use case (pipeline step) | `Assistant.Application/` | `Pipeline.cs`, `AgentLoop.cs` |
| Policy (rules) | `Assistant.Application/Policy/` | `AccessPolicy.cs`, `Guard.cs` |
| Tool | `Assistant.Application/Tools/<Area>/` | `reminders.create` → `Tools/Reminders/CreateReminderTool.cs` |
| Port implementation | `Assistant.Infrastructure/<Kind>/` | `Llm/ClaudeLlmProvider.cs` |
| Channel input (MVC controller) | `Assistant.Bot/<Channel>/` | `Telegram/TelegramController.cs` |
| Channel output (MVC view) | `Assistant.Bot/<Channel>/` | `Telegram/TelegramPresenter.cs` |
| Composition root | `Assistant.Bot/Program.cs` | registers the real classes for dependency injection |

Namespaces follow the folders: `Assistant.Application.Tools.Reminders`.

Dependencies point inward only, enforced by project references (a project can't use a class from a project it doesn't reference):

```text
Assistant.Bot ──► Assistant.Infrastructure ──► Assistant.Application ──► Assistant.Domain
      └──────────────────────────────────────────────►┘
```

Domain references nothing; nothing references `Assistant.Bot`. Inside `Assistant.Application` the order is checked in review: `Pipeline` → `AgentLoop | ContextBuilder | PostProcess | Router` → `Policy | Tools`.

### Same rings in every app and service

Every .NET app and service here has the same rings: `<App>.Domain`, `<App>.Application`, `<App>.Infrastructure`, and an entry point (`<App>.Bot`, `<App>.Api` for HTTP and gRPC, `<App>.Web` for MVC), with `Program.cs` as the composition root. `services/market` (Python) maps them one to one to `domain/`, `application/`, `infrastructure/`, `entrypoints/` and `main.py`, checked by import-linter.

- Tests mirror the source tree (`src/Assistant.Application/Policy/Guard.cs` ↔ `tests/Assistant.Application.Tests/Policy/GuardTests.cs`).
- Same words and naming rules in both languages (§2–§5), each in its own casing: `TenantId`, `IsActive`, `AmountAud` ↔ `tenant_id`, `is_active`, `amount_aud`.
- Where data crosses languages, one casing for everyone (§1): `snake_case` in `.proto` and the database, `camelCase` in edge JSON; the tools convert (generated gRPC code, an EF Core snake_case naming convention).
- Same data rules: ids are UUIDs (`Guid`), times stored in UTC, every table has `id` and `created_at`, schema changes only through migrations (EF Core; Alembic in `market`), one database per service.
- Same process: §11 commits, §13 branches and pull requests, a required `checks` CI job, the same `docs/` set (README, CHANGELOG, decisions, devlog, conventions, requirements, data dictionary, threat model, runbook).

## 10. Tests

- One test project per ring that has logic: `tests/<App>.<Ring>.Tests`, mirroring the folders of `src/<App>.<Ring>`.
- One test class per class under test, named `<ClassName>Tests` (`GuardTests`).
- xUnit: a test is a method marked `[Fact]` (or `[Theory]` with `[InlineData]` for several inputs); its name says the behaviour: `<Method>_<Situation>_<Expected>`, e.g. `Check_RemindAtInThePast_ReturnsError`.
- Arrange, act, assert, with a blank line between them. Fake data only, never real tenant data.

## 11. Commit messages

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <summary>`.

- `summary`: imperative, lower case, no final period, ≤ 72 characters — "add reminder tool", not "Added reminder tool."
- `scope` (optional): the ring or area touched — `domain`, `application`, `infrastructure`, `bot`, `policy`, `tools`, `config`, `docs`, or an area such as `housing`, `reminders`.

| Type | Use for | Example |
| --- | --- | --- |
| `feat` | A new behaviour the user can see | `feat(reminders): add reminders.create tool` |
| `fix` | A bug fix | `fix(policy): block reminders in the past` |
| `test` | Adding or changing tests only | `test(domain): add tests for domain models` |
| `refactor` | Restructuring without changing behaviour | `refactor: split tools into area folders` |
| `docs` | Docs only | `docs: add ADR-16` |
| `style` | Formatting, comment / docstring wording; no code change | `style: start docstrings upper case, comments lower case` |
| `chore` | Tooling, dependencies, config files that don't change behaviour | `chore: add .editorconfig` |
| `build` / `ci` | Build settings, packaging / CI pipeline | `ci: build and test the .NET solutions` |

One commit, one type. If a change needs two types, make two commits. Breaking change: add `!` after the type (`feat(domain)!: rename ToolResult.Content`).

## 12. Doc comments and comments

| What | Starts with | Example |
| --- | --- | --- |
| XML doc comment on a public type or member (`/// <summary>`) | **Capital letter**, full sentence, ends with `.` | `/// <summary>Send the context to the LLM and return its response.</summary>` |
| Comment (`//` in C#, `#` in YAML, `.editorconfig`, Python) | **lower-case letter**, no final `.` | `// cannot be changed after creation` |

- A doc comment that starts with a code name puts a word in front: `/// <summary>Tool reminders.create (WriteSelf): ...</summary>`.
- A comment keeps the original case when it starts with a code name, literal, acronym or proper noun: `// True if the tool call failed`, `// LLM normalisation…`, `// Huy confirms`.
- `TODO` stays upper case so editors and `grep TODO` find it.
- Several sentences in one comment are joined with `;`, not `. `: `// starter cases; replace with real messages`.
- Markdown headings (`# Persona: Secretary` in `config/prompts/*.md`) are not comments.

## 13. Branches and pull requests (ADR-18)

`main` is protected: nobody commits or pushes to it directly, not even the owner. Every change goes through a branch and a pull request (PR).

**Branch name:** `<type>/<short-description>`, the same types as commits (§11), lower case, words joined with `-`:

| Change | Branch |
| --- | --- |
| New Telegram echo | `feat/telegram-echo` |
| Fix a bug in the guard | `fix/guard-past-reminders` |
| Docs only | `docs/git-workflow` |
| CI pipeline | `ci/run-checks` |

**Flow:**

1. Start from an up-to-date `main`: `git switch main`, `git pull`.
2. Create the branch: `git switch -c feat/telegram-echo`.
3. Commit in small steps (§11: one commit, one type).
4. Before pushing, run the checks in the solution folder (`cd apps/assistant`): `dotnet format --verify-no-changes`, `dotnet build`, `dotnet test` (in `services/market`: `ruff check .`, `lint-imports`, `pytest`).
5. Push the branch: `git push -u origin feat/telegram-echo`.
6. Open a PR: `gh pr create`. Title = the main change in commit format (`feat(bot): echo Telegram messages through the pipeline`); fill in the template.
7. Review the diff on GitHub (Files changed), fix anything found with new commits on the same branch.
8. Merge with **Rebase and merge** (keeps every Conventional Commit on a straight `main` history); the branch is deleted after merging.
9. Back to `main`: `git switch main`, `git pull`, delete the local branch: `git branch -d feat/telegram-echo`.

**Rules:**

- One PR, one purpose. Small PRs (under ~400 changed lines) are reviewed better than big ones.
- A PR is merged only when all checks pass.
- Never rewrite `main`'s history (`git push --force` to `main` is blocked).
