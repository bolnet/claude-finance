---
description: Private equity walkthrough -- due diligence scoring, multi-prospect comparison, and portfolio company monitoring
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read, mcp__finance__ping, mcp__finance__validate_environment, mcp__finance__ingest_csv, mcp__finance__investor_classifier, mcp__finance__classify_investor
model: sonnet
---

## Private Equity Walkthrough: Due Diligence Scoring & Portfolio Monitoring

> *You are a VP at a mid-market PE fund evaluating three acquisition prospects for Fund III. The fund manages a portfolio of existing companies and requires quarterly monitoring. The deal team has exported the firm's prospect database from the CRM into `demo/sample_portfolio.csv`. Your mandate: screen the deal pipeline, train a quantitative scoring model, classify three shortlisted prospects, and prepare the investment committee memo.*
>
> **Scenario:** Fund III has a $400M deployment target. The investment committee meets on Friday. The deal team needs a data-driven ranking of three prospects — a growth equity candidate, a leveraged buyout target, and an early-stage venture play — before the IC deck is finalized.

This walkthrough takes approximately 10–15 minutes and runs automatically. Each phase produces data that a real PE deal team would use for investment committee preparation, LP reporting, and portfolio monitoring dashboards.

---

## Walkthrough Instructions

Execute each phase below IN ORDER. After each step:
1. Run the tool or code as instructed
2. Show the result (output, metrics, or data)
3. Provide a PLAIN-ENGLISH EXPLANATION framed as deal team commentary — write as if you are drafting notes for the investment committee memo or the Monday morning deal review
4. Print a separator line (`---`)
5. Proceed immediately to the next step

Do NOT ask the user for input between steps. If any step fails, explain the error in plain English and continue.

---

## Phase 1: Pre-Flight Check

### Step 1: Environment Validation

Call `validate_environment` with no arguments.

After running:
- Confirm all packages are ready
- Note: Before beginning due diligence, the deal team validates that the analytical environment is ready. A PE fund's quantitative screening depends on pandas for data manipulation, scikit-learn for prospect scoring models, and matplotlib for portfolio reporting. All must be present before the due diligence workflow begins — the same way an IC meeting cannot proceed without a complete data room. A missing package at this stage would halt the deal screening before it starts.

---

## Phase 2: Deal Pipeline Profiling

> *The deal team's first step is profiling the CRM export. How many prospects are in the pipeline? Are all required diligence fields populated? The data completeness check determines whether the pipeline is ready for IC presentation or requires remediation before the scoring model runs.*

### Step 2: CRM Export Review — Full Pipeline Profile

Call `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"
- (no target_column — full data profile)

After running:
- Show the column listing, row count, and basic statistics
- Interpret each column in PE/VC terms:
  - **credit_score** — creditworthiness indicator; used in LBO modeling for debt capacity assessment and credit facility sizing. A prospect's credit score determines how much leverage the fund can put on the business at close.
  - **debt_ratio** — leverage profile; maps directly to LBO model inputs (existing debt load, headroom for additional leverage). A high debt_ratio may indicate a business already capital-constrained or one where the fund can refinance at close.
  - **region** — geographic market exposure; determines which regional portfolio team handles the investment. Northeast and West typically command higher entry multiples; South and Midwest often offer better value/buyout opportunities.
  - **liquidity_risk** — liquidity classification score; indicates how quickly the fund could exit or recapitalize. Higher liquidity risk flags prospects where exit planning needs more runway.
  - **age** — management/company maturity proxy; younger businesses have higher growth potential but less operating history for LBO underwriting.
  - **income** — revenue proxy for target sizing; used for deal sizing and fund fit assessment. The fund's sweet spot for Fund III is $50K–$200K revenue businesses.
  - **risk_tolerance** — management risk appetite indicator; critical for post-close value creation planning. Low risk tolerance management teams are better suited for operational efficiency buyouts; high risk tolerance teams are candidates for aggressive growth equity plans.
  - **product_preference** — capital structure orientation; equities/stocks preference indicates equity-aligned management (suitable for growth equity or minority stake); bonds preference suggests debt-oriented operators (typical of mature buyout candidates).
  - **segment** — current fund allocation bucket from the CRM: conservative = value/buyout candidates, moderate = growth equity candidates, aggressive = venture/high-growth candidates.
- Frame as deal team commentary: "The CRM export contains [N] prospects across [C] diligence fields. The data completeness rate is [X]%. Any null values in region or segment indicate prospects that cannot be allocated to a portfolio team or scored by the IC — these must be resolved before the Monday review."
- Note the row count as: "The Fund III deal pipeline contains [N] prospects at various stages of the screening process."

---

### Step 3: Fund Allocation Analysis — Segment Distribution

Call `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"
- target_column: "segment"

