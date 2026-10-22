import os
import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from uuid import uuid4

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'trades.sqlite')


class PersistenceManager:
	def __init__(self, db_path: str = DB_PATH):
		self.db_path = db_path
		self._ensure_db()
		self._migrate_db()

	def _ensure_db(self):
		dirname = os.path.dirname(self.db_path)
		os.makedirs(dirname, exist_ok=True)
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.execute("PRAGMA journal_mode=WAL")
			conn.execute("PRAGMA busy_timeout=15000")
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
					potential_profit_tp3 REAL,
					signal_id TEXT,
					data_source TEXT,
					bid REAL,
					ask REAL,
					point REAL,
					spread_points REAL
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
					status TEXT,
					signal_id TEXT,
					signal_price REAL,
					fill_price REAL,
					data_source TEXT,
					bid REAL,
					ask REAL,
					point REAL,
					spread_points REAL,
					setup_id TEXT,
					magic INTEGER,
					order_comment TEXT,
					open_deal_id INTEGER,
					close_deal_id INTEGER,
					commission REAL,
					swap REAL,
					updated_at TEXT
				)
				"""
			)
			conn.execute(
				"""
				CREATE TABLE IF NOT EXISTS trade_events (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					ticket INTEGER NOT NULL,
					event_type TEXT NOT NULL,
					timestamp TEXT NOT NULL,
					details_json TEXT NOT NULL
				)
				"""
			)
			conn.commit()

	def _migrate_db(self):
		"""Add new lifecycle columns if missing"""
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			# ---- trades table migrations ----
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
				'tier': 'TEXT',
				'engine': 'TEXT',
				'signal_id': 'TEXT',
				'signal_price': 'REAL',
				'fill_price': 'REAL',
				'data_source': 'TEXT',
				'bid': 'REAL',
				'ask': 'REAL',
				'point': 'REAL',
				'spread_points': 'REAL',
				'setup_id': 'TEXT',
				'magic': 'INTEGER',
				'order_comment': 'TEXT',
				'open_deal_id': 'INTEGER',
				'close_deal_id': 'INTEGER',
				'commission': 'REAL',
				'swap': 'REAL',
				'updated_at': 'TEXT'
			}
			for col, col_type in columns_to_add.items():
				if col not in existing_cols:
					conn.execute(f"ALTER TABLE trades ADD COLUMN {col} {col_type}")

			# ---- signals table migrations (quality metrics) ----
			existing_signal_cols = {}
			for row in conn.execute("PRAGMA table_info(signals)").fetchall():
				existing_signal_cols[row[1]] = True
			signal_columns_to_add = {
				'signal_strength': 'REAL',
				'signal_vote_sum': 'REAL',
				'signal_pos_votes': 'INTEGER',
				'signal_neg_votes': 'INTEGER',
				'signal_total_votes': 'INTEGER',
				'signal_id': 'TEXT',
				'data_source': 'TEXT',
				'bid': 'REAL',
				'ask': 'REAL',
				'point': 'REAL',
				'spread_points': 'REAL',
			}
			for col, col_type in signal_columns_to_add.items():
				if col not in existing_signal_cols:
					conn.execute(f"ALTER TABLE signals ADD COLUMN {col} {col_type}")
			conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_ticket ON trades(ticket)")
			conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_signal_id ON trades(signal_id)")
			conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_events_ticket ON trade_events(ticket, id)")
			conn.commit()

	def save_signal(self, data: Dict[str, Any]) -> str:
		# Accept dict-like LiveSignal
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			columns = [
				'timestamp','symbol','current_price','signal','signal_type','confidence','rsi','macd','macd_signal',
				'sma_20','sma_50','price_change','price_change_pct','alert_level','alert_color','target_pips','success_rate',
				'entry_price','stop_loss','take_profit_1','take_profit_2','take_profit_3','risk_reward_ratio','atr_value',
				'position_size_percent','risk_amount_dollars','potential_profit_tp1','potential_profit_tp2','potential_profit_tp3',
				'signal_strength','signal_vote_sum','signal_pos_votes','signal_neg_votes','signal_total_votes',
				'signal_id','data_source','bid','ask','point','spread_points'
			]
			signal_id = str(data.get('signal_id') or uuid4())
			data['signal_id'] = signal_id
			placeholders = ','.join(['?']*len(columns))
			values = [data.get(col) for col in columns]
			conn.execute(f"INSERT INTO signals ({','.join(columns)}) VALUES ({placeholders})", values)
			conn.commit()
			return signal_id

	def save_trade(self, trade: Dict[str, Any]) -> None:
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			# Insert with dynamic columns (only ones present in table)
			conn.row_factory = sqlite3.Row
			table_cols = [r['name'] for r in conn.execute("PRAGMA table_info(trades)").fetchall()]
			cols = [c for c in trade.keys() if c in table_cols]
			placeholders = ','.join(['?']*len(cols))
			values = [trade.get(c) for c in cols]
			conn.execute(f"INSERT INTO trades ({','.join(cols)}) VALUES ({placeholders})", values)
			ticket = trade.get('ticket')
			if ticket is not None:
				self._insert_trade_event(
					conn,
					int(ticket),
					str(trade.get('status') or 'RECORDED').upper(),
					trade,
				)
			conn.commit()

	@staticmethod
	def _insert_trade_event(conn, ticket: int, event_type: str, details: Dict[str, Any]) -> None:
		conn.execute(
			"INSERT INTO trade_events (ticket, event_type, timestamp, details_json) VALUES (?, ?, ?, ?)",
			(
				ticket,
				event_type,
				datetime.now(timezone.utc).isoformat(),
				json.dumps(details, default=str, sort_keys=True),
			),
		)

	def update_trade(self, ticket: int, fields: Dict[str, Any]) -> None:
		if not fields:
			return
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			fields['updated_at'] = datetime.now(timezone.utc).isoformat()
			set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
			values = list(fields.values()) + [ticket]
			conn.execute(f"UPDATE trades SET {set_clause} WHERE ticket = ?", values)
			self._insert_trade_event(
				conn,
				ticket,
				str(fields.get('status') or 'UPDATED').upper(),
				fields,
			)
			conn.commit()

	def get_open_trades(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.row_factory = sqlite3.Row
			if symbol:
				rows = conn.execute("SELECT * FROM trades WHERE status IN ('SENT','OPEN') AND symbol = ?", (symbol,)).fetchall()
			else:
				rows = conn.execute("SELECT * FROM trades WHERE status IN ('SENT','OPEN')").fetchall()
			return [dict(r) for r in rows]

	def get_trade_events(self, ticket: int) -> List[Dict[str, Any]]:
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.row_factory = sqlite3.Row
			rows = conn.execute(
				"SELECT id, ticket, event_type, timestamp, details_json FROM trade_events WHERE ticket = ? ORDER BY id",
				(ticket,),
			).fetchall()
			events = []
			for row in rows:
				event = dict(row)
				event['details'] = json.loads(event.pop('details_json'))
				events.append(event)
			return events

	def recent_trades(self, hours: int = 20, limit: int = 200) -> List[Dict[str, Any]]:
		"""Return trades within the last N hours (open or closed)."""
		cutoff = (datetime.utcnow() - datetime.timedelta(hours=hours)) if hasattr(datetime, 'timedelta') else None
		# Build cutoff string; if datetime.timedelta not available for some reason, default to 20h ago
		from datetime import datetime as _dt, timedelta as _td
		cutoff_dt = _dt.utcnow() - _td(hours=hours)
		cutoff_str = cutoff_dt.strftime('%Y-%m-%d %H:%M:%S')
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.row_factory = sqlite3.Row
			rows = conn.execute(
				"SELECT * FROM trades WHERE timestamp >= ? ORDER BY timestamp DESC LIMIT ?",
				(cutoff_str, limit)
			).fetchall()
			return [dict(r) for r in rows]

	def latest_signal(self) -> Optional[Dict[str, Any]]:
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.row_factory = sqlite3.Row
			row = conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 1").fetchone()
			return dict(row) if row else None

	def recent_signals(self, limit: int = 10) -> List[Dict[str, Any]]:
		with sqlite3.connect(self.db_path, timeout=15.0) as conn:
			conn.row_factory = sqlite3.Row
			rows = conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
			return [dict(r) for r in rows]