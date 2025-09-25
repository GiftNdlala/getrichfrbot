from typing import Optional, Dict
import datetime as dt
import os

try:
	import MetaTrader5 as mt5
except Exception:
	mt5 = None

from .config import get_config


class MT5Connector:
	def __init__(self):
		self.initialized = False
		self.symbol = None
		self._cfg = get_config()

	def initialize(self) -> bool:
		if mt5 is None:
			return False
		cfg = self._cfg
		broker = cfg.get('broker', {})
		login = broker.get('login')
		server = broker.get('server')
		self.symbol = broker.get('symbol', 'XAUUSD')
		password_env = cfg.get('secrets_env', {}).get('mt5_password_env', 'MT5_PASSWORD')
		password = os.getenv(password_env)
		# Initialize terminal (use explicit path if provided)
		terminal_path = os.getenv('MT5_TERMINAL_PATH')
		if terminal_path:
			ok = mt5.initialize(path=terminal_path)
		else:
			ok = mt5.initialize()
		if not ok:
			return False
		# Attempt login (if terminal not already logged in)
		if login and password and server:
			mt5.login(login=login, password=password, server=server)
		# Ensure symbol selected
		mt5.symbol_select(self.symbol, True)
		self.initialized = True
		return True

	def get_rates(self, timeframe, count: int = 1000):
		if not self.initialized and not self.initialize():
			return None
		try:
			rates = mt5.copy_rates_from_pos(self.symbol, timeframe, 0, count)
			return rates
		except Exception:
			return None

	def shutdown(self):
		if mt5:
			mt5.shutdown()
		self.initialized = False

	def get_current_quote(self) -> Optional[Dict]:
		if not self.initialized:
			if not self.initialize():
				return None
		# Try last tick
		tick = mt5.symbol_info_tick(self.symbol)
		if tick:
			price = float(tick.last) if tick.last else float(tick.bid or tick.ask or 0)
			# Get previous close from last M1 bar
			prev_close = price
			rates = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M1, 0, 3)
			if rates is not None and len(rates) >= 2:
				prev_close = float(rates[-2]['close'])
			spread = 0.0
			if tick.bid and tick.ask:
				# Points, not pips
				info = mt5.symbol_info(self.symbol)
				point = info.point if info else 0.01
				spread = float((tick.ask - tick.bid) / (point or 0.01))
			return {
				'price': price,
				'prev_close': prev_close,
				'timestamp': dt.datetime.fromtimestamp(tick.time or dt.datetime.now().timestamp()),
				'volume': float(tick.volume) if hasattr(tick, 'volume') and tick.volume else 0.0,
				'spread_points': spread,
				'source': 'MT5'
			}
		return None

	def get_positions(self, symbol_filter: Optional[str] = None):
		if not self.initialized and not self.initialize():
			return []
		try:
			positions = mt5.positions_get()
			if symbol_filter:
				positions = [p for p in (positions or []) if p.symbol == symbol_filter]
			return positions or []
		except Exception:
			return []

	def get_orders_history(self, count: int = 50):
		if not self.initialized and not self.initialize():
			return []
		try:
			from datetime import datetime, timedelta
			end = dt.datetime.now()
			start = end - dt.timedelta(days=5)
			history = mt5.history_deals_get(start, end)
			return history or []
		except Exception:
			return []

	def get_equity(self) -> Optional[float]:
		if not self.initialized and not self.initialize():
			return None
		try:
			ai = mt5.account_info()
			return float(ai.equity) if ai else None
		except Exception:
			return None

	def get_symbol_info(self):
		if not self.initialized and not self.initialize():
			return None
		try:
			return mt5.symbol_info(self.symbol)
		except Exception:
			return None

	def today_realized_pnl(self) -> float:
		"""Sum of today's realized profit for this symbol."""
		if not self.initialized and not self.initialize():
			return 0.0
		try:
			now = dt.datetime.now()
			start = now.replace(hour=0, minute=0, second=0, microsecond=0)
			deals = mt5.history_deals_get(start, now)
			total = 0.0
			if deals:
				for d in deals:
					try:
						if getattr(d, 'symbol', '') == self.symbol:
							total += float(getattr(d, 'profit', 0.0))
					except Exception:
						pass
			return total
		except Exception:
			return 0.0