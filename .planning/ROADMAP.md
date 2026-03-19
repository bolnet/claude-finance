# Roadmap: Finance AI Skill for Claude Code

## Milestones

- ✅ **v1.0 Finance AI Skill MVP** — Phases 1–4 (shipped 2026-03-18)
- ✅ **v1.1 Interactive Demo** — Phases 5–8 (shipped 2026-03-18)
- ✅ **v1.2 Role Walkthroughs** — Phases 9–12 (shipped 2026-03-18)
- ✅ **v1.3 GitHub Pages Site** — Phases 13–15 (shipped 2026-03-19)
- 🔄 **v1.4 Private Equity Plugin (Anthropic Pattern)** — Phases 16–18 (active)

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

<details>
<summary>✅ v1.2 Role Walkthroughs (Phases 9–12) — SHIPPED 2026-03-18</summary>

- [x] **Phase 9: Market-Analysis Walkthroughs** — Hedge Fund and Investment Banking walkthroughs using volatility, correlation, and comparison tools (2/2 plans, completed 2026-03-18)
- [x] **Phase 10: Data-Profiling Walkthroughs** — FP&A and Accounting walkthroughs using CSV ingestion, data profiling, and liquidity predictor (2/2 plans, completed 2026-03-18)
- [x] **Phase 11: ML-Classifier Walkthrough** — Private Equity walkthrough using investor classifier for due diligence scoring (1/1 plans, completed 2026-03-18)
- [x] **Phase 12: Walkthrough Test Suite** — Dedicated test files for all 5 walkthroughs validating structure, phases, and MCP tool coverage (1/1 plans, completed 2026-03-18)

Full phase details: `.planning/milestones/v1.2-ROADMAP.md`

</details>

<details>
<summary>✅ v1.3 GitHub Pages Site (Phases 13–15) — SHIPPED 2026-03-19</summary>

- [x] **Phase 13: Site Scaffolding and Visual Assets** — docs/ folder structure, .nojekyll, shared HTML/CSS template, mobile viewport, 6-8 curated chart PNGs web-optimized and staged in docs/assets/images/ (2/2 plans, completed 2026-03-18)
- [x] **Phase 14: Content Pages** — Landing page (hero, chart visuals, role entry points, stats bar), Features page (11 MCP tools by category), Walkthroughs page (6 role cards with scenario + chart) (2/2 plans, completed 2026-03-19)
- [x] **Phase 15: Getting Started and Polish** — Getting Started page (two install paths), social card OG image, cross-page navigation audit, Lighthouse verification (2/2 plans, completed 2026-03-19)

Full phase details: `.planning/milestones/v1.3-ROADMAP.md`

</details>

### v1.4 Private Equity Plugin (Anthropic Pattern) (Active)

**Milestone Goal:** Restructure the private equity offering to match Anthropic's financial-services-plugins pattern — complete plugin infrastructure, 15 dedicated PE skills (10 Anthropic-pattern + 5 analytical engine), and 15 lightweight commands — installable via `claude plugin install`.

- [x] **Phase 16: Plugin Infrastructure and Deal Flow Skills** - Plugin manifest, hooks, MCP wiring, directory structure + deal-sourcing, deal-screening, dd-checklist, dd-meeting-prep, ic-memo skills and their commands (completed 2026-03-19)
- [x] **Phase 17: Portfolio and Value Creation Skills** - portfolio-monitoring, returns-analysis, unit-economics, value-creation-plan, ai-readiness skills and their commands (completed 2026-03-19)
- [x] **Phase 18: Analytical Engine Skills** - prospect-scoring, liquidity-risk, pipeline-profiling, public-comp-analysis, market-risk-scan skills (MCP-powered) and their commands (completed 2026-03-19)

## Phase Details

### Phase 16: Plugin Infrastructure and Deal Flow Skills
**Goal**: The plugin is installable with a valid manifest and MCP wiring, and PE professionals can invoke deal-flow commands (sourcing, screening, diligence checklist, meeting prep, IC memo) that load fully-authored skills
**Depends on**: Nothing (first v1.4 phase)
**Requirements**: PLUG-01, PLUG-02, PLUG-03, PLUG-04, SKILL-01, SKILL-02, SKILL-03, SKILL-04, SKILL-05, CMD-01, CMD-02, CMD-03, CMD-04, CMD-05
**Success Criteria** (what must be TRUE):
  1. Running `claude plugin install` against the finance-mcp-plugin directory completes without errors and the plugin appears in the installed list
  2. `.claude-plugin/plugin.json` contains correct bolnet/Claude-Finance URLs, version, and author — no `[owner]` placeholder remaining
  3. A PE professional can invoke `/project:source` and receive a deal-sourcing workflow that uses MCP `ingest_csv` to profile CRM data
  4. A PE professional can invoke `/project:screen-deal` and receive a pass/fail screening framework with a one-page memo structure
  5. A PE professional can invoke `/project:ic-memo` and receive a structured IC memo template that calls `classify_investor` for quantitative scoring
**Plans**: 2 plans

