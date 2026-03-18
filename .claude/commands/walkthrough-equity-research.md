---
description: Detailed equity research walkthrough — coverage initiation, peer comps, risk profiling, and trading analysis
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read, mcp__finance__ping, mcp__finance__validate_environment, mcp__finance__analyze_stock, mcp__finance__get_returns, mcp__finance__get_volatility, mcp__finance__get_risk_metrics, mcp__finance__compare_tickers, mcp__finance__correlation_map
model: sonnet
---

## Equity Research Walkthrough: Coverage Initiation

> *You are a sell-side equity research analyst initiating coverage on a new name. This walkthrough builds the quantitative foundation for your initiation report — the data that feeds into your quarterly earnings model, valuation framework, and peer comparison tables.*
>
> **Scenario:** Your head of research has assigned you coverage of **NVDA** (NVIDIA Corporation) within the semiconductor sector. Your coverage universe peers are **AMD**, **INTC**, **AVGO**, and **QCOM**. You need the quantitative backbone before writing a single page.

This walkthrough takes approximately 10–15 minutes and runs automatically. Each phase produces data that a real analyst would paste into their initiation report or earnings model.

---

## Walkthrough Instructions

Execute each phase below IN ORDER. After each step:
1. Run the tool or code as instructed
2. Show the result (output, metrics, or chart path)
3. Provide a PLAIN-ENGLISH EXPLANATION framed as equity research commentary — write as if you are drafting notes for the "Quantitative Overview" section of the initiation report
4. Print a separator line (`---`)
5. Proceed immediately to the next step

Do NOT ask the user for input between steps. If any step fails, explain the error in plain English and continue.

---

## Phase 1: Pre-Flight Check

### Step 1: Environment Validation

Call `validate_environment` with no arguments.

After running:
- Confirm all packages are ready
- Note: An equity research workflow depends on yfinance for live market data, pandas for data manipulation, matplotlib for chart generation, and scikit-learn for any quantitative screening. All must be present before the analysis begins.

---

## Phase 2: Single-Name Deep Dive (NVDA)

> *The first thing an analyst does when initiating coverage is pull the full quantitative profile of the target company. This phase answers: "What does the stock's price action, return profile, volatility regime, and risk characteristics tell us before we even open the 10-K?"*

### Step 2: Price History — 12-Month Chart

Call `analyze_stock` with:
- ticker: "NVDA"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the price trend and chart path
- Frame as research: "Over the trailing 12 months, NVDA has [risen/fallen] X%..."
- Identify: Was the move linear or did it show distinct regimes (rally, consolidation, drawdown)?
- Note for the initiation report: The 12-month chart establishes the price context that institutional clients see first. A stock that rallied 100% has different investor expectations than one that ground sideways.

---

### Step 3: Price History — 6-Month Chart (Recent Regime)

Call `analyze_stock` with:
- ticker: "NVDA"
- start: [180 days before today, in YYYY-MM-DD format]

After running:
- Compare the 6-month trend to the 12-month trend from Step 2
- Frame as research: "The more recent 6-month window shows [acceleration/deceleration/reversal] relative to the 12-month trend..."
- Note: Analysts often show both timeframes in initiation reports. The 12-month shows the full story; the 6-month shows the current momentum regime. Clients want to know "what is happening NOW, not just what happened."

---

### Step 4: Returns Analysis — Daily and Cumulative

Call `get_returns` with:
- ticker: "NVDA"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show cumulative return, average daily return, and the last 10 trading days
- Frame as research: "NVDA has delivered a cumulative return of X% over 12 months, averaging Y% per trading day..."
- Identify: Are there clusters of large positive or negative days? This reveals event-driven moves (earnings, product launches, macro shocks)
- Note: The cumulative return chart is what analysts paste into the "Performance Summary" section. It answers: "If I had invested $100 a year ago, what would it be worth today?"

---

### Step 5: Volatility Profile

Call `get_volatility` with:
- ticker: "NVDA"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show annualized volatility and note the rolling 21-day chart
- Frame as research: "NVDA exhibits annualized volatility of X%, which is [above/below] the S&P 500 average of ~15%..."
- Interpret the rolling chart: "Volatility spiked around [date/period], likely driven by [earnings/macro/sector rotation]..."
- Note for valuation: High-volatility stocks require wider confidence intervals on price targets. An analyst will adjust their DCF discount rate or comps premium/discount based on this volatility profile.

---

### Step 6: Risk Metrics — Sharpe, Drawdown, Beta

Call `get_risk_metrics` with:
- ticker: "NVDA"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show all three metrics prominently
- Frame as the "Risk Profile" section of the initiation report:
  - **Sharpe ratio:** "NVDA's risk-adjusted return quality is [X] — [above/below] the 1.0 threshold that institutional investors use as a quality hurdle..."
  - **Max drawdown:** "The worst peak-to-trough decline was X% — this is the number the risk committee will ask about. Any investor who bought at the peak experienced a X% paper loss before recovery..."
  - **Beta:** "At X beta, NVDA [amplifies/dampens] S&P 500 moves by [Y]%. This positions it as a [high-beta growth / defensive / market-neutral] holding..."
