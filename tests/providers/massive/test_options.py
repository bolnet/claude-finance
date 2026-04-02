"""Tests for Polygon.io OptionsMixin.

TDD: Tests written before implementation.
Uses FakeClient to avoid real HTTP calls.
"""
from __future__ import annotations

from typing import Any

import pytest

from finance_mcp.providers.massive.options import OptionsMixin


# ---------------------------------------------------------------------------
# FakeClient
# ---------------------------------------------------------------------------


class FakeClient:
    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response
        self.last_path: str = ""
        self.last_params: dict[str, Any] | None = None

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.last_path = path
        self.last_params = params
        return self._response


# ---------------------------------------------------------------------------
# Concrete mixin host for testing
# ---------------------------------------------------------------------------


class FakeProvider(OptionsMixin):
    def __init__(self, response: dict[str, Any]) -> None:
        self.client = FakeClient(response)


# ---------------------------------------------------------------------------
# Sample raw payloads
# ---------------------------------------------------------------------------

OPTIONS_CONTRACTS_RAW: dict[str, Any] = {
    "results": [
        {
            "ticker": "O:AAPL230616C00150000",
            "underlying_ticker": "AAPL",
            "contract_type": "call",
            "strike_price": 150.0,
            "expiration_date": "2023-06-16",
        },
        {
            "ticker": "O:AAPL230616P00150000",
            "underlying_ticker": "AAPL",
            "contract_type": "put",
            "strike_price": 150.0,
            "expiration_date": "2023-06-16",
        },
    ]
}

PREV_CLOSE_RAW: dict[str, Any] = {
    "ticker": "O:AAPL230616C00150000",
    "resultsCount": 1,
    "results": [
        {
            "T": "O:AAPL230616C00150000",
            "o": 5.0,
            "h": 5.5,
            "l": 4.8,
            "c": 5.2,
            "v": 200,
            "t": 1704067200000,
        }
    ],
}

OPTIONS_CHAIN_RAW: dict[str, Any] = {
    "results": [
        {
            "details": {
                "strike_price": 150.0,
                "expiration_date": "2023-06-16",
                "contract_type": "call",
            },
            "greeks": {"delta": 0.65, "gamma": 0.02, "theta": -0.05, "vega": 0.10},
            "implied_volatility": 0.30,
            "open_interest": 1500,
            "last_quote": {"last_price": 5.2},
            "day": {"volume": 200},
        }
    ]
}

OPTIONS_SINGLE_SNAPSHOT_RAW: dict[str, Any] = {
    "results": {
        "details": {
            "strike_price": 150.0,
            "expiration_date": "2023-06-16",
            "contract_type": "call",
            "ticker": "O:AAPL230616C00150000",
        },
        "greeks": {"delta": 0.65, "gamma": 0.02, "theta": -0.05, "vega": 0.10},
        "implied_volatility": 0.30,
        "open_interest": 1500,
        "last_quote": {"last_price": 5.2},
        "day": {"volume": 200},
    }
}


# ---------------------------------------------------------------------------
# Tests: options_contracts
# ---------------------------------------------------------------------------


