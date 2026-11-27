# Ideas

Ideas parked during the architecture freeze (ADR-35). An idea here is not a decision: when the freeze ends, an idea that is still wanted gets an ADR before any work starts. Newest first.

| Idea | Notes | Added |
| --- | --- | --- |
| Family access to `rental-web` | Run on the home server behind Cloudflare Tunnel + Cloudflare Access (sign in with Google), so no port is opened. Install it as a web app on phones (PWA) instead of app stores. | 2026-11-27 |
| Personal domain | One personal domain with subdomains (e.g. `rent.<domain>`). Buy it when `rental-web` starts. The study app gets its own domain. | 2026-11-27 |
| Tool search for large tool lists | If one bot's tool definitions grow past roughly 10K tokens, load tools on demand (tool search, `defer_loading`) instead of sending them all. | 2026-11-27 |
| Try Go | One small service in Go to learn it, possible because each service builds alone (ADR-34). Only after the freeze ends. | 2026-11-27 |
