---
phase: 16-plugin-infrastructure-and-deal-flow-skills
plan: "02"
subsystem: finance-mcp-plugin/skills/private-equity
tags: [private-equity, deal-flow, skills, commands, tests]
dependency_graph:
  requires: []
  provides:
    - finance-mcp-plugin/skills/private-equity/deal-sourcing/SKILL.md
    - finance-mcp-plugin/skills/private-equity/deal-screening/SKILL.md
    - finance-mcp-plugin/skills/private-equity/dd-checklist/SKILL.md
    - finance-mcp-plugin/skills/private-equity/dd-meeting-prep/SKILL.md
    - finance-mcp-plugin/skills/private-equity/ic-memo/SKILL.md
    - finance-mcp-plugin/commands/source.md
    - finance-mcp-plugin/commands/screen-deal.md
    - finance-mcp-plugin/commands/dd-checklist.md
    - finance-mcp-plugin/commands/dd-prep.md
    - finance-mcp-plugin/commands/ic-memo.md
    - tests/test_pe_deal_flow.py
  affects:
    - finance-mcp-plugin plugin manifest (new commands discoverable)
tech_stack:
  added: []
  patterns:
    - SKILL.md frontmatter pattern (name, description, version)
    - Lightweight command loader pattern (3-5 lines with skill path)
    - pytest parametrize for multi-skill/command validation
key_files:
  created:
    - finance-mcp-plugin/skills/private-equity/deal-sourcing/SKILL.md
    - finance-mcp-plugin/skills/private-equity/deal-screening/SKILL.md
    - finance-mcp-plugin/skills/private-equity/dd-checklist/SKILL.md
    - finance-mcp-plugin/skills/private-equity/dd-meeting-prep/SKILL.md
    - finance-mcp-plugin/skills/private-equity/ic-memo/SKILL.md
    - finance-mcp-plugin/commands/source.md
    - finance-mcp-plugin/commands/screen-deal.md
    - finance-mcp-plugin/commands/dd-checklist.md
    - finance-mcp-plugin/commands/dd-prep.md
    - finance-mcp-plugin/commands/ic-memo.md
    - tests/test_pe_deal_flow.py
  modified: []
decisions:
  - "SKILL.md files capped at 400 lines per plan spec — ic-memo trimmed from 461 to 394 lines by condensing tables and template blocks while preserving all substantive content"
  - "Commands use 4-line body format (frontmatter + blank + load instruction) — all pass 3-10 line lightweight check"
  - "Test suite uses pytest.mark.parametrize for per-skill/command checks; conftest.py requires pandas so tests run via venv for isolation"
metrics:
  duration_seconds: 609
  completed_date: "2026-03-19"
  tasks_completed: 2
  files_created: 11
  tests_passing: 22
---

# Phase 16 Plan 02: PE Deal-Flow Skills and Commands Summary

**One-liner:** Five PE deal-flow skills (200-400 lines each) with MCP ingest_csv/classify_investor integration and five lightweight command loaders, validated by 22-test pytest suite.

---

## What Was Built

### Task 1: 5 Deal-Flow PE Skills

| Skill | Lines | MCP Tool | Key Framework |
|-------|-------|----------|---------------|
| deal-sourcing | 328 | `ingest_csv` | Thesis criteria, CRM profiling, fit scoring rubric, outreach templates |
| deal-screening | 257 | `ingest_csv` | 10-criterion pass/fail checklist, knockout triggers, one-page screening memo |
| dd-checklist | 297 | `ingest_csv` | 7 workstreams (64 items), 5 sector add-on sets, data room request list |
| dd-meeting-prep | 387 | — | Management/expert/customer prep, function-specific questions, red flag table |
| ic-memo | 394 | `classify_investor` | 10-section IC memo template, returns/sensitivity tables, quantitative scoring |

### Task 2: 5 Commands and Test Suite

Each command is a 4-line lightweight loader following the established pattern:
- `source.md` → loads deal-sourcing skill
- `screen-deal.md` → loads deal-screening skill
- `dd-checklist.md` → loads dd-checklist skill
- `dd-prep.md` → loads dd-meeting-prep skill
- `ic-memo.md` → loads ic-memo skill

`tests/test_pe_deal_flow.py`: 22 tests covering skill existence, YAML frontmatter, minimum line count (parametrized), MCP tool references, pass/fail content, command existence, command frontmatter, lightweight size constraint (parametrized), and skill linkages (parametrized).

---

## Verification

```
python3 -m pytest tests/test_pe_deal_flow.py -v
22 passed in 0.01s
```

All 5 skills: 200-400 lines, YAML frontmatter, MCP tool references confirmed.
All 5 commands: 3-10 lines, frontmatter present, skill name referenced in body.

---

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] ic-memo SKILL.md exceeded 400-line maximum**
- **Found during:** Task 1 verification
- **Issue:** Initial ic-memo was 461 lines (61 over the 400-line cap in plan spec)
- **Fix:** Condensed Section 3 (market/industry), Section 7 (deal terms), Section 8 (value creation), Section 9 (returns analysis), and error handling table — preserving all substantive PE frameworks while reducing whitespace and verbose templates
- **Files modified:** `finance-mcp-plugin/skills/private-equity/ic-memo/SKILL.md`
- **Result:** 394 lines — within spec

---

## Self-Check

Files exist:
- `finance-mcp-plugin/skills/private-equity/deal-sourcing/SKILL.md` — FOUND
- `finance-mcp-plugin/skills/private-equity/deal-screening/SKILL.md` — FOUND
- `finance-mcp-plugin/skills/private-equity/dd-checklist/SKILL.md` — FOUND
- `finance-mcp-plugin/skills/private-equity/dd-meeting-prep/SKILL.md` — FOUND
- `finance-mcp-plugin/skills/private-equity/ic-memo/SKILL.md` — FOUND
- `finance-mcp-plugin/commands/source.md` — FOUND
- `finance-mcp-plugin/commands/screen-deal.md` — FOUND
- `finance-mcp-plugin/commands/dd-checklist.md` — FOUND
- `finance-mcp-plugin/commands/dd-prep.md` — FOUND
- `finance-mcp-plugin/commands/ic-memo.md` — FOUND
- `tests/test_pe_deal_flow.py` — FOUND

Commits:
- `dcc27f9` — feat(16-02): create 5 PE deal-flow skills — FOUND
- `dd81ea8` — feat(16-02): create 5 PE commands and test suite — FOUND

## Self-Check: PASSED
