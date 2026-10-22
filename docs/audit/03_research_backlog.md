# Research backlog

This is the refined backlog that fits the code as it currently exists.

## 1. Entry-quality and random-entry baseline

Goal: determine whether the strategy's positive/negative drift is attributable to the signal engine or simply to the frequency of entry.

- Replay a random-entry baseline against the same trade frequency and exit policy.
- Check whether `HIGH` and `ICT_ATM` lose money even when entries are random.

Acceptance test: a replay notebook or script produces a distribution of P&L for random and real entries under the exact same exit rules.

## 2. Fill-price and slippage study

Goal: convert signal-price assumptions into actual fill-price realities.

- Capture bid/ask at order time and compare to signal price.
- Measure directional slippage and cost per trade.

Acceptance test: each order record includes signal price, fill price, bid, ask, and spread.

## 3. Exit-rule stress test

Goal: answer whether the exit logic is killing performance.

- Replay with and without the 10-minute default time stop.
- Replay with breakeven enabled/disabled.
- Replay with loss minimizer enabled/disabled.

Acceptance test: a single script produces a side-by-side summary across exit modes.

## 4. Campaign-cap and stacking review

Goal: identify whether stacking is a strategy feature or a bug.

- Compare results by unique setup versus repeated identical entries.
- Check whether repeated trades under the same bucket are producing a real edge or just repeated noise.

Acceptance test: counts by strategy + setup + direction + close reason are logged and summarized.

## 5. Risk gate verification

Goal: confirm whether risk caps are real or inert.

- Verify `max_concurrent_trades` enforcement.
- Verify `max_open_risk_pct` enforcement.
- Verify `get_position_size_multiplier` call path.

Acceptance test: an order is blocked when the cap would be exceeded, and the values are logged.

## 6. Data-source integrity check

Goal: confirm whether the bot is trading on synthetic or real data during failures.

- Log source for every quote and every trade.
- Count fallback and mock usage.
- Fail closed if all real sources fail.

Acceptance test: there is a source field in the order record and the platform blocks trading when no real source is viable.

## 7. Timezone and session consistency

Goal: ensure all strategy windows and trade filters operate on the same time basis.

- Normalise all timestamps to UTC on ingest.
- Verify session logic against the chosen timezone.
- Recheck DST-sensitive windows.

Acceptance test: a single time conversion utility is used consistently across the repo.

## 8. Observability and attribution

Goal: make the export trustworthy.

- Use non-truncated order comments.
- Add a unique `signal_id` to every order.
- Add a `data_source` and `spread_points` field to every trade record.

Acceptance test: a replay script can trace a trade back to the exact signal that opened it.
