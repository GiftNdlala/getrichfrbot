# Windows EC2 runtime

This runtime keeps the bot in one process and lets Windows Task Scheduler
restart it after a crash or reboot. It expects the repository to contain a
`.venv` virtual environment and an `.env` file with the MT5 settings.

From an elevated PowerShell window in the repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\deploy\windows\install_bot_task.ps1 -StartNow
```

The task runs under the Windows account supplied during installation. Use the
same account that owns or can start the MetaTrader 5 terminal. The launcher
writes process output to `logs\bot-service.log`.

Useful checks:

```powershell
Get-ScheduledTask -TaskName GetRichFRBot
Get-ScheduledTaskInfo -TaskName GetRichFRBot
Invoke-WebRequest http://127.0.0.1:5000/api/health
```

The health endpoint returns HTTP 200 only after the streams are running and
have produced a recent market update. It returns HTTP 503 while starting or
when the stream is stale, which is useful for Cloudflared or external
monitoring.

Do not expose port 5000 directly to the public internet. Restrict the EC2
security group and use Cloudflared for mobile access.
