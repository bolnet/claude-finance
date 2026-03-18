# Phase 2: Market Analysis Tools - Research

**Researched:** 2026-03-17
**Domain:** Python financial metrics (pandas/numpy), matplotlib/seaborn charting, FastMCP tool registration, yfinance multi-ticker
**Confidence:** HIGH

---

## Summary

Phase 2 builds seven MCP tools on top of the Phase 1 infrastructure. The data layer (yfinance adapter, output conventions, FastMCP server) is already production-ready. This phase's entire work lives inside `src/finance_mcp/` — specifically: adding a `tools/` sub-package with one module per plan, and registering the new tools in `server.py` via `mcp.add_tool()`.

All financial metric calculations (returns, volatility, Sharpe, drawdown, beta, correlation) are expressible in pure pandas/numpy with no extra libraries. The Phase 1 codebase already has the correct dependencies installed: pandas, numpy, matplotlib, seaborn. No new package installs are needed for Phase 2.

The single biggest pitfall in this phase is plot state leakage: any chart function that does not call `plt.close(fig)` after saving will accumulate figures in memory and potentially bleed styling across calls. The `save_chart()` function in `output.py` already calls `plt.close(fig)` — all chart code must use it exclusively, never call `fig.savefig()` directly.

**Primary recommendation:** Implement each MKTX requirement as a focused pure-function tool module under `src/finance_mcp/tools/`, import and register in `server.py` using `mcp.add_tool()`. Keep business logic (calculations + charting) out of server.py entirely.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| MKTX-01 | User can request stock price chart for any ticker and date range in plain English; chart saved as PNG | `fetch_price_history` + `get_adjusted_prices` already handle data; chart is `ax.plot(prices)` + `save_chart()` |
| MKTX-02 | User can get daily and cumulative returns for a ticker, displayed as table and chart | `prices.pct_change()` for daily, `.add(1).cumprod().sub(1)` for cumulative; two-subplot figure |
| MKTX-03 | User can get annualized volatility and rolling volatility chart for a ticker | `returns.std() * np.sqrt(252)` for point-in-time; `returns.rolling(21).std() * np.sqrt(252)` for chart |
| MKTX-04 | User can get Sharpe ratio, max drawdown, and beta vs S&P 500 | All three computable in pure pandas/numpy; S&P 500 fetched as `^GSPC` via existing adapter |
| MKTX-05 | User can compare 2–5 tickers side-by-side on a normalized price performance chart | `fetch_multi_ticker` already exists; normalize with `prices / prices.iloc[0] * 100` |
| MKTX-06 | User can get correlation heatmap between a set of tickers | `pd.DataFrame(prices_dict).corr()` + `sns.heatmap(annot=True, fmt=".2f", cmap="coolwarm")` |
| MKTX-07 | All market analysis outputs include plain-English summary with benchmark context | `format_output()` enforces ordering; interpretation templates are in SKILL.md |
</phase_requirements>

---

## Standard Stack

### Core (already installed — no new installs needed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pandas | >=2.0 | Returns, rolling stats, correlation matrix, reindexing | All date-aligned operations; `.pct_change()`, `.rolling()`, `.corr()` |
| numpy | >=1.24 | `np.sqrt(252)`, `np.cov`, scalar math | Annualization factor, beta covariance formula |
| matplotlib | >=3.7 | Price charts, returns chart, rolling vol chart | Already set up with Agg backend in output.py |
| seaborn | >=0.13 | Correlation heatmap | `sns.heatmap` with `annot=True` is the standard for annotated correlation matrices |
| yfinance | >=0.2.54 | All market data (single and multi-ticker) | Already wrapped in adapter.py — use only through adapter |

### No New Packages

All Phase 2 requirements are covered by packages installed in Phase 1. Do not add `quantstats`, `empyrical`, or `mplfinance` — hand-rolling the five formulas (returns, volatility, Sharpe, drawdown, beta) in pandas/numpy is ~20 lines total and removes dependency risk.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pandas/numpy for metrics | quantstats / empyrical | Those libraries add significant install weight; pandas covers all v1 needs |
| seaborn heatmap | plotly heatmap | seaborn is already installed; plotly adds JS dependency |
| mplfinance | plain matplotlib | mplfinance is good for OHLC candles but unnecessary for line-only price charts |

