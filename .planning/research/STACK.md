# Stack Research

**Domain:** Multi-page GitHub Pages showcase site (static, no backend)
**Researched:** 2026-03-18
**Confidence:** HIGH

---

## Scope

This file covers ONLY new technologies needed for the v1.3 GitHub Pages milestone.
The existing Python/FastMCP/yfinance/scikit-learn/pandas/matplotlib/seaborn stack is
validated and in production — do not re-evaluate or change it.

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Jekyll | 4.4.1 | Static site generator | Native GitHub Pages ecosystem; Liquid templating is learnable in one sitting; massive theme selection; 17+ years of stability; lowest friction for a 4-5 page product showcase |
| Minimal Mistakes (theme) | 4.28.0 | Site layout and visual design | Ships 9 skins, splash/single/archive page layouts, sidebar, responsive grid, and SEO tags out of the box; remote-theme compatible with GitHub Pages; production-proven on thousands of technical/portfolio sites; no custom CSS needed for core pages |
| GitHub Actions | current | Build + deploy pipeline | Required to use Jekyll 4.x on GitHub Pages — the native Pages environment is pinned to Jekyll 3.10.0; `actions/jekyll-build-pages@v1` + `actions/deploy-pages@v4` is the official first-party workflow pair |
| SCSS (via Jekyll) | bundled | Style overrides | Jekyll's built-in Sass pipeline handles `_sass/` overrides on top of Minimal Mistakes; no separate Node/PostCSS build step needed |

### Supporting Libraries (Jekyll Plugins)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| jekyll-seo-tag | 2.8.0 | Open Graph + meta title/description | Always — one `{% seo %}` tag covers all social sharing and search indexing metadata |
| jekyll-sitemap | 1.4.0 | sitemap.xml auto-generation | Always — search discoverability for a product page matters |
| jekyll-feed | 0.17.0 | Atom feed | Include by default; signals content freshness to crawlers |
| jekyll-redirect-from | 0.16.0 | URL redirects | Only if page slugs change post-launch |

All four are whitelisted GitHub Pages gems — they work with or without GitHub Actions.

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Ruby 3.3.4 | Jekyll runtime | Match the version GitHub Pages uses (confirmed at pages.github.com/versions as of 2026-03-18); install via `rbenv` or `asdf` |
| Bundler | Gem dependency management | `bundle exec jekyll serve --livereload` for local preview; commit `Gemfile.lock` to pin versions |
| `gh` CLI | Deployment verification | `gh pages view` confirms deployment URL and status post-push |

---

## Installation

```bash
# One-time: install Ruby 3.3.4 via rbenv
rbenv install 3.3.4
rbenv local 3.3.4

# Project setup (run from docs/ directory)
gem install bundler
bundle init
```

Gemfile contents:

```ruby
source "https://rubygems.org"
gem "jekyll", "~> 4.4"
gem "minimal-mistakes-jekyll"
gem "jekyll-feed"
gem "jekyll-sitemap"
gem "jekyll-seo-tag"
```

```bash
bundle install

# Local preview with live reload
bundle exec jekyll serve --livereload
```

GitHub Actions workflow (`.github/workflows/pages.yml`):

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/jekyll-build-pages@v1
        with:
          source: ./docs
          destination: ./_site
      - uses: actions/upload-pages-artifact@v3

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Configure repository: Settings > Pages > Source = "GitHub Actions".

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Jekyll 4.4 + Minimal Mistakes | Hugo + theme | When build time matters at scale (100+ pages) and the Go toolchain is acceptable; not worth the friction for a 4-5 page static showcase |
| Jekyll 4.4 + Minimal Mistakes | Eleventy (11ty) | When the team is JavaScript-native and needs npm plugin flexibility; adds Node toolchain with no GitHub Pages native benefit for this use case |
| Jekyll 4.4 + Minimal Mistakes | Plain HTML + Tailwind CDN | Zero dependencies, but no layout/includes scaffold; Tailwind CDN is 100kB+ compressed in production and not recommended for shipping; hand-crafting every page layout costs more than using a proven theme |
| GitHub Actions deploy | `github-pages` gem only (native build) | Acceptable only if you want true zero-CI setup and can live with Jekyll 3.10.0 limitations; you lose Jekyll 4 Sass improvements and unrestricted plugins |
| Jekyll 4.4 + Minimal Mistakes | Docusaurus | React-based; appropriate for large documentation sites, not a 5-page product showcase; adds React build pipeline |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Tailwind CSS (full build) | Requires Node.js + PostCSS build step; no native Jekyll integration without a separate webpack/vite config; adds toolchain complexity that conflicts with the Jekyll-only build | Minimal Mistakes SCSS overrides in `_sass/` |
| Tailwind Play CDN | Tailwind's own docs say "development only, not production"; 100kB+ runtime; no class purging; can break strict CSP headers | Minimal Mistakes built-in skins |
| Bootstrap 5 (CDN or npm) | Conflicts with Minimal Mistakes' own grid; Minimal Mistakes already ships a responsive layout; double-loading CSS frameworks creates specificity conflicts | Minimal Mistakes skin + SCSS overrides |
| Next.js / Nuxt / SvelteKit | Server-rendering overhead is wasted on a fully static showcase; requires Vercel/Netlify or complex CI for GitHub Pages; contradicts the "GitHub Pages" hosting constraint | Jekyll |
| Gatsby | GraphQL layer is massive overkill for 5 pages; slow builds; heavy dependency graph; maintenance cost is high | Jekyll |
| `github-pages` gem as sole deploy mechanism | Pins Jekyll to 3.10.0; you lose Jekyll 4 features and cannot use non-whitelisted plugins | GitHub Actions + `jekyll-build-pages@v1` |
| Jekyll 3.x | Outdated; missing Sass improvements; `github-pages` gem lock-in; limited include/layout features | Jekyll 4.4.1 |
| Interactive chart libraries (Plotly, Chart.js) | v1.3 can use static PNG outputs already generated by the MCP tools; JS charting libraries add bundle weight with no benefit for a showcase that links to static images | Existing `finance_output/charts/*.png` assets |

