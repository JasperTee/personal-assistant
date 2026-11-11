# Tool and persona specs

Write the spec before coding each tool. The code (Pydantic schema + docstring) must match this file.

## Rules for writing tools

- Group by **task**, don't wrap every API endpoint (e.g. `schedule_event` finds a free slot and then creates the event).
- Prefix names by area: `reminders.create`, `expenses.add`, `email.send`.
- Write descriptions as if briefing a new colleague; name parameters clearly (`amount_aud`, not `amount`).
- Return readable names, not opaque IDs; keep IDs internal.
- `is_error` and `hint` are independent. `is_error` says whether the tool failed; `hint` is an optional suggestion for the next step, on success or failure, and only when the tool actually knows one:
  - predictable error → the broken rule, e.g. "remind_at must be after now (2026-11-11 15:20)";
  - partial success → how to get the rest, e.g. "Showing 20 of 135 expenses; pass category to narrow";
  - unexpected error (network, bug) → no hint; a made-up hint is worse than none.
  The hint only suggests; the agent loop decides what to do next.
- Limit long results (paginate / truncate) and use `hint` to say how to narrow them.
- Declare a `RiskLevel`; Policy relies on it.

## Spec template

```markdown
### <tool name>
- Description (for the LLM):
- RiskLevel:
- Personas allowed:
- Parameters: name — type — required? — meaning — value constraints
- Returns (success):
- Predictable errors + hint (the rule that was broken):
- Value checks in Policy:
- Phase:
```

## Tools

### reminders.create
- **Description:** Create a reminder sent to Huy at a given time. Use when Huy says "remind me…".
- **RiskLevel:** WRITE_SELF
- **Persona:** secretary
- **Parameters:**
  - `content` — string — required — reminder text
  - `remind_at` — datetime (Sydney time) — required — when to remind; not in the past
  - `repeat` — enum (none, daily, weekly) — optional — default none
- **Returns:** "Reminder set: <content> at <time, weekday, date>"
- **Errors + hint:** time in the past → "remind_at must be after now (<current Sydney time>)"
- **Policy checks:** now < `remind_at` < 1 year from now
- **Phase:** 3

### reminders.list
- **Description:** List upcoming reminders.
- **RiskLevel:** READ · **Persona:** secretary · **Phase:** 3
- **Parameters:** `within_days` — int — optional — default 7, max 90

### expenses.add
- **Description:** Record one expense. Use when Huy writes something like "coffee 6 dollars".
- **RiskLevel:** WRITE_SELF
- **Persona:** secretary
- **Parameters:**
  - `amount_aud` — decimal — required — amount > 0
  - `category` — enum (food, transport, housing, education, entertainment, other) — required
  - `note` — string — optional
  - `spent_on` — date — optional — default today
- **Returns:** "Recorded <amount> AUD — <category> — <date>"
- **Errors + hint:** negative/zero amount → "The amount must be greater than 0"
- **Policy checks:** 0 < amount_aud < 10 000; spent_on not in the future
- **Phase:** 3

### expenses.summary
- **Description:** Total spending over a date range, optionally filtered by category.
- **RiskLevel:** READ · **Persona:** secretary · **Phase:** 3
- **Parameters:** `from_date`, `to_date` — date — required; `category` — optional

### email.send *(phase 4)*
- **RiskLevel:** EXTERNAL — always creates a draft awaiting approval
- **Policy checks:** recipient is in `contacts`; at most 1 recipient unless confirmed

### ask_specialist *(phase 5b)*
- **Description:** Ask a specialist bot to do a task in its area and return the result.
- **RiskLevel:** READ (the call itself); the specialist's actions still go through its own Policy
- **Persona:** secretary only
- **Parameters:** `persona` — enum (market, email, research); `task` — string — what to do and the desired output format

## Personas

The actual config lives in `config/personas/*.yaml`.

| Persona | Status | Tools | Proactive |
| --- | --- | --- | --- |
| secretary | On (MVP) | reminders.*, tasks.list, calendar.*, ask_specialist | Morning brief |
| rental | On (MVP) | rental.read_meter_photo, rental.confirm_readings, rental.calculate_bills, rental.render_invoice, tenants.*; later: contracts.*, rooms.*, rental.draft_tenant_message | Rent-day reminders, leases about to expire |
| finance | Off (Should) | expenses.*, receipts.read_photo, budgets.*, finance.report | Budget alerts, weekly report |
| email | Off (Should) | email.* (Gmail + Outlook) | Important mail |
| documents | Off (Should) | docs.ingest, docs.search, docs.ask, docs.organize | Documents about to expire |
| learning | Off (Should) | deadlines.*, study.plan, docs.search, docs.ask, applications.* | Deadline reminders, application follow-ups |
| market | Off (Could) | market.* | Big-move alerts, daily report |
| research | Off (Could) | papers.*, web.search, notes.save, research.subagent | New papers weekly |
