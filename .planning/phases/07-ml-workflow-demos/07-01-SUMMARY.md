---
phase: 07-ml-workflow-demos
plan: "01"
subsystem: demo-data
tags: [tdd, data, csv, ml-workflow]
dependency_graph:
  requires: []
  provides: [demo/sample_portfolio.csv]
  affects: [demo/demo.md steps 9-11, liquidity_model.py, investor_model.py, csv_ingest.py]
tech_stack:
  added: []
  patterns: [numpy seed-based synthetic data generation, TDD RED-GREEN]
key_files:
  created:
    - demo/sample_portfolio.csv
    - tests/test_sample_csv.py
  modified: []
decisions:
  - "numpy.random.default_rng(42) used for reproducibility (modern Generator API over legacy RandomState)"
  - "Segment boundaries [0, 0.35) conservative / [0.35, 0.65) moderate / [0.65, 1.0] aggressive yield balanced 35/35/30 distribution"
metrics:
  duration: "3 min"
  completed_date: "2026-03-18"
requirements: [MLWF-01]
---

# Phase 7 Plan 1: Sample Portfolio CSV Summary

**One-liner:** 100-row synthetic portfolio CSV with seed=42 satisfying liquidity_model and investor_classifier column schemas, validated by 13 pytest assertions.

## What Was Built

`demo/sample_portfolio.csv` — a bundled 100-row synthetic dataset with 9 columns covering both ML tool schemas. The file is deterministic (numpy seed=42), loadable by all three ML tools without column errors, and ready for use in demo steps 9-11.

`tests/test_sample_csv.py` — 13 schema validation tests verifying file existence, column completeness, row count, numeric ranges, categorical value sets, and per-class balance.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create sample CSV and schema tests (TDD) | 438dbdc | demo/sample_portfolio.csv, tests/test_sample_csv.py |

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- `demo/sample_portfolio.csv` exists: FOUND
- `tests/test_sample_csv.py` exists: FOUND
- Commit 438dbdc: FOUND
- All 13 tests: PASSED
