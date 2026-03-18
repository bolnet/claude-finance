# Feature Research

**Domain:** Multi-page GitHub Pages showcase site for a Finance AI developer tool
**Researched:** 2026-03-18
**Confidence:** MEDIUM-HIGH (web research confirmed patterns; GitHub Pages structure HIGH; finance professional trust signals HIGH; site-specific copy recommendations MEDIUM)

---

## Context: What This Site Must Do

This is a **showcase site**, not a SaaS landing page and not product documentation. The skill already exists. The site's only job is to convince finance professionals (equity researchers, hedge fund analysts, IBD associates, FP&A managers, PE associates, accountants) that the Finance AI Skill is worth installing and trying — and to get Claude Code users to the install step.

Primary audience: finance professionals who are curious about AI tools but skeptical. They will judge credibility within 10 seconds of landing on the page.

Secondary audience: developers and Claude users discovering MCP tools.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features visitors assume exist. Missing them signals the site is not serious — finance professionals in particular penalize incomplete or low-effort presentation. Confidence: HIGH based on industry research.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Clear value proposition in hero (above fold) | Finance pros have zero patience for ambiguity — if they cannot understand what this does in 5 seconds they leave | LOW | One punchy headline + one sentence subhead; avoid tool jargon ("MCP server") in the first screen |
| Primary CTA visible without scrolling | Every conversion-focused site has a single primary action above the fold | LOW | "Get Started" or "Install Now" — link to Getting Started page |
| What it does, concretely | Finance professionals are skeptical of AI vaporware; concrete examples of outputs build credibility | MEDIUM | Show a real chart output (AAPL price chart, NVDA correlation heatmap) next to the hero or immediately below |
| Navigation to all major pages | Multi-page site needs persistent top nav | LOW | Home, Features, Walkthroughs, Getting Started — max 4 items |
| Mobile-responsive layout | 40%+ of professional browsing is mobile; a broken mobile layout signals low-quality project | MEDIUM | GitHub Pages / Jekyll themes handle this if chosen correctly |
| Page titles and meta descriptions | Search discoverability; also signals the site is not an afterthought | LOW | Each page needs unique `<title>` and `<meta description>` |
| Site loads fast | 53% of users abandon after 3s load time; static sites have no excuse for being slow | LOW | No external JS frameworks; serve charts as optimized PNGs |
| Footer with GitHub repo link | Developers expect to verify the source; finance professionals want to see the code is real | LOW | Link to repo + license notice |

### Differentiators (Competitive Advantage)

