# Roadmap: Finance AI Skill for Claude Code

## Milestones

- ✅ **v1.0 Finance AI Skill MVP** — Phases 1–4 (shipped 2026-03-18)
- ✅ **v1.1 Interactive Demo** — Phases 5–8 (shipped 2026-03-18)
- 🚧 **v1.2 Role Walkthroughs** — Phases 9–12 (in progress)

## Phases

<details>
<summary>✅ v1.0 Finance AI Skill MVP (Phases 1–4) — SHIPPED 2026-03-18</summary>

- [x] **Phase 1: Infrastructure & MCP Scaffold** — FastMCP server, yfinance adapter, output conventions, /finance command, SKILL.md intent classifier (3/3 plans, completed 2026-03-18)
- [x] **Phase 2: Market Analysis Tools** — 6 MCP tools: price chart, returns, volatility, risk metrics, comparison, correlation heatmap (4/4 plans, completed 2026-03-18)
- [x] **Phase 3: ML Workflow Tools** — CSV ingest pipeline, liquidity regression model, investor classifier (5/5 plans, completed 2026-03-18)
- [x] **Phase 4: Web Publishing & Personas** — HTTP transport, /finance-analyst, /finance-pm, plugin package (4/4 plans, completed 2026-03-18)

Full phase details: `.planning/milestones/v1.0-ROADMAP.md`

</details>

<details>
<summary>✅ v1.1 Interactive Demo (Phases 5–8) — SHIPPED 2026-03-18</summary>

- [x] **Phase 5: Demo Command & Flow** — /demo slash command with 14-step guided walkthrough, SKILL.md demo intent routing (2/2 plans, completed 2026-03-18)
- [x] **Phase 6: Market Analysis Demos** — Live integration tests for all 6 market tools, corrected demo.md parameter schemas (2/2 plans, completed 2026-03-18)
- [x] **Phase 7: ML Workflow Demos** — Bundled sample_portfolio.csv, ML integration tests, fixed liquidity_predictor column-mismatch (3/3 plans, completed 2026-03-18)
- [x] **Phase 8: Persona Demos** — Persona framing steps 12-14, analyst vs PM contrast table (2/2 plans, completed 2026-03-18)

Full phase details: `.planning/milestones/v1.1-ROADMAP.md`

</details>

### 🚧 v1.2 Role Walkthroughs (In Progress)

**Milestone Goal:** Build 5 remaining role-based walkthrough slash commands, each a deep multi-phase scenario simulating real finance workflows using the existing 11 MCP tools.

- [x] **Phase 9: Market-Analysis Walkthroughs** — Hedge Fund and Investment Banking walkthroughs using volatility, correlation, and comparison tools (completed 2026-03-18)
- [x] **Phase 10: Data-Profiling Walkthroughs** — FP&A and Accounting walkthroughs using CSV ingestion, data profiling, and liquidity predictor (completed 2026-03-18)
- [ ] **Phase 11: ML-Classifier Walkthrough** — Private Equity walkthrough using investor classifier for due diligence scoring
- [ ] **Phase 12: Walkthrough Test Suite** — Dedicated test files for all 5 walkthroughs validating structure, phases, and MCP tool coverage

## Phase Details

### Phase 9: Market-Analysis Walkthroughs
**Goal**: Finance professionals in hedge fund and investment banking roles can run scenario-driven walkthroughs that simulate real trading desk and deal analysis workflows using market analysis tools
**Depends on**: Phase 8 (v1.1 shipped; existing 11 MCP tools available)
**Requirements**: HF-01, HF-02, HF-03, HF-04, IB-01, IB-02, IB-03
**Success Criteria** (what must be TRUE):
  1. User can run `/walkthrough-hedge-fund` and receive a multi-phase scenario covering volatility regime detection, cross-sector diversification, and correlation-based pair identification
  2. User can run `/walkthrough-investment-banking` and receive a comparable company analysis scenario covering 5-ticker comps with relative valuation framing and relative performance for deal pitch materials
  3. Both walkthroughs auto-run their MCP tool sequences without requiring additional user input per step
  4. Each walkthrough output includes plain-English interpretation with role-appropriate framing (trading desk language vs. deal pitch language)
**Plans:** 2/2 plans complete

Plans:
- [x] 09-01-PLAN.md — Hedge Fund walkthrough: SKILL.md routing, walkthrough-hedge-fund.md scenario file, volatility/correlation tool sequence
- [x] 09-02-PLAN.md — Investment Banking walkthrough: walkthrough-investment-banking.md scenario file, 5-ticker comps tool sequence