**Installation:**
```bash
# No new installs for Phase 2 — all dependencies already in .venv
```

---

## Architecture Patterns

### Recommended Module Structure

```
src/finance_mcp/
├── adapter.py          # Phase 1 — yfinance isolation (DO NOT TOUCH)
├── validators.py       # Phase 1 — DataFrame validation (DO NOT TOUCH)
├── output.py           # Phase 1 — save_chart, format_output, DISCLAIMER (DO NOT TOUCH)
├── check_env.py        # Phase 1 — environment checker (DO NOT TOUCH)
├── server.py           # Phase 1 — FastMCP server; ADD mcp.add_tool() calls here
└── tools/              # NEW in Phase 2 — one module per plan
    ├── __init__.py
    ├── price_chart.py      # MKTX-01: analyze_stock tool
    ├── returns.py          # MKTX-02: get_returns tool
    ├── volatility.py       # MKTX-03: get_volatility tool
    ├── risk_metrics.py     # MKTX-04: get_risk_metrics tool
    ├── comparison.py       # MKTX-05: compare_tickers tool
    └── correlation.py      # MKTX-06: correlation_map tool
```

Each `tools/*.py` module exports exactly one function that becomes one MCP tool.

### Pattern 1: Tool Module Structure

**What:** One file = one MCP tool function. File contains: imports, the public function (with full docstring), and private helper functions prefixed with `_`.

**When to use:** Every Phase 2 tool.

```python
# src/finance_mcp/tools/price_chart.py
# Source: FastMCP docs — https://gofastmcp.com/servers/tools
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "src")  # not needed when installed as package
from finance_mcp.adapter import fetch_price_history, get_adjusted_prices, DataFetchError
from finance_mcp.output import save_chart, format_output
from fastmcp.exceptions import ToolError


def analyze_stock(ticker: str, start: str, end: str = "") -> str:
    """
    Generate a price chart for a single stock ticker over the given date range.

    Args:
        ticker: Yahoo Finance ticker symbol, e.g. "AAPL"
        start: Start date in ISO format "YYYY-MM-DD"
        end: End date in ISO format "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output string with plain-English summary, chart path, and disclaimer.
    """
    try:
        df = fetch_price_history(ticker, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    prices = get_adjusted_prices(df)
    # ... chart and interpret
```

### Pattern 2: Tool Registration in server.py

**What:** Import tool functions from the tools/ sub-package and register via `mcp.add_tool()`. Never define tool logic inline in server.py.

```python
# server.py addition — register all Phase 2 tools
from finance_mcp.tools.price_chart import analyze_stock
from finance_mcp.tools.returns import get_returns
from finance_mcp.tools.volatility import get_volatility
from finance_mcp.tools.risk_metrics import get_risk_metrics
from finance_mcp.tools.comparison import compare_tickers
from finance_mcp.tools.correlation import correlation_map

mcp.add_tool(analyze_stock)
mcp.add_tool(get_returns)
mcp.add_tool(get_volatility)
mcp.add_tool(get_risk_metrics)
mcp.add_tool(compare_tickers)
mcp.add_tool(correlation_map)
```

### Pattern 3: Financial Metric Formulas (verified, pure pandas/numpy)

**Daily returns:**
```python
# Source: pandas docs — pct_change()
daily_returns = prices.pct_change().dropna()
```

**Cumulative returns:**
```python
# (1 + r1)(1 + r2)... - 1
cumulative = (1 + daily_returns).cumprod() - 1
```

**Annualized volatility:**
```python
# 252 trading days per year — industry standard
annualized_vol = daily_returns.std() * np.sqrt(252)

# Rolling 21-day (monthly) window
rolling_vol = daily_returns.rolling(21).std() * np.sqrt(252)
```

**Sharpe ratio (assume risk-free rate = 0 for simplicity, or pass as parameter):**
```python
# Annualized Sharpe = (mean daily return / daily std) * sqrt(252)
# Risk-free rate adjustment: subtract rf/252 from each daily return
sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
```