Features that distinguish this site from a plain README or a generic tool page. These are what make finance professionals actually pay attention. Confidence: MEDIUM (synthesized from finance professional trust research and developer tool site patterns).

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Role-specific walkthrough sections | Finance professionals identify with their job function — "this was made for equity researchers like me" converts better than generic features | MEDIUM | Dedicated cards or sections for each of the 6 roles (equity research, hedge fund, IB, FP&A, PE, accounting); brief scenario + sample output per role |
| Real chart outputs as visual proof | Showing actual matplotlib/seaborn outputs (price charts, correlation heatmaps, confusion matrices, feature importance plots) is proof the tool works — stock photo alternatives destroy credibility with technical audiences | MEDIUM | Use existing `finance_output/charts/` assets; curate 5-8 best-looking ones; optimize file size |
| Persona contrast demonstration | Showing that the analyst vs PM persona produces different framing for the same data is a subtle but compelling differentiator — no other tool does this | MEDIUM | Side-by-side card or callout on Features page showing same risk metric, two different interpretations |
| Plain-language command examples | Finance pros who are not developers need to see that the commands feel like English — "show me NVDA volatility for the last 6 months" not `get_volatility(ticker='NVDA', window=30)` | LOW | Inline code blocks or callout boxes with real command examples from the walkthroughs |
| Disclaimer transparency | Finance professionals know about compliance risk; explicitly noting the disclaimer on every output actually builds trust rather than undermining it — it signals the tool understands its context | LOW | One-line mention in the features section: "Every output includes a plain-English disclaimer — it is analysis, not advice" |
| "No Python required" positioning | The key promise for the finance audience — they can describe what they want in plain English | LOW | State prominently in hero and repeat in features; the skill's core value proposition for non-developer users |
| Instructor / course attribution | Built on the pyfi.com curriculum — gives the skill academic legitimacy and signals the ML models follow sound methodology (not LLM hallucination) | LOW | Brief mention: "Workflows built on the Python & Machine Learning for Finance curriculum" |
| Dual install path (Claude Code + claude.ai) | Different finance professionals use different Claude surfaces — showing both paths removes friction | MEDIUM | Getting Started page shows two distinct paths with clear instructions for each |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem like good ideas for this site but create problems for the specific audience and context.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Live interactive demo embedded in site | "Let users try it right in the browser" | GitHub Pages is static — no server-side execution; embedding Claude API calls requires backend + API key management; fake/canned demos destroy credibility with technical audiences | Use real static chart outputs (proof of results) and link to the actual `/demo` walkthrough inside Claude |
| Full API documentation on the site | Developers want to see all 11 MCP tool signatures | Overwhelming for the finance professional audience; full docs belong in the README, not a showcase site | One-page features overview with tool names, brief descriptions, and link to the GitHub repo for full docs |
| Blog / articles section | "Content marketing" approach | Adds maintenance burden; static GitHub Pages site has no CMS; stale blog posts hurt credibility | Keep the site focused on showcasing the tool; if content is desired, GitHub Discussions or external posts are lower maintenance |
| Testimonials / social proof section | Standard conversion element | No real user base yet — fabricated or placeholder testimonials destroy trust, especially with finance professionals who are trained skeptics | Lead with concrete demonstrations (real charts, real walkthrough scenarios) instead of social proof; add testimonials only if real users provide them |
| Animated hero / video autoplay | Modern and attention-grabbing | Finance professionals — especially in institutional settings — often view this as unprofessional; video autoplay is blocked on many corporate networks; adds load time | Static screenshots of real outputs are more credible than motion graphics for this audience |
| Dark mode toggle | Developer-friendly touch | Adds JavaScript complexity; GitHub Pages Jekyll sites need explicit dark mode support; not a pain point for finance professionals | Pick one high-contrast color scheme (dark or light) appropriate for finance context and stick to it |
| Comments / discussion section | Community building | No server-side component on GitHub Pages; Disqus and similar services introduce tracking, GDPR issues, and load time; static audience | Direct users to GitHub Discussions or Issues for feedback; simpler and more credible for a developer tool |
| Deep feature comparison tables vs competitors | "Show how we're better than Bloomberg Copilot" | Finance professionals already know Bloomberg costs $24k/year — comparison invites scrutiny and can look defensive; positions the tool as inferior by comparison | Focus on what the tool uniquely enables (natural language finance workflows in Claude); no explicit competitor naming |

---

## Feature Dependencies

```
[Hero section: value proposition + CTA]
    └──required by──> [Home / Landing page] (the entry point for all other pages)

[Navigation bar]
    └──required by──> [All pages] (multi-page site cannot function without nav)

[Real chart assets (finance_output/charts/)]
    └──required by──> [Hero visual proof]
    └──required by──> [Features page: tool demonstrations]
    └──required by──> [Walkthroughs page: role scenario visuals]

[Walkthrough scenarios (from existing v1.2 walkthroughs)]
    └──required by──> [Walkthroughs page content]
    └──enhances──> [Hero section: social proof of depth]

[Getting Started: Claude Code install path]
    └──required by──> [Primary CTA button]
    └──conflicts with──> [Getting Started: claude.ai path] (must be shown as separate tabs or sections, not merged)

[Features page: 11 tools overview]
    └──enhances──> [Getting Started page] (users who understand features are more motivated to install)

[Persona contrast demonstration]
    └──requires──> [Features page] (natural home for analyst vs PM framing example)
    └──enhances──> [Walkthroughs page] (reinforces the role-specific angle)
```

### Dependency Notes

- **Chart assets must be curated first** — the features, walkthroughs, and hero sections all depend on having a curated set of high-quality chart images from the existing `finance_output/charts/` directory. This is a content prerequisite, not a technical one.
- **Getting Started page is the terminal conversion point** — every CTA across all pages should ultimately point here. It must exist before CTAs on other pages are meaningful.
- **Walkthroughs page depends on role scenario content** — the 6 walkthrough scripts from v1.2 already exist; the work is condensing each into a 2-3 sentence scenario + selecting representative chart output.
- **Nav bar is a shared component** — build it once as a Jekyll `_include` or layout element; do not duplicate HTML across pages.
- **Persona contrast conflicts with simplified messaging** — the persona angle is a differentiator but risks confusing visitors who do not know what a "persona" is. Place it on the Features page (where curious users go for depth), not in the hero.

---

## MVP Definition

### Launch With (v1 — the GitHub Pages site)

Minimum that makes the site useful for showcasing the tool and driving installs. Confidence: HIGH.

