# Project Research Summary

**Project:** Finance AI Skill — v1.3 GitHub Pages Showcase Site
**Domain:** Static GitHub Pages showcase site for a production Python/MCP developer tool targeting finance professionals
**Researched:** 2026-03-18
**Confidence:** HIGH

## Executive Summary

The v1.3 milestone adds a multi-page static showcase site to an already-shipped Python/FastMCP project. The site does not extend or modify the existing MCP skill — it is a pure marketing and conversion layer whose only job is to get finance professionals from "curious" to "installed." Research confirms the correct approach is plain HTML in a `docs/` folder published via GitHub Pages, with no static site generator and no JavaScript framework. Jekyll and Minimal Mistakes were evaluated but the plain HTML approach is recommended: the 4-page scope does not justify the Ruby toolchain overhead, and the no-build-step path deploys in under 60 seconds with zero build failure risk. If the site grows beyond 8 pages in a future milestone, Jekyll 4.4 + Minimal Mistakes (evaluated at HIGH confidence) is the documented upgrade path.

The primary audience — equity researchers, hedge fund analysts, IB associates, FP&A managers, PE associates, and accountants — is credibility-sensitive but not technically fluent. Research from CFA Institute (2025), FINRA Foundation (2024), and Deloitte (2026) confirms finance professionals penalize AI tools that are opaque, oversell their scope, or do not acknowledge their limitations. The site must lead with outcomes ("finance analysis in plain English — no Python required"), show real chart outputs rather than stock photos or empty promises, and provide explicit disclaimer transparency. These trust signals are differentiators, not boilerplate. The existing `finance_output/charts/` directory contains 60+ real chart PNGs — curating 6-8 of them for the site is a content task, not a technical one.

The dominant risk is messaging, not implementation. A site written from the builder's perspective (MCP servers, FastMCP, stdio transports) will achieve near-zero conversion with the finance professional audience. The second most dangerous risk is deployment mechanics: GitHub Pages project sites serve at a `/repo-name/` URL prefix, and root-absolute asset paths cause every page to load unstyled and every image to 404. Both risks are fully addressable if scaffolding standards and copy conventions are established in Phase 1 before content pages are written.

---

## Key Findings

### Recommended Stack

The site should be built as plain HTML/CSS in a `docs/` folder at the repo root, published via GitHub Pages using "Deploy from branch / /docs folder" in repository Settings. No GitHub Actions workflow is needed for this configuration — GitHub Pages reads the `docs/` folder automatically on every push to main and deploys within 60 seconds. A `docs/.nojekyll` file disables Jekyll processing to prevent conflicts with the Python project's directory structure. All four pages live at the same directory level inside `docs/`, eliminating cross-level relative path complexity.

Chart images are static PNGs from the existing `finance_output/charts/` directory, curated to 6-8 representative examples and web-optimized to under 150KB each before being placed in `docs/assets/images/`. No JavaScript charting library is warranted. If the site grows to 8+ pages or nav complexity increases, Eleventy (JavaScript-native) or Jekyll 4.4 + Minimal Mistakes (Ruby) are the evaluated upgrade paths — but neither is warranted at 4 pages.

**Core technologies:**
- Plain HTML/CSS in `docs/`: all 4 pages — no build step, immediate GitHub Pages compatibility, lowest operational risk
- `docs/.nojekyll`: empty file — disables Jekyll and prevents Python project structure from causing silent build failures
- GitHub Pages (branch source, `/docs` folder): deployment — zero CI overhead, automatic on push, live in under 60 seconds
- Curated and web-optimized PNGs from `finance_output/charts/`: visual proof — real outputs already generated, not mock-ups
- Jekyll 4.4.1 + Minimal Mistakes 4.28.0 (evaluated, deferred): upgrade path if site grows beyond 8 pages; requires Ruby 3.3.4 + GitHub Actions workflow

### Expected Features

