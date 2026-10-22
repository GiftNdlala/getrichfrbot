# Findings

This audit is limited to the repo snapshot and the code paths visible in it. It does not rely on live MT5 access or a broker export.

## F1 — INTRADAY_HIGH has negative expectancy and fires repeatedly

Verdict: CONFIRMED
Evidence labels: DATA + CODE

- DATA: the brief documents a negative net outcome for the `GetRichFR_INTRADAY_HIGH` label. The repo itself does not contain the trade export, so the numbers are externally supplied, but the code path matches the described engine.
- CODE: `src/live_data_stream.py` creates an auto-trade path for any non-zero signal when `trading_enabled` is true and `enable_high` is true. The stream assigns alert level `HIGH`, then routes to the main order path.
- File evidence: `src/live_data_stream.py:1290-1427` and `src/executor.py:153-260`.
- Risk implication: the system is designed to generate repeated high-tier entries, and the order manager can track them as open positions without a strong cross-engine cap.

## F2 — ICT_ATM exits at the default 10-minute timeout

Verdict: CONFIRMED
Evidence labels: CODE

- `src/order_manager.py:_apply_exit_rules()` does:
  - `max_minutes_map = exec_cfg.get('max_position_minutes', {'LOW':10,'MEDIUM':10,'HIGH':20})`
  - `max_age = timedelta(minutes=int(max_minutes_map.get(alert, 10)))`
- `ICT_ATM` is registered with `alert_level='ICT_ATM'` in `src/live_data_stream.py:_process_ict_atm_signal()`.
- Because `ICT_ATM` is not present in `max_position_minutes`, the code falls back to `10` minutes.
- File evidence: `src/order_manager.py:224-257`, `src/live_data_stream.py:2334-2393`.

## F3 — ICT_ATM can stack repeated identical trades

Verdict: CONFIRMED
Evidence labels: CODE

- In `src/live_data_stream.py:_process_ict_atm_signal()`, the bucket is `HIGH_ATM` and the campaign is checked with `self.campaign.allow(self.symbol, signal.direction, atm_bucket)`.
- The strategy itself has no per-setup cooldown; `NYUPIP` is the one with a cooldown field, not ICT ATM.
- File evidence: `src/live_data_stream.py:2334-2393`, `src/strategies/nyupip.py:26-33`.
- The code therefore supports repeated entries under the same pattern bucket until the campaign bucket limit is hit.

## F4 — Position and risk caps are not enforced in practice

Verdict: CONFIRMED
Evidence labels: CODE

- `config.json` contains `risk.max_concurrent_trades: 1` and `risk.symbol_caps.XAUUSDm.max_open_risk_pct: 50.0`.
- `src/order_manager.py:OrderManager.__init__()` reads both values but never uses them to block new orders.
- `src/order_manager.py:get_position_size_multiplier()` exists, but the repo search shows no call site in the trading path.
- `record_trade_closure()` exists but is not used by the live flow.
- File evidence: `config.json:5-30`, `src/order_manager.py:76-90`, `src/order_manager.py:320-390`.

## F5 — The practical hard ceiling is effectively 1.0 lot in the executor

Verdict: CONFIRMED
Evidence labels: CODE

- `src/executor.py:_max_affordable_lot()` sets `hi = max(min(max_lot, min_lot * 100), min_lot)` and searches a bounded lot range.
- In normal MT5 gold settings, `min_lot` is often `0.01`, which makes the search window effectively limited to a maximum of around `1.0` lot.
- The placement path also clamps the order size to the affordable result.
- File evidence: `src/executor.py:78-113`, `src/executor.py:153-260`.

## F6 — Stops, targets and breakeven are anchored to signal price, not fill price

Verdict: CONFIRMED
Evidence labels: CODE

- `src/executor.py:AutoTrader._place_market_order_locked()` computes `market_price` from the live tick and then calculates `lots = self._calc_lot(entry, sl)` based on the strategy entry and stop, not the actual fill price.
- `src/order_manager.py:_apply_exit_rules()` computes `be_price = st.entry + buffer` using the original `st.entry` state, not the actual fill price.
- That means the breakeven adjustment is based on the signal snapshot rather than the trade fill.
- File evidence: `src/executor.py:159-226`, `src/order_manager.py:232-257`.