- [ ] **Landing page (index.html)** — Hero with value prop + primary CTA + one or two real chart visuals; no scrolling required to understand what the tool does
- [ ] **Features page** — Overview of all 11 MCP tools grouped by category (market analysis / ML workflows); real command examples; persona contrast callout
- [ ] **Walkthroughs page** — Six role-based scenarios with brief descriptions and at least one chart output each; cards or sections that finance professionals can self-identify with
- [ ] **Getting Started page** — Two clear install paths (Claude Code via stdio; claude.ai via HTTP + ngrok); copy-pasteable commands; `/demo` command highlighted
- [ ] **Persistent navigation** across all pages
- [ ] **Curated chart assets** — 5-8 optimized PNG outputs from the existing `finance_output/charts/` directory; resized and compressed for web

### Add After Validation (v1.x)

- [ ] **Search engine optimization** — Add structured metadata, Open Graph tags for social sharing; trigger: if organic traffic is a goal
- [ ] **Dark mode** — Only if target audience (developer persona) requests it; not needed for finance professional primary audience
- [ ] **Testimonials / case studies** — Only when real user feedback exists; placeholder testimonials will hurt credibility

### Future Consideration (v2+)

- [ ] **Blog / changelog section** — If the skill is actively maintained and new tool announcements are worth publishing; requires ongoing content effort
- [ ] **Interactive playground** — A genuinely sandboxed demo environment; requires backend; out of scope for a static GitHub Pages site

---

## Feature Prioritization Matrix

For the showcase site specifically:

| Feature | Finance Pro Value | Build Cost | Priority |
|---------|-------------------|------------|----------|
| Hero: clear value proposition + CTA | HIGH | LOW | P1 |
| Real chart outputs as visuals | HIGH | LOW (assets exist) | P1 |
| Getting Started page (two install paths) | HIGH | MEDIUM | P1 |
| Navigation bar (all pages) | HIGH | LOW | P1 |
| Walkthroughs page: 6 role scenarios | HIGH | MEDIUM | P1 |
| Features page: 11 tools overview | HIGH | MEDIUM | P1 |
| Plain-language command examples | HIGH | LOW | P1 |
| Mobile-responsive layout | MEDIUM | LOW (theme handles) | P1 |
| Persona contrast demonstration | MEDIUM | LOW | P2 |
| Course curriculum attribution | MEDIUM | LOW | P2 |
| Open Graph / social meta tags | LOW | LOW | P2 |
| Disclaimer transparency callout | MEDIUM | LOW | P2 |
| Dark mode | LOW | MEDIUM | P3 |
| Blog / changelog | LOW | HIGH | P3 |
| Interactive demo | HIGH | VERY HIGH | P3 |

**Priority key:**
- P1: Must have for the site to launch
- P2: Should have; add before publicizing the site
- P3: Nice to have; future consideration

---

## Page Structure Recommendation

Based on research into developer tool homepages and finance professional landing page patterns. Confidence: MEDIUM-HIGH.

### Page 1: Home / Landing (index.html)

```
[Hero]
  Headline: "Finance analysis in plain English — no Python required"
  Subhead: "A Claude Code skill that runs market analysis and ML workflows
            for finance professionals who describe what they need."
  CTA: "Get Started" → /getting-started
  Visual: One or two real chart outputs (AAPL price chart + NVDA correlation heatmap)

[What it does — 3 columns]
  Market Analysis | Machine Learning Workflows | 6 Role Walkthroughs

[Quick proof]
  2-3 example natural language commands with their chart outputs

[Social proof / attribution]
  "Built on the Python & Machine Learning for Finance curriculum"

[Footer]
  GitHub repo link | License | No tracking
```

### Page 2: Features (/features)

```
[Intro]
  The 11 MCP tools — what they do and why a finance professional cares

[Section 1: Market Analysis Tools]
  Price data, returns, volatility, comparison, correlation, risk metrics
  — real command examples inline

[Section 2: ML Workflow Tools]
  Data ingestion, EDA, liquidity predictor, investor classifier
  — real command examples inline

[Section 3: Persona Modes]
  Analyst vs PM framing — side-by-side example callout

[Section 4: /demo walkthrough]
  What the guided demo covers and how to run it
```

### Page 3: Walkthroughs (/walkthroughs)

```
[Intro]
  "See how each finance role uses the skill"

[6 Role Cards]
  Equity Research | Hedge Fund | Investment Banking | FP&A | Private Equity | Accounting
  Each card: 2-3 sentence scenario + representative chart output

[CTA]
  "Ready to try it? → Get Started"
```

### Page 4: Getting Started (/getting-started)