The site has a clear 4-page structure: Home (landing), Features (11 MCP tools), Walkthroughs (6 role scenarios), Getting Started (two install paths). Chart asset curation is the prerequisite dependency — the hero, features, and walkthroughs sections all require a curated set of web-optimized images from the existing `finance_output/charts/` directory. This is a content task and should be the first deliverable in Phase 1.

**Must have (table stakes — P1):**
- Hero: clear value proposition ("no Python required") + primary CTA above the fold — finance professionals decide in 5 seconds
- Real chart outputs as visual proof — stock photos or placeholder images destroy credibility with this audience
- Persistent navigation across all 4 pages — multi-page site is non-functional without it
- Walkthroughs page: 6 role-based scenario cards (situation sentence + example prompt + chart image) — roles, not feature lists
- Features page: 11 MCP tools with plain-language outcome descriptions and real command examples
- Getting Started: two distinct paths (Claude Code via stdio; claude.ai via HTTP + ngrok) with copy-pasteable commands
- Mobile-responsive layout — 40%+ of professional browsing is mobile; base CSS handles this
- SEO meta tags (title, description, Open Graph) on every page — social shares on LinkedIn are a primary finance professional discovery channel

**Should have (competitive — P2):**
- Persona contrast demonstration (analyst vs PM framing on same data) on Features page — unique differentiator
- Disclaimer transparency callout — builds trust with compliance-aware finance professionals
- Curriculum attribution ("built on pyfi.com curriculum") — academic legitimacy reduces "black box" concern
- Social card image (1200x630 OG image) — blank LinkedIn previews lose finance professional clicks

**Defer (v2+):**
- Interactive embedded demo — requires backend; GitHub Pages is static; canned demos destroy credibility
- Blog/changelog section — ongoing content maintenance burden with no immediate conversion value
- Dark mode toggle — not a pain point for finance professional primary audience; adds JS complexity
- Full API documentation on site — belongs in the GitHub README; overwhelming for this audience

### Architecture Approach

The site is completely isolated from the Python/MCP codebase. The `docs/` folder contains all site files and communicates with the Python project only through a one-time manual image curation step. No runtime coupling exists: the site does not call the MCP server, does not run Python, and has no Python dependencies. GitHub Pages reads the `docs/` folder on every push to main and serves it as a static CDN with no build step required.

**Major components:**
1. `docs/` folder — GitHub Pages root; all HTML, CSS, JS, and curated images; fully isolated from Python source
2. `docs/assets/images/` — 6-8 curated, renamed, web-optimized PNGs copied from `finance_output/charts/`; stable descriptive filenames (e.g., `compare-tech-stocks.png`, not date-stamped originals)
3. `docs/assets/css/style.css` — shared styles; referenced via relative path from all 4 pages at the same directory level
4. `docs/.nojekyll` — empty file that disables Jekyll processing; prevents Python project files from causing build failures
5. GitHub Pages Settings (configure once) — set to branch `main`, folder `/docs`; no workflow YAML needed

### Critical Pitfalls

1. **Root-absolute asset paths cause 404s after deployment** — GitHub Pages project sites serve at `https://username.github.io/repo-name/`; paths starting with `/` resolve to the wrong URL. Use strictly relative paths everywhere. Establish this convention in Phase 1 before writing any content pages; fixing it retroactively requires touching every `href` and `src` across all files.

2. **Jekyll processes Python project structure without `.nojekyll`** — GitHub Pages runs Jekyll by default on every repository. Without `docs/.nojekyll`, Jekyll may fail on Python source files or silently suppress files starting with `_`. Add `.nojekyll` as the very first committed file; do not skip this step.

3. **Developer-centric messaging drives finance professional bounce** — using words like "MCP server," "FastMCP," "stdio transport," or "scikit-learn pipeline" in the hero or features sections will cause near-100% bounce from the target audience. Every feature description must lead with the finance outcome, not the technical mechanism. Validate by reading copy aloud to a non-technical person.

