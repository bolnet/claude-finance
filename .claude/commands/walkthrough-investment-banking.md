---
description: Investment banking walkthrough -- comparable company analysis, relative valuation, and deal pitch quantitative materials
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read, mcp__finance__ping, mcp__finance__validate_environment, mcp__finance__analyze_stock, mcp__finance__get_returns, mcp__finance__get_volatility, mcp__finance__get_risk_metrics, mcp__finance__compare_tickers, mcp__finance__correlation_map
model: sonnet
---

## Investment Banking Walkthrough: Comparable Company Analysis

> *You are a junior analyst on the Technology M&A team at a bulge-bracket investment bank. Your Managing Director is pitching an acquisition advisory mandate for a mid-cap cloud infrastructure company. The target's comps universe is the mega-cap cloud/tech group: **MSFT**, **GOOGL**, **AMZN**, **CRM**, and **ORCL**. You need to build the quantitative exhibits for the pitch book — performance comps, risk profiles, and correlation analysis that frame the "why now" transaction rationale.*

This walkthrough takes approximately 10–15 minutes and runs automatically. Each phase produces data that a real IB analyst would incorporate into the pitch book exhibits and MD talking points.

---

## Walkthrough Instructions

Execute each phase below IN ORDER. After each step:
1. Run the tool or code as instructed
2. Show the result (output, metrics, or chart path)
3. Provide a PLAIN-ENGLISH EXPLANATION framed as deal pitch commentary — write as if you are drafting notes for the pitch book exhibits
4. Print a separator line (`---`)
5. Proceed immediately to the next step

Do NOT ask the user for input between steps. If any step fails, explain the error in plain English and continue.

---

## Phase 1: Pre-Flight Check

### Step 1: Environment Validation

Call `validate_environment` with no arguments.

After running:
- Confirm all packages are ready
- Note: A deal pitch workflow requires market data and quantitative libraries to build defensible comps exhibits. yfinance provides live LTM price data, pandas handles the time series transformations, matplotlib generates the publication-ready charts, and scikit-learn powers any quantitative screening. All must be validated before building pitch book materials.

---

## Phase 2: Individual Comp Profiles

> *The first step in any comparable company analysis is building the per-name data. For each comp, the analyst needs the LTM price trajectory to establish whether the name is trading at a premium or discount to its historical average — a key input to valuation multiples selection.*

### Step 2: Comp Profile — MSFT

Call `analyze_stock` with:
- ticker: "MSFT"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as deal pitch: "Over the LTM period, MSFT traded from $[start price] to $[end price], representing [appreciation/depreciation] of [Z]%. For the pitch book, this establishes MSFT as a [premium/value/in-line] comp — its [upward/downward/sideways] trajectory signals that the market is [rewarding/discounting] its [cloud/enterprise] positioning. If the target prices similarly to MSFT, this sets the upper [or lower] bound on our implied valuation range."

---

### Step 3: Comp Profile — GOOGL

Call `analyze_stock` with:
- ticker: "GOOGL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as deal pitch: "GOOGL's LTM trajectory shows [description vs MSFT from Step 2]. Compare to MSFT: if GOOGL has [outperformed/underperformed] MSFT over the same period, it suggests different market sentiment toward cloud-native vs enterprise software positioning. This divergence is useful for the MD's pitch — it demonstrates that the comps universe is not monolithic and that targeted positioning matters for valuation."

---

### Step 4: Comp Profile — AMZN

Call `analyze_stock` with:
- ticker: "AMZN"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as deal pitch: "AMZN's price action over the LTM reflects its [cloud/e-commerce/logistics] mix. As the comps universe's [largest/most diversified] name by revenue, AMZN's trajectory sets a different benchmark than pure-play SaaS comps like CRM. For the pitch, AMZN serves as the 'market cap anchor' — its valuation multiple typically represents the [premium/floor] end for infrastructure-adjacent targets."

---

### Step 5: Comp Profile — CRM

Call `analyze_stock` with:
- ticker: "CRM"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as deal pitch: "CRM (Salesforce) is the pure-play enterprise SaaS benchmark in this comps set. Its LTM performance of [X]% reflects market sentiment on the SaaS premium. For a cloud infrastructure target, CRM's trading multiple provides the 'software premium' reference point — if the target has meaningful recurring subscription revenue, it may merit CRM-like pricing rather than the hardware/infrastructure discount."