After running:
- Show the segment distribution (count and percentage per category)
- Frame as fund allocation analysis: "The segment distribution reveals how the deal pipeline is distributed across Fund III's three investment strategies. Conservative = value/buyout candidates — mature businesses with predictable cash flows suited for leveraged acquisitions. Moderate = growth equity candidates — established businesses with meaningful upside requiring operational value creation. Aggressive = venture/high-growth candidates — early-stage, capital-intensive businesses requiring minority equity and active board involvement."
- Interpret the distribution results:
  - What does the pipeline composition reveal about the fund's sourcing network? A heavy skew toward one segment suggests the deal sourcing team is overweight in that strategy.
  - Is the pipeline balanced enough to support a diversified Fund III? The fund's LPA typically requires deployment across multiple strategies.
  - Which segment represents the largest deal opportunity by count?
  - Are there any segments with suspiciously low counts that might indicate sourcing gaps the fund needs to address before the next fundraise?
- Frame the pipeline assessment: "A balanced pipeline indicates diversified deal sourcing; heavy skew toward one segment suggests the fund's sourcing network is biased toward that strategy. The IC will want to see whether the pipeline composition aligns with the Fund III mandate."

---

### Step 4: Deal Pipeline Summary Report

Do NOT call any tools. This is a pure analysis step.

Compile the findings from Steps 2 and 3 into a PE-framed data quality report. Frame this as what the deal team would present at the Monday morning investment committee meeting before the IC deck is reviewed.

#### Fund III Deal Pipeline — Monday IC Briefing

**Pipeline Size:**
- Total prospects in CRM export: [N from Step 2]
- Total diligence fields captured: [C from Step 2]
- Data completeness rate: [X]%
- Prospects with complete diligence packages (no null values): [N]
- Prospects requiring additional diligence before scoring: [N nulls, if any]

**Data Completeness Assessment:**

| Field | PE/VC Purpose | Completeness | Screening Risk |
|-------|--------------|--------------|----------------|
| credit_score | Debt capacity / LBO leverage sizing | [X]% | [Low/Medium/High] |
| debt_ratio | Existing leverage / refinancing headroom | [X]% | [Low/Medium/High] |
| region | Portfolio team allocation | [X]% | [High — required for deal assignment] |
| liquidity_risk | Exit planning / recapitalization timeline | [X]% | [Low/Medium/High] |
| age | Growth stage / operating history | [X]% | [Low/Medium/High] |
| income | Deal sizing / fund fit | [X]% | [Low/Medium/High] |
| risk_tolerance | Value creation plan compatibility | [X]% | [Low/Medium/High] |
| product_preference | Capital structure alignment | [X]% | [Low/Medium/High] |
| segment | IC strategy classification | [X]% | [High — required for IC presentation] |

**Strategy Distribution Assessment:**
- Strategy buckets present: [N]
- Largest segment: [name] ([count] prospects, [X]%)
- Smallest segment: [name] ([count] prospects, [X]%)
- Pipeline balance: [Balanced / Moderately skewed / Heavily skewed toward one strategy]
- Sourcing assessment: [Assessment based on the distribution]

**IC Recommendation:**
- [If balanced]: "Pipeline composition supports diversified Fund III deployment. Proceed to quantitative scoring."
- [If skewed]: "Pipeline is overweight [segment] strategy. Flag to sourcing team for rebalancing before next LP update."

