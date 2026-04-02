"""get_technical_indicator MCP tool — SMA, EMA, MACD, RSI for a stock."""
from __future__ import annotations

from typing import Any

import pandas as pd
from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import Capability, get_provider


def get_technical_indicator(
    ticker: str,
    indicator: str = "sma",
    window: int = 50,
    timespan: str = "day",
) -> str:
    """Calculate SMA, EMA, MACD, or RSI for a stock.

    Args:
        ticker: Stock ticker symbol, e.g. ``'AAPL'``.
        indicator: Indicator type — ``'sma'``, ``'ema'``, ``'rsi'``, or ``'macd'``
                   (case-insensitive, default ``'sma'``).
        window: Look-back window in periods (default 50; ignored for MACD).
        timespan: Aggregate bar size — e.g. ``'day'``, ``'week'`` (default ``'day'``).

    Returns:
        Formatted table with the indicator values plus a plain-English summary.
    """
    provider = get_provider()

    if Capability.TECHNICALS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support TECHNICALS. "
            "Switch to a provider that supports technical indicators (e.g. Polygon)."
        )

    ind = indicator.lower()
    ticker_upper = ticker.upper()

    if ind == "macd":
        return _handle_macd(provider, ticker_upper, timespan)

    # SMA / EMA / RSI share the same Series return type
    if ind == "ema":
        series: pd.Series = provider.stocks_ema(ticker_upper, window, timespan)
        label = f"EMA({window})"
    elif ind == "rsi":
        series = provider.stocks_rsi(ticker_upper, window, timespan)
        label = f"RSI({window})"
    else:  # default to sma
        series = provider.stocks_sma(ticker_upper, window, timespan)
        label = f"SMA({window})"

    return _format_series(ticker_upper, label, series)


def _format_series(ticker: str, label: str, series: pd.Series) -> str:
    """Format the last 10 values of a pd.Series indicator into a table."""
    tail = series.tail(10)

    rows: list[list[Any]] = [
        [str(ts)[:10] if hasattr(ts, "strftime") else str(ts), f"{val:.4f}"]
        for ts, val in tail.items()
    ]

    table = tabulate(rows, headers=["Date", label], tablefmt="simple")

    current_value: float | None = float(series.iloc[-1]) if len(series) > 0 else None
    if current_value is not None:
        interpretation = (
            f"{ticker} {label}: current value is {current_value:.4f} "
            f"(showing last {len(rows)} of {len(series)} data points)."
        )
    else:
        interpretation = f"No {label} data available for {ticker}."

    return format_output(plain_english=interpretation, data_section=table)


def _handle_macd(provider: Any, ticker: str, timespan: str) -> str:
    """Fetch and format MACD data (shows last 20 rows)."""
    result: dict[str, Any] = provider.stocks_macd(ticker, timespan=timespan)
    values: list[dict[str, Any]] = result.get("values") or []

    tail = values[-20:] if len(values) > 20 else values

    rows: list[list[Any]] = [
        [
            str(v.get("timestamp", ""))[:10],
            f"{v.get('value', 0):.4f}",
            f"{v.get('signal', 0):.4f}",
            f"{v.get('histogram', 0):.4f}",
        ]
        for v in tail
    ]

    table = tabulate(rows, headers=["Date", "MACD", "Signal", "Histogram"], tablefmt="simple")

    if values:
        latest = values[-1]
        macd_val = latest.get("value", 0)
        signal_val = latest.get("signal", 0)
        crossover = "above" if macd_val > signal_val else "below"
        interpretation = (
            f"{ticker} MACD: current MACD {macd_val:.4f}, signal {signal_val:.4f}. "
            f"MACD is {crossover} the signal line "
            f"(showing last {len(rows)} of {len(values)} data points)."
        )
    else:
        interpretation = f"No MACD data available for {ticker}."

    return format_output(plain_english=interpretation, data_section=table)
