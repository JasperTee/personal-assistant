# Dev log

Problems that **changed the direction of the project**, and how they were solved. Newest first.

- **decisions.md** says which design was chosen and why.
- **CHANGELOG.md** says what changed in each version.
- **This file** says what went wrong, why, how it was fixed, and what to remember.

**What goes here:** only problems that changed the architecture, a data contract, the pipeline, or how the project is built and checked. Usually they end in an ADR or a new rule.
**What doesn't:** editor setup, typos, one-off tool errors, small code-review fixes.

## Template

```markdown
### YYYY-MM-DD — <short title>
- **Situation:** what happened / what I noticed
- **Cause:** why it happened
- **Fix:** what I changed (link the commit or ADR)
- **Lesson:** what I'll do differently next time
```

Status tags: no tag = solved; **(open)** = not solved yet.

---

### 2026-11-12 — No input preprocessing step (open)
- **Situation:** most messages are Vietnamese with teencode ("ko", "nhma", "1tr2") and typos, but the pipeline sent raw text straight into context building and the agent loop.
- **Cause:** the pipeline was designed around the happy path; what real input looks like was never written down.
- **Fix:** being decided — options are a cheap model normalising the message before routing, or sending raw text and measuring first. Will be recorded as ADR-17.
- **Lesson:** list what real input looks like (with real examples) before designing the pipeline.

### 2026-11-11 — Dependency rule existed only on paper
- **Situation:** "domain imports nothing" was written in the README, but nothing stopped a wrong import.
- **Cause:** a rule nobody checks gets broken silently.
- **Fix:** import-linter with a `layers` contract and a `forbidden` contract (frameworks out of inner layers); run `lint-imports`. Checked by adding a bad import on purpose: both contracts reported BROKEN with file and line. ADR-16.
- **Lesson:** every architecture rule should have a tool that fails when it is broken.

### 2026-11-11 — Flat structure mixed responsibilities
- **Situation:** tests were flat (`tests/test_policy.py`), so it was hard to tell which test covered which code; `postprocess.py` mixed message formatting with business logic; `tools/reminders.py` held several tools.
- **Cause:** files were grouped by layer only, not by area.
- **Fix:** layer first, then area: `tools/reminders/create.py`; `tests/` mirrors `src/`; MVC controller/presenter inside `channels/`. ADR-16.
- **Lesson:** the path should say what a file is; test path = source path.

### 2026-11-11 — `hint` validator broke "one tool, one job"
- **Situation:** a validator forced `ToolResult.hint` whenever `is_error` was true.
- **Cause:** assumed every error has a known fix. A tool can't invent a hint for a network error, and hints are useful on success too (e.g. "showing 20 of 135").
- **Fix:** removed the validator; `is_error` and `hint` are independent; hint only when the tool actually knows the next step (docs/tools.md).
- **Lesson:** don't couple two fields with a rule unless the rule is always true.
