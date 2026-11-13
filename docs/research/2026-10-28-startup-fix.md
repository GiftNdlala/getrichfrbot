# Startup fixes — 28 October 2026

The running dashboard status showed NEWS_CALENDAR_UNAVAILABLE blocking execution, NYUPIP disabled despite ALL mode, and Farmer waiting for no_confirmed_pullback. Hidden executor output made this look like an unexplained MT5 failure.

Implemented automatic background current-week calendar refresh at startup and hourly, six-hour cache expiry, atomic cache replacement, five-minute failure retries, and preservation of valid manually maintained calendars. News blackouts and missing/expired coverage still block entries.

Executor diagnostics now survive quiet stdout redirection and identify blocked versus broker-rejected orders with actual reasons. Intraday gates return within their own method so later strategy evaluations continue. Farmer runs independently. ALL enables Farmer and separate gold strategy switches; the Enable all strategies button applies this without arming trading. Event remains an exclusive override. Strategy decisions are visible; Farmer entry requirements and shared risk limits remain enforced.

Validation: 76 automated checks passed, including calendar behavior, rejection diagnostics, independent evaluation, ALL without arming, and Farmer waiting without forced orders. A read-only provider request returned 97 current-week events. No live order, active calendar write, or running-process restart was performed. MT5 execution and profitability still require forward testing.

Apply: Ctrl+C, restart python live_dashboard.py, refresh the dashboard, and watch for NEWS CALENDAR READY. Enable all strategies and use the existing trading arm control when ready for demo testing. Qualifying setups still require session, price confirmation, acceptable spread and available risk budget.