**Deal Team Sign-Off:**
"This pipeline assessment serves as the opening record for Fund III's Q1 deal review. The [N]-prospect CRM export has been profiled and is proceeding to the due diligence scoring model."

---

## Phase 3: Due Diligence Scoring Model

> *The deal team trains a classification model on the historical prospect database to establish a quantitative scoring baseline. This model learns the fund's historical investment decision pattern — the features that most reliably predict how a prospect should be classified. Feature importances become the due diligence priority framework: the team focuses their fieldwork on the fields the model cares about most.*

### Step 5: Train Prospect Scoring Model

Call `investor_classifier` with:
- csv_path: "demo/sample_portfolio.csv"
- (no target_column — defaults to "segment")

After running:
- Show the model accuracy and feature importances
- Frame as deal team commentary: "The deal team trains a classification model on the Fund III historical prospect database to establish a quantitative scoring baseline. Model accuracy represents the consistency of historical IC allocation decisions — a high accuracy means the fund's investment committee has been consistent in how it categorizes prospects over time. A low accuracy would indicate that allocation decisions have been subjective or inconsistent, which is a fund governance concern. Feature importances reveal which prospect characteristics most influence the allocation decision — these are the fields the deal team should scrutinize first during due diligence fieldwork."
- Map accuracy to IC confidence: "Model accuracy of [X]% means that [X]% of the time, a prospect's financial and behavioral profile alone correctly predicts which investment strategy the IC assigned. This is the fund's scoring model reliability rating."

---

### Step 6: Feature Importance as Due Diligence Priorities

Do NOT call any tools. This is a pure analysis step.

Interpret the feature importances from Step 5 as due diligence priorities. The most important features are the fields the deal team should scrutinize first during prospect evaluation. Frame this in PE language.

#### Due Diligence Priority Framework — Derived from Scoring Model

**Feature Importance Rankings:**

| Priority | Feature | Importance | Due Diligence Question | Why It Matters |
|----------|---------|------------|----------------------|----------------|
| #1 | [Top feature] | [X]% | [PE-framed due diligence question for this feature] | [Why this field drives IC allocation decisions] |
| #2 | [Feature 2] | [X]% | [PE-framed due diligence question] | [Why this field is secondary driver] |
| #3 | [Feature 3] | [X]% | [PE-framed due diligence question] | [Why this field is tertiary driver] |
| #4 | [Feature 4] | [X]% | [PE-framed due diligence question] | [Lower priority validation field] |
| #5+ | [Remaining features] | [X]% | [Supporting diligence questions] | [Context fields] |

**Example interpretations by feature:**
- If **risk_tolerance** is the top feature: "The deal team's primary due diligence question for every prospect is: What is management's appetite for operational transformation? A management team with low risk tolerance will resist post-close restructuring — this determines whether the fund can execute its value creation plan."
- If **income** is the top feature: "Deal sizing drives IC allocation more than any other factor. The fund's primary screening question is: Does this prospect's revenue base support a control acquisition at Fund III's target check size?"
- If **age** is the top feature: "Company maturity is the primary IC differentiator. The deal team's first question is: Is this business far enough along in its development to support the fund's value creation timeline and expected exit horizon?"
- If **credit_score** is the top feature: "Creditworthiness drives allocation more than any other factor — this directly determines LBO leverage capacity. The deal team's first question is: Can this business support the debt load required for a leveraged buyout?"

**Implication for Fund III Diligence Process:**
"Based on the scoring model, the Fund III due diligence checklist should be reordered to front-load [top 2-3 features] in the diligence workflow. Spending time on low-importance features early in the process is inefficient — the model says these fields barely influence the IC's allocation decision."

---

### Step 7: Prospect A — Growth Equity Profile

Call `classify_investor` with:
- age: 42
- income: 145000
- risk_tolerance: 0.55
- product_preference: "equities"

