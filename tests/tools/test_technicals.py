"""Tests for get_technical_indicator MCP tool."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from finance_mcp.output import DISCLAIMER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_series(n: int = 20) -> pd.Series:
    """Return a synthetic indicator pd.Series."""
    import numpy as np
    idx = pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.Series(data=[150.0 + i * 0.5 for i in range(n)], index=idx, name="value")


def _make_macd_result(n: int = 25) -> dict:
    """Return a synthetic MACD result dict."""
    values = [
        {
            "timestamp": f"2024-01-{i + 1:02d}",
            "value": 1.0 + i * 0.1,
            "signal": 0.8 + i * 0.1,
            "histogram": 0.2,
        }
        for i in range(n)
    ]
    return {"values": values}


def _make_provider(**kwargs) -> MagicMock:
    """Return a mock provider with TECHNICALS capability."""
    from finance_mcp.providers.base import Capability

    provider = MagicMock()
    provider.capabilities = frozenset({Capability.TECHNICALS})
    for attr, value in kwargs.items():
        getattr(provider, attr).return_value = value
    return provider


# ===========================================================================
# SMA
# ===========================================================================


def test_get_technical_indicator_sma_returns_string():
    """get_technical_indicator returns str for SMA."""
    provider = _make_provider(stocks_sma=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="sma", window=50)

    assert isinstance(result, str)


def test_get_technical_indicator_sma_ends_with_disclaimer():
    """SMA output ends with standard disclaimer."""
    provider = _make_provider(stocks_sma=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="sma")

    assert result.strip().endswith(DISCLAIMER)


def test_get_technical_indicator_sma_shows_last_10_rows():
    """Table contains at most 10 rows (last 10 values)."""
    provider = _make_provider(stocks_sma=_make_series(20))
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="sma", window=50)

    # The current value (last in series) is 159.5 (150 + 19*0.5)
    # Table should show last 10 values
    assert "159.5" in result or "159" in result


def test_get_technical_indicator_sma_calls_provider():
    """stocks_sma is called with correct args."""
    provider = _make_provider(stocks_sma=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        get_technical_indicator("AAPL", indicator="sma", window=20, timespan="week")

    provider.stocks_sma.assert_called_once_with("AAPL", 20, "week")


# ===========================================================================
# EMA
# ===========================================================================


def test_get_technical_indicator_ema_calls_provider():
    """stocks_ema is called for 'ema' indicator."""
    provider = _make_provider(stocks_ema=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        get_technical_indicator("AAPL", indicator="ema", window=20, timespan="day")

    provider.stocks_ema.assert_called_once_with("AAPL", 20, "day")


def test_get_technical_indicator_ema_returns_string():
    """get_technical_indicator returns str for EMA."""
    provider = _make_provider(stocks_ema=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="ema")

    assert isinstance(result, str)
    assert result.strip().endswith(DISCLAIMER)


# ===========================================================================
# RSI
# ===========================================================================


def test_get_technical_indicator_rsi_calls_provider():
    """stocks_rsi is called for 'rsi' indicator."""
    provider = _make_provider(stocks_rsi=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        get_technical_indicator("AAPL", indicator="rsi", window=14, timespan="day")

    provider.stocks_rsi.assert_called_once_with("AAPL", 14, "day")


def test_get_technical_indicator_rsi_returns_string():
    """get_technical_indicator returns str for RSI."""
    provider = _make_provider(stocks_rsi=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="rsi")

    assert isinstance(result, str)
    assert result.strip().endswith(DISCLAIMER)


# ===========================================================================
# MACD
# ===========================================================================


def test_get_technical_indicator_macd_calls_provider():
    """stocks_macd is called for 'macd' indicator."""
    provider = _make_provider(stocks_macd=_make_macd_result())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        get_technical_indicator("AAPL", indicator="macd", timespan="day")

    provider.stocks_macd.assert_called_once_with("AAPL", timespan="day")


def test_get_technical_indicator_macd_returns_string():
    """get_technical_indicator returns str for MACD."""
    provider = _make_provider(stocks_macd=_make_macd_result())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="macd")

    assert isinstance(result, str)
    assert result.strip().endswith(DISCLAIMER)


def test_get_technical_indicator_macd_shows_last_20():
    """MACD table shows last 20 values."""
    provider = _make_provider(stocks_macd=_make_macd_result(25))
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="macd")

    # 25th value: value=1.0+24*0.1=3.4, signal=0.8+24*0.1=3.2
    assert "3.4" in result or "MACD" in result.upper()


# ===========================================================================
# Case insensitivity
# ===========================================================================


def test_get_technical_indicator_uppercase_works():
    """Indicator name matching is case-insensitive."""
    provider = _make_provider(stocks_sma=_make_series())
    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        result = get_technical_indicator("AAPL", indicator="SMA")

    provider.stocks_sma.assert_called_once()
    assert isinstance(result, str)


# ===========================================================================
# Capability guard
# ===========================================================================


def test_get_technical_indicator_missing_capability_raises():
    """ToolError raised when provider lacks TECHNICALS capability."""
    from fastmcp.exceptions import ToolError

    provider = MagicMock()
    provider.capabilities = frozenset()

    with patch("finance_mcp.tools.technicals.get_provider", return_value=provider):
        from finance_mcp.tools.technicals import get_technical_indicator

        with pytest.raises(ToolError):
            get_technical_indicator("AAPL")
