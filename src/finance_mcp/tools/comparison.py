"""compare_tickers MCP tool — normalized multi-ticker price comparison chart (MKTX-05)."""
from finance_mcp.output import save_chart, format_output  # import before pyplot
import matplotlib.pyplot as plt
import pandas as pd
from finance_mcp.adapter import fetch_multi_ticker, DataFetchError
from fastmcp.exceptions import ToolError


def compare_tickers(tickers: str, start: str, end: str = "") -> str:
    """
    Compare 2-5 stock tickers on a normalized price performance chart.

    Prices are normalized to 100 at the start date so relative performance is visible.
    Uses the common date range (dates where ALL tickers have data).

    Args:
        tickers: Comma-separated ticker symbols, e.g. "AAPL,MSFT,GOOGL"
        start: Start date "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with comparison summary, chart path, and disclaimer.
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(ticker_list) < 2:
        raise ToolError("compare_tickers requires at least 2 ticker symbols, comma-separated.")
    if len(ticker_list) > 5:
        raise ToolError("compare_tickers supports up to 5 ticker symbols at a time.")

    try:
        prices_dict = fetch_multi_ticker(ticker_list, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    if len(prices_dict) < 2:
        raise ToolError(
            f"Could only fetch data for {len(prices_dict)} of {len(ticker_list)} tickers. "
            f"Need at least 2 valid tickers to compare."
        )

    # Build DataFrame, restrict to common date range
    prices_df = pd.DataFrame(prices_dict).dropna()
    if prices_df.empty:
        raise ToolError("No overlapping trading dates found for the given tickers and date range.")

    # Normalize to base 100
    normalized = prices_df / prices_df.iloc[0] * 100

    # Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in normalized.columns:
        ax.plot(normalized.index, normalized[col], linewidth=1.5, label=col)
    ax.axhline(100, color="gray", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.set_title("Normalized Price Performance (Base = 100)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price (Start = 100)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    end_label = end if end else "today"
    tickers_str = "_".join(sorted(prices_dict.keys()))
    chart_path = save_chart(fig, f"compare_{tickers_str}_{start}.png")

    # Interpretation: rank by final value
    final_values = normalized.iloc[-1].sort_values(ascending=False)
    best_ticker = final_values.index[0]
    worst_ticker = final_values.index[-1]
    best_return = final_values.iloc[0] - 100
    worst_return = final_values.iloc[-1] - 100

    period_note = f"Comparison uses the common date range: {prices_df.index[0].date()} to {prices_df.index[-1].date()}."
    interpretation = (
        f"Over the period from {start} to {end_label}, {best_ticker} was the top performer "
        f"with a normalized return of {best_return:+.1f}% (starting at 100). "
        f"{worst_ticker} was the weakest performer at {worst_return:+.1f}%. "
        f"{period_note}"
    )

    all_returns = ", ".join(
        f"{t}: {final_values[t] - 100:+.1f}%" for t in final_values.index
    )
    data_section = f"Normalized returns (base 100 at {start}):\n  {all_returns}"

    return format_output(
        plain_english=interpretation,
        data_section=data_section,
        chart_paths=[chart_path],
    )
