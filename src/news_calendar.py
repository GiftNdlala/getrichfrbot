"""
Live News Calendar Module

Hardcoded Tier-1 economic events for USD/Gold.
Used to enforce blackout periods before/after high-impact releases.

For production, integrate with: Forex Factory, TradingView, or Investing.com APIs
"""

from datetime import datetime, timedelta, time
from typing import List, Optional, Tuple
from dataclasses import dataclass
import pytz


@dataclass
class NewsEvent:
    """Represents a single economic calendar event."""
    name: str
    timestamp: datetime  # UTC
    currency: str  # "USD", "AU", etc.
    impact: str  # "HIGH", "MEDIUM", "LOW"
    
    def __str__(self):
        return f"{self.name} @ {self.timestamp.isoformat()}"


class NewsCalendar:
    """Maintains a list of high-impact events.
    
    Should be updated daily (ideally via API, for now hardcoded).
    
    Focus: Tier-1 USD events that move XAUUSD >50 pips.
    """
    
    # Tier-1 USD economic events that reliably move gold
    TIER_1_EVENTS = [
        "NFP",           # Non-Farm Payroll (first Friday of month)
        "CPI",           # Consumer Price Index
        "Core CPI",      # Without food/energy
        "PPI",           # Producer Price Index
        "Core PPI",      # ProducerPrice ex-food/energy
        "PCE",           # Personal Consumption Expenditure
        "Core PCE",      # PCE ex-food/energy
        "FOMC",          # Fed decision
        "ISM",           # Manufacturing PMI
        "ADP",           # ADP Employment
        "Jobless Claims", # Weekly unemployment
        "Durables",      # Durable Goods Orders
        "Retail Sales",  # Retail spending
    ]
    
    def __init__(self):
        self.events: List[NewsEvent] = []
        self.pre_buffer_minutes = 30   # Don't enter 30 min before
        self.post_buffer_minutes = 15  # Don't enter 15 min after
    
    def add_events_from_data(self, events_data: List[dict]):
        """Ingest events from JSON/CSV calendar data.
        
        Expected format per event:
        {
            "name": "NFP",
            "timestamp": "2025-02-07T13:30:00Z",
            "currency": "USD",
            "impact": "HIGH"
        }
        """
        for evt in events_data:
            try:
                ts = datetime.fromisoformat(evt['timestamp'].replace('Z', '+00:00'))
                self.events.append(NewsEvent(
                    name=evt['name'],
                    timestamp=ts,
                    currency=evt.get('currency', 'USD'),
                    impact=evt.get('impact', 'MEDIUM')
                ))
            except Exception as e:
                print(f"⚠️ Failed to parse event {evt}: {e}")
    
    def is_blackout(
        self,
        now: Optional[datetime] = None,
        pre_minutes: int = 30,
        post_minutes: int = 15
    ) -> Tuple[bool, Optional[str]]:
        """Check if we're in a news blackout window.
        
        Args:
            now: Current time (default: UTC now)
            pre_minutes: How long before event to blackout (default 30)
            post_minutes: How long after event to blackout (default 15)
        
        Returns:
            (is_blackout: bool, event_name: Optional[str])
        """
        if now is None:
            now = datetime.now(pytz.UTC)
        elif now.tzinfo is None:
            now = pytz.UTC.localize(now)
        
        for evt in self.events:
            # Ensure event time is UTC
            evt_time = evt.timestamp
            if evt_time.tzinfo is None:
                evt_time = pytz.UTC.localize(evt_time)
            
            delta_minutes = (now - evt_time).total_seconds() / 60
            
            # Within pre-buffer: approaching event
            if 0 <= delta_minutes <= pre_minutes:
                return True, f"{evt.name}_APPROACHING"
            
            # Within post-buffer: event just released
            if -post_minutes <= delta_minutes < 0:
                return True, f"{evt.name}_RELEASED"
        
        return False, None
    
    def next_event(self, now: Optional[datetime] = None) -> Optional[NewsEvent]:
        """Get the next upcoming Tier-1 event.
        
        Useful for logging/alerts.
        """
        if now is None:
            now = datetime.now(pytz.UTC)
        elif now.tzinfo is None:
            now = pytz.UTC.localize(now)
        
        upcoming = [e for e in self.events if e.timestamp > now]
        
        if upcoming:
            return min(upcoming, key=lambda e: e.timestamp)
        
        return None
    
    def events_today(self, now: Optional[datetime] = None) -> List[NewsEvent]:
        """Get all Tier-1 events happening today (in event's local time).
        
        Returns events sorted by time.
        """
        if now is None:
            now = datetime.now(pytz.UTC)
        elif now.tzinfo is None:
            now = pytz.UTC.localize(now)
        
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        today_events = [
            e for e in self.events
            if today_start <= e.timestamp < today_end
        ]
        
        return sorted(today_events, key=lambda e: e.timestamp)


class NewsGate:
    """Master blackout gate for trading decisions.
    
    Single responsibility: "Can we trade right now, or is news imminent?"
    """
    
    def __init__(self, calendar: Optional[NewsCalendar] = None):
        self.calendar = calendar or NewsCalendar()
        self.enabled = True  # Can be disabled to ignore news
    
    def can_trade(
        self,
        now: Optional[datetime] = None,
        high_tier_only: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """Check if it's safe to enter a trade right now.
        
        Args:
            now: Current time (UTC)
            high_tier_only: If True, enforce stricter blackout for HIGH signals
        
        Returns:
            (can_enter: bool, blackout_reason: Optional[str])
        """
        if not self.enabled:
            return True, None
        
        # Check if in blackout window
        in_blackout, reason = self.calendar.is_blackout(now)
        
        if in_blackout:
            return False, reason
        
        # For strict mode (HIGH-tier), also avoid risky windows
        # e.g., don't enter 60 min before FOMC if high_tier_only
        if high_tier_only:
            # Could add additional stricter checking here
            pass
        
        return True, None
    
    def update_calendar(self, events_data: List[dict]):
        """Update calendar with new events (call daily)."""
        self.calendar.add_events_from_data(events_data)


# ============================================================================
# HARDCODED FEBRUARY 2025 EVENTS (for testing / minimal live scenario)
# ============================================================================

def get_default_calendar() -> NewsCalendar:
    """Return a calendar with common Tier-1 USD events.
    
    In production, fetch these from Forex Factory API daily.
    For now, hardcoded for testing.
    """
    cal = NewsCalendar()
    
    # Example: Feb 2025 (dummy times — adjust to real)
    # NFP typically: First Friday @ 13:30 UTC
    # CPI typically: Mid-month, Wednesday @ 13:30 UTC
    # FOMC typically: 8 times/year
    
    events = [
        # February 2025
        {
            "name": "CPI",
            "timestamp": "2025-02-12T13:30:00Z",
            "currency": "USD",
            "impact": "HIGH"
        },
        {
            "name": "NFP",
            "timestamp": "2025-02-07T13:30:00Z",
            "currency": "USD",
            "impact": "HIGH"
        },
        {
            "name": "ADP",
            "timestamp": "2025-02-05T13:15:00Z",
            "currency": "USD",
            "impact": "MEDIUM"
        },
        {
            "name": "Core PCE",
            "timestamp": "2025-02-28T14:00:00Z",
            "currency": "USD",
            "impact": "HIGH"
        },
    ]
    
    cal.add_events_from_data(events)
    return cal
