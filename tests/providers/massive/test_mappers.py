"""Tests for Polygon.io response mapper functions.

TDD: These tests are written before the implementation.
Each mapper converts raw Polygon JSON → pandas / plain Python structures.
"""
from __future__ import annotations

import pandas as pd
import pytest

from finance_mcp.providers.massive.mappers import (
    aggs_to_dataframe,
    dividends_to_list,
    indicator_to_series,
    news_to_list,
    options_chain_to_list,
    prev_close_to_dict,
    snapshot_to_dict,
    snapshots_to_list,
    splits_to_list,
    ticker_details_to_dict,
    trades_to_dataframe,
)


# ---------------------------------------------------------------------------
# Fixtures / sample raw payloads
# ---------------------------------------------------------------------------

AGG_RAW = {
    "ticker": "AAPL",
    "resultsCount": 3,
    "results": [
        {"t": 1704067200000, "o": 185.0, "h": 187.5, "l": 184.0, "c": 186.5, "v": 1_000_000},
        {"t": 1704153600000, "o": 186.5, "h": 189.0, "l": 185.5, "c": 188.0, "v": 1_200_000},
        {"t": 1704240000000, "o": 188.0, "h": 190.0, "l": 187.0, "c": 189.5, "v": 900_000},
    ],
}

PREV_CLOSE_RAW = {
    "ticker": "AAPL",
    "resultsCount": 1,
    "results": [
        {
            "T": "AAPL",
            "o": 185.0,
            "h": 187.5,
            "l": 184.0,
            "c": 186.5,
            "v": 1_000_000,
            "t": 1704067200000,
        }
    ],
}

SNAPSHOT_TICKER_RAW = {
    "ticker": {
        "ticker": "AAPL",
        "todaysChange": 2.5,
        "todaysChangePerc": 1.35,
        "day": {"o": 185.0, "h": 187.5, "l": 184.0, "c": 186.5, "v": 1_000_000},
        "prevDay": {"c": 184.0},
    }
}

SNAPSHOT_TICKERS_RAW = {
    "tickers": [
        {
            "ticker": "AAPL",
            "todaysChange": 2.5,
            "todaysChangePerc": 1.35,
            "day": {"o": 185.0, "h": 187.5, "l": 184.0, "c": 186.5, "v": 1_000_000},
            "prevDay": {"c": 184.0},
        },
        {
            "ticker": "MSFT",
            "todaysChange": -1.0,
            "todaysChangePerc": -0.3,
            "day": {"o": 300.0, "h": 305.0, "l": 299.0, "c": 301.0, "v": 500_000},
            "prevDay": {"c": 302.0},
        },
    ]
}

NEWS_RAW = {
    "results": [
        {
            "title": "Apple hits record high",
            "published_utc": "2024-01-02T10:00:00Z",
            "article_url": "https://example.com/article1",
            "author": "Jane Doe",
            "description": "Apple stock surged today.",
            "tickers": ["AAPL"],
        },
        {
            "title": "Market roundup",
            "published_utc": "2024-01-02T18:00:00Z",
            "article_url": "https://example.com/article2",
            "author": "John Smith",
            "description": "Markets closed mixed.",
            "tickers": ["AAPL", "MSFT"],
        },
    ]
}

OPTIONS_CHAIN_RAW = {
    "results": [
        {
            "details": {
                "strike_price": 180.0,
                "expiration_date": "2024-06-21",
                "contract_type": "call",
            },
            "greeks": {"delta": 0.65, "gamma": 0.02, "theta": -0.05, "vega": 0.12},
            "implied_volatility": 0.28,
            "open_interest": 5000,
            "last_quote": {"last_price": 8.5},
            "day": {"volume": 200},
        }
    ]
}

TRADES_RAW = {
    "results": [
        {"p": 186.5, "s": 100, "t": 1704067200000000000, "x": 4},
        {"p": 186.6, "s": 200, "t": 1704067200100000000, "x": 4},
    ]
}

