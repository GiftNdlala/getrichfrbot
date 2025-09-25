#!/usr/bin/env python3
"""
Quick MT5 order-send smoke test.

Usage (PowerShell/Windows):
  $env:MT5_SERVER="Exness-MT5Trial9"
  $env:MT5_LOGIN="211338841"
  $env:MT5_PASSWORD="your_password"
  python test_place_order.py --symbol XAUUSDm --side buy --tp_points 300 --sl_points 300

If successful, prints the ticket ID; otherwise prints the MT5 error.
"""

import argparse
import sys
import time

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None

from src.mt5_connector import MT5Connector
from src.executor import AutoTrader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="XAUUSDm")
    parser.add_argument("--side", choices=["buy", "sell"], default="buy")
    parser.add_argument("--tp_points", type=float, default=300.0, help="TP distance in points")
    parser.add_argument("--sl_points", type=float, default=300.0, help="SL distance in points")
    args = parser.parse_args()

    if mt5 is None:
        print("MetaTrader5 module not installed. pip install MetaTrader5")
        sys.exit(1)

    # Initialize MT5 via our connector (reads env/server/login/password)
    conn = MT5Connector()
    if not conn.initialize():
        print("❌ MT5 initialize failed - ensure MT5 terminal is running and credentials are set (MT5_SERVER/MT5_LOGIN/MT5_PASSWORD)")
        sys.exit(2)

    # Select symbol
    conn.symbol = args.symbol
    mt5.symbol_select(args.symbol, True)

    tick = mt5.symbol_info_tick(args.symbol)
    info = mt5.symbol_info(args.symbol)
    if not tick or not info:
        print(f"❌ No tick/info for {args.symbol}")
        sys.exit(3)

    point = float(info.point or 0.01)
    price = float(tick.ask or tick.bid or tick.last or 0.0)
    if price <= 0:
        print("❌ Invalid price")
        sys.exit(4)

    # Compute SL/TP around current price
    if args.side == "buy":
        entry = price
        sl = entry - args.sl_points * point
        tp = entry + args.tp_points * point
        direction = 1
    else:
        entry = price
        sl = entry + args.sl_points * point
        tp = entry - args.tp_points * point
        direction = -1

    trader = AutoTrader(args.symbol)
    res = trader.place_market_order(direction=direction, entry=entry, sl=sl, tp=tp)
    if res:
        print(f"✅ Order sent: ticket={res.get('ticket')} volume={res.get('volume')} price={res.get('price')}")
        sys.exit(0)
    else:
        last_error = mt5.last_error() if hasattr(mt5, 'last_error') else None
        print(f"❌ Order send failed. MT5 last_error={last_error}")
        sys.exit(5)


if __name__ == "__main__":
    main()

