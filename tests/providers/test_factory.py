"""Tests for the DataProvider factory.

Verifies that get_provider() selects the correct provider based on environment
variables and raises appropriately when required config is absent.
"""
from __future__ import annotations

import os

import pytest

from finance_mcp.providers.base import DataProvider
from finance_mcp.providers.factory import get_provider


class TestGetProvider:
    def test_default_returns_yfinance(self) -> None:
        """When DATA_PROVIDER is not set, YFinanceProvider is returned."""
        with pytest.MonkeyPatch.context() as mp:
            mp.delenv("DATA_PROVIDER", raising=False)
            provider = get_provider()
        assert type(provider).__name__ == "YFinanceProvider"
        assert isinstance(provider, DataProvider)

    def test_explicit_yfinance(self) -> None:
        """DATA_PROVIDER=yfinance explicitly selects YFinanceProvider."""
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv("DATA_PROVIDER", "yfinance")
            provider = get_provider()
        assert type(provider).__name__ == "YFinanceProvider"
        assert isinstance(provider, DataProvider)

    def test_massive_requires_api_key(self) -> None:
        """DATA_PROVIDER=massive without MASSIVE_API_KEY raises RuntimeError."""
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv("DATA_PROVIDER", "massive")
            mp.delenv("MASSIVE_API_KEY", raising=False)
            with pytest.raises(RuntimeError, match="MASSIVE_API_KEY"):
                get_provider()

    def test_massive_with_api_key(self) -> None:
        """DATA_PROVIDER=massive with MASSIVE_API_KEY returns MassiveProvider."""
        with pytest.MonkeyPatch.context() as mp:
            mp.setenv("DATA_PROVIDER", "massive")
            mp.setenv("MASSIVE_API_KEY", "test123")
            provider = get_provider()
        assert type(provider).__name__ == "MassiveProvider"
        assert isinstance(provider, DataProvider)
