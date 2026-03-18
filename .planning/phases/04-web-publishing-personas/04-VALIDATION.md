---
phase: 4
slug: web-publishing-personas
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7+ |
| **Config file** | `pyproject.toml` (`[tool.pytest.ini_options]`) |
| **Quick run command** | `.venv/bin/python -m pytest tests/ -q --tb=short` |
| **Full suite command** | `.venv/bin/python -m pytest tests/ -v` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/python -m pytest tests/ -q --tb=short`
- **After every plan wave:** Run `.venv/bin/python -m pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 4-01-01 | 01 | 1 | WEB-01 | smoke | `pytest tests/test_http_server.py -x` | ❌ W0 | ⬜ pending |
| 4-01-02 | 01 | 1 | WEB-02 | manual | Manual — ngrok requires live internet | N/A | ⬜ pending |
| 4-02-01 | 02 | 2 | PERS-01 | unit | `pytest tests/test_persona_commands.py::test_analyst_command -x` | ❌ W0 | ⬜ pending |
| 4-02-02 | 02 | 2 | PERS-02 | unit | `pytest tests/test_persona_commands.py::test_pm_command -x` | ❌ W0 | ⬜ pending |
| 4-03-01 | 03 | 3 | WEB-03 | unit | `pytest tests/test_plugin_manifest.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_http_server.py` — stubs for WEB-01: imports `server_http.py`, mocks `mcp.run`, verifies `transport="streamable-http"` is passed
- [ ] `tests/test_plugin_manifest.py` — stubs for WEB-03: reads plugin.json, validates required fields (`name`, `version`, `description`), checks commands directory
- [ ] `tests/test_persona_commands.py` — stubs for PERS-01 and PERS-02: reads `finance-analyst.md` and `finance-pm.md`, checks frontmatter and role framing text

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ngrok tunnel produces public HTTPS URL and claude.ai connects through it | WEB-02 | Requires live internet + claude.ai Pro/Max/Team/Enterprise session; not automatable in unit tests | 1. Run `server_http.py`. 2. Start ngrok tunnel. 3. In claude.ai Settings > Connectors, enter the HTTPS URL. 4. Open a chat and call a finance tool. Verify response. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
