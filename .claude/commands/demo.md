---
description: Guided walkthrough of all Finance AI Skill capabilities — 11 tools, 2 personas
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read, mcp__finance__ping, mcp__finance__validate_environment, mcp__finance__analyze_stock, mcp__finance__get_returns, mcp__finance__get_volatility, mcp__finance__get_risk_metrics, mcp__finance__compare_tickers, mcp__finance__correlation_map, mcp__finance__ingest_csv, mcp__finance__liquidity_predictor, mcp__finance__predict_liquidity, mcp__finance__investor_classifier, mcp__finance__classify_investor
model: sonnet
---

## Welcome to the Finance AI Skill Demo

This walkthrough demonstrates all 11 tools of the Finance AI Skill across 3 categories:

- **Environment** (2 tools): health check and package validation
- **Market Analysis** (6 tools): price charts, returns, volatility, risk metrics, ticker comparison, correlation heatmap
- **ML Workflows** (3 tools): CSV ingestion, liquidity risk regression, investor classification

Plus **6 real-world scenarios** showing how equity research analysts, portfolio managers, hedge funds, IB analysts, FP&A teams, and PE firms use these tools in their daily work.

Each step runs a real tool with real data and explains the results in plain English. The walkthrough takes approximately 10–15 minutes and requires no input from you — just sit back and watch.

---

## Environment Context

Python version: !`.venv/bin/python3 --version 2>&1`
Finance packages: !`.venv/bin/python3 -c "import yfinance, pandas, numpy, matplotlib, seaborn, sklearn; print('All OK')" 2>&1`
Working directory: !`pwd`
Output directory status: !`ls finance_output/ 2>/dev/null && echo "exists" || echo "will be created on first run"`

---

## Walkthrough Instructions

You are running a guided demo of the Finance AI Skill. Execute each step below IN ORDER.

After each step:
1. Run the tool or code as instructed
2. Show the result (output, metrics, or chart path)
3. Provide a PLAIN-ENGLISH EXPLANATION of what just happened in 2–3 sentences
4. Print a separator line (`---`)
5. Proceed immediately to the next step

Do NOT ask the user for input between steps — this is a self-running walkthrough.

If any step fails (network error, missing package, missing file), explain the error in plain English and continue to the next step. Never show a raw Python traceback.

---

## Step 1: Environment Check — validate_environment

Call the MCP tool `validate_environment` with no arguments.

After running:
- Report which packages are installed and their versions
- Explain: This tool confirms all required Python packages (yfinance, pandas, numpy, matplotlib, seaborn, scikit-learn) are installed and ready. It is the first thing to run when troubleshooting a setup issue.

---

## Step 2: Health Check — ping

Call the MCP tool `ping` with no arguments.

After running:
- Report the response
- Explain: The ping tool verifies the MCP server is running and responsive. A successful ping confirms the Finance AI Skill backend is connected and available for all subsequent tool calls.

---

## Step 3: Price Chart — analyze_stock

Call the MCP tool `analyze_stock` with:
- ticker: "AAPL"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the output and chart path
- Explain: This fetches 90 days of Apple's real-time stock price data from Yahoo Finance and generates a price chart. The chart shows the closing price over time, making it easy to spot trends, breakouts, and drawdown periods at a glance.

---

## Step 4: Returns Analysis — get_returns

Call the MCP tool `get_returns` with:
- ticker: "AAPL"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the output and chart path
- Explain: Returns show how much a stock gained or lost each day (daily return) and how a hypothetical $1 investment grew over the period (cumulative return). A cumulative return chart makes it easy to compare performance across different stocks or time periods.

---

## Step 5: Volatility — get_volatility

Call the MCP tool `get_volatility` with:
- ticker: "AAPL"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the output and chart path
- Explain: Volatility measures how much a stock's price fluctuates day to day. The 21-day rolling window shows how calm or turbulent the stock was at different points in the period — a spike in the rolling volatility line signals a period of uncertainty or major news.

---

## Step 6: Risk Metrics — get_risk_metrics

