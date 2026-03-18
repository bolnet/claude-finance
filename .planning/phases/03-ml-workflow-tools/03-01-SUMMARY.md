---
phase: 03-ml-workflow-tools
plan: 01
subsystem: ml-infrastructure
tags: [csv-ingest, test-stubs, fixtures, eda, mcp-tool, wave-1]
dependency_graph:
  requires: []
  provides:
    - tests/test_ml_tools.py (14 stubs — LQDX + INVX coverage)
    - tests/data/liquidity_sample.csv
    - tests/data/liquidity_client_sample.csv
    - tests/data/investor_sample.csv
    - tests/data/investor_sample_2.csv
    - src/finance_mcp/tools/csv_ingest.py (ingest_csv MCP tool)
  affects:
    - src/finance_mcp/server.py (ingest_csv registered)
    - 03-02-PLAN.md (depends on fixture CSVs and test stubs)
    - 03-03-PLAN.md (depends on fixture CSVs and test stubs)
tech_stack:
  added:
    - pandas (select_dtypes, IQR outlier removal, median fill)
    - numpy (numeric dtype detection)
    - matplotlib (EDA histograms via Agg backend)
  patterns:
    - TDD RED-GREEN: stubs first, implementation second
    - Immutable DataFrame operations (df.copy() throughout)
    - IQR (1.5x) outlier removal followed by median imputation
    - MCP tool registration via mcp.add_tool() (not decorator)
    - finance_mcp.output imported first (ensures Agg backend)
key_files:
  created:
    - tests/test_ml_tools.py
    - tests/data/liquidity_sample.csv
    - tests/data/liquidity_client_sample.csv
    - tests/data/investor_sample.csv
    - tests/data/investor_sample_2.csv
    - src/finance_mcp/tools/csv_ingest.py
  modified:
    - src/finance_mcp/server.py
decisions:
  - "pandas select_dtypes uses 'object' and 'string' for cat_cols (not 'str') — tested pandas 3.x behavior; 'str' dtype alias not recognized for select_dtypes"
  - "IQR outlier filter preserves NaN rows during outlier pass then fills with median in second pass — avoids removing valid rows that happen to have NaN in another column"
  - "EDA charts limited to first 4 numeric columns — keeps test runtime reasonable; all columns still appear in describe() data_section"
metrics:
  duration: "2 min 29 sec"
  completed_date: "2026-03-18"
  tasks_completed: 2
  files_created: 6
  files_modified: 1
---

# Phase 3 Plan 1: ML Test Infrastructure and ingest_csv Tool Summary

One-liner: TDD test scaffold with 14 named stubs, 4 deterministic fixture CSVs, and a working ingest_csv MCP tool with IQR cleaning and EDA chart generation.

## Tasks Completed

| # | Task | Commit | Status |
|---|------|--------|--------|
| 1 | Create test stubs and fixture CSVs (Wave 0) | deee738 | Done |
| 2 | Implement ingest_csv MCP tool and register in server.py | 3bebc7d | Done |

## What Was Built

**Task 1 — Test infrastructure:**
- `tests/test_ml_tools.py`: 14 named test stubs covering all LQDX (liquidity) and INVX (investor) requirements
- Wave 2/3 stubs skip gracefully via `pytest.skip()` when tool modules are absent — pytest collection has zero errors
- 4 fixture CSVs with deterministic content, deliberate outliers, and deliberate missing values matching the plan spec

**Task 2 — ingest_csv MCP tool:**
- `_detect_structure(df)`: detects numeric and categorical column types, counts missing values
- `_clean_dataframe(df, numeric_cols)`: IQR outlier removal (1.5x rule) + median fill for missing values; immutable (df.copy() throughout)
- `ingest_csv(csv_path, target_column)`: full MCP tool — validates path, reads CSV, cleans data, generates EDA histograms, returns `format_output()` result
- EDA charts saved to `finance_output/charts/eda_*.png` (up to 4 numeric columns)
- `ToolError` raised for missing paths (not raw `FileNotFoundError`)
- Registered in `server.py` via `mcp.add_tool(ingest_csv)`

## Test Results

```
47 tests: 27 passed, 7 skipped, 13 xpassed
- Phase 2 tests: fully green
- ingest_csv tests (5): all PASS
- Wave 2/3 stubs (7): SKIP (tools not yet implemented — expected)
```

## Decisions Made

1. **`select_dtypes` uses `'object'` not `'str'`** — The plan spec said `include=['str']` for pandas 3.x but `'str'` is not a valid dtype alias for `select_dtypes`. Used `include=['object', 'string']` which correctly catches all string/categorical columns. This is the correct pandas behavior across 1.x-3.x.

2. **NaN rows preserved during IQR outlier pass** — Filter uses `cleaned[col].isna() | (bounds condition)` so rows with NaN in the column being filtered are not removed by the IQR pass. They are then filled with median in the second pass. This prevents valid rows being dropped simply because they have a missing value in one column.

3. **EDA charts capped at 4 numeric columns** — Keeps test suite runtime short (avoids generating 6+ charts per test run) while still producing representative visualizations.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] pandas `select_dtypes(include=['str'])` does not match string columns**
- **Found during:** Task 2 implementation
- **Issue:** Plan specified `'str'` dtype for pandas 3.x cat_cols detection, but `select_dtypes(include=['str'])` returns empty results — `'str'` is not a recognized dtype alias
- **Fix:** Changed to `include=['object', 'string']` which matches all string/categorical data regardless of pandas version
- **Files modified:** `src/finance_mcp/tools/csv_ingest.py`
- **Commit:** 3bebc7d (included in Task 2 commit)

## Self-Check

### Files created/modified
- [x] tests/test_ml_tools.py — FOUND
- [x] tests/data/liquidity_sample.csv — FOUND
- [x] tests/data/liquidity_client_sample.csv — FOUND
- [x] tests/data/investor_sample.csv — FOUND
- [x] tests/data/investor_sample_2.csv — FOUND
- [x] src/finance_mcp/tools/csv_ingest.py — FOUND
- [x] src/finance_mcp/server.py — MODIFIED

### Commits
- [x] deee738 — test(03-01): add 14 ML test stubs and 4 fixture CSVs
- [x] 3bebc7d — feat(03-01): implement ingest_csv MCP tool and register in server.py

## Self-Check: PASSED
