# Testing and evals

Two layers: **unit tests** (fast, use a fake LLM, cost nothing) and **evals** (run against the real LLM, measure quality).

## Unit tests — `tests/`

`tests/` mirrors `src/assistant/`: the test for `src/assistant/policy/guard.py` is `tests/policy/test_guard.py`. Inside a file, tests are grouped in a `Test<ClassName>` class. Shared fixtures go in `tests/conftest.py`.

| File | Checks | From phase |
| --- | --- | --- |
| domain/test_models.py | Contracts reject wrong types, are frozen, have the right defaults | 1 |
| channels/telegram/test_controller.py | Sample Telegram JSON → `IncomingMessage` with the right persona and time | 1 |
| channels/telegram/test_presenter.py | Long replies split; pending actions get Send/Cancel buttons | 1 |
| policy/test_access.py | Strangers blocked; each persona gets only its tools | 3 |
| policy/test_guard.py | EXTERNAL awaits approval; FORBIDDEN rejected; bad values blocked | 3 |
| tools/reminders/test_create.py | A past `remind_at` → `is_error` + the rule as hint | 3 |
| orchestration/test_agent_loop.py | Stops when out of iterations; a predictable tool error returns a hint, an unexpected one doesn't crash the loop; missing parameters → ask back | 2–3 |
| domain/rental/test_billing.py | Readings × unit prices → the right bill for every room | MVP |

Run before every commit, together with `ruff check .` and `lint-imports`.

## Evals — `tests/evals.yaml`

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