Call the MCP tool `get_risk_metrics` with:
- ticker: "AAPL"
- start: [1 year before today, in YYYY-MM-DD format]

After running:
- Show the Sharpe ratio, max drawdown, and beta values
- Explain: The Sharpe ratio measures risk-adjusted return quality — higher is better. Max drawdown is the worst peak-to-trough decline, showing worst-case loss for an investor who bought at the top. Beta measures how sensitive the stock is to S&P 500 moves: a beta above 1 means it amplifies market swings.

---

## Step 7: Ticker Comparison — compare_tickers

Call the MCP tool `compare_tickers` with:
- tickers: "AAPL,MSFT"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the output and chart path
- Explain: The comparison chart normalizes both stocks to a $100 starting value, so you can fairly compare performance regardless of each stock's actual price. This makes it immediately clear which stock outperformed over the period.

---

## Step 8: Correlation Heatmap — correlation_map

Call the MCP tool `correlation_map` with:
- tickers: "AAPL,MSFT,GOOGL"
- start: [90 days before today, in YYYY-MM-DD format]

After running:
- Show the correlation matrix and chart path
- Explain: The correlation heatmap shows how closely the daily returns of these three tech stocks move together, on a scale from -1 (opposite) to +1 (identical). High positive correlations (dark red) mean these stocks tend to rise and fall together — which reduces the diversification benefit of holding all three.

---

## Step 9: CSV Ingestion — ingest_csv

Note: This step requires a sample CSV file at `demo/sample_portfolio.csv`.

If `demo/sample_portfolio.csv` does not exist, skip this step and print:
> "Step 9 (CSV Ingestion) skipped — the sample CSV (demo/sample_portfolio.csv) will be added in a future update. To try ingest_csv now, provide any CSV file path and call the tool with that path."

