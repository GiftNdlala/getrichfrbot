# SWING_HIGH Session & Time Filtering Configuration

## Overview
The SWING_HIGH strategy (HIGH level signals from ICT Swing Points) has been optimized for profitability with strict time-based session filters applied to **HIGH confidence signals only**.

## Trading Windows (SAST Timezone)

### Primary Active Trading Windows ✅
These are the primary windows where HIGH signals are **actively traded**:

1. **London Mid (13:00 Zone): 12:00 - 14:00 SAST**
   - Highly profitable pocket around 13:00
   - Best for consistent scalping and swing entries
   - Status: **ACCEPT ALL HIGH SIGNALS**

2. **London Close (15:30 & 17:00 Pockets): 15:30 - 17:30 SAST**
   - Strong liquidity pockets at 15:30 and 17:00
   - High win rate for reversal signals
   - Status: **ACCEPT ALL HIGH SIGNALS**

### NY Open Window (Conditional): 14:00 - 15:30 SAST ⚠️
This window sits between the two main profitable zones:

- Status: **REQUIRES EXTRA CONFIRMATION**
- Requirement: **Confidence >= 80%** (HTF bias or higher conviction signals only)
- Low confidence signals: **BLOCKED** (down-weighted)
- Rationale: Historically lower quality trades; requires higher bar for entry

### Outside Hours ❌
All times outside the windows above:
- Status: **BLOCKED FOR HIGH SIGNALS**
- Reason: Low profitability, excessive noise
- Note: LOW and MEDIUM signals are not time-filtered and can trade anytime

## Signal Filtering Logic

```
IF signal is HIGH confidence (confidence >= 60):
  IF current_time in [12:00-14:00] OR [15:30-17:30]:
    ✅ ACCEPT signal
    Tag: [ACTIVE_WINDOW]
  
  ELSE IF current_time in [14:00-15:30]:
    IF signal.confidence >= 80:
      ✅ ACCEPT signal
      Tag: [NY_OPEN_CONFIRMED]
    ELSE:
      ❌ REJECT signal
      Tag: [NY_OPEN_BLOCKED_LOW_CONF]
  
  ELSE:
    ❌ REJECT signal
    Tag: [OUTSIDE_TRADING_HOURS]

ELSE:
  ✅ ACCEPT signal (LOW/MEDIUM not filtered)
```

## Implementation Details

### Files Modified
- `src/strategies/ict_swing_points.py`

### New Methods Added
- `_is_active_trading_time(current_local)`: Check if time is in primary profitable windows
- `_is_ny_open_time(current_local)`: Check if time is in NY Open confirmation window

### Filter Classification
- **HIGH signals** (confidence >= 60): Strict time filtering applied
- **MEDIUM signals**: No time filtering
- **LOW signals**: No time filtering

## Rationale

Based on backtest analysis:
- 12:00-14:00: London mid-session provides strong trending and mean-reversion opportunities
- 15:30-17:30: London close liquidity creates defined reversal pockets
- 14:00-15:30: Transition period with lower quality signals (requires 80+ confidence)
- Outside hours: Insufficient liquidity, wide spreads, choppy price action

## Configuration Parameters

```python
ACTIVE_TRADING_WINDOWS = [
    (time(12, 0), time(14, 0)),   # London mid
    (time(15, 30), time(17, 30)),  # London close
]

NY_OPEN_CONFIRMATION_WINDOW = (time(14, 0), time(15, 30))

MIN_CONFIDENCE_FOR_NY_OPEN = 80.0  # Percentage (0-100)
HIGH_SIGNAL_CONFIDENCE_THRESHOLD = 60.0  # Confidence level that identifies HIGH signals
```

## Testing & Validation

To validate the new configuration:

1. **Run backtest** with the new time filters
2. **Monitor live signals** during active windows only
3. **Check diagnostic output** for filter status:
   - `[ACTIVE_WINDOW]` - Signal accepted in prime time
   - `[NY_OPEN_CONFIRMED]` - High confidence NY Open signal accepted
   - `[NY_OPEN_BLOCKED_LOW_CONF]` - NY Open signal rejected (low confidence)
   - `[OUTSIDE_TRADING_HOURS]` - Signal rejected (outside windows)

## Key Metrics to Track

- **Win Rate** during active windows vs. outside
- **Average Profit Per Trade** by window
- **Drawdown** comparison between periods
- **Signal Frequency** reduction (should filter 40-50% of HIGH signals)

## Future Adjustments

If profitability changes, consider adjusting:
- Window start/end times (±30 minutes)
- NY Open confidence threshold (currently 80%)
- High signal confidence floor (currently 60%)
- Add additional market condition filters (e.g., volatility, trend confirmation)
