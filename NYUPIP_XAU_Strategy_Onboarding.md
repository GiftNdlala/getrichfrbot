# NyuPIP (Feni4Real) Strategy Onboarding Document

**Author:** Sbusiso Feni (52 Trading Academy)  
**Date:** September 28, 2025  
**Symbol:** XAUUSD (Gold Spot)  
**Strategy Code:** NYUPIP_XAU  
**Category:** Standalone — Auto-trading  
**Author Reference:** Adapted from Feni4Real's "Ultimate Trading Blueprint"

---

## I. Trading Style & Overview

*   **Primary Instruments:** US30indices, Gold (XAUUSD)
*   **Time Frames:**
    *   1 Hour (H1) for 1HSMA strategy (Trend filter & main zone)
    *   15-Minute (M15) for CIS strategy (Entry timing & confirmation)
*   **Session Focus:** London and New York sessions.
*   **Risk Management:** Risk no more than 1-2% of your account balance per trade.

---

## II. Trading Strategy Components

The NyuPIP strategy merges two core components: the 1HSMA (1-Hour Simple Moving Average) strategy for structured trend alignment and the CIS (Change in Session) strategy for precise session timing.

### A. 1HSMA Strategy (50-SMA on 1-Hour Chart)

**Goal:** Follow the higher timeframe trend.

**Indicator:** 50-period Simple Moving Average (SMA) on the 1-Hour chart.

**Full Setup Flow:**