After running:
- Show the classification result and confidence score
- Frame as deal team commentary: "Prospect A is a mid-career executive leading a $145K revenue business with moderate risk appetite and equity-oriented capital structure. This is the fund's initial growth equity hypothesis for the deal pipeline."
- Interpret the result in PE terms:
  - If classified **moderate** (growth equity): "Textbook growth equity candidate — established business with revenue in the fund's sweet spot, moderate risk tolerance indicating management openness to operational change, and equity-aligned capital structure. The [X]% confidence score indicates this is a clean fit for the growth equity thesis. The deal team should proceed to financial model construction."
  - If classified **conservative** (buyout/value): "The scoring model reclassifies Prospect A as a value/buyout candidate rather than growth equity. At $145K revenue and moderate risk tolerance, the model sees a more mature, stability-oriented profile than the deal team initially assumed. The deal team should pressure-test the growth equity thesis with the management team before presenting to IC."
  - If classified **aggressive** (venture/high-growth): "Surprising classification — the model sees venture-like characteristics in this profile despite the mature revenue base. High confidence here would suggest the management team's risk tolerance is the dominant signal. Verify whether this is a true high-growth operator or a misclassification driven by the equity product preference."
- Note for IC: "Prospect A's confidence score of [X]% indicates how cleanly this profile fits the [segment] archetype. Scores above 75% indicate high-conviction IC recommendations; scores below 60% warrant additional due diligence before presenting."

---

### Step 8: Prospect B — Buyout/Value Profile

Call `classify_investor` with:
- age: 58
- income: 190000
- risk_tolerance: 0.25
- product_preference: "bonds"

After running:
- Show the classification result and confidence score
- Frame as deal team commentary: "Prospect B is a seasoned operator running a $190K revenue business with low risk appetite and debt-oriented capital structure. This profile maps to a classic leveraged buyout candidate — stable cash flows, risk-averse management, and a capital structure orientation consistent with taking on acquisition financing. The deal team expects a conservative/buyout classification."
- Interpret the result in PE terms:
  - If classified **conservative** (buyout/value): "The model confirms the buyout thesis with [X]% confidence. This prospect's profile — high revenue, low risk tolerance, bonds preference — cleanly fits the value/buyout archetype. A high-confidence conservative classification is the strongest signal in the pipeline for a leveraged buyout. The deal team should begin LBO model construction using the credit_score for debt capacity sizing."
  - If classified **moderate** (growth equity): "Unexpected growth equity classification. Despite low risk tolerance and bond preference, the high revenue base ($190K) may be pulling the model toward a growth equity classification. The deal team should investigate whether this operator has been misclassified by the CRM or whether there is growth upside the static profile does not capture."
  - If classified **aggressive** (venture): "The model disagrees strongly with the buyout thesis. A low-confidence aggressive classification on this profile is a red flag — the underlying features are inconsistent. Flag this prospect for additional management interviews before IC."
- Note for IC: "Prospect B's confidence score of [X]% is the key metric. A buyout recommendation to IC with confidence below 65% is not well-supported by the data — the deal team needs qualitative justification for proceeding."

---

### Step 9: Prospect C — Venture/High-Growth Profile

Call `classify_investor` with:
- age: 26
- income: 72000
- risk_tolerance: 0.88
- product_preference: "stocks"

After running:
- Show the classification result and confidence score
- Frame as deal team commentary: "Prospect C is an early-stage operator with a $72K revenue business, very high risk appetite, and equity-oriented structure. This profile maps to a venture/high-growth candidate — limited operating history, management team with high risk tolerance indicating willingness to execute an aggressive growth plan, and equity-aligned capital structure. The deal team expects an aggressive/venture classification."
- Interpret the result in PE terms:
  - If classified **aggressive** (venture/high-growth): "Model confirms the venture thesis with [X]% confidence. This is the fund's highest-risk, highest-potential-return prospect in the pipeline. At $72K revenue with 0.88 risk tolerance, this operator will accept aggressive post-close targets. The deal team should structure this as a minority equity investment with clear milestone-based follow-on provisions rather than a control buyout — the business is too early-stage for full control acquisition."
  - If classified **moderate** (growth equity): "The model tempers the venture thesis — this prospect may be more developed than the CRM data suggests. A moderate classification at 0.88 risk tolerance indicates the revenue base and age factors are pulling toward a more established profile. The deal team should verify revenue quality (recurring vs. one-time) before finalizing the investment strategy."
  - If classified **conservative** (buyout): "Unexpected conservative classification for a high-risk-tolerance early-stage operator. Very low confidence on this classification would indicate the model is uncertain — this prospect may not fit cleanly into any of the fund's three investment archetypes and may require a bespoke deal structure."