Plans:
- [x] 16-01-PLAN.md — Plugin infrastructure: plugin.json, hooks/hooks.json, .mcp.json, directory structure (PLUG-01 through PLUG-04)
- [x] 16-02-PLAN.md — Deal flow skills: deal-sourcing, deal-screening, dd-checklist, dd-meeting-prep, ic-memo (SKILL-01 through SKILL-05) and their commands (CMD-01 through CMD-05)

### Phase 17: Portfolio and Value Creation Skills
**Goal**: PE professionals can invoke portfolio-stage commands (monitoring, returns, unit economics, value creation, AI readiness) that load fully-authored skills with clear frameworks and MCP tool integration where applicable
**Depends on**: Phase 16
**Requirements**: SKILL-06, SKILL-07, SKILL-08, SKILL-09, SKILL-10, CMD-06, CMD-07, CMD-08, CMD-09, CMD-10
**Success Criteria** (what must be TRUE):
  1. A PE professional can invoke `/project:portfolio` and receive a KPI tracking dashboard framework that calls `classify_investor` for classification drift and `get_risk_metrics` for market benchmarks
  2. A PE professional can invoke `/project:returns` and receive IRR/MOIC sensitivity tables backed by live `get_returns` and `get_risk_metrics` MCP data for public comps
  3. A PE professional can invoke `/project:unit-economics` and receive an ARR cohort and LTV/CAC analysis framework that uses `ingest_csv` for cohort data profiling
  4. A PE professional can invoke `/project:value-creation` and receive an EBITDA bridge with a 100-day plan and KPI target structure
  5. A PE professional can invoke `/project:ai-readiness` and receive a per-company go/wait gate with quick wins ranked by EBITDA impact
**Plans**: 2 plans

Plans:
- [x] 17-01-PLAN.md — Portfolio and value creation skills: portfolio-monitoring, returns-analysis, unit-economics, value-creation-plan, ai-readiness (SKILL-06 through SKILL-10)
- [x] 17-02-PLAN.md — Portfolio commands and test suite: portfolio, returns, unit-economics, value-creation, ai-readiness commands (CMD-06 through CMD-10)

### Phase 18: Analytical Engine Skills
**Goal**: PE professionals can invoke MCP-powered analytical commands (prospect scoring, liquidity risk, pipeline profiling, public comps, market risk) that run live ML models and market data tools — our unique advantage over Anthropic's vanilla plugin
**Depends on**: Phase 17
**Requirements**: SKILL-11, SKILL-12, SKILL-13, SKILL-14, SKILL-15, CMD-11, CMD-12, CMD-13, CMD-14, CMD-15
**Success Criteria** (what must be TRUE):
  1. A PE professional can invoke `/project:score-prospect` and the skill trains an ML classifier on a CRM CSV export via `investor_classifier`, then scores individual prospects with confidence levels via `classify_investor`
  2. A PE professional can invoke `/project:liquidity-risk` and the skill trains a regression model on portfolio data via `liquidity_predictor` and returns predicted liquidity risk scores via `predict_liquidity`
  3. A PE professional can invoke `/project:profile-pipeline` and receive a full EDA report (completeness, distributions, outliers, data quality flags) on a CRM CSV export via `ingest_csv`
  4. A PE professional can invoke `/project:public-comps` and receive a comparison chart and correlation heatmap for public market comps via `compare_tickers` and `correlation_map`
  5. A PE professional can invoke `/project:market-risk` and receive Sharpe ratio, drawdown, and beta for public benchmarks via `get_volatility`, `get_risk_metrics`, and `analyze_stock`
**Plans**: 2 plans

Plans:
- [ ] 18-01-PLAN.md — Analytical engine skills: prospect-scoring, liquidity-risk, pipeline-profiling, public-comp-analysis, market-risk-scan (SKILL-11 through SKILL-15)
- [ ] 18-02-PLAN.md — Analytical engine commands and test suite: score-prospect, liquidity-risk, profile-pipeline, public-comps, market-risk commands (CMD-11 through CMD-15)

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
| 10. Data-Profiling Walkthroughs | v1.2 | 2/2 | Complete | 2026-03-18 |
| 11. ML-Classifier Walkthrough | v1.2 | 1/1 | Complete | 2026-03-18 |
| 12. Walkthrough Test Suite | v1.2 | 1/1 | Complete | 2026-03-18 |
| 13. Site Scaffolding and Visual Assets | v1.3 | 2/2 | Complete | 2026-03-18 |
| 14. Content Pages | v1.3 | 2/2 | Complete | 2026-03-19 |
| 15. Getting Started and Polish | v1.3 | 2/2 | Complete | 2026-03-19 |
| 16. Plugin Infrastructure and Deal Flow Skills | v1.4 | 2/2 | Complete | 2026-03-19 |
| 17. Portfolio and Value Creation Skills | v1.4 | 2/2 | Complete | 2026-03-19 |
| 18. Analytical Engine Skills | 2/2 | Complete    | 2026-03-19 | - |

---
*Last updated: 2026-03-19 — Phase 18 planned (2 plans)*
