"""
Trade Loss Classification & Analysis

Analyzes closed trades to identify dominant failure modes.
If 40%+ of losses share one cause, that's a gate you should build.

This turns random losses into systematic improvement.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
import json


@dataclass
class ClosedTrade:
    """Represents a closed trade with full context."""
    ticket: int
    enter_time: datetime
    close_time: datetime
    direction: int  # 1 = BUY, -1 = SELL
    entry_price: float
    close_price: float
    stop_loss: float
    take_profit: float
    pnl_dollars: float
    pnl_percent: float
    
    # Microstructure at entry
    spread_at_entry: float  # pips
    atr_at_entry: float
    volatility_regime: str  # "HIGH", "MEDIUM", "LOW", "CHOP"
    session_at_entry: str  # "LONDON_OPEN", "NY_OPEN", etc.
    
    # Signal quality
    signal_type: str  # "NYUPIP", "ICT_SWING", "ICT_ATM"
    confidence_at_entry: float
    alert_level: str  # "HIGH", "MEDIUM", "LOW"
    
    # Exit reason
    exit_reason: str  # "SL", "TP", "TIME", "MANUAL"
    
    # Post-close analysis
    price_30min_after_close: Optional[float] = None
    failure_mode: Optional[str] = None  # Assigned after analysis
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d['enter_time'] = self.enter_time.isoformat()
        d['close_time'] = self.close_time.isoformat()
        return d


class LossingTradeAnalyzer:
    """Classifies closed trades by failure mode.
    
    Failure modes:
    - SPREAD_SPIKE: Entered during > 2x normal spread
    - NEWS_BLAST: Entered within 15 min of major event
    - CHOP_TRAP: Entered during compression (range < 0.6× ATR)
    - TIMING_WRONG: Right pattern, wrong session (e.g., NY_OPEN_FADE)
    - STOP_TOO_TIGHT: SL hit but price reversed >3R later
    - FAKE_BREAKOUT: Broke key level but reversed within 5 candles
    - VOLATILITY_CRUSH: Entry quality degraded, ATR dropped
    - REGIME_MISMATCH: Signal type bad for current session
    - UNFAVORABLE_SLIP: Entry slippage > 2× expected
    - OTHER: Doesn't fit clean pattern
    """
    
    FAILURE_MODES = {
        "SPREAD_SPIKE": 0,
        "NEWS_BLAST": 0,
        "CHOP_TRAP": 0,
        "TIMING_WRONG": 0,
        "STOP_TOO_TIGHT": 0,
        "FAKE_BREAKOUT": 0,
        "VOLATILITY_CRUSH": 0,
        "REGIME_MISMATCH": 0,
        "UNFAVORABLE_SLIP": 0,
        "OTHER": 0,
    }
    
    # Normal spread baseline for XAUUSD (pips)
    NORMAL_SPREAD_XAUUSD = 3.5
    
    def classify_trade(self, trade: ClosedTrade) -> str:
        """Determine the primary failure mode for a losing trade.
        
        Returns the failure mode string.
        """
        # Only analyze losing trades
        if trade.pnl_dollars >= 0:
            return "WIN"
        
        # Rule 1: Spread spike at entry
        if trade.spread_at_entry > self.NORMAL_SPREAD_XAUUSD * 2:
            return "SPREAD_SPIKE"
        
        # Rule 2: News within 15 min of entry (would need external calendar)
        # This would require passing in event times; stub for now
        # if time_to_event(trade.enter_time) < 15 min:
        #     return "NEWS_BLAST"
        
        # Rule 3: Entered in chop (volatility_regime == "CHOP")
        if trade.volatility_regime == "CHOP":
            return "CHOP_TRAP"
        
        # Rule 4: Session-specific failure (NY_OPEN is notorious for reversals)
        if trade.session_at_entry == "NY_OPEN" and \
           trade.signal_type in ["NYUPIP", "ICT_SWING"]:
            # Fade signals in NY_OPEN need extra confirmation
            if trade.confidence_at_entry < 75:
                return "TIMING_WRONG"
        
        # Rule 5: Stop too tight (SL hit but would have reversed >3R later)
        if trade.exit_reason == "SL" and trade.price_30min_after_close is not None:
            risk_size = abs(trade.entry_price - trade.stop_loss)
            favorable_move = abs(trade.price_30min_after_close - trade.entry_price)
            
            if favorable_move > risk_size * 3:
                return "STOP_TOO_TIGHT"
        
        # Rule 6: Fake breakout (quick reversal after entry)
        # Requires candle-by-candle lookback; stub for now
        # if reversal_within_5_candles(trade):
        #     return "FAKE_BREAKOUT"
        
        # Rule 7: Volatility crush (ATR dropped post-entry)
        # Would require ATR timeseries; stub for now
        
        # Rule 8: HIGH signal in risky session (regime mismatch)
        if trade.alert_level == "HIGH" and \
           trade.session_at_entry in ["ASIA", "NY_OPEN"]:
            return "REGIME_MISMATCH"
        
        # Rule 9: Unfavorable slippage at entry
        if hasattr(trade, 'actual_entry_price'):
            slippage = abs(trade.actual_entry_price - trade.entry_price)
            if slippage > 3:  # 3 pips
                return "UNFAVORABLE_SLIP"
        
        return "OTHER"
    
    def aggregate_failures(self, trades: List[ClosedTrade]) -> Dict[str, int]:
        """Count failure modes across multiple trades.
        
        Returns:
            {failure_mode: count, ...}
        """
        failures = self.FAILURE_MODES.copy()
        
        for trade in trades:
            if trade.pnl_dollars < 0:  # Only losing trades
                mode = self.classify_trade(trade)
                if mode in failures:
                    failures[mode] += 1
        
        return failures
    
    def dominant_failure_mode(self, trades: List[ClosedTrade]) -> Optional[tuple]:
        """Identify if one failure mode dominates losses.
        
        Returns:
            (failure_mode, percentage) if > 30% of losses are one mode
            None otherwise
        """
        failures = self.aggregate_failures(trades)
        
        losing_trades = [t for t in trades if t.pnl_dollars < 0]
        if not losing_trades:
            return None
        
        total_losses = len(losing_trades)
        
        for mode, count in sorted(failures.items(), key=lambda x: x[1], reverse=True):
            if count == 0:
                continue
            
            pct = (count / total_losses) * 100
            
            if pct > 30:  # Professor's magic number
                return (mode, pct)
        
        return None
    
    def generate_report(self, trades: List[ClosedTrade]) -> str:
        """Generate a human-readable loss analysis report."""
        if not trades:
            return "No trades to analyze."
        
        winning = [t for t in trades if t.pnl_dollars >= 0]
        losing = [t for t in trades if t.pnl_dollars < 0]
        
        total_pnl = sum(t.pnl_dollars for t in trades)
        win_rate = (len(winning) / len(trades) * 100) if trades else 0
        
        failures = self.aggregate_failures(trades)
        dominant = self.dominant_failure_mode(trades)
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                    TRADE LOSS ANALYSIS                         ║
╚════════════════════════════════════════════════════════════════╝

SUMMARY:
  Total Trades:        {len(trades)}
  Winning:             {len(winning)} ({win_rate:.1f}%)
  Losing:              {len(losing)}
  Total P&L:           ${total_pnl:+.2f}

FAILURE MODE BREAKDOWN:
"""
        
        for mode in sorted(failures.keys()):
            count = failures[mode]
            if count > 0 and losing:
                pct = (count / len(losing)) * 100
                report += f"  {mode:20s}  {count:3d} ({pct:5.1f}%)\n"
        
        if dominant:
            mode, pct = dominant
            report += f"""
🎯 DOMINANT FAILURE MODE FOUND:
  {mode} accounts for {pct:.1f}% of losses
  
  → Build a gate to filter this out
  → This is your hidden edge
"""
        else:
            report += f"""
✅ No dominant failure mode (losses are diverse)
   Losses are well-distributed across failure types.
"""
        
        report += """
╚════════════════════════════════════════════════════════════════╝
"""
        return report


