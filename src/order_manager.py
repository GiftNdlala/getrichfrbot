from collections import deque, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional, List

from .config import get_config
from .persistence import PersistenceManager
from .executor import AutoTrader
try:
	from .mt5_connector import MT5Connector
except Exception:
	MT5Connector = None


@dataclass
class ManagedOrder:
	"""State for a managed order"""
	ticket: int
	open_time: datetime
	entry: float
	sl: float
	tp: float
	direction: int
	alert_level: str
	tier: Optional[str] = None


class CampaignManager:
	"""Controls per-side trading frequency in a rolling window"""
	def __init__(self, window_minutes: int, max_per_level: Dict[str, int], min_spacing_seconds: int = 60):
		self.window = timedelta(minutes=window_minutes)
		self.max_per_level = max_per_level
		self.min_spacing = timedelta(seconds=min_spacing_seconds)
		self.events: Dict[str, deque] = defaultdict(deque)  # key: f"{symbol}:{side}:{level}"
		self.last_time: Dict[str, datetime] = {}

	def _key(self, symbol: str, side: int, level: str) -> str:
		return f"{symbol}:{'BUY' if side==1 else 'SELL'}:{level}"

	def allow(self, symbol: str, side: int, level: str, now: Optional[datetime] = None) -> bool:
		now = now or datetime.utcnow()
		key = self._key(symbol, side, level)
		# enforce spacing
		last = self.last_time.get(key)
		if last and now - last < self.min_spacing:
			return False
		# evict old entries
		q = self.events[key]
		while q and now - q[0] > self.window:
			q.popleft()
		limit = self.max_per_level.get(level.upper(), self.max_per_level.get('HIGH', 6))
		return len(q) < limit

	def record(self, symbol: str, side: int, level: str, now: Optional[datetime] = None):
		now = now or datetime.utcnow()
		key = self._key(symbol, side, level)
		self.events[key].append(now)
		self.last_time[key] = now

	def current_count(self, symbol: str, side: int, level: str, now: Optional[datetime] = None) -> int:
		now = now or datetime.utcnow()
		key = self._key(symbol, side, level)
		q = self.events[key]
		while q and now - q[0] > self.window:
			q.popleft()
		return len(q)


class OrderManager:
	"""Manages open positions: reconciliation, timed exit, BE moves, tiered TP logic"""
	def __init__(self, symbol: str):
		self.symbol = symbol
		self.cfg = get_config()
		self.persistence = PersistenceManager()
		self.autotrader = AutoTrader(symbol)
		self.mt5 = MT5Connector() if MT5Connector else None
		self.managed: Dict[int, ManagedOrder] = {}

	def register_new_order(self, ticket: int, direction: int, entry: float, sl: float, tp: float, alert_level: str, tier: Optional[str] = None):
		self.managed[ticket] = ManagedOrder(ticket=ticket, open_time=datetime.utcnow(), entry=entry, sl=sl, tp=tp, direction=direction, alert_level=alert_level, tier=tier)
		self.persistence.update_trade(ticket, {
			'open_time': datetime.utcnow().isoformat(),
			'status': 'OPEN',
			'alert_level': alert_level,
			'tier': tier or ''
		})

	def reconcile(self):
		"""Poll MT5 and update statuses; apply exit rules"""
		if not self.mt5:
			return
		positions = self.mt5.get_positions(self.symbol)
		open_tickets = {p.ticket for p in positions}
		# Close detection for tickets we track but are not open anymore
		for ticket, state in list(self.managed.items()):
			if ticket not in open_tickets:
				# closed externally; mark unknown reason
				self.persistence.update_trade(ticket, {
					'status': 'CLOSED'
				})
				self.managed.pop(ticket, None)
		# Apply rules for open positions
		for p in positions:
			st = self.managed.get(p.ticket)
			if not st:
				continue
			self._apply_exit_rules(p, st)

	def _apply_exit_rules(self, pos, st: ManagedOrder):
		"""Apply BE, time-based exit, and tier TP for low/medium/high"""
		try:
			alert = (st.alert_level or 'LOW').upper()
			exec_cfg = self.cfg.get('execution', {})
			max_minutes_map = exec_cfg.get('max_position_minutes', { 'LOW': 10, 'MEDIUM': 10, 'HIGH': 20 })
			max_age = timedelta(minutes=int(max_minutes_map.get(alert, 10)))
			age = datetime.utcnow() - st.open_time
			# current price
			price = pos.price_current
			risk = abs(st.entry - st.sl)
			if risk <= 0:
				return
			unrealized_r = (price - st.entry) / risk if st.direction == 1 else (st.entry - price) / risk
			# Breakeven move at >= 1R
			be_after = float(self.cfg.get('risk', {}).get('move_sl_to_be_after_r_multiple', 1.0))
			if unrealized_r >= be_after:
				# move SL to entry +/- a tiny buffer in price units
				buffer = 0.02
				be_price = st.entry + (buffer * (1 if st.direction == 1 else -1))
				self.autotrader.modify_sl_tp(st.ticket, new_sl=be_price)
			# Tiered TP for HIGH
			if alert == 'HIGH' and st.tier:
				# nothing additional here; tiers were set as per trade creation
				pass
			# Time-based exit
			if age >= max_age:
				# for LOW/MEDIUM prioritize exit quickly
				self.autotrader.close_position(st.ticket)
				self.persistence.update_trade(st.ticket, {
					'status': 'CLOSED',
					'reason': 'TIME'
				})
				self.managed.pop(st.ticket, None)
		except Exception:
			return

