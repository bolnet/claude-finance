# Claude Finance — Getting Started Guide

**Version 1.4.0** | **License: MIT** | **Python 3.10+**

Institutional-grade financial analytics in plain English. Built by a Wall Street engineer with 15 years of experience, Claude Finance gives equity analysts, portfolio managers, hedge funds, IB analysts, FP&A teams, and PE firms access to real-time market data, risk scoring, and ML workflows — without writing a single line of code.

---

## Table of Contents

1. [What You Get](#what-you-get)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
   - [Method 1: MCP Server (Claude Code CLI)](#method-1-mcp-server-claude-code-cli)
   - [Method 2: Claude Code Plugin](#method-2-claude-code-plugin)
   - [Method 3: Web Connection (claude.ai)](#method-3-web-connection-claudeai)
   - [Method 4: Marketplace (Coming Soon)](#method-4-marketplace)
4. [Verify Your Setup](#verify-your-setup)
5. [All 11 Tools](#all-11-tools)
6. [All 18 Slash Commands](#all-18-slash-commands)
7. [Personas](#personas)
8. [Real-World Workflows by Role](#real-world-workflows-by-role)
9. [Sample Data](#sample-data)
10. [Project Structure](#project-structure)
11. [Troubleshooting](#troubleshooting)
12. [Disclaimer](#disclaimer)

---

## What You Get

### 11 MCP Tools

| Category | Tools | What They Do |
|----------|-------|--------------|
| **Environment** (2) | `validate_environment`, `ping` | Health check, package validation |
| **Market Analysis** (6) | `analyze_stock`, `get_returns`, `get_volatility`, `get_risk_metrics`, `compare_tickers`, `correlation_map` | Price charts, daily/cumulative returns, rolling volatility, Sharpe/drawdown/beta, normalized peer comparison, correlation heatmaps |
| **ML Workflows** (3) | `ingest_csv`, `liquidity_predictor` + `predict_liquidity`, `investor_classifier` + `classify_investor` | Auto data profiling, regression risk scoring, classification segmentation |

### 18 Slash Commands

3 finance persona commands + 15 private equity workflow commands. See [full list below](#all-18-slash-commands).

### 2 Personas

- `/finance-analyst` — Equity analyst lens (Sharpe first, single-stock focus)
- `/finance-pm` — Portfolio manager lens (drawdown first, portfolio-level risk)

### 6 Role-Based Walkthroughs

Equity Research, Hedge Fund PM, Investment Banking, FP&A, Accounting, Private Equity.

---

## Prerequisites

- **Python 3.10+**
- **Claude Code CLI** (for MCP/Plugin methods) or **claude.ai account** (for web method)
- **Internet connection** (Yahoo Finance data fetching)

---

## Installation

### Method 1: MCP Server (Claude Code CLI)

This is the primary method. The MCP server runs locally via stdio and Claude Code communicates with it directly.

**Step 1: Clone the repository**

```bash
git clone https://github.com/bolnet/Claude-Finance.git
cd Claude-Finance
```

**Step 2: Create a virtual environment and install dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

This installs all required packages:

| Package | Version | Purpose |
|---------|---------|---------|
| fastmcp | >= 2.0 | MCP server framework |
| yfinance | >= 0.2.40 | Yahoo Finance market data |
| pandas | >= 2.2.0 | Data manipulation |
| numpy | >= 1.26.0 | Numerical computing |
| matplotlib | >= 3.8.0 | Chart generation |
| seaborn | >= 0.13.0 | Heatmap visualization |
| scikit-learn | >= 1.4.0 | ML models (regression, classification) |
| tabulate | >= 0.9.0 | Table formatting |

**Step 3: Configure the MCP server**

Create or edit `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "finance": {
      "command": "/absolute/path/to/Claude-Finance/.venv/bin/python",
      "args": ["-m", "finance_mcp.server"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "/absolute/path/to/Claude-Finance/src"
      }
    }
  }
}
```

Replace `/absolute/path/to/Claude-Finance` with the actual path where you cloned the repo.

**Step 4: Start Claude Code from the project directory**

```bash
cd Claude-Finance
claude
```

Claude Code automatically reads `.mcp.json` and launches the finance MCP server. You should see the finance tools available immediately.

**Step 5: Verify**

```
> /finance validate my environment
```

You should see all packages listed with their versions and an "OK" status.

---

### Method 2: Claude Code Plugin

The plugin method bundles the MCP server with slash commands and skills so Claude Code can discover them as a package.

**Step 1: Clone the repository**

```bash
git clone https://github.com/bolnet/Claude-Finance.git
cd Claude-Finance
```

**Step 2: Install Python dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Step 3: Register the plugin**

The plugin lives in `finance-mcp-plugin/`. Its structure:

```
finance-mcp-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, description)
├── .mcp.json                # MCP server config for the plugin
├── hooks/
│   └── hooks.json           # Event hooks (extensible)
├── commands/                 # 18 slash commands
│   ├── finance.md
│   ├── finance-analyst.md
│   ├── finance-pm.md
│   ├── ai-readiness.md
│   ├── dd-checklist.md
│   └── ... (15 more PE commands)
└── skills/                   # 16 detailed skill definitions
    ├── finance/
    │   └── SKILL.md
    └── private-equity/
        ├── liquidity-risk/SKILL.md
        ├── deal-sourcing/SKILL.md
        └── ... (13 more PE skills)
```

**Plugin manifest** (`finance-mcp-plugin/.claude-plugin/plugin.json`):

```json
{
  "name": "finance-mcp",
  "version": "1.4.0",
  "description": "Private Equity plugin for Claude Code — deal flow, portfolio monitoring, and ML-powered analytics for PE professionals.",
  "homepage": "https://github.com/bolnet/Claude-Finance",
  "repository": "https://github.com/bolnet/Claude-Finance",
  "license": "MIT",
  "keywords": ["finance", "stocks", "yfinance", "ml", "market-analysis", "portfolio", "mcp", "private-equity"]
}
```

Claude Code discovers the plugin when you open the project directory. All 18 slash commands and 11 MCP tools become available.

**Step 4: Start Claude Code**

```bash
cd Claude-Finance
claude
```

**Step 5: Test a slash command**

```
> /finance analyze AAPL over the last 90 days
> /finance-analyst initiate coverage on NVDA
> /finance-pm check my portfolio diversification: AAPL, MSFT, GOOGL
```

---

### Method 3: Web Connection (claude.ai)

Connect the finance server to claude.ai via an HTTP tunnel so you can use the tools from the browser — no CLI required.

**Prerequisites:**
- [ngrok](https://ngrok.com/download) installed (`brew install ngrok` on macOS)
- OR [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) for a persistent URL

**Step 1: Clone and install** (same as Method 1, Steps 1-2)

```bash
git clone https://github.com/bolnet/Claude-Finance.git
cd Claude-Finance
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Step 2: Start the HTTP server + tunnel**

```bash
bash scripts/start_web.sh
```

This script:
1. Starts the Finance MCP HTTP server on port 8000
2. Opens an ngrok tunnel to expose it publicly
3. Prints the public URL

You will see output like:

```
============================================
  Connect claude.ai to:
  https://abc123.ngrok-free.app/mcp

  Steps:
  1. Go to claude.ai
  2. Click Settings (top-right) > Connectors
  3. Click 'Add custom connector'
  4. Paste: https://abc123.ngrok-free.app/mcp
  5. Click Add
  6. In a new chat, click '+' > Connectors > toggle Finance MCP on
============================================
```

**Step 3: Connect in claude.ai**

1. Open [claude.ai](https://claude.ai)
2. Go to **Settings** > **Connectors**
3. Click **Add custom connector**
4. Paste the URL from the terminal output (e.g., `https://abc123.ngrok-free.app/mcp`)
5. Click **Add**
6. Start a new chat, click the **+** button > **Connectors** > toggle **Finance MCP** on

You can now use all 11 tools directly from claude.ai.

**Note:** The ngrok free tier generates a new URL on each restart. For a persistent URL, use Cloudflare Tunnel:

```bash
cloudflared tunnel --url http://localhost:8000
```

**Step 4: Use custom port** (optional)

```bash
bash scripts/start_web.sh 9090
```

---

### Method 4: Marketplace

Marketplace distribution is planned for a future release. The plugin manifest and landing page (`docs/index.html`) are already in place for submission.

When available, installation will be:
1. Search "Claude Finance" in the Claude Code marketplace
2. Click Install
3. All tools and commands activate automatically

---

## Verify Your Setup

Regardless of which method you chose, run these two checks:

### 1. Ping the server

Ask Claude: `ping the finance server`

Expected: `Finance MCP Server is running. Ready to execute finance analysis.`

### 2. Validate the environment

Ask Claude: `validate my finance environment`

Expected: All 7 packages listed with version numbers and `_status: OK`.

| Package | Expected |
|---------|----------|
| yfinance | version number |
| pandas | version number |
| numpy | version number |
| matplotlib | version number |
| seaborn | version number |
| sklearn | version number |
| tabulate | version number |

If any package shows `MISSING`, run:

```bash
source .venv/bin/activate
pip install -e .
```

---

## All 11 Tools

### Environment Tools

| Tool | Description | Example Prompt |
|------|-------------|----------------|
| `ping` | Confirm the MCP server is running | "Ping the finance server" |
| `validate_environment` | Check all required packages are installed | "Validate my finance environment" |

### Market Analysis Tools

| Tool | Parameters | Description | Example Prompt |
|------|-----------|-------------|----------------|
| `analyze_stock` | `ticker`, `start`, `end?` | Price chart with trend summary | "Show me AAPL's price chart for the last 6 months" |
| `get_returns` | `ticker`, `start`, `end?` | Daily + cumulative return charts | "What are NVDA's returns since January?" |
| `get_volatility` | `ticker`, `start`, `end?` | Annualized + 21-day rolling volatility | "How volatile has TSLA been over the past quarter?" |
| `get_risk_metrics` | `ticker`, `start`, `end?` | Sharpe ratio, max drawdown, beta vs S&P 500 | "Get risk metrics for GOOGL over the last year" |
| `compare_tickers` | `tickers` (2-5), `start`, `end?` | Normalized performance comparison chart | "Compare AAPL, MSFT, and GOOGL over 90 days" |
| `correlation_map` | `tickers` (2-10), `start`, `end?` | Return correlation heatmap | "Show correlation between AAPL, JPM, JNJ, and XOM" |

### ML Workflow Tools

| Tool | Parameters | Description | Example Prompt |
|------|-----------|-------------|----------------|
| `ingest_csv` | `csv_path`, `target_column?` | Auto-profile CSV: column detection, outlier removal, EDA charts | "Profile the file demo/sample_portfolio.csv" |
| `liquidity_predictor` | `csv_path`, `target_column?` | Train regression model for liquidity risk | "Train a liquidity model on demo/sample_portfolio.csv" |
| `predict_liquidity` | `credit_score`, `debt_ratio`, `region` | Score a client using the trained model | "Predict liquidity risk: credit 720, debt ratio 0.35, Northeast" |
| `investor_classifier` | `csv_path`, `target_column?` | Train RandomForest classifier for investor segments | "Train an investor classifier on demo/sample_portfolio.csv" |
| `classify_investor` | `age`, `income`, `risk_tolerance`, `product_preference` | Classify a new investor profile | "Classify: age 42, income 120k, risk tolerance 0.5, equities" |

---

## All 18 Slash Commands

### Finance Personas (3)

| Command | Description |
|---------|-------------|
| `/finance` | General-purpose financial analysis — routes to any of the 11 tools based on your request |
| `/finance-analyst` | Equity analyst persona — leads with Sharpe ratio, frames stocks as securities under coverage, compares to sector peers |
| `/finance-pm` | Portfolio manager persona — leads with max drawdown, frames stocks as portfolio holdings, checks concentration risk |

### Private Equity Commands (15)

| Command | Workflow |
|---------|----------|
| `/ai-readiness` | Assess portfolio company AI readiness with go/wait gates |
| `/dd-checklist` | Generate sector-tailored due diligence checklist |
| `/dd-prep` | Prepare for DD meetings with targeted questions and red flags |
| `/ic-memo` | Draft structured Investment Committee memo |
| `/liquidity-risk` | Train regression model, predict liquidity risk scores |
| `/market-risk` | Scan market risk using Sharpe, drawdown, and beta |
| `/portfolio` | Track portfolio KPIs, generate quarterly dashboards |
| `/profile-pipeline` | Profile CRM CSV with full exploratory data analysis |
| `/public-comps` | Compare public market comps with normalized charts |
| `/returns` | Analyze IRR/MOIC returns with sensitivity tables |
| `/score-prospect` | Train ML classifier, score deal prospects with confidence |
| `/screen-deal` | Screen deal against fund criteria |
| `/source` | Source PE deal targets by investment criteria |
| `/unit-economics` | Analyze ARR cohorts, LTV/CAC, net retention |
| `/value-creation` | Build EBITDA bridges, 100-day value creation plans |

---

## Personas

Claude Finance supports two professional personas that interpret the same data differently:

### Equity Analyst (`/finance-analyst`)

| Aspect | Behavior |
|--------|----------|
| Leads with | Sharpe ratio (risk-adjusted return quality) |
| Frames ticker as | Individual security under research coverage |
| Beta means | Stock-level market sensitivity |
| Next step | Compare to sector peers (MSFT, GOOGL, etc.) |
| Audience | Buy-side/sell-side research consumers |

**Example:**
```
> /finance-analyst analyze NVDA's risk profile over the last year
```

### Portfolio Manager (`/finance-pm`)

| Aspect | Behavior |
|--------|----------|
| Leads with | Max drawdown (worst-case portfolio loss) |
| Frames ticker as | A holding in the portfolio book |
| Beta means | Portfolio-level systematic risk exposure |
| Next step | Check correlation with other holdings |
| Audience | Internal risk committee, LP reporting |

**Example:**
```
> /finance-pm review risk on my holdings: AAPL, NVDA, JPM
```

Both personas use the same underlying tools and data — the difference is entirely in framing, priority, and audience.

---

## Real-World Workflows by Role

| Role | Primary Tools | Typical Workflow |
|------|--------------|------------------|
| **Equity Research Analyst** | `analyze_stock`, `get_returns`, `get_risk_metrics` | Coverage initiation, quarterly model updates, peer comparison |
| **Portfolio Manager** | `get_risk_metrics`, `compare_tickers`, `correlation_map` | Book risk review, diversification checks, position sizing |
| **Hedge Fund / Trading Desk** | `get_volatility`, `correlation_map`, `compare_tickers` | Vol regime detection, pair trading signals, cross-asset correlation |
| **Investment Banking Analyst** | `compare_tickers`, `correlation_map` | Comparable company analysis, relative performance for deal pitches |
| **FP&A Analyst** | `ingest_csv`, `liquidity_predictor` | Data profiling, forecasting model inputs, variance analysis prep |
| **Private Equity / VC** | `ingest_csv`, `liquidity_predictor`, `predict_liquidity`, `investor_classifier` | Due diligence scoring, portfolio company monitoring, LP segmentation |
| **Accountant / Controller** | `ingest_csv` | Transaction data profiling, anomaly detection prep, ERP export cleanup |

### Example Workflows

**Equity Research — Coverage Initiation:**
```
> /finance-analyst initiate coverage on NVDA
```
This runs `analyze_stock` (6-month price chart), `get_risk_metrics` (Sharpe, drawdown, beta), and `get_returns` (cumulative performance) — the three data points that feed into every research note.

**Hedge Fund — Diversification Audit:**
```
> /finance-pm check diversification across AAPL, JPM, JNJ, XOM
```
This runs `compare_tickers` (normalized performance) and `correlation_map` (return co-movement) to show whether the book has real diversification or just correlated bets in different names.

**Private Equity — Prospect Scoring:**
```
> /liquidity-risk train a model on demo/sample_portfolio.csv then score three prospects
```
This trains a regression model, then scores each prospect with a risk rating (LOW / MODERATE / HIGH) for the investment committee.

---

## Sample Data

A sample portfolio CSV is included at `demo/sample_portfolio.csv` for testing the ML tools:

- **100 rows** of synthetic client data
- **9 columns:** credit_score, debt_ratio, liquidity_risk, age, income, risk_tolerance, region, product_preference, segment
- **6 numeric + 3 categorical** columns
- Used by `ingest_csv`, `liquidity_predictor`, and `investor_classifier`

To test with your own data, provide any CSV file path:

```
> Profile the file /path/to/your/data.csv
> Train a liquidity model on /path/to/your/portfolio.csv
```

---

## Project Structure

```
Claude-Finance/
├── .mcp.json                        # MCP server config (Claude Code)
├── pyproject.toml                   # Package metadata & dependencies
├── requirements.txt                 # Dependency list
├── scripts/
│   └── start_web.sh                 # HTTP server + ngrok launcher (claude.ai)
├── demo/
│   └── sample_portfolio.csv         # Sample data for ML tools
├── docs/
│   └── index.html                   # Landing page & documentation
├── src/finance_mcp/
│   ├── server.py                    # MCP server (stdio transport)
│   ├── server_http.py               # HTTP server (web transport)
│   ├── adapter.py                   # yfinance wrapper (single data source)
│   ├── output.py                    # Chart saving, output formatting
│   ├── validators.py                # DataFrame validation
│   └── tools/
│       ├── price_chart.py           # analyze_stock
│       ├── returns.py               # get_returns
│       ├── volatility.py            # get_volatility
│       ├── risk_metrics.py          # get_risk_metrics
│       ├── comparison.py            # compare_tickers
│       ├── correlation.py           # correlation_map
│       ├── csv_ingest.py            # ingest_csv
│       ├── liquidity_model.py       # liquidity_predictor + predict_liquidity
│       └── investor_model.py        # investor_classifier + classify_investor
├── finance-mcp-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json              # Plugin manifest
│   ├── .mcp.json                    # Plugin MCP config
│   ├── commands/                    # 18 slash commands (.md files)
│   └── skills/                      # 16 skill definitions
│       ├── finance/SKILL.md
│       └── private-equity/          # 15 PE skill directories
├── tests/                           # 265 tests across 26 files
└── finance_output/                  # Generated outputs
    ├── charts/                      # PNG chart files
    └── models/                      # Persisted ML models (.joblib)
```

---

## Troubleshooting

### "Module not found" errors

Your virtual environment is not activated or dependencies are missing:

```bash
cd Claude-Finance
source .venv/bin/activate
pip install -e .
```

### MCP server not connecting

1. Verify `.mcp.json` uses **absolute paths** (not relative)
2. Check that the `.venv/bin/python` path exists
3. Ensure `PYTHONPATH` points to the `src/` directory
4. Restart Claude Code after editing `.mcp.json`

### No data returned for a ticker

- Verify the ticker symbol is valid on Yahoo Finance (e.g., `AAPL`, not `Apple`)
- Check your internet connection
- yfinance may rate-limit after many rapid requests — wait a few seconds and retry

### Charts not generating

- Matplotlib requires the `Agg` backend for headless operation (already configured)
- Check that `finance_output/charts/` directory exists and is writable
- The tools create this directory automatically on first run

### ngrok tunnel not working (web method)

- Ensure ngrok is installed: `ngrok --version`
- Free tier URLs change on restart — re-paste the new URL in claude.ai
- For persistent URLs, use Cloudflare Tunnel instead:
  ```bash
  cloudflared tunnel --url http://localhost:8000
  ```

### Plugin commands not appearing

- Claude Code must be started from the project root directory
- Verify `finance-mcp-plugin/.claude-plugin/plugin.json` exists
- Restart Claude Code: type `/exit` then relaunch

---

## Disclaimer

For educational and informational purposes only. Not financial advice. Past results do not guarantee future performance.

---

*Built by Surendra Singh — 15 years on Wall Street, from Morgan Stanley to Goldman Sachs to building the tools that should have existed all along.*
