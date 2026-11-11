# Data dictionary

Conventions: every table has `id` (primary key) and `created_at`; times are stored in UTC and shown in Sydney time; schema changes go through migrations (Alembic). The SQLAlchemy models in `src/assistant/infrastructure/db/models.py` must match this file.

"Scope": **Shared** = used by every bot; **Per persona** = separated by persona.

## users — phase 1 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| telegram_id | string, unique | Telegram id — used for the allowlist |
| display_name | string | Display name |
| role | enum: owner, tenant | Role |

## messages — phase 1 · Per persona

| Column | Type | Meaning |
| --- | --- | --- |
| run_id | string | Link to run_logs |
| persona | string | Which bot |
| user_id | FK users | Who sent it |
| role | enum: user, assistant | Who is speaking |
| content | text | Content |

Kept for 12 months (settings.yaml); older messages are summarised, then deleted.

## run_logs — phases 1–2 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| run_id | string, unique | Run id |
| persona | string | Bot that handled it |
| route | string | Router path (fixed / agent) |
| tools_called | json | Tools called + Policy decisions |
| input_tokens, output_tokens | int | Tokens |
| cost_usd | decimal | Cost |
| duration_ms | int | Duration |
| error | text, nullable | Error, if any |

## facts — phase 2 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| topic | string | e.g. schedule, preferences |
| content | text | Long-term fact |
| updated_at | datetime | Last updated |

## reminders — phase 3 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| content | text | Reminder text |
| remind_at | datetime | When |
| repeat | enum: none, daily, weekly | Repeat |
| status | enum: active, sent, cancelled | Status |

## expenses — phase 3 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| amount_aud | decimal(10,2) | Amount |
| category | string | Category |
| note | text, nullable | Note |
| spent_on | date | Date spent |

## pending_actions — phase 4 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| run_id | string | Run that created it |
| tool | string | Tool to run on approval |
| params | json | Final parameters — run exactly these on approval |
| status | enum: pending, approved, rejected, expired | Status |
| expires_at | datetime | Approval deadline |

## contacts — phase 4 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| name | string | Name |
| email | string, nullable | Email — mail is only sent to addresses in this table |
| relation | string, nullable | Relationship (lecturer, friend, work...) |

## events — phase 5b/6 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| source_persona | string | Bot reporting it |
| kind | string | alert, important_mail, new_papers... |
| summary | text | One-line summary |
| is_read_by_secretary | bool | Already included in the brief? |

## learning_notes — phase 5b · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| topic | string | Topic |
| source_url | string | Article link |
| summary | text | Summary |

## alerts_sent — phase 6 · Shared

| Column | Type | Meaning |
| --- | --- | --- |
| subject | string | Ticker or topic |
| level | enum: info, warning, urgent | Level |
| sent_at | datetime | Used to compute the cooldown |

## source_bookmarks — phase 5 · Shared *(planned, ADR-15)*

How far each source has been read by scheduled runs.

| Column | Type | Meaning |
| --- | --- | --- |
| source | string, unique | e.g. gmail, outlook, calendar, market:NVDA |
| read_until_at | datetime | Everything before this has been read; the next read starts 10 minutes earlier |
| last_error | text, nullable | Why the last read failed — a failed read never moves the bookmark |
| updated_at | datetime | Last successful commit |

## deliveries — phase 5 · Shared *(planned, ADR-15)*

Ledger of what scheduled runs have sent, used for de-duplication and confirm-before-commit. Replaces `events.is_read_by_secretary` and `alerts_sent` once built.

| Column | Type | Meaning |
| --- | --- | --- |
| run_id | string | Run that sent it |
| persona | string | Bot that sent it |
| item_key | string | Stable key of the item (source + source id), used for de-duplication |
| title | string | One-line title shown in the brief |
| source_url | string, nullable | Link back to the source |
| status | enum: posting, sent, held | `held` = no clear answer from Telegram; maybe posted |
| telegram_message_id | string, nullable | Set when Telegram confirms the send |
| sent_at | datetime, nullable | Confirmed send time; also used for alert cooldowns |

## Not stored in the DB

API keys, passwords (→ `.env`). OAuth tokens, if they must be stored, are encrypted with `TOKEN_ENCRYPTION_KEY`.
