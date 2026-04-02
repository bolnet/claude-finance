"""Tests for the get_news MCP tool."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.providers.base import Capability


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_provider(news_items: list | None = None) -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset({Capability.NEWS})
    provider.news.return_value = news_items if news_items is not None else [
        {
            "title": "Apple Hits Record High",
            "author": "Jane Doe",
            "published_utc": "2024-01-15T10:00:00Z",
            "description": "Apple stock reached a new all-time high on Monday amid strong demand.",
            "article_url": "https://example.com/apple-record",
            "tickers": ["AAPL"],
        },
        {
            "title": "Market Outlook for 2024",
            "author": "John Smith",
            "published_utc": "2024-01-14T08:30:00Z",
            "description": "Analysts predict a volatile but ultimately positive year for equities.",
            "article_url": "https://example.com/market-2024",
            "tickers": [],
        },
    ]
    return provider


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_get_news_returns_numbered_articles() -> None:
    """Output should contain numbered articles with title, author, date, and URL."""
    provider = _make_provider()
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        result = get_news(ticker="AAPL", limit=5)

    assert "1." in result
    assert "2." in result
    assert "Apple Hits Record High" in result
    assert "Jane Doe" in result
    assert "https://example.com/apple-record" in result


def test_get_news_includes_disclaimer() -> None:
    """Output must end with the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        result = get_news()

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_get_news_truncates_description() -> None:
    """Descriptions longer than 200 chars should be truncated."""
    long_description = "x" * 300
    provider = _make_provider(news_items=[
        {
            "title": "Long Article",
            "author": "Writer",
            "published_utc": "2024-01-01T00:00:00Z",
            "description": long_description,
            "article_url": "https://example.com/long",
            "tickers": [],
        }
    ])
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        result = get_news()

    # Truncated description should not contain the full 300-char string
    assert long_description not in result
    assert "..." in result


def test_get_news_without_capability_raises() -> None:
    """Should raise ToolError when NEWS capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        with pytest.raises(ToolError):
            get_news()


def test_get_news_limit_capped_at_50() -> None:
    """Provider should be called with limit capped at 50."""
    provider = _make_provider()
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        get_news(limit=200)

    provider.news.assert_called_once()
    _, kwargs = provider.news.call_args
    assert kwargs["limit"] <= 50


def test_get_news_no_ticker_calls_provider_without_ticker() -> None:
    """When ticker is None, provider.news should be called with ticker=None."""
    provider = _make_provider()
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        get_news()

    provider.news.assert_called_once_with(ticker=None, limit=10)


def test_get_news_empty_list_returns_graceful_message() -> None:
    """Empty news list should return a human-friendly 'no articles' message."""
    provider = _make_provider(news_items=[])
    with patch("finance_mcp.tools.news.get_provider", return_value=provider):
        from finance_mcp.tools.news import get_news

        result = get_news()

    assert "no" in result.lower() or "0" in result
