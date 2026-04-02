"""Tests for IndicesMixin — Polygon.io indices endpoints."""
from __future__ import annotations

from typing import Any

import pandas as pd
import pytest

from finance_mcp.providers.massive.indices import IndicesMixin


# ---------------------------------------------------------------------------
# FakeClient helper
# ---------------------------------------------------------------------------


class FakeClient:
    """Minimal stand-in for MassiveClient that records calls and returns canned data."""

    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response
        self.last_path: str = ""
        self.last_params: dict[str, Any] = {}

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.last_path = path
        self.last_params = params or {}
        return self._response


class FakeIndices(IndicesMixin):
    """Concrete subclass that binds FakeClient as self.client."""

    def __init__(self, response: dict[str, Any]) -> None:
        self.client: FakeClient = FakeClient(response)


# ---------------------------------------------------------------------------
# Fixtures — canned API response payloads
# ---------------------------------------------------------------------------

PREV_CLOSE_RAW: dict[str, Any] = {
    "resultsCount": 1,
    "results": [
        {
            "T": "I:SPX",
            "o": 4700.0,
            "h": 4750.0,
            "l": 4680.0,
            "c": 4730.0,
            "v": 0.0,
            "t": 1704067200000,
        }
    ],
}

AGGS_RAW: dict[str, Any] = {
    "resultsCount": 2,
    "results": [
        {"t": 1704067200000, "o": 4700.0, "h": 4750.0, "l": 4680.0, "c": 4730.0, "v": 0.0},
        {"t": 1704153600000, "o": 4730.0, "h": 4780.0, "l": 4710.0, "c": 4760.0, "v": 0.0},
    ],
}

SNAPSHOT_RAW: dict[str, Any] = {
    "results": [
        {
            "ticker": "I:SPX",
            "value": 4730.0,
            "todaysChangePerc": 0.64,
            "todaysChange": 30.0,
            "updated": 1704067200000,
        },
        {
            "ticker": "I:NDX",
            "value": 16500.0,
            "todaysChangePerc": 0.82,
            "todaysChange": 135.0,
            "updated": 1704067200000,
        },
    ]
}

UNIFIED_SNAPSHOT_RAW: dict[str, Any] = {
    "results": [
        {"ticker": "I:SPX", "value": 4730.0},
        {"ticker": "I:DJI", "value": 37000.0},
    ]
}

DAILY_OHLC_RAW: dict[str, Any] = {
    "symbol": "I:SPX",
    "from": "2024-01-02",
    "open": 4700.0,
    "high": 4750.0,
    "low": 4680.0,
    "close": 4730.0,
    "volume": 0.0,
}

INDICATOR_RAW: dict[str, Any] = {
    "results": {
        "values": [
            {"timestamp": 1704067200000, "value": 4650.0},
            {"timestamp": 1703980800000, "value": 4630.0},
        ]
    }
}


# ---------------------------------------------------------------------------
# indices_prev_close
# ---------------------------------------------------------------------------


class TestIndicesPrevClose:
    def test_returns_dict(self) -> None:
        mixin = FakeIndices(PREV_CLOSE_RAW)
        result = mixin.indices_prev_close("I:SPX")
        assert isinstance(result, dict)

    def test_ticker_in_result(self) -> None:
        mixin = FakeIndices(PREV_CLOSE_RAW)
        result = mixin.indices_prev_close("I:SPX")
        assert result["ticker"] == "I:SPX"

    def test_close_value(self) -> None:
        mixin = FakeIndices(PREV_CLOSE_RAW)
        result = mixin.indices_prev_close("I:SPX")
        assert result["close"] == 4730.0

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(PREV_CLOSE_RAW)
        mixin.indices_prev_close("I:SPX")
        assert mixin.client.last_path == "/v2/aggs/ticker/I:SPX/prev"

    def test_ticker_not_uppercased(self) -> None:
        """Index tickers like 'I:SPX' must be passed as-is, not double-uppercased."""
        mixin = FakeIndices(PREV_CLOSE_RAW)
        mixin.indices_prev_close("I:spx")
        # Path must preserve the original casing (spec says don't uppercase)
        assert "I:spx" in mixin.client.last_path


# ---------------------------------------------------------------------------
# indices_bars
# ---------------------------------------------------------------------------


