"""analyze_stock MCP tool — price chart for a single ticker (MKTX-01)."""
from finance_mcp.output import save_chart, format_output  # MUST import output first (sets Agg backend)
import matplotlib.pyplot as plt
import pandas as pd
from finance_mcp.adapter import fetch_price_history, get_adjusted_prices, DataFetchError
from fastmcp.exceptions import ToolError


def analyze_stock(ticker: str, start: str, end: str = "") -> str:
    """
    Generate a price chart for a stock ticker over the given date range.

    Args:
        ticker: Yahoo Finance ticker symbol, e.g. "AAPL"
        start: Start date in ISO format "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with plain-English price trend summary, chart path, and disclaimer.
    """
    try:
        df = fetch_price_history(ticker, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    prices = get_adjusted_prices(df)
    ticker_upper = ticker.strip().upper()

    # Build price chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(prices.index, prices.values, linewidth=1.5, color="#1f77b4")
    ax.set_title(f"{ticker_upper} Adjusted Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    end_label = end if end else "today"
    filename = f"{ticker_upper.lower()}_price_{start}_{end_label}.png"
    chart_path = save_chart(fig, filename)

    # Plain-English interpretation
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    pct_change = (end_price - start_price) / start_price * 100
    direction = "increased" if pct_change >= 0 else "decreased"
    interpretation = (
        f"{ticker_upper} {direction} {abs(pct_change):.1f}% from {start} to {end_label}. "
        f"Starting price: ${start_price:.2f}. Ending price: ${end_price:.2f}. "
        f"The price chart has been saved for visual inspection."
    )

    return format_output(
        plain_english=interpretation,
        chart_paths=[chart_path],
    )
