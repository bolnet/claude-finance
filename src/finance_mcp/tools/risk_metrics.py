"""get_risk_metrics MCP tool — Sharpe ratio, max drawdown, beta vs S&P 500 (MKTX-04)."""
from finance_mcp.output import save_chart, format_output  # import before pyplot
import numpy as np
import pandas as pd
from finance_mcp.adapter import DataFetchError
from fastmcp.exceptions import ToolError


def _compute_risk_metrics(returns: pd.Series, benchmark_returns: pd.Series) -> dict:
    """Pure computation — no I/O, no side effects. Testable in isolation."""
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    wealth = (1 + returns).cumprod()
    max_drawdown = ((wealth - wealth.cummax()) / wealth.cummax()).min()

    aligned = pd.concat([returns, benchmark_returns], axis=1).dropna()
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    beta = float(cov[0, 1] / cov[1, 1])

    return {
        "sharpe": float(sharpe),
        "max_drawdown": float(max_drawdown),
        "beta": beta,
    }


def get_risk_metrics(ticker: str, start: str, end: str = "") -> str:
    """
    Calculate Sharpe ratio, maximum drawdown, and beta vs S&P 500 for a stock ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, e.g. "AAPL"
        start: Start date "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with risk metric values, plain-English interpretation, and disclaimer.
    """
    from finance_mcp.server import provider
    ticker_upper = ticker.strip().upper()
    end_label = end if end else None

    try:
        df = provider.fetch_price_history(ticker_upper, start=start, end=end_label)
        bench_df = provider.fetch_price_history("^GSPC", start=start, end=end_label)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    prices = provider.get_adjusted_prices(df)
    bench_prices = provider.get_adjusted_prices(bench_df)

    daily = prices.pct_change().dropna()
    bench_daily = bench_prices.pct_change().dropna()

    metrics = _compute_risk_metrics(daily, bench_daily)

    # Plain-English interpretation
    sharpe = metrics["sharpe"]
    if sharpe > 1.0:
        sharpe_text = f"high risk-adjusted returns (Sharpe ratio {sharpe:.2f}, above the 1.0 threshold)"
    elif sharpe > 0:
        sharpe_text = f"moderate risk-adjusted returns (Sharpe ratio {sharpe:.2f})"
    else:
        sharpe_text = f"negative risk-adjusted returns (Sharpe ratio {sharpe:.2f}) — returns did not compensate for risk"

    drawdown_pct = abs(metrics["max_drawdown"]) * 100
    drawdown_text = (
        f"a maximum drawdown of {drawdown_pct:.1f}% — "
        f"an investor at the peak would have seen their position fall {drawdown_pct:.1f}% before recovering"
    )

    beta = metrics["beta"]
    if beta > 1.2:
        beta_text = f"a beta of {beta:.2f}, indicating higher volatility than the S&P 500 (moves amplify market moves)"
    elif beta > 0.8:
        beta_text = f"a beta of {beta:.2f}, moving roughly in line with the S&P 500"
    else:
        beta_text = f"a beta of {beta:.2f}, indicating lower sensitivity to S&P 500 moves"

    end_display = end if end else "today"
    interpretation = (
        f"{ticker_upper} showed {sharpe_text} from {start} to {end_display}. "
        f"The stock experienced {drawdown_text}. "
        f"It had {beta_text}. "
        f"Note: Sharpe ratio computed with risk-free rate = 0 (FRED integration is a future enhancement)."
    )

    data_section = (
        f"Sharpe Ratio:   {sharpe:.4f}\n"
        f"Max Drawdown:   {metrics['max_drawdown'] * 100:.2f}%\n"
        f"Beta (vs ^GSPC): {beta:.4f}"
    )

    return format_output(
        plain_english=interpretation,
        data_section=data_section,
    )
