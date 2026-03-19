# Requirements: Finance AI Skill — v1.4 Private Equity Plugin (Anthropic Pattern)

**Defined:** 2026-03-19
**Core Value:** Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## v1.4 Requirements

Requirements for restructuring PE into Anthropic's plugin pattern with MCP-powered analytical engine.

### Plugin Infrastructure

- [x] **PLUG-01**: `plugin.json` manifest with name, version, description, author, correct bolnet/Claude-Finance URLs
- [x] **PLUG-02**: `hooks/hooks.json` file (empty array)
- [x] **PLUG-03**: `.mcp.json` referencing finance MCP server for all tool-powered skills
- [x] **PLUG-04**: Plugin directory follows Anthropic's structure: `.claude-plugin/`, `commands/`, `skills/`, `hooks/`

### PE Skills — Anthropic Pattern (10 skills matching their coverage)

- [x] **SKILL-01**: `deal-sourcing` skill — discover targets by criteria, CRM check, draft founder outreach; references MCP `ingest_csv` for CRM data profiling
- [x] **SKILL-02**: `deal-screening` skill — screen CIMs/teasers against fund criteria, pass/fail framework, one-page memo; references MCP `ingest_csv` for deal data extraction
- [x] **SKILL-03**: `dd-checklist` skill — sector-tailored diligence workstreams with request lists and status tracking; references MCP `ingest_csv` for data room file profiling
- [x] **SKILL-04**: `dd-meeting-prep` skill — targeted questions, benchmarks, red flags for management meetings, expert calls, customer references
- [x] **SKILL-05**: `ic-memo` skill — structured IC memo synthesizing diligence, financials, deal terms; references MCP `classify_investor` for quantitative scoring
- [ ] **SKILL-06**: `portfolio-monitoring` skill — KPI tracking, drift detection, quarterly dashboard; references MCP `classify_investor` for classification drift and `get_risk_metrics` for market benchmarks
- [ ] **SKILL-07**: `returns-analysis` skill — IRR/MOIC sensitivity tables, entry/exit scenarios; references MCP `get_returns` and `get_risk_metrics` for public comp return data
- [ ] **SKILL-08**: `unit-economics` skill — ARR cohorts, LTV/CAC, net retention, revenue quality analysis; references MCP `ingest_csv` for cohort data profiling
- [ ] **SKILL-09**: `value-creation-plan` skill — EBITDA bridge, 100-day plan, KPI targets, operational levers
- [ ] **SKILL-10**: `ai-readiness` skill — portfolio AI opportunity scan, per-company go/wait gate, quick wins ranked by EBITDA impact

### PE Skills — Analytical Engine (5 MCP-powered skills unique to us)

- [ ] **SKILL-11**: `prospect-scoring` skill — train ML classifier on CRM export, score individual prospects with confidence; uses MCP `investor_classifier` + `classify_investor`
- [ ] **SKILL-12**: `liquidity-risk` skill — train regression model on portfolio data, predict liquidity risk per target; uses MCP `liquidity_predictor` + `predict_liquidity`
- [ ] **SKILL-13**: `pipeline-profiling` skill — full EDA on CRM exports: completeness, distributions, outliers, data quality; uses MCP `ingest_csv`
- [ ] **SKILL-14**: `public-comp-analysis` skill — compare public market comps for valuation context, correlation analysis; uses MCP `compare_tickers` + `correlation_map`
- [ ] **SKILL-15**: `market-risk-scan` skill — Sharpe, drawdown, beta for public benchmarks of portfolio companies; uses MCP `get_volatility` + `get_risk_metrics` + `analyze_stock`

### PE Commands (15 lightweight loaders)

