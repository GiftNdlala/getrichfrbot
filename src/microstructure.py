"""
Microstructure Analysis Module

Detects real market conditions that defeat elegant strategies:
- Spread spike detection (liquidity crisis)
- Chop/compression detection (false breakouts)
- Session regime identification (time-of-day bias)
"""

from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


class SpreadAnalyzer:
    """Tracks and analyzes bid-ask spread relative to recent median.
    
    Live XAUUSD spread is 2-5 pips typically.
    Spike detection: current > 2x median = SKIP
    Halt condition: current > 3x median = HALT
    """
    
    def __init__(self, lookback_minutes: int = 60, window_size: int = 120):
        """
        Args:
            lookback_minutes: How far back to compute median (default 60 min)
            window_size: Number of price ticks to keep in rolling buffer
        """
        self.lookback_minutes = lookback_minutes
        self.window_size = window_size
        self.spread_history: deque = deque(maxlen=window_size)  # (timestamp, spread_pips)
        
    def record(self, spread_pips: float, timestamp: Optional[datetime] = None):
        """Record current spread observation (in pips)."""
        ts = timestamp or datetime.utcnow()
        self.spread_history.append((ts, float(spread_pips)))
    
    def get_normal_spread(self) -> Optional[float]:
        """Compute median spread over recent window (usually normal conditions)."""
        if len(self.spread_history) < 20:
            return None
        spreads = [s for _, s in self.spread_history]
        return float(np.median(spreads))
    
    def check_spread(self, current_spread: float) -> Tuple[bool, Optional[str]]:
        """Check if current spread is acceptable.
        
        Returns:
            (allow_trading: bool, rejection_reason: Optional[str])
        """
        normal = self.get_normal_spread()
        
        if normal is None:
            # Not enough history, allow with warning
            return True, None
        
        # Halt condition: spread > 3x normal (market crisis)
        if current_spread > normal * 3:
            return False, f"SPREAD_HALT_{current_spread:.1f}pips_vs_{normal:.1f}normal"
        
        # Skip condition: spread > 2x normal (liquidity squeeze)
        if current_spread > normal * 2:
            return False, f"SPREAD_SPIKE_{current_spread:.1f}pips_vs_{normal:.1f}normal"
        
        return True, None


class ChopDetector:
    """Detects consolidation/chop regimes where only noise exists.
    
    Rule: If range over last 20 candles < 0.6 × ATR(14),
    we're in compression zone. Reject entries.
    """
    
    def __init__(self, lookback_bars: int = 20, atr_ratio_threshold: float = 0.6):
        """
        Args:
            lookback_bars: Window for range calculation (default 20 = ~1 hour on 1m)
            atr_ratio_threshold: If range < atr * threshold, it's chop
        """
        self.lookback_bars = lookback_bars
        self.atr_ratio_threshold = atr_ratio_threshold
    
    def is_chop(
        self,
        high_range: float,
        low_range: float,
        atr_current: float
    ) -> Tuple[bool, Optional[str]]:
        """Check if market is in chop compression.
        
        Args:
            high_range: MAX(High) over last N candles
            low_range: MIN(Low) over last N candles
            atr_current: Current ATR(14) value
        
        Returns:
            (is_chop: bool, diagnostic: Optional[str])
        """
        if atr_current <= 0:
            return False, None
        
        range_size = high_range - low_range
        threshold = atr_current * self.atr_ratio_threshold
        
        if range_size < threshold:
            return True, f"CHOP_{range_size:.2f}_range_vs_{threshold:.2f}_threshold"
        
        return False, None


