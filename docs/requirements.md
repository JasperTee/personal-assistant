# Requirements

> Draft — the MoSCoW labels are an initial proposal; Huy reviews and finalises them.

## Goal

A personal AI assistant system for Huy, used through Telegram, made of one **Secretary** that coordinates everything and several **specialist bots**, each playing the role of an expert in one area. Runs 24/7; API cost ≤ $15/month for the MVP, ≤ $50/month with all areas.

## Areas (bots)

| Area | Bot | Expert role | Priority |
| --- | --- | --- | --- |
| Coordinating everything | Secretary (hub) | Personal secretary | **Must** |
| Rental properties | Rental | Property manager | **Must** |
| Spending, cash flow | Finance | Personal finance adviser | Should |
| Gmail, Outlook | Email | Administrative assistant | Should |
| Papers, lectures, images | Documents | Records manager | Should |
| Study, career, deadlines | Learning & Career | Study and career adviser | Should |
| Markets, economy | Market | Economist | Could |
| Scientific papers | Research | Scientist | Could |
| Health, training | (inside Secretary) | Coach | Could |

## Users

| Role | Who | Access |
| --- | --- | --- |
| Owner | Huy | Every bot, every tool; EXTERNAL actions still need approval |
| Tenant | Tenants (via Zalo, after the MVP) | Only their own invoices and information |
| System | Scheduler | Triggers periodic jobs; no EXTERNAL rights |

## Use cases

Risk by RiskLevel: READ · WRITE_SELF · EXTERNAL · FORBIDDEN. Priority: Must · Should · Could.

### Secretary (SEC)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| SEC-01 | Chat with context | "What did I say about the gym yesterday?" | READ | Must |
| SEC-02 | Reminders | "Remind me to go to the gym at 7pm tonight" | WRITE_SELF | Must |
| SEC-03 | To-do list | "What do I still have to do today?" | READ | Must |
| SEC-04 | View / create calendar events (Google Calendar) | "When am I free on Friday?" | READ / WRITE_SELF | Should |
| SEC-05 | Morning brief compiled from every bot | (automatic, 7am) | READ | Should |
| SEC-06 | Ask a specialist bot (`ask_specialist`) | "How much did the rentals bring in this month?" | READ | Should |
| SEC-07 | Ask about API cost | "How much have I spent on the API this month?" | READ | Must |
| SEC-08 | Log workouts, track running/gym | "Ran 5km in 26 minutes today" | WRITE_SELF | Could |

### Rental (RENT)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| RENT-01 | Read a photo of a handwritten meter list (electricity, water…) → text; ask back about uncertain cells | (sends a photo) | WRITE_SELF | **Must** |
| RENT-02 | Calculate rent from unit prices and readings | "Calculate November's rent for block A" | WRITE_SELF | **Must** |
| RENT-03 | Export a PDF/PNG invoice for each room, saved to a folder by month / block | "Export November's invoices" | WRITE_SELF | **Must** |
| RENT-03b | Automatically delete invoices and detailed data older than 3 months | (automatic, start of each month) | WRITE_SELF (code, not via the LLM) | **Must** |
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
| FIN-01 | Log an expense, auto-categorised | "Coffee 6 dollars" | WRITE_SELF | Should |
| FIN-02 | Photo of a receipt → expense logged automatically | (sends a photo) | WRITE_SELF | Should |
| FIN-03 | Budgets per category; warn when close to / over | (automatic) | READ | Should |
| FIN-04 | Weekly / monthly spending report | (automatic, Sunday) | READ | Should |
| FIN-05 | Recurring payments (phone, subscriptions) | "Which subscriptions am I paying for?" | READ | Could |
| FIN-06 | Analyse and suggest cash-flow improvements | "What should I cut?" | READ | Could |
| FIN-07 | Savings goals | "Save 5000 dollars before June" | WRITE_SELF | Could |
| FIN-08 | Separate rental income/expenses from personal spending | (automatic, pulled from RENT) | READ | Could |

### Email (MAIL)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| MAIL-01 | Read and summarise mail (Gmail, Outlook) | "Any important mail this morning?" | READ | Should |
| MAIL-02 | Classify, flag important mail | (automatic) | WRITE_SELF | Should |
| MAIL-03 | Draft and send mail — pending approval | "Email Mr Nam asking for a 2-day extension" | EXTERNAL | Should |
| MAIL-04 | Analyse mail (action items, deadlines in it) | "What does this email want me to do?" | READ | Could |

