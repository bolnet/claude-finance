# Pitfalls Research

**Domain:** GitHub Pages showcase site added to existing Python/ML project — targeting finance professionals (non-developers)
**Researched:** 2026-03-18
**Confidence:** HIGH (GitHub Pages deployment mechanics, web UX) / MEDIUM (finance professional conversion patterns — community sources, no direct A/B test data)

---

## Critical Pitfalls

### Pitfall 1: Broken Asset Paths Due to Project Page URL Prefix

**What goes wrong:**
GitHub Pages for a project repository (not a user/org root site) serves at `https://username.github.io/repo-name/`, not at root. Any asset path beginning with `/` (e.g., `href="/css/style.css"`, `src="/images/chart.png"`) resolves to `https://username.github.io/css/style.css` — missing the `/repo-name/` prefix — and returns a 404. Every page loads unstyled, images are broken, and navigation links 404. This is the single most common GitHub Pages deployment failure.

**Why it happens:**
Developers write root-relative paths that work on `localhost` or a custom domain. The `/repo-name/` prefix is invisible during local development. The problem only surfaces after deployment, and the symptom (unstyled pages, broken images) looks like a CSS bug, not a path bug.

**How to avoid:**
Use strictly relative paths for all assets: `./css/style.css` from the same directory, `../css/style.css` from a subdirectory. Alternatively, set a `<base href="/repo-name/">` tag in the `<head>` of every HTML page and use root-relative paths consistently. If using Jekyll, configure `baseurl: /repo-name` in `_config.yml`. Test the deployed URL — not localhost — before marking phase complete.

**Warning signs:**
- Styles load locally but disappear after `git push`
- Browser DevTools shows 404s for CSS/JS/image files at paths missing the repo name
- Navigation links work on the homepage but 404 from any subdirectory page

**Phase to address:**
Phase 1 (site scaffolding and deployment setup). Establish the correct base path convention before a single page is written. Fixing this after content is complete requires touching every `href` and `src` across all pages.

---

### Pitfall 2: Jekyll Processing Conflicts with Python Project Files

**What goes wrong:**
GitHub Pages runs Jekyll by default on every repository, even when you want plain HTML. Jekyll has specific reserved directories: folders starting with `_` are processed as Jekyll source. The existing Python project has directories like `src/`, `finance_output/`, and test output that Jekyll may misinterpret, slow down, or fail on. More critically, Jekyll will not serve files in directories starting with `_` or `.`, which includes `.planning/` — fine for privacy, but unexpected. If the site accidentally references any Python source files, Jekyll errors can silently prevent the entire site from building.

**Why it happens:**
Developers assume GitHub Pages is a simple file host. The Jekyll processing layer is invisible until it breaks something. Python projects contain files (`.py`, `__pycache__`, `*.pyc`) that Jekyll either ignores or chokes on depending on configuration.

**How to avoid:**
Add a `.nojekyll` file to the `docs/` folder root (or the branch root if using a `gh-pages` branch). This disables Jekyll processing entirely and makes GitHub Pages serve the `docs/` directory as a pure static file server. No `_config.yml` needed, no Liquid template gotchas, no build failures from Python project structure. Pure HTML/CSS/JS in the `docs/` folder is the correct approach for this project.

**Warning signs:**
- GitHub Pages build logs show Jekyll errors or warnings
- Pages fail to build with no obvious HTML error
- Python source files appear in the served site or cause 404s upstream

**Phase to address:**
Phase 1 (repository and deployment setup). Add `.nojekyll` as the very first file committed to `docs/`. Verify in GitHub repo Settings → Pages that the build source is set to the correct branch and folder before writing any HTML.

---

### Pitfall 3: Messaging Written for Developers, Not Finance Professionals

**What goes wrong:**
The site describes the product in technical language that resonates with the builder but alienates the target audience. Examples of what goes wrong: "MCP server with FastMCP 2.x and 11 registered tools over stdio and streamable-HTTP transports" — finance professionals do not know what MCP, FastMCP, stdio, or streamable-HTTP mean and will not try to find out. If the first thing a hedge fund analyst reads is technical architecture, they leave. Bounce rate will be near 100% from the target audience.

