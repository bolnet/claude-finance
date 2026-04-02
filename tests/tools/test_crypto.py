"""Tests for the crypto MCP tools (crypto_snapshot, crypto_movers)."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.providers.base import Capability


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_provider() -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset({Capability.CRYPTO})
    provider.crypto_snapshot.return_value = {
        "ticker": "X:BTCUSD",
        "change": 1234.56,
        "change_percent": 2.45,
        "open": 48000.00,
        "high": 50500.00,
        "low": 47800.00,
        "close": 50123.45,
        "volume": 42350.12,
        "prev_close": 48888.89,
    }
    provider.crypto_gainers.return_value = [
        {
            "ticker": "X:ETHUSD",
            "change_percent": 8.5,
            "close": 2800.00,
            "volume": 120000.0,
        },
        {
            "ticker": "X:SOLUSD",
            "change_percent": 6.2,
            "close": 95.00,
            "volume": 80000.0,
        },
    ]
    provider.crypto_losers.return_value = [
        {
            "ticker": "X:DOTUSD",
            "change_percent": -5.3,
            "close": 7.50,
            "volume": 30000.0,
        },
    ]
    return provider


# ---------------------------------------------------------------------------
# crypto_snapshot tests
# ---------------------------------------------------------------------------


def test_crypto_snapshot_shows_ticker() -> None:
    """Output should display the crypto ticker."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        result = crypto_snapshot("X:BTCUSD")

    assert "BTCUSD" in result or "X:BTCUSD" in result


def test_crypto_snapshot_shows_price() -> None:
    """Output should include price/close value."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        result = crypto_snapshot("X:BTCUSD")

    assert "50123" in result or "50,123" in result


def test_crypto_snapshot_shows_change() -> None:
    """Output should include change percentage."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        result = crypto_snapshot("X:BTCUSD")

    assert "2.45" in result or "2.4" in result


def test_crypto_snapshot_includes_disclaimer() -> None:
    """Output must include the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        result = crypto_snapshot("X:BTCUSD")

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_crypto_snapshot_without_capability_raises() -> None:
    """Should raise ToolError when CRYPTO capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        with pytest.raises(ToolError):
            crypto_snapshot("X:BTCUSD")


def test_crypto_snapshot_forwards_ticker() -> None:
    """Provider should be called with the correct ticker."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_snapshot

        crypto_snapshot("X:ETHUSD")

    provider.crypto_snapshot.assert_called_once_with("X:ETHUSD")


# ---------------------------------------------------------------------------
# crypto_movers tests
# ---------------------------------------------------------------------------


def test_crypto_movers_gainers_calls_gainers() -> None:
    """direction='gainers' should call provider.crypto_gainers."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        crypto_movers(direction="gainers", limit=5)

    provider.crypto_gainers.assert_called_once()
    provider.crypto_losers.assert_not_called()


def test_crypto_movers_losers_calls_losers() -> None:
    """direction='losers' should call provider.crypto_losers."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        crypto_movers(direction="losers", limit=5)

    provider.crypto_losers.assert_called_once()
    provider.crypto_gainers.assert_not_called()


def test_crypto_movers_shows_tickers() -> None:
    """Output table should contain ticker symbols."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        result = crypto_movers(direction="gainers")

    assert "ETHUSD" in result or "X:ETHUSD" in result


def test_crypto_movers_includes_disclaimer() -> None:
    """Output must include the standard disclaimer."""
    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        result = crypto_movers()

    assert "educational" in result.lower() or "not financial advice" in result.lower()


def test_crypto_movers_without_capability_raises() -> None:
    """Should raise ToolError when CRYPTO capability is missing."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        with pytest.raises(ToolError):
            crypto_movers()


def test_crypto_movers_invalid_direction_raises() -> None:
    """Unknown direction value should raise ToolError."""
    from fastmcp.exceptions import ToolError

    provider = _make_provider()
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        with pytest.raises(ToolError):
            crypto_movers(direction="sideways")


def test_crypto_movers_limit_applied() -> None:
    """Output should be limited to the specified number of rows."""
    # Return more items than the limit
    provider = _make_provider()
    provider.crypto_gainers.return_value = [
        {"ticker": f"X:COIN{i}USD", "change_percent": float(10 - i), "close": 100.0, "volume": 1000.0}
        for i in range(15)
    ]
    with patch("finance_mcp.tools.crypto.get_provider", return_value=provider):
        from finance_mcp.tools.crypto import crypto_movers

        result = crypto_movers(direction="gainers", limit=3)

    # Only 3 rows should appear
    assert result.count("COIN") <= 3
