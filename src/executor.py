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

	def _max_affordable_lot(self, order_type: int, entry: float, info) -> float:
		"""Compute the largest lot size affordable by current free margin, honoring lot grid.

		Returns 0.0 if even the broker-minimum lot is unaffordable.
		"""
		try:
			acc = self._account_info()
			if not acc:
				return 0.0
			free_margin = float(getattr(acc, 'margin_free', 0.0) or 0.0)
			min_lot = float(info.volume_min)
			max_lot = float(info.volume_max)
			lot_step = float(info.volume_step or 0.01)
			if free_margin <= 0:
				return 0.0
			# If minimum lot fits, binary-search up to the maximum affordable
			def fits(lots: float) -> bool:
				m = mt5.order_calc_margin(order_type, self.symbol, lots, entry)
				if m is None:
					return False
				return float(m) <= free_margin * 0.95
			# Early reject: min lot unaffordable
			if not fits(min_lot):
				return 0.0
			lo = min_lot
			hi = max(min(max_lot, min_lot * 100), min_lot)  # cap search space
			best = min_lot
			# Binary search 20 iters max
			for _ in range(20):
				mid = (lo + hi) / 2.0
				# Align to lot_step grid
				steps = max(0, int(round((mid - min_lot) / (lot_step or 0.01))))
				mid_aligned = round(min_lot + steps * lot_step, 2)
				if mid_aligned < min_lot:
					mid_aligned = min_lot
				if fits(mid_aligned):
					best = mid_aligned
					lo = mid_aligned + lot_step
				else:
					hi = max(min_lot, mid_aligned - lot_step)
			return round(best, 2)
		except Exception:
			return 0.0

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
			print(f"⏸️ Skip {self.symbol}: risk sizing produced non-positive lots")
			return None
		order_type = mt5.ORDER_TYPE_BUY if direction == 1 else mt5.ORDER_TYPE_SELL
		# --- Normalize SL/TP to broker constraints and tick grid ---
		try:
			point = float(getattr(info, 'point', 0.01) or 0.01)
			tick_size = float(getattr(info, 'trade_tick_size', point) or point)
			stops_level_points = float(getattr(info, 'stops_level', 0) or 0)
			min_distance = stops_level_points * point
			# Align price to tick grid
			def align_to_tick(price: float) -> float:
				return round(round(price / tick_size) * tick_size, 5)
			# Enforce min distance and proper side for SL/TP
			if direction == 1:
				# BUY: SL below, TP above
				if min_distance > 0:
					sl = min(sl, entry - min_distance)
					tp = max(tp, entry + min_distance)
				# Ensure strictly on correct sides
				if not (sl < entry and tp > entry):
					return None
			else:
				# SELL: SL above, TP below
				if min_distance > 0:
					sl = max(sl, entry + min_distance)
					tp = min(tp, entry - min_distance)
				if not (sl > entry and tp < entry):
					return None
			# Align to tick grid
			sl = align_to_tick(sl)
			tp = align_to_tick(tp)
		except Exception:
			pass
		# Margin-aware lot fit: cap by maximum affordable
		affordable = self._max_affordable_lot(order_type, entry, info)
		min_lot = float(info.volume_min)
		lot_step = float(info.volume_step or 0.01)
		if affordable <= 0.0:
			# Even min lot unaffordable -> skip
			print(f"⏸️ Skip {self.symbol}: insufficient free margin for broker minimum lot {min_lot}")
			return None
		# Take the minimum of risk-lot and affordable lot
		if lots > affordable:
			original_lots = lots
			lots = affordable
			print(f"🔽 Downscale {self.symbol}: lots {original_lots} -> {lots} due to margin")
		# Align to lot grid
		steps = max(0, int(round((lots - min_lot) / (lot_step or 0.01))))
		lots = round(min_lot + steps * lot_step, 2)
		if lots < min_lot:
			print(f"⏸️ Skip {self.symbol}: aligned lot {lots} < broker minimum {min_lot}")
			return None
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