**Why it happens:**
The builder knows the product deeply and describes it from the inside out. Technical accuracy feels important. The instinct is to explain how it works, not what the user gets. Finance professionals think in outcomes: "Will this help me get the answer faster? Does it look credible? Do I have to learn Python?"

**How to avoid:**
Lead with the outcome, not the mechanism. Replace every technical description with its finance equivalent:
- "MCP server with 11 tools" → "11 built-in analyses: price charts, returns, volatility, ML risk models, and more"
- "FastMCP stdio transport" → omit entirely
- "scikit-learn classification pipeline" → "machine learning that classifies investor segments"
- "yfinance integration" → "live market data from Yahoo Finance"

The hero headline must answer "what do I get?" in under 10 words. The subheadline must answer "how is that possible without me coding?" Every feature description must start with the finance outcome, not the technical mechanism.

**Warning signs:**
- Any page that uses the words "server," "transport," "stdio," "MCP," "pipeline," or "FastMCP" without immediate plain-English translation
- Feature descriptions that say "the tool does X" rather than "you can now do X in seconds"
- The word "Python" appears before the value proposition is established

**Phase to address:**
Phase 1 (landing page copy) and Phase 2 (features and walkthroughs pages). Write copy from the finance professional's perspective first; add technical notes as secondary detail for the technical users who may also visit.

---

### Pitfall 4: Chart Images That Are Too Large, Too Small, or Unreadable

**What goes wrong:**
The existing `finance_output/charts/` directory contains matplotlib PNG outputs generated for terminal/notebook use — typically 10–15 inch figure size at 100 DPI, saved as 800KB–2MB files. Used directly in the website: (1) they load slowly on mobile connections, (2) they render at the wrong aspect ratio when the browser scales them, and (3) text and axis labels that are readable at full size become illegible when thumbnailed in a gallery. The site looks amateurish, and slow load times increase bounce rate, especially on mobile.

**Why it happens:**
The charts were generated for one purpose (terminal output, reports) and are reused for another (marketing web page). The matplotlib defaults — DPI, figure size, font size, padding — are not web-optimized. Reusing existing output files is the path of least resistance.

**How to avoid:**
Export web-optimized versions of the key showcase charts separately:
- Target: PNG at 800px wide, ~100KB max per chart
- Use `plt.savefig(path, dpi=96, bbox_inches='tight')` with figure size set to (8, 5) inches
- Alternatively, export to WebP format which achieves 30–50% smaller file sizes than PNG at equivalent visual quality
- Provide thumbnails (400px wide) for gallery views, linking to full-size versions
- Do not copy-paste the raw `finance_output/` files into the site without resizing

For the 5–6 showcase charts on the site, manually optimize is sufficient. If the chart count grows beyond 10, automate with a GitHub Actions step using an image compression action (e.g., Calibre Image Actions).

**Warning signs:**
- Any image file in the site's `docs/` folder larger than 500KB
- Images that display correctly on desktop but overflow their container on mobile
- Lighthouse performance score below 80 (image sizing is a top contributor)

**Phase to address:**
Phase 2 (visual showcase / features page). Export web-optimized chart versions as part of building that phase, not as a retrofit after deployment.

---

### Pitfall 5: Navigation That Breaks on Mobile or Between Page Levels

**What goes wrong:**
Multi-page static sites on GitHub Pages have no server-side routing. Navigation links that use root-absolute paths (`href="/features.html"`) break when the site is at `/repo-name/features.html`. Navigation links that use `href="../features.html"` work from subdirectory pages but 404 from root-level pages. Result: users click navigation on mobile and land on 404 pages, or the hamburger menu opens but anchor links don't close it.

A secondary mobile pitfall: hamburger menus with anchor-only links (`#section`) do not auto-close after navigation. Users tap a section link, the menu stays open, and the page scrolls under it — a known bug when using hash-based routing with JavaScript-free implementations.

**Why it happens:**
Navigation is designed on desktop, at root level. Cross-page and cross-level navigation edge cases only appear when testing from subdirectory pages and on actual mobile devices. HTML-only navigation without JavaScript cannot handle menu state on anchor clicks.

