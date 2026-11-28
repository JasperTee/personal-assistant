# Requirements

> Draft — the MoSCoW labels are an initial proposal; Huy reviews and finalises them.

## Goal

A personal AI assistant system for Huy, used through Telegram, made of one **Secretary** that coordinates everything and several **specialist bots**, each playing the role of an expert in one area. Runs 24/7; API cost ≤ $15/month for the MVP, ≤ $50/month with all areas.

## Areas (bots)

| Area | Bot | Expert role | Priority |
| --- | --- | --- | --- |
| Coordinating everything (routes only, ADR-32) | Secretary (hub) | Personal secretary | **Must** |
| Daily life: everything with a date (reminders, to-dos, calendar, study deadlines and schedule), mail, the file store, health and training (ADR-37, ADR-39) | Life | Life manager | **Must** |
| Housing: the rooms Huy rents out (ADR-37) | Housing | Property manager | **Must** |
| Spending, cash flow | Finance | Personal finance adviser | Should |
| Study, science and career: lectures, PTE, scientific papers and topics, daily science updates, applications (ADR-38) | Learning | Teacher, scientist and career adviser | Should |
| Markets, economy | Market | Economist | **Must** (ADR-20) |

## Users

| Role | Who | Access |
| --- | --- | --- |
| Owner | Huy | Every bot, every tool; EXTERNAL actions still need approval |
| Tenant | Tenants (via Zalo, after the MVP) | Only their own invoices and information |
| System | Scheduler | Triggers periodic jobs; no EXTERNAL rights |

## Use cases

Risk by RiskLevel: READ · WRITE_SELF · EXTERNAL · FORBIDDEN. Priority: Must · Should · Could.

### Secretary (SEC)

