from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class EventConfig:
    min_spike_atr_mult: float = 2.0
    retest_tolerance_points: float = 10.0
    sl_buffer_points: float = 10.0
    tp_rr_multiple: float = 2.0
    max_spread_points_event: float = 50.0
    risk_percent: float = 0.5  # percent
    one_trade_per_event: bool = True


class EventEngine:
    """Generic spike/retest event engine for high-impact news trading."""

    def __init__(self, symbol: str, cfg: Optional[Dict] = None):
        self.symbol = symbol
        self.active: bool = False
        self.spike_high: Optional[float] = None
        self.spike_low: Optional[float] = None
        self.spike_marked: bool = False
        self.traded: bool = False
        self.stage: str = "idle"  # idle | waiting_spike | range_marked | traded
        cfg = cfg or {}
        self.config = EventConfig(
            min_spike_atr_mult=float(cfg.get('min_spike_atr_mult', 2.0)),
            retest_tolerance_points=float(cfg.get('retest_tolerance_points', 15.0)),
            sl_buffer_points=float(cfg.get('sl_buffer_points', 10.0)),
            tp_rr_multiple=float(cfg.get('tp_rr_multiple', 2.0)),
            max_spread_points_event=float(cfg.get('max_spread_points_event', 50.0)),
            risk_percent=float(cfg.get('risk_percent', 0.5)),
            one_trade_per_event=bool(cfg.get('one_trade_per_event', True))
        )

    def reset(self):
        self.spike_high = None
        self.spike_low = None
        self.spike_marked = False
        self.traded = False
        self.stage = "waiting_spike" if self.active else "idle"

    def set_active(self, enabled: bool):
        self.active = bool(enabled)
        self.stage = "waiting_spike" if self.active else "idle"

    def set_spike_range(self, high: float, low: float):
        if high and low and high > low:
            self.spike_high = float(high)
            self.spike_low = float(low)
            self.spike_marked = True
            self.stage = "range_marked"

    def try_detect_spike(self, high: float, low: float, atr: float):
        if not self.active or self.spike_marked:
            return
        if atr <= 0:
            return
        displacement = abs(high - low)
        if displacement >= self.config.min_spike_atr_mult * atr:
            # mark spike range
            self.spike_high = high
            self.spike_low = low
            self.spike_marked = True
            self.stage = "range_marked"

    def generate_signal(self, current_price: float) -> Optional[Dict]:
        """If spike marked and not traded (or multi allowed), look for breakout-retest continuation.

        Returns: dict with direction (+1/-1), sl, tp if conditions met; else None
        """
        if not self.active or not self.spike_marked:
            return None
        if self.traded and self.config.one_trade_per_event:
            self.stage = "traded"
            return None

        tol = self.config.retest_tolerance_points

        # Long continuation: price reclaimed spike_high and retested near it
        if current_price > (self.spike_high + tol):
            # wait for retest down into [spike_high - tol, spike_high + tol]
            # This simple engine assumes we call this after retest; in loop it's approximate.
            entry = current_price
            sl = self.spike_low - self.config.sl_buffer_points
            rr = self.config.tp_rr_multiple
            tp = entry + rr * (entry - sl)
            self.traded = True
            self.stage = "traded"
            return {"direction": 1, "entry": entry, "sl": sl, "tp": tp}

        # Short continuation: price broke below spike_low and retested up near it
        if current_price < (self.spike_low - tol):
            entry = current_price
            sl = self.spike_high + self.config.sl_buffer_points
            rr = self.config.tp_rr_multiple
            tp = entry - rr * (sl - entry)
            self.traded = True
            self.stage = "traded"
            return {"direction": -1, "entry": entry, "sl": sl, "tp": tp}

        return None

