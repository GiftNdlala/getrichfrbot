# Roadmap proposal

This is a documentation-only roadmap based on the audited code path and the observed risk patterns.

## Phase 0 — stop the bleeding

1. Disable the repeated high-tier engine by default.
2. Fail closed if all real quote sources are unavailable.
3. Require an explicit demo-account check before live trading.
4. Set real daily loss / open-risk enforcement before any new order can be placed.

Acceptance test: the bot refuses to place a new order when the runtime risk gate is breached or the feed is synthetic only.

## Phase 1 — correctness of the core trade lifecycle

1. Enforce `max_concurrent_trades` and `max_open_risk_pct`.
2. Ensure `get_position_size_multiplier()` is wired into the live sizing path or deleted if unused.
3. Fix `register_new_order()` / `reconcile()` mismatches so `CLOSED` is only written after a real close succeeds.
4. Apply a proper per-engine time cap instead of falling through to a default 10-minute timeout.
5. Anchor orders to actual fill price, not the signal price.
6. Make synthetic quotes non-tradable by design.
7. Move the reconcile/wait logic so it always runs even when the loop hits a temporary gate.

Acceptance test: a trade record contains the actual fill price, the signal price, the source, and the close outcome in a single traceable chain.

## Phase 2 — strategy hygiene and separation of concerns

1. Separate strategy selection from execution logic.
2. Force every strategy to declare its own gate and cooldown logic.
3. Standardize signal metadata: source, strategy, alert level, setup id, and spread.
4. Give each strategy a unique, non-lossy order tag.

Acceptance test: each order can be matched back to one origin signal and one runtime data source.

## Phase 3 — observability and trust

1. Add an order-level audit log.
2. Record bid/ask, point, spread, entry fill, intended SL/TP, actual close, and source.
3. Persist runtime state required for restart recovery.
4. Export a full labelled trade history with strategy + setup + reason + source.

Acceptance test: a full trade export can be reconstructed from the local database without relying on the broker export alone.

## Phase 4 — research and validation

1. Replay each strategy under a minimal random baseline.
2. Test with and without breakeven and time-based exits.
3. Compare strategy outputs by regime, session, and direction.
4. Check whether the signal engine contributes edge versus repeated noise.

Acceptance test: a report shows, for each strategy, the net effect of the signal engine after controlling for frequency, exit rules, and data source.