- Save these exact numbers — they will be compared to each peer in Phase 3.

---

## Phase 3: Peer Comparison (Coverage Universe)

> *No initiation report is complete without a peer comparison. The head of research will ask: "How does NVDA compare to AMD, INTC, AVGO, and QCOM?" This phase builds the quantitative peer table.*

### Step 7: Risk Metrics — AMD

Call `get_risk_metrics` with:
- ticker: "AMD"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe, drawdown, and beta
- Frame briefly: "AMD shows [X] Sharpe, [Y]% drawdown, [Z] beta..."

---

### Step 8: Risk Metrics — INTC

Call `get_risk_metrics` with:
- ticker: "INTC"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe, drawdown, and beta
- Frame briefly: "INTC shows [X] Sharpe, [Y]% drawdown, [Z] beta..."

---

### Step 9: Risk Metrics — AVGO

Call `get_risk_metrics` with:
- ticker: "AVGO"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe, drawdown, and beta
- Frame briefly: "AVGO shows [X] Sharpe, [Y]% drawdown, [Z] beta..."

---

### Step 10: Risk Metrics — QCOM

Call `get_risk_metrics` with:
- ticker: "QCOM"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show Sharpe, drawdown, and beta
- Frame briefly: "QCOM shows [X] Sharpe, [Y]% drawdown, [Z] beta..."

---

### Step 11: Peer Risk Comparison Table

Do NOT call any tools. This is a pure analysis step.

Build a comparison table using the data from Steps 6–10:

#### Semiconductor Coverage Universe — Risk Profile Summary

| Metric | NVDA | AMD | INTC | AVGO | QCOM |
|--------|------|-----|------|------|------|
| Sharpe Ratio | [Step 6] | [Step 7] | [Step 8] | [Step 9] | [Step 10] |
| Max Drawdown | [Step 6] | [Step 7] | [Step 8] | [Step 9] | [Step 10] |
| Beta (vs S&P 500) | [Step 6] | [Step 7] | [Step 8] | [Step 9] | [Step 10] |

After building the table:
- **Rank by Sharpe ratio** — which name delivers the best risk-adjusted returns?
- **Rank by max drawdown** — which name has the worst tail risk?
- **Rank by beta** — which is most/least sensitive to market moves?
- **Identify outliers**: Is any name dramatically different from the peer group? A much higher Sharpe suggests outperformance; a much worse drawdown suggests structural risk.
- Frame as research commentary: "Within the semiconductor coverage universe, [X] stands out for its [metric] while [Y] lags on [metric]..."

---

## Phase 4: Relative Performance

> *Institutional clients want to see how these stocks actually trade relative to each other. Did NVDA outperform its peers, or did the entire sector rise together? This phase answers that question with normalized performance and correlation data.*

### Step 12: Normalized Performance — Full Coverage Universe

Call `compare_tickers` with:
- tickers: "NVDA,AMD,INTC,AVGO,QCOM"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the ranking from best to worst performer
- Frame as research: "Normalizing all five names to a $100 starting value 12 months ago reveals [X] as the clear outperformer at $[Y] and [Z] as the laggard at $[W]..."
- Note: This chart goes directly into the "Relative Performance" section of the initiation report. It is the single most-requested chart by institutional clients during roadshows.

---

### Step 13: Normalized Performance — Recent 90 Days

Call `compare_tickers` with:
- tickers: "NVDA,AMD,INTC,AVGO,QCOM"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Compare the 90-day ranking to the 12-month ranking from Step 12
- Frame as research: "In the more recent 90-day window, the ranking [shifts/holds]..."
- Identify momentum changes: Is a 12-month leader fading? Is a laggard catching up?
- Note: Divergence between the two timeframes signals a regime change — exactly the kind of inflection point that generates buy/sell rating changes.

---

### Step 14: Correlation Heatmap — Coverage Universe

Call `correlation_map` with:
- tickers: "NVDA,AMD,INTC,AVGO,QCOM"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the full 5x5 correlation matrix
- Identify:
  - **Most correlated pair:** These names are near-substitutes from a portfolio construction perspective. An investor holding one gets limited incremental benefit from holding the other.
  - **Least correlated pair:** This is the "diversification trade" within semis. Owning both captures different return drivers.
  - **NVDA's average correlation** with the group: Is NVDA trading as a semiconductor stock, or has it decoupled from the sector (e.g., trading as an AI proxy)?
- Frame as research: "NVDA shows [high/moderate/low] correlation with the broader semi group, suggesting it [is/is not] trading as a pure semiconductor name..."

---

## Phase 5: NVDA vs Broader Market

> *The final phase positions NVDA against non-semiconductor benchmarks. Is NVDA a "tech stock" or an "AI stock"? Does it trade more like MSFT and GOOGL than like its semi peers?*