class PersistentTradeLogger:
    """Persist trades to SQLite for historical analysis."""
    
    def __init__(self, db_path: str = "data/trades.db"):
        self.db_path = db_path
        try:
            import sqlite3
            self.conn = sqlite3.connect(db_path)
            self._init_schema()
        except ImportError:
            self.conn = None
            print("⚠️ sqlite3 not available; trades won't persist")
    
    def _init_schema(self):
        """Create trades table if not exists."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS closed_trades (
                ticket INTEGER PRIMARY KEY,
                enter_time TEXT,
                close_time TEXT,
                direction INTEGER,
                entry_price REAL,
                close_price REAL,
                stop_loss REAL,
                take_profit REAL,
                pnl_dollars REAL,
                pnl_percent REAL,
                spread_at_entry REAL,
                atr_at_entry REAL,
                volatility_regime TEXT,
                session_at_entry TEXT,
                signal_type TEXT,
                confidence_at_entry REAL,
                alert_level TEXT,
                exit_reason TEXT,
                price_30min_after TEXT,
                failure_mode TEXT
            )
        """)
        self.conn.commit()
    
    def save(self, trade: ClosedTrade):
        """Save a closed trade record."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        d = trade.to_dict()
        
        cols = ', '.join(d.keys())
        placeholders = ', '.join(['?' for _ in d.keys()])
        
        try:
            cursor.execute(
                f"INSERT INTO closed_trades ({cols}) VALUES ({placeholders})",
                list(d.values())
            )
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Failed to save trade {trade.ticket}: {e}")
    
    def get_all_trades(self) -> List[ClosedTrade]:
        """Retrieve all closed trades from database."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM closed_trades ORDER BY close_time")
        
        trades = []
        for row in cursor.fetchall():
            # Reconstruct ClosedTrade from row
            # This is simplified; adjust column order as needed
            pass
        
        return trades