1.  **Step 1 – Identify Trend (H1 SMA) - Label C:**
    *   Wait for the price to approach the 50-period SMA on the 1-Hour chart.
    *   **Determine trend direction:**
        *   **Uptrend:** Price is above 50 SMA & SMA slopes upward → only consider buy setups.
        *   **Downtrend:** Price is below 50 SMA & SMA slopes downward → only consider sell setups.
    *   **Key Tip:** Only trade in the direction of H1 trend to increase success rate.
    *   **Do not trade:** If the price is moving sideways (i.e., it's stuck around the SMA without clear direction).

2.  **Step 2 – Define Entry Zone (Label A):**
    *   This is the zone where the price interacts with the 50 SMA on H1.
    *   This is the starting point for trade observation.
    *   Look for price touching, closing near, or slightly piercing the SMA.
    *   H1 SMA acts as dynamic support/resistance depending on trend direction.

3.  **Step 3 – Draw Trend Validation Line (Label B):**
    *   Draw a line connecting recent swing highs/lows in the trend direction.
    *   This trend line must remain unbroken for the trade to stay valid.
    *   If price breaks this line → trade is invalid.

4.  **Step 4 – Zoom to M15 for Entry:**
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
    *   **Confirmation:** Confirm with RSI (Relative Strength Index) or other momentum indicators for additional confirmation (optional).

5.  **Step 5 – Stop-Loss Placement:**
    *   Place SL just beyond the recent M15 swing low/high:
        *   **Buy:** Below the nearest M15 low inside the Label A zone.
        *   **Sell:** Above the nearest M15 high inside the Label A zone.
    *   Ensures tight risk control while allowing the trade to breathe.
    *   Alternatively, 1% of your account balance.

6.  **Step 6 – Take-Profit (TP) Placement:**
    *   TP can be based on:
        1.  Previous H1 swing highs/lows.
        2.  Trend continuation zones.
        3.  UNIT TREND CHANGES.
    *   Alternatively, a risk-to-reward ratio of 2:1.
    *   **Optional:** Partial TP at the first support/resistance level, move SL to breakeven after partial exit.

7.  **Step 7 – Trade Management:**
    *   Monitor Label B (trend line) – if broken, exit immediately.
    *   Optionally scale out partial profits at intermediate zones.
    *   Trail SL if the trend continues strongly in your direction.
    *   If the price moves 50% in favor of the trade, consider moving your stop loss to break-even.

### B. CIS Strategy (Change in Session Strategy)

**Goal:** Capture volatility between London–NY transitions.

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

## III. Risk & Trade Management

### A. Risk Management

*   **Risk per Trade:** 1-2% of equity (contradicts "10-20% of your account balance" in Trade Management section, using 1-2% as per Overview and NyuPIP Onboarding document).
*   **Max Concurrent Trades:** 2
*   **Stop-loss strategy:** Always set a stop loss according to the entry strategy to protect your capital.
*   **Position sizing:** Adjust the position size based on your risk percentage.
*   **Move SL to BE:** Once 50% TP distance achieved.
*   **Hard Stop:** No trading during high-impact news.
*   **Auto Disable:** If daily loss > 5%.

### B. Trade Review

*   **Pre-trade checklist:**
    *   ☐ Have I confirmed the trend on the 1-Hour SMA chart?
    *   ☐ Is the price near a key support/resistance level?
    *   ☐ Have I waited for proper candlestick patterns for confirmation?
    *   ☐ Have I set my stop-loss and take-profit levels?
*   **During the trade:**
    *   ☐ Is the market respecting the trend?
    *   ☐ If the price moves 50% in favor of the trade, consider moving your stop loss to break-even.
*   **Post-trade review:**
    *   ☐ Was my risk-to-reward ratio met?
    *   ☐ Did the trade follow my strategy and trade rules?
    *   ☐ I have reviewed my trade to learn from mistakes or successes.
    *   ☐ I have updated my trading journal with details of the trade.

---

## IV. Psychological Management

*   **Emotion Control:** Stick to the plan. Do not chase trades or deviate from your strategy, especially after a loss.
*   **Patience:** Wait for the right setups to appear, don't force trades.
*   **Confidence:** Trust in your strategy's 92% win rate with the CIS method and the trend-following 1HSMA strategy.
*   **Trade the structure, not emotion.**
*   **No manual override during drawdown.**
*   **Accept invalidations immediately.**
*   **Review after every 20 trades minimum.**

---

## V. Feni4Real Trading Checklist

### Before the Trade:

*   ☐ I have reviewed the market sentiment.
*   ☐ I have identified the trend on the 1-Hour chart using the 50-SMA.
*   ☐ I have confirmed the entry pattern (candlestick confirmation) on the 15-minute chart.
*   ☐ I have set a clear stop-loss and take-profit level.

### During the Trade:

*   ☐ I am managing the trade, moving the stop to break-even if needed.
*   ☐ I am not overtrading.

### After the Trade:

*   ☐ I have reviewed my trade to learn from mistakes or successes.
*   ☐ I have updated my trading journal with details of the trade.

---

## VI. Automation Behavior

*   **Mode:** Fully automated
*   **Active Hours:** 08:00–18:00 SAST
*   **Conditions:**
    *   Volatility > avg 14-day ATR
    *   SMA valid
    *   CIS active
*   **Disable if:** Volatility < 30% or trend invalidated

---

## VII. System Integration Parameters

| Parameter         | Value               |
| :---------------- | :------------------ |
| Strategy Name     | NyuPIP (Feni4Real)  |
| Code              | NYUPIP_XAU          |
| Category          | Standalone          |
| Trading Mode      | Auto                |
| Symbol            | XAUUSD              |
| Entry Timeframes  | H1, M15             |
| Indicators        | SMA(50), RSI (optional) |
| Session Focus     | London / New York   |
| Logging           | Enabled             |

---

## VIII. Final Thoughts

This plan combines both trend-following (1HSMA) and session-based breakout setups (CIS). With proper risk management, patience, and emotional control, you're set to consistently follow a structured approach. Stick to the plan, adapt, and adjust based on what works best for you! The NyuPIP (Feni4Real) strategy merges structured trend alignment (1HSMA) with precise session timing (CIS) to exploit high-probability gold moves under automated control. Designed for consistency, discipline, and precision.
