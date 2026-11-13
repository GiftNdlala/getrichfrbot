# Windows EC2 runtime

This runtime keeps the bot in one process and lets Windows Task Scheduler
restart it after a crash or reboot. It expects the repository to contain a
`.venv` virtual environment and an `.env` file with the MT5 settings.

From an elevated PowerShell window in the repository:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\deploy\windows\install_bot_task.ps1 -StartNow
```

If Python reports `No module named 'encodings'`, the existing virtual
environment may be stale or copied from another machine. Rename or remove
`.venv`, then recreate it with the globally installed Python launcher (`py`),
not the broken environment's `python` command.

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
when the stream is stale.
The URL above assumes the default `BOT_HOST=127.0.0.1`. If `BOT_HOST` is set
to the VM's Tailscale IP below, use that IP in the health-check URL instead;
the server binds only to the configured address.

## SQLite trade history

The bot uses Python's built-in SQLite support; no separate database server or
SQLite installation is needed. Starting the bot creates
`data\trades.sqlite`. Signals, trade details, quote context, and a per-order
event history are stored there. Keep the database on the VM's local disk, not
a network share. Stop the scheduled task before copying the database for a
backup.

Check that the file exists:

```powershell
Test-Path .\data\trades.sqlite
```

## Private dashboard access with Tailscale

The dashboard includes endpoints that can change trading state and close
positions. Do not expose port 5000 directly to the internet or forward it from
the router/EC2 security group. Tailscale provides private access from your
devices without a public dashboard URL.

1. Install Tailscale on the Windows bot VM and sign it into your private
   tailnet (use the official Windows installer). Install/sign in on each
   phone or computer that needs access.
2. On the VM, open PowerShell and run:

   ```powershell
   tailscale ip -4
   ```

3. Copy the returned `100.x.x.x` address into the VM's ignored `.env` file:

   ```dotenv
   BOT_HOST=100.x.x.x
   BOT_PORT=5000
   ```

   Replace `100.x.x.x` with the VM's actual Tailscale IPv4 address. The
   launcher loads `.env` before starting the web server and binds only to that
   address.
   If Windows Firewall blocks access, add a narrow inbound rule from
   Tailscale addresses only, from an elevated PowerShell:

   ```powershell
   New-NetFirewallRule `
     -DisplayName "GetRichFRBot Tailscale dashboard" `
     -Direction Inbound -Protocol TCP -LocalPort 5000 `
     -RemoteAddress 100.64.0.0/10 -Action Allow
   ```

4. Restart the bot task:

   ```powershell
   Stop-ScheduledTask -TaskName GetRichFRBot
   Start-ScheduledTask -TaskName GetRichFRBot
   ```

5. From an authenticated device on your tailnet, open
   `http://100.x.x.x:5000` using the same Tailscale address.

Keep tailnet membership limited to trusted devices/users. Do not enable
Tailscale Funnel, add a public port-forward, or change `BOT_HOST` to
`0.0.0.0`. If your VM's Tailscale address changes, update `.env` and restart
the task. The SQLite file remains on the VM and is not exposed to dashboard
clients. The devices accessing the dashboard must have Tailscale installed
and be signed into your tailnet. `/api/recent_trades` returns the detailed
trade rows, and `/api/trades/<ticket>/events` returns that order's lifecycle
audit events.