- Note for IC: "Prospect C's confidence score of [X]% matters most here. Venture classifications with high confidence (>70%) support minority equity structuring; low confidence (<55%) suggests this prospect is an outlier that doesn't fit the fund's standard investment frameworks."

---

## Phase 4: Portfolio Monitoring & Investment Committee Report

> *The final phase synthesizes all quantitative findings into the deliverables the IC requires: a side-by-side prospect comparison matrix and a portfolio monitoring dashboard. The deal team also reinterprets the three prospect classifications as portfolio company health signals, demonstrating how the scoring model serves double duty — screening new deals AND monitoring existing holdings.*

### Step 10: Multi-Prospect Deal Screening Matrix

Do NOT call any tools. This is a pure analysis step.

Build a side-by-side comparison table of Prospects A, B, and C using the classifications from Steps 7–9. This is the deal screening matrix the investment committee reviews before voting on which prospects advance to Term Sheet stage.

#### Fund III — Deal Screening Matrix (IC Presentation)

| Attribute | Prospect A | Prospect B | Prospect C |
|-----------|-----------|-----------|-----------|
| **Profile** | Mid-career operator | Seasoned operator | Early-stage operator |
| **Age** | 42 | 58 | 26 |
| **Revenue (Income)** | $145,000 | $190,000 | $72,000 |
| **Risk Appetite** | Moderate (0.55) | Low (0.25) | Very High (0.88) |
| **Capital Structure** | Equity-oriented | Debt-oriented | Equity-oriented |
| **Model Classification** | [Step 7 result] | [Step 8 result] | [Step 9 result] |
| **Confidence Score** | [Step 7 %] | [Step 8 %] | [Step 9 %] |
| **Recommended Strategy** | [Growth equity / Buyout / Venture based on Step 7] | [Growth equity / Buyout / Venture based on Step 8] | [Growth equity / Buyout / Venture based on Step 9] |
| **Investment Thesis** | [1-sentence thesis for Prospect A] | [1-sentence thesis for Prospect B] | [1-sentence thesis for Prospect C] |

**Ranking by Model Confidence (Highest = Strongest IC Conviction):**
1. [Prospect with highest confidence] — [X]% — Strongest fit for [strategy] strategy
2. [Prospect with middle confidence] — [X]% — [Assessment]
3. [Prospect with lowest confidence] — [X]% — Requires additional due diligence

**Weakest Fit Analysis:**
"[Lowest-confidence prospect] has the weakest quantitative support for its investment thesis at [X]% confidence. The deal team recommends [specific additional due diligence step — management interviews, financial model stress test, or customer reference checks] before advancing this prospect to Term Sheet."

**IC Vote Recommendation:**
- Advance to Term Sheet: [Highest-confidence prospect] — quantitative support is strong
- Conditional advance: [Middle-confidence prospect] — proceed subject to [specific condition]
- Hold for additional diligence: [Lowest-confidence prospect] — confidence below threshold for IC approval

---

### Step 11: Portfolio Company Monitoring Dashboard

Do NOT call any tools. This is a pure analysis step.

Reinterpret the three classify_investor results as existing portfolio companies rather than acquisition prospects. For existing portfolio companies, the classifier confidence score serves as a portfolio health indicator. A company originally acquired as a 'growth equity' play whose profile now scores with low confidence for that segment is showing drift — the operating characteristics have changed, and the fund should reassess the value creation plan.

#### Fund III — Quarterly Portfolio Monitoring Dashboard

