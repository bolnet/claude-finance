---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Interactive Demo
status: planning
stopped_at: Completed 06-01-PLAN.md
last_updated: "2026-03-18T15:10:24.976Z"
last_activity: 2026-03-18 — v1.1 roadmap created
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 4
  completed_plans: 3
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-18)

**Core value:** Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.
**Current focus:** v1.1 Interactive Demo — /demo slash command walkthrough of all 11 MCP tools and both personas

## Current Position

Phase: 5 — Demo Command & Flow (Not started)
Plan: —
Status: Roadmap defined, ready for Phase 5 planning
Last activity: 2026-03-18 — v1.1 roadmap created

```
Progress: [                    ] 0% (0/9 plans)
Phase 5: [ ] [ ]
Phase 6: [ ] [ ]
Phase 7: [ ] [ ] [ ]
Phase 8: [ ] [ ]
```

## Performance Metrics

**Velocity (v1.0 baseline):**
- Total plans completed: 16
- Average duration: ~5 min/plan
- Total execution time: ~1.3 hours

**By Phase (v1.0):**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-infrastructure-mcp-scaffold | 3/3 | ~10 min | ~3 min |
| 02-market-analysis-tools | 4/4 | ~16 min | ~4 min |
| 03-ml-workflow-tools | 5/5 | ~35 min | ~7 min |
| 04-web-publishing-personas | 4/4 | ~20 min | ~5 min |

