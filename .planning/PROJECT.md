# Finance AI Skill for Claude Code

## What This Is

A Claude Code native skill that lets finance professionals describe what they need in plain English and get back clean financial analysis — no Python coding required, no Excel needed. Built around the pyfi.com Python & Machine Learning for Finance course curriculum, the skill translates natural language requests into executed Python finance workflows (data fetching, cleaning, modeling, insights).

Three persona-specific versions will ship in phases: Financial Analysts, Portfolio Managers / Traders, and a unified generalist version.

## Core Value

Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] `/finance` slash command skill that accepts natural language finance requests
- [ ] Stock analysis workflows (price data, returns, volatility, correlations) using yfinance
- [ ] Data cleaning & exploration pipeline matching ML 01 curriculum (outliers, categoricals, visualization)
- [ ] Liquidity predictor using regression ML (ML 03 — linear/polynomial regression, pipelines)
- [ ] Investor classifier using classification ML (ML 05-06 — stratified sampling, cross-validation, hyperparameter tuning)
- [ ] Support for user-provided CSV/Excel files (matching course dataset formats)
- [ ] Output includes charts (matplotlib/seaborn), summary tables, and plain-English interpretation
- [ ] Three separate persona variants: Analyst, Portfolio Manager/Trader, Generalist

### Out of Scope

- Bloomberg / Refinitiv / Alpha Vantage integration — v1 uses yfinance + CSVs only (course scope)
- Real-time streaming data — batch analysis only for v1
- Web UI or dashboard — Claude Code terminal only for v1
- Users writing Python code themselves — skill handles all code generation/execution
- Algo trading backtesting — deferred to Phase 2 (not covered in available ML notebooks)

## Context

**Course content analyzed:**
- **PF 01-05**: Python fundamentals, NumPy, Pandas (foundational tools the skill uses internally)
- **ML 01**: Data cleaning & exploration — matplotlib/seaborn, outlier handling, categorical correction
- **ML 03**: Liquidity Predictor — regression, model pipelines, train/test splits (uses `liquidity_data.csv`, `liquidity_client.csv`)
- **ML 05-06**: Investor Classifier — feature engineering, dummy variables, stratified sampling, cross-validation, hyperparameter grids (uses `investor_data.csv`, `investor_data_2.csv`)
- **Books**: Python for Finance, Algorithmic Trading Mastery, ML for Finance, Expanded Python Finance Book

**Core insight from user:**
Finance professionals today use Excel for this work. This course teaches them Python as the upgrade. The skill removes even that barrier — they get the Python outputs without writing Python. The skill is the Python layer.

**pyfi.com curriculum maps to these real finance problems:**
1. Stock price analysis → Pandas + yfinance
2. Liquidity risk modeling → Regression ML
3. Client/investor profiling → Classification ML

## Constraints

- **Tech stack**: Python (matches course stack: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, yfinance)
- **Runtime**: Claude Code's native Python execution (Bash tool)
- **Data scope**: yfinance for live data + CSV for user-provided data (v1)
- **Skill format**: Claude Code slash command (`.claude/skills/` or `~/.claude/skills/`)
- **Persona scope**: v1 builds generalist first, then splits into analyst / PM-trader variants in subsequent phases

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Slash command format (not conversational agent) | More actionable for daily use — finance pros want discrete tasks, not chat | — Pending |
| Python execution via Claude Code Bash tool | Course teaches Python; skill should run same code under the hood | — Pending |
| yfinance + CSV only for v1 | Matches course scope; keeps v1 shippable | — Pending |
| Three phases by persona | Each finance persona has different workflows and mental models | — Pending |
| Course curriculum as v1 scope boundary | Prevents scope creep; course provides validated real-world problems | — Pending |

---
*Last updated: 2026-03-17 after initialization*
