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

Each step runs a real tool with real data and explains the results in plain English. The walkthrough takes approximately 5–10 minutes and requires no input from you — just sit back and watch.

---

## Environment Context

Python version: !`python3 --version 2>&1`
Finance packages: !`python3 -c "import yfinance, pandas, numpy, matplotlib, seaborn, sklearn; print('All OK')" 2>&1`
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
- risk_tolerance: "moderate"
- product_preference: "equities"

After running (if not skipped):
- Show the accuracy, cross-validation score, and the predicted segment label
- Explain: The investor classifier trains a classification model to assign each client to a segment (e.g., conservative, growth, aggressive) based on profile attributes. Cross-validation gives a realistic accuracy estimate by testing on held-out data. The second call classifies a new investor profile using the trained model.

---

## Persona Showcase

The Finance AI Skill also includes two persona modes that frame the same underlying analysis differently, depending on your role:

- **/finance-analyst** — Equity analyst lens. Leads with Sharpe ratio and drawdown versus the S&P 500. Useful for single-stock coverage research, earnings context, and client-facing reports.

- **/finance-pm** — Portfolio manager lens. Leads with drawdown and beta before Sharpe ratio, and treats tickers as portfolio holdings rather than individual securities. Useful for risk management, allocation decisions, and portfolio review.

To try a persona, type `/finance-analyst` or `/finance-pm` followed by your analysis request (e.g., `/finance-analyst Show me AAPL risk metrics for 2024`).

---

## Demo Complete — Summary of All 11 Tools

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

---

Demo complete. You can now use `/finance` for ad-hoc analysis, or `/finance-analyst` and `/finance-pm` for role-specific framing.

> For educational/informational purposes only. Not financial advice. Past results do not guarantee future performance.
