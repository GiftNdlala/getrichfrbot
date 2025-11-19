"""ICT Swing Points strategy implementation for XAUUSD.

This module engineers the session-based swing logic as described in the
original Inner Circle Trader (ICT) mentorship transcripts surrounding the
"Trading The Key Swing Points" lesson. The implementation focuses on the
relationship between the Asian open, London open, New York open, and London
close to frame daily range formation and the associated optimal trade entries
that arise from session-based liquidity runs and retracements.

Key characteristics captured directly from the transcript guidance:

* Asian session (consolidation) often sets the initial high/low of the day.
* London open can either extend the initial move or provide a retracement into
  optimal trade entry (OTE) after Asia has created the day?s extreme.
* New York open can mirror London?s role ? either engineering the daily high/low
  or providing the retracement following the London impulse leg.
* London close frequently completes the opposite end of the range or acts as a
  larger-scale turning point when aligned with higher timeframe levels.

The strategy monitors these session interactions in real-time and produces
structured trade signals when price returns into the 62%?79% OTE window after a
stop run / expansion has already been confirmed. Only XAUUSD is supported.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import pytz


@dataclass
class ICTSwingSignal:
    """Structured output for an ICT Swing Points trade idea."""

    timestamp: datetime
    symbol: str
    session: str  # "LONDON", "NEW_YORK", "LONDON_CLOSE"
    scenario: str  # descriptive scenario label
    direction: int  # 1 = long, -1 = short
    entry_price: float
    stop_loss: float
    take_profit_primary: float
    take_profit_secondary: Optional[float] = None
    take_profit_tertiary: Optional[float] = None
    confidence: float = 0.0
    risk_reward: float = 0.0
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "session": self.session,
            "scenario": self.scenario,
            "direction": self.direction,
            "entry_price": float(self.entry_price),
            "stop_loss": float(self.stop_loss),
            "take_profit_primary": float(self.take_profit_primary),
            "take_profit_secondary": float(self.take_profit_secondary)
            if self.take_profit_secondary is not None
            else None,
            "take_profit_tertiary": float(self.take_profit_tertiary)
            if self.take_profit_tertiary is not None
            else None,
            "confidence": float(self.confidence),
            "risk_reward": float(self.risk_reward),
            "notes": self.notes,
            "metadata": dict(self.metadata),
        }


class ICTSwingPointsStrategy:
    """Implements ICT Swing Points session logic for XAUUSD."""

    # Trading sessions - all sessions defined for reference
    SESSIONS: Dict[str, Tuple[time, time]] = {
        "ASIA": (time(0, 0), time(6, 59)),
        "LONDON": (time(7, 0), time(11, 59)),
        "NEW_YORK": (time(12, 0), time(15, 59)),
        "LONDON_CLOSE": (time(15, 30), time(17, 30)),
    }
    
    # Active trading windows for HIGH signal profitability (SAST timezone)
    # Based on backtest results: 12:00-14:00 and 15:30-17:30 show best performance
    ACTIVE_TRADING_WINDOWS = [
        (time(12, 0), time(14, 0)),   # London mid (13:00 profitable zone)
        (time(15, 30), time(17, 30)),  # London close (15:30 & 17:00 pockets)
    ]
    
    # NY Open window (14:00-15:30) requires extra confirmation for HIGH signals
    NY_OPEN_CONFIRMATION_WINDOW = (time(14, 0), time(15, 30))

    def __init__(
        self,
        symbol: str = "XAUUSD",
        timezone: str = "UTC",
        ote_range: Tuple[float, float] = (0.62, 0.79),
        min_break_pct: float = 0.0015,
    ) -> None:
        self.symbol = symbol.upper()
        self.timezone = pytz.timezone(timezone)
        self.ote_range = ote_range
        self.min_break_pct = min_break_pct
        self._last_diagnostics: Dict[str, Any] = {
            "status": "init",
            "reason": None,
            "summary": {},
            "signals": [],
        }

    def _is_active_trading_time(self, current_local: pd.Timestamp) -> bool:
        """Check if current time falls within high-probability trading windows (12:00-14:00 and 15:30-17:30 SAST)."""
        current_time = current_local.time()
        for start, end in self.ACTIVE_TRADING_WINDOWS:
            if start <= current_time <= end:
                return True
        return False
    
    def _is_ny_open_time(self, current_local: pd.Timestamp) -> bool:
        """Check if current time is in NY Open window (14:00-15:30) that requires extra confirmation."""
        current_time = current_local.time()
        start, end = self.NY_OPEN_CONFIRMATION_WINDOW
        return start <= current_time <= end

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def evaluate(
        self,
        historical_data: pd.DataFrame,
        current_quote: Dict[str, Any],
    ) -> Tuple[List[ICTSwingSignal], Dict[str, Any]]:
        """Evaluate current context and emit zero or more swing signals."""

        diagnostics: Dict[str, Any] = {
            "status": "init",
            "reason": None,
            "summary": {},
            "signals": [],
        }

        signals: List[ICTSwingSignal] = []

        # Support any gold symbol (XAUUSD, XAUUSDm, GOLD, etc.)
        symbol_upper = (self.symbol or "").upper()
        is_gold = ("XAU" in symbol_upper) or ("GOLD" in symbol_upper)
        if not is_gold:
            diagnostics.update({"status": "skipped", "reason": "unsupported_symbol"})
            self._last_diagnostics = diagnostics
            return signals, diagnostics

        if historical_data is None or historical_data.empty:
            diagnostics.update({"status": "skipped", "reason": "missing_history"})
            self._last_diagnostics = diagnostics
            return signals, diagnostics

        base_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in historical_data.columns]
        if len(base_cols) < 4:
            diagnostics.update({"status": "skipped", "reason": "missing_columns"})
            self._last_diagnostics = diagnostics
            return signals, diagnostics

        data = historical_data[base_cols].copy().dropna()
        if data.empty or len(data) < 720:
            diagnostics.update({"status": "skipped", "reason": "insufficient_history"})
            self._last_diagnostics = diagnostics
            return signals, diagnostics

        # Ensure timezone awareness for session slicing
        data = self._localize_index(data)

        current_ts = pd.Timestamp(current_quote.get("timestamp", datetime.utcnow()))
        if current_ts.tzinfo is None:
            current_ts = current_ts.tz_localize("UTC")
        current_local = current_ts.tz_convert(self.timezone)

        today_slice = data[(data.index.date == current_local.date()) & (data.index <= current_local)]
        if today_slice.empty:
            diagnostics.update({"status": "skipped", "reason": "no_intraday_data"})
            self._last_diagnostics = diagnostics
            return signals, diagnostics

        sessions = self._extract_sessions(today_slice)

        summary = self._build_summary(today_slice, sessions, current_local, current_quote)
        diagnostics["summary"] = summary

        # Attempt to engineer signals based on the transcript-driven playbook
        session_signals: List[ICTSwingSignal] = []
        session_signals.extend(
            self._london_open_setups(sessions, today_slice, current_local, current_quote)
        )
        session_signals.extend(
            self._new_york_open_setups(sessions, today_slice, current_local, current_quote)
        )
        session_signals.extend(
            self._london_close_setups(sessions, today_slice, current_local, current_quote)
        )

        # Apply time/session filters to HIGH level signals
        # Only trade HIGH signals during active windows: 12:00-14:00 and 15:30-17:30 SAST
        # NY Open (14:00-15:30) requires confidence >= 80 for HIGH signals
        filtered_signals: List[ICTSwingSignal] = []
        for sig in session_signals:
            # Check if this is a HIGH confidence signal (assumed by 0-100 scale in _build_signal)
            is_high_signal = sig.confidence >= 60.0  # HIGH level signals typically have confidence > 60
            
            if is_high_signal:
                # HIGH level signal - apply strict time filtering
                if self._is_active_trading_time(current_local):
                    # Active trading window - accept signal
                    filtered_signals.append(sig)
                    sig.notes += " [ACTIVE_WINDOW]" if "[" not in sig.notes else ""
                elif self._is_ny_open_time(current_local):
                    # NY Open window - only accept if confidence >= 80 (requires HTF confirmation)
                    if sig.confidence >= 80.0:
                        filtered_signals.append(sig)
                        sig.notes += " [NY_OPEN_CONFIRMED]" if "[" not in sig.notes else ""
                    else:
                        sig.notes += " [NY_OPEN_BLOCKED_LOW_CONF]" if "[" not in sig.notes else ""
                else:
                    # Outside trading windows - reject HIGH signals
                    sig.notes += " [OUTSIDE_TRADING_HOURS]" if "[" not in sig.notes else ""
            else:
                # LOW/MEDIUM signals - pass through without time filtering
                filtered_signals.append(sig)

        if filtered_signals:
            diagnostics.update({
                "status": "signal",
                "reason": "session_pattern_matched",
                "signals": [sig.to_payload() for sig in filtered_signals],
            })
            signals.extend(filtered_signals)
        else:
            reason = "no_session_alignment"
            if session_signals and all(s.confidence >= 60.0 for s in session_signals):
                reason = "outside_active_trading_hours"
            diagnostics.update({
                "status": "hold",
                "reason": reason,
                "signals": [],
            })

        self._last_diagnostics = diagnostics
        return signals, diagnostics

    def get_last_diagnostics(self) -> Dict[str, Any]:
        return dict(self._last_diagnostics)

    # ------------------------------------------------------------------
    # Session helpers
    # ------------------------------------------------------------------
    def _localize_index(self, df: pd.DataFrame) -> pd.DataFrame:
        localized = df.copy()
        idx = pd.DatetimeIndex(localized.index)
        if idx.tz is None:
            idx = idx.tz_localize("UTC")
        localized.index = idx.tz_convert(self.timezone)
        return localized

    def _extract_sessions(self, today_slice: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        sessions: Dict[str, pd.DataFrame] = {}
        for name, (start, end) in self.SESSIONS.items():
            try:
                session_df = today_slice.between_time(start_time=start, end_time=end, inclusive="both")
            except TypeError:
                # pandas < 1.4 compatibility (inclusive keyword added later)
                session_df = today_slice.between_time(start_time=start, end_time=end)
            sessions[name] = session_df
        return sessions

    def _build_summary(
        self,
        today_slice: pd.DataFrame,
        sessions: Dict[str, pd.DataFrame],
        current_local: pd.Timestamp,
        current_quote: Dict[str, Any],
    ) -> Dict[str, Any]:
        current_price = float(current_quote.get("price") or today_slice.iloc[-1]["Close"])
        day_high = float(today_slice["High"].max())
        day_low = float(today_slice["Low"].min())
        day_range = max(day_high - day_low, 1e-6)
        position_pct = (current_price - day_low) / day_range if day_range else 0.0

        summary = {
            "timestamp": current_local.isoformat(),
            "current_price": current_price,
            "day_high": day_high,
            "day_low": day_low,
            "day_range": day_range,
            "range_position_pct": round(position_pct * 100, 2),
        }

        for session_name, frame in sessions.items():
            if frame is None or frame.empty:
                summary[f"{session_name.lower()}_available"] = False
                continue
            summary[f"{session_name.lower()}_available"] = True
            summary[f"{session_name.lower()}_high"] = float(frame["High"].max())
            summary[f"{session_name.lower()}_low"] = float(frame["Low"].min())
        return summary

    # ------------------------------------------------------------------
    # Session scenario detection (derived from transcript rules)
    # ------------------------------------------------------------------
    def _london_open_setups(
        self,
        sessions: Dict[str, pd.DataFrame],
        today_slice: pd.DataFrame,
        current_local: pd.Timestamp,
        current_quote: Dict[str, Any],
    ) -> List[ICTSwingSignal]:
        if current_local.time() < time(6, 30) or current_local.time() > time(11, 59):
            return []

        asia = sessions.get("ASIA")
        if asia is None or len(asia) < 4:
            return []

        post_asia = today_slice[today_slice.index > asia.index[-1]]
        if post_asia.empty:
            return []

        current_price = float(current_quote.get("price") or today_slice.iloc[-1]["Close"])
        day_low = float(today_slice["Low"].min())
        day_high = float(today_slice["High"].max())
        asia_low = float(asia["Low"].min())
        asia_high = float(asia["High"].max())
        asia_range = max(asia_high - asia_low, 1e-6)

        signals: List[ICTSwingSignal] = []

        # --- Bullish scenario: Asia creates the low, London retraces into OTE ---
        if np.isclose(asia_low, day_low) or asia_low <= day_low + 0.2:
            impulse_high = float(post_asia["High"].max())
            if impulse_high <= asia_high:
                pass
            else:
                break_amt = impulse_high - asia_high
                if break_amt >= max(self.min_break_pct * current_price, 1.0):
                    ote_high = impulse_high
                    ote_ratio = (current_price - asia_low) / max(ote_high - asia_low, 1e-6)
                    if self.ote_range[0] <= ote_ratio <= self.ote_range[1]:
                        signals.append(
                            self._build_signal(
                                session="LONDON",
                                scenario="asia_low_london_retrace_long",
                                direction=1,
                                current_price=current_price,
                                extreme_level=asia_low,
                                impulse_level=impulse_high,
                                reference_high=asia_high,
                                ote_ratio=ote_ratio,
                                today_slice=today_slice,
                                current_local=current_local,
                                notes="Asia low formed the day?s floor; London retraces into OTE for continuation",
                            )
                        )

        # --- Bearish scenario: Asia creates the high, London retraces into OTE ---
        if np.isclose(asia_high, day_high) or asia_high >= day_high - 0.2:
            impulse_low = float(post_asia["Low"].min())
            if impulse_low >= asia_low:
                pass
            else:
                break_amt = asia_low - impulse_low
                if break_amt >= max(self.min_break_pct * current_price, 1.0):
                    ote_low = impulse_low
                    ote_ratio = (asia_high - current_price) / max(asia_high - ote_low, 1e-6)
                    if self.ote_range[0] <= ote_ratio <= self.ote_range[1]:
                        signals.append(
                            self._build_signal(
                                session="LONDON",
                                scenario="asia_high_london_retrace_short",
                                direction=-1,
                                current_price=current_price,
                                extreme_level=asia_high,
                                impulse_level=impulse_low,
                                reference_high=asia_high,
                                ote_ratio=ote_ratio,
                                today_slice=today_slice,
                                current_local=current_local,
                                notes="Asia high engineered liquidity; London retraces into OTE for sell",
                            )
                        )

        return signals

    def _new_york_open_setups(
        self,
        sessions: Dict[str, pd.DataFrame],
        today_slice: pd.DataFrame,
        current_local: pd.Timestamp,
        current_quote: Dict[str, Any],
    ) -> List[ICTSwingSignal]:
        if current_local.time() < time(11, 30) or current_local.time() > time(15, 30):
            return []

        london = sessions.get("LONDON")
        if london is None or len(london) < 4:
            return []

        post_london = today_slice[today_slice.index > london.index[-1]]
        if post_london.empty:
            return []

        current_price = float(current_quote.get("price") or today_slice.iloc[-1]["Close"])
        day_low = float(today_slice["Low"].min())
        day_high = float(today_slice["High"].max())
        london_low = float(london["Low"].min())
        london_high = float(london["High"].max())

        signals: List[ICTSwingSignal] = []

        # --- Bullish scenario: London prints the impulse low, NY retraces ---
        if np.isclose(london_low, day_low) or london_low <= day_low + 0.2:
            impulse_high = float(post_london["High"].max())
            if impulse_high > london_high:
                break_amt = impulse_high - london_high
            else:
                break_amt = impulse_high - london_low
            if break_amt >= max(self.min_break_pct * current_price, 1.0):
                ote_ratio = (current_price - london_low) / max(impulse_high - london_low, 1e-6)
                if self.ote_range[0] <= ote_ratio <= self.ote_range[1]:
                    signals.append(
                        self._build_signal(
                            session="NEW_YORK",
                            scenario="london_low_ny_retrace_long",
                            direction=1,
                            current_price=current_price,
                            extreme_level=london_low,
                            impulse_level=impulse_high,
                            reference_high=london_high,
                            ote_ratio=ote_ratio,
                            today_slice=today_slice,
                            current_local=current_local,
                            notes="London printed the low; NY retraces into continuation OTE",
                        )
                    )

        # --- Bearish scenario: London prints the impulse high, NY retraces ---
        if np.isclose(london_high, day_high) or london_high >= day_high - 0.2:
            impulse_low = float(post_london["Low"].min())
            if impulse_low < london_low:
                break_amt = london_high - impulse_low
            else:
                break_amt = london_high - impulse_low
            if break_amt >= max(self.min_break_pct * current_price, 1.0):
                ote_ratio = (london_high - current_price) / max(london_high - impulse_low, 1e-6)
                if self.ote_range[0] <= ote_ratio <= self.ote_range[1]:
                    signals.append(
                        self._build_signal(
                            session="NEW_YORK",
                            scenario="london_high_ny_retrace_short",
                            direction=-1,
                            current_price=current_price,
                            extreme_level=london_high,
                            impulse_level=impulse_low,
                            reference_high=london_high,
                            ote_ratio=ote_ratio,
                            today_slice=today_slice,
                            current_local=current_local,
                            notes="London ran the high; NY retraces into OTE for sell-side delivery",
                        )
                    )

        return signals

    def _london_close_setups(
        self,
        sessions: Dict[str, pd.DataFrame],
        today_slice: pd.DataFrame,
        current_local: pd.Timestamp,
        current_quote: Dict[str, Any],
    ) -> List[ICTSwingSignal]:
        if current_local.time() < time(15, 15) or current_local.time() > time(18, 0):
            return []

        london_close = sessions.get("LONDON_CLOSE")
        if london_close is None or london_close.empty:
            return []

        current_price = float(current_quote.get("price") or today_slice.iloc[-1]["Close"])
        day_high = float(today_slice["High"].max())
        day_low = float(today_slice["Low"].min())
        day_range = max(day_high - day_low, 1e-6)
        range_position = (current_price - day_low) / day_range if day_range else 0.0

        signals: List[ICTSwingSignal] = []

        # Fade a bullish day into London close extremes
        if range_position >= 0.85:
            signals.append(
                self._build_reversal_signal(
                    session="LONDON_CLOSE",
                    scenario="london_close_top_reversal",
                    direction=-1,
                    current_price=current_price,
                    extreme_level=day_high,
                    range_mid=day_low + day_range * 0.5,
                    range_position=range_position,
                    current_local=current_local,
                    notes="London close aligns with daily high extreme ? fade for reversal",
                )
            )

        # Fade a bearish day into London close extremes
        if range_position <= 0.15:
            signals.append(
                self._build_reversal_signal(
                    session="LONDON_CLOSE",
                    scenario="london_close_bottom_reversal",
                    direction=1,
                    current_price=current_price,
                    extreme_level=day_low,
                    range_mid=day_low + day_range * 0.5,
                    range_position=range_position,
                    current_local=current_local,
                    notes="London close aligns with daily low extreme ? fade for reversal",
                )
            )

        return signals

    # ------------------------------------------------------------------
    # Signal construction helpers
    # ------------------------------------------------------------------
    def _build_signal(
        self,
        session: str,
        scenario: str,
        direction: int,
        current_price: float,
        extreme_level: float,
        impulse_level: float,
        reference_high: float,
        ote_ratio: float,
        today_slice: pd.DataFrame,
        current_local: pd.Timestamp,
        notes: str,
    ) -> ICTSwingSignal:
        risk_buffer = max(0.0008 * current_price, 1.5)
        atr_like = float((today_slice["High"] - today_slice["Low"]).tail(14).mean())
        if np.isnan(atr_like) or atr_like <= 0:
            atr_like = max(0.0015 * current_price, 3.0)

        if direction == 1:
            stop_loss = extreme_level - risk_buffer
            risk = max(current_price - stop_loss, 0.1)
            take_profit_primary = impulse_level + risk * 1.5
            take_profit_secondary = impulse_level + max(risk * 2.0, atr_like * 0.5)
            take_profit_tertiary = impulse_level + max(risk * 2.5, atr_like)
        else:
            stop_loss = extreme_level + risk_buffer
            risk = max(stop_loss - current_price, 0.1)
            take_profit_primary = impulse_level - risk * 1.5
            take_profit_secondary = impulse_level - max(risk * 2.0, atr_like * 0.5)
            take_profit_tertiary = impulse_level - max(risk * 2.5, atr_like)

        risk_reward = abs((take_profit_primary - current_price) / risk) if risk else 0.0

        ote_mid = sum(self.ote_range) / 2.0
        confidence = max(0.0, 100.0 - abs(ote_ratio - ote_mid) * 220.0)

        metadata = {
            "ote_ratio": round(ote_ratio, 4),
            "impulse_level": round(float(impulse_level), 2),
            "extreme_level": round(float(extreme_level), 2),
            "atr_like": round(float(atr_like), 2),
            "reference_level": round(float(reference_high), 2),
        }

        return ICTSwingSignal(
            timestamp=current_local.to_pydatetime(),
            symbol=self.symbol,
            session=session,
            scenario=scenario,
            direction=direction,
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profit_primary=take_profit_primary,
            take_profit_secondary=take_profit_secondary,
            take_profit_tertiary=take_profit_tertiary,
            confidence=confidence,
            risk_reward=risk_reward,
            notes=notes,
            metadata=metadata,
        )

    def _build_reversal_signal(
        self,
        session: str,
        scenario: str,
        direction: int,
        current_price: float,
        extreme_level: float,
        range_mid: float,
        range_position: float,
        current_local: pd.Timestamp,
        notes: str,
    ) -> ICTSwingSignal:
        buffer = max(0.0009 * current_price, 2.0)
        range_target = range_mid

        if direction == 1:
            stop_loss = extreme_level - buffer
            risk = max(current_price - stop_loss, 0.1)
            take_profit_primary = current_price + risk * 1.2
            take_profit_secondary = range_target
            take_profit_tertiary = current_price + risk * 2.4
        else:
            stop_loss = extreme_level + buffer
            risk = max(stop_loss - current_price, 0.1)
            take_profit_primary = current_price - risk * 1.2
            take_profit_secondary = range_target
            take_profit_tertiary = current_price - risk * 2.4

        risk_reward = abs((take_profit_primary - current_price) / risk) if risk else 0.0

        # Confidence increases the deeper we are into the extreme (closer to 0 or 1)
        extreme_bias = range_position if direction == -1 else (1 - range_position)
        confidence = max(0.0, min(100.0, 60.0 + extreme_bias * 40.0))

        metadata = {
            "range_position_pct": round(range_position * 100, 2),
            "extreme_level": round(float(extreme_level), 2),
            "range_mid": round(float(range_mid), 2),
        }

        return ICTSwingSignal(
            timestamp=current_local.to_pydatetime(),
            symbol=self.symbol,
            session=session,
            scenario=scenario,
            direction=direction,
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profit_primary=take_profit_primary,
            take_profit_secondary=take_profit_secondary,
            take_profit_tertiary=take_profit_tertiary,
            confidence=confidence,
            risk_reward=risk_reward,
            notes=notes,
            metadata=metadata,
        )

