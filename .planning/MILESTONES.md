# Milestones

## v1.1 Interactive Demo (Shipped: 2026-03-18)

**Phases completed:** 4 phases, 9 plans
**Files changed:** 35 (4,042 insertions, 88 deletions)
**Test suite:** 105 tests passing
**Timeline:** 2026-03-17 → 2026-03-18

**Key accomplishments:**
1. `/demo` slash command with 14-step guided walkthrough of all 11 MCP tools and both personas
2. Live integration tests for all 6 market analysis tools with real Yahoo Finance data (xfail CI gate)
3. Bundled `demo/sample_portfolio.csv` (100-row synthetic data, seed=42) for ML demo steps
4. Fixed liquidity_predictor column-mismatch bug — restricted to 3-column feature set for inference stability
5. Persona contrast demo: analyst framing (Sharpe first) vs PM framing (drawdown/beta first) on same data
6. 17/17 v1.1 requirements delivered, all human-verified via `/demo` execution

**Archive:** `.planning/milestones/v1.1-ROADMAP.md` | `.planning/milestones/v1.1-REQUIREMENTS.md`

---

## v1.0 Finance AI Skill MVP (Shipped: 2026-03-18)

**Phases completed:** 4 phases, 16 plans
**LOC:** ~2,767 Python (src + tests)
**Test suite:** 53 passed, 13 xpassed, 0 failures
**Timeline:** 2026-03-17 → 2026-03-18 (72 commits)

**Key accomplishments:**
1. FastMCP server with 11 MCP tools, registered in `.mcp.json` for Claude Code — stdio transport locally, streamable-HTTP for claude.ai
2. 6 market analysis tools: price charts, daily/cumulative returns, annualized volatility, risk metrics (Sharpe/drawdown/beta vs S&P 500), multi-ticker comparison, correlation heatmap
3. Full CSV ingestion pipeline with IQR-based cleaning, EDA charts, and structure auto-detection
4. Liquidity risk regression pipeline (sklearn Pipeline, train/test split before fit, joblib persistence, RMSE/R² with plain-English output)
5. Investor segment classifier (GridSearchCV + StratifiedKFold, confusion matrix, feature importance, single-row inference with column alignment)
6. claude.ai access via HTTP transport; 2 persona variants (equity analyst + portfolio manager); plugin package for marketplace submission

**Archive:** `.planning/milestones/v1.0-ROADMAP.md` | `.planning/milestones/v1.0-REQUIREMENTS.md`

---

