# Paperclip scheduled-tasks DR snapshot

DR snapshots of every Windows scheduled task that runs Paperclip on Greg's machine. XMLs are written daily by [D:\scripts\export-scheduled-tasks.ps1](https://github.com/GregSaxNix/ops-scripts/blob/main/export-scheduled-tasks.ps1) and committed to this repo.

Source of truth for these tasks lives at [D:\scripts\inventory.yaml](https://github.com/GregSaxNix/ops-scripts/blob/main/inventory.yaml). Adding or removing a task = editing that file.

| Task | XML file | Schedule | Launcher |
|---|---|---|---|
| `Paperclip HealthCheck` | `Paperclip__SPACE__HealthCheck.xml` | Every 5 min | `launchers/paperclip-healthcheck-hidden.vbs` |
| `Paperclip Server` | `Paperclip__SPACE__Server.xml` | At startup (always running) | (calls `D:\paperclip\start.cmd` directly) |

## Restore

Open PowerShell as Administrator:

```powershell
powershell.exe -ExecutionPolicy Bypass -File `
  D:\paperclip\infrastructure\scheduled-tasks\restore-scheduled-tasks.ps1
```

After restore, open Task Scheduler MMC (`taskschd.msc`) and set the run-as password on each task -- Windows LSA passwords aren't part of the XML.

See [D:\scripts\RECOVERY.md](https://github.com/GregSaxNix/ops-scripts/blob/main/RECOVERY.md) for the full fresh-machine procedure.

## Filename convention

Task names with spaces have those encoded as `__SPACE__` in the XML filename:

- Task name: `Paperclip HealthCheck`
- XML filename: `Paperclip__SPACE__HealthCheck.xml`

The restore script reverses this when calling `schtasks /create /tn`.
