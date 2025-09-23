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
		# Initialize terminal
		if not mt5.initialize():
			return False
		# Attempt login (if terminal not already logged in)
		if login and password and server:
			mt5.login(login=login, password=password, server=server)
		# Ensure symbol selected
		mt5.symbol_select(self.symbol, True)
		self.initialized = True
		return True

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