4. **Unoptimized matplotlib PNGs tank mobile performance** — `finance_output/charts/` files are generated for terminal/notebook use at 800KB–2MB each. Export web-optimized versions at 800px wide, ~96 DPI, targeting under 150KB per image. Verify Lighthouse Performance score above 80 before marking any content phase complete.

5. **Walkthrough page written as a feature list, not scenarios** — listing role names and tool names ("Equity Research: returns, volatility") tells the finance professional nothing they care about. Each role entry must have: (1) a situation sentence, (2) a verbatim example prompt, (3) a chart output. Feature lists do not convert.

6. **`og:image` meta tag must be an absolute URL** — Open Graph image paths must be absolute (`https://username.github.io/repo-name/assets/images/social-card.png`), not relative. Relative OG image paths produce blank social share previews on LinkedIn and Slack.

---

## Implications for Roadmap

Based on combined research, the site is best built in three phases. The architecture research explicitly recommends this order. Pitfall research confirms that Phases 14 and 15 cannot be done correctly without Phase 13 establishing path conventions, the `.nojekyll` file, and the curated image set as a complete prerequisite foundation.

### Phase 13: Site Scaffolding and Deployment Setup

**Rationale:** Every subsequent content page depends on path conventions, `.nojekyll` configuration, and GitHub Pages settings being correct before the first character of HTML content is written. The most expensive pitfalls (broken asset paths, Jekyll conflicts, inconsistent navigation) are nearly impossible to fix retroactively without touching every file. Verify deployment on a live placeholder page before proceeding to content.

**Delivers:** Working GitHub Pages deployment of a placeholder `index.html`; confirmed zero 404s in browser DevTools on the live URL; complete `docs/` folder structure (`assets/css/`, `assets/js/`, `assets/images/`); `docs/.nojekyll` in place; 6-8 curated chart PNGs copied and renamed to stable descriptive filenames in `docs/assets/images/`; shared `style.css` stub; HTML `<head>` template with viewport meta tag and SEO meta tag placeholders ready to populate per page.

**Addresses:** Navigation (table stakes — template established here), mobile viewport (table stakes — in shared head template), chart asset curation (prerequisite for all content pages), SEO meta tag structure (P2 — add structure now, fill per-page copy later).

**Avoids:** Root-absolute path 404s (Pitfall 1 — relative path convention set before any content), Jekyll conflicts (Pitfall 2 — `.nojekyll` first commit), missing viewport meta tag (UX pitfall — in shared template), SEO meta tags missing at launch (Pitfall 8 — structure established in template).

**Research flag:** Standard patterns. GitHub Docs source is authoritative, current, and unambiguous. No additional research needed.

---

### Phase 14: Content Pages (Landing, Features, Walkthroughs)

**Rationale:** These three pages are the conversion engine of the site and share the scaffolding established in Phase 13. Landing page is built first because it determines the visual design system (color palette, card components, typography scale, CTA button style) that Features and Walkthroughs inherit. Once the design system is established, Features and Walkthroughs can be written in parallel or sequentially without design drift.

**Delivers:** `index.html` — hero with outcome-led value proposition, primary CTA, 1-2 real chart visuals, plain-English feature overview, attribution callout; `features.html` — 11 MCP tools grouped by category (market analysis / ML workflows) with plain-language outcome descriptions, real command examples inline, and a persona contrast callout; `walkthroughs.html` — 6 role cards each with a situation sentence, a verbatim example prompt, and a representative chart image.

**Addresses:** Hero value proposition (P1), real chart outputs as visual proof (P1), plain-language command examples (P1), role-based walkthrough sections (P1 differentiator), persona contrast demonstration (P2), disclaimer transparency callout (P2), curriculum attribution (P2).

**Avoids:** Developer-centric messaging (Pitfall 3 — outcome-led copy from landing page through features), walkthrough page as feature list (Pitfall 9 — scenario format with situation sentence + prompt + chart), unoptimized chart images (Pitfall 4 — Lighthouse verification gate), hero leading with product name not outcome (UX pitfall).

