"""Ticker info MCP tools — details and search for ticker symbols."""
from __future__ import annotations

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability

_DESCRIPTION_MAX_LEN = 500


def get_ticker_details(ticker: str) -> str:
    """Get comprehensive details about a ticker symbol.

    Args:
        ticker: Ticker symbol, e.g. "AAPL".

    Returns:
        Formatted output with company name, market, type, market cap, employees,
        description, homepage URL, and disclaimer.
    """
    provider = get_provider()

    if Capability.TICKER_INFO not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support TICKER_INFO. "
            "Configure a provider with ticker info capability (e.g. Polygon)."
        )

    ticker_upper = ticker.strip().upper()
    details = provider.ticker_details(ticker_upper)

    name = details.get("name", "N/A")
    market = details.get("market", "N/A")
    ticker_type = details.get("type", "N/A")
    market_cap = details.get("market_cap")
    employees = details.get("employees")
    description = details.get("description", "")
    homepage_url = details.get("homepage_url", "")

    # Format market cap in a human-readable way
    if market_cap is not None:
        if market_cap >= 1_000_000_000_000:
            cap_str = f"${market_cap / 1_000_000_000_000:.2f}T"
        elif market_cap >= 1_000_000_000:
            cap_str = f"${market_cap / 1_000_000_000:.2f}B"
        else:
            cap_str = f"${market_cap:,.0f}"
    else:
        cap_str = "N/A"

    employees_str = f"{employees:,}" if employees else "N/A"
    description_truncated = description[:_DESCRIPTION_MAX_LEN] if description else "N/A"

    interpretation = (
        f"{name} ({ticker_upper}) is a {ticker_type} trading on the {market} market "
        f"with a market cap of {cap_str} and {employees_str} employees."
    )

    data_lines = [
        f"Name:         {name}",
        f"Ticker:       {ticker_upper}",
        f"Market:       {market}",
        f"Type:         {ticker_type}",
        f"Market Cap:   {cap_str}",
        f"Employees:    {employees_str}",
        f"Homepage:     {homepage_url or 'N/A'}",
        f"",
        f"Description:",
        f"{description_truncated}",
    ]
    data_section = "\n".join(data_lines)

    return format_output(plain_english=interpretation, data_section=data_section)


def search_tickers(
    query: str,
    market: str | None = None,
    limit: int = 20,
) -> str:
    """Search for tickers by name or symbol.

    Args:
        query: Search string, e.g. "apple" or "AAPL".
        market: Optional market filter, e.g. "stocks", "crypto", "fx".
        limit: Maximum number of results to return. Defaults to 20.

    Returns:
        Formatted output with a table of matching tickers and disclaimer.
    """
    provider = get_provider()

    if Capability.TICKER_INFO not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support TICKER_INFO. "
            "Configure a provider with ticker info capability (e.g. Polygon)."
        )

    results = provider.ticker_search(search=query, market=market, limit=limit)

    table_rows = [
        [r.get("ticker", ""), r.get("name", ""), r.get("market", ""), r.get("type", "")]
        for r in results
    ]
    table = tabulate(
        table_rows,
        headers=["Ticker", "Name", "Market", "Type"],
        tablefmt="simple",
    )

    count = len(results)
    market_label = f" in {market} market" if market else ""
    interpretation = (
        f"Found {count} ticker(s) matching '{query}'{market_label}."
        if results
        else f"No tickers found matching '{query}'{market_label}."
    )

    return format_output(plain_english=interpretation, data_section=table)
