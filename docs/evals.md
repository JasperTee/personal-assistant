# Testing and evals

Two layers: **unit tests** (fast, use a fake LLM, cost nothing) and **evals** (run against the real LLM, measure quality).

## Unit tests — `tests/`

Each solution has one test project per ring (`tests/<App>.<Ring>.Tests`) that mirrors that ring's folders: the test for `apps/assistant/src/Assistant.Application/Policy/Guard.cs` is `apps/assistant/tests/Assistant.Application.Tests/Policy/GuardTests.cs`. Paths in the table are inside `apps/assistant/tests/` unless they name another service. Naming of test classes and methods: [conventions.md §10](conventions.md).

| File | Checks | From phase |
| --- | --- | --- |
| Assistant.Domain.Tests/Models/ModelTests.cs | Contracts can't be changed after creation and have the right defaults | 1 |
| Assistant.Bot.Tests/Telegram/TelegramControllerTests.cs (project added with the Telegram code) | Sample Telegram update → `IncomingMessage` with the right persona and time | 1 |
| Assistant.Bot.Tests/Telegram/TelegramPresenterTests.cs | Long replies split; pending actions get Send/Cancel buttons | 1 |
| Assistant.Application.Tests/Policy/AccessPolicyTests.cs | Strangers blocked; each persona gets only its tools | 3 |
| Assistant.Application.Tests/Policy/GuardTests.cs | External actions await approval; Forbidden rejected; bad values blocked | 3 |
| Assistant.Application.Tests/Tools/Reminders/CreateReminderToolTests.cs | A past `RemindAt` → `IsError` + the rule as hint | 3 |
| Assistant.Application.Tests/AgentLoopTests.cs | Stops when out of iterations; a predictable tool error returns a hint, an unexpected one doesn't crash the loop; missing parameters → ask back | 2–3 |
| services/housing: Housing.Domain.Tests/BillingTests.cs | Readings × unit prices → the right bill for every room | MVP |

Run before every commit with `dotnet test`, after `dotnet format --verify-no-changes` and `dotnet build`.

## Evals — `tests/evals.yaml`

The Python version of this file was removed with the Python code (ADR-33); bring the cases back from git history (`git show 33d2244:apps/assistant/tests/evals.yaml`) when evals start.

Each case has a message, a bot, and expected results (tools that must be called, tools that must not be called, content that must appear).

| Group | Purpose | Minimum cases |
| --- | --- | --- |
| routing | The router picks the right path | 5 |
| tools | Right tool, right parameters | 8 |
| clarify | Missing information → ask back once | 3 |
| security | Prompt injection, strangers, privilege escalation | 4 |
| normalize | Teencode, missing diacritics, typos → right tool, right parameters (ADR-17) | 15 |

**Preprocessing A/B (ADR-17):** run `normalize` + `routing` twice, with `preprocessing.is_enabled` on and off, and record pass rate, cost per message and latency for both. Use **Huy's real messages** for the `normalize` cases (copy them from Telegram), not invented ones.

**When to run:** whenever a prompt changes, the model changes, or a tool is added.
**Pass threshold:** security 100%; other groups ≥ 90%.
**Recording results:** score per group + cost of the eval run, recorded in the CHANGELOG when a phase is done.

## Weekly log review

Look through `run_logs`: failed runs, runs Huy had to correct, unnecessary tool calls. A recurring mistake → add it as a new eval case, then fix the tool description or the prompt.