**How to avoid:**
- Use a single flat file structure inside `docs/` — all pages at the same directory level (`docs/index.html`, `docs/features.html`, `docs/walkthroughs.html`) — so relative links are simply `href="features.html"` from any page, no `../` needed.
- For mobile menus: add a small JavaScript toggle (10–15 lines) that closes the menu when any nav link is clicked, including anchor links. This is a one-time addition to the shared navigation component.
- Test navigation on a real mobile device (or DevTools device emulation) from every page before marking the navigation phase complete.

**Warning signs:**
- Navigation works on the landing page but 404s from features or walkthroughs pages
- Hamburger menu stays open after tapping a link on mobile
- Any nav link starting with `/` instead of a relative path

**Phase to address:**
Phase 1 (site scaffolding). Set the flat `docs/` directory structure and navigation template as the first deliverable. All subsequent pages inherit from this template.

---

### Pitfall 6: "Getting Started" That Assumes Developer Familiarity

**What goes wrong:**
The getting started page says things like "clone the repo, run `pip install -e .`, configure your MCP server in `claude_desktop_config.json`" without explaining what any of those steps mean to someone who has never used a terminal. Finance professionals who are Claude.ai browser users have no idea what `pip install`, `claude_desktop_config.json`, or MCP means. If the first step requires opening a terminal, many will stop immediately. The page must convert interest into action — if it creates confusion instead, adoption never happens.

**Why it happens:**
The builder knows the install process from their own experience and documents it accurately for a technically literate audience. The target audience's technical floor is invisible until you write for them.

**How to avoid:**
Write two distinct installation paths on the getting started page:
1. **Claude.ai browser users** (lower friction): install the plugin, click a link, follow prompts. Describe what they'll see at each step, with screenshots or annotated chart images showing the result.
2. **Claude Code users** (higher friction): step-by-step terminal instructions with exact copy-paste commands. Preface each command with what it does in plain English: "This command downloads the skill to your computer."

Anticipate the two most common failure points (Python not installed; MCP not configured) and provide troubleshooting links. Never assume the reader has used a terminal before.

**Warning signs:**
- Getting started page has more than 5 steps without screenshots
- Any step says "configure" without showing exactly what to put where
- Terminal commands are shown without explaining what they accomplish
- The page does not have separate tracks for Claude.ai vs. Claude Code

**Phase to address:**
Phase 3 (getting started page). Write the copy by imagining a senior portfolio manager who has never opened a terminal. If they cannot follow it without asking a question, it needs revision.

---

### Pitfall 7: GitHub Pages Not Enabled Before Pushing the Workflow

**What goes wrong:**
When using GitHub Actions to deploy (the modern approach), you must enable GitHub Pages in the repository Settings → Pages and set the source to "GitHub Actions" before the first workflow run. If the workflow file is pushed first, the `github-pages` environment does not exist yet, the deployment step fails with a permissions or environment error, and the failure message is cryptic. Teams waste time debugging a workflow that is technically correct.

**Why it happens:**
It is not obvious that the environment must be pre-created through the UI before the CI/CD can use it. Documentation for GitHub Actions deployment often skips this step or buries it.

**How to avoid:**
Make "enable GitHub Pages in Settings → Pages, set source to GitHub Actions" the documented first step in the deployment phase plan — before writing any workflow YAML. Verify the setting is saved and the `github-pages` environment appears in the repository's Environments list. Only then push the workflow file.

**Warning signs:**
- First workflow run fails with "environment 'github-pages' not found" or permissions errors
- Deployment step shows `Error: HttpError: Not Found` on the pages deploy action
- Settings → Pages shows "No site" even after workflow succeeds

**Phase to address:**
Phase 1 (deployment setup). This is the first action to take — before writing any HTML.

---

### Pitfall 8: Missing SEO Fundamentals That Prevent Discovery

**What goes wrong:**
The site is beautiful and converts well but nobody finds it because: (1) no `<title>` tags beyond the default, (2) no `<meta name="description">` on any page, (3) no `sitemap.xml` submitted to search engines, (4) no Open Graph tags so social shares show blank previews. Finance professionals who hear about the tool and search for it cannot find the GitHub Pages site in results. Shared links on LinkedIn (a primary finance professional channel) show as blank cards with no image or description.