| Company | Original Thesis | Original Strategy | Current Classification | Current Confidence | Drift Signal | Recommended Action |
|---------|----------------|-------------------|----------------------|-------------------|--------------|-------------------|
| Portfolio Co A (age=42, income=$145K) | Growth equity — operational value creation | Moderate | [Step 7 result] | [Step 7 %] | [Yes if confidence <65% / No if ≥65%] | [Action based on drift] |
| Portfolio Co B (age=58, income=$190K) | Leveraged buyout — cash flow optimization | Conservative | [Step 8 result] | [Step 8 %] | [Yes if confidence <65% / No if ≥65%] | [Action based on drift] |
| Portfolio Co C (age=26, income=$72K) | Venture — high-growth minority equity | Aggressive | [Step 9 result] | [Step 9 %] | [Yes if confidence <65% / No if ≥65%] | [Action based on drift] |

**Drift Signal Interpretation:**
- **No Drift (confidence ≥ 65%):** Portfolio company is performing within its original investment thesis. Value creation plan is on track. Continue monitoring at standard quarterly cadence.
- **Drift Detected (confidence < 65%):** Portfolio company's operating profile has shifted away from the original thesis. The fund should convene an extraordinary board meeting to reassess the value creation plan, consider a strategy pivot (e.g., repositioning from growth equity to buyout), or evaluate whether the fund's ownership structure is still appropriate.

**Quarterly Monitoring Summary:**
- Companies with no drift: [N] — standard quarterly review
- Companies showing drift: [N] — board-level review recommended
- Most critical monitoring alert: [Company showing most drift, if any]

**LP Reporting Note:**
"For the quarterly LP update, portfolio companies showing drift should be flagged in the 'Portfolio Health' section with a brief explanation of the operating changes detected. LPs will ask about any company whose strategy classification has changed since acquisition — the fund should be prepared to explain the value creation plan update."

---

### Step 12: Investment Committee Memo

Do NOT call any tools. This is a pure synthesis step.

Synthesize all findings into the IC memo the deal team presents on Friday. This is the quantitative backbone of the IC presentation — the data that supports or challenges each investment recommendation.

---

#### Fund III Investment Committee Memo

**Prepared by:** Deal Team / Quantitative Screening
**Meeting:** Friday IC Session
**Subject:** Fund III Q1 Prospect Screening Results and Portfolio Monitoring Update

---

**1. Deal Pipeline Health (Phase 2)**

- Pipeline size: [N] prospects in CRM export across [C] diligence fields
- Data completeness: [X]% — [data quality assessment from Step 4]
- Strategy distribution: [summary from Step 3] — [balanced/skewed assessment]
- Sourcing assessment: [summary of whether pipeline composition aligns with Fund III mandate]

---

**2. Scoring Model Reliability (Phase 3)**