## F7 — A failed time-stop close can still be marked as closed

Verdict: CONFIRMED
Evidence labels: CODE

- In `src/order_manager.py:_apply_exit_rules()`, the code calls `close_position()` and then immediately writes `status: 'CLOSED'` and removes the order from `managed` regardless of whether the close succeeded.
- There is also a bare `except Exception: return`, which suppresses failure details.
- File evidence: `src/order_manager.py:230-257` and `src/order_manager.py:287-319`.

## F8 — Synthetic fallback quotes can feed signals and bypass spread checks

Verdict: CONFIRMED
Evidence labels: CODE

- `src/live_data_stream.py:_fetch_current_quote()` falls back to `_generate_realistic_quote()` when all real sources fail.
- `_generate_realistic_quote()` generates a synthetic price with `source: 'Realistic Mock'` and no `spread_points` field.
- The pre-trade guard only checks `if spread_points is not None`, so the synthetic quote is never rejected on spread.
- File evidence: `src/live_data_stream.py:636-757` and `src/live_data_stream.py:1223-1246`.

## F9 — Trade-gate `continue` statements can skip reconcile/wait on a signal loop

Verdict: CONFIRMED
Evidence labels: CODE

- The `continue` statements occur inside the auto-trading branch, after its outer guard has established an enabled executor, trading enabled, a non-zero signal, an open session, and no spread/ATR/event block.
- In those branches the loop jumps upward before `reconcile()` and before the sleep/wait phase. The next loop may still reach reconciliation if it does not hit a `continue`; therefore the halt flag is not necessarily stuck indefinitely.
- File evidence: `src/live_data_stream.py:1335-1427` and `src/live_data_stream.py:1710-1737`.

## F10 — Gate logic is inconsistent across engines

Verdict: CONFIRMED
Evidence labels: CODE

- `OrderManager.can_place_order()` exists and includes spread/chop/news/halt checks.
- The repo search shows it is called in the NYUPIP path only, not in the general LIVE signal path.
- The high/medium/low and ICT paths each use their own local checks and not the shared order gate.
- File evidence: `src/order_manager.py:344-390`, `src/live_data_stream.py:1964-2010`.

## F11 — Config and code key mismatches are real

Verdict: CONFIRMED
Evidence labels: CODE

- `config.json` contains `risk.move_sl_to_be_after_tp1`, but `src/order_manager.py:_apply_exit_rules()` reads `risk.move_sl_to_be_after_r_multiple`.
- `risk.max_concurrent_trades` is defined in config but not enforced in code.
- `max_open_risk_pct` is loaded and stored, but not used by the order placement path.
- File evidence: `config.json:6-30`, `src/order_manager.py:76-90`, `src/order_manager.py:232-246`.

## F12 — Tagging is lossy and incomplete

Verdict: CONFIRMED
Evidence labels: CODE

- `src/executor.py:AutoTrader._order_comment()` trims the strategy tag to 13 characters.
- The code uses a single fixed magic number, `20250923`.
- This makes strategy attribution in the broker export inherently lossy.
- File evidence: `src/executor.py:63-76`, `src/executor.py:228-247`.

## H1 — NYUPIP compares UTC-naive M15 labels with a SAST-naive timestamp

Verdict: CONFIRMED
Evidence labels: CODE

- `_build_context()` strips timezone information from the history index, resamples that naive index, then converts the quote timestamp to `self.timezone` (Africa/Johannesburg by default) and strips its timezone for `m15_closed` comparisons.
- The history index is subsequently treated as UTC by `_convert_to_timezone()`. Consequently the M15 labels in `m15_closed` are UTC-naive while `current_ts` is SAST-naive (UTC+2 under the repo default).
- The right-labelled resample uses `label="right", closed="right"`. Even with aligned clocks, the code first keeps labels through `current_ts.floor("15min")` and then drops the row at that exact label; that row is the completed bar ending on the boundary, not the still-forming bar.
- This is a code-level timestamp/bar-selection defect; a replay is needed only to quantify its effect on signals.
- File evidence: `src/strategies/nyupip.py:160-220`, especially `_build_context()` and `_resample_ohlc()`.

