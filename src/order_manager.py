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
		# Per-symbol caps
		cfg = get_config()
		caps = cfg.get('risk', {}).get('symbol_caps', {})
		self.daily_loss_limit_pct = float(caps.get(symbol, {}).get('daily_loss_limit_pct', 3.0))
		self.max_open_risk_pct = float(caps.get(symbol, {}).get('max_open_risk_pct', 5.0))
		# Loss minimizer
		lm = cfg.get('execution', {}).get('loss_minimizer', {})
		self.loss_minimizer_enabled = bool(lm.get('enabled', True))
		self.lm_soft_loss = float(lm.get('soft_loss_dollars', 3.0))
		self.lm_max_loss = float(lm.get('max_loss_dollars', 12.0))
		self.lm_retrace_points = float(lm.get('retrace_points', 10.0))
		self.lm_window_seconds = int(lm.get('improvement_window_seconds', 20))
		self._minimize_state: Dict[int, Dict] = {}

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
		# Per-symbol caps: compute realized PnL today
		realized_today = self.mt5.today_realized_pnl()
		equity = self.mt5.get_equity() or 0.0
		loss_pct_today = 0.0
		if equity > 0 and realized_today < 0:
			loss_pct_today = abs(realized_today) / equity * 100.0
		if loss_pct_today >= self.daily_loss_limit_pct:
			print(f"⛔ Daily loss cap hit for {self.symbol}: {loss_pct_today:.2f}% ≥ {self.daily_loss_limit_pct:.2f}%. Halting new orders.")
			# Mark halt state on manager; LiveDataStream can choose to consult here if needed.
			self.halt_new_orders = True
		else:
			self.halt_new_orders = False
		positions = self.mt5.get_positions(self.symbol)
		open_tickets = {p.ticket for p in positions}
		# Close detection for tickets we track but are not open anymore
		for ticket, state in list(self.managed.items()):
			if ticket not in open_tickets:
				# closed: try enrich with close price/time from MT5 deals history
				close_price = None
				close_time_iso = None
				pnl = None
				try:
					deals = []
					if hasattr(self.mt5, 'get_deals_for_position'):
						deals = self.mt5.get_deals_for_position(ticket)
					if not deals:
						deals = self.mt5.get_orders_history(count=500)
					
					# Find the exit deal for this position (deal_type 1 = exit, 0 = entry)
					closing_deal = None
					for d in deals or []:
						# Check position field (not position_id) and deal type
						pos = getattr(d, 'position', None)
						deal_type = getattr(d, 'type', None)
						
						if pos != ticket:
							continue
						
						# Look for exit deal (type 1) or just the latest deal
						if deal_type == 1:  # Exit deal
							if not closing_deal or getattr(d, 'time', 0) >= getattr(closing_deal, 'time', 0):
								closing_deal = d
						elif not closing_deal:  # Fallback to any deal
							closing_deal = d
					
					if closing_deal:
						close_price = float(getattr(closing_deal, 'price', 0.0))
						pnl = float(getattr(closing_deal, 'profit', 0.0))
						try:
							import datetime as _dt
							ts = getattr(closing_deal, 'time', None)
							if ts:
								close_time_iso = _dt.datetime.fromtimestamp(ts).isoformat()
						except Exception as e:
							print(f"⚠️ Error parsing close time for ticket {ticket}: {e}")
					else:
						print(f"⚠️ No closing deal found for ticket {ticket} in {len(deals or [])} deals")
				except Exception as e:
					print(f"❌ Error fetching close data for ticket {ticket}: {e}")
				
				payload = {'status': 'CLOSED'}
				if close_price is not None and close_price > 0:
					payload['close_price'] = close_price
					print(f"✅ Saved close_price={close_price:.2f} for ticket {ticket}")
				if close_time_iso is not None:
					payload['close_time'] = close_time_iso
				if pnl is not None:
					payload['pnl'] = pnl
				self.persistence.update_trade(ticket, payload)
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
			# Time-based exit with loss minimizer
			if age >= max_age:
				if not self._try_loss_minimizer(pos, st):
					self.autotrader.close_position(st.ticket)
					self.persistence.update_trade(st.ticket, {
						'status': 'CLOSED',
						'reason': 'TIME'
					})
					self.managed.pop(st.ticket, None)
		except Exception:
			return

	def _approx_unrealized_dollars(self, pos, current_price: float) -> float:
		try:
			info = self.mt5.get_symbol_info()
			tick_val = float(getattr(info, 'trade_tick_value', 1.0)) if info else 1.0
			tick_size = float(getattr(info, 'trade_tick_size', 0.01)) if info else 0.01
			points = (current_price - pos.price_open) if pos.type == 0 else (pos.price_open - current_price)  # 0=buy,1=sell
			ticks = points / (tick_size or 0.01)
			return float(pos.volume) * ticks * tick_val
		except Exception:
			return 0.0

	def _try_loss_minimizer(self, pos, st: ManagedOrder) -> bool:
		"""If enabled, try to reduce loss by waiting for a small retrace within a short window.
		Returns True if deferring close; False to proceed closing now.
		"""
		if not self.loss_minimizer_enabled:
			return False
		pnl = self._approx_unrealized_dollars(pos, pos.price_current)
		# Close immediately if within soft loss or profitable
		if pnl >= 0 or abs(pnl) <= self.lm_soft_loss:
			return False
		# Close immediately if beyond max allowed loss
		if abs(pnl) >= self.lm_max_loss:
			print(f"⛔ Max loss cap reached ticket={st.ticket}: {pnl:.2f} >= {self.lm_max_loss:.2f}, closing now")
			return False
		state = self._minimize_state.get(st.ticket)
		now = datetime.utcnow()
		# Compute small retrace target in points
		point = float(getattr(self.mt5.get_symbol_info(), 'point', 0.01) or 0.01)
		retrace_price = pos.price_current + (self.lm_retrace_points * point if st.direction == 1 else -self.lm_retrace_points * point)
		if not state:
			self._minimize_state[st.ticket] = {
				'start': now,
				'target': retrace_price,
				'dir': st.direction
			}
			print(f"🕒 Loss minimizer armed ticket={st.ticket} target={retrace_price:.2f} window={self.lm_window_seconds}s")
			return True
		# Window elapsed -> proceed to close
		if (now - state['start']).total_seconds() >= self.lm_window_seconds:
			print(f"⌛ Loss minimizer window elapsed ticket={st.ticket}, proceeding to close")
			self._minimize_state.pop(st.ticket, None)
			return False
		# Retrace achieved -> proceed to close with reduced loss
		if (st.direction == 1 and pos.price_current >= state['target']) or (st.direction == -1 and pos.price_current <= state['target']):
			print(f"✅ Loss minimizer hit target ticket={st.ticket} price={pos.price_current:.2f}, closing")
			self._minimize_state.pop(st.ticket, None)
			return False
		# Still waiting
		return True

