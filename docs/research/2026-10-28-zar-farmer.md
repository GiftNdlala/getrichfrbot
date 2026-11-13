# ZAR Farmer support — 28 October 2026

The account owner confirmed ZAR. Replaced the USD-only Farmer restriction with live broker currency conversion. Discover direct USD/account or inverse account/USD pairs by broker currency metadata, supporting symbol suffixes. Require a finite positive, non-crossed quote no older than 60 seconds and a spread below 5%; otherwise block with USD_CONVERSION_UNAVAILABLE:ZAR.

Convert Farmer USD target, estimated costs, per-trade cash loss cap and daily cash loss cap to account currency. Use one conversion rate throughout each order assessment. MT5 profit calculations and percentage equity/exposure limits remain in account currency. No fixed exchange rate, increased risk percentage or forced order. Dollar figures remain USD economic targets, not R2 targets. Historical booked losses use the current conversion rate for the daily USD limit.

Tests cover direct suffixed and inverse pairs, stale quotes, ZAR order target/risk sizing, converted daily loss caps and existing USD behavior. Restart the dashboard to apply. No live orders or process restart performed during development.
