# Operations runbook

## Emergency shutdown

Use when the bot behaves strangely, costs spike, or a key may have leaked.

1. Stop the bot process (local: Ctrl+C; server: stop the service).
2. Revoke the LLM API key in the provider's dashboard.
3. If a Telegram token may have leaked: BotFather → `/revoke` to issue a new token.
4. If Google access may have leaked: revoke the app's access in the Google account.
5. Look through `run_logs` for the problem time window to find the `run_id` and trace the cause.
6. Record the incident and the fix at the end of this file.

## Running locally (phases 1–3)

1. Create a Python 3.12+ virtualenv at the repo root and install each service from its `services/<name>/pyproject.toml` (commands in README.md).
2. Copy `services/assistant/.env.example` → `services/assistant/.env`, fill in the **dev bot** token, `OWNER_TELEGRAM_ID` and a long random `TELEGRAM_WEBHOOK_SECRET` (e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`).
3. Run the Alembic migrations to create the tables in `services/assistant/data/assistant.db`.
4. Start a tunnel in a second terminal: `cloudflared tunnel --url http://localhost:8080`; put the `https://….trycloudflare.com` URL it prints into `TELEGRAM_WEBHOOK_BASE_URL` (it changes every time).
5. Start the bot (webhook, ADR-29): `python -m assistant.main`; it registers `<base URL>/telegram/secretary` with Telegram.
6. Message the dev bot on Telegram; check the rows in `messages` and `run_logs`.

## Deploying to a server *(write this when we get there)*

- [ ] Create a 1–2 GB RAM AWS VPS; open only SSH and HTTPS.
- [ ] Install Python, create a dedicated user for the bot (never run as root).
- [ ] Put `.env` on the server (never copy it through Git).
- [ ] Point `TELEGRAM_WEBHOOK_BASE_URL` at the server's public HTTPS address (tunnel); real bot token and its own `TELEGRAM_WEBHOOK_SECRET`.
- [ ] Run the bot as a service that restarts on failure.
- [ ] Move SQLite → PostgreSQL when needed (ADR-09).

## Releasing an update

1. Run unit tests and evals locally.
2. Pull the new code on the server, run migrations.
3. Restart the service, send a test message.
4. Record it in the CHANGELOG.

## Backups

- SQLite: copy `data/assistant.db` daily, keep the last 7 copies.
- PostgreSQL on AWS: enable automatic backups.
- Test restoring from a backup at least once a quarter.

## Common problems

| Symptom | Check | Fix |
| --- | --- | --- |
| Bot doesn't reply | Is the process running? Errors in the log? | Restart; check the token |
| Replies "over budget" | Monthly cost in `run_logs` | Find the expensive runs; raise the limit if reasonable |
| A tool keeps failing | `run_logs.error` | Check the external API; update the hint |

## Incident log

| Date | Incident | Cause | Fix |
| --- | --- | --- | --- |
