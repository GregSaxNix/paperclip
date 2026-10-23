# Paperclip - Health Check & Auto-Restart
# Modelled on D:\youtube-brain\healthcheck.ps1.
# Checks if the server is responding on port 3100; starts it if not.
# Runs every 5 minutes via Task Scheduler.
#
# Uses pnpm dev (not python); start.cmd already wraps this.
# Keep this file ASCII-only: Windows PowerShell 5.1 reads BOM-less UTF-8 as ANSI,
# and a UTF-8 em dash decodes to a stray quote that breaks parsing.
#
# Exit codes (surface as the scheduled task's Last Run Result):
#   0 = server responding
#   1 = server down and could not be brought up this cycle
#   2 = Postgres (port 5432) down and could not be started

$logFile = "D:\paperclip\logs\healthcheck.log"
$startScript = "D:\paperclip\start.cmd"
$url = "http://127.0.0.1:3100/"
$pgService = "postgresql-x64-17"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$logDir = Split-Path -Parent $logFile
if (-not (Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory -Force | Out-Null
}

function Write-Log($msg) {
    "$timestamp  $msg" | Out-File -Append -FilePath $logFile -Encoding utf8
}

function Test-Server {
    try {
        $r = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        return ($r.StatusCode -eq 200)
    } catch {
        # 404 is fine: root path may not be defined; what matters is the server is responding.
        if ($_.Exception.Response -and [int]$_.Exception.Response.StatusCode -eq 404) { return $true }
        return $false
    }
}

if (Test-Server) { exit 0 }

Write-Log "Server not responding on 3100."

# Paperclip cannot start without Postgres (ECONNREFUSED 5432), so fix that first.
if (-not (Get-NetTCPConnection -LocalPort 5432 -State Listen -ErrorAction SilentlyContinue)) {
    Write-Log "Postgres not listening on 5432. Starting service $pgService..."
    try {
        Start-Service $pgService -ErrorAction Stop
        Start-Sleep -Seconds 5
    } catch {
        Write-Log "FAILED to start ${pgService}: $_"
        exit 2
    }
    if (-not (Get-NetTCPConnection -LocalPort 5432 -State Listen -ErrorAction SilentlyContinue)) {
        Write-Log "FAILED: $pgService started but nothing listening on 5432."
        exit 2
    }
    Write-Log "Postgres is up."
}

Write-Log "Starting Paperclip via start.cmd..."

# start.cmd uses `pnpm dev` which is long-running. Spawn detached.
$proc = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", $startScript `
    -WindowStyle Hidden `
    -PassThru

# pnpm dev needs time to run migrations and bind; poll for up to 90s.
for ($i = 0; $i -lt 18; $i++) {
    Start-Sleep -Seconds 5
    if (Test-Server) {
        Write-Log "Server started successfully (cmd PID: $($proc.Id))"
        exit 0
    }
    if ($proc.HasExited) {
        Write-Log "FAILED: start.cmd exited with code $($proc.ExitCode) before the server came up."
        exit 1
    }
}

Write-Log "FAILED: server not responding 90s after start (cmd PID: $($proc.Id)). Will retry next cycle."
exit 1
