# Trading correctness and Farmer research — 27 October 2026

## Objective and constraints

The owner wants continuous monitoring and small account-currency profits from a Farmer alongside the slower strategies. The aspirational target is 100% wins; approximately 60% observed winners is acceptable to the owner. Neither is a promised result. Win rate is not account return. Expectancy after spread, commissions, swaps, slippage, and losses is the decision criterion. No martingale, recovery sizing, or hiding unrealized losses is permitted.

Baseline: main commit `6e55f51` (22 October 2026). Changes are local and have not been deployed to EC2 or armed against MT5. Existing dashboard controls remain. Defaults are demo-only and trading remains disarmed at startup. The original baseline can be compared through Git; historical trade data is not rewritten.

## Implemented changes

### Shared execution policy

Every engine still uses `AutoTrader.place_market_order`, now under one fail-closed policy and the existing MT5 lock. The policy requires fresh MT5 quote context, successful signal persistence, and a completed broker-candle refresh, rechecks the live bid/ask spread, verifies the selected account and demo-account type, and checks account-wide positions and pending orders. Failed broker reads block entries. A broker-confirmed order reserves a slot even if its position is not visible immediately; elapsed time alone does not release it.

Sizing uses `order_calc_profit` on the final normalized market entry and stop. Broker minimum volume is never rounded upward beyond the risk budget. Existing position stop-risk, account-wide daily loss, configured per-trade risk, cost buffer, and progressive reduction constrain sizing. Final quotes are checked again immediately before submission; small movements are re-priced and their risk/target economics rechecked, while large drift is refused. The margin fit searches only the proposed risk-sized volume and has no accidental 1-lot ceiling. The daily calculation uses UTC-day deals including commission/swap/fee and current equity, so floating losses count. It reconstructs a cashflow-adjusted daily baseline from current balance minus booked trading P&L and costs. Funding, credit, bonuses, and corrections are excluded from trading profit; fresh demo funding can therefore be used on the first day. Deposits/withdrawals change the capital baseline and require review when interpreting day-over-day returns.

Research defaults: 0.25% intended risk per ordinary trade; one concurrent account position; 0.5% open-risk budget; 2% daily loss ceiling; half size after 1% daily drawdown. Stop orders cannot guarantee a maximum realized loss through gaps or slippage. No claim is made that these settings optimize returns.

### News readiness

The old February 2025 example events no longer constitute permission to trade. Execution reads `data/news_calendar.json` with explicit `valid_from`, `valid_until`, and `events`. Missing, invalid, or expired coverage blocks entries while monitoring and position management continue. USD HIGH events block 30 minutes before and 15 minutes after by default. Coverage must come from a verified current calendar, including an explicitly checked empty-event interval when appropriate. Do not fabricate coverage dates to bypass this gate.

Expected format (illustration only; replace with verified dates and events):

```json
{
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-01-01T23:59:59Z",
  "events": [
    {"name": "EXAMPLE_ONLY", "timestamp": "2026-01-01T13:30:00Z", "currency": "USD", "impact": "HIGH"}
  ]
}
```

The file is ignored by Git. This intentionally expired example is not a usable calendar. Automatic calendar ingestion remains future work. The operator can explicitly disable the news gate for an isolated historical experiment; it should remain enabled in forward demo testing.

### Canonical candles and strategy corrections

The live loop refreshes bounded MT5 M1 history instead of constructing one candle per sampled quote. Bars use UTC-aware OPEN timestamps; only elapsed M1 bars are retained. Repeated snapshots replace rows rather than duplicate them. H1/M15 aggregation excludes forming periods, future observations, and incomplete periods. NYUPIP no longer compares UTC-naive history with SAST-naive current time. CIS now uses New York time: bias candle 07:45–08:00, confirmation candle 08:15–08:30, entries 08:30–08:45, and prior weekday NY range 08:00–16:00. It waits for completion and uses the current price for the proposal rather than a historical close. This explicitly changes summer/winter SAST entry times and requires new evidence.

ICT Swing's four retracement formulas now measure retracement from the impulse end (62–79%), rather than progress from its start (21–38% pullbacks). NY-open entries are no longer approved merely because the same OTE formula generates a high confidence score. These are changes to the experiment; old results cannot validate the new rules.

Swing v2 uses explicit New York research windows: Asia 19:00–24:00 of the prior evening, London 02:00–05:00, NY 07:00–10:00, and London close 10:00–12:00. Eligible HIGH windows are 02:00–05:00, 07:00–08:00, and 09:30–12:00. NY-open 08:00–09:30 is withheld because the old score was circular. These window choices are research parameters, not established profitable hours; changing them is distinct from fixing timezone arithmetic. Both US DST transitions have regression coverage. London-labelled ICT windows follow the chosen New York model, not the separate UK clock.