---

## Integration with Existing Project

The site lives in `docs/` at the repo root, completely isolated from `src/finance_mcp/`.

- Chart PNGs already exist in `finance_output/charts/` — copy representative samples into `docs/assets/images/` (commit directly, no runtime generation)
- No Python runtime is involved in building or serving the site
- Existing `tests/`, `src/`, and Python toolchain are completely unaffected
- The GitHub Actions workflow triggers only on changes to `docs/` or the workflow file itself (filter paths to avoid spurious builds on Python changes)

---

## Stack Patterns by Variant

**For 4-5 pages, GitHub Pages hosted, finance professional audience:**
- Source directory: `docs/` (keeps site files separate from Python source)
- Minimal Mistakes skin: `"air"` (light, clean, professional) or `"contrast"` (bold, high-contrast for finance data density)
- No JavaScript framework — Minimal Mistakes ships vanilla JS for navigation; no additions needed
- Images: static PNGs from existing `finance_output/charts/`; no JS charting library

**If interactive demos are added in a future milestone:**
- Defer Plotly or Chart.js to that milestone; do not pre-install
- Keep v1.3 purely static

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| Jekyll ~> 4.4 | Ruby 3.2+ | Ruby 2.x dropped in Jekyll 4.4; use rbenv to pin 3.3.4 to match GitHub Pages runtime |
| minimal-mistakes-jekyll 4.28 | Jekyll 4.x | Tested against Jekyll 4.x per upstream README; remote theme works with `jekyll-remote-theme` plugin |
| actions/jekyll-build-pages@v1 | Jekyll 4.x | Uses a full Ruby environment, not the restricted `github-pages` gem; supports unrestricted plugins |
| actions/deploy-pages@v4 | actions/upload-pages-artifact@v3 | Must be paired — v4 deploy expects v3 artifact format |
| actions/configure-pages@v5 | actions/checkout@v4 | Standard Pages setup pair; always use latest major version tags |

---

## Sources

- [dasroot.net: Hugo vs Jekyll vs 11ty Comparison 2026](https://dasroot.net/posts/2026/03/hugo-vs-jekyll-vs-11ty-static-site-generator-comparison-2026/) — SSG comparison, current (HIGH — same month as research)
- [pages.github.com/versions](https://pages.github.com/versions/) — Native Jekyll 3.10.0, Ruby 3.3.4, plugin versions confirmed (HIGH — fetched 2026-03-18)
- [Jekyll 4.4.0 Release Notes](https://jekyllrb.com/news/2025/01/27/jekyll-4-4-0-released/) — Latest stable version 4.4.1, January 2025 (HIGH)
- [mmistakes/minimal-mistakes GitHub](https://github.com/mmistakes/minimal-mistakes) — v4.28.0, remote theme compatibility confirmed (HIGH)
- [actions/jekyll-build-pages](https://github.com/actions/jekyll-build-pages) — Official first-party build action (HIGH)
- [GitHub Docs: Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) — Actions deploy pattern (HIGH)
- [Tailwind Play CDN docs](https://v3.tailwindcss.com/docs/installation/play-cdn) — "development only, not production" warning (HIGH)
- [mmistakes/mm-github-pages-starter](https://github.com/mmistakes/mm-github-pages-starter) — Quickstart template confirmed (HIGH)

---
*Stack research for: v1.3 GitHub Pages showcase site addition*
*Researched: 2026-03-18*
