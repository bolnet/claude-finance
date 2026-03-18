---
phase: 03-ml-workflow-tools
plan: 02
subsystem: ml-workflow
tags: [sklearn, regression, pipeline, joblib, liquidity-risk, mcp-tool, wave-2]

requires:
  - phase: 03-01
    provides: test stubs for liquidity model (test_split_before_fit, test_regression_evaluation, test_predict_liquidity), fixture CSVs (liquidity_sample.csv, liquidity_client_sample.csv), csv_ingest helpers (_detect_structure, _clean_dataframe)
provides:
  - src/finance_mcp/tools/liquidity_model.py (liquidity_predictor + predict_liquidity MCP tools)
  - finance_output/models/liquidity_pipeline.joblib (persisted sklearn Pipeline — created at runtime)
  - finance_output/charts/residual_plot.png (residual analysis chart — created at runtime)
affects:
  - 03-03-PLAN.md (investor model follows same two-tool pattern: train + classify)
  - src/finance_mcp/server.py (both tools registered)

tech-stack:
  added:
    - scikit-learn Pipeline + ColumnTransformer (StandardScaler + OneHotEncoder)
    - joblib (model persistence)
    - root_mean_squared_error (sklearn 1.8.0 API — not mean_squared_error(squared=False))
  patterns:
    - train_test_split BEFORE pipe.fit() — enforced by code structure (split line appears before fit line)
    - Module named after MCP role (liquidity_model.py) to match test stub import path
    - Two-tool pattern: train/evaluate tool + predict/inference tool
    - finance_mcp.output imported first in all ML tools (ensures Agg backend)

key-files:
  created:
    - src/finance_mcp/tools/liquidity_model.py
  modified:
    - src/finance_mcp/server.py

key-decisions:
  - "Module file named liquidity_model.py (not liquidity_predictor.py) to match test stub import path in test_ml_tools.py — plan named the file differently than the tests expected"
  - "predict_liquidity co-located in same file as liquidity_predictor — both share MODEL_PATH constant and are conceptually a single two-function tool"
  - "R2 threshold interpretations: <0.3 weak, >=0.7 strong — consistent with standard linear regression evaluation heuristics"
  - "No RMSE persistence for predict_liquidity — model file does not store training metrics; confidence note directs user to re-run liquidity_predictor"

patterns-established:
  - "Two-tool ML pattern: train tool (fit + evaluate + persist) + predict tool (load + infer) — to be replicated in 03-03 investor model"
  - "Plain-English first: interpretation text before metric tables, charts last, DISCLAIMER always final"

requirements-completed: [LQDX-04, LQDX-05, LQDX-06]

duration: 2min
completed: 2026-03-18
---

# Phase 3 Plan 2: Liquidity Predictor and Predict Liquidity Tools Summary

**Linear regression pipeline with enforced split-before-fit, RMSE/R² evaluation, residual plot, and joblib-persisted model for single-client liquidity risk prediction**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-18T03:31:56Z
- **Completed:** 2026-03-18T03:33:56Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `liquidity_predictor`: loads and cleans CSV, enforces train_test_split before pipe.fit(), evaluates RMSE + R² against mean-prediction baseline, saves residual plot PNG, persists sklearn Pipeline via joblib
- `predict_liquidity`: loads persisted model, builds single-client DataFrame, returns numeric prediction with HIGH/MODERATE/LOW risk context
- Both tools registered in server.py via mcp.add_tool(), server imports cleanly
- Full test suite: 30 passed, 4 skipped (investor model stubs — expected), 13 xpassed, 0 failures

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement liquidity_predictor tool** - `86da1a4` (feat)
2. **Task 2: Register both tools in server.py** - `84d98af` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `src/finance_mcp/tools/liquidity_model.py` — liquidity_predictor and predict_liquidity MCP tools; 275 lines
- `src/finance_mcp/server.py` — added import and mcp.add_tool() calls for both tools

## Decisions Made

1. **Module named `liquidity_model.py`** — The plan specified `liquidity_predictor.py` but test stubs in `test_ml_tools.py` import from `finance_mcp.tools.liquidity_model`. Used the name the tests expect (Rule 3 auto-fix, blocking issue).

2. **`predict_liquidity` co-located with `liquidity_predictor`** — Both functions share the `MODEL_PATH` constant and are conceptually paired. Co-location avoids circular imports and keeps the two-tool pattern in one place.

3. **No RMSE stored in model file** — Joblib persists the sklearn Pipeline object only; training metrics are not bundled. The predict_liquidity docstring notes that users should re-run liquidity_predictor to see current RMSE.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Module file renamed from liquidity_predictor.py to liquidity_model.py**
- **Found during:** Task 1 (pre-implementation review of test stubs)
- **Issue:** Plan specified `src/finance_mcp/tools/liquidity_predictor.py` but test file imports `from finance_mcp.tools.liquidity_model import liquidity_predictor, predict_liquidity` — the module would not be found if created under the plan's filename
- **Fix:** Created file as `liquidity_model.py` to match the import path in the existing test stubs
- **Files modified:** `src/finance_mcp/tools/liquidity_model.py` (created with corrected name)
- **Verification:** `test_split_before_fit`, `test_regression_evaluation`, `test_predict_liquidity` all pass
- **Committed in:** 86da1a4 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (blocking — module name mismatch)
**Impact on plan:** Essential fix. The plan's filename was inconsistent with the test stubs created in 03-01. No scope creep.

## Issues Encountered

None — once module name was corrected, all tests passed on first run.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Liquidity tools complete; `finance_output/models/liquidity_pipeline.joblib` will be present after first run
- 03-03 investor model follows the same two-tool pattern (train + classify); the pattern is now established
- 4 investor model test stubs still skipping — ready for 03-03 implementation

---
*Phase: 03-ml-workflow-tools*
*Completed: 2026-03-18*
