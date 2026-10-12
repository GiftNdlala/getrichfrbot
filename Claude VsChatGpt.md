# Claude vs ChatGPT — signal-engine audit

**Scope:** XAUUSD signal engine review, including the research observations supplied in the discussion and a code audit of the repository as of 15 August 2026. NYUPIP is intentionally out of scope; no conclusion here should be read as a whole-system review.

**Safety decision:** keep ICT Swing and ICT ATM disabled for live execution until the critical items below are implemented, tested, and independently backtested. This document is an engineering audit, not trading advice.

## Research context and source hierarchy

The discussion identified the following external, educational sources:

- [AMD / Power of Three overview](https://arongroups.co/forex-articles/amd-ict-power-of-3/): accumulation -> manipulation/liquidity sweep -> distribution. The claimed practical rule is to enter only after the sweep has produced a structure shift.
- [OTE overview](https://arongroups.co/technical-analyze/optimal-trade-entry-techniques/): the 62–79% retracement zone, with 70.5% as the midpoint, should have confluence (for example OB/FVG) and confirmation rather than be treated as an unconditional entry level.
- [ICT ATM model overview](https://icttraders.net/the-ict-atm-model/): H1 liquidity raid -> structural break -> retest.
- [ICT kill-zone overview](https://www.ictkillzone.com/ict-kill-zones): session definitions should be anchored to New York time, which observes DST.

These claims were supplied in the discussion and are recorded as research context; the code findings below were independently checked against this repository. The repository also contains auto-generated ICT transcripts for ATM and Key Swing Points, plus an implementation specification. The specification explicitly lists FVG/OB integration, equal-high/low liquidity-pool detection, and stronger London-close validation as future work.

## Strategy inventory

The six-indicator ensemble is separate from the ICT strategies:

1. SMA crossover(s): 20/50 and 50/200 are separate votes.
2. RSI(14) reversal.
3. MACD(12,26,9) crossover.
4. Bollinger-band touch/re-entry condition.
5. Volume-ratio directional confirmation.
6. Trend-following: price/SMA20/SMA50/RSI alignment.

The stream then derives LOW, MEDIUM, or HIGH labels from confidence. Farmer reuses a non-HOLD ensemble direction. Event, ICT Swing, and ICT ATM are separate engines.

## Confirmed findings

### 1. Session logic has a DST structural defect

`ICTSwingPointsStrategy` reads the configured `Africa/Johannesburg` timezone and slices fixed SAST clock windows:

| Session | Current definition (SAST) |
|---|---:|
| Asia | 00:00–06:59 |
| London | 07:00–11:59 |
| New York | 12:00–15:59 |
| London close | 15:30–17:30 |

Because Johannesburg does not observe DST, these fixed values do **not** follow the New York clock as the United States changes between standard and daylight time. The solution is not to retune SAST constants: define the canonical boundaries in `America/New_York` and convert their instantiated boundaries to the strategy/data timezone at runtime.

There is also a detection-versus-slicer seam. The defined windows are above, but London detection permits 06:30 onward, New York detection 11:30 onward, and London-close detection 15:15 onward. This may be an intentional early-arming design; do not collapse it without a stated design decision and tests. If retained, model it explicitly as `arming_window` versus `eligible_entry_window`.

Evidence: `src/strategies/ict_swing_points.py` lines 81–97, 313–476.

### 2. Swing OTE is zone-touch-only

Swing calculates an OTE ratio and emits a signal when it is between 0.62 and 0.79 after its expansion threshold is met. It does **not** require:

- an order block or fair-value gap at the zone;
- a rejection/confirmation candle;
- lower-timeframe market-structure shift;
- a close/reclaim or follow-through after arriving at the zone.

This is a direct mismatch with the research criterion that the retracement itself is not the entry. The current code turns a bare geometric touch into an executable signal.

Evidence: `src/strategies/ict_swing_points.py` lines 340–390 and 422–470. The design document lists order blocks/FVGs as missing integration work: `docs/ict_swing_point_full_implementation_strategy.md` lines 42 and 74–97.

### 3. ATM confirms structure, but not retest reaction

ATM resamples to H1, requires 60 H1 bars, finds a two-left/two-right fractal pivot, then requires:

- bearish: a strictly higher second pivot high, a subsequent break below the intervening swing low, and price back within the retest tolerance;
- bullish: a strictly lower second pivot low, a subsequent break above the intervening swing high, and price back within the retest tolerance.

The tolerance is `max(0.25 * ATR(14), 0.05% of current price)`. The pattern/break may be up to 48 hours old. That is a genuine structural-break requirement, so ATM is stronger than a bare Swing OTE touch. But execution still fires immediately on **proximity** to the retest level: no rejection candle, reclaim, follow-through, or post-retest micro-structure confirmation is required.

Therefore both ICT engines share the same root confirmation gap. ATM's advantage is its named H1 structure-break/retest shape, not a completed confirmation model.

Evidence: `src/strategies/ict_atm.py` lines 127–155, 242–369, and 371–381.

### 4. ATM does not model equal-high/equal-low liquidity pools

The ATM pivot stream is a simple five-bar fractal (`lookback=2`); the actual setup demands the later high be strictly higher or later low strictly lower. There is no grouping of near-equal highs/lows, no pool-strength measurement, no sweep-distance threshold, and no prior-day/week/month liquidity reference.

Equal-high/low tagging should filter or grade the pivot stream rather than be added as a cosmetic check after entry conditions are already satisfied. The current 2/2 fractal alone is noisy on H1.

Evidence: `src/strategies/ict_atm.py` lines 250–267, 315–332, and 371–381.

### 5. The 48-hour ATM expiry is permissive

`max_pattern_age_hours` defaults to 48. This can admit a retest after another full daily cycle, weakening the assumption that the original broken level still has the intended session context. The limit should be explicitly justified by data or tightened to a session/day-aware expiry before enabling live execution.

Evidence: `src/strategies/ict_atm.py` lines 76–83 and 256–283.

### 6. London-close 15% is local tuning with no provenance

The London-close reversal sends a short at a current-day range position >=85%, and a long at <=15%. No paper, transcript citation, parameter file, or backtest record for those thresholds exists in the repository. The implementation spec also identifies London-close validation as unfinished.

Label this as a local hypothesis/tuned parameter, not an ICT specification, until a controlled backtest documents it.

Evidence: `src/strategies/ict_swing_points.py` lines 490–526; `docs/ict_swing_point_full_implementation_strategy.md` lines 84–97 and 143–144.

### 7. `range_position` does not use future data in live logic

For the London-close rule, `today_slice` explicitly keeps only rows whose timestamps are on the current local date and `<= current_local`. The day's high and low are then calculated from that slice. This prevents future-session look-ahead in the live path.

Backtests must preserve this cutoff when constructing each historical evaluation row; otherwise the backtest harness, rather than the strategy function, could reintroduce look-ahead bias.

Evidence: `src/strategies/ict_swing_points.py` lines 169–189 and 490–494.

### 8. ICT strategies do not vote in the six-signal ensemble

The ensemble is generated solely by `SignalGenerator.generate_all_signals(...)`. ICT Swing and ICT ATM are evaluated later in the stream and are passed straight to independent order handlers. They do not raise the ensemble confidence or add votes to Trend-following.

The SMA collapse is **not** unanimous: the available SMA columns are sorted and each adjacent pair becomes a separate vote. With the configured 20, 50, and 200 SMAs, 20/50 and 50/200 may each vote independently; a single pair can contribute a directional vote, and conflicts cancel only through the simple summed-majority rule.

Evidence: `src/live_data_stream.py` lines 1047–1061 and 1619–1674; `src/indicators.py` lines 288–305; `src/signal_generator.py` lines 39–64 and 266–278.

### 9. Cross-strategy exposure control is absent

The system shares some execution components, but it has no central reservation that counts symbol exposure or aggregate stop-risk before every entry. It also has no strategy mutual-exclusion policy, so the ensemble and a qualifying ICT engine can attempt same-direction entries in the same move.

`risk.max_concurrent_trades = 1` is present in `config.json` but has no code reference. `max_open_risk_pct` is loaded by `OrderManager` but is never enforced. Campaign limits control **entry frequency**, keyed by symbol, side, and level; they are not open-position or total-risk limits. ICT Swing and ATM use different campaign buckets (`HIGH_SWING` and `HIGH_ATM`), so they do not constrain each other through the HIGH bucket.

Evidence: `config.json` lines 9–27 and 120–150; `src/order_manager.py` lines 30–68 and 72–90; repository search finds no use of `max_concurrent_trades` and no enforcement use of `max_open_risk_pct`.

### 10. Farmer is the live-risk priority

Farmer is enabled in the current configuration. It requires only a non-HOLD ensemble signal, not a minimum confidence, vote margin, or HIGH label. It uses the shared executor's per-order risk sizing: current `risk_percent_per_trade` is 0.25% of account equity, subject to broker minimum lot and margin fitting. Its configured stop is 18 pips, and target is 2 pips with ATR-based expansion to 3–5 pips.

The code attempts `trades_per_cycle = 3` every 30 seconds. However, before every attempted Farmer order it calls the shared HIGH campaign gate. After the first successful order it records the entry; the current 10-second minimum spacing then normally blocks the second and third attempt in the same burst. Thus it is **configured as a three-order burst but usually executes one per cycle**, unless campaign tracking is unavailable or behavior changes.

That does not solve the core risk: there is no open-position count or aggregate exposure check, no confidence threshold, and no shared cross-strategy risk reservation. The campaign's HIGH limit is 30 entries in a five-minute rolling window, far above a conservative exposure cap.

Evidence: `config.json` lines 9–12 and 122–150; `src/live_data_stream.py` lines 1495–1560; `src/order_manager.py` lines 42–60; `src/executor.py` lines 106–135 and 137–204.

## Priority remediation order

1. **DST-safe session service.** Store the strategy's canonical kill zones in `America/New_York`; use timezone-aware interval conversion at runtime; name and test separate arming and eligible-entry windows across both US DST transitions.
2. **Shared confirmation gate.** Require an explicit, completed confirmation after price reaches the OTE/retest zone. At minimum: a defined rejection candle, a close/reclaim rule, and a lower-timeframe market-structure shift. Make OB/FVG confluence and liquidity-pool quality typed inputs, not comments.
3. **Central exposure/risk reservation.** Before every engine calls `place_market_order`, atomically check positions and pending reservations for symbol, direction, gross lots, and stop-risk. Enforce `max_concurrent_trades` and `max_open_risk_pct`; define whether same-direction stacking is permitted.
4. **Tighten/validate ATM lifecycle.** Replace the 48-hour flat expiry with a configurable session/day-aware expiry; tag and grade equal-high/low pools before accepting a sweep.
5. **Document local parameters and backtest.** Label the London-close 15% threshold as local until tested. Ensure every backtest evaluates `today_slice` only through the historical decision timestamp.
6. **Only then reconsider enabling ICT Swing/ATM.** Farmer should be reviewed under the same central exposure gate before remaining enabled.

## Implementation acceptance tests

- New York session intervals map correctly to SAST before and after US DST start/end, without changing constants.
- An OTE/retest touch without confluence or confirmation produces HOLD/no-order.
- A qualified retest plus explicit confirmation produces one eligible signal with recorded evidence.
- Equal-high/equal-low pools are detected with tolerance, minimum touches, age, and sweep distance; ordinary fractals do not qualify by default.
- An existing ensemble position prevents or deliberately nets a same-symbol ICT entry according to the selected policy.
- Farmer cannot exceed the configured concurrent-position and aggregate-risk caps, including broker minimum-lot edge cases.
- Historical replay uses no price data later than each decision timestamp.