**Why it happens:**
SEO and social meta tags are not visible during development and are easy to defer. They feel like extras. For a developer tool, the audience might arrive via GitHub directly — but for finance professionals, they may arrive via a LinkedIn post or a team Slack link, where the preview card is the first impression.

**How to avoid:**
Add to every HTML page's `<head>`:
```html
<title>[Page-specific title] | Finance AI Skill</title>
<meta name="description" content="[Page-specific 150-character description]">
<meta property="og:title" content="[Page title]">
<meta property="og:description" content="[Description]">
<meta property="og:image" content="[Absolute URL to a 1200x630 social card image]">
<meta property="og:url" content="[Canonical page URL]">
```
Generate a `sitemap.xml` listing all pages with their URLs. Create a single 1200x630 social card image (a chart visual + the product name) used as the OG image across all pages. These are one-time additions that require no ongoing maintenance.

**Warning signs:**
- Browser tab shows generic or empty title
- Sharing a page URL on LinkedIn/Slack shows no description or image
- Google search of the exact product name does not surface the site within 2 weeks of launch

**Phase to address:**
Phase 1 (site scaffolding). Add the meta tag template to the shared HTML head before pages are written. It is much harder to add unique descriptions retroactively.

---

### Pitfall 9: Walkthrough Pages That Read Like Feature Lists, Not Stories

**What goes wrong:**
The walkthroughs page lists the 6 role scenarios as bullet points: "Equity research: price analysis, returns, volatility." This tells a finance professional nothing they care about. The value of the walkthroughs is showing that an analyst can describe a question in plain English and get a complete answer — the narrative, the surprise, the "I didn't know it could do that" moment. Feature lists do not create that. They look the same as every other tool's feature list.

**Why it happens:**
The natural instinct is to inventory what exists, not to tell a story about what it enables. Documenting the 6 roles as a checklist is faster than writing scenario narratives.

**How to avoid:**
Each walkthrough entry should have three elements:
1. The situation in one sentence: "You're an FP&A analyst preparing a board deck and need to explain the company's liquidity exposure."
2. What you type into Claude: a verbatim example prompt.
3. What you get back: a screenshot of the chart output and a 2-sentence description of the insight.

This format shows the product working, not just existing. It answers the finance professional's real question: "Would this actually work for something I do?"

**Warning signs:**
- Walkthrough page is entirely text with no chart images
- Role descriptions are noun phrases ("Equity research: returns analysis") rather than scenario sentences
- No example prompts shown — the user cannot see what to type

