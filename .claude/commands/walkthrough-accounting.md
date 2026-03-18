---
description: Accounting walkthrough -- transaction data profiling, segment-based anomaly detection, and ERP consolidation patterns
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read, mcp__finance__ping, mcp__finance__validate_environment, mcp__finance__ingest_csv, mcp__finance__investor_classifier, mcp__finance__classify_investor
model: sonnet
---

## Accounting Walkthrough: Transaction Data Profiling & Anomaly Detection

> *You are a Senior Controller at a regional financial services firm preparing for the quarterly close. The accounting team has exported a client portfolio dataset from the ERP system for consolidation review. Before signing off on the trial balance, you need to profile the transaction data for completeness, identify segment distributions to flag potential misclassifications (anomaly detection), and run a classifier to validate that client segments in the general ledger match expected patterns. The scenario uses the bundled `demo/sample_portfolio.csv`.*

This walkthrough takes approximately 10–15 minutes and runs automatically. Each phase produces data that a real controller would use for audit committee preparation, ERP consolidation review, and quarterly close sign-off.

---

## Walkthrough Instructions

Execute each phase below IN ORDER. After each step:
1. Run the tool or code as instructed
2. Show the result (output, metrics, or data)
3. Provide a PLAIN-ENGLISH EXPLANATION framed as controller commentary — write as if you are drafting notes for the audit committee or documenting findings in the audit trail
4. Print a separator line (`---`)
5. Proceed immediately to the next step

Do NOT ask the user for input between steps. If any step fails, explain the error in plain English and continue.

---

## Phase 1: Pre-Flight Check

### Step 1: Environment Validation

Call `validate_environment` with no arguments.

After running:
- Confirm all packages are ready
- Note: Before the quarterly close, the controller's data audit workflow depends on pandas for ledger data manipulation, scikit-learn for segment classification, and matplotlib for variance visualization. All must be present before the audit begins. A missing package at this stage would halt the ERP data review — the same way a broken data feed would delay the trial balance preparation.

---

## Phase 2: Transaction Data Profiling

> *The first step in any quarterly close is profiling the ERP export. The controller needs to verify: How many records were exported? Are all expected columns present? Are there null values that indicate data feed failures? This is the data completeness check that external auditors will ask about during fieldwork.*

### Step 2: General Ledger Data Completeness Review

Call `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"
- (no target_column — full data profile)

After running:
- Show the column listing, row count, and basic statistics
- Interpret each column in accounting terms:
  - **credit_score** — client creditworthiness; used for accounts receivable provisioning and impairment assessment under CECL/IFRS 9
  - **debt_ratio** — client leverage indicator; maps to balance sheet risk and covenant compliance tracking
  - **region** — consolidation entity; determines which legal entity's general ledger this record belongs to (Northeast, South, West, Midwest divisions)
  - **liquidity_risk** — liquidity classification score; relevant for asset/liability management disclosures
  - **age / income** — demographic fields; used for segment assignment rules in the ERP
  - **risk_tolerance / product_preference** — behavioral fields; drive the segment classification that appears in the general ledger
  - **segment** — the general ledger classification (conservative, moderate, aggressive); this is the field the audit committee will scrutinize for systematic misclassification
- Frame as controller commentary: "The ERP export contains [N] client records across [C] columns. The data completeness rate is [X]% — the percentage of non-null fields across all records. Any null values in region or segment indicate records that cannot be allocated to a consolidation entity or classified in the general ledger, and must be resolved before the trial balance is finalized."
- Note for the audit trail: Document this row count and completeness rate as the starting baseline. External auditors will ask: "How many records did you start with, and how many were included in the trial balance?"

---

### Step 3: Segment Distribution — General Ledger Classification Audit

Call `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"
- target_column: "segment"

After running:
- Show the segment distribution (count and percentage per category)
- Frame as controller commentary: "For anomaly detection, the controller designates the 'segment' column as the classification target. The segment distribution reveals whether client records are properly classified in the general ledger — an uneven distribution (e.g., 90% of records in one segment) suggests systematic misclassification that the audit committee will flag. The expected distribution for a diversified client portfolio typically shows meaningful representation across all three segments (conservative, moderate, aggressive)."
- Interpret the distribution results:
  - How many segments are present (should be 3: conservative, moderate, aggressive)?
  - Is the distribution balanced or skewed?
  - What does the largest segment represent, and does its size make business sense for a diversified financial services client book?
  - Are there any segments with suspiciously low counts that might indicate records were incorrectly swept into other buckets during the ERP migration?
