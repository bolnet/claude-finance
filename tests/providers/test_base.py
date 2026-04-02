"""Tests for DataProvider Protocol and Capability flags."""
from __future__ import annotations

import pytest
import pandas as pd

from finance_mcp.providers import Capability, DataProvider, get_provider


class TestCapabilityEnum:
    """Test that Capability enum has all required flags."""

    def test_has_price_history(self) -> None:
        assert hasattr(Capability, "PRICE_HISTORY")

    def test_has_news(self) -> None:
        assert hasattr(Capability, "NEWS")

    def test_has_options_chain(self) -> None:
        assert hasattr(Capability, "OPTIONS_CHAIN")

    def test_has_forex(self) -> None:
        assert hasattr(Capability, "FOREX")

    def test_has_crypto(self) -> None:
        assert hasattr(Capability, "CRYPTO")

    def test_has_indices(self) -> None:
        assert hasattr(Capability, "INDICES")

    def test_has_technicals(self) -> None:
        assert hasattr(Capability, "TECHNICALS")

    def test_has_fundamentals(self) -> None:
        assert hasattr(Capability, "FUNDAMENTALS")

    def test_has_sec_filings(self) -> None:
        assert hasattr(Capability, "SEC_FILINGS")

    def test_has_market_movers(self) -> None:
        assert hasattr(Capability, "MARKET_MOVERS")

    def test_has_ticker_info(self) -> None:
        assert hasattr(Capability, "TICKER_INFO")

    def test_all_flags_count(self) -> None:
        """Ensure exactly 11 capability flags are defined."""
        expected = {
            "PRICE_HISTORY",
            "NEWS",
            "OPTIONS_CHAIN",
            "FOREX",
            "CRYPTO",
            "INDICES",
            "TECHNICALS",
            "FUNDAMENTALS",
            "SEC_FILINGS",
            "MARKET_MOVERS",
            "TICKER_INFO",
        }
        actual = {member.name for member in Capability}
        assert actual == expected


class TestDataProviderProtocol:
    """Test that DataProvider is a runtime-checkable Protocol."""

    def test_data_provider_is_protocol(self) -> None:
        from typing import get_type_hints
        import typing

        # Should be a runtime-checkable Protocol
        assert hasattr(DataProvider, "__protocol_attrs__") or hasattr(
            DataProvider, "_is_protocol"
        )

    def test_minimal_provider_satisfies_protocol(self) -> None:
        """A class implementing all required methods should pass isinstance."""

        class MinimalProvider:
            @property
            def capabilities(self) -> frozenset[Capability]:
                return frozenset({Capability.PRICE_HISTORY})

            def fetch_price_history(
                self,
                ticker: str,
                start: str,
                end: str | None = None,
                period: str | None = None,
            ) -> pd.DataFrame:
                return pd.DataFrame()

            def get_adjusted_prices(self, df: pd.DataFrame) -> pd.Series:
                return pd.Series(dtype=float)

            def fetch_multi_ticker(
                self,
                tickers: list[str],
                start: str,
                end: str | None = None,
                period: str | None = None,
            ) -> dict[str, pd.Series]:
                return {}

        provider = MinimalProvider()
        assert isinstance(provider, DataProvider)

    def test_incomplete_provider_fails_isinstance(self) -> None:
        """A class missing required methods should fail isinstance."""

        class IncompleteProvider:
            @property
            def capabilities(self) -> frozenset[Capability]:
                return frozenset()

            # Missing fetch_price_history, get_adjusted_prices, fetch_multi_ticker

        provider = IncompleteProvider()
        assert not isinstance(provider, DataProvider)
