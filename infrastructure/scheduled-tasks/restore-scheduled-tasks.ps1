# restore-scheduled-tasks.ps1
#
# Idempotent re-installer for every scheduled task whose XML is tracked in
# this directory. Run as Administrator from PowerShell:
#
#   powershell.exe -ExecutionPolicy Bypass -File `
#     D:\TalentMap\infrastructure\scheduled-tasks\restore-scheduled-tasks.ps1
#
# After running, open Task Scheduler MMC (taskschd.msc) and set the run-as
# password on each task. Windows stores passwords in LSA (not the XML), so
# they don't survive a fresh install.
#
# Filename convention: a task with spaces in its name encodes each space as
# the literal `__SPACE__`. Example: `TalentMap SQLite Backup` lives at
# `TalentMap__SPACE__SQLite__SPACE__Backup.xml`.
#
# Note: XML files in this directory must be UTF-16LE with BOM (the encoding
# `schtasks /query /xml` emits). The .gitattributes file marks them as binary
# to prevent IDEs/linters from silently re-encoding them as UTF-8 (which
# `schtasks /create /xml` rejects as "malformed document syntax").
#
# Exit code = number of tasks that failed to install.

Set-StrictMode -Version Latest

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$xmls = @(Get-ChildItem -Path $here -Filter *.xml -File)

if ($xmls.Count -eq 0) {
    Write-Host "No *.xml files found under $here. Nothing to restore." -ForegroundColor Yellow
    exit 0
}

Write-Host "Restoring $($xmls.Count) scheduled task(s) from $here" -ForegroundColor Cyan
Write-Host ""

$failures = 0
foreach ($xml in $xmls) {
    $taskName = $xml.BaseName -replace '__SPACE__', ' '
    # Delete first (idempotent: ignore "task not found")
    & schtasks /delete /tn $taskName /f 2>$null | Out-Null
    # Then create from XML
    $createOutput = & schtasks /create /tn $taskName /xml $xml.FullName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK   $taskName" -ForegroundColor Green
    } else {
        $failures++
        Write-Host "  FAIL $taskName" -ForegroundColor Red
        Write-Host "       $createOutput" -ForegroundColor Yellow
    }
}

Write-Host ""
$summaryColor = if ($failures -eq 0) { 'Green' } else { 'Red' }
Write-Host "$($xmls.Count - $failures) succeeded, $failures failed" -ForegroundColor $summaryColor

if ($failures -gt 0) {
    Write-Host ""
    Write-Host "Common causes of FAIL:" -ForegroundColor Yellow
    Write-Host "  - Run-as user account doesn't exist on this machine (XML embeds the username)" -ForegroundColor Yellow
    Write-Host "  - Drive layout mismatch (XML embeds D:\... paths)" -ForegroundColor Yellow
    Write-Host "  - PowerShell not running as Administrator" -ForegroundColor Yellow
    Write-Host "  - XML files re-encoded as UTF-8 (must be UTF-16LE - see .gitattributes)" -ForegroundColor Yellow
}

exit $failures