INDICATOR_RAW = {
    "results": {
        "values": [
            {"timestamp": 1704067200000, "value": 185.5},
            {"timestamp": 1704153600000, "value": 186.0},
            {"timestamp": 1704240000000, "value": 187.0},
        ]
    }
}

DIVIDENDS_RAW = {
    "results": [
        {
            "ex_dividend_date": "2024-02-09",
            "pay_date": "2024-02-15",
            "cash_amount": 0.24,
            "frequency": 4,
        }
    ]
}

SPLITS_RAW = {
    "results": [
        {
            "execution_date": "2020-08-31",
            "split_from": 1,
            "split_to": 4,
        }
    ]
}

TICKER_DETAILS_RAW = {
    "results": {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "market": "stocks",
        "locale": "us",
        "type": "CS",
        "currency_name": "usd",
        "market_cap": 3_000_000_000_000,
        "description": "Apple designs consumer electronics.",
        "sic_code": "3571",
        "sic_description": "Electronic Computers",
        "homepage_url": "https://www.apple.com",
        "total_employees": 150_000,
        "list_date": "1980-12-12",
        "share_class_shares_outstanding": 15_500_000_000,
        "weighted_shares_outstanding": 15_400_000_000,
    }
}


# ---------------------------------------------------------------------------
# aggs_to_dataframe
# ---------------------------------------------------------------------------


class TestAggsToDataframe:
    def test_converts_ohlcv_columns(self) -> None:
        df = aggs_to_dataframe(AGG_RAW)
        assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_returns_datetime_index_utc(self) -> None:
        df = aggs_to_dataframe(AGG_RAW)
        assert isinstance(df.index, pd.DatetimeIndex)
        assert str(df.index.tz) == "UTC"

    def test_row_count_matches_results(self) -> None:
        df = aggs_to_dataframe(AGG_RAW)
        assert len(df) == 3

    def test_values_are_correct(self) -> None:
        df = aggs_to_dataframe(AGG_RAW)
        assert df["Open"].iloc[0] == pytest.approx(185.0)
        assert df["Close"].iloc[0] == pytest.approx(186.5)
        assert df["Volume"].iloc[0] == 1_000_000

    def test_empty_results_returns_empty_dataframe(self) -> None:
        raw = {"ticker": "AAPL", "results": []}
        df = aggs_to_dataframe(raw)
        assert df.empty
        assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_missing_results_key_returns_empty_dataframe(self) -> None:
        df = aggs_to_dataframe({"ticker": "AAPL"})
        assert df.empty


# ---------------------------------------------------------------------------
# prev_close_to_dict
# ---------------------------------------------------------------------------


class TestPrevCloseToDict:
    def test_extracts_all_fields(self) -> None:
        result = prev_close_to_dict(PREV_CLOSE_RAW)
        assert result["ticker"] == "AAPL"
        assert result["open"] == pytest.approx(185.0)
        assert result["high"] == pytest.approx(187.5)
        assert result["low"] == pytest.approx(184.0)
        assert result["close"] == pytest.approx(186.5)
        assert result["volume"] == 1_000_000
        assert result["timestamp"] == 1704067200000

    def test_keys_are_snake_case(self) -> None:
        result = prev_close_to_dict(PREV_CLOSE_RAW)
        assert "open" in result
        assert "close" in result


# ---------------------------------------------------------------------------
# snapshot_to_dict
# ---------------------------------------------------------------------------


class TestSnapshotToDict:
    def test_ticker_shape(self) -> None:
        result = snapshot_to_dict(SNAPSHOT_TICKER_RAW)
        assert result["ticker"] == "AAPL"
        assert result["change"] == pytest.approx(2.5)
        assert result["change_percent"] == pytest.approx(1.35)
        assert result["open"] == pytest.approx(185.0)
        assert result["close"] == pytest.approx(186.5)
        assert result["volume"] == 1_000_000
        assert result["prev_close"] == pytest.approx(184.0)

    def test_tickers_shape_uses_first(self) -> None:
        result = snapshot_to_dict(SNAPSHOT_TICKERS_RAW)
        assert result["ticker"] == "AAPL"

    def test_missing_prev_day_returns_none(self) -> None:
        raw = {
            "ticker": {
                "ticker": "AAPL",
                "todaysChange": 0,
                "todaysChangePerc": 0,
                "day": {"o": 185.0, "h": 187.5, "l": 184.0, "c": 186.5, "v": 0},
            }
        }
        result = snapshot_to_dict(raw)
        assert result["prev_close"] is None


