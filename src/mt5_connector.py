from typing import Optional, Dict
import datetime as dt
import os
import functools
import threading

try:
	import MetaTrader5 as mt5
except Exception:
	mt5 = None

from .config import get_config


# The MetaTrader5 Python package communicates with one desktop terminal session.
# All dashboard threads must serialize access to that shared IPC connection.
MT5_API_LOCK = threading.RLock()


def mt5_synchronized(method):
	"""Serialize a connector call against the shared MT5 terminal session."""
	@functools.wraps(method)
	def wrapped(*args, **kwargs):
		with MT5_API_LOCK:
			return method(*args, **kwargs)
	return wrapped


class MT5Connector:
	def __init__(self):
		self.initialized = False
		self.symbol = None
		self._cfg = get_config()

	@mt5_synchronized
	def initialize(self) -> bool:
		if mt5 is None:
			return False
		cfg = self._cfg
		broker = cfg.get('broker', {})
		login = broker.get('login')
		server = broker.get('server')
		# Respect a symbol already set by the caller (e.g., per-stream override)
		self.symbol = self.symbol or broker.get('symbol', 'XAUUSD')
		password_env = cfg.get('secrets_env', {}).get('mt5_password_env', 'MT5_PASSWORD')
		password = os.getenv(password_env)
		# Attach only once to the process-wide terminal session. Repeating
		# initialize/login from dashboard polling threads can interrupt requests.
		if mt5.terminal_info() is None:
			terminal_path = os.getenv('MT5_TERMINAL_PATH')
			ok = mt5.initialize(path=terminal_path) if terminal_path else mt5.initialize()
			if not ok:
				print(f"MT5 INITIALIZE FAILED: error={mt5.last_error()}", flush=True)
				return False

		account = mt5.account_info()
		if login and password and server and (account is None or int(account.login) != int(login)):
			if not mt5.login(login=login, password=password, server=server):
				print(f"MT5 LOGIN FAILED: error={mt5.last_error()}", flush=True)
				return False

		# Ensure symbol selected and surface a failure instead of proceeding blind.
		if not mt5.symbol_select(self.symbol, True):
			print(f"MT5 SYMBOL SELECT FAILED: symbol={self.symbol} error={mt5.last_error()}", flush=True)
			return False
		self.initialized = True
		return True

	def _ensure_initialized(self) -> bool:
		"""Reconnect when the terminal disappears during a long-running session."""
		if mt5 is None:
			return False
		try:
			terminal_available = mt5.terminal_info() is not None
		except Exception:
			terminal_available = False
		if self.initialized and terminal_available:
			return True
		self.initialized = False
		return self.initialize()

	@mt5_synchronized
	def get_rates(self, timeframe, count: int = 1000):
		if not self._ensure_initialized():
			return None
		try:
			rates = mt5.copy_rates_from_pos(self.symbol, timeframe, 0, count)
			return rates
		except Exception:
			return None

	@mt5_synchronized
	def shutdown(self):
		if mt5:
			mt5.shutdown()
		self.initialized = False

	@mt5_synchronized
	def get_current_quote(self) -> Optional[Dict]:
		if not self._ensure_initialized():
			return None
		# Try last tick
		tick = mt5.symbol_info_tick(self.symbol)
		if tick is None:
			# A terminal can remain installed but lose its IPC/session connection.
			# Reconnect once before allowing the stream to treat this as a data miss.
			self.initialized = False
			if not self._ensure_initialized():
				return None
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

	@mt5_synchronized
	def get_positions(self, symbol_filter: Optional[str] = None):
		if not self._ensure_initialized():
			return []
		try:
			positions = mt5.positions_get()
			if symbol_filter:
				positions = [p for p in (positions or []) if p.symbol == symbol_filter]
			return positions or []
		except Exception:
			return []

	@mt5_synchronized
	def get_orders_history(self, count: int = 50):
		if not self._ensure_initialized():
			return []
		try:
			from datetime import datetime, timedelta
			end = dt.datetime.now()
			start = end - dt.timedelta(days=5)
			history = mt5.history_deals_get(start, end)
			return history or []
		except Exception:
			return []

	@mt5_synchronized
	def get_deals_for_position(self, position_id: int):
		if not self._ensure_initialized():
			return []
		try:
			deals = mt5.history_deals_get(position=position_id)
			return deals or []
		except Exception:
			return []

	@mt5_synchronized
	def get_account_info(self):
		if not self._ensure_initialized():
			return None
		try:
			return mt5.account_info()
		except Exception:
			return None

	@mt5_synchronized
	def get_equity(self) -> Optional[float]:
		if not self._ensure_initialized():
			return None
		try:
			ai = mt5.account_info()
			return float(ai.equity) if ai else None
		except Exception:
			return None

	@mt5_synchronized
	def get_symbol_info(self):
		if not self._ensure_initialized():
			return None
		try:
			return mt5.symbol_info(self.symbol)
		except Exception:
			return None

	@mt5_synchronized
	def today_realized_pnl(self) -> float:
		"""Sum of today's realized profit for this symbol."""
		if not self._ensure_initialized():
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
