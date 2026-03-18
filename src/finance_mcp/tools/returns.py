"""get_returns MCP tool — daily and cumulative returns for a single ticker (MKTX-02)."""
from finance_mcp.output import save_chart, format_output  # import before pyplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from finance_mcp.adapter import fetch_price_history, get_adjusted_prices, DataFetchError
from fastmcp.exceptions import ToolError


def get_returns(ticker: str, start: str, end: str = "") -> str:
    """
    Calculate and chart daily and cumulative returns for a stock ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, e.g. "AAPL"
        start: Start date "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with returns summary, data table, chart path, and disclaimer.
    """
    try:
        df = fetch_price_history(ticker, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    prices = get_adjusted_prices(df)
    ticker_upper = ticker.strip().upper()
    daily = prices.pct_change().dropna()
    cumulative = (1 + daily).cumprod() - 1

    # Two-subplot chart: daily returns bar + cumulative line
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    colors = ["#d62728" if r < 0 else "#2ca02c" for r in daily.values]
    ax1.bar(daily.index, daily.values * 100, color=colors, width=0.8)
    ax1.set_ylabel("Daily Return (%)")
    ax1.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax2.plot(cumulative.index, cumulative.values * 100, linewidth=1.5, color="#1f77b4")
    ax2.set_ylabel("Cumulative Return (%)")
    ax2.set_xlabel("Date")
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
    fig.suptitle(f"{ticker_upper} Returns")
    fig.tight_layout()

    end_label = end if end else "today"
    chart_path = save_chart(fig, f"{ticker_upper.lower()}_returns_{start}.png")

    total_return = cumulative.iloc[-1] * 100
    avg_daily = daily.mean() * 100
    direction = "gained" if total_return >= 0 else "lost"
    interpretation = (
        f"{ticker_upper} {direction} {abs(total_return):.1f}% over the period from {start} to {end_label}. "
        f"Average daily return: {avg_daily:+.2f}%. "
        f"Daily returns chart (red=negative, green=positive) and cumulative return chart saved."
    )

    # Data table of recent returns
    recent = daily.tail(10) * 100
    data_rows = "\n".join(
        f"  {dt.date()}:  {val:+.2f}%" for dt, val in recent.items()
    )
    data_section = f"Recent daily returns (last 10 trading days):\n{data_rows}"

    return format_output(
        plain_english=interpretation,
        data_section=data_section,
        chart_paths=[chart_path],
    )
