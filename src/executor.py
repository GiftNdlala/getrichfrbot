from typing import Optional, Dict
import math
from .runtime_logging import emit
from .risk_controls import execution_snapshot, money_at_stop, floor_volume, ACKNOWLEDGED_ORDERS, usd_account_rate

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
		self.market_context = {}
		self.last_rejection = None
		self.last_outcome = None

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

	def _max_affordable_lot(self, order_type, entry, info, maximum):
		"""Fit only the proposed risk-sized volume; avoid unnecessary IPC calls."""
		account = self._account_info()
		if account is None:
			return 0.0
		free = float(account.margin_free) * 0.95
		def fits(volume):
			margin = mt5.order_calc_margin(order_type, self.symbol, volume, entry)
			return margin is not None and math.isfinite(margin) and 0 <= margin <= free
		maximum = floor_volume(maximum, info)
		if maximum and fits(maximum):
			return maximum
		minimum, step = float(info.volume_min), float(info.volume_step)
		if maximum < minimum or not fits(minimum):
			return 0.0
		low, high, best = 0, int(round((maximum-minimum)/step)), minimum
		while low <= high:
			mid = (low+high)//2
			volume = round(minimum+mid*step, 8)
			if fits(volume):
				best, low = volume, mid+1
			else:
				high = mid-1
		return best

	def place_market_order(self, direction: int, entry: float, sl: float, tp: float, strategy_tag: Optional[str] = None) -> Optional[Dict]:
		# Serialize quote, sizing, and order_send as one MT5 operation. This
		# prevents another stream or dashboard poll from interrupting it.
		with MT5_API_LOCK:
			try:
				self.last_rejection = None
				self.last_outcome = None
				return self._place_market_order_locked(direction, entry, sl, tp, strategy_tag)
			except Exception as exc:
				self.last_rejection = str(exc)
				self.last_outcome = 'blocked' if isinstance(exc, ValueError) else 'error'
				emit(f"ORDER BLOCKED: symbol={self.symbol} strategy={strategy_tag} reason={exc}", flush=True)
				return None

	def _place_market_order_locked(self, direction: int, entry: float, sl: float, tp: float, strategy_tag: Optional[str] = None) -> Optional[Dict]:
		if not self.enabled or mt5 is None:
			raise ValueError('EXECUTOR_UNAVAILABLE')
		info = self._symbol_info()
		if not info:
			raise ValueError('SYMBOL_UNAVAILABLE')
		tick = self._symbol_tick()
		if not tick:
			raise ValueError('QUOTE_UNAVAILABLE')

		# Use current market price, not the strategy's estimated entry.
		market_price = float(tick.ask if direction == 1 else tick.bid)
		if direction not in (1, -1) or not all(math.isfinite(float(v)) and float(v) > 0 for v in (entry, sl, tp)):
			raise ValueError('INVALID_ORDER_LEVELS')
		account = self._account_info()
		needs_conversion = (strategy_tag or '').startswith('FARMER') or float(self.cfg.get('risk', {}).get('cost_buffer_dollars', 0)) > 0
		usd_rate = usd_account_rate(mt5, account) if needs_conversion and account is not None else 1.0
		budget, farmer = execution_snapshot(mt5, self.cfg, self.symbol, self.market_context, tick, account, strategy_tag or '', usd_rate=usd_rate)
		order_type = mt5.ORDER_TYPE_BUY if direction == 1 else mt5.ORDER_TYPE_SELL
		# --- Normalize SL/TP to broker constraints and tick grid ---
		try:
			point = float(getattr(info, 'point', 0.01) or 0.01)
			tick_size = self._tick_size(info)
			stops_level_points = float(getattr(info, 'trade_stops_level', 0) or 0)
			min_distance = stops_level_points * point
			# Align price to the broker's exact grid
			def align_to_grid(price: float) -> float:
				return self._align_price(price, info)
			# Enforce min distance and proper side for SL/TP
			if direction == 1:
				# BUY: SL below, TP above
				if market_price - sl < min_distance:
					raise ValueError('STOP_TOO_CLOSE')
				# Ensure strictly on correct sides
				if not (sl < market_price and tp > market_price):
					raise ValueError('STOP_OR_TARGET_WRONG_SIDE')
			else:
				# SELL: SL above, TP below
				if sl - market_price < min_distance:
					raise ValueError('STOP_TOO_CLOSE')
				if not (sl > market_price and tp < market_price):
					raise ValueError('STOP_OR_TARGET_WRONG_SIDE')
			# Align to tick grid
			market_price = align_to_grid(market_price)
			sl = align_to_grid(sl)
			tp = align_to_grid(tp)
		except Exception as exc:
			raise ValueError(f'INVALID_BROKER_LEVELS:{exc}') from exc
		# Size only AFTER live-price and tick-grid normalization; never round up.
		fc = self.cfg.get('execution', {}).get('farmer', {})
		cost_buffer = (float(fc.get('estimated_round_trip_cost_dollars', 0.15)) if farmer else float(self.cfg.get('risk', {}).get('cost_buffer_dollars', 0.0))) * usd_rate
		unit_loss = money_at_stop(mt5, self.symbol, order_type, float(info.volume_min), market_price, sl)
		if unit_loss <= 0:
			raise ValueError('INVALID_STOP_RISK')
		lots = floor_volume((budget - cost_buffer) / unit_loss * float(info.volume_min), info)
		if lots <= 0:
			raise ValueError(f'MINIMUM_LOT_EXCEEDS_RISK:currency={account.currency} budget={budget:.2f} minimum_lot={info.volume_min} stop_loss={unit_loss:.2f} costs={cost_buffer:.2f} required={unit_loss+cost_buffer:.2f}')
		# Margin-aware lot fit: cap by maximum affordable
		affordable = self._max_affordable_lot(order_type, market_price, info, lots)
		min_lot = float(info.volume_min)
		lot_step = float(info.volume_step or 0.01)
		if affordable <= 0.0:
			# Even min lot unaffordable -> skip
			raise ValueError('INSUFFICIENT_MARGIN_FOR_MINIMUM_LOT')
		# Take the minimum of risk-lot and affordable lot
		if lots > affordable:
			original_lots = lots
			lots = affordable
			emit(f" Downscale {self.symbol}: lots {original_lots} -> {lots} due to margin")
		# Align to lot grid
		lots = floor_volume(lots, info)
		if lots < min_lot:
			raise ValueError('VOLUME_BELOW_MINIMUM')

		stop_risk = money_at_stop(mt5, self.symbol, order_type, lots, market_price, sl)
		if stop_risk + cost_buffer > budget + 1e-8:
			raise ValueError('FINAL_RISK_EXCEEDS_BUDGET')
		if farmer:
			# Convert USD target into account P&L before deriving a price.
			target = float(fc.get('target_profit_dollars', 2.0)) * usd_rate
			per_tick = mt5.order_calc_profit(order_type, self.symbol, lots, market_price, market_price + direction * self._tick_size(info))
			if per_tick is None or per_tick <= 0:
				raise ValueError('TARGET_CALCULATION_UNAVAILABLE')
			tp = self._align_price(market_price + direction * math.ceil((target + cost_buffer) / per_tick) * self._tick_size(info), info)
			reward = mt5.order_calc_profit(order_type, self.symbol, lots, market_price, tp)
			spread_cost = money_at_stop(mt5, self.symbol, order_type, lots, float(tick.ask if direction == 1 else tick.bid), float(tick.bid if direction == 1 else tick.ask))
			if reward is None or reward - cost_buffer < stop_risk * float(fc.get('min_net_reward_risk', 1.0)):
				raise ValueError('FARMER_REWARD_TOO_SMALL')
			if spread_cost + cost_buffer > target * float(fc.get('max_cost_target_fraction', 0.25)):
				raise ValueError('FARMER_COST_TOO_HIGH')
		if (sl - market_price) * direction >= 0 or (tp - market_price) * direction <= 0 or min(abs(market_price-sl), abs(tp-market_price)) < min_distance:
			raise ValueError('FINAL_LEVELS_INVALID')
		from datetime import datetime, timezone
		from .risk_controls import epoch
		final_tick = self._symbol_tick()
		now = datetime.now(timezone.utc).timestamp()
		max_age = float(self.cfg.get('execution', {}).get('max_quote_age_seconds', 15))
		if not final_tick or not -2 <= now-float(final_tick.time) <= max_age or now-epoch(self.market_context['timestamp']) > max_age:
			raise ValueError('QUOTE_EXPIRED_DURING_CHECKS')
		final_price = float(final_tick.ask if direction == 1 else final_tick.bid)
		drift_cap = float(self.cfg.get('execution', {}).get('max_entry_drift_points', 50)) * float(info.point)
		if not all(math.isfinite(float(v)) and float(v) > 0 for v in (final_tick.bid, final_tick.ask)) or final_tick.ask < final_tick.bid or abs(final_price-market_price) > drift_cap:
			raise ValueError('QUOTE_MOVED_DURING_CHECKS')
		final_spread = (final_tick.ask-final_tick.bid) / info.point
		if final_spread > float(self.cfg.get('filters', {}).get('max_spread_points', 40)):
			raise ValueError('SPREAD_CAP')
		normal = self.market_context.get('normal_spread_points')
		if normal and final_spread > normal * float(self.cfg.get('filters', {}).get('spread_spike_multiplier', 2)):
			raise ValueError('SPREAD_SPIKE')
		final_price = self._align_price(final_price, info)
		if farmer:
			tp = self._align_price(tp + final_price-market_price, info)
		market_price, tick = final_price, final_tick
		final_risk = money_at_stop(mt5, self.symbol, order_type, lots, market_price, sl) + cost_buffer
		if final_risk > budget + 1e-8:
			raise ValueError('FINAL_RISK_EXCEEDS_BUDGET')
		if (sl-market_price)*direction >= 0 or (tp-market_price)*direction <= 0 or min(abs(sl-market_price),abs(tp-market_price)) < min_distance:
			raise ValueError('FINAL_LEVELS_INVALID')
		if farmer:
			gross = mt5.order_calc_profit(order_type,self.symbol,lots,market_price,tp)
			final_spread_cost = money_at_stop(mt5,self.symbol,order_type,lots,tick.ask if direction==1 else tick.bid,tick.bid if direction==1 else tick.ask)
			if gross is None or gross-cost_buffer < max(target,(final_risk-cost_buffer)*float(fc.get('min_net_reward_risk',1))) - 1e-8 or final_spread_cost+cost_buffer > target*float(fc.get('max_cost_target_fraction',.25)):
				raise ValueError('FARMER_FINAL_ECONOMICS_CHANGED')
		stop_risk = final_risk-cost_buffer
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
		if result and result.retcode in (mt5.TRADE_RETCODE_DONE, getattr(mt5, 'TRADE_RETCODE_DONE_PARTIAL', 10010)):
			lots = min(lots, float(getattr(result, 'volume', lots)))
			self.last_outcome = 'filled'
			ACKNOWLEDGED_ORDERS[(account.login, result.order)] = {'volume': lots, 'risk': stop_risk + cost_buffer, 'cost_buffer': cost_buffer, 'symbol': self.symbol, 'strategy': strategy_tag or '', 'deal': getattr(result, 'deal', None)}
			emit(
				f"ORDER OPEN SENT [DONE]: ticket={result.order} symbol={self.symbol} volume={lots} open_price={getattr(result,'price', None)} sl={sl} tp={tp}" + (f" strategy={strategy_tag}" if strategy_tag else ""),
				flush=True
			)
			return {
				"ticket": result.order,
				"open_deal_id": getattr(result, "deal", None),
				"bid": float(tick.bid),
				"ask": float(tick.ask),
				"point": float(info.point),
				"spread_points": (tick.ask-tick.bid)/info.point,
				"volume": lots,
				"price": result.price,
				"sl": sl,
				"tp": tp,
				"magic": request["magic"],
				"order_comment": comment,
			}
		self.last_outcome = 'rejected'
		self.last_rejection = f"BROKER_REJECTED:retcode={getattr(result,'retcode',None)} comment={getattr(result,'comment',None)}"
		# Failed open attempt
		try:
			mt5_error = mt5.last_error()
		except Exception:
			mt5_error = None
		emit(
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
			emit(f"ORDER CLOSE FAILED [mt5_not_available]: ticket={ticket}", flush=True)
			return False
		try:
			pos = next((p for p in mt5.positions_get() or [] if p.ticket == ticket), None)
			if not pos:
				emit(f"ORDER CLOSE FAILED [position_not_found]: ticket={ticket}", flush=True)
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
				"type_filling": mt5.ORDER_FILLING_IOC,
			}

			result = mt5.order_send(request)
			ok = bool(result and result.retcode == mt5.TRADE_RETCODE_DONE)

			if ok:
				emit(
					f"ORDER CLOSE SENT [DONE]: ticket={ticket} symbol={pos.symbol} volume={pos.volume} close_price={getattr(result,'price', None)}",
					flush=True
				)
			else:
				try:
					mt5_error = mt5.last_error()
				except Exception:
					mt5_error = None
				emit(
					f"ORDER CLOSE SENT [FAILED]: ticket={ticket} symbol={pos.symbol} volume={pos.volume} retcode={getattr(result,'retcode', None)} mt5_error={mt5_error}",
					flush=True
				)

			return ok
		except Exception as e:
			emit(f"ORDER CLOSE FAILED [exception]: ticket={ticket} error={e}", flush=True)
			return False