*v1.1 metrics will populate after plans complete*
| Phase 05-demo-command-flow P01 | 13 | 2 tasks | 2 files |
| Phase 05-demo-command-flow P02 | 15 | 2 tasks | 1 files |
| Phase 06-market-analysis-demos P01 | 3 | 2 tasks | 3 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Phase 1]: Build yfinance adapter layer before any analysis workflow — data correctness bugs propagate to every workflow if not fixed at foundation
- [Phase 1, SUPERSEDED by 01-02]: Use `Adj Close` exclusively — CORRECTION: yfinance 0.2.54+ auto_adjust=True makes `Close` the adjusted price; `Adj Close` does not exist; use `Close` (via get_adjusted_prices())
- [Phase 3]: Split data before any `.fit()` call — enforced in code templates, not retrofitted; look-ahead bias is unrecoverable
- [01-01]: fastmcp.exceptions.ToolError (not fastmcp.ToolError) — API moved in fastmcp 3.x; all future tool files must import from exceptions submodule
- [01-01]: .venv virtual environment at project root — PEP 668 blocks system pip on macOS Homebrew Python 3.14; use .venv/bin/python3 for all pytest and server runs
- [01-01]: setuptools.build_meta build backend (not setuptools.backends.legacy) — legacy path removed in current setuptools
- [Phase 01-02]: Close column is adjusted price (auto_adjust=True in yfinance 0.2.54+); Adj Close removed; get_adjusted_prices() accessor enforces this
- [Phase 01-02]: matplotlib.use(Agg) in output.py module scope before pyplot import; plt.show() string banned across all src; enforced by test
- [Phase 01-02]: validate_dataframe requires minimum 2 rows — single-row DataFrames break return calculations; fail fast at fetch time
- [Phase 01-infrastructure-mcp-scaffold]: /finance command uses dynamic context injection (!command syntax) for python version, packages, pwd, CSV files, and output dir status before any code generation
- [Phase 01-infrastructure-mcp-scaffold]: Write-then-execute is the ONLY allowed Python execution method — finance_output/last_run.py written via Write tool, then executed via Bash; no inline python3 -c strings
- [Phase 02-market-analysis-tools]: Use mcp.add_tool() for Phase 2 tool registration — imported functions must be registered explicitly, not decorated
- [Phase 02-market-analysis-tools]: Import finance_mcp.output first in all tools/ modules — ensures Agg backend set before pyplot
- [Phase 02-market-analysis-tools]: _compute_risk_metrics exposed as public function — allows direct unit testing of Sharpe/drawdown/beta math without mocking fetch_price_history or the full tool I/O
- [Phase 02-market-analysis-tools]: Sharpe ratio computed with rf=0; FRED integration deferred and noted in output text as future enhancement
- [Phase 02-market-analysis-tools]: get_risk_metrics fetches ^GSPC benchmark via same fetch_price_history adapter — reuses existing validation and DataFetchError handling
- [Phase 02-market-analysis-tools]: Import seaborn inside correlation_map function body — ensures output.py has set Agg backend before seaborn loads
- [Phase 02-market-analysis-tools]: Correlation computed on pct_change().dropna() not raw prices — return-based correlation avoids spurious correlations from shared price trends
- [Phase 03-ml-workflow-tools]: pandas select_dtypes uses 'object'/'string' not 'str' for categorical column detection — 'str' dtype alias not recognized in select_dtypes across pandas versions
- [Phase 03-ml-workflow-tools]: IQR outlier filter preserves NaN rows during outlier pass (isna() OR bounds) then fills with median — prevents valid rows being dropped due to missing values in the filtered column
- [Phase 03-ml-workflow-tools]: liquidity_model.py named to match test stub import path (not liquidity_predictor.py as plan specified)
- [Phase 03-ml-workflow-tools]: Two-tool ML pattern established: train/evaluate tool + predict/inference tool co-located in same module
- [Phase 03-ml-workflow-tools]: investor_model.py named to match test stub import path — tests import from investor_model not investor_classifier
- [Phase 03-ml-workflow-tools]: classify_investor uses reindex(columns=train_cols, fill_value=0) for column alignment in single-row inference after get_dummies
- [Phase 03-ml-workflow-tools]: No changes needed to tool modules — 03-02 and 03-03 implementations were correct and complete at merge
- [Phase 03-ml-workflow-tools]: Direct imports (not try/except guards) are the correct post-integration pattern for test files
- [Phase 03-ml-workflow-tools]: Human verification sign-off is the acceptance gate for ML tools — synthetic unit tests prove correctness, real CSV verification proves the tool handles unknown column schemas and real distributions
- [Phase 03-ml-workflow-tools]: Chart visual inspection is a required acceptance criterion — feature importance bars with real column names confirm get_dummies column alignment works correctly on unseen data
- [Phase 04-web-publishing-personas]: server_http.py imports mcp from server.py (same object) — all tools available with zero duplication; stdio server unchanged for Claude Code
- [Phase 04-web-publishing-personas]: start() function abstraction enables unit testing HTTP server without spawning a real process — mocker.patch on finance_mcp.server.mcp.run
- [Phase 04-web-publishing-personas]: Persona commands reuse all existing MCP tools — zero new Python code; differentiation is entirely in role framing and intent routing
- [Phase 04-web-publishing-personas]: finance-analyst emphasizes Sharpe/drawdown vs S&P 500 in single-stock context; finance-pm leads with drawdown/beta before Sharpe and treats tickers as portfolio holdings
- [Phase 04-web-publishing-personas]: Plugin .mcp.json uses python -m finance_mcp.server (pip-installed), not .venv path — distributable without project clone
- [Phase 04-web-publishing-personas]: start_web.sh reads ngrok URL from localhost:4040 API — avoids parsing ngrok stdout which varies by version
- [Phase 04-web-publishing-personas]: Cloudflare Tunnel documented in start_web.sh as persistent-URL alternative to ngrok free tier
- [Phase 04-web-publishing-personas]: Human verification sign-off is the acceptance gate for Phase 4 — automated tests prove structural correctness; human review confirms persona framing works in Claude Code
- [Phase 04-web-publishing-personas]: WEB-02 ngrok live URL test deferred to real deployment; automated import test sufficient for CI gate
- [Phase 05-demo-command-flow]: /demo takes no arguments — self-running walkthrough with pause-and-explain, CSV skip logic for Steps 9-11
- [Phase 05-demo-command-flow]: All 13 MCP function names in allowed-tools (13 functions = 11 logical tools; pairs counted as one logical tool)
- [Phase 05-demo-command-flow]: Frontmatter parser splits on first two --- delimiters only — body can contain --- horizontal rule without breaking slash command tests
- [Phase 06-market-analysis-demos]: demo.md Steps 3-8 use start: [N days before today, YYYY-MM-DD format] dynamic instruction pattern — computes dates at Claude runtime
- [Phase 06-market-analysis-demos]: xfail used as CI gate for network tests — tests degrade gracefully when Yahoo Finance unreachable, xpassed when live

### Pending Todos

None yet.

### Blockers/Concerns

None — v1.0 complete. v1.1 roadmap ready.

## Session Continuity

Last session: 2026-03-18T15:10:15.630Z
Stopped at: Completed 06-01-PLAN.md
Resume file: None