### Documents (DOC)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| DOC-01 | Receive files (PDF, slides, images, photos of papers) → read, classify, tag, store | (sends a file) | WRITE_SELF | Should |
| DOC-02 | Find a file by asking | "Week 5 slides for the cloud course" | READ | Should |
| DOC-03 | Summarise / Q&A over one document | "What does this lecture say about VPC?" | READ | Should |
| DOC-04 | Remind about documents that are about to expire | (automatic) | READ | Could |
| DOC-05 | Organise folders by course / document type | (automatic) | WRITE_SELF | Could |

### Learning & Career (EDU / CAR)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| EDU-01 | Manage assignment and exam deadlines; remind in advance | "Any deadlines this week?" | WRITE_SELF | Should |
| EDU-02 | Break a big assignment into small tasks, schedule study | "Plan assignment 2" | WRITE_SELF | Should |
| EDU-03 | Explain lectures (using files from DOC) | "Explain the IAM part of the week 6 slides" | READ | Should |
| EDU-04 | Daily PTE practice, grade writing, track frequent mistakes | "Give me today's practice" | READ | Could |
| EDU-05 | Flashcard-style review (spaced repetition) | (automatic) | READ | Could |
| CAR-01 | Track internship applications (company, date, status); remind to follow up | "Where have I applied?" | WRITE_SELF | Should |
| CAR-02 | Tailor CV / cover letter to a job ad | (sends a link) | READ | Could |
| CAR-03 | Interview practice | "Ask me a cloud interview question" | READ | Could |
| CAR-04 | Find and filter suitable job ads | (automatic, weekly) | READ | Could |

### Market (MKT)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| MKT-01 | Watchlist, daily market report | (automatic) | READ | Could |
| MKT-02 | Early alerts on big moves (thresholds, cooldown, quiet hours) | (automatic) | READ | Could |
| MKT-03 | Read and analyse financial reports | "How did NVIDIA do this quarter?" | READ | Could |
| MKT-04 | Read, filter and connect economic news | "How does this week's news affect the chip sector?" | READ | Could |
| MKT-05 | Portfolio tracking (tracking only, no trading) | "How is my portfolio doing today?" | READ | Could |
| MKT-06 | Upcoming earnings calendar | "Who reports earnings this week?" | READ | Could |

### Research (SCI)

| ID | Use case | Example message | Risk | Priority |
| --- | --- | --- | --- | --- |
| SCI-01 | Explain scientific papers (TL;DR / explanation / deep dive), citing sections | "Explain this arXiv paper" | READ | Could |
| SCI-02 | Learn about a new topic (medicine, technology…), with sources | "What's new in AI agents this week?" | READ | Could |
| SCI-03 | Explain scientific terms | "What is mRNA?" | READ | Could |
| SCI-04 | New papers weekly on followed topics | (automatic) | READ | Could |
| SCI-05 | Save notes, a searchable knowledge base | "What have I read about RAG?" | READ | Could |

## MVP

**Secretary** (SEC-01, 02, 03, 07) + **Rental** (RENT-01, 02, 03, 03b, 04).

Done when: photograph the meter book → the bot reads it and asks about uncertain cells → Huy confirms the whole table → rent is calculated correctly for every room → PDF/PNG invoices are exported to `invoices/<year-month>/<block>/` → Huy sends them to tenants manually; data older than 3 months is deleted automatically; and reminders run reliably.

**Retention:** keep at most the last 3 months of invoice files, meter-book photos, readings and detailed calculation results. The latest month's readings are always kept as the "previous reading" for the next month. Tenant info, rooms and unit prices are not deleted by this rule.

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
| Cost | ≤ $15/month (MVP), ≤ $50/month (all areas); stop and notify when exceeded |
| Response time | Simple messages < 5 seconds; agent tasks < 30 seconds; photo reading + billing < 2 minutes |
| Accuracy | Rent: 100% after Huy's confirmation step; no invoice is issued without approval |
| Availability | 24/7 once on a server |
| Security | Per [threat-model.md](threat-model.md); tenant data and documents are sensitive data |
| Observability | Every run has a run_id, tokens, cost, errors |
| Scheduled runs (phase 5+) | No item is missed or sent twice; a source that fails to read is reported as failed, never as "nothing new"; state changes only after Telegram confirms the send (ADR-15) |