- [x] **CMD-01**: `source.md` command — loads deal-sourcing skill (3-5 lines)
- [x] **CMD-02**: `screen-deal.md` command — loads deal-screening skill
- [x] **CMD-03**: `dd-checklist.md` command — loads dd-checklist skill
- [x] **CMD-04**: `dd-prep.md` command — loads dd-meeting-prep skill
- [x] **CMD-05**: `ic-memo.md` command — loads ic-memo skill
- [ ] **CMD-06**: `portfolio.md` command — loads portfolio-monitoring skill
- [ ] **CMD-07**: `returns.md` command — loads returns-analysis skill
- [ ] **CMD-08**: `unit-economics.md` command — loads unit-economics skill
- [ ] **CMD-09**: `value-creation.md` command — loads value-creation-plan skill
- [ ] **CMD-10**: `ai-readiness.md` command — loads ai-readiness skill
- [ ] **CMD-11**: `score-prospect.md` command — loads prospect-scoring skill
- [ ] **CMD-12**: `liquidity-risk.md` command — loads liquidity-risk skill
- [ ] **CMD-13**: `profile-pipeline.md` command — loads pipeline-profiling skill
- [ ] **CMD-14**: `public-comps.md` command — loads public-comp-analysis skill
- [ ] **CMD-15**: `market-risk.md` command — loads market-risk-scan skill

## Future Requirements

### Additional Verticals

- **VERT-01**: Investment Banking plugin (same Anthropic pattern)
- **VERT-02**: Equity Research plugin (same Anthropic pattern)
- **VERT-03**: Wealth Management plugin (same Anthropic pattern)
- **VERT-04**: FP&A plugin (same Anthropic pattern)

### Marketplace

- **MKT-01**: Register as marketplace for `claude plugin marketplace add`
- **MKT-02**: PyPI publish for `pip install finance-mcp`

## Out of Scope

| Feature | Reason |
|---------|--------|
| Other verticals (IB, ER, WM) | v1.4 is PE only — other verticals deferred to future milestones |
| New MCP tools | v1.4 uses existing 11 tools — no new Python code for tool registration |
| Modifying existing walkthrough | walkthrough-private-equity.md stays unchanged alongside new plugin |
| Real CRM integration (email/Slack) | Anthropic's deal-sourcing references Gmail/Slack MCP — we don't have those connectors |
| PyPI publishing | Separate milestone concern |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLUG-01 | Phase 16 | Complete |
| PLUG-02 | Phase 16 | Complete |
| PLUG-03 | Phase 16 | Complete |
| PLUG-04 | Phase 16 | Complete |
| SKILL-01 | Phase 16 | Complete |
| SKILL-02 | Phase 16 | Complete |
| SKILL-03 | Phase 16 | Complete |
| SKILL-04 | Phase 16 | Complete |
| SKILL-05 | Phase 16 | Complete |
| SKILL-06 | Phase 17 | Pending |
| SKILL-07 | Phase 17 | Pending |
| SKILL-08 | Phase 17 | Pending |
| SKILL-09 | Phase 17 | Pending |
| SKILL-10 | Phase 17 | Pending |
| SKILL-11 | Phase 18 | Pending |
| SKILL-12 | Phase 18 | Pending |
| SKILL-13 | Phase 18 | Pending |
| SKILL-14 | Phase 18 | Pending |
| SKILL-15 | Phase 18 | Pending |
| CMD-01 | Phase 16 | Complete |
| CMD-02 | Phase 16 | Complete |
| CMD-03 | Phase 16 | Complete |
| CMD-04 | Phase 16 | Complete |
| CMD-05 | Phase 16 | Complete |
| CMD-06 | Phase 17 | Pending |
| CMD-07 | Phase 17 | Pending |
| CMD-08 | Phase 17 | Pending |
| CMD-09 | Phase 17 | Pending |
| CMD-10 | Phase 17 | Pending |
| CMD-11 | Phase 18 | Pending |
| CMD-12 | Phase 18 | Pending |
| CMD-13 | Phase 18 | Pending |
| CMD-14 | Phase 18 | Pending |
| CMD-15 | Phase 18 | Pending |

**Coverage:**
- v1.4 requirements: 34 total
- Mapped to phases: 34
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-19*
*Last updated: 2026-03-19 — traceability complete after roadmap creation*