**Maximum drawdown:**
```python
# Cumulative wealth index, then rolling peak, then drawdown series
wealth = (1 + daily_returns).cumprod()
rolling_peak = wealth.cummax()
drawdown_series = (wealth - rolling_peak) / rolling_peak
max_drawdown = drawdown_series.min()  # negative number, e.g. -0.34
```

**Beta vs benchmark (e.g. ^GSPC):**
```python
# Beta = Cov(stock, benchmark) / Var(benchmark)
aligned = pd.concat([daily_returns, benchmark_returns], axis=1).dropna()
cov_matrix = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
beta = cov_matrix[0, 1] / cov_matrix[1, 1]
```

**Normalized price for multi-ticker chart:**
```python
# Base 100 normalization — each series starts at 100
normalized = prices_df / prices_df.iloc[0] * 100
```

**Correlation matrix + heatmap:**
```python
import seaborn as sns
corr = prices_df.corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, center=0, ax=ax)
ax.set_title("Price Return Correlation Matrix")
```

### Anti-Patterns to Avoid

- **Calling `fig.savefig()` directly:** Always use `save_chart(fig, filename)` from output.py — it handles `plt.close(fig)` and the correct output directory.
- **Importing yfinance directly in tool modules:** All data access must go through `adapter.py`.
- **Putting tool logic in server.py:** server.py is wiring only; all computation lives in `tools/`.
- **Using `plt.show()`:** Banned. No display in headless MCP server context.
- **Forgetting `.dropna()` after `pct_change()`:** First row is always NaN; all metric calculations must drop it.
- **Referencing `df['Adj Close']`:** Does not exist in yfinance 0.2.54+. Use `get_adjusted_prices(df)`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Annotated correlation matrix viz | Custom grid of text + colors | `seaborn.heatmap(annot=True)` | Handles colormap normalization, cell sizing, value formatting |
| Rolling stats | Manual loop over window slices | `pandas.Series.rolling().std()` | Vectorized, handles edge cases, respects minimum periods |
| Date alignment for multi-ticker | Manual merge loops | `pd.concat([...], axis=1)` or `pd.DataFrame(dict)` | Auto-aligns by DatetimeIndex; drops dates where any ticker is missing |
| Figure memory cleanup | `del fig` | `plt.close(fig)` (already in `save_chart`) | pyplot keeps internal figure registry; `del` doesn't release it |

**Key insight:** Every financial metric needed for MKTX-01 through MKTX-07 is a 1-3 line pandas/numpy expression. The complexity is in the output formatting and plain-English interpretation, not the math.

---

## Common Pitfalls

### Pitfall 1: Beta Calculation Requires Benchmark Date Alignment

**What goes wrong:** Fetching AAPL and ^GSPC independently and then computing covariance on mismatched lengths (different holidays, different fetch windows).

**Why it happens:** `pd.concat` aligns by index, but if one series has extra rows (e.g., a dividend adjustment date appearing differently), the shapes diverge before `dropna()`.

**How to avoid:** Always fetch both series with the same `start`/`end`, then `pd.concat([stock_returns, bench_returns], axis=1).dropna()` before `np.cov()`. The `.dropna()` removes any rows where either series has NaN.

**Warning signs:** `np.cov` result is `nan`; beta is `nan` or `inf`.

### Pitfall 2: Sharpe Ratio Sign Convention

**What goes wrong:** Returning a positive Sharpe for a negative-return period, or vice versa.

**Why it happens:** If `daily_returns.mean()` is negative and `daily_returns.std()` is positive, the ratio is negative — correct. But some implementations divide by absolute std or use `abs()`. Don't.

**How to avoid:** `sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)`. No `abs()`. Return the raw signed value and let the plain-English interpretation explain what it means.

### Pitfall 3: Correlation on Price Levels vs Returns

**What goes wrong:** Computing `prices_df.corr()` on raw price levels instead of returns. Price levels are non-stationary and almost always produce spuriously high correlations (~0.9+) even for unrelated assets.