- Frame the implication: "A segment distribution that deviates significantly from business expectations is a red flag for the audit team. In the next phase, we will train a classification model to validate whether these segment assignments match the underlying client financial profiles — any mismatch is a potential misclassification in the general ledger."

---

### Step 4: ERP Data Audit Report

Do NOT call any tools. This is a pure analysis step.

Compile the findings from Steps 2 and 3 into an audit-ready data quality report. Frame this as what the controller would present to the audit committee during the quarterly close review.

#### ERP Export — Data Quality Audit Report

**Data Completeness Summary:**
- Total records exported from ERP: [N from Step 2]
- Total columns: [C from Step 2]
- Overall data completeness rate: [X]%
- Records with no null values (complete records): [N]
- Records requiring remediation before close: [N nulls, if any]

**Column Integrity Assessment:**

| Column | Data Type | Accounting Purpose | Completeness | Audit Risk Level |
|--------|-----------|--------------------|--------------|-----------------|
| credit_score | Numeric | A/R provisioning, CECL impairment | [X]% | [Low/Medium/High] |
| debt_ratio | Numeric | Balance sheet leverage, covenant tracking | [X]% | [Low/Medium/High] |
| region | Categorical | Consolidation entity allocation | [X]% | [High — required for GL posting] |
| liquidity_risk | Numeric | ALM disclosures | [X]% | [Low/Medium/High] |
| age | Numeric | Segment assignment rule input | [X]% | [Low/Medium/High] |
| income | Numeric | Segment assignment rule input | [X]% | [Low/Medium/High] |
| risk_tolerance | Numeric | Segment assignment rule input | [X]% | [Low/Medium/High] |
| product_preference | Categorical | Segment assignment rule input | [X]% | [Low/Medium/High] |
| segment | Categorical | General ledger classification | [X]% | [High — audit target] |

**Segment Distribution Assessment:**
- Segment categories present: [N]
- Largest segment: [name] ([count] records, [X]%)
- Smallest segment: [name] ([count] records, [X]%)
- Distribution assessment: [Balanced / Moderately skewed / Highly skewed]
- Audit risk: [If >70% in one segment: HIGH — systematic misclassification risk. If balanced: LOW — distribution aligns with a diversified portfolio.]

**Red Flags for External Auditor:**
- [List any completeness issues, unusual distributions, or missing segment categories found in Steps 2-3]
- If no issues: "No material data quality exceptions identified. Data is ready for classification validation."

**Controller Sign-Off Note:**
"This data quality assessment serves as the opening record for the quarterly close audit trail. The [N]-record ERP export has been profiled and is proceeding to segment classification validation."

---

## Phase 3: Segment Classification & Anomaly Detection

> *The controller trains a classification model on the ERP export to establish the expected segment pattern. This model learns what a 'correctly classified' record looks like — any record that the model classifies differently from the ledger entry is a potential misclassification (anomaly) that requires investigation before the quarter is certified.*

### Step 5: Train Segment Classification Model

Call `investor_classifier` with:
- csv_path: "demo/sample_portfolio.csv"
- (no target_column — defaults to "segment")

After running:
- Show the model accuracy and feature importances
- Frame as controller commentary: "The controller trains a classification model on the ERP export to establish the expected segment pattern. The model accuracy of [X]% represents the rate at which the ERP's existing segment assignments match what the model predicts based on the underlying client financial profile. This is the baseline accuracy for the anomaly detection workflow."
- Note the feature importances: "The most influential features for segment assignment are [top features]. These are the fields the audit team should scrutinize first if misclassifications are found — if a client's [top feature] does not match the pattern for their assigned segment, that record is the highest-priority item for remediation."

---

### Step 6: Classification Accuracy as Audit Metric

Do NOT call any tools. This is a pure analysis step.

Interpret the model's accuracy and feature importances in controller language.

#### Classification Model Audit Interpretation

**Model Accuracy as Misclassification Rate:**
- Model accuracy: [X]% from Step 5
- Potential misclassification rate: [100 - X]%
- Interpretation: A model accuracy of [X]% means [X]% of records in the ledger match the expected classification pattern based on the client's financial profile. The remaining [100-X]% are potential anomalies — records where the actual segment assignment deviates from what the model predicts. In audit terms, this is the misclassification rate that the external auditor will review.

**Feature Importance — Audit Implications:**

| Feature | Importance | Audit Implication |
|---------|------------|-------------------|
| [Feature 1] | [X]% | [If this field is unreliable, the segment assignment rule is compromised for X% of decisions] |
| [Feature 2] | [X]% | [Secondary driver — validate data quality for this field in the next ERP data feed] |
| [Feature 3] | [X]% | [Tertiary driver — monitor for anomalies in future quarters] |

