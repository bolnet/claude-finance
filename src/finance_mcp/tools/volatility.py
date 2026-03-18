"""get_volatility MCP tool — annualized and rolling volatility (MKTX-03)."""
from finance_mcp.output import save_chart, format_output  # import before pyplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from finance_mcp.adapter import fetch_price_history, get_adjusted_prices, DataFetchError
from fastmcp.exceptions import ToolError


def get_volatility(ticker: str, start: str, end: str = "") -> str:
    """
    Calculate annualized volatility and rolling 21-day volatility for a stock ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, e.g. "AAPL"
        start: Start date "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with annualized volatility, rolling chart path, and disclaimer.
    """
    try:
        df = fetch_price_history(ticker, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    prices = get_adjusted_prices(df)
    ticker_upper = ticker.strip().upper()
    daily = prices.pct_change().dropna()

    annualized_vol = daily.std() * np.sqrt(252)
    rolling_vol = daily.rolling(21).std() * np.sqrt(252)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(rolling_vol.index, rolling_vol.values * 100, linewidth=1.5, color="#ff7f0e",
            label="21-day rolling annualized vol")
    ax.axhline(annualized_vol * 100, color="#1f77b4", linewidth=1.0, linestyle="--",
               label=f"Full-period annualized vol: {annualized_vol * 100:.1f}%")
    ax.set_title(f"{ticker_upper} Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized Volatility (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    end_label = end if end else "today"
    chart_path = save_chart(fig, f"{ticker_upper.lower()}_volatility_{start}.png")

    vol_pct = annualized_vol * 100
    sp500_avg = 15.0  # approximate historical average (assumption noted in output)
    comparison = "above" if vol_pct > sp500_avg else "below"
    interpretation = (
        f"{ticker_upper} had annualized volatility of {vol_pct:.1f}% over the period from {start} to {end_label}. "
        f"This is {comparison} the S&P 500 historical average of ~{sp500_avg:.0f}%. "
        f"Rolling volatility (21-day window) is shown in the chart; the first 21 days have no rolling value. "
        f"Note: Sharpe ratio assumes risk-free rate = 0 (FRED integration is a future enhancement)."
    )

    return format_output(
        plain_english=interpretation,
        data_section=f"Annualized volatility: {vol_pct:.2f}%",
        chart_paths=[chart_path],
    )
