"""Tests for market_movers tool — TDD-first."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from finance_mcp.output import DISCLAIMER
from finance_mcp.providers.base import Capability


def _make_provider(capabilities: set[Capability], method_name: str, return_value: list) -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset(capabilities)
    getattr(provider, method_name).return_value = return_value
    return provider


SAMPLE_GAINERS = [
    {"ticker": "AAPL", "price": 195.0, "change_pct": 5.2, "volume": 1_000_000},
    {"ticker": "MSFT", "price": 400.0, "change_pct": 3.1, "volume": 800_000},
]

SAMPLE_LOSERS = [
    {"ticker": "META", "price": 300.0, "change_pct": -4.5, "volume": 600_000},
    {"ticker": "NVDA", "price": 450.0, "change_pct": -2.8, "volume": 700_000},
]


def test_market_movers_gainers_contains_tickers():
    """market_movers returns a string containing ticker symbols for gainers."""
    provider = _make_provider({Capability.MARKET_MOVERS}, "stocks_gainers", SAMPLE_GAINERS)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers(direction="gainers", market="stocks", limit=10)

    assert isinstance(result, str)
    assert "AAPL" in result
    assert "MSFT" in result


def test_market_movers_losers_contains_tickers():
    """market_movers returns losers when direction='losers'."""
    provider = _make_provider({Capability.MARKET_MOVERS}, "stocks_losers", SAMPLE_LOSERS)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers(direction="losers", market="stocks", limit=10)

    assert "META" in result
    assert "NVDA" in result


def test_market_movers_ends_with_disclaimer():
    """market_movers output ends with the standard disclaimer."""
    provider = _make_provider({Capability.MARKET_MOVERS}, "stocks_gainers", SAMPLE_GAINERS)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers()

    assert result.strip().endswith(DISCLAIMER)


def test_market_movers_respects_limit():
    """market_movers limits output to the requested number of rows."""
    many_rows = [
        {"ticker": f"T{i:03d}", "price": 100.0 + i, "change_pct": float(i), "volume": 1_000_000}
        for i in range(20)
    ]
    provider = _make_provider({Capability.MARKET_MOVERS}, "stocks_gainers", many_rows)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers(direction="gainers", market="stocks", limit=5)

    # Only first 5 tickers should appear
    assert "T000" in result
    assert "T004" in result
    assert "T005" not in result


def test_market_movers_capability_missing_raises():
    """market_movers raises ToolError when provider lacks MARKET_MOVERS capability."""
    from fastmcp.exceptions import ToolError
    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        with pytest.raises(ToolError):
            market_movers()


def test_market_movers_forex():
    """market_movers maps market='forex' to forex_gainers/losers methods."""
    sample = [{"ticker": "EUR/USD", "price": 1.08, "change_pct": 0.5, "volume": 5_000_000}]
    provider = _make_provider({Capability.MARKET_MOVERS}, "forex_gainers", sample)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers(direction="gainers", market="forex", limit=10)

    assert "EUR/USD" in result


def test_market_movers_crypto():
    """market_movers maps market='crypto' to crypto_gainers/losers methods."""
    sample = [{"ticker": "BTC-USD", "price": 60000.0, "change_pct": 3.0, "volume": 2_000_000}]
    provider = _make_provider({Capability.MARKET_MOVERS}, "crypto_gainers", sample)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers(direction="gainers", market="crypto", limit=10)

    assert "BTC-USD" in result


def test_market_movers_plain_english_first():
    """market_movers output starts with an alphabetical character (plain English)."""
    provider = _make_provider({Capability.MARKET_MOVERS}, "stocks_gainers", SAMPLE_GAINERS)
    with patch("finance_mcp.tools.market_movers.get_provider", return_value=provider):
        from finance_mcp.tools.market_movers import market_movers
        result = market_movers()

    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"