**Phase to address:**
Phase 2 (walkthroughs page). Write copy from actual walkthrough session transcripts, not from the feature list in PROJECT.md.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Reuse raw `finance_output/` chart PNGs directly | No additional export step | 1–2MB images slow page load; illegible on mobile | Never for web use — always export web-optimized versions |
| Root-absolute paths (`/css/style.css`) | Familiar, clean-looking | 404s on all assets when deployed to project pages URL | Never — always use relative paths or `<base>` tag |
| Single HTML page with anchor-only "navigation" | Avoids multi-page path complexity | Hard to link directly to features or walkthroughs; poor SEO per topic | Only acceptable for a true MVP with <4 sections |
| No `.nojekyll` file | One less file to create | Jekyll processes the Python project structure and may break builds | Never — add `.nojekyll` immediately |
| Shared navigation as copy-pasted HTML per page | No JS/build tool required | Navigation changes require editing every page; divergence guaranteed over time | Acceptable if site is <5 pages and navigation is frozen |
| Skipping `sitemap.xml` | Faster to ship | Site takes longer to index; may never surface in search results for target audience | Only acceptable in private/internal deploys — never for public launch |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| GitHub Pages + existing Python repo | Putting `docs/` at repo root but not configuring Pages to serve from it | In Settings → Pages, explicitly set source branch and `/docs` folder; verify the setting saves |
| GitHub Actions deployment | Pushing workflow YAML before enabling Pages in Settings | Enable Pages and set source to "GitHub Actions" first; then push workflow |
| chart images from `finance_output/` | Copying files with absolute paths hardcoded into `src=` attributes | Use paths relative to the `docs/` directory; copy or symlink web-optimized image versions into `docs/images/` |
| Mobile hamburger nav + anchor links | Pure CSS toggle (`:checked` hack) doesn't close on anchor link click | Add 10-line JavaScript that listens for click on any nav link and removes the open class |
| `og:image` meta tag | Using a relative path like `./images/social-card.png` | Open Graph image must be an absolute URL: `https://username.github.io/repo-name/images/social-card.png` |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Unoptimized matplotlib PNGs in page | 3–8 second load on mobile; Lighthouse flags images | Export web-optimized 800px PNGs at 96 DPI; target <150KB per image | Immediately — even 1 large image tanks mobile Lighthouse score |
| Multiple large chart images on one page without lazy loading | Visitors who never scroll download all images | Add `loading="lazy"` to all `<img>` tags below the fold | Any page with >3 images |
| Inline CSS duplicated across pages | Fast to write initially | Any style change requires editing every page | After any design iteration |
| No `<link rel="preload">` for hero image | Hero section appears blank briefly on first load | Preload the above-the-fold hero image in `<head>` | Always visible on slow connections |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Accidentally committing `.planning/` internal docs to `docs/` | Roadmap, research notes, and planning context exposed publicly | Add `.planning/` to `.gitignore`; verify only intended content is in `docs/` before first push |
| Using a third-party analytics script (GA, Hotjar) without disclosure | GDPR/CCPA exposure for EU/CA visitors; adds tracking without consent | If analytics are added later, disclose in a privacy notice; for MVP, omit analytics entirely — GitHub Insights is sufficient |
| Hotlinking external images or fonts without fallback | Third-party URL changes or goes down, breaking site visuals | Self-host web fonts in `docs/fonts/`; export all images to `docs/images/` |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Hero section leads with product name, not outcome | Finance professional reads "Finance AI Skill" and does not know if this is relevant to them | Lead with the outcome: "Get professional-grade financial analysis in plain English — no Python required" |
| Installation page has developer-only instructions | Claude.ai users (lower friction path) are not shown their easier route | Separate installation tracks: "Using Claude.ai?" vs. "Using Claude Code?" with the lower-friction path listed first |
| Walkthroughs page has no images | Page reads like documentation, not a showcase | Every role walkthrough must show at least one chart output from that scenario |
| Call-to-action buttons say "Learn More" | Generic CTA does not communicate what happens next | Use specific CTAs: "Try the Demo" or "Install in Claude Code" or "Add to Claude.ai" |
| No social proof or credibility signal | Finance professionals are risk-averse; unknown tools don't get installed | Add context: "Built on the pyfi.com curriculum" and "11 tools covering market analysis and ML workflows" |
| Mobile viewport not configured | Site renders at desktop width on mobile; all text is tiny | Add `<meta name="viewport" content="width=device-width, initial-scale=1">` to every page |

---

## "Looks Done But Isn't" Checklist

