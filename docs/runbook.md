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

1. Install the .NET SDK 10 and build the solution (commands in README.md).
2. Copy `apps/assistant/.env.example` → `apps/assistant/.env`, fill in the **dev bot** token and `OWNER_TELEGRAM_ID` (the real bot token is only on the server: one process per token, ADR-31).
3. Apply the EF Core migrations to create the tables (commands arrive with the database code).
4. Start the bot (long polling, ADR-31): `dotnet run --project src/Assistant.Bot` in `apps/assistant`; stop it with Ctrl+C.
5. Message the dev bot on Telegram; check the rows in `messages` and `run_logs`.

## Deploying to the home server *(write the details when we get there)*

The apps and services run on the home server (ADR-35), reached from the Mac through Tailscale.

- [ ] Install the .NET runtime (or run in Docker), create a dedicated user for the bot (never run as root).
- [ ] Put the secrets on the server only (never copy them through Git).
- [ ] Real bot tokens only on the server; the bot polls, so no inbound port or tunnel is needed for it (ADR-31).
- [ ] Run each bot and service as a service that restarts on failure.
- [ ] Move SQLite → PostgreSQL when needed.

## Releasing an update

1. Run unit tests and evals locally.
2. Pull the new code on the server, run migrations.
3. Restart the service, send a test message.
4. Record it in the CHANGELOG.

## File storage

Original files live on the home server's disk, outside the repository. The database keeps only the metadata and the path.

```text
/srv/
├── assistant/files/      Life's file store (the documents table, ADR-39)
│   └── 2026/11/<id>.pdf  named by id, not by the original name
└── housing/files/        meter photos, invoices, leases, ID cards (owned by housing, ADR-34)
```

- **Files are named by id.** The original name is kept in the database, so a file name never shows what is inside.
- **One folder per service:** a service never reads another service's folder (ADR-34).
- **Sensitive files are encrypted before they are written** (ID cards, passports, visas, bank documents). The disk has no full-disk encryption yet. The key is kept in the secrets, never next to the files.
- **Never** keep files in the repository or in a build folder.

## Backups

Follow the 3-2-1 rule: 3 copies, on 2 kinds of device, 1 of them somewhere else.

| Copy | Where | When | Protects against |
| --- | --- | --- | --- |
| 1 | The home server's disk | Live | — |
| 2 | An external USB disk plugged into the server | Every night | The server's disk failing; fast restore |
| 3 | Cloud object storage (S3 or Backblaze B2), encrypted before upload | Every night | The laptop being lost, stolen or burnt, together with the USB disk |

- **Tool:** `restic`.
  - It encrypts on the server, so the cloud only ever stores encrypted data.
  - It sends only what changed.
  - Keep the restic password in the password manager. Without it the backups cannot be read.
- **What to back up:**
  - a dump of each database (`pg_dump`, or SQLite `.backup`; never copy a live database file);
  - `/srv/*/files`;
  - config.
- **What not to back up:** secrets. They live in the password manager.
- **How long:** keep 7 daily, 4 weekly and 12 monthly snapshots (`restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune`). Nothing is kept longer than 12 months (ADR-27).
- **Test a restore at least once a quarter:** restore to a temporary folder and open the database and a few files. A backup that was never restored is not a backup.
- **Check the disk:** install `smartmontools` and check the SSD's wear monthly; the disk is QLC and wears faster under heavy writes.

## Common problems

| Symptom | Check | Fix |
| --- | --- | --- |
| Bot doesn't reply | Is the process running? Errors in the log? | Restart; check the token |
| Replies "over budget" | Monthly cost in `run_logs` | Find the expensive runs; raise the limit if reasonable |
| A tool keeps failing | `run_logs.error` | Check the external API; update the hint |

## Incident log

| Date | Incident | Cause | Fix |
| --- | --- | --- | --- |