# ---------------------------------------------------------------------------
# snapshots_to_list
# ---------------------------------------------------------------------------


class TestSnapshotsToList:
    def test_returns_list_of_dicts(self) -> None:
        result = snapshots_to_list(SNAPSHOT_TICKERS_RAW)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_each_item_has_ticker(self) -> None:
        result = snapshots_to_list(SNAPSHOT_TICKERS_RAW)
        tickers = [r["ticker"] for r in result]
        assert "AAPL" in tickers
        assert "MSFT" in tickers

    def test_empty_tickers_returns_empty_list(self) -> None:
        result = snapshots_to_list({"tickers": []})
        assert result == []


# ---------------------------------------------------------------------------
# news_to_list
# ---------------------------------------------------------------------------


class TestNewsToList:
    def test_returns_correct_count(self) -> None:
        result = news_to_list(NEWS_RAW)
        assert len(result) == 2

    def test_extracts_required_fields(self) -> None:
        result = news_to_list(NEWS_RAW)
        item = result[0]
        assert item["title"] == "Apple hits record high"
        assert item["published_utc"] == "2024-01-02T10:00:00Z"
        assert item["article_url"] == "https://example.com/article1"
        assert item["author"] == "Jane Doe"
        assert item["description"] == "Apple stock surged today."
        assert item["tickers"] == ["AAPL"]

    def test_empty_results_returns_empty_list(self) -> None:
        assert news_to_list({"results": []}) == []

    def test_missing_results_returns_empty_list(self) -> None:
        assert news_to_list({}) == []


# ---------------------------------------------------------------------------
# options_chain_to_list
# ---------------------------------------------------------------------------


class TestOptionsChainToList:
    def test_returns_list(self) -> None:
        result = options_chain_to_list(OPTIONS_CHAIN_RAW)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_extracts_contract_details(self) -> None:
        result = options_chain_to_list(OPTIONS_CHAIN_RAW)
        item = result[0]
        assert item["strike_price"] == pytest.approx(180.0)
        assert item["expiration_date"] == "2024-06-21"
        assert item["contract_type"] == "call"

    def test_extracts_greeks(self) -> None:
        result = options_chain_to_list(OPTIONS_CHAIN_RAW)
        item = result[0]
        assert item["delta"] == pytest.approx(0.65)
        assert item["gamma"] == pytest.approx(0.02)
        assert item["theta"] == pytest.approx(-0.05)
        assert item["vega"] == pytest.approx(0.12)

    def test_extracts_implied_volatility_and_oi(self) -> None:
        result = options_chain_to_list(OPTIONS_CHAIN_RAW)
        item = result[0]
        assert item["implied_volatility"] == pytest.approx(0.28)
        assert item["open_interest"] == 5000

    def test_missing_greeks_uses_none(self) -> None:
        raw = {
            "results": [
                {
                    "details": {
                        "strike_price": 180.0,
                        "expiration_date": "2024-06-21",
                        "contract_type": "call",
                    },
                    "implied_volatility": 0.28,
                    "open_interest": 5000,
                }
            ]
        }
        result = options_chain_to_list(raw)
        assert result[0]["delta"] is None


# ---------------------------------------------------------------------------
# trades_to_dataframe
# ---------------------------------------------------------------------------


