# Naming conventions

One name for one idea, everywhere: code, database, config, docs. If two names mean the same thing, one of them is wrong.
Base rules come from [PEP 8](https://peps.python.org/pep-0008/#naming-conventions); Ruff checks them (`N` rules in `pyproject.toml`). The project-specific rules below are checked in code review.

## 1. Case

| What | Style | Example |
| --- | --- | --- |
| Class, Pydantic model, enum, Protocol | `PascalCase` | `ToolCall`, `RiskLevel`, `LLMProvider` |
| Function, method, variable, field, parameter | `snake_case` | `build_context`, `received_at` |
| Constant (module level) | `UPPER_SNAKE_CASE` | `MAX_ITERATIONS` |
| Enum member | `UPPER_SNAKE_CASE` | `RiskLevel.WRITE_SELF` |
| Module / file, folder | `snake_case`, short | `agent_loop.py`, `context_builder.py` |
| Private (internal to a module/class) | leading `_` | `_parse_update` |
| DB table | `snake_case`, plural | `messages`, `run_logs` |
| DB column | same name as the model field | `received_at` |
| Config key (YAML) | `snake_case` | `max_iterations` |
| Environment variable | `UPPER_SNAKE_CASE` | `TELEGRAM_TOKEN_SECRETARY` |
| Tool name | `<area>.<verb>`, lowercase | `reminders.create`, `expenses.summary` |
| Persona id | lowercase, one word | `secretary`, `rental` |

Acronyms in `PascalCase` stay upper case: `LLMProvider`, `HTTPClient` (not `LlmProvider`).

## 2. Identifiers (ids)

- An object's **own** id is always `id`.
- A **reference** to another object is `<object>_id`, where `<object>` is that class's name in `snake_case`.
- Never `Id`, `ID`, `toolId`, or a bare `call_id` when the class is `ToolCall`.

| Class | Own id | References |
| --- | --- | --- |
| `ToolCall` | `id` | — |
| `ToolResult` | — | `tool_call_id` (→ `ToolCall.id`) |
| `IncomingMessage` | — | `sender_id` (→ the user who sent it), `run_id` |
| DB `messages` | `id` | `user_id` (→ `users.id`), `run_id` |

Exception: an id that comes from an outside system keeps its source in the name: `telegram_id`.

## 3. Suffixes that carry meaning

| Kind of value | Suffix | Example |
| --- | --- | --- |
| Moment in time (`datetime`, time-zone aware) | `_at` | `received_at`, `remind_at`, `expires_at` |
| Calendar date (`date`) | `_on` | `spent_on`, `due_on` |
| Duration | unit | `duration_ms`, `cooldown_hours` |
| Money | currency | `amount_aud`, `cost_usd` |
| Count | `_count` | `retry_count` |

A name without a unit (`timeout`, `amount`) is not allowed when the value has one.

## 4. Booleans

Read as a yes/no question: `is_`, `has_`, `can_`, `should_`.
`is_error`, `is_enabled`, `has_attachments` — not `error`, `enabled`, `ok`.

Exception: on/off switches under `proactive:` in persona YAML are feature names (`morning_brief: true`).

## 5. Collections

Plural noun: `tool_calls`, `messages`, `allowed_tools`. A dict mapping keys to values: `<value>_by_<key>`, e.g. `persona_by_token`.

## 6. Functions and methods

Start with a verb. The same verb always means the same thing:

| Verb | Meaning | Returns |
| --- | --- | --- |
| `get_` | Fetch one; it must exist | the object, raises if missing |
| `find_` | Look for one | the object or `None` |
| `list_` | Fetch many | a list (may be empty) |
| `create_` / `save_` | Insert new / insert-or-update | the stored object |
| `update_` | Change an existing one | the updated object |
| `delete_` | Remove | `None` |
| `build_` | Assemble an object in memory, no I/O | the object |
| `parse_` | Turn raw data into a model | the model |
| `to_` | Convert to another format | the converted value |
| `check_` / `validate_` | Verify, raise on failure | `None` |
| `load_` | Read config or files from disk at start-up | the typed object |
| `generate_` | Ask an LLM to produce something | the LLM's response |
| `send_` | Deliver something outside (a chat message) | `None` |
| `handle_` | Entry point a framework calls for an event | `None` |

Async functions are named like sync ones (no `_async` suffix).

## 7. Classes

- Models (data) are nouns: `ToolCall`, `AgentReply`.
- Interfaces (Protocols in `domain/ports.py`) are the role: `LLMProvider`, `Repository`, `Channel`.
- Implementations are `<Technology><Role>`: `ClaudeLLMProvider`, `FakeLLMProvider`, `SQLiteRepository`, `TelegramChannel`.
- No `Manager`, `Helper`, `Utils`, `Data`, `Info` suffixes — they say nothing.

## 8. Words

- English only (ADR-14), no abbreviations except well-known ones: `id`, `url`, `db`, `llm`, `ms`.
- Use the project's words consistently: **persona** (not bot/agent in code), **tool** (not function/skill), **run** (one pass through the pipeline), **owner** (Huy), **tenant**.

## 9. Structure (ADR-16)

Layer first, then area. The path tells you the layer and the job:

| What | Path | Example |
| --- | --- | --- |
| Data contract shared by all | `domain/models.py` | `ToolCall` |
| Area business rules (pure code) | `domain/<area>/` | `domain/rental/billing.py` |
| Interface (Protocol) | `domain/ports.py` | `LLMProvider` |
| Channel input (MVC controller) | `channels/<channel>/controller.py` | `TelegramController` |
| Channel output (MVC view) | `channels/<channel>/presenter.py` | `TelegramPresenter` |
| Tool | `tools/<area>/<verb>.py` — same as the tool name | `reminders.create` → `tools/reminders/create.py` |
| Port implementation | `infrastructure/<kind>/<technology>.py` | `infrastructure/llm/claude.py` → `ClaudeLLMProvider` |

Import only downwards: `main` → `channels | infrastructure` → `orchestration` → `policy | tools` → `domain`. `lint-imports` fails the check otherwise.

## 10. Tests

- `tests/` mirrors `src/assistant/`: `src/assistant/policy/guard.py` → `tests/policy/test_guard.py`.
- One `Test<ClassName>` class per class under test; test names say the behaviour: `test_<what>_<expected>`, e.g. `test_tool_call_rejects_wrong_types`.
- Shared fixtures in `tests/conftest.py`; no `__init__.py` in `tests/`.


## 11. Commit messages

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <summary>`.

- `summary`: imperative, lower case, no final period, ≤ 72 characters — "add reminder tool", not "Added reminder tool."
- `scope` (optional): the layer or area touched — `domain`, `channels`, `policy`, `orchestration`, `tools`, `infrastructure`, `config`, `docs`, or an area such as `rental`, `reminders`.

| Type | Use for | Example |
| --- | --- | --- |
| `feat` | A new behaviour the user can see | `feat(reminders): add reminders.create tool` |
| `fix` | A bug fix | `fix(policy): block reminders in the past` |
| `test` | Adding or changing tests only | `test(domain): add tests for domain models` |
| `refactor` | Restructuring without changing behaviour | `refactor: split tools into area folders` |
| `docs` | Docs only | `docs: add ADR-16` |
| `style` | Formatting, comment / docstring wording; no code change | `style: start docstrings upper case, comments lower case` |
| `chore` | Tooling, dependencies, config files that don't change behaviour | `chore: add import-linter` |
| `build` / `ci` | Packaging / CI pipeline | `ci: run ruff and pytest on push` |

One commit, one type. If a change needs two types, make two commits. Breaking change: add `!` after the type (`feat(domain)!: rename ToolResult.content`).

## 12. Docstrings and comments

| What | Starts with | Example |
| --- | --- | --- |
| Docstring (module, class, function) | **Capital letter**, full sentence, ends with `.` | `"""Send the context to the LLM and return its response."""` |
| Comment (`#`, in Python, YAML, TOML, `.env.example`) | **lower-case letter**, no final `.` | `# cannot be changed after creation` |

- A docstring that starts with a code name puts a word in front: `"""Tool reminders.create (WRITE_SELF): ..."""`, `"""Tests for reminders.create: ..."""`.
- A comment keeps the original case when it starts with a code name, literal, acronym or proper noun: `# True if the tool call failed`, `# LLM normalisation…`, `# Huy confirms`, `# EXTERNAL — awaits approval`.
- `TODO` stays upper case so editors and `grep TODO` find it.
- Several sentences in one comment are joined with `;`, not `. `: `# starter cases; replace with real messages`.
- Ruff rule `D403` checks function and method docstrings; module and class docstrings and comments are checked in code review.
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
4. Before pushing, run the checks: `ruff check .`, `lint-imports`, `pytest`.
5. Push the branch: `git push -u origin feat/telegram-echo`.
6. Open a PR: `gh pr create`. Title = the main change in commit format (`feat(channels): echo Telegram messages through the pipeline`); fill in the template.
7. Review the diff on GitHub (Files changed), fix anything found with new commits on the same branch.
8. Merge with **Rebase and merge** (keeps every Conventional Commit on a straight `main` history); the branch is deleted after merging.
9. Back to `main`: `git switch main`, `git pull`, delete the local branch: `git branch -d feat/telegram-echo`.

**Rules:**

- One PR, one purpose. Small PRs (under ~400 changed lines) are reviewed better than big ones.
- A PR is merged only when all checks pass.
- Never rewrite `main`'s history (`git push --force` to `main` is blocked).
