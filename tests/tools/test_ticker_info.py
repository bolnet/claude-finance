"""Tests for ticker_info tools — TDD-first."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from finance_mcp.output import DISCLAIMER
from finance_mcp.providers.base import Capability


def _make_provider(capabilities: set[Capability]) -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset(capabilities)
    return provider


SAMPLE_TICKER_DETAILS = {
    "name": "Apple Inc.",
    "market": "stocks",
    "type": "CS",
    "market_cap": 3_000_000_000_000,
    "employees": 161_000,
    "description": (
        "Apple Inc. designs, manufactures, and markets smartphones, personal computers, "
        "tablets, wearables, and accessories worldwide."
    ),
    "homepage_url": "https://www.apple.com",
}

SAMPLE_SEARCH_RESULTS = [
    {"ticker": "AAPL", "name": "Apple Inc.", "market": "stocks", "type": "CS"},
    {"ticker": "AAPLW", "name": "Apple Inc. Warrants", "market": "stocks", "type": "WARRANT"},
]


def test_get_ticker_details_returns_string():
    """get_ticker_details returns a non-empty string."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    assert isinstance(result, str)
    assert len(result) > 0


def test_get_ticker_details_contains_name():
    """get_ticker_details output includes the company name."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    assert "Apple Inc." in result


def test_get_ticker_details_contains_market_cap():
    """get_ticker_details output includes market cap information."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    # market_cap should appear in some form
    assert "3" in result  # 3 trillion


def test_get_ticker_details_contains_description():
    """get_ticker_details output includes a truncated description."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    assert "Apple Inc. designs" in result


def test_get_ticker_details_ends_with_disclaimer():
    """get_ticker_details output ends with the standard disclaimer."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_ticker_details_capability_missing_raises():
    """get_ticker_details raises ToolError when provider lacks TICKER_INFO capability."""
    from fastmcp.exceptions import ToolError
    provider = _make_provider(set())
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        with pytest.raises(ToolError):
            get_ticker_details(ticker="AAPL")


def test_get_ticker_details_calls_provider():
    """get_ticker_details passes ticker to provider.ticker_details."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        get_ticker_details(ticker="MSFT")

    provider.ticker_details.assert_called_once_with("MSFT")


def test_get_ticker_details_plain_english_first():
    """get_ticker_details output starts with an alphabetical character."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_details.return_value = SAMPLE_TICKER_DETAILS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import get_ticker_details
        result = get_ticker_details(ticker="AAPL")

    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"


def test_search_tickers_returns_string():
    """search_tickers returns a non-empty string."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_search.return_value = SAMPLE_SEARCH_RESULTS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        result = search_tickers(query="apple")

    assert isinstance(result, str)
    assert len(result) > 0


def test_search_tickers_contains_results():
    """search_tickers output includes ticker symbols and names."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_search.return_value = SAMPLE_SEARCH_RESULTS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        result = search_tickers(query="apple")

    assert "AAPL" in result
    assert "Apple Inc." in result


def test_search_tickers_ends_with_disclaimer():
    """search_tickers output ends with the standard disclaimer."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_search.return_value = SAMPLE_SEARCH_RESULTS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        result = search_tickers(query="apple")

    assert result.strip().endswith(DISCLAIMER)


def test_search_tickers_capability_missing_raises():
    """search_tickers raises ToolError when provider lacks TICKER_INFO capability."""
    from fastmcp.exceptions import ToolError
    provider = _make_provider(set())
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        with pytest.raises(ToolError):
            search_tickers(query="apple")


def test_search_tickers_passes_market_filter():
    """search_tickers passes market argument to provider.ticker_search."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_search.return_value = SAMPLE_SEARCH_RESULTS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        search_tickers(query="apple", market="stocks", limit=5)

    provider.ticker_search.assert_called_once_with(search="apple", market="stocks", limit=5)


def test_search_tickers_plain_english_first():
    """search_tickers output starts with an alphabetical character."""
    provider = _make_provider({Capability.TICKER_INFO})
    provider.ticker_search.return_value = SAMPLE_SEARCH_RESULTS
    with patch("finance_mcp.tools.ticker_info.get_provider", return_value=provider):
        from finance_mcp.tools.ticker_info import search_tickers
        result = search_tickers(query="apple")

    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"