**What the Audit Committee Should Know:**
- A high-accuracy model ([X]% > 85%) validates that the ERP's segment assignment rules are functioning as designed. The misclassification rate of [100-X]% represents records that warrant spot-checking.
- The feature importances reveal which data fields drive the classification decision. If those fields have data quality issues (null values, outliers, stale data), the segment assignments are unreliable — a finding the audit committee must address before certifying the close.
- In a production audit workflow, the controller would run this model against the full general ledger extract and generate an exception report for all records where the model disagrees with the ledger assignment.

---

### Step 7: Individual Record Validation — Test Case 1 (Expected Conservative Profile)

Call `classify_investor` with:
- age: 55
- income: 180000
- risk_tolerance: 0.43
- product_preference: "equities"

After running:
- Show the classification result and confidence
- Frame as controller commentary: "Test Case 1 — Expected Conservative Profile. The controller tests a client profile that should clearly classify as conservative based on the ERP's segment assignment rules: high income, moderate-low risk tolerance, equities preference. If the model agrees and assigns 'conservative', this validates the classifier — the model has correctly learned the conservative segment pattern. If the model assigns a different segment, this client profile would be flagged as a potential misclassification in the general ledger and sent to the accounting team for manual review."
- Note for the audit trail: Record the classification result and confidence score. In a full quarterly close workflow, this individual record validation would be performed on a sample of records from each segment to confirm the model generalizes correctly.

---

### Step 8: Individual Record Validation — Test Case 2 (Ambiguous Profile)

Call `classify_investor` with:
- age: 28
- income: 63000
- risk_tolerance: 0.19
- product_preference: "equities"

After running:
- Show the classification result and confidence
- Frame as controller commentary: "Test Case 2 — Ambiguous Profile. This client has characteristics that could fall into multiple segments: young age (suggesting aggressive risk appetite), lower income, low risk tolerance (suggesting conservative), but equities product preference. The controller uses ambiguous cases to stress-test the classifier — records like this are most likely to be misclassified in the general ledger because they do not fit cleanly into a single segment bucket. A low confidence score on an ambiguous profile is a signal that the ERP's segment assignment rule needs refinement for edge cases."
- Note: Ambiguous profiles are the audit team's highest-priority items. In a large GL extract, the controller would sort by model confidence and prioritize manual review for the lowest-confidence records.

---

## Phase 4: Consolidation & Audit Synthesis

> *The final phase synthesizes the anomaly detection findings into a quarterly close recommendation. The controller compiles the data completeness assessment, segment classification accuracy, and individual record validation results into a single audit deliverable.*

### Step 9: Individual Record Validation — Test Case 3 (Cross-Check Profile)

Call `classify_investor` with:
- age: 40
- income: 120000
- risk_tolerance: 0.65
- product_preference: "bonds"

After running:
- Show the classification result and confidence
- Frame as controller commentary: "Test Case 3 — Cross-Check Profile. Testing a profile where the product preference (bonds) may conflict with the risk tolerance (moderate-high at 0.65). The controller looks for internal consistency — if the model classifies this record differently than the ledger, it suggests the segment rules need updating for the next consolidation cycle. A bonds-preferring client with high risk tolerance is an internally inconsistent profile, and the model's handling of this case tests whether the ERP's segment assignment logic accounts for conflicting signals."
- Note for the audit trail: Record whether the model confidence is lower for this cross-check profile versus the clear conservative profile in Step 7. Systematically lower confidence on internally inconsistent profiles is evidence that the ERP's segment assignment rules have gaps.

---

### Step 10: Anomaly Detection Summary

Do NOT call any tools. This is a pure analysis step.

Compile the individual record classifications from Steps 7, 8, and 9 into an anomaly detection results table.

#### Anomaly Detection — Individual Record Validation Results

| Test Case | Age | Income | Risk Tolerance | Product Pref | Model Classification | Confidence | Expected | Match/Mismatch |
|-----------|-----|--------|----------------|--------------|----------------------|------------|----------|----------------|
| Conservative Profile (Step 7) | 55 | $180,000 | 0.43 | equities | [Step 7 result] | [X]% | conservative | [Match/Mismatch] |
| Ambiguous Profile (Step 8) | 28 | $63,000 | 0.19 | equities | [Step 8 result] | [X]% | conservative or aggressive | [Match/Mismatch] |
| Cross-Check Profile (Step 9) | 40 | $120,000 | 0.65 | bonds | [Step 9 result] | [X]% | moderate | [Match/Mismatch] |

