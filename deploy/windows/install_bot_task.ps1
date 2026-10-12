param(
    [string]$TaskName = "GetRichFRBot",
    [string]$ProjectPath = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [switch]$StartNow
)

$ErrorActionPreference = "Stop"
$launcher = Join-Path $ProjectPath "deploy\windows\start_bot.ps1"
if (-not (Test-Path -LiteralPath $launcher)) {
    throw "Launcher not found at $launcher"
}

$credential = Get-Credential -Message "Enter the Windows account that should run MT5 and the bot"
$action = New-ScheduledTaskAction `
    -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$launcher`" -ProjectPath `"$ProjectPath`"" `
    -WorkingDirectory $ProjectPath

$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -User $credential.UserName `
    -Password $credential.GetNetworkCredential().Password `
    -RunLevel Highest `
    -Description "Starts and restarts the Get Rich FR Bot production runtime." `
    -Force | Out-Null

Write-Host "Installed scheduled task '$TaskName'."
if ($StartNow) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Started scheduled task '$TaskName'."
}
