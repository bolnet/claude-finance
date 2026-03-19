# Requirements: Finance AI Skill — v1.3 GitHub Pages Site

**Defined:** 2026-03-18
**Core Value:** Finance professionals get professional-grade analysis by describing what they want — the skill writes, runs, and interprets the code for them.

## v1.3 Requirements

Requirements for the GitHub Pages showcase site. Each maps to roadmap phases.

### Infrastructure

- [x] **INFRA-01**: Site deploys from `docs/` folder on main branch with `.nojekyll` file
- [x] **INFRA-02**: Shared HTML template (head, nav bar, footer) used by all pages
- [x] **INFRA-03**: All pages are mobile responsive with proper viewport meta
- [x] **INFRA-04**: Social card (OG meta image) displays when site is shared on LinkedIn/Twitter

### Landing Page

- [x] **LAND-01**: Hero section with finance-outcome headline and CTA targeting finance professionals
- [x] **LAND-02**: Real chart output visuals embedded as proof of capability
- [x] **LAND-03**: Role-based entry points linking to specific walkthrough sections ("I'm a hedge fund analyst")
- [x] **LAND-04**: Stats bar displaying key credibility numbers (11 tools, 6 walkthroughs, etc.)

### Features Page

- [x] **FEAT-01**: 11 MCP tools displayed organized by category (market analysis vs ML workflows)
- [x] **FEAT-02**: Visual examples (chart screenshots) for each tool category

### Walkthroughs Page

- [x] **WALK-01**: 6 role cards with scenario descriptions and tool usage per role
- [x] **WALK-02**: Role-specific chart examples embedded per walkthrough card

### Getting Started Page

- [x] **START-01**: Claude Code installation path with copy-paste commands
- [x] **START-02**: claude.ai installation path with step-by-step instructions

### Visual Assets

- [x] **VIS-01**: 6-8 best charts curated from `finance_output/charts/`
- [x] **VIS-02**: All site images web-optimized (800px wide, <150KB each)
- [x] **VIS-03**: Favicon for browser tab

## Future Requirements

### Site Enhancements

- **SITE-01**: Dark mode toggle
- **SITE-02**: Animated hero section with chart transitions
- **SITE-03**: Blog/changelog page for release notes
- **SITE-04**: Custom domain (CNAME) configuration

## Out of Scope

| Feature | Reason |
|---------|--------|
| Live interactive demo | GitHub Pages is static; cannot run MCP server |
| Testimonials section | No real user testimonials yet; placeholder quotes destroy credibility with finance audience |
| Competitor comparison table | Invites scrutiny, looks defensive |
| Analytics/tracking | Not needed for v1.3; revisit if custom domain added |
| Jekyll/SSG build pipeline | Plain HTML is simpler and avoids version conflicts |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 13 | Complete |
| INFRA-02 | Phase 13 | Complete |
| INFRA-03 | Phase 13 | Complete |
| INFRA-04 | Phase 15 | Complete |
| LAND-01 | Phase 14 | Complete |
| LAND-02 | Phase 14 | Complete |
| LAND-03 | Phase 14 | Complete |
| LAND-04 | Phase 14 | Complete |
| FEAT-01 | Phase 14 | Complete |
| FEAT-02 | Phase 14 | Complete |
| WALK-01 | Phase 14 | Complete |
| WALK-02 | Phase 14 | Complete |
| START-01 | Phase 15 | Complete |
| START-02 | Phase 15 | Complete |
| VIS-01 | Phase 13 | Complete |
| VIS-02 | Phase 13 | Complete |
| VIS-03 | Phase 13 | Complete |

**Coverage:**
- v1.3 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 — traceability mapped after roadmap creation*