**Anomaly Rate from Spot Check:**
- Records validated: 3
- Matches (model agrees with expected segment): [N]
- Mismatches (model flags for review): [N]
- Spot-check anomaly rate: [N/3 * 100]%

**Extrapolation to Full GL Extract:**
"In a full production run, the controller would run this classifier against the entire ledger export of [total records from Step 2] records. Based on the model accuracy of [X]% from Step 5, approximately [total * (100-X)/100] records would be flagged as potential misclassifications and added to the exception report for manual review before certifying the quarterly close."

**Audit Committee Talking Points:**
- The segment classification model achieves [X]% accuracy on the ERP training data — this is the internal consistency rate
- [N] of 3 spot-check records aligned with expected segment assignments
- Ambiguous profiles (mixed signals across demographic, financial, and behavioral fields) are the highest-risk records and should receive priority attention during the manual review phase

---

### Step 11: Quarterly Close Recommendation

Do NOT call any tools. This is a pure synthesis step.

Synthesize all findings into the quarterly close recommendation that the controller would present to the CFO and audit committee.

---

#### Quarterly Close — Controller Certification Report

**1. Data Completeness Assessment (Phase 2)**
- ERP export: [N] records, [C] columns
- Completeness rate: [X]%
- Data quality risk level: [Low / Medium / High]
- Action required: [None / Remediate [N] null-value records before close]

**2. Segment Classification Accuracy (Phase 3)**
- Classification model accuracy: [X]%
- Potential misclassification rate: [100-X]%
- Key driver of segment assignment: [top feature from Step 5]
- Classification risk level: [Low (>90% accuracy) / Medium (80-90%) / High (<80%)]
- Action required: [None / Flag [N] low-confidence records for manual review]

**3. Anomaly Detection Findings (Phase 4)**
- Individual records spot-checked: 3
- Anomaly rate from spot check: [N/3 * 100]%
- Most ambiguous profile type: [description from Step 8]
- Anomaly risk level: [Low / Medium / High]

**4. What a Controller Would Do Next**

Before certifying this quarterly close, the controller's action plan is:

1. **Run the classifier against the full GL extract** — Apply the trained model to all [N] records in the ERP export. Generate a ranked exception report: records with model confidence below 70% go to the top of the review queue.

2. **Generate a misclassification exception report** — For every record where model classification differs from the GL segment assignment, create a line item in the exception report with: record ID, current segment, model-predicted segment, confidence score, and the reviewer assignment.

3. **Present findings to the audit committee** — The data completeness rate, classification accuracy, and anomaly rate from this workflow constitute the quantitative basis for the controller's sign-off. The audit committee will ask: "How do you know the segment assignments are correct?" This model provides the answer.

4. **Update segment assignment rules in the ERP** — If the anomaly rate exceeds the materiality threshold (typically 5-10% of records), the root cause is usually outdated segment rules that do not account for new client profiles. Work with the ERP administrator to update the assignment logic before the next quarter.

5. **Schedule pre-close data quality checks** — Implement a standing process to run this data profiling and classification check one week before each quarter-end. Early detection of data feed failures (null values, missing columns) prevents last-minute close delays.

**Controller Sign-Off Status:**
Based on the data completeness rate of [X]% and classification accuracy of [X]%, this dataset [is ready / requires remediation before] quarterly close certification. The misclassification exception report should be reviewed by the senior accountant before the trial balance is finalized.

---

### How This Maps to Traditional Accounting and ERP Tools

| This Walkthrough | Traditional Tool | Time Saved |
|-----------------|------------------|------------|
| `ingest_csv` (data profile) | SAP ABAP data dictionary review / Oracle GL export validation in Excel | Auto-computed column stats, null analysis, and row counts vs manual cell-by-cell review |
| `ingest_csv` (segment distribution) | Pivot table in Excel from GL export / Crystal Reports segment summary | Instant distribution analysis vs manual pivot construction |
| `investor_classifier` (segment model) | Manual segment cross-referencing in Excel / audit sampling by hand | End-to-end classification model trained in 1 call vs days of manual cross-referencing |
| `classify_investor` (record validation) | Individual record spot-checks during substantive testing / manual segment rule lookup | Single-call validation vs manual rule table lookup for each test case |

**Total estimated time savings:** 3–5 hours of manual ERP data extraction, pivot table construction, and segment cross-referencing → ~5 minutes with the Finance AI Skill.

---

Walkthrough complete. Use `/finance` for ad-hoc accounting data analysis, or `/demo` for a guided tour of all Finance AI Skill capabilities.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