The Secretary holds no domain tools; it routes through `ask_specialist` (ADR-32). It sends nothing on a schedule: SEC-05 (combined morning brief) is dropped, and each specialist sends its own report instead, at its own pace and only when there is news (REPORT-01 to 05, ADR-39). SEC-02, 03, 04 and 08 moved to the Life bot as LIFE-01 to LIFE-04; the IDs are kept free so older ADRs still point somewhere.

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| SEC-01 | Chat with context | "What did I say about the gym yesterday?" | READ | Must |
| SEC-06 | Ask a specialist bot (`ask_specialist`) | "How much did the rooms bring in this month?" | READ | **Must** (ADR-32: the Secretary's only tool) |
| SEC-07 | Ask about API cost | "How much have I spent on the API this month?" | READ | Must |

### Life (LIFE)

The Life bot owns daily life and everything with a date (ADR-32, ADR-37). Its data lives in `assistant` itself (ADR-36).

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| LIFE-01 (was SEC-02) | Reminders | "Remind me to go to the gym at 7pm tonight" | WRITE_SELF | Must |
| LIFE-02 (was SEC-03) | To-do list | "What do I still have to do today?" | READ | Must |
| LIFE-03 (was SEC-04) | View / create calendar events (Google Calendar) | "When am I free on Friday?" | READ / WRITE_SELF | Should |
| LIFE-04 (was SEC-08) | Log workouts, track running/gym | "Ran 5km in 26 minutes today" | WRITE_SELF | Could |
| LIFE-05 (was EDU-01) | Manage assignment and exam deadlines; remind in advance | "Any deadlines this week?" | WRITE_SELF | Should |
| LIFE-06 (was EDU-02) | Break a big assignment into small tasks, schedule study | "Plan assignment 2" | WRITE_SELF | Should |

### Housing (RENT / HOME)

The Housing bot and service (`services/housing`, ADR-37) cover the rooms Huy rents out (RENT). Huy's own rent and household bills are expenses in Finance (FIN-01), not part of Housing.

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| RENT-01 | Read a photo of a handwritten meter list (electricity, water…) → text; ask back about uncertain cells | (sends a photo) | WRITE_SELF | **Must** |
| RENT-02 | Calculate rent from unit prices and readings | "Calculate November's rent for block A" | WRITE_SELF | **Must** |
| RENT-03 | Export a PDF/PNG invoice for each room, saved to a folder by month / block | "Export November's invoices" | WRITE_SELF | **Must** |
| RENT-03b | Automatically delete invoices and detailed data older than 12 months, meter-book photos older than 3 months (ADR-27) | (automatic, start of each month) | WRITE_SELF (code, not via the LLM) | **Must** |
| RENT-04 | Manage tenants (details, room, contact) | "Who is in room 5, block B?" | READ / WRITE_SELF | **Must** |
| RENT-05 | Manage leases; warn before they expire | "Which leases expire within 30 days?" | READ | Should |
| RENT-06 | Move-out / move-in (check-in, check-out, deposit, final readings) | "Room 3 moves out on the 30th" | WRITE_SELF | Should |
| RENT-07 | Track who has paid and who hasn't; remind on rent day | "Who hasn't paid this month?" | READ | Should |
| RENT-08 | Draft messages to tenants for Huy to send | "Draft a payment reminder for room 7" | READ | Could |
| RENT-09 | Repair request log | "Room 2 reports a broken tap" | WRITE_SELF | Could |
| RENT-10 | Income report by month / block | "Income this quarter by block" | READ | Could |

### Personal finance (FIN)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| FIN-01 | Log an expense, auto-categorised; categories include Rent (the room Huy rents) and Utilities (electricity, internet) | "Coffee 6 dollars", "Paid rent 250" | WRITE_SELF | Should |
| FIN-02 | Photo of a receipt → expense logged automatically | (sends a photo) | WRITE_SELF | Should |
| FIN-03 | Budgets per category; warn when close to / over | (automatic) | READ | Should |
| FIN-04 | Monthly spending report (REPORT-05) | (automatic, 1st of the month) | READ | Should |
| FIN-05 | Recurring payments (phone, subscriptions) | "Which subscriptions am I paying for?" | READ | Could |
| FIN-06 | Analyse and suggest cash-flow improvements | "What should I cut?" | READ | Could |
| FIN-07 | Savings goals | "Save 5000 dollars before June" | WRITE_SELF | Could |
| FIN-08 | Separate rental income/expenses from personal spending | (automatic, pulled from `housing`) | READ | Could |
| FIN-09 | Log work shifts at Huy's one job: date, start, end, break. Huy does not say how it is paid: the code decides (see the bank hours cap below) | "Worked 5pm–10pm today, 30 min break" | WRITE_SELF | Should |
| FIN-10 | Calculate pay per shift and per pay period from the rates in `pay.yaml`: day type (weekday, evening, Saturday, Sunday, public holiday) and payment method (bank and cash each have their own rate and their own pay delay). A shift that crosses the bank hours cap is split: the hours up to the cap are bank, the rest cash | "How much did I earn this week?" | READ | Should |
| FIN-11 | Check a payslip against the logged shifts: hours, rate, gross, tax withheld, super; flag any gap | (sends a payslip photo) → "Short 2 hours on Saturday" | WRITE_SELF | Should |
| FIN-12 | Estimate income tax for the financial year (1 July – 30 June) on all wages, cash and bank, against the tax already withheld; show the likely refund or amount owed. Reference only: the official figure comes from myTax or a registered tax agent | "How much tax will I owe this year?" | READ | Should |
| FIN-13 | Total pay not yet received, split by cash and bank: each shift has an expected pay date from its method's delay; Huy marks it received. Answered on request only, no alerts | "How much pay haven't I received yet?" | WRITE_SELF | Should |
| FIN-14 | Hours summary per week and per fortnight, split by payment method | "How many hours this fortnight?" | READ | Should |

**Work and pay rules:**
- One job, one employer.
- **Bank hours cap:** in each period (`bank_hours_cap` in `pay.yaml`: hours and per week or fortnight), hours are counted in shift order; hours up to the cap are paid to the bank, with tax withheld and a payslip; hours over the cap are paid in cash, with no tax withheld and no payslip. Date ranges with no cap are listed in `pay.yaml`.
- Only bank hours are checked against a payslip.
- Real rates, delays and amounts live only in `pay.yaml` (gitignored) and the database on the home server, never in the repository.
- **Rates come only from `pay.yaml`**, which Huy fills in from his contract or award; the bot never guesses a rate.
- **Tax rates come only from `tax_rates.yaml`**, copied from the ATO for each financial year, together with Huy's residency status for tax. The bot never uses rates from memory.
- **Cash wages count as income** for tax like bank wages. The estimate always includes them, and the year-end summary lists them so they can be declared.
- **A Tax File Number (TFN) is never stored or sent to the LLM**; it is masked when a payslip is read.

### Mail (MAIL), part of Life

The Email bot merged into Life (ADR-39); MAIL IDs are kept.

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| MAIL-01 | Read and summarise mail (Gmail, Outlook) | "Any important mail this morning?" | READ | Should |
| MAIL-02 | Classify, flag important mail | (automatic) | WRITE_SELF | Should |
| MAIL-03 | Draft and send mail — pending approval | "Email Mr Nam asking for a 2-day extension" | EXTERNAL | Should |
| MAIL-04 | Analyse mail (action items, deadlines in it) | "What does this email want me to do?" | READ | Could |

### Files (DOC), part of Life

The Documents bot merged into Life (ADR-39); DOC IDs are kept. Life keeps one store for every file; the specialist of each area summarises its own files and keeps the summaries (DOC-06). Housing files never enter this store (ADR-34).

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| DOC-01 | Receive files (PDF, slides, images, photos of papers) → read, classify, tag, store | (sends a file) | WRITE_SELF | Should |
| DOC-02 | Find a file by asking | "Week 5 slides for the cloud course" | READ | Should |
| DOC-03 | Summarise / Q&A over one document | "What does this lecture say about VPC?" | READ | Should |
| DOC-04 | Remind about documents that are about to expire | (automatic) | READ | Could |
| DOC-05 | Organise folders by course / document type | (automatic) | WRITE_SELF | Could |
| DOC-06 | The area's specialist summarises each new file and keeps the summary (e.g. Learning: lecture summaries per course) | (sends week 6 slides) → Learning saves a summary for that course | WRITE_SELF | Should |

### Learning: study, science and career (EDU / SCI / CAR)

The Research bot merged into Learning (ADR-38); SCI IDs are kept.

Study deadlines and the study schedule moved to Life (LIFE-05, 06; ADR-37). EDU-01 and 02 are kept free so older ADRs still point somewhere.

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| EDU-03 | Explain lectures (using files from DOC) | "Explain the IAM part of the week 6 slides" | READ | Should |
| EDU-04 | Daily PTE practice, grade writing, track frequent mistakes | "Give me today's practice" | READ | Could |
| EDU-05 | Flashcard-style review (spaced repetition) | (automatic) | READ | Could |
| CAR-01 | Track internship applications (company, date, status); remind to follow up | "Where have I applied?" | WRITE_SELF | Should |
| CAR-02 | Tailor CV / cover letter to a job ad | (sends a link) | READ | Could |
| CAR-03 | Interview practice | "Ask me a cloud interview question" | READ | Could |
| CAR-04 | Find and filter suitable job ads | (automatic, weekly) | READ | Could |
| SCI-01 | Explain scientific papers (TL;DR / explanation / deep dive), citing sections | "Explain this arXiv paper" | READ | Could |
| SCI-02 | Learn about a new topic (medicine, technology…), with sources | "What's new in AI agents this week?" | READ | Could |
| SCI-03 | Explain scientific terms | "What is mRNA?" | READ | Could |
| SCI-04 | New papers weekly on followed topics | (automatic) | READ | Could |
| SCI-05 | Save notes, a searchable knowledge base | "What have I read about RAG?" | READ | Could |
| SCI-06 | Morning science newspaper: what the world discovered or invented yesterday (new inventions, studies, breakthroughs), written for a general reader, not a list of papers. At most 5 stories, each a headline + 2–3 plain sentences + source, none sent twice. Under each story, buttons: "Summarise it", "Explain the science", "Go deeper" (ADR-15, ADR-38) | (automatic, every morning) → "Explain the science" on story 2 | READ | Could |

### Market (MKT)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| MKT-01 | Watchlist, daily market report | (automatic) | READ | Could |
| MKT-02 | Early alerts on big moves (thresholds, cooldown, quiet hours) | (automatic) | READ | Could |
| MKT-03 | Read and analyse financial reports | "How did NVIDIA do this quarter?" | READ | Could |
| MKT-04 | Read, filter and connect economic news | "How does this week's news affect the chip sector?" | READ | Could |
| MKT-05 | Portfolio tracking (tracking only, no trading) | "How is my portfolio doing today?" | READ | Could |
| MKT-06 | Upcoming earnings calendar | "Who reports earnings this week?" | READ | Could |
| MKT-07 | Deep multi-factor analysis of a company or sector: causal chains across tiers 0–4, graded evidence, counter-evidence, scenarios with probabilities (docs/market-data.md) | "How will this year's La Niña affect hydropower stocks?" | READ | **Must** |
| MKT-09 | Market-state check: is a move driven by fundamentals or by panic / euphoria (market data, search attention, press and social sentiment; ADR-22) | "Is VN-Index falling because of fear or because of earnings?" | READ | Should |
| MKT-10 | Quantitative baselines: statistics / ML on past data feed the analysis as graded evidence (ADR-23) | "How did bank stocks react to past rate rises?" | READ | Should |
| MKT-11 | Indicator trust by time and regime, from scored past results (ADR-24) | "Which indicators have been most reliable lately?" | READ | Should |
| MKT-08 | Log every forecast and score it when its horizon passes | "How accurate were last quarter's forecasts?" | WRITE_SELF | **Must** |

### Reports (REPORT)

Each specialist sends its own report in its own chat, at the pace of its area (ADR-39):
- Each report is a scheduled run (ADR-15) on the persona's `report` schedule, and each can be turned off.
- **A report with nothing in it is not sent.**
- Urgent things are sent as alerts when they happen, without waiting for the report.

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| REPORT-01 | Life, daily: today's plan, reminders, deadlines, important mail | (automatic, 7am) | READ | Should |
| REPORT-02 | Learning, daily: morning science newspaper (SCI-06) and what is due to study | (automatic, 7am) | READ | Could |
| REPORT-03 | Market, every trading day: market report (MKT-01) | (automatic, 7am on trading days) | READ | Could |
| REPORT-04 | Housing, monthly: rent collected and still owed, leases expiring next month, open repairs | (automatic, 1st of the month) | READ | Should |
| REPORT-05 | Finance, monthly: last month's spending against budget, cash flow (FIN-04) | (automatic, 1st of the month) | READ | Could |

## MVP

**Secretary** (SEC-01, 06, 07) + **Life** (LIFE-01, 02) + **Housing** (RENT-01, 02, 03, 03b, 04) + **Market** (MKT-07, 08) — ADR-20, ADR-32, ADR-36, ADR-37.

Done when: photograph the meter book → the bot reads it and asks about uncertain cells → Huy confirms the whole table → rent is calculated correctly for every room → PDF/PNG invoices are exported to `invoices/<year-month>/<block>/` → Huy sends them to tenants manually; details older than 12 months and photos older than 3 months are deleted automatically.

Market is done when: for one sector with a written factor map, a deep analysis "as of" a date uses only data published before that date, every number in the reply comes from a cited evidence row, tier ≥ 2 evidence comes with a path to the subject, and the forecast is saved in `forecasts` with a horizon to score it.

**Retention (ADR-27):** keep at most the last 12 months of invoice files, readings and detailed calculation results, and the last 3 months of meter-book photos. The latest month's readings are always kept as the "previous reading" for the next month. Tenant info, rooms and unit prices are not deleted by this rule.

## Out of scope

- No automatic stock trading or money transfers.
- Nothing is sent outside (mail, messages to tenants) without approval.
- No sending invoices to tenants in this version (no Zalo, no ZNS): the bot only creates files, Huy sends them. See ADR-12.
- No bulk data deletion.
- No replies to strangers (outside the allowlist).
- Not a substitute for professional advice: leases, deposits, notice periods under NSW rules (NSW Fair Trading), investment advice, medical information — the bot only gives references and drafts; Huy checks and decides.
- Identity documents (passport, visa…) are not sent to the LLM unless it is necessary.
- No local models in this phase.

## Non-functional requirements

| Item | Requirement |
| --- | --- |
| Cost | ≤ $15/month (MVP), ≤ $50/month (all areas); stop and notify when exceeded. The MVP limit is under review now that Market is in the MVP (ADR-20) |
| Response time | Simple messages < 5 seconds; agent tasks < 30 seconds; photo reading + billing < 2 minutes |
| Accuracy | Rent: 100% after Huy's confirmation step; no invoice is issued without approval |
| Availability | 24/7 once on a server |
| Security | Per [threat-model.md](threat-model.md); tenant data and documents are sensitive data |
| Observability | Every run has a run_id, tokens, cost, errors |
| Scheduled runs (phase 5+) | No item is missed or sent twice; a source that fails to read is reported as failed, never as "nothing new"; state changes only after Telegram confirms the send (ADR-15) |