**Research flag:** The finance professional messaging research (FINRA, CFA, Deloitte sources in FEATURES.md) should be referenced when writing hero and feature copy. No additional technical research needed. The quality gate for this phase is copy validation, not implementation complexity.

---

### Phase 15: Getting Started Page and Final Polish

**Rationale:** Getting Started is the terminal conversion page — every CTA across all other pages points here. It should be written last because its content (exact install commands, final repo URL) is most accurate after the rest of the site is complete and the developer has verified both install paths work correctly. Final polish — consistent navigation verification, mobile testing on real 375px viewport, social card image creation, cross-page link audit — is done last to catch any drift that emerged during Phase 14 authoring.

**Delivers:** `getting-started.html` — two distinct install paths (Claude Code stdio; claude.ai HTTP + ngrok), copy-pasteable commands with plain-English step descriptions, troubleshooting callout for yfinance rate limits and ngrok auth; social card image (1200x630 PNG) for Open Graph `og:image` across all pages; verified navigation from every page to every other page; Lighthouse Performance score above 80 on all pages; mobile navigation confirmed on 375px viewport.

**Addresses:** Dual install path (P1), Getting Started page (P1), social card image for LinkedIn (P2), mobile navigation verification (table stakes), final SEO validation.

**Avoids:** Getting Started written for developers only (Pitfall 6 — two explicit paths, plain-English step descriptions, troubleshooting pre-empted), mobile navigation breakage (Pitfall 5 — verified on 375px from every page), blank LinkedIn social share (Pitfall 8 — absolute URL `og:image` created and validated via opengraph.xyz before launch).

**Research flag:** No additional research needed. Both install paths are fully documented from the existing project. The quality gate is a non-technical person readability test: if a senior portfolio manager who has never opened a terminal cannot follow every step without asking a question, the copy needs revision.

---

### Phase Ordering Rationale

- **Phase 13 before all content:** Path conventions and GitHub Pages verification must be in place before any page references CSS, images, or links to other pages. Fixing path conventions after 4 pages exist requires touching every `href` and `src`.
- **Landing page before Features and Walkthroughs in Phase 14:** The visual design system originates in `index.html`. Features and Walkthroughs should inherit from it, not define their own patterns in parallel and then require a reconciliation pass.
- **Image curation in Phase 13, not Phase 14:** Curated chart assets are a dependency of every content page (hero image, features illustrations, walkthrough cards). Deferring curation to Phase 14 would block content authoring.
- **Getting Started last:** Its content (install commands, troubleshooting notes, final repo URL) is most accurate after the rest of the site is built. It is also the highest-risk page for developer-centric writing — writing it last allows applying messaging lessons from Phase 14.

### Research Flags

Phases likely needing deeper research during planning:
- **None identified.** All three phases use fully documented patterns (GitHub Pages official docs, plain HTML, established finance professional trust signals from named primary sources). The technical implementation is straightforward; the quality risk is in copy and image optimization — both of which have clear, verifiable quality gates.

Phases with standard patterns (skip research-phase):
- **Phase 13 (scaffolding):** GitHub Pages `docs/` folder publishing is official, unambiguous, and verified at pages.github.com/versions on 2026-03-18.
- **Phase 14 (content pages):** HTML authoring with web-optimized images and plain-language copy; no novel technical patterns; Lighthouse is the objective quality gate.
- **Phase 15 (Getting Started + polish):** Two-path install documentation is a known pattern; mobile verification and OG tag validation have established tooling (DevTools, opengraph.xyz).

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All stack decisions sourced from official GitHub Docs and Jekyll release notes; version compatibility verified against pages.github.com/versions on 2026-03-18; plain HTML decision is unambiguous for 4-page scope |
| Features | MEDIUM-HIGH | Table stakes and page structure from developer tool homepage research (HIGH); finance professional trust signal recommendations from CFA Institute, FINRA Foundation, Deloitte (HIGH); conversion rate implications for specific copy choices (MEDIUM — no A/B test data) |
| Architecture | HIGH | Sourced entirely from GitHub official documentation; `docs/` folder pattern, `.nojekyll` behavior, relative path requirement, and image serving constraints are all confirmed from authoritative sources |
| Pitfalls | HIGH (technical) / MEDIUM (messaging) | Asset path and Jekyll pitfalls sourced from GitHub Docs and confirmed real-world issue reports (HIGH); finance professional messaging pitfalls synthesized from industry trust research — general patterns are solid, but specific conversion copy is unvalidated until real users interact with the site |