If the file exists, call the MCP tool `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"

After running (if not skipped):
- Show the column summary, data types, and any cleaning actions taken
- Explain: The CSV ingestion tool automatically detects column types, computes summary statistics, and flags data quality issues (missing values, outliers). This is the first step in any ML workflow — understanding your data before modeling prevents misleading results.

---

## Step 10: ML Regression — liquidity_predictor + predict_liquidity

Note: This step requires `demo/sample_portfolio.csv` (same dependency as Step 9).

If `demo/sample_portfolio.csv` does not exist, skip this step and print:
> "Step 10 (Liquidity Regression) skipped — requires demo/sample_portfolio.csv. This step trains a regression model to predict liquidity risk, then scores a sample client."

If the file exists:

First, call the MCP tool `liquidity_predictor` with:
- csv_path: "demo/sample_portfolio.csv"

Then call the MCP tool `predict_liquidity` with:
- credit_score: 720
- debt_ratio: 0.35
- region: "Northeast"

After running (if not skipped):
- Show R-squared, RMSE, and the prediction result
- Explain: The liquidity predictor trains a regression model on historical client data to estimate liquidity risk scores. R-squared tells you how much of the variance the model explains (closer to 1.0 is better), and RMSE is the average prediction error in the same units as the target. The second call then scores a new hypothetical client using the trained model.

---

## Step 11: ML Classification — investor_classifier + classify_investor

Note: This step requires `demo/sample_portfolio.csv` (same dependency as Steps 9–10).

If `demo/sample_portfolio.csv` does not exist, skip this step and print:
> "Step 11 (Investor Classification) skipped — requires demo/sample_portfolio.csv. This step trains a classification model to segment investors, then classifies a sample investor profile."

If the file exists:

First, call the MCP tool `investor_classifier` with:
- csv_path: "demo/sample_portfolio.csv"

Then call the MCP tool `classify_investor` with:
- age: 42
- income: 120000
- risk_tolerance: 0.5
- product_preference: "equities"

After running (if not skipped):
- Show the accuracy, cross-validation score, and the predicted segment label
- Explain: The investor classifier trains a classification model to assign each client to a segment (e.g., conservative, growth, aggressive) based on profile attributes. Cross-validation gives a realistic accuracy estimate by testing on held-out data. The second call classifies a new investor profile using the trained model.

---

## Step 12: Equity Analyst Framing — get_risk_metrics

Call the MCP tool `get_risk_metrics` with:
- ticker: "AAPL"
- start: [1 year before today, in YYYY-MM-DD format]

After running, explain the results using the equity analyst persona framing:
- Lead with: "From an equity perspective..."
- Emphasize Sharpe ratio first as the primary measure of risk-adjusted return quality
- Then discuss max drawdown as the worst peak-to-trough decline
- Frame beta as sensitivity to market moves
- Express performance relative to S&P 500 benchmark
- Offer context: "An analyst covering AAPL would compare these metrics to sector peers like MSFT and GOOGL"
- End the analyst section with: "That was the equity analyst lens — Sharpe and drawdown first, single-stock focus."

---

## Step 13: Portfolio Manager Framing — same data, different lens

Do NOT call `get_risk_metrics` again — reuse the exact same output from Step 12.

Re-explain the SAME results using the portfolio manager persona framing:
- Lead with: "From a portfolio perspective..."
- Emphasize max drawdown FIRST as the primary risk concern ("what is my worst-case loss on this holding?")
- Then discuss beta as portfolio-level market sensitivity
- Mention Sharpe ratio LAST as a secondary quality check
- Frame AAPL as "a holding in your book" not an individual security
- Add portfolio context: "A PM would next check correlation with other holdings to assess concentration risk"
- End the PM section with: "That was the portfolio manager lens — drawdown and beta first, portfolio holdings focus."

---

## Step 14: Persona Contrast — side-by-side explanation

Do NOT call any tools. This is a pure explanation step.

Print a comparison explaining how the two personas interpreted the SAME data differently:

### How the two personas differ

Both personas used the exact same risk metrics from `get_risk_metrics`. The difference is entirely in framing and priority:

| Aspect | Equity Analyst | Portfolio Manager |
|--------|---------------|-------------------|
| Leads with | Sharpe ratio (return quality) | Max drawdown (worst-case loss) |
| Frames ticker as | Individual security under coverage | A holding in the portfolio book |
| Beta means | Market sensitivity for the stock | Portfolio-level systematic risk |
| Next step | Compare to sector peers | Check correlation with other holdings |

The underlying data is identical — the persona determines which metrics matter most and how they are communicated to the audience.

---

## Real-World Finance Scenarios

The next steps demonstrate how professionals in different finance roles use these same tools in their daily work. Each scenario combines multiple tools into a realistic workflow.

---

## Step 15: Equity Research — Coverage Initiation on NVDA

> *An equity research analyst initiating coverage runs a full diagnostic on a new name before writing a single page of the research note.*

Call the MCP tool `analyze_stock` with:
- ticker: "NVDA"
- start: [180 days before today, in YYYY-MM-DD format]

Then call the MCP tool `get_risk_metrics` with:
- ticker: "NVDA"
- start: [1 year before today, in YYYY-MM-DD format]

Then call the MCP tool `get_returns` with:
- ticker: "NVDA"
- start: [180 days before today, in YYYY-MM-DD format]

After running all three:
- Show the price trend, risk metrics (Sharpe, drawdown, beta), and cumulative return
- Frame this as a coverage initiation: "An analyst starting coverage on NVDA would begin with these three data points..."
- Compare NVDA's beta and Sharpe to AAPL's from Step 6 — note which stock has higher risk-adjusted returns and which amplifies market moves more
- Explain: In equity research, every formula must be auditable and every number sourced. These three tools produce the foundational data that feeds into the analyst's quarterly earnings model and valuation framework.

---

## Step 16: Hedge Fund — Cross-Sector Diversification Check

> *A hedge fund PM checks whether their book is actually diversified or just holds correlated bets disguised as different names. As Nomura's deputy chief digital officer stated: "Python already replaced Excel in banking."*

Call the MCP tool `compare_tickers` with:
- tickers: "AAPL,JPM,JNJ,XOM"
- start: [90 days before today, in YYYY-MM-DD format]

Then call the MCP tool `correlation_map` with:
- tickers: "AAPL,JPM,JNJ,XOM"
- start: [90 days before today, in YYYY-MM-DD format]

After running both:
- Show the normalized performance comparison and correlation matrix
- Frame this as portfolio construction: "A hedge fund PM would read this correlation matrix to determine whether these four holdings provide real diversification..."
- Highlight: which pairs have the lowest correlation (best diversification benefit) and which pairs move most closely together (concentration risk)
- Explain: On a trading desk, this analysis runs on millions of rows in Python. The correlation_map tool does the same math on daily returns — computed on pct_change(), not raw prices, to avoid spurious correlations from shared price trends.

---

## Step 17: FP&A — Data Profiling Before Forecasting

> *An FP&A analyst spends 45% of their time on data collection and validation (2024 FP&A Trends survey). The biggest time-sink: monthly copy-paste from ERP exports. This step shows the automated alternative.*

Call the MCP tool `ingest_csv` with:
- csv_path: "demo/sample_portfolio.csv"
- target_column: "liquidity_risk"

After running:
- Show the column summary, cleaning actions, and EDA chart paths
- Frame this as an FP&A data pipeline: "In an FP&A workflow, this replaces 3-4 hours of manual data profiling..."
- Highlight: the automatic outlier removal (IQR method), the detection of 6 numeric vs 3 categorical columns, and the target column identification — all without configuration
- Explain: FP&A teams using Power Query in Excel do similar cleanup, but Python handles inconsistent formats across multiple regional offices, different date formats, and varying column names — all in one pass. The ingest_csv tool is the first step before any regression or forecasting model.

---

## Step 18: Private Equity — Portfolio Company Risk Scoring

> *A PE firm monitors 10-20 portfolio companies monthly. This step shows how the ML tools score a new deal prospect against the existing portfolio data.*

Call the MCP tool `liquidity_predictor` with:
- csv_path: "demo/sample_portfolio.csv"

Then call the MCP tool `predict_liquidity` with three different client profiles to simulate portfolio company scoring:

First, call `predict_liquidity` with:
- credit_score: 580
- debt_ratio: 0.65
- region: "South"

Then call `predict_liquidity` with:
- credit_score: 750
- debt_ratio: 0.20
- region: "West"

Then call `predict_liquidity` with:
- credit_score: 650
- debt_ratio: 0.50
- region: "Midwest"

After running all four:
- Show R-squared and RMSE from the model, then all three predictions in a comparison table
- Frame this as PE due diligence: "A PE firm evaluating three potential investments would score each against the trained model..."
- Rank the three prospects from lowest to highest risk
- Explain: In private equity, due diligence data rooms can contain hundreds of documents. Python extracts and normalizes the data; the ML model scores it. What took 2 analysts a full week can be completed overnight. The liquidity_predictor trains a fresh model each time, ensuring the scoring reflects the most current portfolio data.

---

## Step 19: Investment Banking — Comparable Company Analysis

> *A first-year IB analyst spends 2,000+ hours annually in Excel building comps. This step shows the Python equivalent: normalized performance comparison and risk profiling across peer companies.*

Call the MCP tool `compare_tickers` with:
- tickers: "AAPL,MSFT,GOOGL,AMZN,META"
- start: [180 days before today, in YYYY-MM-DD format]

Then call the MCP tool `correlation_map` with:
- tickers: "AAPL,MSFT,GOOGL,AMZN,META"
- start: [180 days before today, in YYYY-MM-DD format]

After running both:
- Show the normalized returns ranking (best to worst performer) and the full 5x5 correlation matrix
- Frame this as IB comps: "An investment banking analyst building a comparable company analysis would use this data to..."
- Identify: which mega-cap tech name outperformed, which pairs are most correlated (potential substitutes in a deal), and which name stands apart (differentiated risk profile)
- Explain: In traditional IB, CapIQ and Bloomberg Excel add-ins pull EV/EBITDA and P/E multiples for peer companies. The compare_tickers and correlation_map tools provide the price-performance and co-movement layer that complements those fundamental multiples — answering "how do these stocks actually trade relative to each other?"

---

## Step 20: Role-Tool Mapping — Who Uses What

Do NOT call any tools. This is a pure explanation step.

Print a mapping showing which tools each finance role would use most frequently:

### Finance AI Skill by Role

| Role | Primary Tools | Key Workflow |
|------|--------------|--------------|
| **Equity Research Analyst** | analyze_stock, get_returns, get_risk_metrics | Coverage initiation, quarterly model updates, peer comparison |
| **Portfolio Manager** | get_risk_metrics, compare_tickers, correlation_map | Book risk review, diversification checks, position sizing |
| **Hedge Fund / Trading Desk** | get_volatility, correlation_map, compare_tickers | Vol regime detection, pair trading signals, cross-asset correlation |
| **Investment Banking Analyst** | compare_tickers, correlation_map | Comparable company analysis, relative performance for deal pitches |
| **FP&A Analyst** | ingest_csv, liquidity_predictor | Data profiling, forecasting model inputs, variance analysis prep |
| **Private Equity / VC** | ingest_csv, liquidity_predictor, predict_liquidity, investor_classifier | Due diligence scoring, portfolio company monitoring, LP segment analysis |
| **Accountant / Controller** | ingest_csv | Transaction data profiling, anomaly detection prep, ERP export cleanup |

The winning playbook is AND, not OR — Excel handles the final auditable model that clients open; the Finance AI Skill handles the analysis, scoring, and visualization that feeds into it.

---

## Demo Complete — Summary of All 11 Tools and 2 Personas

You have just seen the full Finance AI Skill in action. Here is a summary of every tool demonstrated:

### Environment (2 tools)

| Tool | What it does |
|------|-------------|
| `validate_environment` | Confirms all required Python packages are installed |
| `ping` | Verifies the MCP server is running and responsive |

### Market Analysis (6 tools)

| Tool | What it does |
|------|-------------|
| `analyze_stock` | Fetches price history and generates a price chart for any ticker |
| `get_returns` | Calculates daily and cumulative returns |
| `get_volatility` | Measures annualized volatility with a rolling window chart |
| `get_risk_metrics` | Computes Sharpe ratio, max drawdown, and beta vs S&P 500 |
| `compare_tickers` | Normalized performance comparison chart for multiple tickers |
| `correlation_map` | Return correlation heatmap showing diversification relationships |

### ML Workflows (3 tools)

| Tool | What it does |
|------|-------------|
| `ingest_csv` | Automatic column detection, summary statistics, and data cleaning |
| `liquidity_predictor` + `predict_liquidity` | Train a regression model on client data, then score new clients for liquidity risk |
| `investor_classifier` + `classify_investor` | Train a classification model, then assign a segment label to a new investor profile |

### Personas (2 modes)

| Persona | Framing |
|---------|---------|
| `/finance-analyst` | Equity analyst lens — Sharpe/drawdown first, single-stock focus |
| `/finance-pm` | Portfolio manager lens — drawdown/beta first, portfolio holdings focus |

---

### Real-World Scenarios (6 roles)

| Step | Role | Tools Used | Workflow |
|------|------|-----------|----------|
| 15 | Equity Research | analyze_stock, get_risk_metrics, get_returns | Coverage initiation on NVDA |
| 16 | Hedge Fund / PM | compare_tickers, correlation_map | Cross-sector diversification check |
| 17 | FP&A Analyst | ingest_csv | Data profiling before forecasting |
| 18 | Private Equity | liquidity_predictor, predict_liquidity | Portfolio company risk scoring |
| 19 | Investment Banking | compare_tickers, correlation_map | Comparable company analysis |
| 20 | All Roles | — | Role-tool mapping reference |

Demo complete. You can now use `/finance` for ad-hoc analysis, or `/finance-analyst` and `/finance-pm` for role-specific framing.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
