# Paperclip - Health Check & Auto-Restart
# Modelled on D:\youtube-brain\healthcheck.ps1.
# Checks if the server is responding on port 3100; starts it if not.
# Runs every 5 minutes via Task Scheduler.
#
# Uses pnpm dev (not python) — start.cmd already wraps this.

$logFile = "D:\paperclip\logs\healthcheck.log"
$startScript = "D:\paperclip\start.cmd"
$url = "http://127.0.0.1:3100/"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$logDir = Split-Path -Parent $logFile
if (-not (Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory -Force | Out-Null
}

function Write-Log($msg) {
    "$timestamp  $msg" | Out-File -Append -FilePath $logFile -Encoding utf8
}

try {
    $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 404) {
        # 404 is fine — root path may not be defined; what matters is the server is responding.
        exit 0
    }
} catch {
    Write-Log "Server not responding. Starting via start.cmd..."

    # start.cmd uses `pnpm dev` which is long-running. Spawn detached.
    $proc = Start-Process -FilePath "cmd.exe" `
        -ArgumentList "/c", $startScript `
        -WindowStyle Hidden `
        -PassThru

    # pnpm + Next.js needs ~15-20s to come up
    Start-Sleep -Seconds 20

    try {
        $check = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        if ($check.StatusCode -eq 200 -or $check.StatusCode -eq 404) {
            Write-Log "Server started successfully (cmd PID: $($proc.Id))"
        } else {
            Write-Log "Server started but returned status $($check.StatusCode)"
        }
    } catch {
        Write-Log "Server failed to start within 20s. Error: $_ (may still be coming up — will recheck next cycle)"
    }
}
