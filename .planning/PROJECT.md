# Finance AI Skill for Claude Code

## What This Is

A Claude Code native skill (and claude.ai plugin) that lets finance professionals describe what they need in plain English and receive executed Python finance analysis — no Python coding required. Built around the pyfi.com Python & Machine Learning for Finance course curriculum.

The skill is an MCP server with 11 tools covering market analysis (price charts, returns, volatility, risk metrics, comparison, correlation) and ML workflows (CSV ingestion, liquidity risk regression, investor segment classification). Two persona variants ship: equity analyst (`/finance-analyst`) and portfolio manager (`/finance-pm`). A guided `/demo` walkthrough demonstrates all capabilities step-by-step.

**v1.1 shipped.** v1.0 MVP (38 requirements) + v1.1 Interactive Demo (17 requirements) delivered across 8 phases.

## Core Value

Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## Requirements

### Validated

- ✓ `/finance` slash command with intent classification and dynamic context injection — v1.0
- ✓ Stock analysis workflows (price data, returns, volatility, correlations) via yfinance — v1.0
- ✓ Data cleaning pipeline matching ML 01 curriculum (IQR outliers, missing value fill, EDA charts) — v1.0
- ✓ Liquidity predictor using regression ML (sklearn Pipeline, train/test split before fit, RMSE/R²) — v1.0
- ✓ Investor classifier using classification ML (GridSearchCV, StratifiedKFold, feature importance) — v1.0
- ✓ User-provided CSV file support with auto-structure detection — v1.0
- ✓ Output includes PNG charts, summary tables, and plain-English interpretation with disclaimer — v1.0
- ✓ Equity analyst persona (`/finance-analyst`) and portfolio manager persona (`/finance-pm`) — v1.0
- ✓ claude.ai browser access via HTTP transport + ngrok startup script — v1.0
- ✓ Plugin package for Claude marketplace submission — v1.0
- ✓ `/demo` slash command launches guided walkthrough of all 11 MCP tools — v1.1
- ✓ Live yfinance data for market analysis demos with pause-and-explain flow — v1.1
- ✓ Bundled sample CSV for ML workflow demos (no user data required) — v1.1
- ✓ Persona contrast demo: analyst vs PM framing on same risk metrics data — v1.1

### Active

- [ ] Replace `[owner]` placeholder in `finance-mcp-plugin/.claude-plugin/plugin.json` before marketplace submission
- [ ] Add Phase 2+3 MCP tool names to `/finance` command `allowed-tools` (SKILL.md inconsistency with direct MCP dispatch)
- [ ] Alpha Vantage integration for fundamental data (earnings, P/E, revenue) — DATA-01
- [ ] FRED integration for macroeconomic indicators — DATA-02
- [ ] Persona detection via conversation context (no explicit command) — PERS-03
- [ ] Algorithmic trading backtesting — ADVX-01
- [ ] Portfolio optimization (efficient frontier, max Sharpe) — ADVX-02

### Out of Scope

- Bloomberg / Refinitiv integration — paid API, not in course scope
- Real-time streaming data — batch analysis only
- Trading execution / order placement — regulatory liability
- Web UI / dashboard — Claude Code terminal + claude.ai only
- DCF / fundamental valuation — not in course curriculum
- Excel (.xlsx) support — CSV only for now (DATA-03 deferred)

## Context

**v1.1 shipped 2026-03-18.** 8 phases, 25 plans, 3,832 LOC Python, 105 tests passing.

**Tech stack:** Python 3.14, FastMCP 2.x, yfinance 0.2.54+, scikit-learn 1.8.0, pandas, matplotlib (Agg), seaborn, joblib

**Architecture:** Single FastMCP server instance shared across stdio (Claude Code) and streamable-HTTP (claude.ai) transports. All 11 tools registered in `server.py`. Adapter pattern isolates yfinance behind `adapter.py`. All output enforces plain-English-first + disclaimer via `output.py`.

**Known tech debt:** 10 items from v1.0 tracked in `.planning/milestones/v1.0-MILESTONE-AUDIT.md` — none are blockers. Most notable: VALIDATION.md files remain in draft state (Nyquist validation not run).

## Constraints

- **Tech stack**: Python (matches pyfi.com course stack)
- **Runtime**: Claude Code (Bash tool) + claude.ai (streamable-HTTP)
- **Data scope**: yfinance for live market data + CSV for user-provided data
- **Skill format**: Claude Code slash command + FastMCP server

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Slash command format (not conversational agent) | More actionable for daily use | ✓ Good — intent classification in SKILL.md routes cleanly |
| Python execution via Write-then-Bash | Course teaches Python; skill runs same code; no inline `-c` | ✓ Good — documented pattern, consistent across all tools |
| yfinance + CSV only for v1 | Matches course scope; keeps v1 shippable | ✓ Good — shipped on time |
| FastMCP server as shared engine | Single registration point; both transports reuse same instance | ✓ Good — server_http.py is 29 lines |
| Close column (not Adj Close) | yfinance 0.2.54+ auto_adjust=True removes Adj Close | ✓ Good — adapter.py enforces, AST test confirms isolation |
| matplotlib.use(Agg) in output.py module scope | Must be set before pyplot import; enforced on every tool import | ✓ Good — no plt.show() anywhere in codebase |
| Train/test split before any .fit() call | Look-ahead bias is unrecoverable; enforced in code | ✓ Good — structural test passes |
| Two-tool ML pattern (train+evaluate / predict+infer) | Clean separation of training and inference | ✓ Good — adopted for both liquidity and investor models |
| Persona reuse of existing MCP tools | Zero new Python code per persona; differentiation is in framing | ✓ Good — both persona variants work |
| Deferred Nyquist validation | VALIDATION.md files created but not completed | ⚠️ Revisit — all 4 v1.0 phases in draft state |
| /demo as self-running walkthrough (no arguments) | Simpler UX; all steps pre-sequenced | ✓ Good — 14 steps cover all 11 tools + both personas |
| Persona framing via instructional prose in demo.md | Cannot invoke slash commands from slash commands | ✓ Good — Claude interprets framing correctly |
| xfail as CI gate for network-dependent tests | Tests degrade gracefully when Yahoo Finance unreachable | ✓ Good — xpassed confirms connectivity |
| liquidity_predictor restricted to 3 features | Full CSV columns caused column-mismatch at inference time | ✓ Good — fixed inference stability |

---
*Last updated: 2026-03-18 after v1.1 milestone completion*
