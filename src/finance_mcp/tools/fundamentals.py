"""Fundamentals MCP tools — dividends, splits, short interest."""
from __future__ import annotations

from typing import Any

from fastmcp.exceptions import ToolError
from tabulate import tabulate

from finance_mcp.output import format_output
from finance_mcp.providers import Capability, get_provider


def _require_fundamentals() -> Any:
    """Return the active provider, raising ToolError if FUNDAMENTALS is unsupported."""
    provider = get_provider()
    if Capability.FUNDAMENTALS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support FUNDAMENTALS. "
            "Switch to a provider that supports fundamental data (e.g. Polygon)."
        )
    return provider


def get_dividends(ticker: str, limit: int = 20) -> str:
    """Get dividend history for a stock.

    Args:
        ticker: Stock ticker symbol, e.g. ``'AAPL'``.
        limit: Maximum number of dividend records to return (default 20).

    Returns:
        Formatted table with Ex-Date, Pay Date, Amount, and Frequency.
    """
    provider = _require_fundamentals()
    records: list[dict[str, Any]] = provider.dividends(ticker, limit)

    rows: list[list[Any]] = []
    for d in records:
        ex_date = d.get("ex_dividend_date") or d.get("ex_date") or "N/A"
        pay_date = d.get("pay_date") or "N/A"
        amount = d.get("cash_amount")
        amount_str = f"${amount:.4f}" if isinstance(amount, (int, float)) else "N/A"
        freq = d.get("frequency") or d.get("freq") or "N/A"
        rows.append([ex_date, pay_date, amount_str, freq])

    ticker_upper = ticker.upper()
    if rows:
        table = tabulate(
            rows,
            headers=["Ex-Date", "Pay Date", "Amount", "Frequency"],
            tablefmt="simple",
        )
        interpretation = (
            f"{ticker_upper} dividend history: {len(rows)} record(s) found. "
            f"Most recent ex-dividend date: {rows[0][0]}."
        )
    else:
        table = "(no dividend records found)"
        interpretation = f"No dividend history found for {ticker_upper}."

    return format_output(plain_english=interpretation, data_section=table)


def get_splits(ticker: str, limit: int = 20) -> str:
    """Get stock split history for a stock.

    Args:
        ticker: Stock ticker symbol, e.g. ``'AAPL'``.
        limit: Maximum number of split records to return (default 20).

    Returns:
        Formatted table with Date and Ratio (split_from:split_to).
    """
    provider = _require_fundamentals()
    records: list[dict[str, Any]] = provider.splits(ticker, limit)

    rows: list[list[Any]] = []
    for s in records:
        date = s.get("execution_date") or s.get("date") or "N/A"
        split_from = s.get("split_from") or 1
        split_to = s.get("split_to") or 1
        ratio = f"{split_from}:{split_to}"
        rows.append([date, ratio])

    ticker_upper = ticker.upper()
    if rows:
        table = tabulate(rows, headers=["Date", "Ratio"], tablefmt="simple")
        interpretation = (
            f"{ticker_upper} split history: {len(rows)} split(s) found. "
            f"Most recent split on {rows[0][0]} ({rows[0][1]})."
        )
    else:
        table = "(no split records found)"
        interpretation = f"No split history found for {ticker_upper}."

    return format_output(plain_english=interpretation, data_section=table)


def get_short_interest(ticker: str) -> str:
    """Get short interest and float data for a stock.

    Args:
        ticker: Stock ticker symbol, e.g. ``'AAPL'``.

    Returns:
        Formatted output combining short interest metrics and float share data.
    """
    provider = _require_fundamentals()
    si: dict[str, Any] = provider.short_interest(ticker)
    fl: dict[str, Any] = provider.float_shares(ticker)

    ticker_upper = ticker.upper()

    # Short interest section
    si_rows: list[list[Any]] = []
    if si:
        short_shares = si.get("short_interest")
        short_pct = si.get("short_percent_of_float")
        settle_date = si.get("settlement_date") or "N/A"
        si_rows.append(["Short Shares", f"{short_shares:,}" if isinstance(short_shares, (int, float)) else "N/A"])
        si_rows.append(["% of Float", f"{short_pct:.4%}" if isinstance(short_pct, float) else "N/A"])
        si_rows.append(["Settlement Date", settle_date])

    # Float section
    fl_rows: list[list[Any]] = []
    if fl:
        float_shares = fl.get("float")
        outstanding = fl.get("outstanding_shares")
        fl_date = fl.get("date") or "N/A"
        fl_rows.append(["Float Shares", f"{float_shares:,}" if isinstance(float_shares, (int, float)) else "N/A"])
        fl_rows.append(["Outstanding Shares", f"{outstanding:,}" if isinstance(outstanding, (int, float)) else "N/A"])
        fl_rows.append(["As of Date", fl_date])

    sections: list[str] = []
    if si_rows:
        sections.append("Short Interest:\n" + tabulate(si_rows, tablefmt="simple"))
    if fl_rows:
        sections.append("Float Data:\n" + tabulate(fl_rows, tablefmt="simple"))

    data_section = "\n\n".join(sections) if sections else "(no short interest / float data found)"

    if si or fl:
        interpretation = (
            f"{ticker_upper} short interest and float summary. "
            f"Short interest: {si.get('short_interest', 'N/A')} shares. "
            f"Float: {fl.get('float', 'N/A')} shares."
        )
    else:
        interpretation = f"No short interest or float data available for {ticker_upper}."

    return format_output(plain_english=interpretation, data_section=data_section)
