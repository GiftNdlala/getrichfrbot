# NYUPIP Backtest Plan

## Objectives

1. Validate each module (1HSMA and CIS) independently to confirm edge, risk/return profile, and parameter stability.
2. Evaluate combined operation to detect signal conflicts, overlapping exposure, and aggregate drawdowns.
3. Stress-test risk controls (ATR filter, spread guard, news lockout, daily loss cap) under historical volatility regimes.

## Data Requirements

- **Instrument:** XAUUSD spot or CFD proxy with tick or 1-minute resolution.
- **Coverage:** Minimum 3 years (include quiet, volatile, and news-heavy periods).
- **Session calendar:** London and New York session boundaries, major holidays, Tier-1 USD/Gold economic events.
- **Broker specifics:** Spread history, trading hours, server time offsets.

## Module A: 1HSMA Engine

| Step | Description |
|------|-------------|
| A1   | Generate H1 50-SMA trend bias; mark Label A/B/C per spec. |
| A2   | Detect qualifying M15 price-action patterns (engulfing, pin bar, inside bar breakout) with deterministic rules. |
| A3   | Apply ATR filter, spread guard, and news lockout; size positions at 1% risk; cap at 2 trades. |
| A4   | Record metrics: win %, average RR, profit factor, expectancy, max intraday and peak-to-trough drawdowns. |
| A5   | Sensitivity checks: SMA length +/- 10, entry confirmation toggles (RSI on/off), ATR multiplier sweep (1.0-1.3). |

## Module B: CIS Engine

| Step | Description |
|------|-------------|
| B1   | Convert historical data to SAST, isolate 14:45 and 15:15 M15 candles per trading day. |
| B2   | Determine directional bias from 14:45 close; validate entry at 15:15 close with spread/ATR filters. |
| B3   | Calculate SL (14:45 open) and TP (previous NY session high/low). Set risk at 1% equity. |
| B4   | Capture metrics: win %, average RR, profit factor, expectancy, max drawdown, time-in-trade. |
| B5   | Scenario checks: alt TP rules (fixed 2R, trailing) and day-of-week performance. |

## Combined Engine Tests

1. **Signal Coordination:** Determine priority when both modules trigger simultaneously (e.g., SMA bias overrides CIS opposite signal).
2. **Portfolio Risk:** Evaluate combined exposure with shared risk budget (max 2 trades) and daily loss cap enforcement.
3. **Equity Curve Analysis:** Compute aggregate metrics (win %, RR, profit factor, max drawdown, expectancy, Sharpe) and compare to modules individually.
4. **Conflict Simulation:** Track frequency of conflicting signals and measure performance with/without arbitration rules.

## Risk-Control Validation

- **ATR Filter:** Verify live ATR computation and threshold behavior; log instances of filter blocking trades.
- **Spread Guard:** Replay historical spreads to ensure entries respect 2x 30-minute average limit.
- **News Lockout:** Overlay economic-calendar timestamps; confirm suppression of affected trades.
- **Circuit Breakers:** Simulate sequential loss scenarios to validate daily (5%) and weekly (10%) kill-switches.

## Reporting

- Summaries with tables/plots for each module and combined system.
- Annotated trade examples (3 wins + 3 losses per module) exported for chart library with Label A/B/C, entry, SL, TP, filters.
- Parameter sweep appendix documenting performance shifts.
- Risk assessment comparing historical drawdowns vs. risk caps.
