#!/usr/bin/env python3
"""
Trade History Analyzer
Retrieves and analyzes historical trade data from the SQLite database
Can be run standalone without the Flask dashboard
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'trades.sqlite')


def get_trade_history(hours: int = 24) -> List[Dict[str, Any]]:
    """Retrieve trade history from the last N hours"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("   No trades have been recorded yet.")
        return []
    
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all trades within the time window
            cursor.execute("""
                SELECT * FROM trades 
                WHERE timestamp >= ? 
                ORDER BY timestamp DESC
            """, (cutoff_str,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return []


def calculate_pnl(trade: Dict[str, Any]) -> float:
    """Calculate P&L for a trade"""
    # If PnL is already stored, use it
    if trade.get('pnl') is not None and trade.get('pnl') != '':
        try:
            return float(trade['pnl'])
        except (ValueError, TypeError):
            pass
    
    # Otherwise calculate from prices
    if trade.get('status') != 'CLOSED':
        return 0.0
    
    try:
        direction = int(trade.get('direction', 0))
        entry = float(trade.get('entry', 0))
        lots = float(trade.get('lots', 0.01))
        
        # Determine close price (prioritize close_price, then tp, then sl)
        close_price = None
        if trade.get('close_price') is not None and trade.get('close_price') != '':
            close_price = float(trade['close_price'])
        elif trade.get('tp') is not None and trade.get('tp') != '':
            close_price = float(trade['tp'])
        elif trade.get('sl') is not None and trade.get('sl') != '':
            close_price = float(trade['sl'])
        
        if close_price is None or entry == 0:
            return 0.0
        
        # Calculate P&L (for XAUUSD: 1 point = $1 per 0.01 lot)
        if direction == 1:  # BUY
            pnl = (close_price - entry) * lots * 100
        else:  # SELL
            pnl = (entry - close_price) * lots * 100
        
        return pnl
    except (ValueError, TypeError, KeyError):
        return 0.0


def format_trade(trade: Dict[str, Any]) -> Dict[str, Any]:
    """Format a trade for display"""
    direction = int(trade.get('direction', 0))
    pnl = calculate_pnl(trade)
    
    return {
        'Timestamp': trade.get('timestamp', 'N/A'),
        'Ticket': trade.get('ticket', 'N/A'),
        'Strategy': trade.get('engine', 'Unknown'),
        'Direction': 'BUY' if direction == 1 else 'SELL',
        'Entry': f"{float(trade.get('entry', 0)):.2f}",
        'Close': f"{float(trade.get('close_price', 0)):.2f}" if trade.get('close_price') else 'N/A',
        'Lots': f"{float(trade.get('lots', 0)):.2f}",
        'Status': trade.get('status', 'N/A'),
        'P&L': f"${pnl:.2f}",
        'Alert_Level': trade.get('alert_level', 'N/A'),
        'Open_Time': trade.get('open_time', 'N/A'),
        'Close_Time': trade.get('close_time', 'N/A'),
        'Reason': trade.get('reason', 'N/A')
    }


def analyze_trades(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze trade statistics"""
    if not trades:
        return {
            'total_trades': 0,
            'closed_trades': 0,
            'open_trades': 0,
            'wins': 0,
            'losses': 0,
            'breakevens': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'avg_pnl': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'largest_win': 0.0,
            'largest_loss': 0.0,
            'by_strategy': {}
        }
    
    total_trades = len(trades)
    closed_trades = [t for t in trades if t.get('status') == 'CLOSED']
    open_trades = [t for t in trades if t.get('status') in ('OPEN', 'SENT')]
    
    # Calculate P&L stats
    pnls = [calculate_pnl(t) for t in closed_trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    breakevens = [p for p in pnls if p == 0]
    
    total_pnl = sum(pnls)
    avg_pnl = total_pnl / len(closed_trades) if closed_trades else 0
    win_rate = (len(wins) / len(closed_trades) * 100) if closed_trades else 0
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    largest_win = max(wins) if wins else 0
    largest_loss = min(losses) if losses else 0
    
    # By strategy
    by_strategy = {}
    for trade in trades:
        strategy = trade.get('engine', 'Unknown')
        if strategy not in by_strategy:
            by_strategy[strategy] = {
                'total': 0,
                'closed': 0,
                'wins': 0,
                'losses': 0,
                'pnl': 0.0
            }
        
        by_strategy[strategy]['total'] += 1
        
        if trade.get('status') == 'CLOSED':
            by_strategy[strategy]['closed'] += 1
            pnl = calculate_pnl(trade)
            by_strategy[strategy]['pnl'] += pnl
            if pnl > 0:
                by_strategy[strategy]['wins'] += 1
            elif pnl < 0:
                by_strategy[strategy]['losses'] += 1
    
    return {
        'total_trades': total_trades,
        'closed_trades': len(closed_trades),
        'open_trades': len(open_trades),
        'wins': len(wins),
        'losses': len(losses),
        'breakevens': len(breakevens),
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_pnl': avg_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'largest_win': largest_win,
        'largest_loss': largest_loss,
        'by_strategy': by_strategy
    }


def print_report(hours: int, trades: List[Dict[str, Any]], format: str = 'text'):
    """Print a formatted report"""
    
    if format == 'json':
        # JSON output for parsing by other tools
        output = {
            'timeframe': f'{hours} hours',
            'timestamp': datetime.utcnow().isoformat(),
            'trades': [format_trade(t) for t in trades],
            'analysis': analyze_trades(trades)
        }
        print(json.dumps(output, indent=2))
        return
    
    # Text format for human reading
    stats = analyze_trades(trades)
    
    print("\n" + "=" * 80)
    print(f"📊 TRADE HISTORY REPORT - Last {hours} Hours")
    print("=" * 80)
    print(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Database: {DB_PATH}")
    print("=" * 80)
    
    if not trades:
        print("\n❌ No trades found in the specified time period.")
        print(f"   Looking back {hours} hours from now.")
        print("=" * 80 + "\n")
        return
    
    print(f"\n📈 SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total Trades:        {stats['total_trades']}")
    print(f"Closed Trades:       {stats['closed_trades']}")
    print(f"Open Trades:         {stats['open_trades']}")
    print(f"Wins:                {stats['wins']} ({stats['win_rate']:.1f}%)")
    print(f"Losses:              {stats['losses']}")
    print(f"Breakevens:          {stats['breakevens']}")
    print(f"Total P&L:           ${stats['total_pnl']:.2f}")
    print(f"Average P&L:         ${stats['avg_pnl']:.2f}")
    print(f"Average Win:         ${stats['avg_win']:.2f}")
    print(f"Average Loss:        ${stats['avg_loss']:.2f}")
    print(f"Largest Win:         ${stats['largest_win']:.2f}")
    print(f"Largest Loss:        ${stats['largest_loss']:.2f}")
    
    # By Strategy
    if stats['by_strategy']:
        print(f"\n📊 PERFORMANCE BY STRATEGY")
        print("-" * 80)
        for strategy, data in sorted(stats['by_strategy'].items()):
            win_rate = (data['wins'] / data['closed'] * 100) if data['closed'] > 0 else 0
            print(f"\n🔹 {strategy}")
            print(f"   Total: {data['total']} | Closed: {data['closed']} | Wins: {data['wins']} | Losses: {data['losses']}")
            print(f"   Win Rate: {win_rate:.1f}% | Total P&L: ${data['pnl']:.2f}")
    
    # Detailed trade list
    print(f"\n📋 DETAILED TRADE LIST")
    print("-" * 80)
    
    # Header
    print(f"{'Time':<19} {'Ticket':<12} {'Strategy':<15} {'Dir':<6} {'Entry':<8} {'Close':<8} {'P&L':<12} {'Status':<8}")
    print("-" * 80)
    
    # Trades
    for trade in trades:
        formatted = format_trade(trade)
        time_str = formatted['Timestamp'][:19] if formatted['Timestamp'] != 'N/A' else 'N/A'
        
        # Color coding for P&L (if terminal supports it)
        pnl_str = formatted['P&L']
        
        print(f"{time_str:<19} {str(formatted['Ticket']):<12} {formatted['Strategy']:<15} "
              f"{formatted['Direction']:<6} {formatted['Entry']:<8} {formatted['Close']:<8} "
              f"{pnl_str:<12} {formatted['Status']:<8}")
    
    print("=" * 80 + "\n")


def main():
    """Main entry point"""
    # Parse command line arguments
    hours = 24
    format = 'text'
    
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid hours argument: {sys.argv[1]}")
            print("Usage: python get_trade_history.py [hours] [format]")
            print("  hours:  Number of hours to look back (default: 24)")
            print("  format: 'text' or 'json' (default: text)")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        format = sys.argv[2].lower()
        if format not in ('text', 'json'):
            print(f"❌ Invalid format: {format}")
            print("Format must be 'text' or 'json'")
            sys.exit(1)
    
    # Retrieve trades
    trades = get_trade_history(hours)
    
    # Print report
    print_report(hours, trades, format)


if __name__ == '__main__':
    main()
