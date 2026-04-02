"""market_movers MCP tool — top gainers/losers across stocks, forex, or crypto."""
from __future__ import annotations

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability

# Direction → method suffix
_DIRECTIONS = {"gainers", "losers"}
# Market → method prefix
_MARKETS = {"stocks", "forex", "crypto"}


def market_movers(
    direction: str = "gainers",
    market: str = "stocks",
    limit: int = 10,
) -> str:
    """Get top market movers (gainers or losers) across stocks, forex, or crypto.

    Args:
        direction: "gainers" or "losers". Defaults to "gainers".
        market: "stocks", "forex", or "crypto". Defaults to "stocks".
        limit: Maximum number of results to return. Defaults to 10.

    Returns:
        Formatted output with plain-English summary, tabulated mover data, and disclaimer.
    """
    provider = get_provider()

    if Capability.MARKET_MOVERS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support MARKET_MOVERS. "
            "Configure a provider with market mover capability (e.g. Polygon)."
        )

    direction = direction.lower().strip()
    market = market.lower().strip()

    if direction not in _DIRECTIONS:
        raise ToolError(f"Invalid direction '{direction}'. Must be one of: {sorted(_DIRECTIONS)}.")
    if market not in _MARKETS:
        raise ToolError(f"Invalid market '{market}'. Must be one of: {sorted(_MARKETS)}.")

    method_name = f"{market}_{direction}"
    method = getattr(provider, method_name)
    rows = method()[:limit]

    table_rows = [
        [r.get("ticker", ""), r.get("price", ""), r.get("change_pct", ""), r.get("volume", "")]
        for r in rows
    ]
    table = tabulate(
        table_rows,
        headers=["Ticker", "Price", "Change %", "Volume"],
        tablefmt="simple",
        floatfmt=".2f",
    )

    count = len(rows)
    direction_label = "gainers" if direction == "gainers" else "losers"
    interpretation = (
        f"Top {count} {market} {direction_label}: "
        f"{'leading gainer' if direction == 'gainers' else 'biggest loser'} is "
        f"{rows[0].get('ticker', 'N/A')} at {rows[0].get('change_pct', 0):+.2f}% change."
        if rows
        else f"No {market} {direction_label} data available."
    )

    return format_output(plain_english=interpretation, data_section=table)
