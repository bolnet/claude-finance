---
phase: 15-getting-started-and-polish
plan: "01"
subsystem: docs
tags: [getting-started, install-guide, html, css, two-path]
dependency_graph:
  requires: [14-02]
  provides: [getting-started-page]
  affects: [docs/getting-started.html, docs/assets/css/style.css]
tech_stack:
  added: []
  patterns: [two-path install section, numbered step layout, callout note, dark code block]
key_files:
  created: []
  modified:
    - docs/getting-started.html
    - docs/assets/css/style.css
decisions:
  - "Used two stacked sections (not JS tabs) for install paths — sections scroll better for finance professionals and work without JavaScript"
  - "HTTP server command is python -m finance_mcp.server_http per plan interfaces (not --transport flag variant from research)"
  - "All new CSS added to shared style.css — no separate getting-started.css per Phase 15 research anti-patterns"
metrics:
  duration: 3 minutes
  completed_date: "2026-03-19"
  tasks_completed: 2
  files_changed: 2
---

# Phase 15 Plan 01: Getting Started — Two-Path Install Page Summary

**One-liner:** Full two-path install page (Claude Code stdio + claude.ai HTTP/ngrok) with numbered steps, copy-pasteable commands, ngrok URL warning, and plain-English troubleshooting — replacing the page-stub stub.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add install step CSS classes to shared style.css | 07df032 | docs/assets/css/style.css |
| 2 | Replace getting-started.html stub with full two-path install content | 66c890f | docs/getting-started.html |

## What Was Built

**Task 1 — CSS classes (style.css):**
Added a new `/* ===== GETTING STARTED PAGE ===== */` section with 13 class definitions:
- `.install-path` / `.install-path:last-of-type` — section wrappers with bottom border separator
- `.path-heading` — 1.5rem bold heading with 3px red bottom border (matches feature-category h2 pattern)
- `.path-audience` — grey 0.95rem subtitle below heading
- `.step` — flex row layout for numbered steps
- `.step-num` — 2rem dark-blue circle with centered white number
- `.step-content` / `.step-content strong` / `.step-content p` — step text layout
- `.code-block` — dark (#1a1a2e) monospace block for copy-paste commands
- `.callout-note` / `.callout-note strong` — yellow (#fff8e1) warning box with amber left border
- `.first-analysis` — light grey section for the shared example prompt
Plus `@media (max-width: 768px)` overrides: `.step` goes column, `.code-block` reduces to 0.78rem.

**Task 2 — getting-started.html (full content):**
- Page header: "Get Started" + "Start analyzing finance data in minutes" subtitle
- Path A (Claude Code — 4 steps): clone repo, pip install -e ., run claude, type /finance
- Path B (claude.ai — 5 steps): clone+install, start HTTP server, ngrok tunnel setup, add integration to claude.ai, type /finance
- Callout warning on Path B Step 3 about free-tier ngrok URL regeneration on restart, with link to claim static domain
- First Analysis section: "Show me a 6-month price comparison of Apple, Google, and Microsoft" prompt
- Troubleshooting: 3 pre-empted failures (yfinance rate limits, python not found, ngrok auth required)

## Verification Results

**Automated checks (all PASS):**
- claude-code section present (id="claude-code")
- claude-ai section present (id="claude-ai")
- pip install -e . present
- ngrok http 8000 present
- callout-note present
- code-block count >= 5
- no absolute /assets/ paths
- no page-stub content remaining
- step-num elements >= 8

**Python test suite:** 151 passed, 1 xfailed, 19 xpassed — no regression.

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check

**Files exist:**
- docs/getting-started.html: present
- docs/assets/css/style.css: present

**Commits exist:**
- 07df032: feat(15-01): add install step CSS classes to shared style.css
- 66c890f: feat(15-01): replace getting-started.html stub with full two-path install page

## Self-Check: PASSED
