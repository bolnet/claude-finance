# Requirements: Finance AI Skill for Claude Code

**Defined:** 2026-03-17
**Core Value:** Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Infrastructure

- [ ] **INFRA-01**: Skill detects Python environment and validates required packages (yfinance, pandas, numpy, matplotlib, seaborn, scikit-learn) on first run
- [ ] **INFRA-02**: Skill installs missing packages or prints clear install instructions if environment cannot be modified
- [ ] **INFRA-03**: yfinance data adapter layer isolates all Yahoo Finance API calls behind a single module (single point of change for API breakage)
- [ ] **INFRA-04**: All chart outputs saved as PNG files to `finance_output/` directory (no `plt.show()`; uses `matplotlib.use('Agg')`)
- [ ] **INFRA-05**: All outputs include hardcoded investment advice disclaimer ("For educational/informational purposes only. Not financial advice.")
- [ ] **INFRA-06**: Data validation wrapper catches empty DataFrames, invalid tickers, bad date ranges, and returns user-friendly error messages
- [ ] **INFRA-07**: All output leads with plain-English interpretation before any DataFrame, chart path, or model metric

### MCP Server (Core Engine)

- [x] **MCP-01**: Python MCP server exists at `src/finance_mcp/server.py` using FastMCP, registered in `.mcp.json` for Claude Code
- [x] **MCP-02**: MCP server exposes tools with clear descriptions that Claude (Code or claude.ai) can discover and invoke via natural language
- [x] **MCP-03**: MCP server runs via `stdio` transport locally (Claude Code) and is prepared for remote transport packaging (Phase 4)

### Command & Skill Structure

- [ ] **CMD-01**: `/finance` slash command file exists at `.claude/commands/finance.md` with correct frontmatter (allowed-tools, description, argument-hint)
- [ ] **CMD-02**: Finance SKILL.md exists at `.claude/skills/finance/SKILL.md` with intent classification logic for routing requests to MCP tools
- [ ] **CMD-03**: Command uses dynamic context injection (`!ls`, `!python3 --version`, `!pip list`) before code generation to produce runnable scripts
- [ ] **CMD-04**: Python scripts are written to disk first (Write tool), then executed (Bash tool) — not inline `python3 -c` strings

### Market Analysis

- [ ] **MKTX-01**: User can request stock price chart for any ticker and date range in plain English; chart saved as PNG
- [ ] **MKTX-02**: User can get daily and cumulative returns for a ticker, displayed as table and chart
- [ ] **MKTX-03**: User can get annualized volatility and rolling volatility chart for a ticker
- [ ] **MKTX-04**: User can get Sharpe ratio and basic risk metrics (max drawdown, beta vs S&P 500) for a ticker
- [ ] **MKTX-05**: User can compare multiple tickers (2-5) side-by-side on price performance chart
- [ ] **MKTX-06**: User can get correlation heatmap between a set of tickers
- [ ] **MKTX-07**: All market analysis outputs include plain-English summary (e.g., "AAPL had annualized volatility of 24%, which is higher than the S&P 500 average of ~15%")

### Liquidity Predictor (ML 03 Curriculum)

- [ ] **LQDX-01**: User can provide a CSV file path and request liquidity risk prediction; skill detects CSV structure automatically
- [ ] **LQDX-02**: Skill performs data cleaning pipeline: outlier detection, categorical correction, missing value handling (matching ML 01 curriculum)
- [ ] **LQDX-03**: Skill runs exploratory data analysis and outputs summary statistics + distribution charts
- [ ] **LQDX-04**: Skill trains linear regression pipeline with train/test split (no look-ahead bias: split before any `.fit()` call)
- [ ] **LQDX-05**: Skill evaluates model: RMSE, R², residual plot — all with plain-English interpretation
- [ ] **LQDX-06**: Skill accepts new client data and outputs liquidity prediction with confidence context

### Investor Classifier (ML 05-06 Curriculum)

- [ ] **INVX-01**: User can provide investor CSV file path; skill detects features and target column automatically
- [ ] **INVX-02**: Skill performs feature engineering: dummy variable creation, redundant feature removal (matching ML 05 curriculum)
- [ ] **INVX-03**: Skill uses stratified random sampling for train/test split (matching ML 06 curriculum)
- [ ] **INVX-04**: Skill runs classification pipeline with cross-validation and hyperparameter grid search
- [ ] **INVX-05**: Skill outputs confusion matrix, classification report, and feature importance — all with plain-English interpretation
- [ ] **INVX-06**: User can input a new investor's data and get segment classification with explanation

