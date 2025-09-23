import os
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'trades.sqlite')


class PersistenceManager:
	def __init__(self, db_path: str = DB_PATH):
		self.db_path = db_path
		self._ensure_db()

	def _ensure_db(self):
		dirname = os.path.dirname(self.db_path)
		os.makedirs(dirname, exist_ok=True)
		with sqlite3.connect(self.db_path) as conn:
			conn.execute(
				"""
				CREATE TABLE IF NOT EXISTS signals (
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
			conn.execute(
				"""
				CREATE TABLE IF NOT EXISTS trades (
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
			conn.commit()

	def save_signal(self, data: Dict[str, Any]) -> None:
		# Accept dict-like LiveSignal
		with sqlite3.connect(self.db_path) as conn:
			columns = [
				'timestamp','symbol','current_price','signal','signal_type','confidence','rsi','macd','macd_signal',
				'sma_20','sma_50','price_change','price_change_pct','alert_level','alert_color','target_pips','success_rate',
				'entry_price','stop_loss','take_profit_1','take_profit_2','take_profit_3','risk_reward_ratio','atr_value',
				'position_size_percent','risk_amount_dollars','potential_profit_tp1','potential_profit_tp2','potential_profit_tp3'
			]
			placeholders = ','.join(['?']*len(columns))
			values = [data.get(col) for col in columns]
			conn.execute(f"INSERT INTO signals ({','.join(columns)}) VALUES ({placeholders})", values)
			conn.commit()

	def save_trade(self, trade: Dict[str, Any]) -> None:
		with sqlite3.connect(self.db_path) as conn:
			columns = ['timestamp','symbol','direction','entry','sl','tp','lots','ticket','status']
			values = [trade.get(c) for c in columns]
			placeholders = ','.join(['?']*len(columns))
			conn.execute(f"INSERT INTO trades ({','.join(columns)}) VALUES ({placeholders})", values)
			conn.commit()

	def latest_signal(self) -> Optional[Dict[str, Any]]:
		with sqlite3.connect(self.db_path) as conn:
			conn.row_factory = sqlite3.Row
			row = conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 1").fetchone()
			return dict(row) if row else None

	def recent_signals(self, limit: int = 10) -> List[Dict[str, Any]]:
		with sqlite3.connect(self.db_path) as conn:
			conn.row_factory = sqlite3.Row
			rows = conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
			return [dict(r) for r in rows]