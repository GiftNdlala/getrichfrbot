# Open questions and answers from the repo

This section answers the questions in the audit brief using the current repo snapshot.

## 1. Where is `live_signal.stop_loss` computed?

It is computed in `src/live_data_stream.py:LiveDataStream._calculate_risk_management()`.

Relevant logic:
- reads `ATR_14` from `latest_data`
- uses the alert category (`HIGH`, `MEDIUM`, `LOW`)
- derives `entry_price`, `stop_loss`, and `take_profit_1` from `current_price` and the ATR value
- uses the latest row in the in-memory OHLC dataset, not a fixed broker snapshot

Code evidence: `src/live_data_stream.py:918-1004`.

## 2. Which price does MT5 return, and what is `spread_points`?

`src/mt5_connector.py:get_current_quote()` does:
- prefer `tick.last` if available
- otherwise use `tick.bid`/`tick.ask`
- compute `prev_close` from the last 3 M1 bars
- compute `spread = (tick.ask - tick.bid) / point`

So `spread_points` is a point-based spread value, not a pips value. The scale depends on the symbol's `point` from `mt5.symbol_info(self.symbol)`. For XAUUSDm, that value must be checked against the broker symbol metadata; the repo does not hardcode it.

Code evidence: `src/mt5_connector.py:99-129`.

## 3. What is the poll interval and what feed do the indicators use?

- Default `update_interval` is 30 seconds (`LiveDataStream.__init__(symbol='XAUUSD', update_interval=30)`).
- It does not appear to poll a strict M1 history feed at the strategy level; it polls a current quote and then appends a one-row OHLC bar into `historical_data`.
- The strategy indicators (`RSI_14`, `SMA_200`, `ATR_14`) are then calculated on that in-memory bar stream.

Code evidence: `src/live_data_stream.py:150-206`, `src/live_data_stream.py:749-782`, `src/indicators.py:258-312`.

## 4. Does anything enforce `max_concurrent_trades`, `max_open_risk_pct`, or call `get_position_size_multiplier()`?

Not in the live code path.

- `max_concurrent_trades` is loaded into config but not used in enforcement logic.
- `max_open_risk_pct` is stored on `OrderManager` but not checked before order placement.
- `get_position_size_multiplier()` exists, but no call site was found in the repo path for runtime trading.

Code evidence: `config.json:5-30`, `src/order_manager.py:76-90`, `src/order_manager.py:320-390`.

## 5. What `alert_level` is passed to `register_new_order()`, and which time cap applies?

In the current repo, different engines pass different `alert_level` strings:

- `EVENT` -> `self.order_manager.register_new_order(..., 'EVENT', tier='EVENT')`
- `ICT_ATM` -> `'ICT_ATM'`
- `ICT_SWING_*` -> `'ICT_SWING_{session}'`
- NYUPIP uses its own signal module / strategy context

`OrderManager._apply_exit_rules()` uses `max_position_minutes` keyed on `alert_level`, but `ICT_ATM` is not in the config map. That means it falls back to the default `10` minutes.

Code evidence: `src/live_data_stream.py:1308-1316`, `src/live_data_stream.py:2231-2393`, `src/order_manager.py:224-257`.

## 6. Are `engine_mode`, `enable_high`, `farmer_enabled`, and NYUPIP guard states what the config says?

- `enable_high` defaults to `False` in `LiveDataStream.__init__()`.
- `farmer_enabled` is loaded from config and set in `__init__()`.
- `strategy_guards` values are loaded from `config.json` and are explicitly false in the current config.
- `engine_mode` is a runtime property, not a direct config-only property, and it is not obviously stored in the config file itself.

Code evidence: `config.json:70-95`, `src/live_data_stream.py:156-181`, `src/live_data_stream.py:1355-1410`.

## 7. Why did NYUPIP, ICT Swing and FARMER not trade?

The repo does not show them trading in the current default runtime state for several reasons:

- `enable_high` is default false and the engines are explicitly gated by engine mode.
- Sessions and blackout logic are checked before entry.
- `strategy_guards.nyupip_active_window_enabled` and `nyupip_extra_order_gate_enabled` are false in config.
- The code path for FARMER is present but the flow is a separate engine path and not enabled by default in the same way as the general stream.

This is not a proof that the engine cannot trade; it is evidence that the default runtime state is not set to trade every strategy on every loop.

## 8. How does `CampaignManager` get `min_spacing_seconds`?

`CampaignManager.__init__` accepts `min_spacing_seconds` and defaults to 60 seconds.

The live stream passes `min_seconds_between_entries` from the config into the campaign manager in `LiveDataStream.__init__()`.

Code evidence: `src/order_manager.py:30-45`, `src/live_data_stream.py:165-181`.

## 9. What does `today_realized_pnl` include?

It sums `deal.profit` for the current symbol over the current local day. It does not appear to sum floating P&L, swaps, or commission in the method itself.

Code evidence: `src/mt5_connector.py:198-218`.

## 10. Is there any mechanism to stop the bot if all real quote sources fail?

No hard-stop mechanism is visible. The fallback path logs a warning and then generates a synthetic mock quote. That synthetic quote does not carry a spread field, and the code does not reject it on source.

Code evidence: `src/live_data_stream.py:636-757`.

## 11. Where is `demo_only` read, and is there any account-type check?

`demo_only` is in `config.json` and is loaded as part of the runtime config. The repo does not show a runtime check that the connected account is an actual demo account before trading.

Code evidence: `config.json:112-119`, `src/config.py:17-43`.

## 12. What resets after a restart?

The repo keeps runtime state in memory:
- `self.managed` in `OrderManager`
- `self.campaign.events` and `self.campaign.last_time`
- `self.halt_new_orders`
- `self._farmer_last_cycle`

These are not restored from disk on restart. That means a fresh process can lose entry-state continuity and risk gating continuity.

Code evidence: `src/order_manager.py:62-90`, `src/live_data_stream.py:156-181`.

## 13. Is there a test suite or backtest harness?

I do not see a dedicated `tests/` suite or a general backtest harness in the repo snapshot. There are strategy documents and summary notes, but not a clear automated replay suite for the live strategies.

## 14. Where are trades persisted, and is that a source of truth?

Trades and signals are persisted in SQLite via `src/persistence.py`, with database path `data/trades.sqlite`.

This is a useful local audit trail, but it is not a direct replacement for the broker export or the live MT5 trade history because it lacks some broker-level metadata by default (for example, not every order record captures spread, source, and signal IDs in a uniform, guaranteed way).

Code evidence: `src/persistence.py:1-170`.
