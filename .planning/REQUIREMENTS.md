# Requirements: Finance AI Skill — Interactive Demo

**Defined:** 2026-03-18
**Core Value:** Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## v1.1 Requirements

Requirements for the interactive demo milestone. Each maps to roadmap phases.

### Demo Command

- [x] **DEMO-01**: User can type `/demo` to start the interactive walkthrough
- [x] **DEMO-02**: Demo displays a welcome message explaining what the Finance AI Skill does
- [x] **DEMO-03**: Demo pauses after each tool's result with an explanation of what happened
- [x] **DEMO-04**: Demo shows a completion summary at the end with all tools demonstrated

### Market Analysis Demos

- [x] **MRKT-01**: Demo runs `analyze_stock` with a live ticker (e.g. AAPL) and shows price chart
- [x] **MRKT-02**: Demo runs `get_returns` and explains daily/cumulative return output
- [x] **MRKT-03**: Demo runs `get_volatility` and explains annualized volatility
- [x] **MRKT-04**: Demo runs `get_risk_metrics` and explains Sharpe/drawdown/beta
- [x] **MRKT-05**: Demo runs `compare_tickers` with two tickers (e.g. AAPL vs MSFT)
- [x] **MRKT-06**: Demo runs `correlation_map` and explains the heatmap

### ML Workflow Demos

- [ ] **MLWF-01**: Bundled sample CSV file ships with the project for demo use
- [ ] **MLWF-02**: Demo runs `ingest_csv` on the sample CSV and shows cleaning/EDA output
- [ ] **MLWF-03**: Demo runs `predict_liquidity` (train + predict) and explains regression results
- [ ] **MLWF-04**: Demo runs `classify_investor` (train + predict) and explains classification results

### Persona Demos

- [ ] **PERS-01**: Demo runs an analysis through `/finance-analyst` persona framing
- [ ] **PERS-02**: Demo runs the same analysis through `/finance-pm` persona framing
- [ ] **PERS-03**: Demo highlights the difference in framing between the two personas

## Future Requirements

- Alpha Vantage integration for fundamental data — DATA-01
- FRED integration for macroeconomic indicators — DATA-02
- Persona auto-detection via conversation context — deferred from v1.0
- Algorithmic trading backtesting — ADVX-01
- Portfolio optimization (efficient frontier) — ADVX-02

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automated end-to-end demo (no pauses) | Users need time to read and understand each tool's output |
| Web-based demo UI | Demo runs in Claude Code terminal only |
| Demo for claude.ai transport | Demo is a slash command; claude.ai uses MCP tools directly |
| Benchmarking / performance demo | Not relevant to user onboarding |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DEMO-01 | Phase 5 | Complete |
| DEMO-02 | Phase 5 | Complete |
| DEMO-03 | Phase 5 | Complete |
| DEMO-04 | Phase 5 | Complete |
| MRKT-01 | Phase 6 | Complete |
| MRKT-02 | Phase 6 | Complete |
| MRKT-03 | Phase 6 | Complete |
| MRKT-04 | Phase 6 | Complete |
| MRKT-05 | Phase 6 | Complete |
| MRKT-06 | Phase 6 | Complete |
| MLWF-01 | Phase 7 | Pending |
| MLWF-02 | Phase 7 | Pending |
| MLWF-03 | Phase 7 | Pending |
| MLWF-04 | Phase 7 | Pending |
| PERS-01 | Phase 8 | Pending |
| PERS-02 | Phase 8 | Pending |
| PERS-03 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 — traceability mapped to Phases 5–8*