## H2 — Hard-coded session windows are fixed to the configured local clock

Verdict: CONFIRMED
Evidence labels: CODE

- The default timezone is `Africa/Johannesburg` (SAST, UTC+2); `APP_TIMEZONE` can override it. The session windows are clock values, not conversions from `Europe/London` or `America/New_York`.
- Therefore, assuming the default timezone, their UTC conversions do not change across the 25 October 2026 UK DST transition or the 1 November 2026 US DST transition. The nominal London/NY labels do not move with those markets.
- The complete window inventory and UTC conversions are in “Second-pass answers” below.
- File evidence: `config.json:sessions`, `src/config.py:_merge_env()`, `src/strategies/ict_swing_points.py:80-100`, `src/strategies/nyupip.py:60-70`.

## H3 — ICT Swing OTE formulas accept 21–38% pullbacks

Verdict: CONFIRMED
Evidence labels: CODE + ARITHMETIC

- All four OTE calculations are constrained by `self.ote_range`, default `(0.62, 0.79)`.
- For bullish setups, the ratio measures progress upward from the low toward the impulse high; 62–79% progress leaves a 21–38% pullback from the high. For bearish setups, it measures progress downward from the high toward the impulse low; 62–79% progress leaves a 21–38% pullback upward from the low.
- Thus the implementation accepts 21–38% pullbacks, not 62–79% pullbacks. This arithmetic does not establish strategy profitability.
- File evidence: `src/strategies/ict_swing_points.py:340-470`.

## H4 — In-range ICT Swing OTE ratios always clear the 80 confidence gate

Verdict: CONFIRMED
Evidence labels: CODE + ARITHMETIC

- With the default OTE band `[0.62, 0.79]`, `ote_mid=(0.62+0.79)/2=0.705`. The confidence formula is `max(0, 100 - abs(ote_ratio - ote_mid) * 220)`.
- The maximum in-band distance from the midpoint is `0.085`, so the minimum confidence is `100 - 0.085*220 = 81.3`; the maximum is 100 at the midpoint.
- The evaluator treats confidence `>=60` as a HIGH signal, and its NY-open confirmation accepts confidence `>=80`; thus every in-range OTE signal clears both confidence thresholds. The remaining session-window filters still apply.
- File evidence: `src/strategies/ict_swing_points.py:208-243, 540-580`.

## H5 — NYUPIP CIS uses the previous calendar day, not previous trading day

Verdict: CONFIRMED
Evidence labels: CODE

- CIS sets `previous_day = now_sast.date() - timedelta(days=1)` and selects rows with exactly that calendar date.
- On Monday this means Sunday, not Friday. If there are no Sunday bars, the diagnostic reason is `no_previous_day_data`; if Sunday bars are present, CIS uses Sunday’s 13:00–21:00 SAST range as its prior-day NY session.
- This proves the calendar-day behavior; whether a particular Monday produced no order still depends on that run’s history, signal gates, and enabled state.
- File evidence: `src/strategies/nyupip.py:560-590`.

## H6 — London-close reversal confidence has a 94-point floor

Verdict: CONFIRMED
Evidence labels: CODE + ARITHMETIC

- The only London-close reversal callers require `range_position >= 0.85` for a short or `range_position <= 0.15` for a long.
- `_build_reversal_signal()` sets `extreme_bias` to `range_position` for shorts and `1-range_position` for longs, then computes `60 + extreme_bias*40`, clamped to `[0,100]`.
- Each caller therefore supplies `extreme_bias >=0.85`, giving a confidence floor of `60 + 0.85*40 = 94` (maximum 100). The post-filter still rejects generated signals outside its accepted time windows.
- File evidence: `src/strategies/ict_swing_points.py:483-525, 605-640`.

## H7 — ICT ATM H1 preparation may include unfinished candles

Verdict: CONFIRMED
Evidence labels: CODE

- The strategy resamples the input using `h1 = df.resample("1h", label="right", closed="right").agg(...)` and passes the resulting `h1` (including its final row) into ATR and pattern detection.
- There is no filter comparing the final H1 label with the current quote time and no drop-last operation. If the input history reaches into the current hour, that partial hour is included.
- Exact line: `src/strategies/ict_atm.py:219-226`.

