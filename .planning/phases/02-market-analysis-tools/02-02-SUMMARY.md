---
phase: 02-market-analysis-tools
plan: "02"
subsystem: api
tags: [yfinance, pandas, numpy, matplotlib, fastmcp, returns, volatility, sharpe, drawdown, beta]

# Dependency graph
requires:
  - phase: 02-01
    provides: analyze_stock price_chart tool, adapter layer, output conventions (format_output, save_chart, DISCLAIMER)
  - phase: 01-infrastructure-mcp-scaffold
    provides: FastMCP server scaffold, .venv environment, mcp.add_tool() registration pattern
provides:
  - get_returns MCP tool (daily + cumulative returns, two-subplot chart)
  - get_volatility MCP tool (annualized vol, rolling 21-day chart)
  - get_risk_metrics MCP tool (Sharpe ratio, max drawdown, beta vs ^GSPC)
  - _compute_risk_metrics() pure function for isolated unit testing
  - 7 new passing tests in test_market_tools.py
affects: [02-03, 02-04, phase-03-machine-learning]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Pure-function inner helper (_compute_risk_metrics) pattern for testability without mocking I/O
    - Tool module output.py import-first to guarantee Agg backend before pyplot
    - mcp.add_tool() registration (not decorator) for all Phase 2 tools

key-files:
  created:
    - src/finance_mcp/tools/returns.py
    - src/finance_mcp/tools/volatility.py
    - src/finance_mcp/tools/risk_metrics.py
  modified:
    - src/finance_mcp/server.py
    - tests/test_market_tools.py

key-decisions:
  - "_compute_risk_metrics exposed as public function — allows direct unit testing of Sharpe/drawdown/beta math without mocking fetch_price_history or the full tool I/O"
  - "Sharpe ratio computed with rf=0; FRED integration deferred and noted in output text as future enhancement"
  - "get_risk_metrics fetches ^GSPC benchmark separately via same fetch_price_history adapter — reuses existing validation and error handling"

patterns-established:
  - "Pure inner helper pattern: complex math extracted to _compute_X() with no I/O, registered tool wraps it with fetch + format_output"
  - "All tool modules start with: from finance_mcp.output import save_chart, format_output  # import before pyplot"

requirements-completed: [MKTX-02, MKTX-03, MKTX-04, MKTX-07]

# Metrics
duration: 7min
completed: 2026-03-18
---

# Phase 2 Plan 02: Market Analysis Metric Tools Summary

**Three quantitative MCP tools (returns, volatility, risk metrics) built on pct_change/cumprod formulas with Sharpe/drawdown/beta math, driving 7 failing stubs to green.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-18T01:48:14Z
- **Completed:** 2026-03-18T01:55:00Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- get_returns tool: daily pct_change and compound cumulative returns with two-subplot bar+line PNG chart
- get_volatility tool: annualized std*sqrt(252) and 21-day rolling volatility with chart; formula verified numerically in test
- get_risk_metrics tool: Sharpe ratio (rf=0), max drawdown via wealth/cummax formula, beta via np.cov — all three verified against independent calculations in tests
- 7 new tests passing (total 9 in test_market_tools, 14 across full suite); 6 stubs remain for plans 02-03 and MKTX-07

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement get_returns and get_volatility tools; update 4 tests to green** - `d16b366` (feat)
2. **Task 2: Implement get_risk_metrics tool; update 3 tests to green** - `501cc7a` (feat)

**Plan metadata:** committed with docs commit after SUMMARY creation

## Files Created/Modified

- `src/finance_mcp/tools/returns.py` - get_returns MCP tool with pct_change/cumprod formulas and two-subplot chart
- `src/finance_mcp/tools/volatility.py` - get_volatility MCP tool with annualized vol and rolling 21-day window chart
- `src/finance_mcp/tools/risk_metrics.py` - get_risk_metrics and _compute_risk_metrics with Sharpe/drawdown/beta formulas
- `src/finance_mcp/server.py` - registered all three new tools via mcp.add_tool()
- `tests/test_market_tools.py` - replaced 7 stubs with real tests; 6 future stubs remain

## Decisions Made

- Exposed `_compute_risk_metrics()` as a public function (leading underscore marks internal but importable) to enable direct unit testing of formula correctness without mocking the full tool pipeline.
- Sharpe ratio uses rf=0; FRED integration for real risk-free rate is noted in tool output as a future enhancement and logged as a Phase 3 research item.
- get_risk_metrics fetches ^GSPC benchmark through the same fetch_price_history adapter rather than a hardcoded dataset — reuses all existing validation and DataFetchError handling.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All three metric tools registered and importable from server.py without errors
- test_market_tools.py has 9 passing, 6 future stubs (test_normalized_prices_start_at_100, test_compare_tickers_chart, test_correlation_uses_returns, test_correlation_map_chart, test_output_plain_english_first, test_output_ends_with_disclaimer) ready for plan 02-03
- Plan 02-03 (comparison tools) can import from adapter and output with no setup needed

---
*Phase: 02-market-analysis-tools*
*Completed: 2026-03-18*
