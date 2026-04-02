"""Tests for the get_options_chain MCP tool."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.providers.base import Capability


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_provider(contracts: list | None = None) -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset({Capability.OPTIONS_CHAIN})
    provider.options_chain_snapshot.return_value = contracts if contracts is not None else [
        {
            "contract_type": "call",
            "strike_price": 150.0,
            "expiration_date": "2024-03-15",
            "last_price": 5.20,
            "volume": 1200,
            "open_interest": 8500,
            "implied_volatility": 0.32,
            "delta": 0.55,
            "gamma": 0.04,
            "theta": -0.08,
            "vega": 0.22,
        },
        {
            "contract_type": "put",
            "strike_price": 145.0,
            "expiration_date": "2024-03-15",
            "last_price": 3.10,
            "volume": 900,
            "open_interest": 6200,
            "implied_volatility": 0.28,
            "delta": -0.40,
            "gamma": 0.03,
            "theta": -0.06,
            "vega": 0.18,
        },
    ]
    return provider


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_get_options_chain_returns_table() -> None:
    """Output should contain a tabulate table with option rows."""
    provider = _make_provider()
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        result = get_options_chain("AAPL")

    assert "call" in result.lower() or "Call" in result
    assert "put" in result.lower() or "Put" in result
    assert "150" in result


def test_get_options_chain_table_columns() -> None:
    """Table should include Type, Strike, Expiry, and Greek columns."""
    provider = _make_provider()
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        result = get_options_chain("AAPL")

    for col in ("Strike", "Expiry", "Delta", "IV"):
        assert col in result


def test_get_options_chain_includes_disclaimer() -> None:
    """Output must include the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        result = get_options_chain("AAPL")

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_get_options_chain_without_capability_raises() -> None:
    """Should raise ToolError when OPTIONS_CHAIN capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        with pytest.raises(ToolError):
            get_options_chain("AAPL")


def test_get_options_chain_forwards_filters() -> None:
    """contract_type and expiration_date should be forwarded to the provider."""
    provider = _make_provider()
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        get_options_chain("AAPL", contract_type="call", expiration_date="2024-03-15", limit=10)

    provider.options_chain_snapshot.assert_called_once_with(
        "AAPL",
        contract_type="call",
        expiration_date="2024-03-15",
        limit=10,
    )


def test_get_options_chain_empty_returns_graceful_message() -> None:
    """Empty chain should return a human-friendly message."""
    provider = _make_provider(contracts=[])
    with patch("finance_mcp.tools.options_chain.get_provider", return_value=provider):
        from finance_mcp.tools.options_chain import get_options_chain

        result = get_options_chain("AAPL")

    assert "no" in result.lower() or "0" in result
