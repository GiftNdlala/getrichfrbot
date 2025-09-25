import os
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'trades.sqlite')


class PersistenceManager:
	def __init__(self, db_path: str = DB_PATH):
		self.db_path = db_path
		self._ensure_db()
		self._migrate_db()

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

	def _migrate_db(self):
		"""Add new lifecycle columns if missing"""
		with sqlite3.connect(self.db_path) as conn:
			existing_cols = {}
			for row in conn.execute("PRAGMA table_info(trades)").fetchall():
				existing_cols[row[1]] = True
			# Columns to add
			columns_to_add = {
				'open_time': 'TEXT',
				'close_time': 'TEXT',
				'close_price': 'REAL',
				'pnl': 'REAL',
				'pnl_r': 'REAL',
				'reason': 'TEXT',
				'alert_level': 'TEXT',
				'campaign_id': 'TEXT',
				'tier': 'TEXT'
			}
			for col, col_type in columns_to_add.items():
				if col not in existing_cols:
					try:
						conn.execute(f"ALTER TABLE trades ADD COLUMN {col} {col_type}")
					except Exception:
						pass
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
			# Insert with dynamic columns (only ones present in table)
			conn.row_factory = sqlite3.Row
			table_cols = [r['name'] for r in conn.execute("PRAGMA table_info(trades)").fetchall()]
			cols = [c for c in trade.keys() if c in table_cols]
			placeholders = ','.join(['?']*len(cols))
			values = [trade.get(c) for c in cols]
			conn.execute(f"INSERT INTO trades ({','.join(cols)}) VALUES ({placeholders})", values)
			conn.commit()

	def update_trade(self, ticket: int, fields: Dict[str, Any]) -> None:
		with sqlite3.connect(self.db_path) as conn:
			if not fields:
				return
			set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
			values = list(fields.values()) + [ticket]
			conn.execute(f"UPDATE trades SET {set_clause} WHERE ticket = ?", values)
			conn.commit()

	def get_open_trades(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
		with sqlite3.connect(self.db_path) as conn:
			conn.row_factory = sqlite3.Row
			if symbol:
				rows = conn.execute("SELECT * FROM trades WHERE status IN ('SENT','OPEN') AND symbol = ?", (symbol,)).fetchall()
			else:
				rows = conn.execute("SELECT * FROM trades WHERE status IN ('SENT','OPEN')").fetchall()
			return [dict(r) for r in rows]

	def recent_trades(self, hours: int = 20, limit: int = 200) -> List[Dict[str, Any]]:
		"""Return trades within the last N hours (open or closed)."""
		cutoff = (datetime.utcnow() - datetime.timedelta(hours=hours)) if hasattr(datetime, 'timedelta') else None
		# Build cutoff string; if datetime.timedelta not available for some reason, default to 20h ago
		from datetime import datetime as _dt, timedelta as _td
		cutoff_dt = _dt.utcnow() - _td(hours=hours)
		cutoff_str = cutoff_dt.strftime('%Y-%m-%d %H:%M:%S')
		with sqlite3.connect(self.db_path) as conn:
			conn.row_factory = sqlite3.Row
			rows = conn.execute(
				"SELECT * FROM trades WHERE timestamp >= ? ORDER BY timestamp DESC LIMIT ?",
				(cutoff_str, limit)
			).fetchall()
			return [dict(r) for r in rows]

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