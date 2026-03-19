# Phase 14: Content Pages — Research

**Researched:** 2026-03-18
**Domain:** Static HTML content authoring — landing page, features page, walkthroughs page — for a finance professional audience
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LAND-01 | Hero section with finance-outcome headline and CTA targeting finance professionals | Outcome-led copy patterns, CSS hero layout already in style.css |
| LAND-02 | Real chart output visuals embedded as proof of capability | 8 curated PNGs already in docs/assets/images/ — all under 150KB |
| LAND-03 | Role-based entry points linking to specific walkthrough sections | Link anchors to walkthroughs.html role cards |
| LAND-04 | Stats bar displaying key credibility numbers (11 tools, 6 walkthroughs) | Static HTML element, no JS needed |
| FEAT-01 | 11 MCP tools displayed organized by category (market analysis vs ML workflows) | Tool inventory confirmed: 6 market analysis + 5 ML workflow tools |
| FEAT-02 | Visual examples (chart screenshots) for each tool category | Curated PNGs already available and named descriptively |
| WALK-01 | 6 role cards with scenario descriptions and tool usage per role | All 6 walkthrough command files contain verbatim scenario text |
| WALK-02 | Role-specific chart examples embedded per walkthrough card | 8 curated PNGs — specific assignments documented below |
</phase_requirements>

---

## Summary

Phase 14 replaces three stub pages (`index.html`, `features.html`, `walkthroughs.html`) with full content. The infrastructure is fully in place from Phase 13: the `docs/` folder, shared CSS, mobile nav, 8 curated chart PNGs (all under 150KB), and the HTML template pattern. This phase is primarily a content authoring task, not a technical engineering task.

The single highest-risk item is copy quality, not implementation. Finance professionals (equity researchers, hedge fund analysts, IB associates, FP&A managers, PE associates, controllers) are trained skeptics who judge tools within 10 seconds. Every sentence of hero copy, feature description, and walkthrough card must lead with the finance professional's outcome — never the technical mechanism. The six walkthrough command files (`.claude/commands/walkthrough-*.md`) contain verbatim scenario descriptions and tool invocation sequences that should be adapted directly into the walkthroughs page.

The 11 MCP tools map cleanly into two categories: 6 market analysis tools and 5 ML workflow tools. This category split is the organizing principle for `features.html`. All 8 curated chart images are already in `docs/assets/images/` with stable descriptive filenames — no additional image work is required for this phase.

**Primary recommendation:** Author index.html first (establish design patterns), then features.html, then walkthroughs.html. Each new page extends the existing CSS classes — do not add new CSS files or JavaScript.

---

## Standard Stack

### Core (already in place — Phase 13 delivered)

| Component | Version/Detail | Purpose | Status |
|-----------|---------------|---------|--------|
| `docs/assets/css/style.css` | Phase 13 created | Shared styles — hero, nav, footer, CTA, hero-image | In place |
| `docs/assets/js/main.js` | Phase 13 created | Mobile nav toggle (12-line IIFE) | In place |
| `docs/assets/images/` | 8 PNGs, all <150KB | Chart proof visuals | In place |
| Relative asset paths | Convention set in Phase 13 | No root-absolute paths — GitHub Pages safe | Enforced |

### CSS Classes Already Available

From `docs/assets/css/style.css` (verified by reading the file):