---

### Step 6: Comp Profile — ORCL

Call `analyze_stock` with:
- ticker: "ORCL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as deal pitch: "ORCL (Oracle) represents the legacy enterprise technology comp — a high-margin, slower-growth name that typically trades at a discount to pure-play cloud names. ORCL's LTM performance of [X]% establishes the valuation floor in this comps set. If the target's growth profile is closer to ORCL than to MSFT or CRM, the MD must justify any premium in the pitch book."

---

## Phase 3: Relative Performance — Deal Pitch Exhibits

> *The core of any pitch book is the relative performance exhibit. Normalized to a common starting point, this chart instantly communicates which names have outperformed — and frames the 'why now' argument by showing recent momentum shifts.*

### Step 7: Exhibit A — LTM Relative Performance

Call `compare_tickers` with:
- tickers: "MSFT,GOOGL,AMZN,CRM,ORCL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the normalized performance ranking (best to worst)
- Frame as pitch book: "Exhibit A — LTM Relative Performance. On a normalized basis (all names indexed to $100 at the start of the LTM period), [top performer] has outperformed the comps group by [Y] percentage points over 12 months, suggesting the market assigns a growth premium to its [cloud/AI/enterprise] positioning. [Bottom performer] has lagged the group by [Z]pp, which the MD can use to identify where the valuation gap is widest — and where an acquirer might find the most attractive entry point."

---

### Step 8: Exhibit B — Recent Momentum (90-Day Window)

Call `compare_tickers` with:
- tickers: "MSFT,GOOGL,AMZN,CRM,ORCL"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the 90-day normalized performance ranking
- Compare to the 12-month ranking from Step 7
- Frame as pitch book: "Exhibit B — Recent Momentum. The 90-day window reveals [acceleration/deceleration] in [name]. Compare to the LTM exhibit: if the 90-day ranking [matches/diverges from] the 12-month ranking, it signals [momentum continuation/momentum reversal]. The MD will use this to frame the 'why now' timing argument — specifically, [name]'s recent [outperformance/underperformance] suggests the market is beginning to [reprice/re-rate] the [cloud/enterprise] segment. This is the timing hook for the acquisition pitch."

---

### Step 9: Deep Dive — Top LTM Performer

Look at the Step 7 compare_tickers output. Identify the ticker with the highest LTM normalized return.

Call `get_returns` with:
- ticker: [the top LTM performer from Step 7]
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show cumulative return, average daily return, and the return chart path
- Frame as pitch book: "The strongest comp, [X], delivered cumulative returns of [Y]% over the LTM with average daily returns of [Z]%. This sets the upper bound for valuation multiples in the pitch — an acquirer pricing the target off this comp will apply the highest implied premium. However, the MD should note that [X]'s performance may reflect idiosyncratic factors (e.g., a specific product cycle or M&A catalyst) that do not apply to the target. The pitch book should document why [X] is or is not the most relevant comp for multiple selection."

---

### Step 10: Deep Dive — Bottom LTM Performer

Look at the Step 7 compare_tickers output. Identify the ticker with the lowest LTM normalized return.

Call `get_returns` with:
- ticker: [the bottom LTM performer from Step 7]
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show cumulative return, average daily return, and the return chart path
- Frame as pitch book: "The weakest comp, [X], with cumulative returns of [Y]% over the LTM, establishes the valuation floor for the comps group. An acquirer using [X] as the primary pricing benchmark would imply a lower transaction value for the target. The MD's job is to argue why the target deserves positioning above [X] — typically by citing superior growth rates, higher recurring revenue, or stronger customer retention. The pitch book must include this floor-to-ceiling comps range to show the full valuation spectrum."

---

## Phase 4: Risk Profile Comps Table

> *Beyond price performance, institutional buyers evaluate risk-adjusted quality. The Sharpe ratio, maximum drawdown, and beta tell the story of how each comp manages downside — and which names command valuation premiums for their superior risk management.*

### Step 11: Risk Profile — MSFT

Call `get_risk_metrics` with:
- ticker: "MSFT"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe ratio, max drawdown, and beta
- Note these exact values for the Exhibit C table in Step 16

