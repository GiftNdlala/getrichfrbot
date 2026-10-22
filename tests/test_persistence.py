import os
import sqlite3
import tempfile
import unittest
from datetime import datetime
from types import SimpleNamespace

from src.persistence import PersistenceManager
from src.order_manager import ManagedOrder, OrderManager


class PersistenceManagerTests(unittest.TestCase):
	def test_migrates_existing_database_and_records_trade_history(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			db_path = os.path.join(temp_dir, "trades.sqlite")
			with sqlite3.connect(db_path) as conn:
				conn.execute(
					"""
					CREATE TABLE trades (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						timestamp TEXT NOT NULL,
						symbol TEXT NOT NULL,
						direction INTEGER,
						entry REAL,
						sl REAL,
						tp REAL,
						lots REAL,
						ticket INTEGER,
						status TEXT
					)
					"""
				)
				conn.execute(
					"INSERT INTO trades (timestamp, symbol, ticket, status) VALUES (?, ?, ?, ?)",
					("2026-01-01T00:00:00", "XAUUSDm", 100, "OPEN"),
				)
				conn.execute(
					"""
					CREATE TABLE signals (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						timestamp TEXT NOT NULL,
						symbol TEXT NOT NULL,
						current_price REAL,
						signal INTEGER,
						signal_type TEXT,
						confidence REAL,
						rsi REAL,
						macd REAL,
						macd_signal REAL,
						sma_20 REAL,
						sma_50 REAL,
						price_change REAL,
						price_change_pct REAL,
						alert_level TEXT,
						alert_color TEXT,
						target_pips INTEGER,
						success_rate REAL,
						entry_price REAL,
						stop_loss REAL,
						take_profit_1 REAL,
						take_profit_2 REAL,
						take_profit_3 REAL,
						risk_reward_ratio REAL,
						atr_value REAL,
						position_size_percent REAL,
						risk_amount_dollars REAL,
						potential_profit_tp1 REAL,
						potential_profit_tp2 REAL,
						potential_profit_tp3 REAL
					)
					"""
				)

			store = PersistenceManager(db_path)
			signal_id = store.save_signal({
				"timestamp": "2026-10-22T07:00:00",
				"symbol": "XAUUSDm",
				"signal_id": "signal-abc",
				"data_source": "MT5",
				"bid": 2700.1,
				"ask": 2700.2,
				"point": 0.01,
				"spread_points": 10,
			})
			store.save_trade({
				"timestamp": "2026-10-22T07:00:00",
				"symbol": "XAUUSDm",
				"ticket": 456,
				"status": "SENT",
				"signal_id": signal_id,
				"signal_price": 2700.15,
				"fill_price": 2700.2,
				"entry": 2700.2,
				"sl": 2690,
				"tp": 2720,
				"data_source": "MT5",
				"bid": 2700.1,
				"ask": 2700.2,
				"point": 0.01,
				"spread_points": 10,
				"setup_id": "TEST",
				"magic": 20250923,
				"order_comment": "GetRichFR_TEST",
			})
			store.update_trade(456, {
				"status": "CLOSED",
				"close_price": 2710.0,
				"close_time": "2026-10-22T07:10:00",
				"pnl": 9.8,
				"commission": -0.1,
				"swap": 0.0,
				"reason": "TP",
			})
			store.save_trade({
				"timestamp": "2026-10-22T07:00:00",
				"symbol": "XAUUSDm",
				"ticket": 457,
				"direction": 1,
				"entry": 2700.0,
				"lots": 0.01,
				"status": "SENT",
			})
			store.update_trade(457, {"status": "CLOSED", "pnl": 2.0})

			with sqlite3.connect(db_path) as conn:
				conn.row_factory = sqlite3.Row
				trade = dict(conn.execute(
					"SELECT * FROM trades WHERE ticket = ?", (456,)
				).fetchone())
				trade_without_close_fill = dict(conn.execute(
					"SELECT * FROM trades WHERE ticket = ?", (457,)
				).fetchone())
				legacy_status = conn.execute(
					"SELECT status FROM trades WHERE ticket = ?", (100,)
				).fetchone()[0]
			events = store.get_trade_events(456)

			self.assertEqual(signal_id, "signal-abc")
			self.assertEqual(trade["signal_price"], 2700.15)
			self.assertEqual(trade["fill_price"], 2700.2)
			self.assertEqual(trade["data_source"], "MT5")
			self.assertEqual(trade["spread_points"], 10)
			self.assertEqual(trade["close_price"], 2710.0)
			self.assertEqual(trade["reason"], "TP")
			self.assertIsNone(trade_without_close_fill["close_price"])
			self.assertEqual(legacy_status, "OPEN")
			self.assertEqual([event["event_type"] for event in events], ["SENT", "CLOSED"])
			self.assertEqual(events[-1]["details"]["commission"], -0.1)

	def test_reconcile_waits_for_broker_close_deal(self):
		manager = OrderManager.__new__(OrderManager)
		manager.symbol = "XAUUSDm"
		manager.mt5 = SimpleNamespace(
			today_realized_pnl=lambda: 0.0,
			get_equity=lambda: 1000.0,
			get_positions=lambda _symbol: [],
			get_deals_for_position=lambda _ticket: [],
			get_orders_history=lambda count: [],
		)
		manager.daily_loss_limit_pct = 5.0
		manager.halt_new_orders = False
		manager.managed = {
			123: ManagedOrder(
				ticket=123,
				open_time=datetime.now(),
				entry=2700.0,
				sl=2690.0,
				tp=2720.0,
				direction=1,
				alert_level="LOW",
			)
		}
		manager.persistence = SimpleNamespace(update_trade=lambda *_args: self.fail("unconfirmed close must not be persisted"))

		manager.reconcile()

		self.assertIn(123, manager.managed)

	def test_reconcile_persists_confirmed_exit_fill_and_net_pnl(self):
		manager = OrderManager.__new__(OrderManager)
		manager.symbol = "XAUUSDm"
		deals = [
			SimpleNamespace(position_id=456, entry=0, ticket=900, price=100.0, volume=0.1, profit=0.0, commission=-0.1, swap=0.0, time=1, time_msc=1000),
			SimpleNamespace(position_id=456, entry=1, ticket=901, price=101.0, volume=0.1, profit=10.0, commission=-0.4, swap=-0.2, reason=2, time=2, time_msc=2000),
			SimpleNamespace(position_id=456, entry=1, ticket=902, price=102.0, volume=0.2, profit=20.0, commission=-0.5, swap=0.0, reason=2, time=3, time_msc=3000),
		]
		manager.mt5 = SimpleNamespace(
			today_realized_pnl=lambda: 0.0,
			get_equity=lambda: 1000.0,
			get_positions=lambda _symbol: [],
			get_deals_for_position=lambda _ticket: deals,
		)
		manager.daily_loss_limit_pct = 5.0
		manager.halt_new_orders = False
		manager.managed = {
			456: ManagedOrder(
				ticket=456,
				open_time=datetime.now(),
				entry=100.0,
				sl=90.0,
				tp=120.0,
				direction=1,
				alert_level="LOW",
			)
		}
		updates = []
		manager.persistence = SimpleNamespace(update_trade=lambda ticket, fields: updates.append((ticket, fields.copy())))

		manager.reconcile()

		self.assertNotIn(456, manager.managed)
		self.assertEqual(updates[0][0], 456)
		self.assertEqual(updates[0][1]["status"], "CLOSED")
		self.assertAlmostEqual(updates[0][1]["close_price"], 101.6666667)
		self.assertAlmostEqual(updates[0][1]["pnl"], 28.8)
		self.assertEqual(updates[0][1]["close_deal_id"], 902)


if __name__ == "__main__":
	unittest.main()
