"""get_news MCP tool — fetch latest market news, optionally filtered by ticker."""
from __future__ import annotations

from typing import Any

from fastmcp.exceptions import ToolError

from finance_mcp.output import format_output
from finance_mcp.providers import get_provider
from finance_mcp.providers.base import Capability


def get_news(ticker: str | None = None, limit: int = 10) -> str:
    """Fetch latest market news, optionally filtered by ticker.

    Args:
        ticker: Optional ticker symbol to filter news (e.g. "AAPL").
                When omitted, returns general market news.
        limit: Maximum number of articles to return (capped at 50).

    Returns:
        Formatted string with numbered article list and standard disclaimer.
    """
    provider = get_provider()

    if Capability.NEWS not in provider.capabilities:
        raise ToolError(
            "The active data provider does not support NEWS. "
            "Switch to a Polygon provider to access market news."
        )

    capped_limit = min(limit, 50)
    articles: list[dict[str, Any]] = provider.news(ticker=ticker, limit=capped_limit)

    ticker_label = f" for {ticker.upper()}" if ticker else ""
    if not articles:
        interpretation = f"No news articles found{ticker_label}."
        return format_output(interpretation)

    interpretation = (
        f"Found {len(articles)} recent news article{'s' if len(articles) != 1 else ''}"
        f"{ticker_label}."
    )

    lines: list[str] = []
    for i, article in enumerate(articles, start=1):
        title = article.get("title") or "Untitled"
        author = article.get("author") or "Unknown"
        date = article.get("published_utc") or ""
        description = article.get("description") or ""
        url = article.get("article_url") or ""

        # Truncate description to 200 characters
        if len(description) > 200:
            description = description[:200] + "..."

        lines.append(
            f"{i}. **{title}**\n"
            f"   By {author} | {date}\n"
            f"   {description}\n"
            f"   {url}"
        )

    data_section = "\n\n".join(lines)
    return format_output(interpretation, data_section=data_section)
