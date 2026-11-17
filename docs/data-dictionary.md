# Data dictionary

Conventions: every table has `id` (primary key) and `created_at`; times are stored in UTC and shown in Sydney time; schema changes go through migrations (Alembic). The SQLAlchemy models in `src/assistant/infrastructure/db/tables.py` must match this file.

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

## Market tables — MVP · Per persona (market)

Model and rules: [market-data.md](market-data.md), ADR-21. Layers: bronze `raw_records` → silver `observations` → gold `evidence`.

### raw_records — bronze

| Column | Type | Meaning |
| --- | --- | --- |
| source | string | Where it came from, e.g. `open_meteo`, `company_filings` |
| request | json | What was asked (endpoint, parameters) — enough to fetch it again |
| payload | text | Exactly what the source returned; never changed |
| ingested_at | datetime | When the bot fetched it |

### observations — silver

| Column | Type | Meaning |
| --- | --- | --- |
| raw_record_id | FK raw_records | Where it was parsed from |
| series | string | `source:series_id`, as in the factor map |
| entity | string | Company, commodity, region or country it describes |
| period_start_on, period_end_on | date | Period the value describes |
| value | decimal | Value, in `unit` |
| unit | string | e.g. `vnd_bn`, `usd_per_tonne`, `mm_rain`, `percent` |
| value_vs_norm | decimal, nullable | Deviation from the seasonal norm (seasonal series only) |
| published_at | datetime | When it became public — the point-in-time key |

### evidence — gold

| Column | Type | Meaning |
| --- | --- | --- |
| subject | string | Node id of tier 0 this evidence is about |
| factor_id | string | Node id in the factor map |
| tier | int 0–4 | Computed from the factor map (shortest path) |
| path | json | Edge ids from `factor_id` down to the subject |
| statement | text | One sentence the LLM may use |
| direction | enum: +, - | Effect on the subject |
| source_reliability | enum: A–F | Grade of the source for this kind of claim |
| credibility | int 1–6 | Grade of this item (corroboration) |
| kind | enum: fact, model, derived | Fact from a source; model output (ADR-23); or derived note |
| model_run_id | FK model_runs, nullable | Model run that produced it (`kind = model`) |
| observation_ids | json | Silver rows it is built from |
| published_at | datetime | Latest `published_at` among those rows |

### forecasts

| Column | Type | Meaning |
| --- | --- | --- |
| run_id | string | Run that made it |
| subject | string | What it is about |
| statement | text | The forecast, measurable |
| probability | decimal 0–1 | Stated probability |
| evidence_ids | json | Evidence it relied on |
| model | string | LLM used — scoring ignores periods inside its training data |
| due_on | date | When it can be scored |
| outcome | enum: pending, correct, wrong, unclear | Result |
| scored_at | datetime, nullable | When it was scored |

### source_ratings

| Column | Type | Meaning |
| --- | --- | --- |
| source | string | Source name |
| claim_type | string | e.g. `official_figure`, `forecast`, `news`, `social` |
| reliability | enum: A–F | Current grade (F for new sources) |
| hit_count, miss_count | int | Track record used to move the grade |
| updated_at | datetime | Last change |

### sentiment_snapshots — gold (ADR-22)

One row per subject, family and time window. No personal data.

| Column | Type | Meaning |
| --- | --- | --- |
| subject | string | Ticker, sector or market (e.g. `vn_index`) |
| family | enum: market, attention, text | Signal family |
| source | string | e.g. `search_trends`, `press`, `social:<platform>` |
| window_start_at, window_end_at | datetime | Time window |
| post_count | int, nullable | Posts after the bot filter (text family) |
| removed_count | int, nullable | Posts dropped by the bot / coordination filter |
| negative_share, positive_share | decimal 0–1, nullable | Share of negative / positive items |
| value_vs_norm | decimal | Deviation from the recent baseline (e.g. z-score) |
| is_above_threshold | bool | Crossed its threshold in `services/market/config/sentiment.yaml` |
| published_at | datetime | End of window — point-in-time key |

### model_runs — ADR-23 (proposed)

| Column | Type | Meaning |
| --- | --- | --- |
| model_name | string | e.g. `baseline_mean`, `ridge_rates_banks` |
| target | string | What it predicts (series, horizon) |
| trained_from_on, trained_to_on | date | Training window (point-in-time data only) |
| validation | enum: walk_forward | Validation method |
| oos_error | decimal | Out-of-sample error (metric named in `oos_metric`) |
| oos_metric | string | e.g. `mse`, `brier` |
| baseline_oos_error | decimal | Same metric for the baseline model |
| sample_count | int | Observations used |
| trial_number | int | How many models / settings had been tried for this target |

### indicator_ratings — ADR-24 (proposed)

| Column | Type | Meaning |
| --- | --- | --- |
| indicator | string | Indicator, sentiment family or model name |
| regime | string | Regime id defined in `services/market/config/indicator_trust.yaml` |
| horizon_days | int | Forecast horizon |
| scored_count | int | Past calls scored in this regime and horizon |
| score | decimal | Decayed average score (e.g. Brier) |
| trust | decimal 0–1 | Score shrunk toward the average by `scored_count` |
| updated_at | datetime | Last recalculation |
