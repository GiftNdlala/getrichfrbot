from typing import Optional, Dict
import math

try:
	import MetaTrader5 as mt5
except Exception:
	mt5 = None

from .config import get_config
from .mt5_connector import MT5_API_LOCK


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

	def _symbol_tick(self):
		if mt5 is None:
			return None
		try:
			tick = mt5.symbol_info_tick(self.symbol)
			if tick is None:
				mt5.symbol_select(self.symbol, True)
				tick = mt5.symbol_info_tick(self.symbol)
			return tick
		except Exception:
			return None

	def _price_digits(self, info) -> int:
		try:
			return int(getattr(info, 'digits', 2) or 2)
		except Exception:
			return 2

	def _tick_size(self, info) -> float:
		try:
			point = float(getattr(info, 'point', 0.01) or 0.01)
			tick_size = float(getattr(info, 'trade_tick_size', point) or point)
			return tick_size if tick_size > 0 else point
		except Exception:
			return 0.01

	def _align_price(self, price: float, info) -> float:
		try:
			tick_size = self._tick_size(info)
			digits = self._price_digits(info)
			return round(round(price / tick_size) * tick_size, digits)
		except Exception:
			return round(price, 2)

	def _account_info(self):
		return mt5.account_info()

	def _order_comment(self, strategy_tag: Optional[str] = None) -> str:
		"""Return an MT5-safe order comment accepted by the MT5 Python API.

		This terminal rejects longer comments before they reach the broker.
		Keep the value ASCII-only, avoid spaces, and stay within the
		23-character format validated with MT5's order check.
		"""
		base = "GetRichFR"
		if strategy_tag:
			# Keep the strategy visible, without using spaces or exceeding the
			# terminal limit validated by order_check.
			tag = "".join(ch if ch.isascii() and (ch.isalnum() or ch in "_-") else "_" for ch in strategy_tag)
			return f"{base}_{tag[:13]}"
		return base

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

	def place_market_order(self, direction: int, entry: float, sl: float, tp: float, strategy_tag: Optional[str] = None) -> Optional[Dict]:
		# Serialize quote, sizing, and order_send as one MT5 operation. This
		# prevents another stream or dashboard poll from interrupting it.
		with MT5_API_LOCK:
			return self._place_market_order_locked(direction, entry, sl, tp, strategy_tag)

	def _place_market_order_locked(self, direction: int, entry: float, sl: float, tp: float, strategy_tag: Optional[str] = None) -> Optional[Dict]:
		if not self.enabled or mt5 is None:
			return None
		info = self._symbol_info()
		if not info:
			return None
		tick = self._symbol_tick()
		if not tick:
			print(f"⏸️ Skip {self.symbol}: no live tick available")
			return None

		# Use current market price, not the strategy's estimated entry.
		market_price = float(tick.ask if direction == 1 else tick.bid)
		lots = self._calc_lot(entry, sl)
		if lots <= 0:
			print(f"⏸️ Skip {self.symbol}: risk sizing produced non-positive lots")
			return None
		order_type = mt5.ORDER_TYPE_BUY if direction == 1 else mt5.ORDER_TYPE_SELL
		# --- Normalize SL/TP to broker constraints and tick grid ---
		try:
			point = float(getattr(info, 'point', 0.01) or 0.01)
			tick_size = self._tick_size(info)
			stops_level_points = float(getattr(info, 'stops_level', 0) or 0)
			min_distance = stops_level_points * point
			# Align price to the broker's exact grid
			def align_to_grid(price: float) -> float:
				return self._align_price(price, info)
			# Enforce min distance and proper side for SL/TP
			if direction == 1:
				# BUY: SL below, TP above
				if min_distance > 0:
					sl = min(sl, market_price - min_distance)
					tp = max(tp, market_price + min_distance)
				# Ensure strictly on correct sides
				if not (sl < market_price and tp > market_price):
					return None
			else:
				# SELL: SL above, TP below
				if min_distance > 0:
					sl = max(sl, market_price + min_distance)
					tp = min(tp, market_price - min_distance)
				if not (sl > market_price and tp < market_price):
					return None
			# Align to tick grid
			market_price = align_to_grid(market_price)
			sl = align_to_grid(sl)
			tp = align_to_grid(tp)
		except Exception:
			pass
		# Margin-aware lot fit: cap by maximum affordable
		affordable = self._max_affordable_lot(order_type, market_price, info)
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

		comment = self._order_comment(strategy_tag)
		request = {
			"action": mt5.TRADE_ACTION_DEAL,
			"symbol": self.symbol,
			"volume": lots,
			"type": order_type,
			"price": market_price,
			"sl": sl,
			"tp": tp,
			"deviation": int(self.cfg.get('execution', {}).get('deviation_points', 30)),
			"magic": 20250923,
			"comment": comment,
			"type_filling": mt5.ORDER_FILLING_IOC,
		}
		result = mt5.order_send(request)
		if result and result.retcode == mt5.TRADE_RETCODE_DONE:
			print(
				f"ORDER OPEN SENT [DONE]: ticket={result.order} symbol={self.symbol} volume={lots} open_price={getattr(result,'price', None)} sl={sl} tp={tp}" + (f" strategy={strategy_tag}" if strategy_tag else ""),
				flush=True
			)
			return {
				"ticket": result.order,
				"volume": lots,
				"price": result.price,
			}
		# Failed open attempt
		try:
			mt5_error = mt5.last_error()
		except Exception:
			mt5_error = None
		print(
			f"ORDER OPEN SENT [FAILED]: symbol={self.symbol} volume={lots} open_price={market_price} sl={sl} tp={tp} retcode={getattr(result,'retcode', None)} result_comment={getattr(result,'comment', None)} request_id={getattr(result,'request_id', None)} deal={getattr(result,'deal', None)} order={getattr(result,'order', None)} mt5_error={mt5_error}" + (f" strategy={strategy_tag}" if strategy_tag else ""),
			flush=True
		)
		return None

	def modify_sl_tp(self, ticket: int, new_sl: Optional[float] = None, new_tp: Optional[float] = None) -> bool:
		with MT5_API_LOCK:
			return self._modify_sl_tp_locked(ticket, new_sl, new_tp)

	def _modify_sl_tp_locked(self, ticket: int, new_sl: Optional[float] = None, new_tp: Optional[float] = None) -> bool:
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
		with MT5_API_LOCK:
			return self._close_position_locked(ticket)

	def _close_position_locked(self, ticket: int) -> bool:
		if mt5 is None:
			print(f"ORDER CLOSE FAILED [mt5_not_available]: ticket={ticket}", flush=True)
			return False
		try:
			pos = next((p for p in mt5.positions_get() or [] if p.ticket == ticket), None)
			if not pos:
				print(f"ORDER CLOSE FAILED [position_not_found]: ticket={ticket}", flush=True)
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
			ok = bool(result and result.retcode == mt5.TRADE_RETCODE_DONE)

			if ok:
				print(
					f"ORDER CLOSE SENT [DONE]: ticket={ticket} symbol={pos.symbol} volume={pos.volume} close_price={getattr(result,'price', None)}",
					flush=True
				)
			else:
				try:
					mt5_error = mt5.last_error()
				except Exception:
					mt5_error = None
				print(
					f"ORDER CLOSE SENT [FAILED]: ticket={ticket} symbol={pos.symbol} volume={pos.volume} retcode={getattr(result,'retcode', None)} mt5_error={mt5_error}",
					flush=True
				)

			return ok
		except Exception as e:
			print(f"ORDER CLOSE FAILED [exception]: ticket={ticket} error={e}", flush=True)
			return False