## H8 — Indicator history is effectively a rolling synthetic bar stream

Verdict: CONFIRMED
Evidence labels: CODE

- `src/live_data_stream.py:_update_historical_data()` appends a one-row OHLC bar for every quote.
- `src/indicators.py:calculate_all_indicators()` recalculates RSI, SMA, ATR, etc. on that live stream.
- This means the indicator stream is not a strict M1 feed; it is a synthetic, quote-driven sequence.
- File evidence: `src/live_data_stream.py:749-782`, `src/indicators.py:258-312`.

## H9 — `today_realized_pnl` only sums realized P&L for the local day

Verdict: CONFIRMED
Evidence labels: CODE

- `src/mt5_connector.py:today_realized_pnl()` sums `deal.profit` for the current local day and the current symbol.
- It does not include floating P&L or swap/commission fields directly.
- File evidence: `src/mt5_connector.py:198-218`.

## H10 — Point scale in `deviation_points` and spread handling must be verified on the symbol

Verdict: CONFIRMED
Evidence labels: CODE

- `src/mt5_connector.py:get_current_quote()` computes `spread = (ask-bid) / point`.
- `src/executor.py` and `src/order_manager.py` also use MT5 point-based values.
- The correct scale depends on `mt5.symbol_info(self.symbol).point`; the repo does not hardcode it for XAUUSDm, so the actual meaning of a number like `40` must be checked against that symbol's metadata.
- File evidence: `src/mt5_connector.py:99-129`, `src/executor.py:177-199`.

## Second-pass answers

### 1. `_calculate_risk_management()` formulas and price-dollar offsets

For a non-zero signal, let `P=current_price`, `A=ATR_14` (invalid/non-positive values fall back to 20), and `T=alert_category["target_pips"]`. The function offsets these values directly from the XAU price; the resulting distances are price-dollar movements, not account-currency P&L.

| Side | Entry | Stop loss | TP1 | TP2 | TP3 |
|---|---|---|---|---|---|
| BUY | `P + 0.05A` | HIGH: `P - 2A`; MEDIUM: `P - 1.5A`; LOW: `P - A` | `P + T` | `P + 1.5T` | `P + 2T` |
| SELL | `P - 0.05A` | HIGH: `P + 2A`; MEDIUM: `P + 1.5A`; LOW: `P + A` | `P - T` | `P - 1.5T` | `P - 2T` |

The alert category’s caller derives `T` as `int(16+5*min(A/20,2))` for HIGH, `int(10+5*min(A/20,2))` for MEDIUM, and `int(5+3*min(A/20,2))` for LOW. Category selection additionally depends on confidence, RSI, and MACD. For A=1, 2, or 3, these yield HIGH `T=16`, MEDIUM `T=10`, LOW `T=5`.

Offsets from `P` at those ATR values are:

| A | Entry buffer | HIGH SL / TP1,TP2,TP3 | MEDIUM SL / TP1,TP2,TP3 | LOW SL / TP1,TP2,TP3 |
|---:|---:|---|---|---|
| 1 | 0.05 | 2 / 16, 24, 32 | 1.5 / 10, 15, 20 | 1 / 5, 7.5, 10 |
| 2 | 0.10 | 4 / 16, 24, 32 | 3 / 10, 15, 20 | 2 / 5, 7.5, 10 |
| 3 | 0.15 | 6 / 16, 24, 32 | 4.5 / 10, 15, 20 | 3 / 5, 7.5, 10 |

Those are magnitudes; BUY stops/targets are below/above `P` as shown in the formulas, and SELL signs reverse. Distance from the buffered entry to the stop is `(stop ATR multiple + 0.05)A`. For HOLD, entry, stop, and targets all equal `P`. The function’s separate risk/profit dollar estimates use an assumed $10,000 balance and an estimated position size; they are not a broker-calculated cash risk/profit guarantee.

For a selected category, the function's `risk_amount_dollars` field is independent of ATR: it is nominally `$150` HIGH, `$200` MEDIUM, or `$250` LOW (1.5%, 2%, or 2.5% of the assumed $10,000 balance, each below its `$500` cap). This is the reported risk budget, not an actual broker loss calculation.

