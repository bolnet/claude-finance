"""get_options_chain MCP tool — options chain with Greeks for an underlying ticker."""
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


def get_options_chain(
    ticker: str,
    contract_type: str | None = None,
    expiration_date: str | None = None,
    limit: int = 20,
) -> str:
    """Fetch options chain with Greeks for a given underlying ticker.

    Args:
        ticker: Underlying ticker symbol (e.g. "AAPL").
        contract_type: Filter by "call" or "put". Omit for both.
        expiration_date: Filter by expiration date "YYYY-MM-DD". Omit for all expirations.
        limit: Maximum number of contracts to return (default 20).

    Returns:
        Formatted string with options table (Type, Strike, Expiry, Last, Vol,
        OI, IV, Delta, Gamma, Theta, Vega) and standard disclaimer.
    """
    provider = get_provider()

    if Capability.OPTIONS_CHAIN not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support OPTIONS_CHAIN. "
            "Switch to a Polygon provider to access options data."
        )

    contracts: list[dict[str, Any]] = provider.options_chain_snapshot(
        ticker,
        contract_type=contract_type,
        expiration_date=expiration_date,
        limit=limit,
    )

    ticker_upper = ticker.upper()
    filters: list[str] = []
    if contract_type:
        filters.append(contract_type)
    if expiration_date:
        filters.append(f"exp {expiration_date}")
    filter_label = f" ({', '.join(filters)})" if filters else ""

    if not contracts:
        interpretation = f"No options contracts found for {ticker_upper}{filter_label}."
        return format_output(interpretation)

    interpretation = (
        f"Options chain for {ticker_upper}{filter_label}: "
        f"{len(contracts)} contract{'s' if len(contracts) != 1 else ''} returned."
    )

    rows = [
        [
            c.get("contract_type", "-"),
            _fmt(c.get("strike_price")),
            c.get("expiration_date", "-"),
            _fmt(c.get("last_price")),
            _fmt(c.get("volume"), 0),
            _fmt(c.get("open_interest"), 0),
            _fmt(c.get("implied_volatility"), 4),
            _fmt(c.get("delta"), 4),
            _fmt(c.get("gamma"), 4),
            _fmt(c.get("theta"), 4),
            _fmt(c.get("vega"), 4),
        ]
        for c in contracts
    ]

    headers = ["Type", "Strike", "Expiry", "Last", "Vol", "OI", "IV", "Delta", "Gamma", "Theta", "Vega"]
    table = tabulate(rows, headers=headers, tablefmt="simple")
    return format_output(interpretation, data_section=table)
