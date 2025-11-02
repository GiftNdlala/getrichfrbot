# NyuPIP (Feni4Real) Strategy Onboarding Document

**Author:** Sbusiso Feni (52 Trading Academy)  
**Date:** September 28, 2025  
**Symbol:** XAUUSD (Gold Spot)  
**Strategy Code:** NYUPIP_XAU  
**Category:** Standalone - Auto-trading  
**Author Reference:** Adapted from Feni4Real's "Ultimate Trading Blueprint"

---

## I. Trading Style & Overview

*   **Primary Instruments:** US30 indices, Gold (XAUUSD)
*   **Time Frames:**
    *   1 Hour (H1) for 1HSMA strategy (trend filter & main zone)
    *   15-Minute (M15) for CIS strategy (entry timing & confirmation)
*   **Session Focus:** London and New York sessions.
*   **Risk Management:** Default 1% equity risk per trade (maximum 2%).

---

## II. Trading Strategy Components

The NyuPIP strategy merges two core components: the 1HSMA (1-Hour Simple Moving Average) strategy for structured trend alignment and the CIS (Change in Session) strategy for precise session timing.

### A. 1HSMA Strategy (50-SMA on 1-Hour Chart)

**Label Glossary:**

*   **Label A (Entry Zone):** Region where price touches, closes near, or marginally pierces the H1 50-SMA; treated as dynamic support/resistance.
*   **Label B (Trend-Validation Line):** Trendline drawn along recent swing highs/lows in the prevailing trend direction. A decisive close beyond Label B invalidates pending setups.
*   **Label C (Trend Filter):** The H1 50-SMA itself; price relative to Label C defines directional bias.

**Goal:** Follow the higher timeframe trend.

**Indicator:** 50-period Simple Moving Average (SMA) on the 1-Hour chart.

**Full Setup Flow:**