Swing and ATM additionally require a completed M1 directional reaction through the previous candle extreme following a recent zone touch. ATM's structural break requires an H1 close through the level; its M1 reaction must occur after that H1 bar completes. Mere proximity no longer authorizes an order. Stable setup identities prevent another recorded entry into the same ATM key/break or the same Swing session/day/direction. These confirmation and deduplication policies are hypotheses to compare with the baseline, not proven improvements.

### Trade lifecycle

Reconciliation distinguishes unavailable broker positions from a confirmed empty list. On restart, live positions bearing this bot's magic are adopted using actual entry, stop, target, broker open time, and stored strategy label when available. Unknown recovered positions have no invented timeout. Per-engine holding periods are explicit research settings: Farmer 10 minutes, ATM and Swing 120, 1HSMA 120, CIS 60, Event 10. These settings need ablation tests, not assumptions of optimality. Loss-minimizer deferral is disabled for the first controlled baseline.

Reconciliation and the polling wait execute in `finally`, including after a gate's `continue`. SQLite connections are explicitly closed, avoiding Windows backup/test locks. Recent-history queries compare real instants with SQLite date functions, including mixed legacy timestamp formats and UTC offsets. Trade-management logging no longer depends on emoji-capable consoles.

## Farmer v2 hypothesis

This is a dedicated M1 trend-pullback model rather than a burst of orders copied from any non-HOLD ensemble vote. It evaluates each newly completed minute bar, independently of LOW/MEDIUM/HIGH switches, subject to the existing Farmer switch, overall trading arm, session, engine mode, and shared execution gate. It never forces an entry just to stay busy.

- At least 60 contiguous M1 candles.
- Long: EMA20 above EMA50 and rising over three intervals; prior bar touches EMA20; latest completed close breaks prior high. Short is symmetric.
- Stop beyond the last five-bar extreme with 0.1 ATR buffer.
- Target: $2 account profit plus a configurable estimated round-trip cost allowance, converted to a broker price AFTER choosing volume. USD accounts only for this version.
- Intended risk: at most 0.1% equity and $2, including the configured cost allowance. A small account may be unable to fit minimum volume and should remain flat.
- Dollar daily loss budget: $5, plus the stricter shared account limit. Cooldown: 120 seconds after recent Farmer activity, recovered from broker deals, not just memory.
- Net target must cover at least 1x proposed stop risk; estimated spread plus cost allowance must be no more than 25% of target. The $0.15 allowance is an assumption to calibrate against the actual broker, not a measured fee.
- Farmer setup IDs are persisted, so a recorded entry cannot be repeated after a restart on the same bar/direction.
- Farmer competes for the same one-position budget. Continuous monitoring does not mean continuous exposure or guaranteed daily income.

## Dashboard interpretation

Indicator confidence is labelled as an alignment score. Claimed success percentages are unmeasured, not derived from that score. The assumed $10,000 dashboard account and tier-dependent 1.5–2.5% sizing are replaced with actual broker equity and the configured risk budget. Projected rewards are mathematical budget scenarios, not actual fills or net profit forecasts. Farmer exposes its latest waiting/blocker reason instead of a countdown promising a trade.

## Validation and next evidence

Automated tests cover submission refusals, actual-entry sizing, minimum volume, account-wide exposure, failed reads, delayed position visibility, Farmer dollar targets and daily limits, completed UTC candles, report handling of unknown outcomes, database migration, and confirmed broker exits. See `docs/research/validation-2026-10-27.md` for actual results and limits.

The existing generic backtester is not approved for profitability decisions. No out-of-sample MT5 replay or live forward test has been completed for these changes. Historical replay, a random-entry comparator with identical exits/costs, execution integration on the VM, independent setup counts, realistic spread/slippage stress, and configuration sensitivity remain required. Prioritize accurate baseline evidence over adding more filters.

EC2 next: use `python analysis/backup_database.py` with the running bot's interpreter to create a consistent backup through SQLite's backup API, including committed WAL data without stopping monitoring. The script refuses to overwrite an existing snapshot or the source and runs an integrity check. Alternatively, stop the scheduled task before making a raw file copy. Export MT5 deal history, and record the deployed revision plus non-secret effective settings and enabled engines. Compare broker fills against database entries before any profitability conclusion. The local database ends on 10 September 2026 and contains no October results.

Generate read-only reports with:

```powershell
python analysis/performance_report.py data/trades.sqlite --output docs/research/local-history-report.json
python analysis/performance_report.py PATH_TO_EC2_COPY.sqlite --since 2026-10-01T00:00:00Z --output docs/research/october-report.json
```

Evaluate each fixed strategy version separately. Target at least 100 independent setups across multiple weeks and regimes before an initial assessment, then confirm on an untouched period. This is a minimum research sample, not statistical proof. Report missing outcomes, net expectancy, win/loss sizes, profit factor, drawdown from broker equity, costs, worst day, and results by session. Any missing costs/outcomes qualify the conclusions. Increasing risk to recover past losses is not a remediation step.
