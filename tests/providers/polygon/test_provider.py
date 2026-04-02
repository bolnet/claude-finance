"""Tests for PolygonProvider – composition and DataProvider protocol."""
from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from finance_mcp.providers.base import Capability, DataProvider
from finance_mcp.providers.polygon.provider import PolygonProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_provider(mock_client: MagicMock | None = None) -> PolygonProvider:
    """Return a PolygonProvider with a mocked PolygonClient."""
    with patch(
        "finance_mcp.providers.polygon.provider.PolygonClient",
        return_value=mock_client or MagicMock(),
    ):
        return PolygonProvider(api_key="test-key")


def _sample_df() -> pd.DataFrame:
    """Return a minimal OHLCV DataFrame for testing."""
    idx = pd.date_range("2024-01-02", periods=3, freq="D")
    return pd.DataFrame(
        {
            "Open": [100.0, 101.0, 102.0],
            "High": [105.0, 106.0, 107.0],
            "Low": [99.0, 100.0, 101.0],
            "Close": [103.0, 104.0, 105.0],
            "Volume": [1_000_000, 1_100_000, 1_200_000],
        },
        index=idx,
    )


# ---------------------------------------------------------------------------
# Protocol satisfaction
# ---------------------------------------------------------------------------


def test_satisfies_data_provider_protocol() -> None:
    provider = _make_provider()
    assert isinstance(provider, DataProvider)


# ---------------------------------------------------------------------------
# capabilities
# ---------------------------------------------------------------------------


def test_capabilities_returns_frozenset() -> None:
    provider = _make_provider()
    caps = provider.capabilities
    assert isinstance(caps, frozenset)


def test_capabilities_include_all_11_flags() -> None:
    provider = _make_provider()
    caps = provider.capabilities
    assert caps == frozenset(Capability)


# ---------------------------------------------------------------------------
# fetch_price_history
# ---------------------------------------------------------------------------


def test_fetch_price_history_calls_stocks_bars() -> None:
    provider = _make_provider()
    expected_df = _sample_df()
    provider.stocks_bars = MagicMock(return_value=expected_df)  # type: ignore[method-assign]

    result = provider.fetch_price_history("AAPL", start="2024-01-02", end="2024-01-04")

    provider.stocks_bars.assert_called_once_with(
        "AAPL",
        multiplier=1,
        timespan="day",
        from_date="2024-01-02",
        to_date="2024-01-04",
    )
    assert result is expected_df


def test_fetch_price_history_period_1mo() -> None:
    """period='1mo' should compute an end-date 30 days from start."""
    provider = _make_provider()
    provider.stocks_bars = MagicMock(return_value=_sample_df())  # type: ignore[method-assign]

    provider.fetch_price_history("AAPL", start="2024-01-02", period="1mo")

    call_kwargs = provider.stocks_bars.call_args[1]
    expected_end = (date(2024, 1, 2) + timedelta(days=30)).isoformat()
    assert call_kwargs["to_date"] == expected_end


def test_fetch_price_history_period_1y() -> None:
    provider = _make_provider()
    provider.stocks_bars = MagicMock(return_value=_sample_df())  # type: ignore[method-assign]

    provider.fetch_price_history("MSFT", start="2023-01-01", period="1y")

    call_kwargs = provider.stocks_bars.call_args[1]
    expected_end = (date(2023, 1, 1) + timedelta(days=365)).isoformat()
    assert call_kwargs["to_date"] == expected_end


def test_fetch_price_history_explicit_end_overrides_period() -> None:
    """If both end and period are provided, end wins."""
    provider = _make_provider()
    provider.stocks_bars = MagicMock(return_value=_sample_df())  # type: ignore[method-assign]

    provider.fetch_price_history("AAPL", start="2024-01-02", end="2024-06-01", period="1mo")

    call_kwargs = provider.stocks_bars.call_args[1]
    assert call_kwargs["to_date"] == "2024-06-01"


# ---------------------------------------------------------------------------
# get_adjusted_prices
# ---------------------------------------------------------------------------


def test_get_adjusted_prices_returns_close_series() -> None:
    provider = _make_provider()
    df = _sample_df()
    series = provider.get_adjusted_prices(df)
    pd.testing.assert_series_equal(series, df["Close"])


# ---------------------------------------------------------------------------
# fetch_multi_ticker
# ---------------------------------------------------------------------------


def test_fetch_multi_ticker_returns_dict_of_series() -> None:
    provider = _make_provider()
    df = _sample_df()
    provider.fetch_price_history = MagicMock(return_value=df)  # type: ignore[method-assign]

    result = provider.fetch_multi_ticker(["AAPL", "MSFT"], start="2024-01-02")

    assert set(result.keys()) == {"AAPL", "MSFT"}
    for series in result.values():
        assert isinstance(series, pd.Series)


def test_fetch_multi_ticker_skips_failures(capsys: pytest.CaptureFixture[str]) -> None:
    provider = _make_provider()
    df = _sample_df()

    def side_effect(ticker: str, **kwargs: object) -> pd.DataFrame:
        if ticker == "BAD":
            raise RuntimeError("network error")
        return df

    provider.fetch_price_history = MagicMock(side_effect=side_effect)  # type: ignore[method-assign]

    result = provider.fetch_multi_ticker(["AAPL", "BAD"], start="2024-01-02")

    assert "AAPL" in result
    assert "BAD" not in result
    # Failure should be logged to stderr
    captured = capsys.readouterr()
    assert "BAD" in captured.err


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


def test_close_delegates_to_client() -> None:
    mock_client = MagicMock()
    provider = _make_provider(mock_client)
    provider.close()
    mock_client.close.assert_called_once()