---

### Step 12: Risk Profile — GOOGL

Call `get_risk_metrics` with:
- ticker: "GOOGL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe ratio, max drawdown, and beta
- Note these exact values for the Exhibit C table in Step 16

---

### Step 13: Risk Profile — AMZN

Call `get_risk_metrics` with:
- ticker: "AMZN"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe ratio, max drawdown, and beta
- Note these exact values for the Exhibit C table in Step 16

---

### Step 14: Risk Profile — CRM

Call `get_risk_metrics` with:
- ticker: "CRM"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe ratio, max drawdown, and beta
- Note these exact values for the Exhibit C table in Step 16

---

### Step 15: Risk Profile — ORCL

Call `get_risk_metrics` with:
- ticker: "ORCL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe ratio, max drawdown, and beta
- Note these exact values for the Exhibit C table in Step 16

---

### Step 16: Exhibit C — Comparable Company Risk Profiles

Do NOT call any tools. This is a pure analysis step.

Build the comparison table using data from Steps 11–15:

#### Exhibit C — Comparable Company Risk Profiles

| Metric | MSFT | GOOGL | AMZN | CRM | ORCL |
|--------|------|-------|------|-----|------|
| Sharpe Ratio | [Step 11] | [Step 12] | [Step 13] | [Step 14] | [Step 15] |
| Max Drawdown | [Step 11] | [Step 12] | [Step 13] | [Step 14] | [Step 15] |
| Beta (vs S&P 500) | [Step 11] | [Step 12] | [Step 13] | [Step 14] | [Step 15] |

After building the table:
- **Rank by Sharpe ratio** (best risk-adjusted returns = premium comp): "[#1 name] leads the comps group with a Sharpe of [X], indicating the highest quality of risk-adjusted returns. This name commands premium multiples."
- **Rank by max drawdown** (least tail risk = defensive comp): "[#1 name by min drawdown] shows the most defensive profile with a peak-to-trough decline of [X]% — buyers seeking downside protection would price a target similarly to this comp."
- **Rank by beta** (market sensitivity): "Beta ranges from [low] to [high] across the group. [Lowest beta name] is the most defensive; [highest beta name] amplifies market moves most aggressively."
- **Frame for the pitch book**: "For the pitch book, the comps with Sharpe above [median threshold] command premium multiples. The target should be positioned against [highest Sharpe name] to justify a higher implied valuation — provided the MD can demonstrate comparable return quality in the operating business. The MD should be prepared to defend any premium above the comps group median Sharpe."

---

## Phase 5: Correlation Analysis — Transaction Rationale

> *The correlation exhibit answers the acquirer's portfolio question: "If I buy this target, am I getting diversification or duplication?" For the deal pitch, low correlation to existing holdings is a key strategic rationale.*

### Step 17: Exhibit D — Return Correlation Matrix

Call `correlation_map` with:
- tickers: "MSFT,GOOGL,AMZN,CRM,ORCL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the full 5x5 correlation matrix
- Frame as pitch book: "Exhibit D — Return Correlation Matrix. The [X]/[Y] pair at r=[Z] shows the highest co-movement in the comps group, suggesting these names are near-substitutes from a portfolio perspective. For the deal pitch, an acquirer holding [X] gains limited incremental diversification from acquiring a target that trades similarly to [X] — the strategic rationale must rest on operational synergies rather than portfolio construction benefits. Conversely, the [A]/[B] pair at r=[C] shows the least co-movement, suggesting an acquirer holding [A] would add meaningful diversification by acquiring a target that trades like [B]."

---

### Step 18: Most Differentiated Comp Analysis

Do NOT call any tools. This is a pure analysis step.

Using the correlation matrix from Step 17, calculate each comp's average pairwise correlation with the other four names. Identify the comp with the lowest average correlation.

Frame as pitch book: "The most differentiated comp in the group is [X] with an average pairwise correlation of [Y]. This name trades most independently from the rest of the comps universe — suggesting its return drivers are more idiosyncratic (product cycle, geographic mix, or business model differences) rather than purely macro/sector driven. For the deal pitch, an acquirer seeking portfolio diversification through M&A should focus on targets that trade more like [X] than like the highly correlated [most correlated pair from Step 17]. If the target's return profile resembles [X]'s, that is a strong diversification argument for the acquiring board."

