# Tool and persona specs

Write the spec before coding each tool. The code (tool name, description and input schema) must match this file.

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
- **Persona:** life
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
- **RiskLevel:** READ · **Persona:** life · **Phase:** 3
- **Parameters:** `within_days` — int — optional — default 7, max 90

### expenses.add
- **Description:** Record one expense. Use when Huy writes something like "coffee 6 dollars".
- **RiskLevel:** WRITE_SELF
- **Persona:** finance
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
- **RiskLevel:** READ · **Persona:** finance · **Phase:** 3
- **Parameters:** `from_date`, `to_date` — date — required; `category` — optional

### email.send *(phase 4)*
- **RiskLevel:** EXTERNAL — always creates a draft awaiting approval
- **Policy checks:** recipient is in `contacts`; at most 1 recipient unless confirmed

### ask_specialist *(phase 5b)*
- **Description:** Ask a specialist bot to do a task in its area and return the result.
- **RiskLevel:** READ (the call itself); the specialist's actions still go through its own Policy
- **Persona:** secretary only
- **Parameters:** `persona` — enum (life, housing, finance, market; more as specialists are added); `task` — string — what to do and the desired output format

## Personas

The actual config lives in `apps/assistant/config/personas/`. Reports (ADR-39): each persona's `report` sets its pace (`every`: daily, trading_days, monthly); a report with nothing in it is not sent, and urgent alerts do not wait for the report. Two tiers (ADR-32): the Secretary only routes; each specialist holds its area's tools and is its own Telegram bot. Write tools act only on the specialist's own service; read-only tools on other services are allowed.

| Persona | Status | Tools | Proactive |
| --- | --- | --- | --- |
| secretary | On (MVP) | ask_specialist only | None (each specialist sends its own report, ADR-39) |
| life | On (MVP) | reminders.*, tasks.list, calendar.*, deadlines.*, study.plan, email.* (Gmail + Outlook), docs.ingest, docs.search, docs.ask, docs.organize; later: workouts.* (ADR-36, ADR-37, ADR-39) | Daily report, reminders, deadline reminders, important mail, documents about to expire |
| housing | On (MVP) | housing.read_meter_photo, housing.confirm_readings, housing.calculate_bills, housing.render_invoice, tenants.*; later: contracts.*, rooms.*, housing.draft_tenant_message | Monthly report, rent-day reminders, leases about to expire |
| finance | Off (Should) | expenses.*, receipts.read_photo, budgets.*, finance.report, shifts.*, pay.calculate, payslips.read_photo, tax.estimate; read-only: rental income from `housing` | Monthly report, budget alerts |
| learning | Off (Should) | docs.search, docs.ask (read-only, Life's file store), notes.save (summaries per course), applications.*, papers.*, web.search, research.subagent; later: pte.practice, flashcards.* (deadlines are Life's, ADR-37; science from Research, ADR-38) | Daily report (science newspaper), application follow-ups, new papers weekly |
| market | Off (Could) | market.* | Report every trading day, big-move alerts |