class SessionRegimeDetector:
    """Identifies which market session we're in and its typical volatility profile.
    
    XAUUSD sessions (SAST timezone):
    - ASIA (00:00-06:59): Low volatility, range-bound
    - LONDON (07:00-11:59): Expansion, breakouts favor
    - LONDON_MID (12:00-14:00): Peak liquidity
    - NY_OPEN (14:00-15:30): Reversal zone (London fade)
    - LONDON_CLOSE (15:30-17:30): Second expansion or chop
    - NY (17:30-23:59): Variable
    """
    
    # Session definitions (SAST: UTC+2)
    SESSIONS = {
        "ASIA": (0, 6),
        "LONDON_OPEN": (7, 9),
        "LONDON_MID": (12, 14),
        "NY_OPEN": (14, 15),  # Tricky zone - fades common
        "LONDON_CLOSE": (15, 17),
        "NY": (17, 23),
    }
    
    # Expected ATR ranges (rough, for XAUUSD)
    # Volatility profiles by session
    EXPECTED_ATR = {
        "ASIA": (10, 20),  # Low
        "LONDON_OPEN": (25, 40),  # Medium-High
        "LONDON_MID": (30, 50),  # High
        "NY_OPEN": (20, 35),  # Medium (choppy)
        "LONDON_CLOSE": (20, 40),  # Medium
        "NY": (15, 30),  # Low-Medium
    }
    
    def __init__(self, timezone: str = "Africa/Johannesburg"):
        import pytz
        self.tz = pytz.timezone(timezone)
    
    def current_session(self, dt: Optional[datetime] = None) -> str:
        """Identify which session we're in."""
        if dt is None:
            import pytz
            dt = datetime.now(pytz.UTC).astimezone(self.tz)
        else:
            dt = dt.astimezone(self.tz) if dt.tzinfo else self.tz.localize(dt)
        
        hour = dt.hour
        
        for session_name, (start_hour, end_hour) in self.SESSIONS.items():
            if start_hour <= hour <= end_hour:
                return session_name
        
        return "UNKNOWN"
    
    def is_high_risk_session(self, session: Optional[str] = None) -> Tuple[bool, str]:
        """Check if current session is known for chop/reversals (NY_OPEN, late ASIA).
        
        Returns:
            (is_risky: bool, reason: str)
        """
        session = session or self.current_session()
        
        # Sessions with known false breakouts or choppy behavior
        risky = {
            "NY_OPEN": "NY Open (14:00-15:30) — London fade zone, reversals common",
            "ASIA": "Asia (00:00-06:59) — Low liquidity, range-bound noise",
        }
        
        if session in risky:
            return True, risky[session]
        
        return False, ""
    
    def expected_atr_range(self, session: Optional[str] = None) -> Tuple[float, float]:
        """Get typical ATR range for this session.
        
        Returns:
            (min_atr, max_atr)
        """
        session = session or self.current_session()
        return self.EXPECTED_ATR.get(session, (15, 30))


class MicrostructureGate:
    """Master gate that combines spread, chop, session into one verdict.
    
    Used by strategies to decide: "Is this actually a good time to trade?"
    """
    
    def __init__(self, symbol: str = "XAUUSD"):
        self.symbol = symbol
        self.spread_analyzer = SpreadAnalyzer()
        self.chop_detector = ChopDetector()
        self.session_detector = SessionRegimeDetector()
    
    def record_spread(self, spread_pips: float, timestamp: Optional[datetime] = None):
        """Record a spread observation for later analysis."""
        self.spread_analyzer.record(spread_pips, timestamp)
    
    def evaluate(
        self,
        current_spread: float,
        high_range: float,
        low_range: float,
        atr_current: float,
        timestamp: Optional[datetime] = None,
        strict: bool = False,  # If True, also check session risk
    ) -> Tuple[bool, Optional[str]]:
        """Comprehensive microstructure check.
        
        Returns:
            (ok_to_trade: bool, rejection_reason: Optional[str])
        """
        # Check spread
        spread_ok, spread_reason = self.spread_analyzer.check_spread(current_spread)
        if not spread_ok:
            return False, spread_reason
        
        # Check chop
        is_chop, chop_reason = self.chop_detector.is_chop(high_range, low_range, atr_current)
        if is_chop:
            return False, chop_reason
        
        # Optionally check session risk (for HIGH-tier signals only)
        if strict:
            is_risky, risk_reason = self.session_detector.is_high_risk_session()
            if is_risky:
                return False, f"HIGH_RISK_SESSION_{risk_reason}"
        
        return True, None
