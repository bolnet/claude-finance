# Roadmap: Finance AI Skill for Claude Code

## Milestones

- ✅ **v1.0 Finance AI Skill MVP** — Phases 1–4 (shipped 2026-03-18)
- 🚧 **v1.1 Interactive Demo** — Phases 5–8 (in progress)

## Phases

<details>
<summary>✅ v1.0 Finance AI Skill MVP (Phases 1–4) — SHIPPED 2026-03-18</summary>

- [x] **Phase 1: Infrastructure & MCP Scaffold** — FastMCP server, yfinance adapter, output conventions, /finance command, SKILL.md intent classifier (3/3 plans, completed 2026-03-18)
- [x] **Phase 2: Market Analysis Tools** — 6 MCP tools: price chart, returns, volatility, risk metrics, comparison, correlation heatmap (4/4 plans, completed 2026-03-18)
- [x] **Phase 3: ML Workflow Tools** — CSV ingest pipeline, liquidity regression model, investor classifier (5/5 plans, completed 2026-03-18)
- [x] **Phase 4: Web Publishing & Personas** — HTTP transport, /finance-analyst, /finance-pm, plugin package (4/4 plans, completed 2026-03-18)

Full phase details: `.planning/milestones/v1.0-ROADMAP.md`

</details>

### 🚧 v1.1 Interactive Demo (In Progress)

**Milestone Goal:** Users can experience every capability of the Finance AI Skill through a guided `/demo` slash command that runs all 11 MCP tools and both personas with real examples, pausing between each for explanation.

## Phase Details

### Phase 5: Demo Command & Flow
**Goal**: Users can launch a guided interactive walkthrough that introduces the skill and navigates between steps with explanations
**Depends on**: Phase 4 (v1.0 complete)
**Requirements**: DEMO-01, DEMO-02, DEMO-03, DEMO-04
**Success Criteria** (what must be TRUE):
  1. User types `/demo` and the walkthrough starts immediately with a welcome message explaining what the Finance AI Skill does
  2. After each tool demo step, the user sees a plain-English explanation of what just happened before the next step begins
  3. At the end of the walkthrough, the user sees a completion summary listing all 11 tools demonstrated
  4. The demo command is registered in `.claude/commands/` and discoverable via Claude Code slash command autocomplete
**Plans**: 2 plans

Plans:
- [ ] 05-01-PLAN.md — Create /demo slash command with walkthrough script and SKILL.md demo intent
- [ ] 05-02-PLAN.md — Structural validation tests and human verification of discoverability

### Phase 6: Market Analysis Demos
**Goal**: Users see all 6 market analysis MCP tools execute live with real ticker data and receive a plain-English explanation of each output
**Depends on**: Phase 5
**Requirements**: MRKT-01, MRKT-02, MRKT-03, MRKT-04, MRKT-05, MRKT-06
**Success Criteria** (what must be TRUE):
  1. User sees `analyze_stock` run on a live ticker (AAPL) and a price chart is produced with explanation
  2. User sees `get_returns` output with daily and cumulative return values explained in plain English
  3. User sees `get_volatility` output with annualized volatility explained in plain English
  4. User sees `get_risk_metrics` output with Sharpe ratio, max drawdown, and beta explained in plain English
  5. User sees `compare_tickers` run on AAPL vs MSFT and `correlation_map` produce a heatmap, each with explanation
**Plans**: 2 plans

Plans:
- [ ] 06-01-PLAN.md — Fix demo.md parameter schemas and create live integration tests for all 6 market analysis tools
- [ ] 06-02-PLAN.md — Full test suite verification and human sign-off on demo Steps 3-8

### Phase 7: ML Workflow Demos
**Goal**: Users see all 4 ML workflow MCP tools execute on bundled sample data and receive explanations of the cleaning, training, and inference outputs
**Depends on**: Phase 6
**Requirements**: MLWF-01, MLWF-02, MLWF-03, MLWF-04
**Success Criteria** (what must be TRUE):
  1. A bundled sample CSV file ships with the project and is referenced by the demo without requiring user-provided data
  2. User sees `ingest_csv` run on the sample CSV and receives cleaning/EDA output with explanation
  3. User sees `predict_liquidity` (train + predict cycle) produce regression results with RMSE/R² explained in plain English
  4. User sees `classify_investor` (train + predict cycle) produce classification results with segment label and feature importance explained in plain English
**Plans**: 3 plans

Plans:
- [ ] 07-01-PLAN.md — Bundled sample CSV with schema tests matching liquidity and investor model columns
- [ ] 07-02-PLAN.md — Integration tests proving all 4 ML tools work with sample CSV using demo.md parameters
- [ ] 07-03-PLAN.md — Fix demo.md parameter mismatches and human verification of Steps 9-11

### Phase 8: Persona Demos
**Goal**: Users see the same analysis delivered through both the equity analyst and portfolio manager personas and understand how the framing differs
**Depends on**: Phase 7
**Requirements**: PERS-01, PERS-02, PERS-03
**Success Criteria** (what must be TRUE):
  1. User sees an analysis step delivered through `/finance-analyst` persona framing (Sharpe/drawdown emphasis, single-stock lens)
  2. User sees the same analysis delivered through `/finance-pm` persona framing (portfolio holdings lens, drawdown/beta lead)
  3. User sees an explicit side-by-side or sequential explanation of how the two personas interpret the same data differently
**Plans**: 2 plans

Plans:
- [ ] 08-01-PLAN.md — Persona demo steps: replace text-only Persona Showcase with Steps 12-14 (analyst framing, PM framing, contrast table) plus structural tests
- [ ] 08-02-PLAN.md — Functional verification: full test suite regression check and human sign-off on /demo Steps 12-14

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1. Infrastructure & MCP Scaffold | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Market Analysis Tools | v1.0 | 4/4 | Complete | 2026-03-18 |
| 3. ML Workflow Tools | v1.0 | 5/5 | Complete | 2026-03-18 |
| 4. Web Publishing & Personas | v1.0 | 4/4 | Complete | 2026-03-18 |
| 5. Demo Command & Flow | v1.1 | 2/2 | Complete | 2026-03-18 |
| 6. Market Analysis Demos | 2/2 | Complete   | 2026-03-18 | - |
| 7. ML Workflow Demos | 3/3 | Complete   | 2026-03-18 | - |
| 8. Persona Demos | 1/2 | In Progress|  | - |

---
*Last updated: 2026-03-18 — Phase 8 plans created*