class TestIndicesBars:
    def test_returns_dataframe(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        df = mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert isinstance(df, pd.DataFrame)

    def test_dataframe_columns(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        df = mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_dataframe_row_count(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        df = mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert len(df) == 2

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert mixin.client.last_path == "/v2/aggs/ticker/I:SPX/range/1/day/2024-01-01/2024-01-02"

    def test_default_params_sent(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert mixin.client.last_params["sort"] == "asc"
        assert mixin.client.last_params["limit"] == 50000

    def test_custom_sort_and_limit(self) -> None:
        mixin = FakeIndices(AGGS_RAW)
        mixin.indices_bars("I:SPX", 5, "minute", "2024-01-01", "2024-01-02", sort="desc", limit=100)
        assert mixin.client.last_params["sort"] == "desc"
        assert mixin.client.last_params["limit"] == 100

    def test_empty_results_returns_empty_dataframe(self) -> None:
        mixin = FakeIndices({"results": []})
        df = mixin.indices_bars("I:SPX", 1, "day", "2024-01-01", "2024-01-02")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


# ---------------------------------------------------------------------------
# indices_snapshot
# ---------------------------------------------------------------------------


class TestIndicesSnapshot:
    def test_returns_list(self) -> None:
        mixin = FakeIndices(SNAPSHOT_RAW)
        result = mixin.indices_snapshot(["I:SPX", "I:NDX"])
        assert isinstance(result, list)

    def test_returns_two_items(self) -> None:
        mixin = FakeIndices(SNAPSHOT_RAW)
        result = mixin.indices_snapshot(["I:SPX", "I:NDX"])
        assert len(result) == 2

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(SNAPSHOT_RAW)
        mixin.indices_snapshot(["I:SPX", "I:NDX"])
        assert mixin.client.last_path == "/v3/snapshot/indices"

    def test_ticker_any_of_param(self) -> None:
        mixin = FakeIndices(SNAPSHOT_RAW)
        mixin.indices_snapshot(["I:SPX", "I:NDX"])
        assert mixin.client.last_params["ticker.any_of"] == "I:SPX,I:NDX"

    def test_single_ticker(self) -> None:
        mixin = FakeIndices({"results": [SNAPSHOT_RAW["results"][0]]})
        result = mixin.indices_snapshot(["I:SPX"])
        assert len(result) == 1


# ---------------------------------------------------------------------------
# indices_unified_snapshot
# ---------------------------------------------------------------------------


class TestIndicesUnifiedSnapshot:
    def test_returns_list(self) -> None:
        mixin = FakeIndices(UNIFIED_SNAPSHOT_RAW)
        result = mixin.indices_unified_snapshot(["I:SPX", "I:DJI"])
        assert isinstance(result, list)

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(UNIFIED_SNAPSHOT_RAW)
        mixin.indices_unified_snapshot(["I:SPX", "I:DJI"])
        assert mixin.client.last_path == "/v3/snapshot"

    def test_ticker_any_of_param(self) -> None:
        mixin = FakeIndices(UNIFIED_SNAPSHOT_RAW)
        mixin.indices_unified_snapshot(["I:SPX", "I:DJI"])
        assert mixin.client.last_params["ticker.any_of"] == "I:SPX,I:DJI"


# ---------------------------------------------------------------------------
# indices_daily_ohlc
# ---------------------------------------------------------------------------


class TestIndicesDailyOhlc:
    def test_returns_dict(self) -> None:
        mixin = FakeIndices(DAILY_OHLC_RAW)
        result = mixin.indices_daily_ohlc("I:SPX", "2024-01-02")
        assert isinstance(result, dict)

    def test_symbol_in_result(self) -> None:
        mixin = FakeIndices(DAILY_OHLC_RAW)
        result = mixin.indices_daily_ohlc("I:SPX", "2024-01-02")
        assert result["symbol"] == "I:SPX"

    def test_ohlcv_fields_present(self) -> None:
        mixin = FakeIndices(DAILY_OHLC_RAW)
        result = mixin.indices_daily_ohlc("I:SPX", "2024-01-02")
        for field in ("open", "high", "low", "close", "volume"):
            assert field in result

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(DAILY_OHLC_RAW)
        mixin.indices_daily_ohlc("I:SPX", "2024-01-02")
        assert mixin.client.last_path == "/v1/open-close/I:SPX/2024-01-02"


# ---------------------------------------------------------------------------
# indices_sma
# ---------------------------------------------------------------------------


class TestIndicesSma:
    def test_returns_series(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        result = mixin.indices_sma("I:SPX")
        assert isinstance(result, pd.Series)

    def test_series_length(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        result = mixin.indices_sma("I:SPX")
        assert len(result) == 2

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_sma("I:SPX")
        assert mixin.client.last_path == "/v1/indicators/sma/I:SPX"

    def test_default_params_sent(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_sma("I:SPX")
        params = mixin.client.last_params
        assert params["window"] == 50
        assert params["timespan"] == "day"
        assert params["series_type"] == "close"

    def test_custom_window(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_sma("I:SPX", window=200)
        assert mixin.client.last_params["window"] == 200

    def test_empty_results_returns_empty_series(self) -> None:
        mixin = FakeIndices({"results": {"values": []}})
        result = mixin.indices_sma("I:SPX")
        assert isinstance(result, pd.Series)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# indices_ema
# ---------------------------------------------------------------------------


class TestIndicesEma:
    def test_returns_series(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        result = mixin.indices_ema("I:SPX")
        assert isinstance(result, pd.Series)

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_ema("I:SPX")
        assert mixin.client.last_path == "/v1/indicators/ema/I:SPX"

    def test_default_window(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_ema("I:SPX")
        assert mixin.client.last_params["window"] == 50


# ---------------------------------------------------------------------------
# indices_rsi
# ---------------------------------------------------------------------------


class TestIndicesRsi:
    def test_returns_series(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        result = mixin.indices_rsi("I:SPX")
        assert isinstance(result, pd.Series)

    def test_correct_path_called(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_rsi("I:SPX")
        assert mixin.client.last_path == "/v1/indicators/rsi/I:SPX"

    def test_default_window_14(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_rsi("I:SPX")
        assert mixin.client.last_params["window"] == 14

    def test_custom_timespan(self) -> None:
        mixin = FakeIndices(INDICATOR_RAW)
        mixin.indices_rsi("I:SPX", timespan="week")
        assert mixin.client.last_params["timespan"] == "week"
