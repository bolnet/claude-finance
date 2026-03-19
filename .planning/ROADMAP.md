# Roadmap: Finance AI Skill for Claude Code

## Milestones

- ✅ **v1.0 Finance AI Skill MVP** — Phases 1–4 (shipped 2026-03-18)
- ✅ **v1.1 Interactive Demo** — Phases 5–8 (shipped 2026-03-18)
- ✅ **v1.2 Role Walkthroughs** — Phases 9–12 (shipped 2026-03-18)
- 🔄 **v1.3 GitHub Pages Site** — Phases 13–15 (active)

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

### v1.3 GitHub Pages Site (Active)

**Milestone Goal:** Build a beautiful, multi-page GitHub Pages site that showcases the Finance AI Skill to finance professionals — landing page with a strong hook, features, role walkthroughs, demo visuals, and getting started guide.

- [x] **Phase 13: Site Scaffolding and Visual Assets** — docs/ folder structure, .nojekyll, shared HTML/CSS template, mobile viewport, 6-8 curated chart PNGs web-optimized and staged in docs/assets/images/ (completed 2026-03-18)
- [x] **Phase 14: Content Pages** — Landing page (hero, chart visuals, role entry points, stats bar), Features page (11 MCP tools by category), Walkthroughs page (6 role cards with scenario + chart) (completed 2026-03-19)
- [x] **Phase 15: Getting Started and Polish** — Getting Started page (two install paths), social card OG image, cross-page navigation audit, Lighthouse verification (completed 2026-03-19)

## Phase Details

### Phase 13: Site Scaffolding and Visual Assets
**Goal**: A working GitHub Pages deployment exists with the correct folder structure, path conventions, and curated chart assets — so every content page can be authored without revisiting infrastructure decisions
**Depends on**: Nothing (first v1.3 phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03, VIS-01, VIS-02, VIS-03
**Success Criteria** (what must be TRUE):
  1. Visiting the live GitHub Pages URL in a browser loads a styled placeholder index.html with zero 404 errors in DevTools
  2. All asset paths in HTML and CSS are relative (no leading `/`), confirmed by inspecting the deployed page
  3. A finance professional on a phone (375px viewport) can read the placeholder page without horizontal scrolling
  4. 6-8 chart PNGs are present in `docs/assets/images/` with stable descriptive filenames (e.g., `compare-tech-stocks.png`), each under 150KB
  5. All pages share a single HTML head/nav/footer template — no copy-paste duplication of boilerplate across files
**Plans:** 2/2 plans complete

Plans:
- [x] 13-01-PLAN.md — Create docs/ folder structure, HTML template, CSS, JS, curate 8 chart images, favicon
- [x] 13-02-PLAN.md — Enable GitHub Pages deployment, verify live URL, visual verification

### Phase 14: Content Pages
**Goal**: Finance professionals can visit the landing page, understand the skill's value in plain English, see real chart outputs as proof, explore all 11 tools by category, and read the 6 role walkthroughs with scenario context
**Depends on**: Phase 13
**Requirements**: LAND-01, LAND-02, LAND-03, LAND-04, FEAT-01, FEAT-02, WALK-01, WALK-02
**Success Criteria** (what must be TRUE):
  1. Landing page hero section states the value proposition in outcome-led language ("finance analysis in plain English — no Python required") above the fold on desktop and mobile
  2. Landing page shows at least one real chart output image as visual proof of capability
  3. Landing page includes role-based entry points (e.g., "I'm a hedge fund analyst") that link to the relevant walkthrough card
  4. Features page groups all 11 MCP tools by category (market analysis vs ML workflows) with plain-language outcome descriptions — no developer jargon in descriptions
  5. Walkthroughs page presents all 6 role cards, each containing a situation sentence, a verbatim example prompt, and a representative chart image
**Plans:** 2/2 plans complete

Plans:
- [x] 14-01-PLAN.md — Landing page content + all Phase 14 CSS component classes (completed 2026-03-19)
- [x] 14-02-PLAN.md — Features page (11 tools by category) + Walkthroughs page (6 role cards)

### Phase 15: Getting Started and Polish
**Goal**: Finance professionals can follow a complete, step-by-step installation path for either Claude Code or claude.ai, every page links correctly to every other page, and the site renders correctly on mobile and produces a rich social card when shared on LinkedIn
**Depends on**: Phase 14
**Requirements**: START-01, START-02, INFRA-04
**Success Criteria** (what must be TRUE):
  1. Getting Started page presents two clearly separated install paths (Claude Code via stdio; claude.ai via HTTP + ngrok), each with copy-pasteable commands and plain-English step descriptions
  2. Every navigation link on every page resolves to the correct destination — no broken links on any of the 4 pages
  3. Sharing the site URL on LinkedIn (verified via opengraph.xyz) produces a rich preview with title, description, and chart image — not a blank card
  4. Lighthouse Performance score is 80 or above on all 4 pages
**Plans:** 2/2 plans complete

Plans:
- [ ] 15-01-PLAN.md — Getting Started page content (two install paths) + install step CSS classes
- [ ] 15-02-PLAN.md — Social card OG image, OG meta tags on all pages, cross-page navigation audit

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
| 15. Getting Started and Polish | 2/2 | Complete   | 2026-03-19 | - |

---
*Last updated: 2026-03-18 — Phase 15 planned (2 plans)*