**Why it happens:** Using `prices_df.corr()` directly instead of `prices_df.pct_change().dropna().corr()`.

**How to avoid:** For MKTX-06, always compute correlation on daily returns, not price levels. The plain-English interpretation should note this ("correlation of daily returns").

### Pitfall 4: Multi-Ticker DataFrame Shape When One Ticker Has Less History

**What goes wrong:** `fetch_multi_ticker` returns series of different lengths (e.g., a recently-listed stock has fewer rows than SPY). `pd.DataFrame(prices_dict)` fills missing dates with NaN, which then propagates through normalization and correlation.

**Why it happens:** New or delisted tickers have shorter histories than benchmark periods.

**How to avoid:** After `pd.DataFrame(prices_dict)`, call `.dropna()` to restrict to the common date range, then normalize. Document the truncation in the plain-English output ("Comparison uses the common date range: YYYY-MM-DD to YYYY-MM-DD").

### Pitfall 5: Rolling Volatility Chart Has Leading NaN Gap

**What goes wrong:** First 20 data points of rolling vol are NaN (window not yet full), causing a gap at the left edge of the chart that looks like a bug.

**Why it happens:** `rolling(21).std()` requires 21 observations before returning a value.

**How to avoid:** Use `min_periods=1` if a shorter initial window is acceptable, OR simply let the NaN gap exist and note in the plain-English output "Rolling volatility shown from 21 days into the period." The gap is technically correct behavior.

### Pitfall 6: ToolError Import Path (Critical — Phase 1 Learnt)

**What goes wrong:** `ImportError: cannot import name 'ToolError' from 'fastmcp'`

**Why it happens:** In fastmcp 3.x, ToolError moved to `fastmcp.exceptions`.

**How to avoid:** Every tool module must use `from fastmcp.exceptions import ToolError`. Never `from fastmcp import ToolError`.

---

## Code Examples

### Price Chart (MKTX-01)

```python
# Standard price chart pattern
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(prices.index, prices.values, linewidth=1.5, color="#1f77b4")
ax.set_title(f"{ticker} Adjusted Close Price")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.grid(True, alpha=0.3)
fig.tight_layout()
path = save_chart(fig, f"{ticker.lower()}_price_{start}_{end}.png")
```

### Returns Table + Chart (MKTX-02)

```python
# Two-subplot figure: daily returns bar + cumulative line
daily = prices.pct_change().dropna()
cumulative = (1 + daily).cumprod() - 1

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
ax1.bar(daily.index, daily.values * 100, color=["#d62728" if r < 0 else "#2ca02c" for r in daily], width=0.8)
ax1.set_ylabel("Daily Return (%)")
ax2.plot(cumulative.index, cumulative.values * 100, linewidth=1.5)
ax2.set_ylabel("Cumulative Return (%)")
ax2.set_xlabel("Date")
fig.suptitle(f"{ticker} Returns")
fig.tight_layout()
path = save_chart(fig, f"{ticker.lower()}_returns_{start}.png")
```

### Sharpe + Drawdown + Beta (MKTX-04)

```python
import numpy as np

def compute_risk_metrics(returns: pd.Series, benchmark_returns: pd.Series) -> dict:
    """Pure computation — no side effects, no I/O."""
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    wealth = (1 + returns).cumprod()
    max_drawdown = ((wealth - wealth.cummax()) / wealth.cummax()).min()

    aligned = pd.concat([returns, benchmark_returns], axis=1).dropna()
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    beta = cov[0, 1] / cov[1, 1]

    return {"sharpe": sharpe, "max_drawdown": max_drawdown, "beta": beta}
```

### Correlation Heatmap (MKTX-06)

```python
import seaborn as sns

# Source: https://seaborn.pydata.org/generated/seaborn.heatmap.html
prices_df = pd.DataFrame(prices_dict)
returns_df = prices_df.pct_change().dropna()  # correlation on RETURNS not price levels
corr = returns_df.corr()

fig, ax = plt.subplots(figsize=(max(6, len(tickers) * 1.5), max(5, len(tickers) * 1.2)))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0,
    square=True,
    linewidths=0.5,
    ax=ax,
)
ax.set_title("Return Correlation Matrix")
fig.tight_layout()
path = save_chart(fig, "correlation_heatmap.png")
```

