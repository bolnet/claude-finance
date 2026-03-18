"""correlation_map MCP tool — return correlation heatmap for a set of tickers (MKTX-06)."""
from finance_mcp.output import save_chart, format_output  # import before pyplot; sets Agg backend
import matplotlib.pyplot as plt
import pandas as pd
from finance_mcp.adapter import fetch_multi_ticker, DataFetchError
from fastmcp.exceptions import ToolError


def correlation_map(tickers: str, start: str, end: str = "") -> str:
    """
    Generate a return correlation heatmap for a set of stock tickers.

    Correlation is computed on daily returns (not price levels) to avoid spurious correlations
    from non-stationary price series.

    Args:
        tickers: Comma-separated ticker symbols, e.g. "AAPL,MSFT,GOOGL,AMZN"
        start: Start date "YYYY-MM-DD"
        end: End date "YYYY-MM-DD". Defaults to today if omitted.

    Returns:
        Formatted output with correlation summary, heatmap chart path, and disclaimer.
    """
    import seaborn as sns  # imported here — output.py has already set Agg backend

    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(ticker_list) < 2:
        raise ToolError("correlation_map requires at least 2 ticker symbols, comma-separated.")
    if len(ticker_list) > 10:
        raise ToolError("correlation_map supports up to 10 ticker symbols at a time.")

    try:
        prices_dict = fetch_multi_ticker(ticker_list, start=start, end=end or None)
    except DataFetchError as exc:
        raise ToolError(str(exc)) from exc

    if len(prices_dict) < 2:
        raise ToolError(
            f"Could only fetch data for {len(prices_dict)} of {len(ticker_list)} tickers. "
            f"Need at least 2 valid tickers for a correlation map."
        )

    # Restrict to common date range, compute correlation on RETURNS (not price levels)
    prices_df = pd.DataFrame(prices_dict).dropna()
    returns_df = prices_df.pct_change().dropna()

    if returns_df.empty or len(returns_df) < 5:
        raise ToolError("Insufficient overlapping return data for the given tickers and date range.")

    corr = returns_df.corr()

    n = len(corr)
    fig, ax = plt.subplots(figsize=(max(6, n * 1.5), max(5, n * 1.2)))
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

    end_label = end if end else "today"
    tickers_str = "_".join(sorted(prices_dict.keys()))
    chart_path = save_chart(fig, f"correlation_{tickers_str}_{start}.png")

    # Find highest and lowest correlated pair
    pairs = []
    tickers_fetched = list(corr.columns)
    for i in range(len(tickers_fetched)):
        for j in range(i + 1, len(tickers_fetched)):
            pairs.append(
                (tickers_fetched[i], tickers_fetched[j], corr.iloc[i, j])
            )

    if pairs:
        most_correlated = max(pairs, key=lambda x: x[2])
        least_correlated = min(pairs, key=lambda x: x[2])
        pair_note = (
            f"The most correlated pair is {most_correlated[0]}/{most_correlated[1]} "
            f"(r = {most_correlated[2]:.2f}). "
            f"The least correlated pair is {least_correlated[0]}/{least_correlated[1]} "
            f"(r = {least_correlated[2]:.2f})."
        )
    else:
        pair_note = ""

    period_note = (
        f"Correlation computed on daily returns from {prices_df.index[0].date()} "
        f"to {prices_df.index[-1].date()} (common trading days only). "
        f"Note: this measures co-movement of returns, not price levels."
    )

    interpretation = (
        f"Return correlation heatmap for {', '.join(tickers_fetched)} from {start} to {end_label}. "
        f"{pair_note} {period_note}"
    )

    return format_output(
        plain_english=interpretation,
        chart_paths=[chart_path],
    )
