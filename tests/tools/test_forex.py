"""Tests for the forex MCP tools (forex_convert, forex_quote)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.providers.base import Capability


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_provider() -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset({Capability.FOREX})
    provider.forex_conversion.return_value = {
        "from": "USD",
        "to": "EUR",
        "initial_amount": 100.0,
        "converted": 92.50,
    }
    provider.forex_last_quote.return_value = {
        "ask": 0.9260,
        "bid": 0.9250,
        "timestamp": 1705312800000,
    }
    return provider


# ---------------------------------------------------------------------------
# forex_convert tests
# ---------------------------------------------------------------------------


def test_forex_convert_shows_amount() -> None:
    """Output should include the converted amount."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_convert

        result = forex_convert("USD", "EUR", 100.0)

    assert "92.5" in result or "92.50" in result


def test_forex_convert_shows_currencies() -> None:
    """Output should display source and destination currency codes."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_convert

        result = forex_convert("USD", "EUR", 100.0)

    assert "USD" in result
    assert "EUR" in result


def test_forex_convert_includes_disclaimer() -> None:
    """Output must include the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_convert

        result = forex_convert("USD", "EUR")

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_forex_convert_without_capability_raises() -> None:
    """Should raise ToolError when FOREX capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_convert

        with pytest.raises(ToolError):
            forex_convert("USD", "EUR")


def test_forex_convert_forwards_amount() -> None:
    """Provider should be called with the correct amount."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_convert

        forex_convert("USD", "EUR", 250.0)

    provider.forex_conversion.assert_called_once_with(
        from_currency="USD", to_currency="EUR", amount=250.0
    )


# ---------------------------------------------------------------------------
# forex_quote tests
# ---------------------------------------------------------------------------


def test_forex_quote_shows_bid_ask() -> None:
    """Output should include bid and ask values."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_quote

        result = forex_quote("USD", "EUR")

    assert "0.925" in result
    assert "0.926" in result


def test_forex_quote_shows_spread() -> None:
    """Output should include the spread."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_quote

        result = forex_quote("USD", "EUR")

    assert "spread" in result.lower() or "Spread" in result


def test_forex_quote_includes_disclaimer() -> None:
    """Output must include the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_quote

        result = forex_quote("USD", "EUR")

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_forex_quote_without_capability_raises() -> None:
    """Should raise ToolError when FOREX capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_quote

        with pytest.raises(ToolError):
            forex_quote("USD", "EUR")


def test_forex_quote_forwards_currencies() -> None:
    """Provider should be called with the correct currency codes."""
    provider = _make_provider()
    with patch("finance_mcp.tools.forex.get_provider", return_value=provider):
        from finance_mcp.tools.forex import forex_quote

        forex_quote("GBP", "JPY")

    provider.forex_last_quote.assert_called_once_with(
        from_currency="GBP", to_currency="JPY"
    )
