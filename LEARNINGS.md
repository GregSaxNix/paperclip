# Paperclip learnings

## Server down since 15 October 2026, health check reported success
- **Symptom:** nothing on port 3100, "Paperclip Server" task result 1, "Paperclip HealthCheck" result 0, no `logs/healthcheck.log`.
- **Root cause:** (1) duplicate Postgres services `postgresql-x64-17` and `postgresql17` raced on the same data dir at boot and both stopped, so `pnpm dev` died on ECONNREFUSED 5432. (2) `scripts/paperclip-healthcheck.ps1` contained UTF-8 em dashes; PowerShell 5.1 read them as a quote and the script never parsed. (3) the VBS launcher did not wait, so the task always exited 0.
- **Fix:** `postgresql17` set to Manual. Health check is ASCII-only, starts Postgres if needed, exits 0/1/2, and the VBS passes the code through.
- **Don't try:** adding non-ASCII characters to `.ps1` files run by Windows PowerShell 5.1 unless saved with a BOM.
