"""
Backfill missing close_price and pnl from MT5 history for closed trades.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta

try:
    import MetaTrader5 as mt5
except ImportError:
    print("❌ MetaTrader5 module not installed. Please install it: pip install MetaTrader5")
    exit(1)

DB_PATH = Path(__file__).parent / "data" / "trades.sqlite"


def initialize_mt5():
    """Initialize MT5 connection"""
    terminal_path = os.getenv('MT5_TERMINAL_PATH')
    if terminal_path:
        ok = mt5.initialize(path=terminal_path)
    else:
        ok = mt5.initialize()
    
    if not ok:
        print(f"❌ MT5 initialization failed: {mt5.last_error()}")
        return False
    
    print("✅ MT5 initialized successfully")
    return True


def fetch_deals_for_position(ticket: int):
    """Fetch all deals for a specific position"""
    try:
        deals = mt5.history_deals_get(position=ticket)
        return deals if deals else []
    except Exception as e:
        print(f"⚠️ Error fetching deals for ticket {ticket}: {e}")
        return []


def fetch_recent_deals(days: int = 14):
    """Fetch all deals from the last N days"""
    try:
        end = datetime.now()
        start = end - timedelta(days=days)
        deals = mt5.history_deals_get(start, end)
        return deals if deals else []
    except Exception as e:
        print(f"⚠️ Error fetching recent deals: {e}")
        return []


def backfill_from_mt5():
    """Backfill close_price and pnl from MT5 history"""
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return
    
    if not initialize_mt5():
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Get all closed trades missing close_price or pnl
    rows = conn.execute(
        """
        SELECT ticket, direction, entry, lots, status, timestamp, close_price, pnl
        FROM trades
        WHERE status = 'CLOSED'
          AND (close_price IS NULL OR close_price = '' OR pnl IS NULL OR pnl = '')
        ORDER BY timestamp DESC
        LIMIT 2000
        """
    ).fetchall()
    
    if not rows:
        print("✅ No trades require backfill.")
        conn.close()
        mt5.shutdown()
        return
    
    print(f"📊 Found {len(rows)} closed trades missing data")
    
    # First, try to fetch deals by position
    updated_count = 0
    not_found_count = 0
    
    for i, row in enumerate(rows, 1):
        ticket = row["ticket"]
        
        if i % 50 == 0:
            print(f"   Progress: {i}/{len(rows)}...")
        
        # Fetch deals for this specific position
        deals = fetch_deals_for_position(ticket)
        
        if not deals:
            not_found_count += 1
            continue
        
        # Find the exit deal (type 1)
        exit_deal = None
        for d in deals:
            deal_type = getattr(d, 'type', None)
            if deal_type == 1:  # Exit deal
                if not exit_deal or getattr(d, 'time', 0) >= getattr(exit_deal, 'time', 0):
                    exit_deal = d
        
        if not exit_deal:
            # Fallback to latest deal
            exit_deal = max(deals, key=lambda d: getattr(d, 'time', 0))
        
        if exit_deal:
            close_price = float(getattr(exit_deal, 'price', 0.0))
            pnl = float(getattr(exit_deal, 'profit', 0.0))
            close_time = getattr(exit_deal, 'time', None)
            
            if close_price > 0:
                updates = {}
                if not row['close_price'] or row['close_price'] == '':
                    updates['close_price'] = close_price
                if not row['pnl'] or row['pnl'] == '':
                    updates['pnl'] = pnl
                if close_time:
                    updates['close_time'] = datetime.fromtimestamp(close_time).isoformat()
                
                if updates:
                    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
                    values = list(updates.values()) + [ticket]
                    conn.execute(f"UPDATE trades SET {set_clause} WHERE ticket = ?", values)
                    updated_count += 1
    
    conn.commit()
    conn.close()
    mt5.shutdown()
    
    print(f"\n✅ Backfill complete!")
    print(f"   Updated: {updated_count} trades")
    print(f"   Not found in MT5: {not_found_count} trades")
    
    if not_found_count > 0:
        print(f"\n⚠️ {not_found_count} trades could not be found in MT5 history.")
        print("   This is normal for older trades beyond MT5's history window.")


if __name__ == "__main__":
    backfill_from_mt5()
