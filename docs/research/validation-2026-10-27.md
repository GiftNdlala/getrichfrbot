# Validation — 27 October 2026

Status: local engineering checks pass; not yet deployed or forward-tested on EC2.

## Completed checks

- 65 automated tests passed, with zero failures and errors. Full output: [test-results.txt](test-results.txt).
- Python source and test syntax parsed successfully, including the dashboard module.
- The dashboard's inline JavaScript parsed successfully with Node (one script block).
- Live-stream module imported successfully in the local test environment.
- Read-only performance reports generated from the existing local database. October selection contains zero records; no October result has been inferred.
- Git whitespace/diff checks passed before this documentation update; final review checks are recorded with the delivered changes.

The test runner used the bundled Python 3.12.14 interpreter and available bundled numeric libraries, with pure Python dependencies resolved from the copied environment when needed. The VM's native MT5/Python environment is a separate integration target. All broker order responses in the tests are simulated; no tests submitted live MT5 orders. SQLite migration, backup, timestamp filtering, and connection cleanup tests use temporary databases, not the historical database.

## Regression coverage

Shared execution: demo/account identity, fresh broker quotes and candle readiness, audit-storage readiness, session gating including Event, fixed and relative spread limits, failed position/order/history reads, global position capacity, outstanding acknowledged orders, unprotected exposure, final-entry risk sizing and quote drift, broker stop constraints, minimum lot refusal, funding versus trading profit, daily realized/floating loss, fees, progressive reduction, and long/short order sides.

Farmer: independent operation with HIGH disabled and no ensemble signal; positive completed-pullback candidate; refusal to force trades in a flat market; once-per-bar evaluation; dollar target conversion after volume selection; USD account requirement; daily loss attribution for a position opened on the preceding day; broker-based cooldown and shared limits.

Market/strategy: UTC M1 snapshots replace duplicates and exclude forming/stale bars; incomplete H1/M15 periods and future observations are excluded; exact completed boundaries are retained; NYUPIP uses aware UTC comparisons; US DST transitions retain the New York session clock; Asia is the preceding evening; OTE accepts the intended deep pullback instead of shallow progress; mere retest touches do not pass reaction confirmation.

Lifecycle: original broker open time survives adoption after restart; failed broker reads do not imply a close; failed close requests remain tracked and retry; confirmed exits aggregate fills and costs; absent broker exit deals retain tracking; explicit ATM holding period is respected; gate `continue` branches still reconcile and wait.

Persistence/reporting: legacy migration and trade events; deterministic Windows connection cleanup; mixed ISO timestamp formats and offsets; live WAL-safe backup and overwrite refusal; unknown trade outcomes cannot become wins; a 60% win rate can still have negative expectancy; no-history results remain unmeasured.

## What remains unverified

1. Native EC2/MT5 integration, symbol-specific lot/tick/filling constraints, actual fees and spread distribution, task scheduling, private dashboard access, and recovery across a real terminal disconnect/reboot. Run on a flat demo account with trading initially disarmed; do not silently change exit policies for existing positions mid-trade.
2. Current verified news coverage. No live calendar is bundled or fabricated; a missing/expired calendar intentionally blocks new entries while management continues. Automatic current-week calendar ingestion is now implemented; see 2026-10-28-startup-fix.md.
3. October broker-versus-database reconciliation and account attribution. Legacy records lack reliable account identity and may mix strategy versions/accounts; do not combine them into an account return. Reconcile against the correct MT5 account export, including unknown/duplicate tickets.
4. Forward demo results and out-of-sample historical replay using identical entry/exit/cost rules. The inherited generic stock-style backtester remains unapproved for MT5 profitability decisions.
5. Calibration of the $0.15 cost allowance, $2 target/loss cap, holding periods, session windows, and confirmation rules. They are declared research settings, not optimized parameters or evidence of edge. Equal-high/liquidity-pool refinements and comparisons against random entries remain research items.
6. Browser visual checks and real device interaction; only syntax and logic-level tests ran locally.
7. Previously tracked environment files remain in Git. New ignore rules prevent new environment/dependency files being added; the existing 6,822 tracked venv files were preserved rather than deleted during trading changes.

## Operator handover

Preserve the currently working VM revision. Use the standalone SQLite backup tool to collect committed October data without replacing the running bot. Save matching MT5 deals, logs, symbol specifications, revision, and non-secret effective settings. Once that evidence and a fresh verified calendar are available, smoke-test this version on demo, including explicit arming, refusal reasons, fills, stops, exits, disconnection, and restart. Re-run `python -m unittest discover -s tests -v` with the VM's installed dependencies before arming.

Aspirational 100% wins is not an acceptance guarantee. A roughly 60% observed win rate is acceptable to the owner, but approval also requires positive net expectancy, bounded equity drawdown, accurate attribution, and an untouched validation period. No account-return percentage is inferred from win rate.
