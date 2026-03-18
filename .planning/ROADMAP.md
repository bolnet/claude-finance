# Roadmap: Finance AI Skill for Claude Code

## Overview

Build a finance AI skill that works in both Claude Code (terminal) and claude.ai (browser) via an MCP server architecture. Finance professionals describe what they need in plain English and receive executed Python analysis — no coding required. The MCP server is the core engine; the Claude Code slash command and claude.ai plugin are thin interfaces on top of it. Work flows in four delivery boundaries: infrastructure + MCP scaffold → market analysis tools → ML workflow tools → web publishing, persona variants, and marketplace submission.

## Interfaces

| Interface | Who Uses It | How |
|-----------|------------|-----|
| Claude Code `/finance` command | Power users, developers | Terminal slash command |
| claude.ai browser plugin | All finance professionals | Chat at claude.ai |
| MCP server (shared engine) | Both above | Python finance engine |

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3, 4): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Infrastructure & MCP Scaffold** - MCP server foundation, data adapter, output conventions, Claude Code command wrapper, and environment validation (completed 2026-03-18)
- [ ] **Phase 2: Market Analysis Tools** - Live stock analysis via yfinance — price charts, returns, volatility, risk metrics, multi-ticker comparison, correlation heatmap — as MCP tools
- [ ] **Phase 3: ML Workflow Tools** - Liquidity predictor (regression, ML 03) and investor classifier (classification, ML 05-06) as MCP tools on user-provided CSV data
- [ ] **Phase 4: Web Publishing & Personas** - claude.ai plugin packaging, marketplace submission, analyst/PM-trader persona variants

## Phase Details

### Phase 1: Infrastructure & MCP Scaffold
**Goal**: MCP server exists and is connectable, `/finance` Claude Code command works, Python environment validated, yfinance adapter correct, output conventions established, disclaimer on all outputs
**Depends on**: Nothing (first phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05, INFRA-06, INFRA-07, CMD-01, CMD-02, CMD-03, CMD-04, MCP-01, MCP-02, MCP-03
**Success Criteria** (what must be TRUE):
  1. Running `/finance` in Claude Code produces a response (not an error) and Claude can introspect the local Python environment before generating any code
  2. The yfinance adapter uses `Close` (auto_adjust=True default in 0.2.54+) and raises a user-readable error if the ticker is invalid, the date range is empty, or the DataFrame is empty
  3. All chart output is written as PNG files to `finance_output/charts/` using the `Agg` backend — no `plt.show()` calls anywhere
  4. Every output — regardless of workflow — leads with a plain-English interpretation and ends with the hardcoded investment advice disclaimer
  5. Generated Python scripts are written to disk as `.py` files (Write tool) and then executed via Bash — never run as inline `-c` strings
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Python project scaffold (pyproject.toml, FastMCP server, .mcp.json, Wave 0 test stubs)
- [x] 01-02-PLAN.md — yfinance adapter layer, validators, output conventions module, environment checker
- [x] 01-03-PLAN.md — Claude Code command file, SKILL.md intent classifier, human verification checkpoint

### Phase 2: Market Analysis Tools
**Goal**: Users (in Claude Code or claude.ai) can request stock analysis in plain English and receive price charts, return metrics, risk statistics, multi-ticker comparisons, and correlation heatmaps — all with plain-English interpretation
**Depends on**: Phase 1
**Requirements**: MKTX-01, MKTX-02, MKTX-03, MKTX-04, MKTX-05, MKTX-06, MKTX-07
**Success Criteria** (what must be TRUE):
  1. User can say "show me AAPL's price chart from 2023 to 2024" and receive a saved PNG chart with a plain-English summary of the price trend
  2. User can request daily and cumulative returns for any ticker and receive both a table and a chart, with volatility expressed in annualized percentage terms
  3. User can request risk metrics for a ticker and receive Sharpe ratio, max drawdown, and beta vs. S&P 500 — each explained in plain English with benchmark context
  4. User can compare 2-5 tickers side-by-side on a normalized price performance chart, with the interpretation noting which performed best and by how much
  5. User can request a correlation heatmap for a set of tickers and receive a PNG heatmap with an explanation of which pairs are most and least correlated
**Plans**: 4 plans

Plans:
- [ ] 02-01-PLAN.md — Test scaffold (15 stubs) + tools/__init__.py + analyze_stock tool (MKTX-01)
- [ ] 02-02-PLAN.md — get_returns, get_volatility, get_risk_metrics tools (MKTX-02, MKTX-03, MKTX-04)
- [ ] 02-03-PLAN.md — compare_tickers, correlation_map tools + MKTX-07 tests (MKTX-05, MKTX-06, MKTX-07)
- [ ] 02-04-PLAN.md — Phase 2 functional testing — live end-to-end verification with real tickers

### Phase 3: ML Workflow Tools
**Goal**: Users can point the tool at a CSV file and receive a trained, evaluated liquidity risk regression model or investor segment classifier — with plain-English interpretation and prediction interface for new data
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
- [ ] 03-01: CSV ingestion, EDA pipeline, and data cleaning (shared MCP tool `ingest_csv`)
- [ ] 03-02: MCP tool `liquidity_predictor` — regression pipeline, split-before-fit enforcement, evaluation outputs
- [ ] 03-03: MCP tool `investor_classifier` — feature engineering, stratified split, cross-validation, hyperparameter search
- [ ] 03-04: MCP tools `predict_liquidity`, `classify_investor` — prediction interfaces for new data
- [ ] 03-05: Phase 3 functional testing — end-to-end verification of ML tools using course CSV files (liquidity_data.csv, investor_data.csv)

### Phase 4: Web Publishing & Personas
**Goal**: Finance professionals can use the skill at claude.ai in their browser; analyst and PM/trader persona variants ship; skill is packaged for the Claude plugin marketplace
**Depends on**: Phase 3
**Requirements**: PERS-01, PERS-02, WEB-01, WEB-02, WEB-03
**Success Criteria** (what must be TRUE):
  1. A finance professional with no Claude Code install can connect the MCP server to claude.ai and use all tools via chat
  2. `/finance-analyst` variant emphasizes stock analysis and peer comparison in its responses
  3. `/finance-pm` variant emphasizes portfolio risk/return attribution in its responses
  4. The MCP server is packaged and documented for marketplace submission

Plans:
- [ ] 04-01: claude.ai MCP integration — remote transport, server packaging, connection guide for non-technical users
- [ ] 04-02: Analyst persona variant (`.claude/commands/finance-analyst.md`) + PM/trader variant (`finance-pm.md`)
- [ ] 04-03: Marketplace packaging — README, screenshots, install instructions, listing metadata
- [ ] 04-04: Phase 4 functional testing — end-to-end verification of claude.ai integration, persona variants, and full user journey

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Infrastructure & MCP Scaffold | 3/3 | Complete   | 2026-03-18 |
| 2. Market Analysis Tools | 0/4 | Not started | - |
| 3. ML Workflow Tools | 0/5 | Not started | - |
| 4. Web Publishing & Personas | 0/4 | Not started | - |
