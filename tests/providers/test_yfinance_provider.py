"""Tests for YFinanceProvider."""
from __future__ import annotations

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from finance_mcp.providers import Capability, DataProvider
from finance_mcp.providers.yfinance_provider import YFinanceProvider


@pytest.fixture
def provider() -> YFinanceProvider:
    return YFinanceProvider()


@pytest.fixture
def sample_price_df() -> pd.DataFrame:
    dates = pd.date_range("2023-01-01", periods=5, freq="B")
    return pd.DataFrame(
        {
            "Open": np.random.uniform(150, 160, 5),
            "High": np.random.uniform(160, 170, 5),
            "Low": np.random.uniform(140, 150, 5),
            "Close": np.random.uniform(150, 165, 5),
            "Volume": np.random.randint(1_000_000, 5_000_000, 5),
        },
        index=dates,
    )


class TestYFinanceProviderProtocol:
    """Test that YFinanceProvider satisfies the DataProvider Protocol."""

    def test_satisfies_data_provider_protocol(self, provider: YFinanceProvider) -> None:
        assert isinstance(provider, DataProvider)

    def test_capabilities_returns_frozenset(self, provider: YFinanceProvider) -> None:
        assert isinstance(provider.capabilities, frozenset)

    def test_capabilities_include_price_history(self, provider: YFinanceProvider) -> None:
        assert Capability.PRICE_HISTORY in provider.capabilities

    def test_capabilities_include_news(self, provider: YFinanceProvider) -> None:
        assert Capability.NEWS in provider.capabilities

    def test_capabilities_include_fundamentals(self, provider: YFinanceProvider) -> None:
        assert Capability.FUNDAMENTALS in provider.capabilities

    def test_capabilities_include_ticker_info(self, provider: YFinanceProvider) -> None:
        assert Capability.TICKER_INFO in provider.capabilities


class TestYFinanceProviderExcludedCapabilities:
    """Test that polygon-only features are NOT in YFinanceProvider capabilities."""

    def test_excludes_options_chain(self, provider: YFinanceProvider) -> None:
        assert Capability.OPTIONS_CHAIN not in provider.capabilities

    def test_excludes_forex(self, provider: YFinanceProvider) -> None:
        assert Capability.FOREX not in provider.capabilities

    def test_excludes_crypto(self, provider: YFinanceProvider) -> None:
        assert Capability.CRYPTO not in provider.capabilities

    def test_excludes_indices(self, provider: YFinanceProvider) -> None:
        assert Capability.INDICES not in provider.capabilities

    def test_excludes_sec_filings(self, provider: YFinanceProvider) -> None:
        assert Capability.SEC_FILINGS not in provider.capabilities

    def test_excludes_market_movers(self, provider: YFinanceProvider) -> None:
        assert Capability.MARKET_MOVERS not in provider.capabilities


class TestYFinanceProviderMethods:
    """Test that YFinanceProvider methods delegate to the adapter."""

    def test_get_adjusted_prices_returns_series(
        self, provider: YFinanceProvider, sample_price_df: pd.DataFrame
    ) -> None:
        result = provider.get_adjusted_prices(sample_price_df)
        assert isinstance(result, pd.Series)

    def test_get_adjusted_prices_returns_close_column(
        self, provider: YFinanceProvider, sample_price_df: pd.DataFrame
    ) -> None:
        result = provider.get_adjusted_prices(sample_price_df)
        pd.testing.assert_series_equal(result, sample_price_df["Close"])

    def test_fetch_price_history_delegates_to_adapter(
        self, provider: YFinanceProvider
    ) -> None:
        mock_df = pd.DataFrame({"Close": [100.0, 101.0]})
        with patch(
            "finance_mcp.providers.yfinance_provider.adapter.fetch_price_history",
            return_value=mock_df,
        ) as mock_fetch:
            result = provider.fetch_price_history("AAPL", "2023-01-01", end="2023-01-10")
            mock_fetch.assert_called_once_with(
                "AAPL", "2023-01-01", end="2023-01-10", period=None
            )
            assert result is mock_df

    def test_fetch_multi_ticker_delegates_to_adapter(
        self, provider: YFinanceProvider
    ) -> None:
        mock_result = {"AAPL": pd.Series([100.0, 101.0])}
        with patch(
            "finance_mcp.providers.yfinance_provider.adapter.fetch_multi_ticker",
            return_value=mock_result,
        ) as mock_fetch:
            result = provider.fetch_multi_ticker(
                ["AAPL"], "2023-01-01", end="2023-01-10"
            )
            mock_fetch.assert_called_once_with(
                ["AAPL"], "2023-01-01", end="2023-01-10", period=None
            )
            assert result is mock_result
