# Retrospective

Living retrospective — updated at each milestone completion.

---

## Milestone: v1.0 — Finance AI Skill MVP

**Shipped:** 2026-03-18
**Phases:** 4 | **Plans:** 16 | **Commits:** 72 | **Timeline:** 1 day (2026-03-17 → 2026-03-18)

### What Was Built

- FastMCP server with 11 tools — 3 infrastructure, 6 market analysis, 5 ML workflow; shared across stdio (Claude Code) and HTTP (claude.ai) transports
- Adapter isolation pattern: all yfinance calls behind `adapter.py`; output conventions (Agg backend, disclaimer, plain-English-first) enforced in `output.py`
- Two ML pipelines: liquidity regression (sklearn Pipeline, joblib persistence) and investor classifier (GridSearchCV + StratifiedKFold), each with train+evaluate tool and predict+infer tool
- 2 persona variants (equity analyst, portfolio manager) with zero new Python code — differentiation entirely in command framing
- Plugin package for claude.ai marketplace submission + ngrok launch script for browser users

### What Worked

- **Adapter pattern from Phase 1** — building `adapter.py` + `validators.py` + `output.py` before any analysis tools prevented data-correctness and backend bugs from propagating; every Phase 2-3 tool got correct behavior for free by importing these
- **Write-then-execute discipline** — documenting the pattern in both `finance.md` and `SKILL.md` at Phase 1 created a clear behavioral contract that shaped all subsequent phases
- **Two-tool ML pattern** (train/evaluate + predict/infer co-located in same module) — clean separation that made testing and MCP registration straightforward
- **Phase 4 reuse principle** — persona variants adding zero new Python code by reusing all existing MCP tools; differentiation entirely in command files; proved the MCP architecture was clean
- **Human verification checkpoints** at each phase end (01-03, 02-04, 03-05, 04-04) — caught behavioral-only concerns that automated tests cannot verify and provided explicit sign-off gates

### What Was Inefficient

- **SUMMARY frontmatter not populated** — 7 of 16 SUMMARY files have empty or missing `requirements-completed` and `one_liner` fields; the gsd-tools `summary-extract` command returned no data, causing the milestone archive to show "none recorded" for accomplishments; must populate these fields during plan execution, not retroactively
- **Nyquist VALIDATION.md files never promoted** — all 4 VALIDATION.md files were created during planning and never used; the files remained in `draft` state with `nyquist_compliant: false`; either run `/gsd:validate-phase` during execution or don't create the files at all
- **ROADMAP.md plan checkboxes not updated** — Phases 2, 3 plan checkboxes remained `[ ]` throughout execution (not checked as plans completed); the roadmap shows accurate phase-level status but plan-level history is incorrect
- **STATE.md progress percentage frozen at 67%** — STATE.md showed Phase 1 velocity metrics only and progress stuck at 67% throughout all subsequent phases; not a blocker but misleading when checking project status mid-milestone

### Patterns Established

- **Agg-before-pyplot import order** — `output.py` must be the first import in every tool file to ensure the matplotlib backend is locked before pyplot or seaborn loads; enforced as a test (`test_no_plt_show_in_codebase`)
- **`Close` not `Adj Close`** — yfinance 0.2.54+ auto_adjust=True makes `Close` the adjusted price; `Adj Close` removed from API; use `get_adjusted_prices()` accessor
- **`fastmcp.exceptions.ToolError`** — not `fastmcp.ToolError`; API moved in fastmcp 3.x; all tool files must import from the exceptions submodule
- **`mcp.add_tool()`** for Phase 2+ tool registration — imported functions must be registered explicitly; decorator-based registration only works for functions defined in `server.py` scope
- **`select_dtypes('object')`** not `'str'` for categorical detection — pandas does not recognize `'str'` as a dtype alias in `select_dtypes` across versions
- **`reindex(columns=train_cols, fill_value=0)`** for single-row inference after `get_dummies` — column alignment required when input schema differs from training schema

### Key Lessons

1. **Build the foundation before the tools.** Every Phase 2-3 tool worked cleanly because the adapter, validators, and output conventions were correct before any analysis code was written. The 3-plan Phase 1 investment paid back immediately in Phase 2.
2. **Populate SUMMARY frontmatter fields during execution.** The `one_liner` and `requirements-completed` fields must be written while the context is fresh. Retroactive population after phase completion is error-prone and the gsd-tools CLI depends on them.
3. **Shared-instance HTTP transport is the right architecture for MCP.** `server_http.py` at 29 lines (importing the same `mcp` object) is a better design than a separate server. Zero duplication of tool registration. Phase 4 was simple because of Phase 1's architecture.
4. **Persona differentiation belongs in the command file, not in code.** Writing zero new Python for two persona variants proved that clear MCP tool descriptions + role-framing in the command file is the correct abstraction boundary.

