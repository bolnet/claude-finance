---
phase: 1
slug: infrastructure-mcp-scaffold
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-17
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `tests/conftest.py` (Wave 0 creates) |
| **Quick run command** | `python3 -m pytest tests/test_infrastructure.py -v --tb=short` |
| **Full suite command** | `python3 -m pytest tests/ -v --tb=short` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python3 -m pytest tests/test_infrastructure.py -v --tb=short`
- **After every plan wave:** Run `python3 -m pytest tests/ -v --tb=short`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 0 | MCP-01 | integration | `python3 -c "from src.finance_mcp.server import mcp; print('MCP OK')"` | ❌ W0 | ⬜ pending |
| 1-01-02 | 01 | 1 | MCP-01, MCP-02 | integration | `python3 -m pytest tests/test_mcp_server.py -v` | ❌ W0 | ⬜ pending |
| 1-01-03 | 01 | 1 | MCP-03 | manual | See manual table | N/A | ⬜ pending |
| 1-02-01 | 02 | 1 | INFRA-03 | unit | `python3 -m pytest tests/test_yfinance_adapter.py -v` | ❌ W0 | ⬜ pending |
| 1-02-02 | 02 | 1 | INFRA-06 | unit | `python3 -m pytest tests/test_data_validation.py -v` | ❌ W0 | ⬜ pending |
| 1-02-03 | 02 | 1 | INFRA-04 | unit | `python3 -m pytest tests/test_output_dir.py -v` | ❌ W0 | ⬜ pending |
| 1-02-04 | 02 | 1 | INFRA-01, INFRA-02 | integration | `python3 src/finance_mcp/check_env.py` | ❌ W0 | ⬜ pending |
| 1-03-01 | 03 | 2 | CMD-01, CMD-02 | manual | See manual table | N/A | ⬜ pending |
| 1-03-02 | 03 | 2 | CMD-03, CMD-04 | manual | See manual table | N/A | ⬜ pending |
| 1-03-03 | 03 | 2 | INFRA-05, INFRA-07 | unit | `python3 -m pytest tests/test_output_format.py -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/conftest.py` — shared fixtures (tmp dirs, mock yfinance responses)
- [ ] `tests/test_mcp_server.py` — stubs for MCP-01, MCP-02 (server importable, tool count)
- [ ] `tests/test_yfinance_adapter.py` — stubs for INFRA-03 (adapter returns DataFrame, handles bad ticker)
- [ ] `tests/test_data_validation.py` — stubs for INFRA-06 (empty DataFrame detected, user-friendly error returned)
- [ ] `tests/test_output_dir.py` — stubs for INFRA-04 (finance_output/charts/ created, PNG written correctly)
- [ ] `tests/test_output_format.py` — stubs for INFRA-05, INFRA-07 (disclaimer present, plain-English first)
- [ ] `pytest` installed: `pip install pytest pytest-mock`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `/finance` command invocable in Claude Code | CMD-01 | Claude Code UI interaction | Open Claude Code, type `/finance`, verify response not error |
| SKILL.md auto-loaded by Claude Code | CMD-02 | Runtime skill loading behavior | Confirm skill description appears in `/finance` context |
| Dynamic context injection (`!ls`, `!pip list`) fires | CMD-03 | Requires Claude Code runtime | Run `/finance test` and inspect that env info appears before code gen |
| Write-then-execute pattern (no inline -c) | CMD-04 | Requires inspecting Claude's behavior | Run `/finance analyze AAPL` and verify .py file created in finance_output/ before execution |
| MCP server connects via `.mcp.json` | MCP-03 | Requires Claude Code MCP handshake | Check Claude Code MCP panel shows finance server connected |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