class TestTradesToDataframe:
    def test_columns(self) -> None:
        df = trades_to_dataframe(TRADES_RAW)
        assert "price" in df.columns
        assert "size" in df.columns
        assert "timestamp" in df.columns
        assert "exchange" in df.columns

    def test_row_count(self) -> None:
        df = trades_to_dataframe(TRADES_RAW)
        assert len(df) == 2

    def test_empty_results_returns_empty_dataframe(self) -> None:
        df = trades_to_dataframe({"results": []})
        assert df.empty

    def test_missing_results_returns_empty_dataframe(self) -> None:
        df = trades_to_dataframe({})
        assert df.empty

    def test_timestamp_converted_from_ns(self) -> None:
        df = trades_to_dataframe(TRADES_RAW)
        # timestamp should be datetime with UTC timezone
        assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])


# ---------------------------------------------------------------------------
# indicator_to_series
# ---------------------------------------------------------------------------


class TestIndicatorToSeries:
    def test_returns_series(self) -> None:
        s = indicator_to_series(INDICATOR_RAW)
        assert isinstance(s, pd.Series)

    def test_index_is_datetime_utc(self) -> None:
        s = indicator_to_series(INDICATOR_RAW)
        assert isinstance(s.index, pd.DatetimeIndex)
        assert str(s.index.tz) == "UTC"

    def test_values_are_correct(self) -> None:
        s = indicator_to_series(INDICATOR_RAW)
        assert s.iloc[0] == pytest.approx(185.5)
        assert len(s) == 3

    def test_empty_values_returns_empty_series(self) -> None:
        s = indicator_to_series({"results": {"values": []}})
        assert s.empty

    def test_missing_results_returns_empty_series(self) -> None:
        s = indicator_to_series({})
        assert s.empty


# ---------------------------------------------------------------------------
# dividends_to_list
# ---------------------------------------------------------------------------


class TestDividendsToList:
    def test_extracts_fields(self) -> None:
        result = dividends_to_list(DIVIDENDS_RAW)
        assert len(result) == 1
        item = result[0]
        assert item["ex_dividend_date"] == "2024-02-09"
        assert item["pay_date"] == "2024-02-15"
        assert item["cash_amount"] == pytest.approx(0.24)
        assert item["frequency"] == 4

    def test_empty_results_returns_empty_list(self) -> None:
        assert dividends_to_list({"results": []}) == []


# ---------------------------------------------------------------------------
# splits_to_list
# ---------------------------------------------------------------------------


class TestSplitsToList:
    def test_extracts_fields(self) -> None:
        result = splits_to_list(SPLITS_RAW)
        assert len(result) == 1
        item = result[0]
        assert item["execution_date"] == "2020-08-31"
        assert item["split_from"] == 1
        assert item["split_to"] == 4

    def test_empty_results_returns_empty_list(self) -> None:
        assert splits_to_list({"results": []}) == []


# ---------------------------------------------------------------------------
# ticker_details_to_dict
# ---------------------------------------------------------------------------


class TestTickerDetailsToDict:
    def test_extracts_core_fields(self) -> None:
        result = ticker_details_to_dict(TICKER_DETAILS_RAW)
        assert result["ticker"] == "AAPL"
        assert result["name"] == "Apple Inc."
        assert result["market"] == "stocks"
        assert result["locale"] == "us"
        assert result["type"] == "CS"
        assert result["currency_name"] == "usd"

    def test_extracts_extended_fields(self) -> None:
        result = ticker_details_to_dict(TICKER_DETAILS_RAW)
        assert result["market_cap"] == 3_000_000_000_000
        assert result["description"] == "Apple designs consumer electronics."
        assert result["sic_code"] == "3571"
        assert result["sic_description"] == "Electronic Computers"
        assert result["homepage_url"] == "https://www.apple.com"
        assert result["total_employees"] == 150_000
        assert result["list_date"] == "1980-12-12"

    def test_extracts_shares_outstanding(self) -> None:
        result = ticker_details_to_dict(TICKER_DETAILS_RAW)
        assert result["share_class_shares_outstanding"] == 15_500_000_000
        assert result["weighted_shares_outstanding"] == 15_400_000_000

    def test_missing_optional_fields_return_none(self) -> None:
        minimal = {"results": {"ticker": "XYZ", "name": "XYZ Corp"}}
        result = ticker_details_to_dict(minimal)
        assert result["market_cap"] is None
        assert result["description"] is None
