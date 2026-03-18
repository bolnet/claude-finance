# Architecture Research

**Domain:** GitHub Pages static showcase site integrated into existing Python MCP project
**Researched:** 2026-03-18
**Confidence:** HIGH (sourced from GitHub official docs + verified against current GitHub Pages configuration options)

---

## Note on Scope

This file supersedes the v1.0 ARCHITECTURE.md (MCP skill architecture) for the v1.3 GitHub Pages milestone. The Python/MCP architecture is stable and fully shipped. This document covers only the GitHub Pages site layer and how it integrates with the existing repo.

---

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                     GitHub Repository (main branch)              │
│                                                                  │
│  ┌────────────────────┐      ┌────────────────────────────────┐  │
│  │  Existing Python   │      │   New: GitHub Pages Site       │  │
│  │  MCP Project       │      │   docs/                        │  │
│  │                    │      │                                │  │
│  │  src/finance_mcp/  │      │   docs/index.html              │  │
│  │  finance_output/   │      │   docs/features.html           │  │
│  │    charts/*.png ───┼──────┼──► docs/assets/images/*.png   │  │
│  │    models/*.joblib │      │   docs/walkthroughs.html       │  │
│  │  tests/            │      │   docs/getting-started.html    │  │
│  │  demo/             │      │   docs/assets/css/style.css    │  │
│  │  scripts/          │      │   docs/assets/js/main.js       │  │
│  └────────────────────┘      └──────────────┬─────────────────┘  │
│                                             │                    │
└─────────────────────────────────────────────┼────────────────────┘
                                              │ push to main
                                              ▼
                              ┌───────────────────────────────┐
                              │   GitHub Pages CDN            │
                              │   https://[owner].github.io/  │
                              │   machine_learning_skill/     │
                              └───────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| `docs/` folder | GitHub Pages root — all site files live here | Static HTML/CSS/JS, no build step required |
| `docs/assets/images/` | Curated chart PNGs for the site | Copies of select PNGs from `finance_output/charts/` |
| `docs/assets/css/style.css` | Site-wide styling | Hand-authored CSS; no framework required at this scale |
| `docs/assets/js/main.js` | Optional interactivity | Progressive enhancement only; site works without JS |
| `finance_output/charts/` | Source of truth for generated PNGs | Existing directory; charts committed to repo or copied at build time |
| GitHub Pages (Settings) | Publishing source configuration | Point to `main` branch, `/docs` folder |

---

## Recommended Project Structure

```
machine_learning_skill/
├── src/finance_mcp/          # existing — untouched
├── finance_output/
│   ├── charts/               # existing — source PNGs live here
│   └── models/               # existing
├── tests/                    # existing — untouched
├── demo/                     # existing — untouched
├── docs/                     # NEW — GitHub Pages root
│   ├── index.html            # Landing page
│   ├── features.html         # 11 MCP tools showcase
│   ├── walkthroughs.html     # 6 role walkthroughs
│   ├── getting-started.html  # Installation guide
│   └── assets/
│       ├── css/
│       │   └── style.css     # Site-wide styles
│       ├── js/
│       │   └── main.js       # Optional interactivity
│       └── images/           # Curated chart PNGs (copied from finance_output)
│           ├── correlation_AAPL_GOOGL_MSFT_2025-03-18.png
│           ├── compare_AAPL_GOOGL_MSFT_NVDA_2025-03-18.png
│           ├── confusion_matrix.png
│           ├── feature_importance.png
│           ├── eda_credit_score.png
│           └── aapl_volatility_2025-03-18.png
├── pyproject.toml            # existing — untouched
└── requirements.txt          # existing — untouched
```

### Structure Rationale

- **`docs/` at repo root:** GitHub Pages natively supports `main` branch + `/docs` folder as a publishing source. No extra branch, no CI workflow required for a static HTML site. This is the lowest-friction option for a no-build-step site.
- **`docs/assets/images/` as a copy, not a symlink:** GitHub Pages serves files statically from the `docs/` tree. Symlinks to `finance_output/charts/` do not resolve. Selected PNGs must be physically present in `docs/assets/images/`.
- **Flat HTML page structure:** Four pages (index, features, walkthroughs, getting-started) do not warrant a site generator. Plain HTML avoids Jekyll dependency, build failures, and Gemfile version conflicts.
- **No Jekyll:** Adding an empty `.nojekyll` file to `docs/` disables Jekyll processing entirely. This eliminates the risk of Jekyll ignoring files that start with `_` and removes all Ruby/Gemfile dependencies.

---

## Architectural Patterns

### Pattern 1: docs/ Folder Publishing (No Build Step)

**What:** Configure GitHub Pages to publish from `main` branch, `/docs` folder. Commit HTML/CSS/JS/images directly. Every push to `main` triggers a publish.

**When to use:** When the site is static HTML with no preprocessing needed. Correct for this project — the site is a showcase, not an application.

**Trade-offs:**
- Pro: Zero CI overhead, zero build failures, works immediately after settings change
- Pro: All site files live on the same branch as the Python source — one PR covers both
- Con: Chart PNGs in `docs/assets/images/` are manually curated copies; they will drift from `finance_output/charts/` over time if charts are regenerated
- Con: Images committed to `docs/` add repo size; acceptable for a small curated set (~10 PNGs)

**How to enable:**
```
GitHub repo → Settings → Pages
  Source: Deploy from a branch
  Branch: main
  Folder: /docs
```

### Pattern 2: Curated Image Copy (Not Full Directory Mirror)

**What:** Manually select 6-10 representative PNGs from `finance_output/charts/` and copy them to `docs/assets/images/`. Do not mirror the full charts directory.

**When to use:** Always for a showcase site. `finance_output/charts/` contains 60+ files with date-stamped names. The site needs 6-8 stable, well-named representative images.

**Trade-offs:**
- Pro: Site images have stable, human-readable filenames (not `aapl_volatility_2025-03-18.png`)
- Pro: Chart directory churn does not affect the site
- Con: Requires a one-time manual curation step
- Con: If charts are regenerated with better data, images need manual re-copy

**Recommended curated set:**

| Site use | Source file | Destination name |
|----------|-------------|-----------------|
| Hero / market analysis demo | `compare_AAPL_GOOGL_MSFT_NVDA_2025-03-18.png` | `compare-tech-stocks.png` |
| Correlation heatmap | `correlation_AAPL_GOOGL_MSFT_2025-03-18.png` | `correlation-heatmap.png` |
| Volatility chart | `aapl_volatility_2025-03-18.png` | `volatility-analysis.png` |
| ML confusion matrix | `confusion_matrix.png` | `confusion-matrix.png` |
| Feature importance | `feature_importance.png` | `feature-importance.png` |
| EDA chart | `eda_credit_score.png` | `eda-sample.png` |

### Pattern 3: Relative Paths Throughout

**What:** All links between pages and all asset references use relative paths, not absolute paths or root-relative paths.

**When to use:** Always. GitHub Pages serves the site at `https://[owner].github.io/machine_learning_skill/` — the repo name is in the URL path. Root-relative paths (`/assets/css/style.css`) resolve to `https://[owner].github.io/assets/css/style.css` which is wrong.

**Trade-offs:**
- Pro: Works correctly regardless of repo name or custom domain
- Con: Slightly more tedious — `../assets/css/style.css` from a subpage vs `assets/css/style.css` from index

**Correct pattern:**
```html
<!-- In docs/index.html -->
<link rel="stylesheet" href="assets/css/style.css">
<img src="assets/images/compare-tech-stocks.png" alt="Tech stock comparison">
<a href="features.html">Features</a>

<!-- In docs/features.html -->
<link rel="stylesheet" href="assets/css/style.css">
<img src="assets/images/confusion-matrix.png" alt="ML model accuracy">
<a href="index.html">Home</a>
```

---

## Data Flow

### Chart Images: Source to Site

```
Python MCP tool runs
    |
    v
finance_output/charts/[ticker]_[type]_[date].png   (auto-generated, date-stamped)
    |
    | (one-time manual curation — rename to stable names)
    v
docs/assets/images/[stable-name].png               (committed to repo)
    |
    | (push to main branch)
    v
GitHub Pages CDN serves image at:
https://[owner].github.io/machine_learning_skill/assets/images/[stable-name].png
```

### Page Navigation Flow

```
User visits: https://[owner].github.io/machine_learning_skill/
    |
    v
docs/index.html  (landing page — value prop, hook, CTAs)
    |
    |---> features.html      (11 MCP tools, chart visuals)
    |---> walkthroughs.html  (6 role scenarios)
    |---> getting-started.html (Claude Code + claude.ai install)
```

### Deployment Flow

```
Developer edits docs/*.html or docs/assets/*
    |
    v
git add docs/ && git commit && git push origin main
    |
    v
GitHub Pages build triggered automatically (branch source mode)
    |
    v (typically < 60 seconds)
Site live at https://[owner].github.io/machine_learning_skill/
```

---

## Integration Points

### New vs Modified Components

| Component | Status | Notes |
|-----------|--------|-------|
| `docs/` directory | NEW — create from scratch | GitHub Pages root |
| `docs/index.html` | NEW | Landing page |
| `docs/features.html` | NEW | Tools showcase |
| `docs/walkthroughs.html` | NEW | Role scenarios |
| `docs/getting-started.html` | NEW | Install guide |
| `docs/assets/css/style.css` | NEW | Shared styles |
| `docs/assets/js/main.js` | NEW (optional) | Minor interactivity |
| `docs/assets/images/*.png` | NEW — copied from finance_output/charts/ | 6-8 curated PNGs, renamed |
| `docs/.nojekyll` | NEW — empty file | Disables Jekyll processing |
| `finance_output/charts/` | UNCHANGED | Source PNGs remain here |
| `src/finance_mcp/` | UNCHANGED | Python MCP server untouched |
| GitHub repo Settings > Pages | CONFIGURE once | Point to main branch, /docs folder |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `finance_output/charts/` → `docs/assets/images/` | Manual file copy at site creation | One-time; re-copy only if charts are regenerated with better data |
| `docs/*.html` → `docs/assets/` | Relative paths in HTML `src`/`href` attributes | Must be relative — never root-relative |
| Python codebase → GitHub Pages site | Zero runtime coupling | Site is a static brochure; it does not call the MCP server |
| GitHub Pages → GitHub repo | GitHub reads `docs/` folder on every push to main | No workflow YAML needed for this configuration |

---

## Anti-Patterns

### Anti-Pattern 1: Using Root-Relative Asset Paths

**What people do:** Write `<link href="/assets/css/style.css">` in HTML files.

**Why it's wrong:** GitHub Pages serves project sites at `https://[owner].github.io/machine_learning_skill/`. A root-relative path resolves to `https://[owner].github.io/assets/css/style.css` — a 404. This is the most common GitHub Pages breakage.

**Do this instead:** Use relative paths: `href="assets/css/style.css"` from `docs/index.html`, `href="../assets/css/style.css"` from any file in a subdirectory.

### Anti-Pattern 2: Referencing finance_output/charts/ Directly in HTML

**What people do:** Write `<img src="../../finance_output/charts/aapl_volatility_2025-03-18.png">` to avoid copying files.

**Why it's wrong:** GitHub Pages only serves files inside the configured publishing folder (`docs/`). Files outside `docs/` are not served. The relative path points to a non-served location — the image will 404 in production even if it appears to work locally.

**Do this instead:** Copy selected PNGs into `docs/assets/images/` and reference them from there.

### Anti-Pattern 3: Enabling Jekyll Without a Build Configuration

**What people do:** Leave no `.nojekyll` file, allowing GitHub Pages to run Jekyll automatically.

**Why it's wrong:** Jekyll silently ignores files and directories whose names begin with `_`. If any CSS, JS, or data file uses that naming convention, it disappears in production with no error. Jekyll also introduces Gemfile version conflicts that fail builds unpredictably.

**Do this instead:** Add an empty `docs/.nojekyll` file. This tells GitHub Pages to serve the files exactly as they are, with no preprocessing.

### Anti-Pattern 4: Committing All 60+ Charts to docs/assets/images/

**What people do:** Mirror the full `finance_output/charts/` directory into `docs/assets/images/` to avoid deciding which charts to use.

**Why it's wrong:** The chart directory contains 60+ date-stamped files totalling significant repo size. Site visitors never benefit from the full set — a showcase needs 6-8 best examples. The date-stamped filenames are also meaningless to visitors.

**Do this instead:** Curate 6-8 representative charts, rename them to stable descriptive names, and commit only those.

### Anti-Pattern 5: gh-pages Branch for a No-Build-Step Site

**What people do:** Create a separate `gh-pages` branch to keep source and site separate.

**Why it's wrong:** `gh-pages` branches are designed for CI-built sites (Hugo, Gatsby, etc.) where the source and the built output are genuinely different. For a plain HTML site, a separate branch doubles the maintenance burden — every change requires both a main branch edit and a gh-pages push. There is no build output to isolate.

**Do this instead:** Use the `docs/` folder on `main`. Source and site live together, one PR covers both, no branch gymnastics needed.

---

## Build Order Implications

The GitHub Pages site has no runtime dependency on the Python MCP server. This means all site phases can proceed independently of further Python development.

```
Phase 13 (recommended first): Site scaffolding
  ├── Create docs/ folder structure
  ├── Add docs/.nojekyll
  ├── Copy and rename curated PNGs to docs/assets/images/
  ├── Configure GitHub Pages in repo Settings (one-time)
  └── Publish placeholder index.html to verify path setup

Phase 14: Content pages (can be done in any order)
  ├── index.html — landing page (do first; sets visual tone)
  ├── features.html — 11 MCP tools with chart images
  ├── walkthroughs.html — 6 role scenarios
  └── getting-started.html — install instructions

Phase 15: Polish
  ├── Consistent navigation across all pages
  ├── Mobile-responsive CSS
  └── Final review of all relative paths
```

**Why this order:**
- Configure GitHub Pages and verify the `/docs` path resolves before writing content — catches path issues early
- Landing page first because it determines the visual design system (colors, typography, component patterns) that all other pages follow
- Content pages are parallel-safe once the CSS and nav pattern are established from index.html
- Getting-started page last because it requires knowing the final repo URL and any install quirks discovered during site development

---

## Scaling Considerations

GitHub Pages is a CDN-hosted static site. Scale is not a concern. The relevant "scaling" for this project is page count:

| Page count | Architecture adjustment |
|------------|------------------------|
| 4 pages (current plan) | Plain HTML — no abstraction needed |
| 8-12 pages | Extract shared nav/footer to a common include pattern; consider a minimal static site generator like Eleventy |
| 12+ pages | Adopt a lightweight SSG (Eleventy, Hugo) to avoid HTML duplication; trigger build via GitHub Actions |

At 4 pages, a static site generator adds more complexity than it solves. Shared nav can be duplicated across 4 files without significant maintenance burden.

---

## Sources

- [GitHub Docs: Configuring a publishing source for your GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) — HIGH confidence (official)
- [GitHub Docs: Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) — HIGH confidence (official)
- [Adding images to your GitHub Pages site](https://tomcam.github.io/least-github-pages/adding-images-github-pages-site.html) — MEDIUM confidence (community guide, verified against official docs)
- [GitHub Pages image path issues — mkdocs community](https://github.com/mkdocs/mkdocs/issues/1757) — MEDIUM confidence (real-world report confirming root-relative path breakage)

---
*Architecture research for: GitHub Pages showcase site integration with Python MCP project*
*Researched: 2026-03-18*
