"""indices_snapshot MCP tool — current snapshot for one or more market indices."""
from __future__ import annotations

from typing import Any

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import Capability, get_provider


def indices_snapshot(tickers: str) -> str:
    """Get current snapshot for one or more market indices.

    Args:
        tickers: Comma-separated index ticker symbols using the I: prefix,
                 e.g. ``'I:SPX,I:NDX'``.

    Returns:
        Formatted table with Ticker, Name, and current Value for each index.
    """
    provider = get_provider()

    if Capability.INDICES not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support INDICES. "
            "Switch to a provider that supports index snapshots (e.g. Polygon)."
        )

    ticker_list: list[str] = [t.strip() for t in tickers.split(",") if t.strip()]
    results: list[dict[str, Any]] = provider.indices_snapshot(ticker_list)

    rows: list[list[Any]] = []
    for item in results:
        ticker: str = item.get("ticker", "")
        name: str = item.get("name", "")
        # Polygon v3 snapshot stores current value under session.close
        session: dict[str, Any] = item.get("session") or {}
        value: float | str = session.get("close") or item.get("value") or "N/A"
        if isinstance(value, float):
            value = f"{value:,.2f}"
        rows.append([ticker, name, value])

    if rows:
        table = tabulate(rows, headers=["Ticker", "Name", "Value"], tablefmt="simple")
        interpretation = (
            f"Index snapshot for {', '.join(ticker_list)}: "
            f"{len(rows)} index(es) returned."
        )
    else:
        table = "(no data returned)"
        interpretation = f"No snapshot data found for: {', '.join(ticker_list)}."

    return format_output(plain_english=interpretation, data_section=table)