### Phase 10: Data-Profiling Walkthroughs
**Goal**: Finance professionals in FP&A and accounting roles can run scenario-driven walkthroughs that simulate real ERP data profiling, forecasting prep, and transaction anomaly detection workflows using CSV ingestion and ML tools
**Depends on**: Phase 9
**Requirements**: FPA-01, FPA-02, FPA-03, ACCT-01, ACCT-02, ACCT-03
**Success Criteria** (what must be TRUE):
  1. User can run `/walkthrough-fpa` and receive a scenario covering CSV data profiling with target column identification and ERP export cleanup leading into liquidity predictor forecasting prep
  2. User can run `/walkthrough-accounting` and receive a scenario covering transaction data profiling via CSV ingestion and anomaly detection prep with ERP consolidation patterns
  3. Both walkthroughs use the bundled sample CSV (no user data required) and complete without manual intervention
  4. Output shows data profiling results and ML forecasting interpretation in role-appropriate language (budget variance framing vs. controller/audit framing)
**Plans:** 2/2 plans complete

Plans:
- [ ] 10-01-PLAN.md — FP&A walkthrough: walkthrough-fpa.md scenario file, CSV profiling + liquidity predictor tool sequence
- [ ] 10-02-PLAN.md — Accounting walkthrough: walkthrough-accounting.md scenario file, CSV ingestion + anomaly framing tool sequence

### Phase 11: ML-Classifier Walkthrough
**Goal**: Finance professionals in private equity and venture capital roles can run a scenario-driven walkthrough that simulates real due diligence scoring and portfolio monitoring using the investor classifier
**Depends on**: Phase 10
**Requirements**: PE-01, PE-02, PE-03
**Success Criteria** (what must be TRUE):
  1. User can run `/walkthrough-private-equity` and receive a multi-phase due diligence scenario that uses the investor classifier to score prospects
  2. Walkthrough covers multi-prospect comparison (side-by-side scoring) and portfolio company monitoring output
  3. Output interprets classifier results in PE/VC framing (investment thesis language, portfolio risk language) rather than generic ML output
**Plans**: TBD

Plans:
- [ ] 11-01: Private Equity walkthrough — walkthrough-private-equity.md scenario file, investor classifier due diligence sequence

### Phase 12: Walkthrough Test Suite
**Goal**: All 5 walkthrough slash commands have dedicated test files that validate structure, phase completeness, and MCP tool coverage — giving the team confidence that walkthroughs are structurally sound and will execute correctly
**Depends on**: Phase 11
**Requirements**: TEST-01
**Success Criteria** (what must be TRUE):
  1. Each of the 5 walkthroughs has its own test file (e.g., `test_walkthrough_hedge_fund.py`) that passes in the CI test suite
  2. Tests validate that each walkthrough file references the expected MCP tools for its scenario
  3. Tests validate that each walkthrough has the required phase structure (multi-phase scenario sections present)
  4. `pytest` passes with 0 failures across all 5 walkthrough test files
**Plans**: TBD

Plans:
- [ ] 12-01: Test files for all 5 walkthroughs — structure validation, tool coverage assertions, pytest integration

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Infrastructure & MCP Scaffold | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Market Analysis Tools | v1.0 | 4/4 | Complete | 2026-03-18 |
| 3. ML Workflow Tools | v1.0 | 5/5 | Complete | 2026-03-18 |
| 4. Web Publishing & Personas | v1.0 | 4/4 | Complete | 2026-03-18 |
| 5. Demo Command & Flow | v1.1 | 2/2 | Complete | 2026-03-18 |
| 6. Market Analysis Demos | v1.1 | 2/2 | Complete | 2026-03-18 |
| 7. ML Workflow Demos | v1.1 | 3/3 | Complete | 2026-03-18 |
| 8. Persona Demos | v1.1 | 2/2 | Complete | 2026-03-18 |
| 9. Market-Analysis Walkthroughs | v1.2 | 2/2 | Complete | 2026-03-18 |
| 10. Data-Profiling Walkthroughs | 2/2 | Complete    | 2026-03-18 | - |
| 11. ML-Classifier Walkthrough | v1.2 | 0/1 | Not started | - |
| 12. Walkthrough Test Suite | v1.2 | 0/1 | Not started | - |

---
*Last updated: 2026-03-18 — Phase 10 plans created*
