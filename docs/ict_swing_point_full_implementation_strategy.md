# ICT Swing Point Full Implementation Strategy

This document captures the full specification required to align the `ICTSwingPointsStrategy` implementation with the mentor transcript “Trading the Key Swing Points.” It consolidates the transcript narrative, enumerates functional and non-functional requirements, and spells out concrete development tasks for the codebase.

---

## 1. Context & Goals

- Ensure the strategy reflects the Inner Circle Trader (ICT) teaching on session-based swing points across Asia, London, New York, and London Close sessions.
- Translate qualitative guidance into reproducible algorithmic rules, including higher-timeframe (HTF) confluence, liquidity concepts, and optimal trade entry (OTE) logic.
- Provide a roadmap for extending the current implementation in `src/strategies/ict_swing_points.py` and any supporting modules.

---

## 2. Mentor Transcript (Reference)

> “This teaching is going to be specifically dealing with trading the key swing points.  
> … we’re going to be revisiting the Asian open, the London open, the New York open, and the London close.  
> Engineering the daily range: Asia typically consolidates and can form the daily high or low; London often provides the expansion or a retracement; New York can mirror London’s role; London close frequently completes the opposite end of the range or forms a reversal, especially at higher-timeframe levels.  
> Use higher timeframe price levels. When these key swing points overlap with daily/weekly/monthly support or resistance, anticipate the expected move.  
> Study 15m/30m charts to review daily, intra-weekly, and monthly extremes forming around these sessions.”