1.  **Step 1 - Identify Trend (H1 SMA) - Label C:**
    *   Wait for the price to approach the 50-period SMA on the 1-Hour chart.
    *   **Determine trend direction:**
        *   **Uptrend:** Price is above 50 SMA & SMA slopes upward -> only consider buy setups.
        *   **Downtrend:** Price is below 50 SMA & SMA slopes downward -> only consider sell setups.
    *   **Key Tip:** Only trade in the direction of H1 trend to increase success rate.
    *   **Do not trade:** If the price is moving sideways (i.e., it's stuck around the SMA without clear direction).

2.  **Step 2 - Define Entry Zone (Label A):**
    *   Monitor the area where the price interacts with the 50-SMA on H1.
    *   Begin observation when price touches, closes near, or slightly pierces the SMA.
    *   Treat the H1 SMA as dynamic support/resistance aligned with the identified trend.

3.  **Step 3 - Draw Trend Validation Line (Label B):**
    *   Draw a line connecting recent swing highs/lows in the trend direction.
    *   This trend line must remain unbroken for the trade to stay valid.
    *   If price breaks this line -> trade is invalid.

4.  **Step 4 - Zoom to M15 for Entry:**
    *   Go to the 15-minute chart inside the Label A zone.
    *   Look for confirmation patterns in the trend direction:
        *   **Buy Setups (H1 trend up, price above SMA):**
            *   Bullish engulfing candle
            *   Hammer / Pin bar with rejection
            *   Inside bar breakout to the upside
        *   **Sell Setups (H1 trend down, price below SMA):**
            *   Bearish engulfing candle
            *   Shooting star / Pin bar rejection
            *   Inside bar breakout to the downside
    *   **Entry Rule:** Enter after the M15 candle closes in the trend direction at the Label A zone.
    *   **Momentum Filter (optional):** RSI(14) on M15 must be > 50 for buys or < 50 for sells when the RSI filter is enabled.

5.  **Step 5 - Stop-Loss Placement:**
    *   Place SL just beyond the recent M15 swing low/high:
        *   **Buy:** Below the nearest M15 low inside the Label A zone.
        *   **Sell:** Above the nearest M15 high inside the Label A zone.
    *   Ensures tight risk control while allowing the trade to breathe and supports fixed-percentage position sizing.

6.  **Step 6 - Take-Profit (TP) Placement:**
    *   TP can be based on:
        1.  Previous H1 swing highs/lows.
        2.  Trend continuation zones.
        3.  Until trend changes (price closes beyond the 50-SMA in the opposite direction).
    *   Alternatively, target a minimum risk-to-reward ratio (RR) of 2:1.
    *   **Optional:** Take partial profit at the first support/resistance level and move SL to breakeven after partial exit.

7.  **Step 7 - Trade Management:**
    *   Monitor Label B (trend line) - if broken, exit immediately.
    *   Optionally scale out partial profits at intermediate zones.
    *   Trail SL if the trend continues strongly in your direction.
    *   If the price moves 50% in favor of the trade, consider moving your stop loss to break-even.

### B. CIS Strategy (Change in Session Strategy)

**Goal:** Capture volatility between London-NY transitions.

**Time Frame:** 15-minute chart.
**Session Focus:** London session, specifically the 14:45 and 15:15 candles (South African Time).

**Conditions for Buying:**

1.  Look at the 15-minute chart for the London session, specifically the 14:45 and 15:15 candles (South African time).
2.  The 14:45 candle must be bullish (price should close higher than it opened).
3.  The entry level is the closing price of the 15:15 candle.
4.  The stop loss is the opening price of the 14:45 candle.
5.  The take profit is set at the previous day's New York session high.

**Conditions for Selling:**

1.  For the selling setup, focus on the same 15-minute chart for the 14:45 and 15:15 candles.
2.  The 14:45 candle must be bearish (price closes lower than it opened).
3.  The entry level is the closing price of the 15:15 candle.
4.  The stop loss is the opening price of the 14:45 candle.
5.  The take profit is set at the previous day's New York session low.

---

## III. Session Timing & Time Zones

| Reference Event               | SAST (UTC+2) | UTC Time  | Notes                                                   |
|------------------------------|--------------|-----------|---------------------------------------------------------|
| London open alignment        | 09:00        | 07:00     | Use for pre-session context checks                      |
| CIS candle 1                 | 14:45        | 12:45     | 15-minute candle that defines directional bias          |
| CIS candle 2 (entry trigger) | 15:15        | 13:15     | Entry evaluated at the close of this candle             |
| New York session reference   | 15:00-23:00  | 13:00-21:00 | Previous NY session high/low sourced from this window   |
| Automation active window     | 08:00-18:00  | 06:00-16:00 | Trading disabled outside this range                     |

**Time-zone handling:** Map broker/server timestamps to UTC first, then convert to SAST (UTC+2). South Africa does not observe daylight saving; adjust for brokers that shift to DST so CIS windows align.

---

## IV. Risk & Trade Management

### A. Risk Management

*   **Risk per Trade:** Default 1% of equity; configurable up to a hard cap of 2%.
*   **Max Concurrent Trades:** 2 (one per module unless otherwise specified).
*   **Stop-loss strategy:** Set SL according to the entry playbook before submitting the order.
*   **Position sizing:** Calculate lots so the defined SL distance equals the intended risk percentage.
*   **Break-even protocol:** When price covers 50% of planned TP distance, move SL to entry or trail per module rules.
*   **News filter:** Suspend entries during Tier-1 economic releases affecting USD or precious metals.
*   **Daily loss circuit breaker:** Disable strategy when realized daily drawdown reaches 5% of equity.

### B. Trade Review

*   **Pre-trade checklist:**
    *   [ ] Have I confirmed the trend on the 1-Hour SMA chart?
    *   [ ] Is the price near a key support/resistance level?
    *   [ ] Have I waited for proper candlestick patterns for confirmation?
    *   [ ] Have I set my stop-loss and take-profit levels?
*   **During the trade:**
    *   [ ] Is the market respecting the trend?
    *   [ ] If the price moves 50% in favor of the trade, consider moving your stop loss to break-even.
*   **Post-trade review:**
    *   [ ] Was my risk-to-reward ratio met?
    *   [ ] Did the trade follow my strategy and trade rules?
    *   [ ] I have reviewed my trade to learn from mistakes or successes.
    *   [ ] I have updated my trading journal with details of the trade.

---

## V. Psychological Management

*   **Emotion Control:** Stick to the plan. Do not chase trades or deviate from your strategy, especially after a loss.
*   **Patience:** Wait for the right setups to appear, don't force trades.
*   **Confidence:** Treat the published 92% CIS win-rate claim as unverified until backtested and validated.
*   **Trade the structure, not emotion.**
*   **No manual override during drawdown.**
*   **Accept invalidations immediately.**
*   **Review after every 20 trades minimum.**

---

## VI. Feni4Real Trading Checklist

### Before the Trade:

*   [ ] I have reviewed the market sentiment.
*   [ ] I have identified the trend on the 1-Hour chart using the 50-SMA.
*   [ ] I have confirmed the entry pattern (candlestick confirmation) on the 15-minute chart.
*   [ ] I have set a clear stop-loss and take-profit level.

### During the Trade:

*   [ ] I am managing the trade, moving the stop to break-even if needed.
*   [ ] I am not overtrading.

### After the Trade:

*   [ ] I have reviewed my trade to learn from mistakes or successes.
*   [ ] I have updated my trading journal with details of the trade.

---

## VII. Automation Behavior

*   **Mode:** Fully automated
*   **Active Hours:** 08:00-18:00 SAST (06:00-16:00 UTC)
*   **Volatility filter:** Trade only when current H1 ATR(14) >= 1.1 x SMA(ATR(14), 14).
*   **Trend validation:** H1 50-SMA bias must align with the intended trade direction and Label B must remain intact.
*   **CIS activation:** CIS entries require valid 14:45/15:15 SAST candle pattern and confirmed previous NY high/low reference.
*   **Disable conditions:**
    *   Volatility filter fails for three consecutive H1 closes.
    *   Realized daily loss >= 5% equity.
    *   Session window closed or high-impact news lockout active.

---

## VIII. Parameter Summary

| Group                | Field                          | Value / Guidance                                  |
|----------------------|--------------------------------|---------------------------------------------------|
| Identification       | Strategy Name                  | NyuPIP (Feni4Real)                                |
|                      | Code                           | NYUPIP_XAU                                        |
| Instruments          | Symbol                         | XAUUSD                                            |
| Trend Filter         | SMA length (H1)                | 50                                                |
| Entry Timeframes     | Trend                          | H1                                                |
|                      | Execution                      | M15                                               |
| Volatility Filter    | ATR period (H1)                | 14                                                |
|                      | Threshold                      | Current ATR14 >= 1.1 x SMA(ATR(14), 14)           |
| Momentum Filter      | RSI period (M15)               | 14 (if enabled: > 50 for buys, < 50 for sells)    |
| CIS Window           | Candle times (SAST)            | 14:45 bias, 15:15 entry                           |
| Risk Settings        | Default risk per trade         | 1% equity                                         |
|                      | Maximum risk per trade         | 2% equity                                         |
|                      | Max concurrent trades          | 2                                                 |
|                      | Daily loss cap                 | 5% equity                                         |
| Execution Constraints| Spread limit                   | <= 2 x rolling 30-minute average spread           |
| Logging & Audit      | Trade logging                  | Enabled (store entries, exits, filter status)     |

---

## IX. Risk Policy Appendix

| Scope              | Rule                                              | Action When Breached                         |
|--------------------|---------------------------------------------------|----------------------------------------------|
| Per Trade          | Risk <= 2% equity; SL placed before order         | Block order; raise alert                     |
| Daily              | Max realized loss 5% equity                       | Disable automation for remainder of day      |
| Weekly             | Max realized loss 10% equity                      | Require manual review before reactivation    |
| Consecutive Losses | 4 consecutive losing trades per module            | Pause affected module; run diagnostics       |
| Spread             | Live spread > 2 x rolling 30-min average         | Skip entry; re-check next evaluation cycle   |
| Volatility         | ATR condition fails 3 consecutive H1 closes       | Suspend until ATR filter recovers            |
| News Lockout       | Tier-1 USD/Gold events within +/-30 minutes       | Suspend new entries; manage open trades only |

---

## X. Supporting Deliverables

1.  **Chart library:** Capture three winning and three losing examples for both 1HSMA and CIS modules. Annotate Label A/B/C, entry candle, SL, TP, filter status, and spread snapshot. Store under `charts/nyupip/` with consistent naming (`module_outcome_date.png`).
2.  **Backtest plan:** Run module-level and combined backtests collecting win %, average RR, profit factor, max drawdown, expectancy, and sample trade logs. Ensure ATR, news, and spread filters are enforced in simulation.
3.  **Data provenance:** Archive historical data sources, broker configuration, and session calendars alongside test results for reproducibility.

---

## XI. Strategic Assessment

The NyuPIP (Feni4Real) strategy blends higher-timeframe trend alignment (1HSMA) with session-momentum tactics (CIS) for a disciplined multi-timeframe approach. Strengths include explicit guardrails, modular automation hooks, and clear execution choreography. Remaining risks center on the unverified "92% win rate" claim, reliance on accurate volatility and session detection, and the need for deterministic definitions when coding candlestick and trendline patterns. With clarified parameters and validated backtests, the strategy can mature into a robust semi-systematic gold framework.
