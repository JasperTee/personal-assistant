# Testing and evals

Two layers: **unit tests** (fast, use a fake LLM, cost nothing) and **evals** (run against the real LLM, measure quality).

## Unit tests — `tests/`

| File | Checks | From phase |
| --- | --- | --- |
| test_channels.py | Sample Telegram JSON → `IncomingMessage` with the right persona and time | 1 |
| test_policy.py | Strangers blocked; EXTERNAL awaits approval; FORBIDDEN rejected; bad values blocked | 3 |
| test_agent_loop.py | Stops when out of iterations; a predictable tool error returns a hint, an unexpected one doesn't crash the loop; missing parameters → ask back | 2–3 |

Run before every commit.

## Evals — `tests/evals.yaml`

Each case has a message, a bot, and expected results (tools that must be called, tools that must not be called, content that must appear).

| Group | Purpose | Minimum cases |
| --- | --- | --- |
| routing | The router picks the right path | 5 |
| tools | Right tool, right parameters | 8 |
| clarify | Missing information → ask back once | 3 |
| security | Prompt injection, strangers, privilege escalation | 4 |

**When to run:** whenever a prompt changes, the model changes, or a tool is added.
**Pass threshold:** security 100%; other groups ≥ 90%.
**Recording results:** score per group + cost of the eval run, recorded in the CHANGELOG when a phase is done.

## Weekly log review

Look through `run_logs`: failed runs, runs Huy had to correct, unnecessary tool calls. A recurring mistake → add it as a new eval case, then fix the tool description or the prompt.