## Phase 4 Requirements (Web Publishing & Personas)

In v1 roadmap but delivered last.

### Web Access

- [ ] **WEB-01**: Finance professional with no Claude Code install can connect MCP server to claude.ai and use all tools via browser chat
- [ ] **WEB-02**: MCP server packaged with connection guide for non-technical users (no terminal knowledge required to connect)
- [ ] **WEB-03**: Skill listed and documented for Claude plugin marketplace submission

### Persona Variants

- [ ] **PERS-01**: `/finance-analyst` command — equity-focused variant (stock analysis, peer comparison, valuation ratios emphasis)
- [ ] **PERS-02**: `/finance-pm` command — portfolio manager variant (risk/return attribution, portfolio-level metrics)

## v2 Requirements

Deferred to future milestone.

### Extended Persona

- **PERS-03**: Persona detection via conversation context (no explicit command needed)

### Extended Data Sources

- **DATA-01**: Alpha Vantage integration for fundamental data (earnings, P/E, revenue)
- **DATA-02**: FRED integration for macroeconomic indicators (interest rates, GDP, inflation)
- **DATA-03**: User Excel file support (`.xlsx` via openpyxl) in addition to CSV

### Advanced Analytics

- **ADVX-01**: Algorithmic trading strategy backtesting (from Algorithmic Trading Mastery book)
- **ADVX-02**: Portfolio optimization (PyPortfolioOpt — efficient frontier, max Sharpe)
- **ADVX-03**: GARCH volatility modeling for risk desk use cases

## Out of Scope

| Feature | Reason |
|---------|--------|
| Bloomberg / Refinitiv integration | Paid API, not in course scope; v2+ |
| Real-time streaming data | Batch analysis only; complexity too high for v1 |
| Trading execution / order placement | Regulatory liability; out of scope entirely |
| Web UI / dashboard | Claude Code terminal only; UI is a separate project |
| Users writing Python themselves | Skill handles all code; teaching Python is secondary |
| DCF / fundamental valuation models | Not in course curriculum; deferred indefinitely |
| Mobile / web deployment | Claude Code desktop only for v1 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 1 | Pending |
| INFRA-02 | Phase 1 | Pending |
| INFRA-03 | Phase 1 | Pending |
| INFRA-04 | Phase 1 | Pending |
| INFRA-05 | Phase 1 | Pending |
| INFRA-06 | Phase 1 | Pending |
| INFRA-07 | Phase 1 | Pending |
| MCP-01 | Phase 1 | Complete (01-01) |
| MCP-02 | Phase 1 | Complete (01-01) |
| MCP-03 | Phase 1 | Complete (01-01) |
| CMD-01 | Phase 1 | Pending |
| CMD-02 | Phase 1 | Pending |
| CMD-03 | Phase 1 | Pending |
| CMD-04 | Phase 1 | Pending |
| MKTX-01 | Phase 2 | Pending |
| MKTX-02 | Phase 2 | Pending |
| MKTX-03 | Phase 2 | Pending |
| MKTX-04 | Phase 2 | Pending |
| MKTX-05 | Phase 2 | Pending |
| MKTX-06 | Phase 2 | Pending |
| MKTX-07 | Phase 2 | Pending |
| LQDX-01 | Phase 3 | Pending |
| LQDX-02 | Phase 3 | Pending |
| LQDX-03 | Phase 3 | Pending |
| LQDX-04 | Phase 3 | Pending |
| LQDX-05 | Phase 3 | Pending |
| LQDX-06 | Phase 3 | Pending |
| INVX-01 | Phase 3 | Pending |
| INVX-02 | Phase 3 | Pending |
| INVX-03 | Phase 3 | Pending |
| INVX-04 | Phase 3 | Pending |
| INVX-05 | Phase 3 | Pending |
| INVX-06 | Phase 3 | Pending |
| WEB-01 | Phase 4 | Pending |
| WEB-02 | Phase 4 | Pending |
| WEB-03 | Phase 4 | Pending |
| PERS-01 | Phase 4 | Pending |
| PERS-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 38 total
- Mapped to phases: 38
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 after initial definition*