### 2. Hard-coded session windows and UTC conversion

The table assumes the repo’s configured default `Africa/Johannesburg` timezone (SAST, UTC+2) and no `APP_TIMEZONE` override. Every UTC value shown applies before 25 October (e.g. 24 October), after 25 October but before 1 November (e.g. 26 October), and after 1 November 2026 (e.g. 2 November): Johannesburg does not observe DST. London/NY labels are not linked to London or New York time zones, so those labels shift relative to actual local market clocks when DST changes.

| Source / use | Local window (SAST unless noted) | UTC window |
|---|---|---|
| Configured overall trade window (`config.json`) | 00:01–23:59, Mon–Fri | 22:01 previous day–21:59 |
| `LiveDataStream` fallback if configured trade times are absent | 10:00–19:00 | 08:00–17:00 |
| ICT session slices: ASIA | 00:00–06:59 | 22:00 previous day–04:59 |
| ICT session slices: LONDON | 07:00–11:59 | 05:00–09:59 |
| ICT session slices: NEW_YORK | 12:00–15:59 | 10:00–13:59 |
| ICT session slices: LONDON_CLOSE | 15:30–17:30 | 13:30–15:30 |
| ICT London setup caller | 06:30–11:59 | 04:30–09:59 |
| ICT New York setup caller | 11:30–15:30 | 09:30–13:30 |
| ICT London-close setup caller | 15:15–18:00 | 13:15–16:00 |
| ICT active HIGH windows | 12:00–14:00; 15:30–17:30 | 10:00–12:00; 13:30–15:30 |
| ICT NY-open confirmation window | 14:00–15:30 | 12:00–13:30 |
| NYUPIP optional active window | 08:00–18:00 | 06:00–16:00 |
| NYUPIP CIS trade window | 15:10–15:30 | 13:10–13:30 |
| NYUPIP CIS prior-day NY range lookup | 13:00–21:00 | 11:00–19:00 |
| Microstructure session classifier: ASIA / LONDON_OPEN / LONDON_MID / NY_OPEN / LONDON_CLOSE / NY | 00:00–06:59 / 07:00–09:59 / 12:00–14:59 / 14:00–15:59 / 15:00–17:59 / 17:00–23:59 | 22:00 prev day–04:59 / 05:00–07:59 / 10:00–12:59 / 12:00–13:59 / 13:00–15:59 / 15:00–21:59 |

NYUPIP’s optional 08:00–18:00 filter is disabled in the checked config (`nyupip_active_window_enabled: false`), but CIS has its separate 15:10–15:30 gate. CIS also looks up candles at 14:45 and 15:15 SAST. The global configured window and weekdays are separate from the strategy-specific windows above.

### 3. ICT ATM forming H1 bar

It is **not excluded**. The exact resample line is:

```python
h1 = df.resample("1h", label="right", closed="right").agg(
```

The final resampled row is retained and used by ATR and pattern detection; no current-time filter removes it (`src/strategies/ict_atm.py:219-226`).

### 4. Why no ICT Swing, NYUPIP, or FARMER orders?

The repository snapshot does not contain runtime logs, a trade database, or a record of the live dashboard controls, so it cannot identify the cause for a specific period.

Code establishes these default/gating facts:

- Every newly constructed stream starts with `trading_enabled=False`, `enable_high=False`, `nyupip_enabled=False`, `ict_swing_enabled=False`, and `ict_atm_enabled=False`. `engine_mode` starts as `ALL`, which does not itself turn on the tier flags.
- ICT Swing is not evaluated until its own toggle is enabled. Even after it generates a signal, order placement requires an enabled executor, `trading_enabled`, no spread/ATR/event/session block, an allowed engine mode, `enable_high=True`, no daily halt, and campaign capacity. Therefore a generic HIGH disable also blocks ICT Swing.
- NYUPIP is not evaluated until `nyupip_enabled=True`. Its diagnostics report context/module reasons such as `insufficient_history`, `outside_active_hours`, `trend_bias_missing`, `zone_invalid`, `trendline_invalid`, `atr_filter_failed`, `no_price_action_pattern`, `outside_trade_window`, `required_candles_missing`, `no_previous_day_data`, and `risk_reward_below_threshold`. A generated signal can still be blocked by the executor/trading/session/spread/ATR/event/daily-halt gates.
- FARMER is enabled from `execution.farmer.enabled` (true in the checked config), but it is nested under the general auto-trading guard: an enabled executor, `trading_enabled`, a non-zero main signal, open session, acceptable spread/ATR, and no event mode. Engine modes other than `ALL`/`FARMER_ONLY` suppress its `farmer_allowed` flag; `NONE` and `EVENT_ONLY` suppress it as well. It also requires an elapsed cycle and available HIGH campaign capacity. It does not run simply because its config flag is true.