**Overall confidence:** HIGH

### Gaps to Address

- **Finance professional conversion rates for specific copy choices:** No direct A/B test data exists for this specific tool and audience combination. The non-technical person readability test is the practical validation gate for Phase 14 and 15 copy. Plan for a copy iteration after the site is shared with real finance professionals.
- **claude.ai HTTP transport install friction:** The ngrok-based install path is documented and known to work, but actual friction for a non-developer finance professional is unvalidated. The Getting Started page should pre-empt the two known failure points (Python not installed, ngrok auth), but expect to discover additional friction points when real users attempt the install.
- **Best social card image for LinkedIn shares:** The 1200x630 OG image should feature the most visually compelling chart output. The multi-stock comparison chart (`compare_AAPL_GOOGL_MSFT_NVDA_2025-03-18.png`) is the recommended starting point, but validate that it reads clearly at social card thumbnail size before finalizing.

---

## Sources

### Primary (HIGH confidence)
- GitHub Docs — Configuring a publishing source for GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Docs — Using custom workflows with GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- pages.github.com/versions — Native Jekyll 3.10.0, Ruby 3.3.4, plugin versions confirmed on 2026-03-18
- Jekyll 4.4.0 Release Notes: https://jekyllrb.com/news/2025/01/27/jekyll-4-4-0-released/
- mmistakes/minimal-mistakes GitHub — v4.28.0, remote theme compatibility: https://github.com/mmistakes/minimal-mistakes
- CFA Institute 2025 — "Explainable AI in Finance": https://rpc.cfainstitute.org/research/reports/2025/explainable-ai-in-finance
- FINRA Foundation 2024 — AI vs Financial Professional trust study: https://www.finra.org/media-center/newsreleases/2024
- Deloitte 2026 — "Trust Emerges as Main Barrier to Agentic AI Adoption in Finance": https://tipalti.com/press/ai-in-finance-trust-gap-report/

### Secondary (MEDIUM confidence)
- dasroot.net — Hugo vs Jekyll vs 11ty Comparison 2026: https://dasroot.net/posts/2026/03/hugo-vs-jekyll-vs-11ty-static-site-generator-comparison-2026/
- Maxim Orlov — "Deploying to Github Pages? Don't Forget to Fix Your Links": https://maximorlov.com/deploying-to-github-pages-dont-forget-to-fix-your-links/
- everydeveloper.com — "How 30 Dev Tool Homepages Put Developers First": https://everydeveloper.com/developer-tool-homepages/
- Landingi — "Finance Landing Pages: Definition, How to Create & 8 Examples": https://landingi.com/blog/landing-pages-in-finance/
- Python Graph Gallery (gallery-first page pattern reference): https://github.com/holtzy/The-Python-Graph-Gallery
- Growth Fueling — "Landing Page Mistakes That Kill Conversions in 2025": https://growthfueling.com/landing-page-mistakes-that-kill-conversions-in-2025/

### Tertiary (LOW confidence)
- SaaS hero copy patterns: https://landingrabbit.com/blog/saas-website-hero-text — general SaaS patterns applied to finance professional context; needs validation with real users

---
*Research completed: 2026-03-18*
*Ready for roadmap: yes*