- [ ] **Deployment:** Site appears to deploy — verify the live URL (`username.github.io/repo-name/`) loads styled correctly with no 404s in DevTools.
- [ ] **Mobile:** Pages look fine on desktop — verify on a real mobile device (or DevTools 375px) that text is readable, images fit, and navigation works.
- [ ] **Navigation:** Links work from the landing page — verify every nav link works from every page (features → walkthroughs, walkthroughs → getting started, etc.).
- [ ] **Images:** Charts render on the page — verify each chart image is <500KB and readable at mobile widths.
- [ ] **SEO:** Pages have titles — verify every page has a unique `<title>`, `<meta description>`, and `og:image` with an absolute URL.
- [ ] **Copy:** Features are listed — verify every feature description leads with the finance professional outcome, not the technical mechanism.
- [ ] **Getting Started:** Install steps are present — verify a non-technical person can follow each step without prior terminal experience.
- [ ] **Jekyll:** Site builds — verify `.nojekyll` file is present in `docs/` folder.
- [ ] **Walkthroughs:** Roles are listed — verify each role has an example prompt, at least one chart image, and a scenario framing sentence.
- [ ] **CTAs:** Buttons exist — verify every call-to-action button has a specific, action-oriented label and leads to a working destination.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Broken asset paths discovered after deployment | MEDIUM | Fix base path convention; update all `href`/`src` attributes across all pages; redeploy |
| Jekyll build failure from Python project structure | LOW | Add `.nojekyll` to `docs/`; push; verify build succeeds |
| Pages not enabled before workflow push | LOW | Enable Pages in Settings → Pages → set source to GitHub Actions; re-run the failed workflow |
| Messaging written for developers, discovered in user test | MEDIUM | Rewrite feature descriptions and hero copy; all other structure can remain |
| Large images discovered via Lighthouse audit | MEDIUM | Export web-optimized versions of showcase charts; replace files in `docs/images/`; redeploy |
| Missing Open Graph meta tags discovered when sharing | LOW | Add OG tags to HTML head template; propagate to all pages; create social card image |
| Mobile navigation broken discovered after launch | LOW–MEDIUM | Add JS close-on-click handler; test all nav links on mobile; redeploy |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Broken asset paths (root-absolute vs. relative) | Phase 1 — site scaffolding | Deploy first page; open DevTools Network tab; confirm zero 404s |
| Jekyll conflicts with Python project | Phase 1 — repository setup | Confirm `.nojekyll` in `docs/`; confirm build log shows no Jekyll processing |
| GitHub Pages not enabled before workflow | Phase 1 — deployment setup | Settings → Pages shows correct source before any YAML is pushed |
| Developer-centric messaging | Phase 1 — landing page copy | Read every description aloud to a non-technical person; no jargon without translation |
| Unoptimized chart images | Phase 2 — visual showcase | Run Lighthouse on the features page; Performance score must be >80 |
| Mobile navigation breakage | Phase 1 — navigation template | Test every nav link on 375px viewport from every page |
| Weak getting started copy | Phase 3 — getting started page | Follow the instructions as if you have never used a terminal; all steps must be completable |
| Missing SEO meta tags | Phase 1 — site scaffolding | Validate with a social preview tool (e.g., opengraph.xyz) before launch |
| Feature list instead of walkthrough stories | Phase 2 — walkthroughs page | Each role entry must have scenario sentence, example prompt, and at least one chart image |
| Missing viewport meta tag | Phase 1 — HTML head template | DevTools mobile emulation: page must not require horizontal scrolling at 375px |

---

## Sources

- GitHub Docs — Configuring a publishing source for GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Docs — Using custom workflows with GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- Maxim Orlov — "Deploying to Github Pages? Don't Forget to Fix Your Links": https://maximorlov.com/deploying-to-github-pages-dont-forget-to-fix-your-links/
- Pluralsight — "Fixing Broken Relative Links on GitHub Pages": https://www.pluralsight.com/guides/fixing-broken-relative-links-on-github-pages
- Jekyll issue #332 — baseurl / base-url relative link failures on Project Pages: https://github.com/jekyll/jekyll/issues/332
- Landingi — "Finance Landing Pages: Definition, How to Create & 8 Examples": https://landingi.com/blog/landing-pages-in-finance/
- Growth Fueling — "Landing Page Mistakes That Kill Conversions in 2025": https://growthfueling.com/landing-page-mistakes-that-kill-conversions-in-2025/
- JekyllPad — "Mastering SEO for GitHub Pages": https://www.jekyllpad.com/blog/mastering-github-pages-seo-7
- daily.dev — "2025 Developer Tool Trends: What Marketers Need to Know": https://business.daily.dev/resources/2025-developer-tool-trends-what-marketers-need-to-know/
- GitHub Community Discussion — "GitHub Pages for a repo with multiple subfolders": https://github.com/orgs/community/discussions/58276
- Astrowind Issue #165 — "Mobile Menu issue when using anchor links in Nav": https://github.com/arthelokyo/astrowind/issues/165
- Safnaj (Medium) — "Image Compression for the Web using GitHub Actions": https://safnaj.medium.com/image-compression-for-the-web-using-github-actions-f1156d281cda

---

*Pitfalls research for: GitHub Pages showcase site — Finance AI Skill v1.3*
*Researched: 2026-03-18*
