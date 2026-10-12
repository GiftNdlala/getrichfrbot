param(
    [string]$ProjectPath = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $ProjectPath

$pythonPath = Join-Path $ProjectPath ".venv\Scripts\python.exe"
$entrypoint = Join-Path $ProjectPath "run_bot_windows.py"
$logDirectory = Join-Path $ProjectPath "logs"
$logPath = Join-Path $logDirectory "bot-service.log"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Python virtual environment not found at $pythonPath"
}
if (-not (Test-Path -LiteralPath $entrypoint)) {
    throw "Bot entrypoint not found at $entrypoint"
}

New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
Add-Content -LiteralPath $logPath -Value "[$(Get-Date -Format o)] Starting bot service"

& $pythonPath -u $entrypoint *>> $logPath
$exitCode = $LASTEXITCODE
Add-Content -LiteralPath $logPath -Value "[$(Get-Date -Format o)] Bot service exited with code $exitCode"
exit $exitCode
