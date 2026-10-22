# Architecture map

This is a code-only map of the system as it exists in the current repo. It is not a runtime or broker-level audit.

## 1. Config and runtime bootstrap

- Config is loaded from `config.json` via `src/config.py:get_config()`.
- The active runtime config is then used by:
  - `src/live_data_stream.py:LiveDataStream.__init__()`
  - `src/order_manager.py:OrderManager.__init__()`
  - `src/executor.py:AutoTrader.__init__()`
- Config keys used directly by the runtime include:
  - `execution.enabled`, `execution.demo_only`
  - `execution.campaign_window_minutes`, `execution.min_seconds_between_entries`, `execution.campaign_max_trades`, `execution.max_position_minutes`
  - `execution.high_tier_tp_pips`, `execution.farmer`, `execution.loss_minimizer`
  - `filters.max_spread_points`, `filters.quality_gates`
  - `risk.risk_percent_per_trade`, `risk.max_concurrent_trades`, `risk.symbol_caps`, `risk.progressive_defense`
  - `strategy_guards.*`, `sessions.*`, `news.*`

## 2. Quote-to-signal data flow

1. `LiveDataStream.start_streaming()` creates the loop in `src/live_data_stream.py`.
2. Each tick, `stream_loop` runs `self._fetch_current_quote()`.
3. `self._fetch_current_quote()` tries MT5 first, then backup real feeds, then the final fallback: `_generate_realistic_quote()`.
4. The quote is passed through the spread / ATR gate, then appended to `historical_data` by `_update_historical_data()`.
5. Indicators are recalculated with `TechnicalIndicators.calculate_all_indicators()` from `src/indicators.py`.
6. `self._generate_live_signal(current_quote)` emits a `LiveSignal` containing entry, SL, TP and alert category.
7. `self._notify_callbacks(live_signal)` pushes the signal to any listeners.
8. The stream decides whether an engine can enter an order.

## 3. Engine-to-order flow

The main auto-trade path is in `src/live_data_stream.py`.

- `EVENT` path: `self.event_engine.try_detect_spike(...)` and `self.autotrader.place_market_order(...)`
- `NYUPIP` path: `self._process_nyupip_signal(...)`
- `ICT Swing` path: `self._process_ict_swing_signal(...)`
- `ICT ATM` path: `self._process_ict_atm_signal(...)`
- High/medium/low path: the `stream_loop` auto-trading block decides if `live_signal.alert_level` is enabled and then calls `place_market_order(...)`

All placements ultimately hit `src/executor.py:AutoTrader.place_market_order()` and `_place_market_order_locked()`.

## 4. What writes the tag / magic number

Order comments are assembled in `src/executor.py:AutoTrader._order_comment()`.

- Base prefix: `GetRichFR`
- Strategy tag is sanitized and truncated to 13 characters
- Magic number is hardcoded as `20250923`

This means the live MT5 order comment is effectively `GetRichFR_` + a short sanitized engine tag, and the order is not unique by strategy.

## 5. Exit management and state tracking

The live position manager is `src/order_manager.py:OrderManager`.

- `register_new_order()` creates a `ManagedOrder` record and writes status `OPEN`
- `reconcile()` polls MT5 positions and applies exit logic
- `_apply_exit_rules()` enforces:
  - breakeven move at 1R
  - time limit by `execution.max_position_minutes`
  - loss minimizer logic in `_try_loss_minimizer()`
- `self.managed` is the live open-order registry
- `self.halt_new_orders` is toggled when the daily loss cap is reached

## 6. Where the code reads config keys

The key-read locations are clustered as follows:

- `src/live_data_stream.py`
  - `self.config.get('execution', {})`
  - `self.config.get('filters', {})`
  - `self.config.get('sessions', {})`
  - `self.config.get('strategy_guards', {})`
- `src/order_manager.py`
  - `risk.symbol_caps`
  - `risk.progressive_defense`
  - `execution.loss_minimizer`
  - `execution.max_position_minutes`
  - `risk.move_sl_to_be_after_r_multiple`
- `src/executor.py`
  - `risk.risk_percent_per_trade`
  - `execution.deviation_points`
  - `execution.enabled`

## 7. Key architecture issue

The system is not a single, strict “one signal -> one strategy -> one governed order” pipeline. It is a mixed engine:

- a price stream,
- multiple strategy engines,
- an order-placement layer,
- and a separate position management layer.

The operational risk is that different engines use different gates and different defaults, while the final order executor does not consistently enforce cross-engine caps or a single risk model.