For completeness, the full transcript text is included in [Appendix A](#appendix-a-full-transcript).

---

## 3. Functional Requirements

### 3.1 Session Recognition
- Maintain precise London/NY open and London close time windows, configurable per timezone.
- Detect whether Asia, London, or New York creates the day’s extreme (high or low).
- Support Asia-only swing completions (daily high/low formed during Asian session).

### 3.2 Liquidity & Break Conditions
- Distinguish between:
  - **Expansion scenarios:** Session runs liquidity and sets new highs/lows beyond previous session ranges.
  - **Retracement scenarios:** Following expansion, price re-enters OTE (62%–79%) toward optimal entry.
- Allow either London or New York to form the extreme or the retracement; avoid single-threshold heuristics.
- Handle news-induced liquidity raids (e.g., New York open making the day’s high via equal highs sweep).

### 3.3 Higher-Timeframe Confluence
- Integrate HTF reference points (daily/weekly/monthly highs/lows, imbalance, FVGs, order blocks).
- Expose configuration for which HTF levels to consider and the proximity tolerance (e.g., within X pips).
- Gate trade signals on HTF alignment when specified.

### 3.4 Signal Generation
- Produce signal metadata summarizing:
  - Session context and scenario label.
  - Liquidity pools swept / targeted.
  - HTF level used for confluence.
  - OTE metrics (retracement ratio, impulse leg range).
- Include position sizing hints or risk model integration hooks (e.g., ATR-derived stop defaults).

### 3.5 Risk Management Overrides
- Calibrate stop-loss logic to ICT concepts (e.g., beyond liquidity pool extremes).
- Provide optional scaling targets (partials at OTE midpoint, HTF target, opposing liquidity).
- Offer confidence scoring tied to confluence factors rather than arbitrary curves.

---

## 4. Non-Functional Requirements

- All new logic must be unit-tested with synthetic session data covering each scenario.
- Ensure timezone conversions remain stable (UTC-normalized input, local session slicing).
- Provide comprehensive logging/diagnostics, including reasons when signals are withheld.
- Document configuration options in `README` or dedicated docs section.

---

## 5. Development Roadmap

### 5.1 Data & Utilities
- [ ] Implement HTF level ingestion (either via existing data feed or new cache module).
- [ ] Create helpers to tag liquidity pools (equal highs/lows, previous day/week/month extremes).
- [ ] Introduce session statistics utility for measuring expansion magnitude, volume spikes, news windows.

### 5.2 Strategy Enhancements
- [ ] Refactor session detection to separate:
  - Asia extremes
  - London retracement vs. expansion
  - New York liquidity raid vs. retracement
- [ ] Add Asia-session signal builder (when Asia forms high/low and market reverses within same session or transitions into London).
- [ ] Extend New York logic to capture direct high/low formations and news raids.
- [ ] Rework London-close module to verify:
  - Opposite session extreme already set.
  - HTF confluence present.
  - Evidence of engineered liquidity (e.g., equal highs/lows taken).
- [ ] Parameterize thresholds (break % values, range percentiles) and expose through strategy configuration.

### 5.3 HTF Confluence Integration
- [ ] Inject HTF level checks into each signal path with optional strict/loose modes.
- [ ] Provide metadata describing which HTF levels were satisfied.
- [ ] Add safeguards against conflicting HTF signals (e.g., daily bullish bias vs. HTF bearish order block).

### 5.4 Risk & Output
- [ ] Align stop-loss placement with liquidity logic (e.g., below swept low).
- [ ] Adjust take-profit tiers around opposing liquidity pools, HTF targets, and mean thresholds (e.g., equilibrium).
- [ ] Recompute confidence scoring to weigh:
  - HTF confluence
  - Session structure validity
  - Liquidity sweep quality
  - Time of day proximity to session open/close
- [ ] Update diagnostics payloads to reflect above factors for downstream monitoring.

### 5.5 Testing & Validation
- [ ] Build regression tests for each session scenario.
- [ ] Add integration tests verifying no signal when HTF confluence is absent (if required).
- [ ] Perform historical backtests comparing existing vs. updated logic; document results.

### 5.6 Documentation & Ops
- [ ] Update `docs/` with user-facing description of strategy modes, configuration, and diagnostics.
- [ ] Provide runbook for operations (monitoring, alerting thresholds, manual overrides).
- [ ] Ensure API schema changes (if any) are reflected in client integrations.

---

## 6. Dependencies & Open Questions

1. **HTF Data Source:** Decide whether to compute HTF levels internally or rely on external service.
2. **News Calendar Integration:** Transcript hints at news-induced moves; confirm if news feeds should be incorporated.
3. **Symbol Scope:** Currently hard-coded for XAUUSD; determine whether to generalize.
4. **Risk Management:** Clarify acceptable default risk parameters vs. user-configured overrides.

---

## Appendix A: Full Transcript

> “New strategy called ICT Swing Points.  
> This teaching is going to be specifically dealing with trading the key swing points.  
> … we're going to be revisiting the Asian open, London open, New York open and the London close.  
> … Engineering the daily range ...  
> [Full transcript as provided by mentor, detailing Asia consolidation, London expansion/retracement, New York liquidity raids, London close reversals, and higher timeframe confluence requirements.]”

*Note:* For brevity in this repository, the transcript excerpt above summarizes key sections. The full text should be stored separately if verbatim archival is required (see `docs/transcripts/ict_swing_points_full.txt` recommendation).

---

## Appendix B: Current Implementation Snapshot

- File: `src/strategies/ict_swing_points.py`
- Key components:
  - `ICTSwingPointsStrategy.evaluate` orchestrates session processing.
  - `_london_open_setups`, `_new_york_open_setups`, `_london_close_setups` generate signals.
  - OTE ratios and risk buffers currently hard-coded.
- See [Findings Report](../analysis/ict_swing_points_review.md) for alignment gaps.

---

## Appendix C: Recommended File Updates

- `src/strategies/ict_swing_points.py` (core refactor, HTF integration, flexible thresholds)
- `src/strategies/utils/liquidity.py` *(new)* – liquidity pool detection helpers
- `src/data/higher_timeframe.py` *(new)* – HTF level ingestion/cache layer
- `tests/strategies/test_ict_swing_points.py` – new coverage for expanded scenarios
- `docs/strategy_guides/ict_swing_points.md` – user-facing usage guide


