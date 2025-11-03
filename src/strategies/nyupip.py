"""NYUPIP (Feni4Real) gold strategy implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pytz

from ..indicators import TechnicalIndicators


@dataclass
class NYUPIPSignal:
    """Structured signal output for the NYUPIP strategy."""

    timestamp: datetime
    symbol: str
    module: str  # "1HSMA" or "CIS"
    direction: int  # 1 for long, -1 for short
    entry_price: float
    stop_loss: float
    take_profit_primary: float
    take_profit_secondary: Optional[float] = None
    take_profit_tertiary: Optional[float] = None
    risk_percent: float = 0.01
    risk_reward: float = 0.0
    notes: str = ""
    metadata: Dict[str, float] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, object]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "module": self.module,
            "direction": self.direction,
            "entry_price": round(self.entry_price, 3),
            "stop_loss": round(self.stop_loss, 3),
            "take_profit_primary": round(self.take_profit_primary, 3),
            "take_profit_secondary": round(self.take_profit_secondary, 3) if self.take_profit_secondary else None,
            "take_profit_tertiary": round(self.take_profit_tertiary, 3) if self.take_profit_tertiary else None,
            "risk_percent": self.risk_percent,
            "risk_reward": round(self.risk_reward, 2),
            "notes": self.notes,
            "metadata": self.metadata,
        }


class NYUPIPStrategy:
    """Implements the NYUPIP 1HSMA + CIS trading workflow."""

    def __init__(
        self,
        symbol: str = "XAUUSD",
        risk_percent: float = 0.01,
        max_risk_percent: float = 0.02,
        atr_multiplier: float = 1.1,
        timezone: str = "Africa/Johannesburg",
        cooldown_minutes: int = 30,
        enable_rsi_confirmation: bool = False,
    ) -> None:
        self.symbol = symbol
        self.risk_percent = min(max(risk_percent, 0.0), max_risk_percent)
        self.max_risk_percent = max_risk_percent
        self.atr_multiplier = atr_multiplier
        self.timezone = pytz.timezone(timezone)
        self.cooldown = timedelta(minutes=cooldown_minutes)
        self.enable_rsi_confirmation = enable_rsi_confirmation
        self._indicators = TechnicalIndicators()
        self._last_signal_time: Dict[str, Optional[datetime]] = {"1HSMA": None, "CIS": None}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def evaluate(
        self,
        historical_data: pd.DataFrame,
        current_quote: Dict[str, float],
    ) -> List[NYUPIPSignal]:
        """Return zero or more actionable signals for the current tick."""

        if historical_data is None or historical_data.empty or not current_quote:
            return []

        context = self._build_context(historical_data, current_quote)
        if not context:
            return []

        signals: List[NYUPIPSignal] = []

        try:
            signals.extend(self._evaluate_1hsma(context))
        except Exception as exc:  # pragma: no cover - defensive logging only
            print(f"[NYUPIP] 1HSMA evaluation error: {exc}")

        try:
            signals.extend(self._evaluate_cis(context))
        except Exception as exc:  # pragma: no cover - defensive logging only
            print(f"[NYUPIP] CIS evaluation error: {exc}")

        return signals

    # ------------------------------------------------------------------
    # Context preparation helpers
    # ------------------------------------------------------------------
    def _build_context(
        self, historical_data: pd.DataFrame, current_quote: Dict[str, float]
    ) -> Optional[Dict[str, object]]:
        data = historical_data.copy()
        data = data.sort_index()
        try:
            data.index = pd.DatetimeIndex(data.index).tz_localize(None)
        except (AttributeError, TypeError):
            data.index = pd.to_datetime(data.index)

        current_ts_raw = pd.Timestamp(current_quote.get("timestamp", datetime.utcnow()))
        if current_ts_raw.tzinfo is None:
            current_ts_raw = current_ts_raw.tz_localize("UTC")
        current_ts_sast = current_ts_raw.tz_convert(self.timezone)
        current_ts = current_ts_sast.tz_localize(None)

        h1 = self._resample_ohlc(data, "1H")
        m15 = self._resample_ohlc(data, "15T")

        if h1 is None or m15 is None or len(h1) < 80 or len(m15) < 40:
            return None

        h1 = self._indicators.add_sma(h1, periods=[50])
        h1 = self._indicators.add_atr(h1, period=14)
        m15 = self._indicators.add_rsi(m15, period=14)

        current_price = float(current_quote.get("price") or h1.iloc[-1]["Close"])
        atr_series = h1.get("ATR_14")
        atr_current = float(atr_series.iloc[-1]) if isinstance(atr_series, pd.Series) else np.nan
        atr_avg = float(atr_series.tail(14).mean()) if isinstance(atr_series, pd.Series) else np.nan

        sma_series = h1.get("SMA_50")
        sma_current = float(sma_series.iloc[-1]) if isinstance(sma_series, pd.Series) else np.nan
        sma_prev = float(sma_series.iloc[-4]) if isinstance(sma_series, pd.Series) and len(sma_series) >= 4 else np.nan

        trend_bias = None
        if not np.isnan(sma_current) and not np.isnan(sma_prev):
            if current_price > sma_current and sma_current >= sma_prev:
                trend_bias = "LONG"
            elif current_price < sma_current and sma_current <= sma_prev:
                trend_bias = "SHORT"

        zone_distance = abs(current_price - sma_current) if not np.isnan(sma_current) else np.nan
        zone_threshold = np.nan
        if not np.isnan(atr_current):
            zone_threshold = max(atr_current * 0.35, current_price * 0.0015)
        elif current_price:
            zone_threshold = current_price * 0.0015

        zone_valid = (
            not np.isnan(zone_distance)
            and not np.isnan(zone_threshold)
            and zone_distance <= zone_threshold
        )

        trendline_valid = self._validate_trendline(h1, trend_bias)

        atr_valid = False
        if not np.isnan(atr_current) and not np.isnan(atr_avg) and atr_avg > 0:
            atr_valid = atr_current >= atr_avg * self.atr_multiplier

        m15_closed = m15[m15.index <= current_ts.floor("15T")]
        if len(m15_closed) >= 2 and m15_closed.index[-1] == current_ts.floor("15T"):
            # Remove potentially forming bar
            m15_closed = m15_closed.iloc[:-1]

        m15_sast = self._convert_to_timezone(m15, self.timezone)

        return {
            "timestamp": current_ts,
            "timestamp_tz": current_ts_sast,
            "current_price": current_price,
            "h1": h1,
            "m15": m15,
            "m15_closed": m15_closed,
            "m15_sast": m15_sast,
            "atr_current": atr_current,
            "atr_avg": atr_avg,
            "atr_valid": atr_valid,
            "sma_current": sma_current,
            "trend_bias": trend_bias,
            "zone_valid": zone_valid,
            "zone_distance": zone_distance,
            "zone_threshold": zone_threshold,
            "trendline_valid": trendline_valid,
        }

    @staticmethod
    def _resample_ohlc(data: pd.DataFrame, rule: str) -> Optional[pd.DataFrame]:
        if data.empty:
            return None
        try:
            agg = data.resample(rule, label="right", closed="right").agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            })
            agg = agg.dropna(how="any")
            return agg
        except Exception:
            return None

    def _convert_to_timezone(self, df: pd.DataFrame, tz: pytz.timezone) -> pd.DataFrame:
        converted = df.copy()
        idx = pd.DatetimeIndex(converted.index)
        if idx.tz is None:
            idx = idx.tz_localize("UTC")
        converted.index = idx.tz_convert(tz)
        return converted

    @staticmethod
    def _validate_trendline(h1: pd.DataFrame, bias: Optional[str]) -> bool:
        if bias not in {"LONG", "SHORT"} or len(h1) < 5:
            return False if bias else True
        try:
            if bias == "LONG":
                lows = h1["Low"].iloc[-5:]
                return bool(np.all(np.diff(lows) >= 0))
            highs = h1["High"].iloc[-5:]
            return bool(np.all(np.diff(highs) <= 0))
        except Exception:
            return True

    # ------------------------------------------------------------------
    # Strategy modules
    # ------------------------------------------------------------------
    def _evaluate_1hsma(self, ctx: Dict[str, object]) -> List[NYUPIPSignal]:
        if ctx.get("trend_bias") not in {"LONG", "SHORT"}:
            return []
        if not ctx.get("zone_valid") or not ctx.get("trendline_valid"):
            return []
        if not ctx.get("atr_valid"):
            return []

        m15_closed: pd.DataFrame = ctx["m15_closed"]  # type: ignore[assignment]
        if m15_closed is None or len(m15_closed) < 5:
            return []

        pattern = self._detect_price_action(m15_closed, ctx["trend_bias"] == "LONG")
        if not pattern:
            return []

        if self.enable_rsi_confirmation:
            rsi_series = m15_closed.get("RSI_14")
            if isinstance(rsi_series, pd.Series):
                rsi_value = float(rsi_series.iloc[-1])
                if ctx["trend_bias"] == "LONG" and rsi_value < 50:
                    return []
                if ctx["trend_bias"] == "SHORT" and rsi_value > 50:
                    return []

        current_price = float(ctx["current_price"])  # type: ignore[assignment]
        atr_current = float(ctx.get("atr_current") or 0)
        h1: pd.DataFrame = ctx["h1"]  # type: ignore[assignment]
        direction = 1 if ctx["trend_bias"] == "LONG" else -1

        if direction == 1:
            swing_low = float(m15_closed["Low"].iloc[-5:-1].min())
            stop_loss = swing_low - (atr_current * 0.2 if atr_current else 0.5)
            prev_high = float(h1["High"].iloc[-6:-1].max())
            risk = max(current_price - stop_loss, 0.1)
            tp_rr = current_price + risk * 2
            take_profit = max(prev_high, tp_rr)
        else:
            swing_high = float(m15_closed["High"].iloc[-5:-1].max())
            stop_loss = swing_high + (atr_current * 0.2 if atr_current else 0.5)
            prev_low = float(h1["Low"].iloc[-6:-1].min())
            risk = max(stop_loss - current_price, 0.1)
            tp_rr = current_price - risk * 2
            take_profit = min(prev_low, tp_rr)

        if direction == 1 and take_profit <= current_price:
            take_profit = current_price + risk * 2
        if direction == -1 and take_profit >= current_price:
            take_profit = current_price - risk * 2

        if (direction == 1 and stop_loss >= current_price) or (
            direction == -1 and stop_loss <= current_price
        ):
            return []

        risk_reward = abs((take_profit - current_price) / (current_price - stop_loss))
        if risk_reward < 1.5:
            return []

        signal_time = ctx["timestamp"]  # type: ignore[assignment]
        if not self._cooldown_passed("1HSMA", signal_time):
            return []

        metadata = {
            "label_a_distance": round(float(ctx.get("zone_distance") or 0), 3),
            "label_a_threshold": round(float(ctx.get("zone_threshold") or 0), 3),
            "pattern": pattern,
            "atr_current": round(atr_current, 3) if atr_current else None,
            "module": "1HSMA",
        }

        signal = NYUPIPSignal(
            timestamp=signal_time.to_pydatetime(),
            symbol=self.symbol,
            module="1HSMA",
            direction=direction,
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profit_primary=take_profit,
            take_profit_secondary=current_price + (take_profit - current_price) * 1.5 if direction == 1 else current_price - (current_price - take_profit) * 1.5,
            take_profit_tertiary=None,
            risk_percent=self.risk_percent,
            risk_reward=risk_reward,
            notes=f"1HSMA confirmation via {pattern}",
            metadata=metadata,
        )

        self._last_signal_time["1HSMA"] = signal_time
        return [signal]

    def _evaluate_cis(self, ctx: Dict[str, object]) -> List[NYUPIPSignal]:
        if ctx.get("trend_bias") not in {"LONG", "SHORT"}:
            return []
        if not ctx.get("atr_valid"):
            return []

        now_sast: datetime = ctx["timestamp_tz"]  # type: ignore[assignment]
        if now_sast.time() < time(15, 10) or now_sast.time() > time(15, 30):
            return []

        m15_sast: pd.DataFrame = ctx["m15_sast"]  # type: ignore[assignment]
        if m15_sast is None or m15_sast.empty:
            return []

        today_mask = m15_sast.index.date == now_sast.date()
        today_data = m15_sast.loc[today_mask]
        if today_data.empty:
            return []

        c1445 = self._find_candle(today_data, time(14, 45))
        c1515 = self._find_candle(today_data, time(15, 15))
        if c1445 is None or c1515 is None:
            return []

        direction = None
        if c1445["Close"] > c1445["Open"] and ctx["trend_bias"] == "LONG":
            direction = 1
        elif c1445["Close"] < c1445["Open"] and ctx["trend_bias"] == "SHORT":
            direction = -1
        else:
            return []

        entry_price = float(c1515["Close"])
        stop_loss = float(c1445["Open"])

        if direction == 1 and stop_loss >= entry_price:
            return []
        if direction == -1 and stop_loss <= entry_price:
            return []

        previous_day = now_sast.date() - timedelta(days=1)
        prev_mask = m15_sast.index.date == previous_day
        prev_day_data = m15_sast.loc[prev_mask]
        if prev_day_data.empty:
            return []

        ny_session = prev_day_data.between_time("13:00", "21:00")
        if ny_session.empty:
            return []

        if direction == 1:
            take_profit = float(ny_session["High"].max())
            if take_profit <= entry_price:
                take_profit = entry_price + abs(entry_price - stop_loss) * 2
        else:
            take_profit = float(ny_session["Low"].min())
            if take_profit >= entry_price:
                take_profit = entry_price - abs(stop_loss - entry_price) * 2

        risk_reward = abs((take_profit - entry_price) / (entry_price - stop_loss))
        if risk_reward < 1.5:
            return []

        signal_time = ctx["timestamp"]  # type: ignore[assignment]
        if not self._cooldown_passed("CIS", signal_time):
            return []

        metadata = {
            "module": "CIS",
            "entry_candle": c1515.name.isoformat(),
            "bias_candle": c1445.name.isoformat(),
        }

        signal = NYUPIPSignal(
            timestamp=signal_time.to_pydatetime(),
            symbol=self.symbol,
            module="CIS",
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit_primary=take_profit,
            take_profit_secondary=None,
            take_profit_tertiary=None,
            risk_percent=self.risk_percent,
            risk_reward=risk_reward,
            notes="CIS session alignment",
            metadata=metadata,
        )

        self._last_signal_time["CIS"] = signal_time
        return [signal]

    # ------------------------------------------------------------------
    # Pattern helpers
    # ------------------------------------------------------------------
    def _detect_price_action(self, m15: pd.DataFrame, is_long: bool) -> Optional[str]:
        if len(m15) < 3:
            return None
        latest = m15.iloc[-1]
        prev = m15.iloc[-2]
        older = m15.iloc[-3]

        if is_long and self._is_bullish_engulfing(prev, latest):
            return "bullish_engulfing"
        if not is_long and self._is_bearish_engulfing(prev, latest):
            return "bearish_engulfing"

        if is_long and self._is_hammer(latest):
            return "hammer"
        if not is_long and self._is_shooting_star(latest):
            return "shooting_star"

        if self._is_inside_breakout(older, prev, latest, is_long):
            return "inside_breakout"

        return None

    @staticmethod
    def _is_bullish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
        return (
            prev["Close"] < prev["Open"]
            and curr["Close"] > curr["Open"]
            and curr["Close"] >= prev["Open"]
            and curr["Open"] <= prev["Close"]
        )

    @staticmethod
    def _is_bearish_engulfing(prev: pd.Series, curr: pd.Series) -> bool:
        return (
            prev["Close"] > prev["Open"]
            and curr["Close"] < curr["Open"]
            and curr["Close"] <= prev["Open"]
            and curr["Open"] >= prev["Close"]
        )

    @staticmethod
    def _is_hammer(candle: pd.Series) -> bool:
        body = abs(candle["Close"] - candle["Open"])
        lower_wick = (candle[["Open", "Close"]].min() - candle["Low"]).abs()
        upper_wick = (candle["High"] - candle[["Open", "Close"]].max()).abs()
        return body > 0 and lower_wick >= body * 2 and upper_wick <= body * 0.5

    @staticmethod
    def _is_shooting_star(candle: pd.Series) -> bool:
        body = abs(candle["Close"] - candle["Open"])
        upper_wick = (candle["High"] - candle[["Open", "Close"]].max()).abs()
        lower_wick = (candle[["Open", "Close"]].min() - candle["Low"]).abs()
        return body > 0 and upper_wick >= body * 2 and lower_wick <= body * 0.5

    @staticmethod
    def _is_inside_breakout(older: pd.Series, prev: pd.Series, curr: pd.Series, is_long: bool) -> bool:
        inside = prev["High"] <= older["High"] and prev["Low"] >= older["Low"]
        if not inside:
            return False
        if is_long:
            return curr["Close"] > older["High"]
        return curr["Close"] < older["Low"]

    @staticmethod
    def _find_candle(df: pd.DataFrame, target_time: time) -> Optional[pd.Series]:
        subset = df[df.index.time == target_time]
        if subset.empty:
            return None
        return subset.iloc[-1]

    def _cooldown_passed(self, module: str, current_time: datetime) -> bool:
        last_time = self._last_signal_time.get(module)
        if last_time is None:
            return True
        return (current_time - last_time) >= self.cooldown
