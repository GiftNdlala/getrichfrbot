"""
Backfill missing close_price values in trades.sqlite by using stored PnL.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "trades.sqlite"


def compute_close_price(direction: int, entry: float, lots: float, pnl: float) -> float | None:
	if direction not in (1, -1):
		return None
	if lots in (None, 0):
		lots = 0.01
	if not entry and entry != 0:
		return None
	try:
		price_delta = pnl / (lots * 100.0)
		if direction == 1:
			return entry + price_delta
		return entry - price_delta
	except Exception:
		return None


def backfill() -> None:
	if not DB_PATH.exists():
		print(f"Database not found at {DB_PATH}")
		return

	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row

	rows = conn.execute(
		"""
		SELECT ticket, direction, entry, lots, pnl
		FROM trades
		WHERE status = 'CLOSED'
		  AND (close_price IS NULL OR close_price = '')
		  AND pnl IS NOT NULL
		"""
	).fetchall()

	if not rows:
		print("No trades require backfill.")
		conn.close()
		return

	updated = 0
	for row in rows:
		try:
			direction = row["direction"]
			entry = row["entry"]
			lots = row["lots"]
			pnl = row["pnl"]
			if pnl is None:
				continue
			close_price = compute_close_price(direction, entry, lots, pnl)
			if close_price is None:
				continue
			conn.execute(
				"UPDATE trades SET close_price = ? WHERE ticket = ?",
				(close_price, row["ticket"]),
			)
			updated += 1
		except Exception:
			continue

	conn.commit()
	conn.close()
	print(f"Backfilled close_price for {updated} trade(s).")


if __name__ == "__main__":
	backfill()