| Class | Purpose |
|-------|---------|
| `.hero` | Hero section — centered, padding 3rem 1rem |
| `.hero h1` | 2.5rem dark blue (#0f3460), responsive to 1.8rem at 640px |
| `.hero p` | 1.1rem grey, max-width 600px |
| `.cta-primary` | Red (#e94560) button, 0.75rem padding, border-radius 4px |
| `.hero-image` | Max 800px wide, box-shadow, margin auto |
| `.page-stub` | Placeholder — replace with real content sections |
| `footer` | Border-top, disclaimer text, 0.85rem grey |

**Brand colors (CSS custom properties pattern):**
- Dark blue: `#0f3460` — nav background, headings
- Red: `#e94560` — CTA buttons, links
- Dark navy: `#1a1a2e` — body text
- White: `#ffffff` — nav text, button text

### New CSS Required

The current stylesheet has hero and stub styles but no card grid, feature list, or stats bar components. These must be added to `style.css` in this phase:

| Component | CSS to add | Notes |
|-----------|-----------|-------|
| Stats bar | `.stats-bar` — flexbox row, 4 numbers centered | LAND-04 |
| Feature category section | `.feature-category`, `.feature-list` | FEAT-01 |
| Walkthrough role card grid | `.role-grid`, `.role-card` | WALK-01, WALK-02 |
| "What it does" 3-column section | `.feature-columns` | LAND-01 supporting content |
| Role entry points | `.role-entry-points` | LAND-03 |

**Installation:** No new packages. All in plain HTML/CSS.

---

## Architecture Patterns

### Recommended Page Structure

All pages live at `docs/` root — sibling files sharing identical relative paths:

```
docs/
├── index.html          # PHASE 14: full content (replace stub hero)
├── features.html       # PHASE 14: full content (replace page-stub)
├── walkthroughs.html   # PHASE 14: full content (replace page-stub)
├── getting-started.html # PHASE 15
├── .nojekyll
└── assets/
    ├── css/style.css   # extend with new classes
    ├── js/main.js      # no changes needed
    └── images/         # 8 curated PNGs already in place
```

### Pattern 1: Head/Nav/Footer Template Reuse

**What:** All four pages share identical `<head>`, `<header>`, and `<footer>` HTML. Only the `<main>` content changes.

**When to use:** Every page in this phase.

**Example (established in Phase 13):**
```html
<!-- head: title + meta description vary per page; all else identical -->
<title>[Page Title] | Finance AI Skill</title>
<meta name="description" content="[Page-specific 150-char description]">

<!-- nav: identical across all 4 pages -->
<nav>
  <a class="nav-brand" href="index.html">Finance AI Skill</a>
  <button class="nav-toggle" aria-label="Toggle navigation">&#9776;</button>
  <ul class="nav-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="features.html">Features</a></li>
    <li><a href="walkthroughs.html">Walkthroughs</a></li>
    <li><a href="getting-started.html">Get Started</a></li>
  </ul>
</nav>

<!-- footer: identical across all 4 pages -->
<footer>
  <p>For educational and informational purposes only. Not financial advice.</p>
</footer>
```

### Pattern 2: Landing Page Section Order (index.html)

**What:** Established section order for the landing page, balancing above-the-fold impact with scroll conversion.

**Section order:**
1. **Hero** — outcome headline + subhead + CTA + chart image (above fold)
2. **Stats bar** — 11 tools | 6 roles | No Python required | Free & open source
3. **What it does** — 3 columns: Market Analysis / ML Workflows / Role Walkthroughs
4. **Role entry points** — 6 role links to walkthroughs.html (LAND-03)
5. **Proof / quick demo** — 1-2 more chart images with caption sentences
6. **Attribution callout** — "Built on the Python & Machine Learning for Finance curriculum"

**Hero headline pattern (outcome-led, not product-led):**
```
WRONG: "Finance AI Skill — An MCP Server with 11 Tools"
RIGHT: "Finance analysis in plain English — no Python required"
```

**Hero subhead template:**
```
"Describe what you need. The skill writes the code, runs the analysis,
and explains the results — so you can focus on the decision, not the data."
```

### Pattern 3: Features Page Tool Grouping (features.html)

**What:** 11 MCP tools organized into two categories. Tool names translated to finance outcomes.

**Confirmed tool inventory** (from `src/finance_mcp/tools/` + SKILL.md):

**Category 1: Market Analysis Tools (6 tools)**

| MCP Tool | Plain-English Name | Finance Outcome |
|----------|-------------------|-----------------|
| `analyze_stock` | Price Chart | "See any stock's price history — 1 month to 5 years — as a publication-ready chart" |
| `get_returns` | Returns Analysis | "Calculate daily returns, cumulative performance, and compare to any benchmark" |
| `get_volatility` | Volatility Analysis | "Measure price volatility and identify regime changes — key for position sizing and risk review" |
| `get_risk_metrics` | Risk Metrics | "Get Sharpe ratio, max drawdown, and beta in one command — no spreadsheet needed" |
| `compare_tickers` | Multi-Ticker Comparison | "Compare up to 5 stocks on a normalized basis — ideal for peer analysis and comps" |
| `correlation_map` | Correlation Heatmap | "See how your holdings move together — critical for portfolio construction and diversification" |

**Category 2: ML Workflow Tools (5 tools)**

| MCP Tool | Plain-English Name | Finance Outcome |
|----------|-------------------|-----------------|
| `ingest_csv` | Data Profiling | "Upload your ERP or portfolio CSV — the skill profiles the data, flags anomalies, and identifies modeling targets" |
| `liquidity_predictor` | Liquidity Risk Model | "Train a regression model on your data to predict liquidity risk scores — no Python, no sklearn setup" |
| `predict_liquidity` | Liquidity Scoring | "Score a new client or position against your trained model — single command, instant result" |
| `investor_classifier` | Investor Segmentation | "Train a classification model to segment investors by profile — outputs labeled segments and feature importance" |
| `classify_investor` | Investor Classification | "Classify a new investor into a segment using your trained model" |

### Pattern 4: Walkthroughs Page Card Format (walkthroughs.html)

**What:** 6 role cards. Each card has exactly three elements: situation sentence, verbatim example prompt, chart image.

**Source material** (confirmed from `.claude/commands/walkthrough-*.md`):

| Role | Command | Scenario Summary | Key Tickers/Data | Best Chart |
|------|---------|-----------------|-----------------|------------|
| Equity Research | `/walkthrough-equity-research` | Sell-side analyst initiating NVDA coverage; needs quantitative backbone for initiation report | NVDA vs AMD/INTC/AVGO/QCOM | `compare-semiconductor-stocks.png` |
| Hedge Fund | `/walkthrough-hedge-fund` | Quant PM assessing volatility regimes and pair trading opportunities across semis + mega-cap tech | NVDA/AMD/AVGO vs AAPL/MSFT/GOOGL | `correlation-heatmap.png` |
| Investment Banking | `/walkthrough-investment-banking` | IB analyst building comps exhibits for M&A pitch on cloud infrastructure target | MSFT/GOOGL/AMZN/CRM/ORCL | `compare-tech-stocks.png` |
| Accounting | `/walkthrough-accounting` | Controller profiling ERP transaction data for quarterly close sign-off and audit committee prep | sample_portfolio.csv | `confusion-matrix.png` |
| FP&A | `/walkthrough-fpa` | FP&A analyst profiling ERP export and building liquidity risk forecast for VP of Finance | sample_portfolio.csv | `residual-plot.png` |
| Private Equity | `/walkthrough-private-equity` | VP at mid-market PE fund scoring deal pipeline for IC memo; Fund III $400M deployment target | sample_portfolio.csv | `feature-importance.png` |

**Card structure template:**
```html
<div class="role-card">
  <h3>[Role Title]</h3>
  <p class="scenario">[One situation sentence — "You are a [role] preparing to [task]..."]</p>
  <blockquote class="example-prompt">"[Verbatim example prompt the user would type]"</blockquote>
  <img src="assets/images/[chart].png" alt="[Descriptive alt text]" loading="lazy">
  <a href="walkthroughs.html#[role-anchor]" class="role-link">See full walkthrough</a>
</div>
```

### Anti-Patterns to Avoid

- **Using MCP jargon in copy:** "MCP server," "stdio transport," "FastMCP," "scikit-learn pipeline" must never appear in marketing copy without immediate plain-English translation. If it appears, it should appear only in a secondary "How it works" technical detail, never in the primary description.
- **Feature list walkthroughs:** "Equity Research: returns, volatility, risk metrics" tells the finance professional nothing. Each card MUST have a situation sentence, not a noun list.
- **Root-absolute paths:** Never use `/assets/...`. Always use `assets/...` (relative, no leading slash). This was established in Phase 13 and must not drift.
- **Adding a new CSS file:** Do not create a `features.css` or `walkthroughs.css`. All new component styles go in the single shared `style.css`.
- **`loading="lazy"` on the hero image:** The hero image is above the fold — it should NOT have `loading="lazy"`. Below-fold images should. Note: the current `index.html` stub incorrectly has `loading="lazy"` on the hero image — this should be corrected in Phase 14.
- **Hero headline starting with the product name:** "Finance AI Skill is a..." — finance professionals do not know or care what the product is named until after they understand the value.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Mobile card grid | Custom flexbox/grid from scratch | CSS grid with `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` | Standard responsive card pattern, one line |
| Stats bar numbers | JS counter animation | Static HTML numbers | No JS needed; animation adds complexity for no conversion value with finance professionals |
| Tab component for feature categories | JS tab switcher | Two `<section>` elements with `<h2>` headings | Finance pros scroll; tabs hide content; sections are indexable by search |
| Role filter buttons | JS filter system | Static card grid — all 6 visible | 6 cards is not too many to show at once; filtering adds JS complexity with zero benefit |
| Copy-pasted navigation HTML | Find-replace across files | Copy nav HTML verbatim from index.html to features.html and walkthroughs.html | Site is 4 pages — template engines not warranted; note any nav change requires touching 4 files |

**Key insight:** This phase is HTML authoring. The less JavaScript introduced, the better — GitHub Pages serves static files and finance professionals on corporate networks often have script blockers.

---

## Common Pitfalls

### Pitfall 1: Hero Headline That Leads with the Product Name

**What goes wrong:** "Finance AI Skill — Professional Analysis Tools" — finance professional does not know if this is relevant to them after reading the headline.

**Why it happens:** The builder naturally leads with what the thing IS rather than what the user GETS.

**How to avoid:** Test the headline with this question: "Does this tell a hedge fund PM what they get, in 8 words or fewer?" Lead with the outcome. "Finance analysis in plain English — no Python required" passes. "Finance AI Skill" fails.

**Warning signs:** Hero h1 contains the words "Finance AI Skill", "MCP", "tool", or "platform" before any mention of what the user achieves.

---

### Pitfall 2: Walkthrough Cards Written as Feature Lists

**What goes wrong:** "Equity Research: analyze_stock, get_returns, get_volatility, get_risk_metrics, compare_tickers, correlation_map" — tells the finance professional nothing about why they would want this.

**Why it happens:** The builder lists what they built; the user wants to know what problem is solved.

**How to avoid:** Each walkthrough card must answer three questions: (1) What situation am I in? (2) What would I type? (3) What do I get back? Use the verbatim scenario text from `.claude/commands/walkthrough-*.md` as source material — do not paraphrase from memory.

**Warning signs:** Walkthrough card contains MCP tool names, no situation sentence, or no example prompt.

---

### Pitfall 3: `loading="lazy"` on the Hero Image

**What goes wrong:** The hero image — the chart directly below the hero headline — flickers in blank on first page load, making the page look broken on slow connections.

**Why it happens:** Phase 13 stub applied `loading="lazy"` to the hero image as a copy-paste default. This is correct for below-fold images but wrong for the hero.

**How to avoid:** Remove `loading="lazy"` from the hero image in `index.html`. All other images on all three pages should keep `loading="lazy"`.

**Warning signs:** Hero image is slow to appear on throttled connection in DevTools.

---

### Pitfall 4: Role Entry Points on Landing Page Don't Link to Specific Cards

**What goes wrong:** "Walkthroughs →" link goes to `walkthroughs.html` top, not to the specific role card — e.g., clicking "I'm a hedge fund analyst" drops the user at the top of the page with no visual connection to the relevant card.

**Why it happens:** Anchor links to specific sections require matching `id` attributes on the target cards.

**How to avoid:** Give each role card a matching `id` attribute on `walkthroughs.html` (e.g., `id="equity-research"`, `id="hedge-fund"`). Then link from `index.html` LAND-03 entry points as `walkthroughs.html#equity-research`.

**Warning signs:** Clicking a role entry point lands at the top of the walkthroughs page with no scroll to the relevant section.

---

### Pitfall 5: Chart Image Alt Text Is Empty or Generic

**What goes wrong:** `alt=""` or `alt="chart"` — fails accessibility audit and loses context if image fails to load on corporate network.

**Why it happens:** Alt text is easy to defer; the image is the important thing.

**How to avoid:** Each image alt text should describe what the chart shows and why it matters: `alt="AAPL, GOOGL, MSFT, and NVDA normalized price comparison over 6 months"`. The existing Phase 13 hero image has `alt="Tech stock comparison chart"` — improve this in Phase 14.

---

### Pitfall 6: Stats Bar Numbers That Are Wrong or Stale

**What goes wrong:** Claiming "12 tools" when 11 are shipped, or "7 walkthroughs" when 6 exist — finance professionals who verify are immediately distrustful.

**Why it happens:** Aspirational copy written before feature count is locked.

**How to avoid:** Use only confirmed-shipped numbers: **11 tools** (6 market analysis + 5 ML workflow, confirmed from `src/finance_mcp/tools/`), **6 role walkthroughs** (confirmed from SKILL.md), **2 install paths** (Claude Code + claude.ai — confirmed).

---

## Code Examples

### Landing Page Hero Section

```html
<!-- index.html — replace current <section class="hero"> -->
<section class="hero">
  <h1>Finance analysis in plain English —<br>no Python required</h1>
  <p>Describe what you need. The Finance AI Skill writes the code, runs the analysis,
     and explains the results — so you focus on the decision, not the data.</p>
  <a class="cta-primary" href="getting-started.html">Get Started Free</a>
  <img
    class="hero-image"
    src="assets/images/compare-tech-stocks.png"
    alt="AAPL, GOOGL, MSFT, and NVDA normalized price comparison over 6 months"
  >
  <!-- No loading="lazy" on hero image — it is above the fold -->
</section>
```

### Stats Bar (LAND-04)

```html
<!-- Add to index.html after hero, new CSS class needed in style.css -->
<section class="stats-bar">
  <div class="stat"><strong>11</strong><span>built-in analyses</span></div>
  <div class="stat"><strong>6</strong><span>role walkthroughs</span></div>
  <div class="stat"><strong>0</strong><span>Python required</span></div>
  <div class="stat"><strong>Free</strong><span>open source</span></div>
</section>
```

```css
/* Add to style.css */
.stats-bar {
  display: flex;
  justify-content: center;
  gap: 3rem;
  padding: 2rem 1rem;
  background: #f8f9fa;
  text-align: center;
  flex-wrap: wrap;
}

.stat strong {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #0f3460;
}

.stat span {
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Role Entry Points (LAND-03)

```html
<!-- Add to index.html — links into specific walkthrough anchors -->
<section class="role-entry-points">
  <h2>Built for how you work</h2>
  <div class="role-grid">
    <a href="walkthroughs.html#equity-research" class="role-entry">
      <strong>Equity Research</strong>
      <span>Coverage initiation, peer comps, risk profiling</span>
    </a>
    <a href="walkthroughs.html#hedge-fund" class="role-entry">
      <strong>Hedge Fund</strong>
      <span>Volatility regimes, pair trading, cross-sector correlation</span>
    </a>
    <a href="walkthroughs.html#investment-banking" class="role-entry">
      <strong>Investment Banking</strong>
      <span>Comparable company analysis, deal pitch exhibits</span>
    </a>
    <a href="walkthroughs.html#fpa" class="role-entry">
      <strong>FP&amp;A</strong>
      <span>ERP data profiling, liquidity forecasting, budget variance</span>
    </a>
    <a href="walkthroughs.html#private-equity" class="role-entry">
      <strong>Private Equity</strong>
      <span>Deal scoring, IC memo prep, portfolio monitoring</span>
    </a>
    <a href="walkthroughs.html#accounting" class="role-entry">
      <strong>Accounting &amp; Control</strong>
      <span>Transaction profiling, anomaly detection, ERP review</span>
    </a>
  </div>
</section>
```

### Walkthrough Role Card

```html
<!-- walkthroughs.html — one card per role, with anchor id for deep-linking -->
<div class="role-card" id="equity-research">
  <h3>Equity Research Analyst</h3>
  <p class="scenario">
    Your head of research assigns you coverage of NVDA within the semiconductor sector.
    You need the quantitative backbone — price history, risk profile, and peer comps —
    before writing a single page of the initiation report.
  </p>
  <blockquote class="example-prompt">
    "Compare NVDA against AMD, INTC, AVGO, and QCOM over the last year
    and show me correlation and risk metrics for each name."
  </blockquote>
  <img
    src="assets/images/compare-semiconductor-stocks.png"
    alt="NVDA, AMD, INTC, AVGO, and QCOM normalized price comparison — semiconductor peer group"
    loading="lazy"
  >
  <p class="walkthrough-cta">Run <code>/walkthrough-equity-research</code> in Claude Code for the full scenario.</p>
</div>
```

### Role Card Grid CSS

```css
/* Add to style.css */
.role-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.role-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: #ffffff;
}

.role-card h3 {
  color: #0f3460;
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
}

.role-card .scenario {
  color: #444;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.role-card .example-prompt {
  background: #f8f9fa;
  border-left: 3px solid #e94560;
  padding: 0.75rem 1rem;
  margin: 0 0 1rem;
  font-style: italic;
  font-size: 0.9rem;
  color: #333;
}

.role-card img {
  border-radius: 4px;
  margin-bottom: 1rem;
}

.walkthrough-cta {
  font-size: 0.85rem;
  color: #666;
}

.walkthrough-cta code {
  background: #f0f0f0;
  padding: 0.1em 0.3em;
  border-radius: 3px;
  font-size: 0.9em;
}
```

### Feature Category Section CSS

```css
/* Add to style.css */
.feature-category {
  margin-bottom: 3rem;
}

.feature-category h2 {
  color: #0f3460;
  font-size: 1.6rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e94560;
}

.feature-category .category-intro {
  color: #666;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  list-style: none;
}

.feature-item {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 1rem 1.25rem;
}

.feature-item strong {
  color: #0f3460;
  display: block;
  margin-bottom: 0.25rem;
}

.feature-item p {
  color: #555;
  font-size: 0.9rem;
  margin: 0;
}
```

---

## State of the Art

| Old Approach | Current Approach | Impact for This Phase |
|--------------|-----------------|----------------------|
| Tab-based tool categories | Sectioned scroll layout | Sections are indexable, more readable, no JS |
| Generic "Learn More" CTAs | Action-specific CTAs ("Run /walkthrough-equity-research") | Higher intent match for finance audience |
| Product-led hero headline | Outcome-led hero headline | Finance professionals identify faster |
| Feature list walkthroughs | Scenario + prompt + chart card format | Converts by showing real use, not just listing capability |
| Lazy-load all images | Lazy-load below fold only; eager-load hero | Better LCP (Largest Contentful Paint) score |

---

## Image Assignment Map

All 8 curated PNGs from Phase 13 and their recommended usage in Phase 14:

| Filename | Assigned To | Page |
|----------|------------|------|
| `compare-tech-stocks.png` | Hero image (primary) + IB walkthrough card | index.html + walkthroughs.html |
| `compare-semiconductor-stocks.png` | Equity Research walkthrough card + Market Analysis feature section | walkthroughs.html + features.html |
| `correlation-heatmap.png` | Hedge Fund walkthrough card + Market Analysis feature section | walkthroughs.html + features.html |
| `volatility-analysis.png` | Supporting proof section on landing page | index.html |
| `confusion-matrix.png` | Accounting walkthrough card + ML Workflow feature section | walkthroughs.html + features.html |
| `feature-importance.png` | Private Equity walkthrough card + ML Workflow feature section | walkthroughs.html + features.html |
| `eda-credit-risk.png` | FP&A walkthrough card + ML Workflow feature section | walkthroughs.html + features.html |
| `residual-plot.png` | FP&A walkthrough card (secondary) | walkthroughs.html |

Note: Some images are used on multiple pages. This is intentional — the same PNG can appear in the features page (illustrating a category) and the walkthroughs page (for a specific role card). No duplication of files needed.

---

## Open Questions

1. **Page section heading for LAND-04 stats bar placement**
   - What we know: LAND-04 requires a stats bar with key credibility numbers
   - What's unclear: Whether the stats bar sits directly below the hero (between hero and "what it does" section) or is embedded within the hero section
   - Recommendation: Place it directly below the hero as a visually distinct band — max contrast between the centered hero and the stats bar's grey background

2. **How many chart images to show on features.html**
   - What we know: FEAT-02 requires "visual examples for each tool category" — that means at least 2 images (one per category)
   - What's unclear: Whether one image per category satisfies, or one image per major tool
   - Recommendation: One representative image per category (market analysis → `compare-semiconductor-stocks.png`; ML workflows → `confusion-matrix.png`) is sufficient; showing all 8 on one page would overwhelm

3. **Persona contrast callout (P2 feature from FEATURES.md)**
   - What we know: Research flagged "analyst vs PM framing on same data" as a differentiator for features.html
   - What's unclear: Whether this is in scope for Phase 14 (not listed in LAND-01 through WALK-02 requirements)
   - Recommendation: Implement as a simple callout box on features.html if it does not add complexity — it requires only a text description, no new chart image. Keep it if it fits naturally; defer if it extends authoring time.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (existing — confirmed from tests/ directory) |
| Config file | pytest.ini (check if exists) or pyproject.toml |
| Quick run command | `python3 -m pytest tests/ -x -q` |
| Full suite command | `python3 -m pytest tests/ -v` |

Note: Phase 14 is pure HTML/CSS content authoring. No Python code is modified. The existing pytest suite remains the test framework for the Python MCP skill; Phase 14 does not introduce new Python tests.

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LAND-01 | Hero headline present, outcome-led, above fold | Manual visual review | DevTools: check h1 text at 1200px viewport | N/A — HTML content |
| LAND-02 | At least one real chart image embedded in index.html | Manual / grep | `grep -c "assets/images" docs/index.html` — expect ≥ 1 | N/A |
| LAND-03 | Role entry points link to walkthroughs.html with anchors | Manual / link check | Check all hrefs contain `walkthroughs.html#` | N/A |
| LAND-04 | Stats bar with tool count, walkthrough count visible | Manual visual review | DevTools: confirm stats-bar section present | N/A |
| FEAT-01 | features.html has sections for both tool categories, all 11 tools named | Manual review | Read features.html and count tool entries | N/A |
| FEAT-02 | At least one chart image per tool category on features.html | Manual / grep | `grep -c "assets/images" docs/features.html` — expect ≥ 2 | N/A |
| WALK-01 | 6 role cards, each with situation sentence and example prompt | Manual review | Check for 6 `.role-card` divs, each with `.scenario` and `.example-prompt` | N/A |
| WALK-02 | Each walkthrough card has a chart image | Manual / grep | `grep -c "role-card" docs/walkthroughs.html` vs `grep -c "assets/images" docs/walkthroughs.html` | N/A |

### Sampling Rate

- **Per task commit:** Run existing Python test suite to verify no Python regressions: `python3 -m pytest tests/ -x -q`
- **Per wave merge:** Full suite + manual browser check of all three pages at 375px and 1200px viewports
- **Phase gate:** All 8 requirements verified manually in browser (DevTools Network tab: zero 404s); Lighthouse Performance score ≥ 80 on index.html

### Wave 0 Gaps

None — existing Python test infrastructure covers all phase requirements. Phase 14 introduces no new Python code. HTML content verification is manual.

---

## Sources

### Primary (HIGH confidence)

- Phase 13 SUMMARY (`13-01-SUMMARY.md`) — exact files created, CSS classes available, image filenames, decisions made
- `docs/assets/css/style.css` — verified CSS class inventory and brand colors
- `docs/index.html` — confirmed current stub structure, identified `loading="lazy"` hero bug
- `docs/features.html` / `docs/walkthroughs.html` — confirmed stub state ready for content replacement
- `.claude/skills/finance/SKILL.md` — confirmed all 6 walkthroughs, 11 tools, intent routing, demo mode
- `.claude/commands/walkthrough-*.md` (all 6 files) — confirmed verbatim scenario text, role descriptions, tool sequences
- `src/finance_mcp/tools/` directory listing — confirmed 11 tool files (6 market analysis + 5 ML)
- `.planning/REQUIREMENTS.md` — confirmed exact requirement text for LAND-01 through WALK-02
- `.planning/research/FEATURES.md` — finance professional trust signals, page structure recommendation
- `.planning/research/PITFALLS.md` — copy pitfalls, image pitfalls, navigation pitfalls
- `.planning/research/SUMMARY.md` — executive summary, phase rationale, confidence assessment

### Secondary (MEDIUM confidence)

- CFA Institute 2025 — "Explainable AI in Finance" (cited in FEATURES.md and SUMMARY.md) — finance professional trust signals
- FINRA Foundation 2024 — AI vs Financial Professional trust study (cited in FEATURES.md) — outcome-led copy rationale
- Deloitte 2026 — "Trust Emerges as Main Barrier to Agentic AI Adoption in Finance" (cited in FEATURES.md) — disclaimer transparency value

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Phase 13 delivered and verified; all CSS classes, images, and paths confirmed by reading actual files
- Architecture: HIGH — page structure sourced from reading actual HTML; tool inventory confirmed from source directory
- Copy patterns: MEDIUM-HIGH — outcome-led copy guidelines sourced from research with named industry sources; specific headline wording untested with real users
- Pitfalls: HIGH — verified by reading Phase 13 stub and identifying the `loading="lazy"` hero image bug in the actual code

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable static HTML domain; no external dependencies to go stale)
