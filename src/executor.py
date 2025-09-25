from typing import Optional, Dict
import math

try:
	import MetaTrader5 as mt5
except Exception:
	mt5 = None

from .config import get_config


class AutoTrader:
	def __init__(self, symbol: str):
		self.cfg = get_config()
		self.symbol = symbol
		self.enabled = self.cfg.get('execution', {}).get('enabled', False)

	def _symbol_info(self):
		info = mt5.symbol_info(self.symbol)
		if info is None:
			raised = mt5.symbol_select(self.symbol, True)
			info = mt5.symbol_info(self.symbol) if raised else None
		return info

	def _account_info(self):
		return mt5.account_info()

	def _calc_lot(self, entry: float, stop: float) -> float:
		# Simple risk model: risk % of equity divided by monetary risk per lot
		risk_pct = float(self.cfg.get('risk', {}).get('risk_percent_per_trade', 0.75)) / 100.0
		acc = self._account_info()
		if not acc:
			return 0.0
		equity = float(acc.equity)
		risk_amount = equity * risk_pct
		info = self._symbol_info()
		if not info:
			return 0.0
		point = float(info.point)
		contract_size = float(getattr(info, 'trade_contract_size', 100))
		# approximate tick value per lot
		tick_value = float(getattr(info, 'trade_tick_value', 1.0))
		tick_size = float(getattr(info, 'trade_tick_size', point))
		price_risk = abs(entry - stop)
		if price_risk <= 0:
			return 0.0
		# monetary risk per lot approximated via tick value ratio
		monetary_risk_per_lot = (price_risk / (tick_size or point)) * (tick_value or 1.0)
		if monetary_risk_per_lot <= 0:
			return 0.0
		lots = risk_amount / monetary_risk_per_lot
		# clamp to broker min/step
		min_lot = float(info.volume_min)
		lot_step = float(info.volume_step)
		max_lot = float(info.volume_max)
		lots = max(min_lot, min(max_lot, math.floor(lots / lot_step) * lot_step))
		return round(lots, 2)

	def place_market_order(self, direction: int, entry: float, sl: float, tp: float) -> Optional[Dict]:
		if not self.enabled or mt5 is None:
			return None
		info = self._symbol_info()
		if not info:
			return None
		lots = self._calc_lot(entry, sl)
		if lots <= 0:
			return None
		order_type = mt5.ORDER_TYPE_BUY if direction == 1 else mt5.ORDER_TYPE_SELL
		request = {
			"action": mt5.TRADE_ACTION_DEAL,
			"symbol": self.symbol,
			"volume": lots,
			"type": order_type,
			"price": entry,
			"sl": sl,
			"tp": tp,
			"deviation": int(self.cfg.get('execution', {}).get('deviation_points', 30)),
			"magic": 20250923,
			"comment": "GetRichFR AutoTrader",
			"type_filling": mt5.ORDER_FILLING_IOC,
		}
		result = mt5.order_send(request)
		if result and result.retcode == mt5.TRADE_RETCODE_DONE:
			return {
				"ticket": result.order,
				"volume": lots,
				"price": result.price,
			}
		return None

	def modify_sl_tp(self, ticket: int, new_sl: Optional[float] = None, new_tp: Optional[float] = None) -> bool:
		if mt5 is None:
			return False
		try:
			position = next((p for p in mt5.positions_get() or [] if p.ticket == ticket), None)
			if not position:
				return False
			request = {
				"action": mt5.TRADE_ACTION_SLTP,
				"symbol": position.symbol,
				"position": ticket,
				"sl": new_sl if new_sl is not None else position.sl,
				"tp": new_tp if new_tp is not None else position.tp,
				"magic": 20250923,
				"comment": "Modify SLTP",
			}
			result = mt5.order_send(request)
			return bool(result and result.retcode == mt5.TRADE_RETCODE_DONE)
		except Exception:
			return False

	def close_position(self, ticket: int) -> bool:
		if mt5 is None:
			return False
		try:
			pos = next((p for p in mt5.positions_get() or [] if p.ticket == ticket), None)
			if not pos:
				return False
			price = None
			order_type = None
			if pos.type == mt5.POSITION_TYPE_BUY:
				order_type = mt5.ORDER_TYPE_SELL
				price = mt5.symbol_info_tick(pos.symbol).bid
			else:
				order_type = mt5.ORDER_TYPE_BUY
				price = mt5.symbol_info_tick(pos.symbol).ask
			request = {
				"action": mt5.TRADE_ACTION_DEAL,
				"symbol": pos.symbol,
				"position": ticket,
				"volume": pos.volume,
				"type": order_type,
				"price": price,
				"deviation": int(self.cfg.get('execution', {}).get('deviation_points', 30)),
				"magic": 20250923,
				"comment": "Close position",
			}
			result = mt5.order_send(request)
			return bool(result and result.retcode == mt5.TRADE_RETCODE_DONE)
		except Exception:
			return False