class TestOptionsContracts:
    def test_returns_list_of_results(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        result = provider.options_contracts("AAPL")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_calls_correct_path(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL")
        assert provider.client.last_path == "/v3/reference/options/contracts"

    def test_sends_underlying_ticker_param(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL")
        assert provider.client.last_params is not None
        assert provider.client.last_params["underlying_ticker"] == "AAPL"

    def test_default_limit_param(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL")
        assert provider.client.last_params is not None
        assert provider.client.last_params["limit"] == 100

    def test_custom_limit_param(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL", limit=50)
        assert provider.client.last_params is not None
        assert provider.client.last_params["limit"] == 50

    def test_optional_contract_type_included(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL", contract_type="call")
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("contract_type") == "call"

    def test_optional_expiration_date_included(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL", expiration_date="2023-06-16")
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("expiration_date") == "2023-06-16"

    def test_optional_strike_price_included(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL", strike_price=150.0)
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("strike_price") == 150.0

    def test_none_optionals_not_in_params(self) -> None:
        provider = FakeProvider(OPTIONS_CONTRACTS_RAW)
        provider.options_contracts("AAPL")
        params = provider.client.last_params or {}
        assert "contract_type" not in params
        assert "expiration_date" not in params
        assert "strike_price" not in params

    def test_empty_results_returns_empty_list(self) -> None:
        provider = FakeProvider({"results": []})
        result = provider.options_contracts("AAPL")
        assert result == []

    def test_missing_results_key_returns_empty_list(self) -> None:
        provider = FakeProvider({})
        result = provider.options_contracts("AAPL")
        assert result == []


# ---------------------------------------------------------------------------
# Tests: options_prev_close
# ---------------------------------------------------------------------------


class TestOptionsPrevClose:
    def test_returns_dict(self) -> None:
        provider = FakeProvider(PREV_CLOSE_RAW)
        result = provider.options_prev_close("O:AAPL230616C00150000")
        assert isinstance(result, dict)

    def test_calls_correct_path(self) -> None:
        provider = FakeProvider(PREV_CLOSE_RAW)
        provider.options_prev_close("O:AAPL230616C00150000")
        assert provider.client.last_path == "/v2/aggs/ticker/O:AAPL230616C00150000/prev"

    def test_result_has_expected_keys(self) -> None:
        provider = FakeProvider(PREV_CLOSE_RAW)
        result = provider.options_prev_close("O:AAPL230616C00150000")
        assert "ticker" in result
        assert "open" in result
        assert "close" in result
        assert "volume" in result

    def test_result_values_are_correct(self) -> None:
        provider = FakeProvider(PREV_CLOSE_RAW)
        result = provider.options_prev_close("O:AAPL230616C00150000")
        assert result["ticker"] == "O:AAPL230616C00150000"
        assert result["open"] == 5.0
        assert result["close"] == 5.2
        assert result["volume"] == 200

    def test_empty_results_returns_none_values(self) -> None:
        provider = FakeProvider({"results": []})
        result = provider.options_prev_close("O:AAPL230616C00150000")
        assert result["ticker"] is None
        assert result["close"] is None


# ---------------------------------------------------------------------------
# Tests: options_chain_snapshot
# ---------------------------------------------------------------------------


class TestOptionsChainSnapshot:
    def test_returns_list(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        result = provider.options_chain_snapshot("AAPL")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_calls_correct_path(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL")
        assert provider.client.last_path == "/v3/snapshot/options/AAPL"

    def test_default_limit_param(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL")
        assert provider.client.last_params is not None
        assert provider.client.last_params["limit"] == 250

    def test_optional_contract_type_included(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL", contract_type="call")
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("contract_type") == "call"

    def test_optional_expiration_date_included(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL", expiration_date="2023-06-16")
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("expiration_date") == "2023-06-16"

    def test_optional_strike_price_included(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL", strike_price=150.0)
        assert provider.client.last_params is not None
        assert provider.client.last_params.get("strike_price") == 150.0

    def test_none_optionals_not_in_params(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        provider.options_chain_snapshot("AAPL")
        params = provider.client.last_params or {}
        assert "contract_type" not in params
        assert "expiration_date" not in params
        assert "strike_price" not in params

    def test_contract_fields_present(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        result = provider.options_chain_snapshot("AAPL")
        contract = result[0]
        assert "strike_price" in contract
        assert "expiration_date" in contract
        assert "contract_type" in contract
        assert "delta" in contract
        assert "implied_volatility" in contract
        assert "open_interest" in contract

    def test_contract_values_correct(self) -> None:
        provider = FakeProvider(OPTIONS_CHAIN_RAW)
        result = provider.options_chain_snapshot("AAPL")
        contract = result[0]
        assert contract["strike_price"] == 150.0
        assert contract["delta"] == 0.65
        assert contract["implied_volatility"] == 0.30
        assert contract["open_interest"] == 1500


# ---------------------------------------------------------------------------
# Tests: options_single_snapshot
# ---------------------------------------------------------------------------


class TestOptionsSingleSnapshot:
    def test_returns_dict(self) -> None:
        provider = FakeProvider(OPTIONS_SINGLE_SNAPSHOT_RAW)
        result = provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        assert isinstance(result, dict)

    def test_calls_correct_path(self) -> None:
        provider = FakeProvider(OPTIONS_SINGLE_SNAPSHOT_RAW)
        provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        assert provider.client.last_path == "/v3/snapshot/options/AAPL/O:AAPL230616C00150000"

    def test_result_has_expected_keys(self) -> None:
        provider = FakeProvider(OPTIONS_SINGLE_SNAPSHOT_RAW)
        result = provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        assert "details" in result
        assert "greeks" in result
        assert "implied_volatility" in result
        assert "open_interest" in result
        assert "last_price" in result
        assert "volume" in result

    def test_result_values_correct(self) -> None:
        provider = FakeProvider(OPTIONS_SINGLE_SNAPSHOT_RAW)
        result = provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        assert result["implied_volatility"] == 0.30
        assert result["open_interest"] == 1500
        assert result["last_price"] == 5.2
        assert result["volume"] == 200

    def test_greeks_present(self) -> None:
        provider = FakeProvider(OPTIONS_SINGLE_SNAPSHOT_RAW)
        result = provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        greeks = result["greeks"]
        assert greeks["delta"] == 0.65
        assert greeks["gamma"] == 0.02
        assert greeks["theta"] == -0.05
        assert greeks["vega"] == 0.10

    def test_empty_result_returns_none_values(self) -> None:
        provider = FakeProvider({"results": {}})
        result = provider.options_single_snapshot("AAPL", "O:AAPL230616C00150000")
        assert result["implied_volatility"] is None
        assert result["open_interest"] is None
        assert result["last_price"] is None
        assert result["volume"] is None
