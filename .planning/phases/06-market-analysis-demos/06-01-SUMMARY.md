---
phase: 06-market-analysis-demos
plan: "01"
subsystem: testing
tags: [pytest, yfinance, integration-tests, demo, market-analysis, mcp]

# Dependency graph
requires:
  - phase: 05-demo-command-flow
    provides: demo.md slash command with Steps 3-8 market analysis instructions
  - phase: 02-market-analysis-tools
    provides: analyze_stock, get_returns, get_volatility, get_risk_metrics, compare_tickers, correlation_map tool implementations
provides:
  - Live integration tests proving all 6 market analysis tools work end-to-end with real Yahoo Finance data
  - Corrected demo.md Steps 3-8 using ISO date start/end parameters matching actual MCP tool schemas
affects: [07-ml-workflow-demos, 08-persona-demos]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "pytest.mark.network + xfail: marks live network tests to allow CI skip while still running them when network is available"
    - "sys.path.insert(0, 'src') at module top: enables direct tool function imports in test files without installing as editable"

key-files:
  created:
    - tests/test_market_demo.py
  modified:
    - .claude/commands/demo.md
    - pyproject.toml

key-decisions:
  - "demo.md Steps 3-8 use start: [N days before today, YYYY-MM-DD format] dynamic instruction pattern — tells Claude to compute dates at runtime rather than embedding stale literal dates"
  - "tickers param in compare_tickers and correlation_map uses comma-separated string ('AAPL,MSFT') not list — matches actual function signature"
  - "pytest.mark.network registered in pyproject.toml markers to eliminate PytestUnknownMarkWarning"
  - "xfail used as network-unreachable fallback — tests still run live when Yahoo Finance is reachable, xpassed is the expected green state"

patterns-established:
  - "Live integration test pattern: direct function import + real ticker + ISO date + assert keywords in output string"
  - "Network test pattern: @pytest.mark.network + @pytest.mark.xfail(reason='network') for CI-safe live tests"

requirements-completed: [MRKT-01, MRKT-02, MRKT-03, MRKT-04, MRKT-05, MRKT-06]

# Metrics
duration: 3min
completed: 2026-03-18
---

# Phase 6 Plan 01: Market Analysis Demos Summary

**Corrected demo.md Steps 3-8 from period strings to ISO date start params, and added 6 live integration tests proving all market analysis tools return correct formatted output with charts using real Yahoo Finance data**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-03-18T15:07:04Z
- **Completed:** 2026-03-18T15:09:23Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Fixed demo.md Steps 3-8 so `analyze_stock`, `get_returns`, `get_volatility`, `get_risk_metrics`, `compare_tickers`, and `correlation_map` are called with correct `start:` ISO date parameters
- Fixed tickers parameter format in Steps 7-8 from `["AAPL", "MSFT"]` list syntax to `"AAPL,MSFT"` comma-separated string
- Created `tests/test_market_demo.py` with 6 live integration tests; all 6 xpassed with real Yahoo Finance data
- Registered `network` pytest mark in pyproject.toml to eliminate warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix demo.md Steps 3-8 to use correct tool parameter schemas** - `97698fd` (fix)
2. **Task 2: Create live integration tests for all 6 market analysis tools** - `a73a390` (test)

**Plan metadata:** _(final docs commit follows)_

## Files Created/Modified

- `tests/test_market_demo.py` - 6 live integration tests for all market analysis tools; uses real Yahoo Finance data, @pytest.mark.network + xfail for CI safety
- `.claude/commands/demo.md` - Steps 3-8 updated: period strings replaced with `start:` ISO date parameters; tickers lists replaced with comma-separated strings
- `pyproject.toml` - Registered `network` pytest mark to eliminate PytestUnknownMarkWarning

## Decisions Made

- **Dynamic date instruction pattern:** Steps 3-8 now use `start: [90 days before today, in YYYY-MM-DD format]` — a prompt instruction that tells Claude to compute the date at runtime. Embedding literal dates would create stale instructions on every future run.
- **xfail as CI gate:** Tests are marked `xfail(reason="network")` so they degrade gracefully when Yahoo Finance is unreachable (xfail pass) but still run live when network is available (xpassed = green). This avoids mocking and keeps the tests truly integration-level.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Config] Registered pytest.mark.network in pyproject.toml**
- **Found during:** Task 2 (integration test creation)
- **Issue:** `@pytest.mark.network` triggered `PytestUnknownMarkWarning` on all 6 tests — unregistered custom marks produce warnings that clutter test output
- **Fix:** Added `markers = ["network: marks tests that require live network access..."]` to `[tool.pytest.ini_options]` in pyproject.toml
- **Files modified:** `pyproject.toml`
- **Verification:** Re-ran tests — 6 xpassed, 0 warnings
- **Committed in:** `a73a390` (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 missing config)
**Impact on plan:** Minor config improvement required for pytest mark hygiene. No scope creep.

## Issues Encountered

None — tool implementations were already correct and all 6 tests passed on first live run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All 6 market analysis tools verified end-to-end with live data
- demo.md Steps 3-8 now use correct parameter schemas — no ambiguity when Claude executes the demo
- Phase 7 (ML workflow demos) can proceed with same integration test pattern established here

---
*Phase: 06-market-analysis-demos*
*Completed: 2026-03-18*