### Cost Observations

- Model mix: claude-sonnet-4-6 throughout (all phases)
- Yolo mode: all phases executed without confirmation gates
- Notable: Single-day delivery of 4 phases + 16 plans across a non-trivial MCP server with ML pipelines suggests the GSD workflow is well-suited to Python tool-building projects with clear phase boundaries

---

## Milestone: v1.1 — Interactive Demo

**Shipped:** 2026-03-18
**Phases:** 4 | **Plans:** 9 | **Commits:** 30 | **Timeline:** 1 day (2026-03-17 → 2026-03-18)

### What Was Built

- `/demo` slash command — 14-step guided walkthrough of all 11 MCP tools and both persona variants, with pause-and-explain flow between each step
- Live integration test suite for 6 market analysis tools using real Yahoo Finance data (xfail CI gate pattern)
- Bundled `demo/sample_portfolio.csv` (100-row synthetic data, numpy seed=42) for ML workflow demo steps
- Persona contrast demo: Steps 12-14 show analyst framing (Sharpe first) vs PM framing (drawdown/beta first) on same get_risk_metrics output
- Fixed liquidity_predictor column-mismatch bug — restricted training to 3-column feature set for stable inference

### What Worked

- **v1.0 architecture held up perfectly** — all 11 MCP tools were demo-ready with zero changes to tool implementations; the demo only needed correct parameter schemas in demo.md
- **xfail as CI gate** — `pytest.mark.network` + `xfail` allowed live integration tests to exist in CI without flaking; tests xpass when Yahoo Finance is reachable, gracefully degrade when not
- **Human verification via /demo** — running the actual slash command caught parameter mismatches (wrong date formats, string vs float types) that structural tests could not detect; adopted as acceptance gate for every phase
- **Iterative parameter correction** — Phase 6 corrected market tool schemas, Phase 7 corrected ML tool parameters, Phase 8 added persona steps; each phase built cleanly on the previous one's corrections

### What Was Inefficient

- **SUMMARY frontmatter still not populated** — v1.1 summaries again have null `one_liner` fields; the `gsd-tools summary-extract` command returned null for all 9 summaries; same issue as v1.0 that was identified but not fixed
- **Demo.md parameter schemas wrong on first write** — Phase 5 wrote demo.md with incorrect parameter names/formats for most tools; Phases 6 and 7 spent significant effort correcting these; should validate tool signatures before writing demo steps
- **Column-mismatch bug in liquidity_predictor** — training on all CSV columns caused inference failure when predict_liquidity received a 3-column input; discovered only through integration testing, not caught by existing unit tests

### Patterns Established

- **xfail + pytest.mark.network** — standard pattern for tests that require live API access; CI-safe with informative xpass/xfail reporting
- **Instructional prose for persona framing in slash commands** — demo.md simulates persona roles by telling Claude how to frame results, since slash commands cannot invoke other slash commands
- **Synthetic CSV with seed for reproducibility** — `numpy.default_rng(42)` produces identical data across runs; schema validates against both ML model column requirements
- **Reuse-data pattern** — Step 13 reuses Step 12 tool output instead of re-calling get_risk_metrics; avoids redundant API calls while demonstrating persona contrast

### Key Lessons

1. **Validate tool signatures before writing demo steps.** The biggest rework in v1.1 was correcting parameter schemas that didn't match actual MCP tool function signatures. A pre-write validation step would have saved Phases 6 and 7 significant correction effort.
2. **Integration tests reveal column alignment bugs that unit tests miss.** The liquidity_predictor bug only surfaced when real CSV data with more columns than the training features was passed through the full pipeline. Unit tests with mocked data never exercised this path.
3. **SUMMARY frontmatter population must be enforced during plan execution.** Two milestones in a row have this gap. The accomplishment extraction in milestone completion depends on `one_liner` fields that are consistently left empty.

### Cost Observations

- Model mix: claude-sonnet-4-6 throughout (all phases)
- Yolo mode: all phases executed without confirmation gates
- Notable: 9 plans completed same-day as v1.0, demonstrating that demo/test phases are faster than implementation phases (~3 min/plan avg vs ~5 min/plan for v1.0)

---

## Cross-Milestone Trends

| Metric | v1.0 | v1.1 |
|--------|------|------|
| Phases | 4 | 4 |
| Plans | 16 | 9 |
| LOC | ~2,767 Python | ~3,832 Python (cumulative) |
| Tests | 53 passed, 13 xpassed | 105 passing |
| Timeline | 1 day | 1 day |
| Requirements | 38/38 | 17/17 |
| Tech debt items | 10 (none blocking) | 10 carried (none blocking) |
| SUMMARY one_liner populated | 0/16 | 0/9 |
