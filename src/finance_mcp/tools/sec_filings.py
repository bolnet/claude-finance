"""SEC filings MCP tools — search EDGAR filings and retrieve risk factors."""
from __future__ import annotations

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability


def get_sec_filings(
    ticker: str | None = None,
    filing_type: str | None = None,
    limit: int = 10,
) -> str:
    """Search SEC EDGAR filings by ticker and/or filing type.

    Args:
        ticker: Ticker symbol to filter by, e.g. "AAPL". Optional.
        filing_type: SEC filing type to filter by, e.g. "10-K", "10-Q", "8-K". Optional.
        limit: Maximum number of results to return. Defaults to 10.

    Returns:
        Formatted output with plain-English summary, tabulated filings, and disclaimer.
    """
    provider = get_provider()

    if Capability.SEC_FILINGS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support SEC_FILINGS. "
            "Configure a provider with SEC filing capability (e.g. Polygon)."
        )

    filings = provider.sec_filings(ticker, filing_type, limit)

    table_rows = [
        [f.get("type", ""), f.get("date", ""), f.get("company", "")]
        for f in filings
    ]
    table = tabulate(
        table_rows,
        headers=["Type", "Date", "Company"],
        tablefmt="simple",
    )

    count = len(filings)
    ticker_label = f" for {ticker}" if ticker else ""
    type_label = f" ({filing_type})" if filing_type else ""
    interpretation = (
        f"Found {count} SEC filing(s){ticker_label}{type_label}. "
        f"Results are ordered by most recent filing date."
        if filings
        else f"No SEC filings found{ticker_label}{type_label}."
    )

    return format_output(plain_english=interpretation, data_section=table)


def get_risk_factors(ticker: str) -> str:
    """Get risk factors from the latest 10-K filing for a ticker.

    Args:
        ticker: Ticker symbol, e.g. "AAPL".

    Returns:
        Formatted output with the risk factors text and disclaimer.
    """
    provider = get_provider()

    if Capability.SEC_FILINGS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support SEC_FILINGS. "
            "Configure a provider with SEC filing capability (e.g. Polygon)."
        )

    ticker_upper = ticker.strip().upper()
    risk_text = provider.sec_risk_factors(ticker_upper)

    interpretation = (
        f"Risk factors from {ticker_upper}'s latest 10-K annual filing are shown below. "
        f"These represent management's assessment of material risks to the business."
    )

    return format_output(plain_english=interpretation, data_section=str(risk_text))