### Step 15: Cross-Sector Comparison

Call `compare_tickers` with:
- tickers: "NVDA,AAPL,MSFT,GOOGL"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the normalized returns ranking
- Frame as research: "Against mega-cap tech peers outside the semiconductor sector, NVDA has [outperformed/underperformed/matched]..."
- Note: If NVDA outperforms AAPL/MSFT/GOOGL by a wide margin, it reinforces the "AI premium" thesis. If it trades in line, the premium may already be priced in.

---

### Step 16: Cross-Sector Correlation

Call `correlation_map` with:
- tickers: "NVDA,AAPL,MSFT,GOOGL,AMD"
- start: [365 days before today, in YYYY-MM-DD format]

After running:
- Show the correlation matrix
- **Key question:** Is NVDA more correlated with AMD (its semiconductor peer) or with MSFT/GOOGL (its AI ecosystem partners)?
  - If NVDA/MSFT correlation > NVDA/AMD correlation: NVDA is trading as an AI infrastructure play, not a traditional semiconductor
  - If NVDA/AMD correlation > NVDA/MSFT correlation: NVDA is still trading within its semiconductor peer group
- Frame as research: "Correlation analysis reveals that NVDA is more closely correlated with [X] (r=[Y]) than with [Z] (r=[W]), suggesting the market views NVDA primarily as a [semiconductor/AI infrastructure] name..."

---

## Phase 6: Initiation Report Summary

### Step 17: Executive Summary — Quantitative Foundation

Do NOT call any tools. This is a pure synthesis step.

Compile the full quantitative case for the NVDA initiation report:

#### NVDA Coverage Initiation — Quantitative Summary

**Price Action (Steps 2–3):**
- 12-month return: [X]%
- 6-month trend: [acceleration/deceleration]
- Current regime: [trending/range-bound/correcting]

**Return Quality (Steps 4–6):**
- Cumulative return: [X]%
- Annualized volatility: [X]% (vs S&P 500 ~15%)
- Sharpe ratio: [X] — [above/below] institutional quality hurdle of 1.0
- Max drawdown: [X]% — worst-case loss for a peak buyer
- Beta: [X] — [high/moderate/low] market sensitivity

**Peer Positioning (Steps 7–14):**
- Risk-adjusted rank within semis: [1st/2nd/etc.] by Sharpe
- Drawdown rank: [best/worst] within peer group
- Performance rank: [1st/2nd/etc.] by 12-month return
- Sector correlation: [high/moderate/low] — [trading with/apart from] semi peers

**Market Positioning (Steps 15–16):**
- vs mega-cap tech: [outperforming/in line/lagging]
- Trading identity: [semiconductor / AI infrastructure / hybrid]
- Most correlated peer: [X] (r=[Y]) — this is the closest substitute

**Bottom Line:**
Summarize the quantitative case in 2-3 sentences. Does the data support a positive, neutral, or cautious initiation stance? What is the single biggest risk? What is the single strongest quantitative signal?

---

#### What an Analyst Would Do Next

This walkthrough produced the quantitative foundation. In a real coverage initiation, the analyst would next:

1. **Build the earnings model** — Link these price/return/risk data points into a 3-statement financial model (Excel)
2. **Set the valuation** — Use EV/EBITDA and P/E multiples from the peer table, apply a premium or discount based on the risk profile, and back into a price target
3. **Draft the report** — The Sharpe/drawdown/beta table goes into "Risk Profile", the normalized performance chart goes into "Relative Performance", and the correlation data supports the "Portfolio Implications" section
4. **Present at morning meeting** — The head of research reviews the quantitative case before the narrative is finalized

The Finance AI Skill replaces the 4-6 hours of Bloomberg/FactSet data pulling, chart building, and metrics calculation that precede the actual analysis.

---

### How This Maps to Traditional Equity Research Tools

| This Walkthrough | Traditional Tool | Time Saved |
|-----------------|------------------|------------|
| analyze_stock (price chart) | Bloomberg `GP` command | Minutes vs manual formatting |
| get_returns (daily/cumulative) | Bloomberg `TRA` screen | Same data, auto-charted |
| get_volatility (rolling vol) | Bloomberg `HVG` function | Auto-computed, no manual formula |
| get_risk_metrics (Sharpe/DD/beta) | FactSet screening + Excel formulas | 3 metrics in 1 call vs 3 separate workflows |
| compare_tickers (normalized perf) | Bloomberg `COMP` or FactSet charting | Auto-normalized, publication-ready |
| correlation_map (return correlation) | Excel CORREL matrix (manual setup) | 5x5 matrix in 1 call vs 25 formulas |

**Total estimated time savings:** 4–6 hours of data gathering and chart construction → ~5 minutes with the Finance AI Skill.

---

Walkthrough complete. Use `/finance-analyst` to run ad-hoc equity research queries, or `/finance` for general analysis.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
