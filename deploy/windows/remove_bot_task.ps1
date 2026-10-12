param([string]$TaskName = "GetRichFRBot")

$ErrorActionPreference = "Stop"
Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Removed scheduled task '$TaskName'."