```
[Two-tab or two-section layout]
  Claude Code (recommended) | claude.ai browser plugin

[Claude Code path]
  1. Install Python dependencies (command)
  2. Configure Claude Code (config snippet)
  3. Run /finance — first command example
  4. Run /demo — the guided walkthrough

[claude.ai path]
  1. Start ngrok server (command)
  2. Add HTTP transport in claude.ai settings
  3. Use as plugin

[Troubleshooting callout]
  Common issues: yfinance rate limits, ngrok auth
```

---

## Finance Professional Trust Signals

Research from Deloitte (2026), FINRA Foundation (2024), CFA Institute (2025) confirms finance professionals have specific trust requirements for AI tools. These are not typical developer tool concerns. Confidence: HIGH.

| Trust Signal | Why It Matters to Finance Professionals | How to Implement |
|--------------|----------------------------------------|-----------------|
| Transparency about what the tool does NOT do | Finance pros are trained to identify scope creep and liability | State clearly on the site: "Analysis output only — not financial advice, not live trading, not Bloomberg data" |
| Disclaimer on every output | 59.7% of finance pros trust AI only within a defined framework; seeing a tool that acknowledges its own limits is reassuring | Screenshot or callout showing the disclaimer text appended to real output |
| Plain-English output, not just raw numbers | Finance professionals at senior levels are decision-makers, not data scientists — they want interpretation | Show the narrative summary below the chart in screenshots |
| Open source / visible code | "Code transparency" is a differentiator vs black-box AI finance tools (Bloomberg Copilot has no transparency) | Link to GitHub repo prominently; mention generated Python code is visible in every output |
| Curriculum alignment | Academic backing reduces the "black box" concern — they know the methodology follows established finance/ML practice | Brief attribution to pyfi.com curriculum in hero or features section |

---

## Competitor / Comparable Site Analysis

Sites analyzed to understand what finance AI tool showcase pages look like in practice. Confidence: MEDIUM.

| Site Pattern | Observation | Implication for This Site |
|--------------|-------------|--------------------------|
| OpenBB Terminal (openbb.co) | Technical documentation focus; heavy on API references; minimal finance professional empathy | Opportunity to differentiate with role-based framing and plain-English copy |
| FinChat.io | Chat-focused; emphasizes natural language; minimal technical transparency | Similar positioning; differentiate with code transparency and ML depth |
| Bloomberg Copilot | Enterprise marketing tone; implies Bloomberg Terminal required | Natural contrast: "No Bloomberg subscription needed; works inside Claude Code you already use" |
| yfinance docs (ranaroussi.github.io) | Pure developer documentation; no finance professional empathy | Shows what NOT to do for this audience |
| Python Graph Gallery (holtzy.github.io) | Gallery-first; chart outputs are the hero; minimal copy | Useful pattern for the walkthroughs page — let the chart outputs speak |

---

## Sources

- Deloitte 2026: "Trust Emerges as Main Barrier to Agentic AI Adoption in Finance" — [tipalti.com/press/ai-in-finance-trust-gap-report/](https://tipalti.com/press/ai-in-finance-trust-gap-report/)
- CFA Institute 2025: "Explainable AI in Finance" — [rpc.cfainstitute.org/research/reports/2025/explainable-ai-in-finance](https://rpc.cfainstitute.org/research/reports/2025/explainable-ai-in-finance)
- FINRA Foundation 2024: AI vs Financial Professional trust study — [finra.org/media-center/newsreleases/2024](https://www.finra.org/media-center/newsreleases/2024/report-finra-foundation-financial-professional-or-artificial-intelligence)
- everydeveloper.com: "How 30 Dev Tool Homepages Put Developers First" — [everydeveloper.com/developer-tool-homepages/](https://everydeveloper.com/developer-tool-homepages/)
- SaaS hero copy patterns: [landingrabbit.com/blog/saas-website-hero-text](https://landingrabbit.com/blog/saas-website-hero-text)
- Unicorn Platform: "Showcase Your Projects With a GitHub Personal Page" — [unicornplatform.com/blog/showcase-your-projects-with-a-github-personal-page-guide/](https://unicornplatform.com/blog/showcase-your-projects-with-a-github-personal-page-guide/)
- Python Graph Gallery (pattern reference): [github.com/holtzy/The-Python-Graph-Gallery](https://github.com/holtzy/The-Python-Graph-Gallery)
- Project context: `.planning/PROJECT.md`

---
*Feature research for: v1.3 GitHub Pages showcase site for Finance AI Skill*
*Researched: 2026-03-18*
