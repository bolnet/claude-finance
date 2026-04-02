"""Tests for CurrenciesMixin — Forex and Crypto endpoints."""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pandas as pd
import pytest

from finance_mcp.providers.polygon.currencies import CurrenciesMixin


# ---------------------------------------------------------------------------
# FakeClient
# ---------------------------------------------------------------------------


class FakeClient:
    """Minimal stub that records the last call made via .get()."""

    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response
        self.last_path: str | None = None
        self.last_params: dict[str, Any] | None = None

    def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        self.last_path = path
        self.last_params = params or {}
        return self._response


# ---------------------------------------------------------------------------
# Concrete subject under test
# ---------------------------------------------------------------------------


class Provider(CurrenciesMixin):
    """Minimal concrete class that satisfies the mixin contract."""

    def __init__(self, client: FakeClient) -> None:
        self.client = client  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

_PREV_CLOSE_RESPONSE: dict[str, Any] = {
    "results": [
        {"T": "C:EURUSD", "o": 1.08, "h": 1.09, "l": 1.07, "c": 1.085, "v": 50000, "t": 1700000000000}
    ]
}

_AGGS_RESPONSE: dict[str, Any] = {
    "results": [
        {"t": 1700000000000, "o": 1.08, "h": 1.09, "l": 1.07, "c": 1.085, "v": 50000}
    ]
}

_CONVERSION_RESPONSE: dict[str, Any] = {
    "converted": 1.085,
    "from": "USD",
    "to": "EUR",
    "initialAmount": 1.0,
}

_LAST_QUOTE_RESPONSE: dict[str, Any] = {
    "last": {"ask": 1.086, "bid": 1.084, "timestamp": 1700000000},
}

_SNAPSHOTS_RESPONSE: dict[str, Any] = {
    "tickers": [
        {
            "ticker": "C:EURUSD",
            "todaysChange": 0.001,
            "todaysChangePerc": 0.09,
            "day": {"o": 1.08, "h": 1.09, "l": 1.07, "c": 1.085, "v": 50000},
            "prevDay": {"c": 1.084},
        }
    ]
}

_QUOTES_RESPONSE: dict[str, Any] = {
    "results": [{"ask_price": 1.086, "bid_price": 1.084, "participant_timestamp": 1700000000}]
}

_CRYPTO_SNAPSHOT_RESPONSE: dict[str, Any] = {
    "ticker": {
        "ticker": "X:BTCUSD",
        "todaysChange": 100.0,
        "todaysChangePerc": 0.3,
        "day": {"o": 35000, "h": 36000, "l": 34500, "c": 35800, "v": 1200},
        "prevDay": {"c": 35700},
    }
}

_DAILY_OHLC_RESPONSE: dict[str, Any] = {
    "symbol": "BTC-USD",
    "day": "2024-01-01",
    "open": 42000.0,
    "high": 43000.0,
    "low": 41500.0,
    "close": 42800.0,
    "volume": 5000.0,
}


# ---------------------------------------------------------------------------
# Forex tests
# ---------------------------------------------------------------------------


class TestForexPrevClose:
    def test_returns_dict_with_expected_keys(self) -> None:
        provider = Provider(FakeClient(_PREV_CLOSE_RESPONSE))
        result = provider.forex_prev_close("C:EURUSD")
        assert isinstance(result, dict)
        assert result["ticker"] == "C:EURUSD"
        assert result["close"] == 1.085

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_PREV_CLOSE_RESPONSE)
        provider = Provider(client)
        provider.forex_prev_close("C:EURUSD")
        assert client.last_path == "/v2/aggs/ticker/C:EURUSD/prev"


class TestForexBars:
    def test_returns_dataframe(self) -> None:
        provider = Provider(FakeClient(_AGGS_RESPONSE))
        df = provider.forex_bars("C:EURUSD", 1, "day", "2024-01-01", "2024-01-31")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_AGGS_RESPONSE)
        provider = Provider(client)
        provider.forex_bars("C:EURUSD", 1, "day", "2024-01-01", "2024-01-31")
        assert client.last_path == "/v2/aggs/ticker/C:EURUSD/range/1/day/2024-01-01/2024-01-31"

    def test_default_sort_and_limit(self) -> None:
        client = FakeClient(_AGGS_RESPONSE)
        provider = Provider(client)
        provider.forex_bars("C:EURUSD", 1, "hour", "2024-01-01", "2024-01-31")
        assert client.last_params.get("sort") == "asc"
        assert client.last_params.get("limit") == 50000


class TestForexConversion:
    def test_returns_dict_with_from_to_amounts(self) -> None:
        provider = Provider(FakeClient(_CONVERSION_RESPONSE))
        result = provider.forex_conversion("USD", "EUR", amount=1.0)
        assert isinstance(result, dict)
        assert "from" in result
        assert "to" in result
        assert "initial_amount" in result
        assert "converted" in result

    def test_calls_correct_path_uppercase(self) -> None:
        client = FakeClient(_CONVERSION_RESPONSE)
        provider = Provider(client)
        provider.forex_conversion("usd", "eur")
        assert client.last_path == "/v1/conversion/USD/EUR"

    def test_amount_passed_as_param(self) -> None:
        client = FakeClient(_CONVERSION_RESPONSE)
        provider = Provider(client)
        provider.forex_conversion("USD", "EUR", amount=100.0)
        assert client.last_params.get("amount") == 100.0