### Plain-English Interpretation Templates

```python
# Sharpe
if metrics["sharpe"] > 1.0:
    sharpe_text = f"high risk-adjusted returns (Sharpe ratio {metrics['sharpe']:.2f} > 1.0)"
elif metrics["sharpe"] > 0:
    sharpe_text = f"moderate risk-adjusted returns (Sharpe ratio {metrics['sharpe']:.2f})"
else:
    sharpe_text = f"negative risk-adjusted returns (Sharpe ratio {metrics['sharpe']:.2f})"

# Max drawdown
drawdown_pct = abs(metrics["max_drawdown"]) * 100
drawdown_text = f"a maximum drawdown of {drawdown_pct:.1f}% — meaning an investor at the peak would have seen their position fall {drawdown_pct:.1f}% before recovering"

# Beta
beta_val = metrics["beta"]
if beta_val > 1.2:
    beta_text = f"a beta of {beta_val:.2f}, indicating higher volatility than the S&P 500"
elif beta_val > 0.8:
    beta_text = f"a beta of {beta_val:.2f}, moving roughly in line with the S&P 500"
else:
    beta_text = f"a beta of {beta_val:.2f}, indicating lower sensitivity to S&P 500 moves"
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `df['Adj Close']` | `df['Close']` (auto_adjust=True) | yfinance 0.2.54 | KeyError if old approach used |
| `@mcp.tool` decorator | `mcp.add_tool(fn)` for imported functions | fastmcp 3.x | Enables tool-in-module pattern |
| `from fastmcp import ToolError` | `from fastmcp.exceptions import ToolError` | fastmcp 3.x | ImportError if old path used |
| Inline `python3 -c` execution | Write-then-execute (last_run.py) | Project decision Phase 1 | Non-negotiable; all scripts written to disk first |

**Deprecated/outdated:**
- `plt.show()`: Banned across the entire project. Use `save_chart()` from output.py.
- Direct `fig.savefig()` calls: Bypasses output directory convention and skips `plt.close(fig)`.
- `setuptools.backends.legacy:build`: Removed in current setuptools; already using `setuptools.build_meta`.

---

## Open Questions

1. **Seaborn version compatibility with Agg backend**
   - What we know: seaborn 0.13+ builds on matplotlib and inherits the Agg backend when set before pyplot import.
   - What's unclear: Whether `import seaborn as sns` at module level (after `output.py` sets Agg) triggers any pyplot import internally.
   - Recommendation: Import seaborn inside the `correlation_map` tool function, after `from finance_mcp.output import ...` has already run. This ensures Agg is always set before seaborn's internal matplotlib usage.

2. **Figure sizing for variable-length ticker lists (MKTX-06)**
   - What we know: A 2-ticker heatmap looks very different from a 5-ticker heatmap at fixed figure size.
   - What's unclear: Optimal formula for dynamic figure sizing.
   - Recommendation: `figsize=(max(6, n * 1.5), max(5, n * 1.2))` where `n = len(tickers)`. This is LOW confidence (empirical guess); validate during implementation.

3. **Risk-free rate assumption for Sharpe ratio**
   - What we know: A true Sharpe adjusts for the current risk-free rate (e.g., US T-bill yield). That requires a FRED or another API call.
   - What's unclear: Whether to use 0 (simpler) or a hard-coded approximate value (e.g., 0.05 / 252 daily).
   - Recommendation: Use `rf=0` for MKTX-04 and note the assumption in the plain-English output. This is consistent with the scope defined in REQUIREMENTS.md (FRED integration is a v2 feature).

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | `pyproject.toml` (already configured) |
| Quick run command | `.venv/bin/python3 -m pytest tests/test_market_tools.py -x -q` |
| Full suite command | `.venv/bin/python3 -m pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| MKTX-01 | `analyze_stock` returns formatted string with chart path | unit (mock adapter) | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_analyze_stock_returns_output -x` | Wave 0 |
| MKTX-01 | Chart PNG is saved to `finance_output/charts/` | unit (tmp_path) | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_analyze_stock_saves_chart -x` | Wave 0 |
| MKTX-02 | `get_returns` daily and cumulative values are correct | unit (synthetic data) | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_get_returns_values -x` | Wave 0 |
| MKTX-02 | Returns chart saved as PNG | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_get_returns_chart -x` | Wave 0 |
| MKTX-03 | Annualized volatility = `std * sqrt(252)` (numerically verified) | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_annualized_volatility_formula -x` | Wave 0 |
| MKTX-03 | Rolling vol chart saved as PNG | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_volatility_chart -x` | Wave 0 |
| MKTX-04 | Sharpe ratio sign correct (positive for profitable series) | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_sharpe_sign -x` | Wave 0 |
| MKTX-04 | Max drawdown is <= 0 | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_max_drawdown_nonpositive -x` | Wave 0 |
| MKTX-04 | Beta computed against aligned benchmark | unit (mock ^GSPC) | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_beta_calculation -x` | Wave 0 |
| MKTX-05 | `compare_tickers` normalized prices start at 100.0 | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_normalized_prices_start_at_100 -x` | Wave 0 |
| MKTX-05 | Comparison chart saved as PNG | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_compare_tickers_chart -x` | Wave 0 |
| MKTX-06 | Correlation matrix computed on returns not price levels | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_correlation_uses_returns -x` | Wave 0 |
| MKTX-06 | Heatmap PNG saved | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_correlation_map_chart -x` | Wave 0 |
| MKTX-07 | All tool outputs begin with plain-English text (not raw numbers) | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_output_plain_english_first -x` | Wave 0 |
| MKTX-07 | All tool outputs end with DISCLAIMER constant | unit | `.venv/bin/python3 -m pytest tests/test_market_tools.py::test_output_ends_with_disclaimer -x` | Wave 0 |

