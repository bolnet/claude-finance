"""Crypto MCP tools — snapshot for a pair and top gainers/losers."""
from __future__ import annotations

from typing import Any

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability


def _fmt(value: float | None, decimals: int = 2) -> str:
    """Format a float to a fixed number of decimal places, or '-' if None."""
    if value is None:
        return "-"
    return f"{value:.{decimals}f}"


def crypto_snapshot(ticker: str) -> str:
    """Get current snapshot for a cryptocurrency pair.

    Args:
        ticker: Crypto ticker symbol (e.g. "X:BTCUSD").

    Returns:
        Formatted string with price, change, volume and standard disclaimer.
    """
    provider = get_provider()

    if Capability.CRYPTO not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support CRYPTO. "
            "Switch to a Polygon provider to access crypto data."
        )

    snap: dict[str, Any] = provider.crypto_snapshot(ticker)

    symbol = snap.get("ticker") or ticker.upper()
    close = snap.get("close")
    change = snap.get("change")
    change_pct = snap.get("change_percent")
    volume = snap.get("volume")
    high = snap.get("high")
    low = snap.get("low")
    prev_close = snap.get("prev_close")

    price_str = f"{close:,.2f}" if close is not None else "N/A"
    change_str = (
        f"{change:+.2f} ({change_pct:+.2f}%)" if (change is not None and change_pct is not None) else "-"
    )

    direction = ""
    if change_pct is not None:
        direction = "up" if change_pct >= 0 else "down"

    interpretation = (
        f"{symbol} is trading at {price_str}, "
        f"{direction} {abs(change_pct):.2f}% from the previous close."
        if change_pct is not None
        else f"{symbol} is currently trading at {price_str}."
    )

    data_section = (
        f"Ticker:       {symbol}\n"
        f"Price:        {price_str}\n"
        f"Change:       {change_str}\n"
        f"High:         {_fmt(high)}\n"
        f"Low:          {_fmt(low)}\n"
        f"Prev Close:   {_fmt(prev_close)}\n"
        f"Volume:       {_fmt(volume, 2)}"
    )
    return format_output(interpretation, data_section=data_section)


def crypto_movers(direction: str = "gainers", limit: int = 10) -> str:
    """Get top crypto gainers or losers.

    Args:
        direction: "gainers" for top gainers, "losers" for top losers.
        limit: Maximum number of results to display (default 10).

    Returns:
        Formatted table of top movers with standard disclaimer.
    """
    provider = get_provider()

    if Capability.CRYPTO not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support CRYPTO. "
            "Switch to a Polygon provider to access crypto data."
        )

    if direction not in ("gainers", "losers"):
        raise ToolError(
            f"Invalid direction {direction!r}. Must be 'gainers' or 'losers'."
        )

    if direction == "gainers":
        movers: list[dict[str, Any]] = provider.crypto_gainers()
    else:
        movers = provider.crypto_losers()

    # Apply limit
    movers = movers[:limit]

    label = "Top Crypto Gainers" if direction == "gainers" else "Top Crypto Losers"
    interpretation = f"{label}: {len(movers)} result{'s' if len(movers) != 1 else ''} returned."

    if not movers:
        return format_output(interpretation)

    rows = [
        [
            m.get("ticker", "-"),
            _fmt(m.get("close")),
            _fmt(m.get("change_percent"), 2) + "%" if m.get("change_percent") is not None else "-",
            _fmt(m.get("volume"), 0),
        ]
        for m in movers
    ]
    headers = ["Ticker", "Price", "Change %", "Volume"]
    table = tabulate(rows, headers=headers, tablefmt="simple")
    return format_output(interpretation, data_section=table)
