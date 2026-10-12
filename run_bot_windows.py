"""Production entrypoint for the Get Rich FR Bot on Windows EC2."""

import os
import signal
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from live_dashboard import (
    app,
    configure_dashboard_logging,
    init_live_stream,
    start_background_monitors,
    stop_background_monitors,
    stop_live_streams,
)


def main() -> None:
    host = os.getenv("BOT_HOST", "0.0.0.0")
    port = int(os.getenv("BOT_PORT", "5000"))
    shutdown_started = False

    def request_shutdown(signum, _frame):
        nonlocal shutdown_started
        if shutdown_started:
            return
        shutdown_started = True
        print(f"Shutdown requested (signal {signum})", flush=True)
        stop_background_monitors()
        stop_live_streams()
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, request_shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, request_shutdown)

    print("Starting Get Rich FR Bot production runtime", flush=True)
    print(f"Dashboard listening on {host}:{port}", flush=True)
    configure_dashboard_logging()
    init_live_stream()
    start_background_monitors()

    try:
        from waitress import serve
    except ImportError as exc:
        raise RuntimeError(
            "Waitress is required for the Windows production runtime. "
            "Install dependencies with: python -m pip install -r requirements.txt"
        ) from exc

    try:
        # One process is intentional: live streams and the MT5 terminal are
        # process-shared and must not be duplicated by multiple web workers.
        serve(app, host=host, port=port, threads=8, asyncore_use_poll=True)
    finally:
        if not shutdown_started:
            stop_background_monitors()
            stop_live_streams()


if __name__ == "__main__":
    main()
