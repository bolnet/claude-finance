# Roadmap: Finance AI Skill for Claude Code

## Overview

Build a Claude Code native `/finance` slash command that lets finance professionals describe what they need in plain English and receive executed Python analysis — no coding required. The work flows in three natural delivery boundaries dictated by the dependency graph: first, lay the data-correct infrastructure that all workflows share; second, build the live-market analysis workflows that prove the write-then-execute pattern; third, implement the ML workflows (liquidity predictor and investor classifier) that complete the pyfi.com curriculum scope and deliver the primary competitive differentiators.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Infrastructure & Skill Scaffold** - Data-correct foundation, environment validation, output conventions, and slash command skeleton that all workflows depend on
- [ ] **Phase 2: Market Analysis Workflows** - Live stock analysis via yfinance — price charts, returns, volatility, risk metrics, multi-ticker comparison, correlation heatmap
- [ ] **Phase 3: ML Workflows** - Liquidity predictor (regression, ML 03) and investor classifier (classification, ML 05-06) on user-provided CSV data

## Phase Details

### Phase 1: Infrastructure & Skill Scaffold
**Goal**: The `/finance` command exists, connects to the Python environment, fetches adjusted price data correctly, writes results to the output directory, and surfaces user-friendly errors with a mandatory disclaimer on all outputs
**Depends on**: Nothing (first phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05, INFRA-06, INFRA-07, CMD-01, CMD-02, CMD-03, CMD-04
**Success Criteria** (what must be TRUE):
  1. Running `/finance` in Claude Code produces a response (not an error) and Claude can introspect the local Python environment before generating any code
  2. The yfinance adapter fetches `Adj Close` data (never raw `Close`) and raises a user-readable error if the ticker is invalid, the date range is empty, or the DataFrame is empty
  3. All chart output is written as PNG files to `finance_output/charts/` using the `Agg` backend — no `plt.show()` calls anywhere
  4. Every output — regardless of workflow — leads with a plain-English interpretation and ends with the hardcoded investment advice disclaimer
  5. Generated Python scripts are written to disk as `.py` files (Write tool) and then executed via Bash — never run as inline `-c` strings
**Plans**: TBD

Plans:
- [ ] 01-01: Command file, skill scaffold, and environment context injection
- [ ] 01-02: yfinance adapter layer, data validation wrapper, and output directory setup
- [ ] 01-03: Output formatting conventions — disclaimer template, plain-English header, chart save pattern

### Phase 2: Market Analysis Workflows
**Goal**: Users can request stock analysis in plain English and receive price charts, return metrics, risk statistics, multi-ticker comparisons, and correlation heatmaps — all with plain-English interpretation and no Python knowledge required
**Depends on**: Phase 1
**Requirements**: MKTX-01, MKTX-02, MKTX-03, MKTX-04, MKTX-05, MKTX-06, MKTX-07
**Success Criteria** (what must be TRUE):
  1. User can say "show me AAPL's price chart from 2023 to 2024" and receive a saved PNG chart with a plain-English summary of the price trend
  2. User can request daily and cumulative returns for any ticker and receive both a table and a chart, with volatility expressed in annualized percentage terms
  3. User can request risk metrics for a ticker and receive Sharpe ratio, max drawdown, and beta vs. S&P 500 — each explained in plain English with benchmark context
  4. User can compare 2-5 tickers side-by-side on a normalized price performance chart, with the interpretation noting which performed best and by how much
  5. User can request a correlation heatmap for a set of tickers and receive a PNG heatmap with an explanation of which pairs are most and least correlated
**Plans**: TBD

Plans:
- [ ] 02-01: Intent routing in SKILL.md for market analysis task type + stock price chart workflow
- [ ] 02-02: Returns, volatility, and risk metrics workflows (Sharpe, drawdown, beta)
- [ ] 02-03: Multi-ticker comparison and correlation heatmap workflows

### Phase 3: ML Workflows
**Goal**: Users can point the skill at a CSV file and receive a trained, evaluated liquidity risk regression model or an investor segment classifier — with plain-English interpretation of every model metric and a prediction interface for new data
**Depends on**: Phase 2
**Requirements**: LQDX-01, LQDX-02, LQDX-03, LQDX-04, LQDX-05, LQDX-06, INVX-01, INVX-02, INVX-03, INVX-04, INVX-05, INVX-06
**Success Criteria** (what must be TRUE):
  1. User can provide a CSV file path and request liquidity risk modeling; the skill auto-detects the CSV structure, cleans the data (outliers, missing values, categoricals), and reports what it found before modeling
  2. The liquidity predictor trains a regression pipeline with the train/test split performed before any `.fit()` call, and outputs RMSE, R², and a residual plot — each with plain-English interpretation and a baseline comparison
  3. User can provide a new client row and receive a liquidity risk prediction with context on model confidence
  4. User can provide an investor CSV file path; the skill engineers features (dummy variables, redundant feature removal), uses stratified sampling for the split, and runs classification with cross-validation and hyperparameter search
  5. The investor classifier outputs a confusion matrix, classification report, and feature importance chart — all interpreted in plain English without ML jargon
  6. User can input a new investor's attributes and receive a segment classification with a plain-English explanation of which features drove the prediction
**Plans**: TBD

Plans:
- [ ] 03-01: CSV ingestion, EDA pipeline, and data cleaning workflows (shared by both ML tasks)
- [ ] 03-02: Liquidity predictor — regression pipeline, train/test split enforcement, evaluation outputs
- [ ] 03-03: Investor classifier — feature engineering, stratified split, classification pipeline, hyperparameter search
- [ ] 03-04: Prediction interfaces for new data — liquidity client prediction and investor segment classification

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Infrastructure & Skill Scaffold | 0/3 | Not started | - |
| 2. Market Analysis Workflows | 0/3 | Not started | - |
| 3. ML Workflows | 0/4 | Not started | - |