Use the live `last_diagnostics` fields (`/api/ict_swing/status`, `/api/nyupip/status`) to identify signal-generation failures; use timestamped process logs for post-signal order blockers. FARMER has no equivalent structured diagnostics; its order/error lines and the surrounding main-signal/gate logs are required.

### 5. Open positions on process restart

The broker-side positions are not closed by process restart. A new `OrderManager` initializes `managed` as an empty dictionary and resets in-memory campaign, halt, and loss-minimizer state; there is no load/recovery path from persistence. Its periodic `reconcile()` fetches broker positions, but only applies exit rules to positions whose tickets are already in `managed`. Thus pre-restart positions remain open at MT5 (subject to broker-side SL/TP), but this process will not restore their time-stop/breakeven management. The daily loss halt is recalculated on a later reconcile; it is not restored from memory.

### 6. Runtime toggle callers and startup state

Repository-wide search finds the setters called only from these Flask routes (besides their definitions):

| Setter | Caller |
|---|---|
| `set_farmer_enabled` | `POST /api/farmer_toggle` |
| `set_engine_enabled` | `POST /api/engine_toggle` |
| `set_engine_mode` | `POST /api/engine_mode` |
| `set_trading_enabled` | `POST /api/trading_toggle` |
| `set_nyupip_enabled` | `POST /api/nyupip/toggle` |
| `set_ict_swing_enabled` | `POST /api/ict_swing/toggle` |
| `set_ict_atm_enabled` | `POST /api/ict_atm/toggle` |

No env/script caller was found in the repository. Startup sets `trading_enabled=False`; LOW/MEDIUM/HIGH, NYUPIP, ICT Swing, ICT ATM, and event mode to false; `engine_mode='ALL'`; and FARMER from config (`true` here). These are in-memory settings and are reset by process restart. The dashboard start path starts streams but does not call a trading-arm setter.

### 7. Does `MT5Connector.get_current_quote()` return `spread_points`?

For a successful MT5 tick, yes: its returned dictionary always has a `spread_points` key, with a computed value (zero if bid/ask are unavailable). If initialization/tick retrieval fails, it returns `None`, not a quote dictionary. Separate YFinance/mock fallback dictionaries do not include `spread_points`, so the stream’s `if spread_points is not None` guard is skipped for those sources.

### 8. Dashboard port, authentication, and state-changing endpoints

`live_dashboard.py` runs Flask on `0.0.0.0:5000`. The file has no Flask authentication middleware, login/session check, or route-level authorization; no auth is apparent in this application code. This does not establish whether AWS security groups or a reverse proxy add an external access restriction.

Trading-state/control endpoints are:

- `POST /api/pause`, `POST /api/resume` — stop/restart the stream worker.
- `POST /api/session_toggle` — bypass/restore the configured session filter.
- `POST /api/farmer_toggle`, `POST /api/engine_toggle`, `POST /api/event_toggle`, `POST /api/engine_mode` — change engine selection/gates.
- `POST /api/trading_toggle` — arm/disarm automated trading.
- `POST /api/nyupip/toggle`, `POST /api/ict_swing/toggle`, `POST /api/ict_atm/toggle` — enable/disable individual strategies.
- `POST /api/close_all_trades`, `POST /api/close_profitable_trades`, `POST /api/close_losing_trades` — close live broker positions.
- `POST /api/auto_take_profit` — enable/configure the background profit monitor, which can close all open positions when its threshold is reached.

Whether port 5000 is reachable from the public internet, and whether an AWS proxy/security group provides a separate authentication boundary, remains unverified from this repository.
