"""Forex MCP tools — currency conversion and bid/ask quote."""
from __future__ import annotations

from fastmcp.exceptions import ToolError

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability


def forex_convert(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """Convert between currencies using real-time rates.

    Args:
        from_currency: Source currency code (e.g. "USD").
        to_currency: Destination currency code (e.g. "EUR").
        amount: Amount to convert (default 1.0).

    Returns:
        Formatted string with conversion result and standard disclaimer.
    """
    provider = get_provider()

    if Capability.FOREX not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support FOREX. "
            "Switch to a Polygon provider to access forex data."
        )

    result = provider.forex_conversion(
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
    )

    from_code = (result.get("from") or from_currency).upper()
    to_code = (result.get("to") or to_currency).upper()
    initial = result.get("initial_amount") or amount
    converted = result.get("converted")

    if converted is None:
        interpretation = (
            f"Currency conversion from {from_code} to {to_code} returned no data. "
            "The rate may be unavailable at this time."
        )
        return format_output(interpretation)

    rate = converted / initial if initial else 0.0
    interpretation = (
        f"{initial:,.2f} {from_code} = {converted:,.4f} {to_code} "
        f"(rate: 1 {from_code} = {rate:.6f} {to_code})."
    )
    data_section = (
        f"From:       {from_code}\n"
        f"To:         {to_code}\n"
        f"Amount:     {initial:,.2f}\n"
        f"Converted:  {converted:,.4f}\n"
        f"Rate:       {rate:.6f}"
    )
    return format_output(interpretation, data_section=data_section)


def forex_quote(from_currency: str, to_currency: str) -> str:
    """Get latest bid/ask quote for a currency pair.

    Args:
        from_currency: Source currency code (e.g. "USD").
        to_currency: Destination currency code (e.g. "EUR").

    Returns:
        Formatted string with bid, ask, spread and standard disclaimer.
    """
    provider = get_provider()

    if Capability.FOREX not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support FOREX. "
            "Switch to a Polygon provider to access forex data."
        )

    quote = provider.forex_last_quote(
        from_currency=from_currency,
        to_currency=to_currency,
    )

    from_upper = from_currency.upper()
    to_upper = to_currency.upper()
    pair = f"{from_upper}/{to_upper}"

    ask = quote.get("ask")
    bid = quote.get("bid")

    if ask is None and bid is None:
        interpretation = f"No quote data available for {pair} at this time."
        return format_output(interpretation)

    spread = (ask - bid) if (ask is not None and bid is not None) else None
    spread_str = f"{spread:.6f}" if spread is not None else "-"

    interpretation = (
        f"Latest {pair} quote — Bid: {bid}, Ask: {ask}, Spread: {spread_str}."
    )
    data_section = (
        f"Pair:    {pair}\n"
        f"Bid:     {bid}\n"
        f"Ask:     {ask}\n"
        f"Spread:  {spread_str}"
    )
    return format_output(interpretation, data_section=data_section)
