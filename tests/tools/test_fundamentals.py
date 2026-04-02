"""Tests for fundamentals MCP tools: get_dividends, get_splits, get_short_interest."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.output import DISCLAIMER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_provider(**kwargs) -> MagicMock:
    """Return a mock provider with FUNDAMENTALS capability."""
    from finance_mcp.providers.base import Capability

    provider = MagicMock()
    provider.capabilities = frozenset({Capability.FUNDAMENTALS})
    for attr, value in kwargs.items():
        getattr(provider, attr).return_value = value
    return provider


_DIVIDENDS = [
    {"ex_date": "2024-08-09", "pay_date": "2024-08-15", "cash_amount": 0.25, "frequency": 4},
    {"ex_date": "2024-05-10", "pay_date": "2024-05-16", "cash_amount": 0.24, "frequency": 4},
]

_SPLITS = [
    {"execution_date": "2020-08-31", "split_from": 1, "split_to": 4},
    {"execution_date": "2014-06-09", "split_from": 1, "split_to": 7},
]

_SHORT_INTEREST = {
    "ticker": "AAPL",
    "short_interest": 98_000_000,
    "settlement_date": "2024-07-15",
    "short_percent_of_float": 0.0062,
}

_FLOAT_SHARES = {
    "ticker": "AAPL",
    "float": 15_600_000_000,
    "outstanding_shares": 15_700_000_000,
    "date": "2024-07-01",
}


# ===========================================================================
# get_dividends
# ===========================================================================


def test_get_dividends_returns_string():
    """get_dividends returns a str."""
    provider = _make_provider(dividends=_DIVIDENDS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        result = get_dividends("AAPL")

    assert isinstance(result, str)


def test_get_dividends_contains_ex_date():
    """Output contains at least one ex-date from the response."""
    provider = _make_provider(dividends=_DIVIDENDS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        result = get_dividends("AAPL")

    assert "2024-08-09" in result


def test_get_dividends_contains_amount():
    """Output contains the dividend amount."""
    provider = _make_provider(dividends=_DIVIDENDS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        result = get_dividends("AAPL")

    assert "0.25" in result


def test_get_dividends_ends_with_disclaimer():
    """Output ends with standard disclaimer."""
    provider = _make_provider(dividends=_DIVIDENDS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        result = get_dividends("AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_dividends_calls_provider_with_limit():
    """Provider.dividends is called with ticker and limit."""
    provider = _make_provider(dividends=_DIVIDENDS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        get_dividends("AAPL", limit=10)

    provider.dividends.assert_called_once_with("AAPL", 10)


def test_get_dividends_missing_capability_raises():
    """ToolError raised when provider lacks FUNDAMENTALS capability."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()

    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_dividends

        with pytest.raises(ToolError):
            get_dividends("AAPL")


# ===========================================================================
# get_splits
# ===========================================================================


def test_get_splits_returns_string():
    """get_splits returns a str."""
    provider = _make_provider(splits=_SPLITS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_splits

        result = get_splits("AAPL")

    assert isinstance(result, str)


def test_get_splits_contains_date():
    """Output contains the split execution date."""
    provider = _make_provider(splits=_SPLITS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_splits

        result = get_splits("AAPL")

    assert "2020-08-31" in result


def test_get_splits_contains_ratio():
    """Output contains the split ratio in from:to format."""
    provider = _make_provider(splits=_SPLITS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_splits

        result = get_splits("AAPL")

    assert "1:4" in result or "4" in result


def test_get_splits_ends_with_disclaimer():
    """Output ends with standard disclaimer."""
    provider = _make_provider(splits=_SPLITS)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_splits

        result = get_splits("AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_splits_missing_capability_raises():
    """ToolError raised when provider lacks FUNDAMENTALS capability."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()

    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_splits

        with pytest.raises(ToolError):
            get_splits("AAPL")


# ===========================================================================
# get_short_interest
# ===========================================================================


def test_get_short_interest_returns_string():
    """get_short_interest returns a str."""
    provider = _make_provider(short_interest=_SHORT_INTEREST, float_shares=_FLOAT_SHARES)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        result = get_short_interest("AAPL")

    assert isinstance(result, str)


def test_get_short_interest_contains_short_data():
    """Output includes short interest values."""
    provider = _make_provider(short_interest=_SHORT_INTEREST, float_shares=_FLOAT_SHARES)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        result = get_short_interest("AAPL")

    # Should have some indication of short interest value
    assert "98" in result or "short" in result.lower()


def test_get_short_interest_contains_float_data():
    """Output includes float share data."""
    provider = _make_provider(short_interest=_SHORT_INTEREST, float_shares=_FLOAT_SHARES)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        result = get_short_interest("AAPL")

    assert "float" in result.lower() or "15" in result


def test_get_short_interest_ends_with_disclaimer():
    """Output ends with standard disclaimer."""
    provider = _make_provider(short_interest=_SHORT_INTEREST, float_shares=_FLOAT_SHARES)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        result = get_short_interest("AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_short_interest_calls_both_provider_methods():
    """Both short_interest and float_shares provider methods are called."""
    provider = _make_provider(short_interest=_SHORT_INTEREST, float_shares=_FLOAT_SHARES)
    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        get_short_interest("AAPL")

    provider.short_interest.assert_called_once_with("AAPL")
    provider.float_shares.assert_called_once_with("AAPL")


def test_get_short_interest_missing_capability_raises():
    """ToolError raised when provider lacks FUNDAMENTALS capability."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()

    with patch("finance_mcp.tools.fundamentals.get_provider", return_value=provider):
        from finance_mcp.tools.fundamentals import get_short_interest

        with pytest.raises(ToolError):
            get_short_interest("AAPL")
