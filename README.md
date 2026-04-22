# Claude Finance

> **The analyst team you always wanted. Available whenever you ask.**

**🔗 Live demo →** https://bolnet.github.io/Claude-Finance/

Claude Finance is an open-source AI skill for Claude Code. Ask Claude institutional-grade questions about any stock, any portfolio, or any market — in plain English. Get charts, risk metrics, ML-powered scoring, and written interpretation in under a minute.

No Python. No tickets. No waiting.

---

## What you get

- **Live portfolio dashboard** — positions, cost basis, allocation donut, day/all-time changes. Live prices via yfinance.
- **11 MCP tools** — `analyze_stock`, `get_returns`, `get_volatility`, `get_risk_metrics`, `compare_tickers`, `correlation_map`, `ingest_csv`, `liquidity_predictor`, `investor_classifier`, `ping`, `validate_environment`
- **18 slash commands** — 3 finance personas + 15 private equity workflows
- **16 skill definitions** — focused reasoning scaffolds that teach Claude the method, the domain, and the expected output shape
- **2 professional personas** — `/finance-analyst` (Sharpe-first, equity research lens) and `/finance-pm` (drawdown-first, portfolio risk lens)
- **6 guided walkthroughs** — Equity Research, Hedge Fund PM, Investment Banking, FP&A, Accounting, Private Equity

## Data layer

Three providers stacked for progressive capability:

| Provider | Status | Purpose |
|---|---|---|
| **yfinance** | ✅ Default | Zero-config price history, returns, risk metrics |
| **Massive** | ✅ Shipped | `DataProvider` Protocol wrapping 57 endpoints — stocks, options + Greeks, forex, crypto, indices, news, SEC filings, technicals, fundamentals, movers, ticker info |
| **Plaid** | 🟡 Roadmap v1.5 | Connect your broker in 20 seconds. Positions + cost basis from Fidelity, Schwab, E*TRADE, Vanguard, Interactive Brokers, Robinhood, and 12,000+ institutions |

Swap providers via the `DATA_PROVIDER` env var — yfinance stays the default, Massive unlocks the rest.

## Install

### 1. MCP Server (recommended)

```bash
git clone https://github.com/bolnet/Claude-Finance.git
cd Claude-Finance
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Claude Code Plugin

```bash
cd Claude-Finance
claude

# All 18 commands auto-discovered
❯ /finance analyze AAPL
```

### 3. Web (claude.ai)

```bash
bash scripts/start_web.sh

# Paste URL in claude.ai → Settings → Connectors → Add
```

## Example

```
❯ /finance-pm check diversification across AAPL, JPM, JNJ, XOM

✓ Retrieved 252 trading days per ticker

  Portfolio Risk Summary (PM Lens)
  ┌──────┬────────┬──────────┬──────┐
  │ AAPL │ 1.42   │ -14.2%   │ 1.12 │
  │ JPM  │ 1.18   │ -9.7%    │ 1.08 │
  │ JNJ  │ 0.64   │ -7.1%    │ 0.55 │
  │ XOM  │ 0.91   │ -11.4%   │ 0.72 │
  └──────┴────────┴──────────┴──────┘

  ✓ Correlation heatmap saved
  ✓ Normalized performance chart saved

Real diversification detected. JNJ (beta 0.55) and XOM (0.72)
provide meaningful downside protection against the tech-heavy
AAPL position. Cross-correlation between JNJ and AAPL is 0.31.
```

## The stack it fits into

Three complementary surfaces for finance professionals:

| Surface | By | Role |
|---|---|---|
| Copilot for Finance | Microsoft | Operational finance — reconciliation, variance analysis, collections |
| Claude in Excel | Anthropic | Model intelligence — formula tracing, scenario testing |
| **Claude Finance** | **Open source** | **Analytical horsepower — Sharpe, beta, ML models, PE workflows** |

## Requirements

- Python 3.10+
- Claude Code CLI *or* claude.ai
- *(Optional)* Plaid API keys — for v1.5 broker sync
- *(Optional)* Massive API keys — to enable the 57 market-data endpoints

## Project stats

- 265 tests passing
- MIT licensed
- 11 MCP tools · 18 slash commands · 16 skill definitions · 15 PE workflows

## About

Built by [Surendra Singh](https://www.linkedin.com/in/surendrasingh/) — 15 years building technology for Wall Street (Merrill Lynch, Fidelity, fintech startups). Now building it *for* the people who run it.

## License

MIT — see [LICENSE](LICENSE).