class TestForexLastQuote:
    def test_returns_dict_with_ask_bid_timestamp(self) -> None:
        provider = Provider(FakeClient(_LAST_QUOTE_RESPONSE))
        result = provider.forex_last_quote("USD", "EUR")
        assert isinstance(result, dict)
        assert "ask" in result
        assert "bid" in result
        assert "timestamp" in result

    def test_calls_correct_path_uppercase(self) -> None:
        client = FakeClient(_LAST_QUOTE_RESPONSE)
        provider = Provider(client)
        provider.forex_last_quote("usd", "eur")
        assert client.last_path == "/v1/last_quote/currencies/USD/EUR"


class TestForexQuotes:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_QUOTES_RESPONSE))
        result = provider.forex_quotes("C:EURUSD")
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_QUOTES_RESPONSE)
        provider = Provider(client)
        provider.forex_quotes("C:EURUSD")
        assert client.last_path == "/v3/quotes/C:EURUSD"

    def test_default_limit(self) -> None:
        client = FakeClient(_QUOTES_RESPONSE)
        provider = Provider(client)
        provider.forex_quotes("C:EURUSD")
        assert client.last_params.get("limit") == 100


class TestForexSnapshotAll:
    def test_returns_list_of_dicts(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.forex_snapshot_all()
        assert isinstance(result, list)
        assert result[0]["ticker"] == "C:EURUSD"

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.forex_snapshot_all()
        assert client.last_path == "/v2/snapshot/locale/global/markets/forex/tickers"

    def test_passes_tickers_param_when_given(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.forex_snapshot_all(tickers=["C:EURUSD", "C:GBPUSD"])
        assert "tickers" in client.last_params


class TestForexGainers:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.forex_gainers()
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.forex_gainers()
        assert client.last_path == "/v2/snapshot/locale/global/markets/forex/gainers"


class TestForexLosers:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.forex_losers()
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.forex_losers()
        assert client.last_path == "/v2/snapshot/locale/global/markets/forex/losers"


# ---------------------------------------------------------------------------
# Crypto tests
# ---------------------------------------------------------------------------


class TestCryptoPrevClose:
    def test_returns_dict_with_expected_keys(self) -> None:
        provider = Provider(FakeClient(_PREV_CLOSE_RESPONSE))
        result = provider.crypto_prev_close("X:BTCUSD")
        assert isinstance(result, dict)
        assert "ticker" in result
        assert "close" in result

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_PREV_CLOSE_RESPONSE)
        provider = Provider(client)
        provider.crypto_prev_close("X:BTCUSD")
        assert client.last_path == "/v2/aggs/ticker/X:BTCUSD/prev"


class TestCryptoBars:
    def test_returns_dataframe(self) -> None:
        provider = Provider(FakeClient(_AGGS_RESPONSE))
        df = provider.crypto_bars("X:BTCUSD", 1, "day", "2024-01-01", "2024-01-31")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_AGGS_RESPONSE)
        provider = Provider(client)
        provider.crypto_bars("X:BTCUSD", 1, "day", "2024-01-01", "2024-01-31")
        assert client.last_path == "/v2/aggs/ticker/X:BTCUSD/range/1/day/2024-01-01/2024-01-31"

    def test_default_sort_and_limit(self) -> None:
        client = FakeClient(_AGGS_RESPONSE)
        provider = Provider(client)
        provider.crypto_bars("X:BTCUSD", 1, "hour", "2024-01-01", "2024-01-31")
        assert client.last_params.get("sort") == "asc"
        assert client.last_params.get("limit") == 50000


class TestCryptoSnapshotAll:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.crypto_snapshot_all()
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.crypto_snapshot_all()
        assert client.last_path == "/v2/snapshot/locale/global/markets/crypto/tickers"


class TestCryptoSnapshot:
    def test_returns_dict(self) -> None:
        provider = Provider(FakeClient(_CRYPTO_SNAPSHOT_RESPONSE))
        result = provider.crypto_snapshot("X:BTCUSD")
        assert isinstance(result, dict)
        assert result["ticker"] == "X:BTCUSD"

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_CRYPTO_SNAPSHOT_RESPONSE)
        provider = Provider(client)
        provider.crypto_snapshot("X:BTCUSD")
        assert client.last_path == "/v2/snapshot/locale/global/markets/crypto/tickers/X:BTCUSD"


class TestCryptoGainers:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.crypto_gainers()
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.crypto_gainers()
        assert client.last_path == "/v2/snapshot/locale/global/markets/crypto/gainers"


class TestCryptoLosers:
    def test_returns_list(self) -> None:
        provider = Provider(FakeClient(_SNAPSHOTS_RESPONSE))
        result = provider.crypto_losers()
        assert isinstance(result, list)

    def test_calls_correct_path(self) -> None:
        client = FakeClient(_SNAPSHOTS_RESPONSE)
        provider = Provider(client)
        provider.crypto_losers()
        assert client.last_path == "/v2/snapshot/locale/global/markets/crypto/losers"


class TestCryptoDailyOhlc:
    def test_returns_dict_with_ohlcv(self) -> None:
        provider = Provider(FakeClient(_DAILY_OHLC_RESPONSE))
        result = provider.crypto_daily_ohlc("BTC", "USD", "2024-01-01")
        assert isinstance(result, dict)
        assert "symbol" in result
        assert "date" in result
        assert "open" in result
        assert "close" in result
        assert "volume" in result

    def test_calls_correct_path_uppercase(self) -> None:
        client = FakeClient(_DAILY_OHLC_RESPONSE)
        provider = Provider(client)
        provider.crypto_daily_ohlc("btc", "usd", "2024-01-01")
        assert client.last_path == "/v1/open-close/crypto/BTC/USD/2024-01-01"
