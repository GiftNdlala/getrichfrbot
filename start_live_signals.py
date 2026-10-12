#!/usr/bin/env python3
"""Backward-compatible launcher for the Windows production runtime."""

from run_bot_windows import main


def start_live_dashboard():
    main()


if __name__ == "__main__":
    start_live_dashboard()