### Sampling Rate

- **Per task commit:** `.venv/bin/python3 -m pytest tests/test_market_tools.py -x -q`
- **Per wave merge:** `.venv/bin/python3 -m pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_market_tools.py` — all 15 test stubs above (covers MKTX-01 through MKTX-07)
- [ ] `src/finance_mcp/tools/__init__.py` — empty init to make tools a package

*(No framework install needed — pytest and all fixtures already configured in conftest.py and pyproject.toml)*

---

## Sources

### Primary (HIGH confidence)

- FastMCP official docs — https://gofastmcp.com/servers/tools — `mcp.add_tool()` registration pattern
- seaborn 0.13.2 official docs — https://seaborn.pydata.org/generated/seaborn.heatmap.html — `sns.heatmap` parameters
- Phase 1 source files (adapter.py, output.py, validators.py, server.py) — directly read; all API contracts verified
- Phase 1 decisions (STATE.md) — yfinance 0.2.54+ `Close` column, ToolError import path, matplotlib Agg pattern

### Secondary (MEDIUM confidence)

- WebSearch: pandas `pct_change`, `rolling().std()`, `np.sqrt(252)` — corroborated by multiple finance tutorial sites using identical formulas
- WebSearch: normalized price comparison `prices / prices.iloc[0] * 100` — standard pattern in quantitative finance

### Tertiary (LOW confidence)

- Figure sizing formula for dynamic heatmap `(max(6, n*1.5), max(5, n*1.2))` — empirical estimate, not from official docs

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages confirmed installed in Phase 1; no new dependencies required
- Architecture: HIGH — FastMCP `mcp.add_tool()` confirmed in official docs; module pattern follows Phase 1 conventions
- Financial formulas: HIGH — pandas/numpy patterns corroborated across multiple sources; standard industry conventions
- Pitfalls: HIGH (5 of 6) — derived from Phase 1 lessons learned and directly from source code; LOW for figure sizing only

**Research date:** 2026-03-17
**Valid until:** 2026-09-17 (stable libraries; yfinance API changes could occur; re-verify if yfinance >= 0.3 releases)