- Training data: [N]-prospect historical CRM database
- Model accuracy: [X]% — [interpret as "fund's IC decisions have been [X]% consistent with prospect profiles"]
- Top due diligence driver: [Feature #1 from Step 6] — [PE interpretation of why this field dominates]
- Secondary driver: [Feature #2 from Step 6]
- Model reliability rating: [High (>85%) / Medium (75–85%) / Low (<75%)] — [implication for IC confidence]

---

**3. Prospect Screening Results (Phase 3)**

| Prospect | Classification | Confidence | IC Recommendation |
|----------|---------------|------------|-------------------|
| Prospect A ($145K revenue, moderate risk) | [Step 7] | [%] | [Advance / Conditional / Hold] |
| Prospect B ($190K revenue, low risk) | [Step 8] | [%] | [Advance / Conditional / Hold] |
| Prospect C ($72K revenue, high risk) | [Step 9] | [%] | [Advance / Conditional / Hold] |

---

**4. Portfolio Monitoring Alerts (Phase 4)**

- Portfolio companies reviewed: 3
- Companies showing classification drift: [N from Step 11]
- [If drift detected]: "[Company name] is showing drift from its original [strategy] thesis. Board review recommended before next LP update."
- [If no drift]: "All portfolio companies are performing within their original investment thesis. No extraordinary board sessions required this quarter."

---

**5. Recommended Actions (Prioritized)**

1. **Advance [highest-confidence prospect] to Term Sheet** — [X]% model confidence supports [strategy] thesis. Assign deal lead to begin financial model construction.
2. **Conditional advance for [middle-confidence prospect]** — [Specific condition] required before IC approval. [Timeframe] to resolve.
3. **Hold [lowest-confidence prospect] for additional diligence** — [X]% confidence is below the fund's [Y]% IC approval threshold. Assign to sourcing team for [specific diligence action].
4. **[If portfolio drift detected]: Convene extraordinary board meeting for [drifting company]** — operating profile has shifted from original [strategy] thesis.
5. **Update sourcing strategy** — [If pipeline is skewed, recommend corrective action to rebalance pipeline toward underweight strategies].

---

**Bottom Line:**
"Based on the scoring model's [X]% accuracy and the prospect classifications, the deal team recommends [advancing/tabling/declining] each prospect as outlined above. Portfolio monitoring identifies [N] companies [showing classification drift that warrant board-level review / performing within original thesis with no extraordinary action required]. The quantitative screening confirms [summary of overall pipeline quality and IC readiness]."

---

#### What a PE Fund Would Do Next

This walkthrough produced the quantitative foundation for the IC meeting. In a real Fund III deal process, the deal team would next:

1. **Build the financial model** — For each prospect advancing to Term Sheet, construct a 3-statement financial model (income statement, balance sheet, cash flow) plus an LBO model using credit_score for debt capacity sizing and income as the revenue proxy.

2. **Prepare the management presentation** — The deal team schedules management meetings with each shortlisted prospect. The scoring model's top features become the structured interview agenda — if risk_tolerance is the #1 feature, the first management meeting question is: "Walk us through how you approach operational risk."

3. **Draft the Term Sheet** — For the highest-confidence prospect, the deal team drafts a non-binding letter of intent (LOI) with proposed valuation range, deal structure (control vs. minority), and key conditions to closing.

4. **Update the quarterly board deck for portfolio drift companies** — For any portfolio company showing classification drift, the deal team prepares a one-pager for the LP quarterly update explaining the operating changes and revised value creation plan.

5. **Commission management background checks** — The deal team engages a third-party due diligence firm for reference checks on the management teams of prospects advancing to Term Sheet stage. The scoring model cannot capture character or operational track record — those require qualitative investigation.

---

### How This Maps to Traditional PE Due Diligence Tools

| This Walkthrough | Traditional Tool | Time Saved |
|-----------------|------------------|------------|
| `ingest_csv` (pipeline profile) | PitchBook / Preqin CRM export review in Excel — manual column mapping, null count formulas, and pivot tables for completeness assessment | Auto-computed column stats, completeness rates, and distribution analysis vs. manual cell-by-cell review |
| `ingest_csv` (segment distribution) | Manual pivot table from CRM export / Crystal Reports strategy summary for LP reporting | Instant strategy distribution vs. manual pivot construction and formatting |
| `investor_classifier` (scoring model) | Manual deal scoring rubric in Excel — each prospect rated by hand across 8–12 criteria by the deal team | End-to-end classification model trained in 1 call vs. days of manual scoring sheet construction and calibration |
| `classify_investor` (prospect scoring) | IC scoring card — individual manual evaluation of each prospect's fit across criteria, then committee discussion | Single-call scoring with confidence score vs. subjective multi-person rubric scoring |
| Multi-prospect comparison matrix | Side-by-side Excel comps with manual scoring — one column per prospect, scores entered by hand | Automated side-by-side comparison derived directly from model outputs |
| Portfolio monitoring dashboard | Quarterly portfolio review deck built manually in Excel/PowerPoint — each company's metrics updated by hand | Classification-based drift detection derived automatically from the scoring model |

**Total estimated time savings:** 4–8 hours of CRM export review, manual deal scoring, IC deck preparation, and portfolio monitoring → ~10 minutes with the Finance AI Skill.

---

Walkthrough complete. Use `/finance` for ad-hoc analysis.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
