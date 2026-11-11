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

Async functions are named like sync ones (no `_async` suffix).

## 7. Classes

- Models (data) are nouns: `ToolCall`, `AgentReply`.
- Interfaces (Protocols in `domain/ports.py`) are the role: `LLMProvider`, `Repository`, `Channel`.
- Implementations are `<Technology><Role>`: `ClaudeLLMProvider`, `FakeLLMProvider`, `SQLiteRepository`, `TelegramChannel`.
- No `Manager`, `Helper`, `Utils`, `Data`, `Info` suffixes — they say nothing.

## 8. Words

- English only (ADR-14), no abbreviations except well-known ones: `id`, `url`, `db`, `llm`, `ms`.
- Use the project's words consistently: **persona** (not bot/agent in code), **tool** (not function/skill), **run** (one pass through the pipeline), **owner** (Huy), **tenant**.
