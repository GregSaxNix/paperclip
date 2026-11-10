# Paperclip learnings

## Server down since 15 October 2026, health check reported success
- **Symptom:** nothing on port 3100, "Paperclip Server" task result 1, "Paperclip HealthCheck" result 0, no `logs/healthcheck.log`.
- **Root cause:** (1) duplicate Postgres services `postgresql-x64-17` and `postgresql17` raced on the same data dir at boot and both stopped, so `pnpm dev` died on ECONNREFUSED 5432. (2) `scripts/paperclip-healthcheck.ps1` contained UTF-8 em dashes; PowerShell 5.1 read them as a quote and the script never parsed. (3) the VBS launcher did not wait, so the task always exited 0.
- **Fix:** `postgresql17` set to Manual. Health check is ASCII-only, starts Postgres if needed, exits 0/1/2, and the VBS passes the code through.
- **Don't try:** adding non-ASCII characters to `.ps1` files run by Windows PowerShell 5.1 unless saved with a BOM.

## Model Lineup Monitor failed silently every Monday from 12 October 2026
- **Symptom:** "Model Lineup Monitor" last result 1 (9 November 2026), and `scripts/model-lineups.log` had no entry after the 6 October manual run, so no weekly research issue was ever posted.
- **Root cause:** on about 6 October the task moved from `python` (every 4 weeks) to `C:\Python313\pythonw.exe` (weekly). Under pythonw there is no console, so `sys.stdout` is `None`, and line 39 of `scripts/check_model_lineups.py` (`if sys.stdout.encoding != "utf-8"`) raised `AttributeError: 'NoneType' object has no attribute 'encoding'` before logging was set up. pythonw also has no stderr, so the traceback went nowhere.
- **Fix:** guard it: `if sys.stdout is not None and sys.stdout.encoding != "utf-8":`. `print()` is a no-op when `sys.stdout` is `None`, so nothing else needed changing.
- **Don't try:** running the script with `python.exe` to reproduce: it works there. Reproduce under pythonw with a wrapper that writes the traceback to a file (`runpy.run_path` inside try/except). Any script moved onto pythonw needs the same check for `sys.stdout.`/`sys.stderr.` attribute use at import time.