---

### Step 19: Deal Pitch Summary

Do NOT call any tools. This is a pure synthesis step.

Compile the full quantitative case for the pitch book:

#### Pitch Book Quantitative Summary — Cloud/Tech Comps Analysis

**LTM Performance (Steps 2–8):**
- Top performer: [X] at [Y]% (premium comp — upper valuation bound)
- Bottom performer: [X] at [Y]% (value comp — valuation floor)
- Sector dispersion: [Y pp - Z pp] range across the group ([high/moderate/low] dispersion signals [dispersed/tight] valuation multiples)
- Recent momentum shift: [Yes/No — describe which names are accelerating or decelerating in the 90-day window vs LTM]

**Risk Profiles (Steps 11–16):**
- Highest Sharpe: [X] at [Y] — commands valuation premium; represents the quality benchmark
- Lowest drawdown: [X] at [Y]% — most defensive positioning; relevant for risk-averse acquirers
- Beta range: [low]–[high] across the group (market sensitivity spectrum for the comps set)

**Correlation & Diversification (Steps 17–18):**
- Most correlated pair: [X]/[Y] at r=[Z] — near-substitutes; limited diversification benefit
- Most differentiated: [X] with avg r=[Y] — best diversification target profile
- Portfolio implication: [Describe what an acquirer should consider given the correlation structure — which comps suggest strategic duplication vs genuine diversification]

**Transaction Rationale ("Why Now"):**
Using the quantitative evidence from this analysis, frame the timing argument in 2–3 sentences: reference the momentum shifts from Exhibit B (Step 8) to explain market positioning, use the valuation dispersion from Exhibit C (Step 16) to explain the pricing window, and use the differentiation analysis from Step 18 to explain the strategic rationale. The "why now" should answer: "Why should the acquirer act in this market environment rather than waiting?"

---

#### What an IB Analyst Would Do Next

This walkthrough produced the quantitative exhibits for the pitch book. In a live deal situation, the analyst would next:

1. **Overlay EV/Revenue and EV/EBITDA multiples** — Pull trading multiples from CapIQ or Bloomberg for each comp and add them to the Exhibit C risk table. This creates the full "Selected Comparable Companies" analysis that anchors the valuation range.
2. **Build the football field valuation chart** — Use the comps range (Sharpe-ranked floor and ceiling) plus DCF, precedent transactions, and 52-week trading range to construct the football field. The pitch book needs this chart to show the full implied value spectrum.
3. **Draft the pitch book exhibits** — Exhibit A (LTM Relative Performance), Exhibit B (90-Day Momentum), Exhibit C (Risk Profiles), and Exhibit D (Correlation Matrix) are all ready to paste into PowerPoint. Each needs a 2-sentence MD talking point.
4. **Prepare the MD talking points** — The MD needs one-liners for each exhibit: "Our comps show that [top Sharpe name] commands a [X]x multiple — here is why our target deserves [premium/discount] to that benchmark." This is what the analyst writes the night before the pitch.

---

### How This Maps to Traditional Investment Banking Tools

| This Walkthrough | Traditional Tool | Time Saved |
|-----------------|------------------|------------|
| analyze_stock (LTM price chart per comp) | Bloomberg `GP` command × 5 names | Minutes vs manual Bloomberg exports |
| compare_tickers (normalized performance) | Bloomberg `COMP` exhibit or FactSet charting | Auto-normalized, pitch-book-ready |
| get_returns (cumulative returns analysis) | Bloomberg `TRA` screen | Auto-computed cumulative return series |
| get_risk_metrics (Sharpe/drawdown/beta) | FactSet screening + Excel formulas × 5 names | 5 calls vs 5 separate FactSet workflows + Excel |
| correlation_map (5x5 return correlation) | Excel CORREL matrix (manual setup, 25 formulas) | 1 call vs 25 manual Excel formulas |

**Total estimated time savings:** 6–10 hours of Bloomberg/CapIQ data pulling, exhibit formatting, and comps table construction → ~10 minutes with the Finance AI Skill.

---

Walkthrough complete. Use `/finance-analyst` to run ad-hoc equity research queries, or `/finance` for general analysis.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
