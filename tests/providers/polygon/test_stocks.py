"""Tests for StocksMixin – all 30 stocks endpoints.

Uses a FakeClient to avoid real network calls.
"""
from __future__ import annotations

import pandas as pd

from finance_mcp.providers.polygon.stocks import StocksMixin


# ---------------------------------------------------------------------------
# FakeClient
# ---------------------------------------------------------------------------


class FakeClient:
    """Minimal test double for PolygonClient."""

    def __init__(self, response: object) -> None:
        self._response = response
        self.last_path: str = ""
        self.last_params: dict | None = None

    def get(self, path: str, params: dict | None = None) -> object:
        self.last_path = path
        self.last_params = params
        return self._response


# ---------------------------------------------------------------------------
# Concrete subclass that satisfies the mixin contract
# ---------------------------------------------------------------------------


class StocksProvider(StocksMixin):
    def __init__(self, response: object) -> None:
        self.client: FakeClient = FakeClient(response)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _aggs_raw(ticker: str = "AAPL") -> dict:
    return {
        "results": [
            {"T": ticker, "t": 1_700_000_000_000, "o": 1.0, "h": 2.0, "l": 0.5, "c": 1.5, "v": 1000},
        ]
    }


def _prev_close_raw(ticker: str = "AAPL") -> dict:
    return {
        "results": [
            {"T": ticker, "t": 1_700_000_000_000, "o": 150.0, "h": 155.0, "l": 148.0, "c": 153.0, "v": 500_000},
        ]
    }


def _snapshot_raw(ticker: str = "AAPL") -> dict:
    return {
        "ticker": {
            "ticker": ticker,
            "todaysChange": 2.5,
            "todaysChangePerc": 1.7,
            "day": {"o": 150.0, "h": 155.0, "l": 148.0, "c": 153.0, "v": 500_000},
            "prevDay": {"c": 150.5},
        }
    }


def _snapshots_raw() -> dict:
    return {
        "tickers": [
            {
                "ticker": "AAPL",
                "todaysChange": 2.5,
                "todaysChangePerc": 1.7,
                "day": {"o": 150.0, "h": 155.0, "l": 148.0, "c": 153.0, "v": 500_000},
                "prevDay": {"c": 150.5},
            }
        ]
    }


def _news_raw() -> dict:
    return {
        "results": [
            {
                "title": "AAPL hits ATH",
                "published_utc": "2024-01-01T00:00:00Z",
                "article_url": "https://example.com",
                "author": "Jane Doe",
                "description": "desc",
                "tickers": ["AAPL"],
            }
        ]
    }


def _indicator_raw() -> dict:
    return {
        "results": {
            "values": [
                {"timestamp": 1_700_000_000_000, "value": 150.5},
                {"timestamp": 1_700_100_000_000, "value": 151.0},
            ]
        }
    }


def _dividends_raw() -> dict:
    return {
        "results": [
            {"ex_dividend_date": "2024-02-01", "pay_date": "2024-02-15", "cash_amount": 0.24, "frequency": 4},
        ]
    }


def _splits_raw() -> dict:
    return {
        "results": [
            {"execution_date": "2020-08-31", "split_from": 1, "split_to": 4},
        ]
    }


def _ticker_details_raw() -> dict:
    return {
        "results": {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "market": "stocks",
            "locale": "us",
            "type": "CS",
            "currency_name": "usd",
            "market_cap": 3_000_000_000_000,
            "description": "Apple.",
            "sic_code": "3571",
            "sic_description": "Electronic Computers",
            "homepage_url": "https://apple.com",
            "total_employees": 160_000,
            "list_date": "1980-12-12",
            "share_class_shares_outstanding": 15_000_000_000,
            "weighted_shares_outstanding": 15_200_000_000,
        }
    }


def _trades_raw() -> dict:
    return {
        "results": [
            {"p": 150.0, "s": 100, "t": 1_700_000_000_000_000_000, "x": 4},
        ]
    }


# ===========================================================================
# Tests: Aggregates & OHLC
# ===========================================================================


class TestPrevClose:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_prev_close_raw())
        sp.stocks_prev_close("aapl")
        assert sp.client.last_path == "/v2/aggs/ticker/AAPL/prev"

    def test_ticker_uppercased(self) -> None:
        sp = StocksProvider(_prev_close_raw())
        sp.stocks_prev_close("msft")
        assert "MSFT" in sp.client.last_path

    def test_returns_dict_with_close(self) -> None:
        sp = StocksProvider(_prev_close_raw())
        result = sp.stocks_prev_close("AAPL")
        assert isinstance(result, dict)
        assert result["close"] == 153.0
        assert result["ticker"] == "AAPL"

    def test_empty_response(self) -> None:
        sp = StocksProvider({"results": []})
        result = sp.stocks_prev_close("AAPL")
        assert result["ticker"] is None


class TestStocksBars:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_aggs_raw())
        sp.stocks_bars("aapl", 1, "day", "2024-01-01", "2024-01-31")
        assert sp.client.last_path == "/v2/aggs/ticker/AAPL/range/1/day/2024-01-01/2024-01-31"

    def test_returns_dataframe(self) -> None:
        sp = StocksProvider(_aggs_raw())
        result = sp.stocks_bars("AAPL", 1, "day", "2024-01-01", "2024-01-31")
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["Open", "High", "Low", "Close", "Volume"]

    def test_default_params_passed(self) -> None:
        sp = StocksProvider(_aggs_raw())
        sp.stocks_bars("AAPL", 1, "day", "2024-01-01", "2024-01-31")
        params = sp.client.last_params
        assert params is not None
        assert params["adjusted"] is True
        assert params["sort"] == "asc"
        assert params["limit"] == 50000


class TestGroupedDaily:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_aggs_raw())
        sp.stocks_grouped_daily("2024-01-15")
        assert sp.client.last_path == "/v2/aggs/grouped/locale/us/market/stocks/2024-01-15"

    def test_returns_dataframe(self) -> None:
        sp = StocksProvider(_aggs_raw())
        result = sp.stocks_grouped_daily("2024-01-15")
        assert isinstance(result, pd.DataFrame)


class TestDailyOhlc:
    _raw = {"open": 150.0, "high": 155.0, "low": 148.0, "close": 153.0, "volume": 500_000,
            "symbol": "AAPL", "from": "2024-01-15"}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.stocks_daily_ohlc("aapl", "2024-01-15")
        assert sp.client.last_path == "/v1/open-close/AAPL/2024-01-15"

    def test_returns_ohlcv_dict(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.stocks_daily_ohlc("AAPL", "2024-01-15")
        assert result["open"] == 150.0
        assert result["close"] == 153.0
        assert result["symbol"] == "AAPL"
        assert result["date"] == "2024-01-15"


# ===========================================================================
# Tests: Snapshots
# ===========================================================================


class TestSnapshot:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_snapshot_raw())
        sp.stocks_snapshot("aapl")
        assert sp.client.last_path == "/v2/snapshot/locale/us/markets/stocks/tickers/AAPL"

    def test_returns_dict(self) -> None:
        sp = StocksProvider(_snapshot_raw())
        result = sp.stocks_snapshot("AAPL")
        assert isinstance(result, dict)
        assert result["ticker"] == "AAPL"
        assert result["close"] == 153.0


class TestSnapshotAll:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        sp.stocks_snapshot_all()
        assert sp.client.last_path == "/v2/snapshot/locale/us/markets/stocks/tickers"

    def test_with_tickers_param(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        sp.stocks_snapshot_all(tickers=["AAPL", "MSFT"])
        assert sp.client.last_params is not None
        assert sp.client.last_params["tickers"] == "AAPL,MSFT"

    def test_returns_list(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        result = sp.stocks_snapshot_all()
        assert isinstance(result, list)
        assert result[0]["ticker"] == "AAPL"


class TestGainers:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        sp.stocks_gainers()
        assert sp.client.last_path == "/v2/snapshot/locale/us/markets/stocks/gainers"

    def test_returns_list(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        result = sp.stocks_gainers()
        assert isinstance(result, list)


class TestLosers:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        sp.stocks_losers()
        assert sp.client.last_path == "/v2/snapshot/locale/us/markets/stocks/losers"

    def test_returns_list(self) -> None:
        sp = StocksProvider(_snapshots_raw())
        result = sp.stocks_losers()
        assert isinstance(result, list)


# ===========================================================================
# Tests: Trades
# ===========================================================================


class TestLastTrade:
    _raw = {
        "results": {
            "T": "AAPL",
            "p": 153.0,
            "s": 100,
            "t": 1_700_000_000_000,
            "x": 4,
        }
    }

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.stocks_last_trade("aapl")
        assert sp.client.last_path == "/v2/last/trade/AAPL"

    def test_returns_trade_dict(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.stocks_last_trade("AAPL")
        assert isinstance(result, dict)
        assert result["ticker"] == "AAPL"
        assert result["price"] == 153.0
        assert result["size"] == 100
        assert result["exchange"] == 4


class TestTrades:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_trades_raw())
        sp.stocks_trades("aapl")
        assert sp.client.last_path == "/v3/trades/AAPL"

    def test_returns_dataframe(self) -> None:
        sp = StocksProvider(_trades_raw())
        result = sp.stocks_trades("AAPL")
        assert isinstance(result, pd.DataFrame)
        assert "price" in result.columns


# ===========================================================================
# Tests: Reference
# ===========================================================================


class TestTickerDetails:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_ticker_details_raw())
        sp.ticker_details("aapl")
        assert sp.client.last_path == "/v3/reference/tickers/AAPL"

    def test_returns_dict_with_name(self) -> None:
        sp = StocksProvider(_ticker_details_raw())
        result = sp.ticker_details("AAPL")
        assert isinstance(result, dict)
        assert result["name"] == "Apple Inc."
        assert result["ticker"] == "AAPL"


class TestTickerSearch:
    _raw = {"results": [{"ticker": "AAPL", "name": "Apple Inc.", "market": "stocks", "locale": "us", "type": "CS", "active": True}]}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.ticker_search(search="Apple")
        assert sp.client.last_path == "/v3/reference/tickers"

    def test_search_param_passed(self) -> None:
        sp = StocksProvider(self._raw)
        sp.ticker_search(search="Apple")
        assert sp.client.last_params is not None
        assert sp.client.last_params["search"] == "Apple"

    def test_returns_list(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.ticker_search()
        assert isinstance(result, list)


class TestTickerTypes:
    def test_correct_path(self) -> None:
        sp = StocksProvider({"results": []})
        sp.ticker_types()
        assert sp.client.last_path == "/v3/reference/tickers/types"


class TestExchanges:
    def test_correct_path(self) -> None:
        sp = StocksProvider({"results": []})
        sp.exchanges()
        assert sp.client.last_path == "/v3/reference/exchanges"


class TestConditions:
    def test_correct_path(self) -> None:
        sp = StocksProvider({"results": []})
        sp.conditions()
        assert sp.client.last_path == "/v3/reference/conditions"


class TestMarketHolidays:
    def test_correct_path(self) -> None:
        sp = StocksProvider([{"date": "2024-01-15", "status": "closed", "exchange": "NYSE", "name": "MLK Day"}])
        sp.market_holidays()
        assert sp.client.last_path == "/v1/marketstatus/upcoming"

    def test_returns_list(self) -> None:
        sp = StocksProvider([{"date": "2024-01-15"}])
        result = sp.market_holidays()
        assert isinstance(result, list)


class TestNews:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_news_raw())
        sp.news()
        assert sp.client.last_path == "/v2/reference/news"

    def test_ticker_param_passed(self) -> None:
        sp = StocksProvider(_news_raw())
        sp.news(ticker="AAPL")
        assert sp.client.last_params is not None
        assert sp.client.last_params["ticker"] == "AAPL"

    def test_returns_list_of_articles(self) -> None:
        sp = StocksProvider(_news_raw())
        result = sp.news()
        assert isinstance(result, list)
        assert result[0]["title"] == "AAPL hits ATH"


class TestDividends:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_dividends_raw())
        sp.dividends("aapl")
        assert sp.client.last_path == "/v3/reference/dividends"

    def test_ticker_param_uppercased(self) -> None:
        sp = StocksProvider(_dividends_raw())
        sp.dividends("aapl")
        assert sp.client.last_params is not None
        assert sp.client.last_params["ticker"] == "AAPL"

    def test_returns_list(self) -> None:
        sp = StocksProvider(_dividends_raw())
        result = sp.dividends("AAPL")
        assert isinstance(result, list)
        assert result[0]["cash_amount"] == 0.24


class TestSplits:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_splits_raw())
        sp.splits("aapl")
        assert sp.client.last_path == "/v3/reference/splits"

    def test_ticker_param_uppercased(self) -> None:
        sp = StocksProvider(_splits_raw())
        sp.splits("aapl")
        assert sp.client.last_params is not None
        assert sp.client.last_params["ticker"] == "AAPL"

    def test_returns_list(self) -> None:
        sp = StocksProvider(_splits_raw())
        result = sp.splits("AAPL")
        assert isinstance(result, list)
        assert result[0]["split_to"] == 4


# ===========================================================================
# Tests: Short / Float
# ===========================================================================


class TestShortInterest:
    _raw = {"results": [{"ticker": "AAPL", "short_interest": 100_000}]}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.short_interest("aapl")
        assert sp.client.last_path == "/v1/short-interest/AAPL"

    def test_returns_first_result(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.short_interest("AAPL")
        assert result["short_interest"] == 100_000

    def test_empty_returns_empty_dict(self) -> None:
        sp = StocksProvider({"results": []})
        result = sp.short_interest("AAPL")
        assert result == {}


class TestShortVolume:
    _raw = {"results": [{"ticker": "AAPL", "short_volume": 500_000}]}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.short_volume("aapl")
        assert sp.client.last_path == "/v1/short-volume/AAPL"

    def test_returns_first_result(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.short_volume("AAPL")
        assert result["short_volume"] == 500_000


class TestFloatShares:
    _raw = {"results": [{"ticker": "AAPL", "float_shares": 15_000_000_000}]}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.float_shares("aapl")
        assert sp.client.last_path == "/v1/float/AAPL"

    def test_returns_first_result(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.float_shares("AAPL")
        assert result["float_shares"] == 15_000_000_000


# ===========================================================================
# Tests: SEC
# ===========================================================================


class TestSecFilings:
    _raw = {"results": [{"filing_type": "10-K", "period_of_report": "2023-12-31"}]}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.sec_filings()
        assert sp.client.last_path == "/v1/sec/filings"

    def test_ticker_param_passed(self) -> None:
        sp = StocksProvider(self._raw)
        sp.sec_filings(ticker="aapl")
        assert sp.client.last_params is not None
        assert sp.client.last_params["ticker"] == "AAPL"

    def test_returns_list(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.sec_filings()
        assert isinstance(result, list)


class TestSecRiskFactors:
    _raw = {"results": {"ticker": "AAPL", "risk_factors": "Some risks"}}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.sec_risk_factors("aapl")
        assert sp.client.last_path == "/v1/sec/risk-factors/AAPL"

    def test_returns_dict(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.sec_risk_factors("AAPL")
        assert isinstance(result, dict)
        assert result["ticker"] == "AAPL"


class TestSec10kSections:
    _raw = {"results": {"ticker": "AAPL", "sections": {}}}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.sec_10k_sections("aapl")
        assert sp.client.last_path == "/v1/sec/10k-sections/AAPL"

    def test_returns_dict(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.sec_10k_sections("AAPL")
        assert isinstance(result, dict)


class TestSec8kText:
    _raw = {"results": {"ticker": "AAPL", "text": "earnings announcement"}}

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.sec_8k_text("aapl")
        assert sp.client.last_path == "/v1/sec/8k-text/AAPL"

    def test_returns_dict(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.sec_8k_text("AAPL")
        assert isinstance(result, dict)


# ===========================================================================
# Tests: Technical Indicators
# ===========================================================================


class TestSma:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_sma("aapl")
        assert sp.client.last_path == "/v1/indicators/sma/AAPL"

    def test_default_params(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_sma("AAPL")
        params = sp.client.last_params
        assert params is not None
        assert params["window"] == 50
        assert params["timespan"] == "day"
        assert params["series_type"] == "close"

    def test_returns_series(self) -> None:
        sp = StocksProvider(_indicator_raw())
        result = sp.stocks_sma("AAPL")
        assert isinstance(result, pd.Series)
        assert len(result) == 2

    def test_custom_window(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_sma("AAPL", window=200)
        assert sp.client.last_params is not None
        assert sp.client.last_params["window"] == 200


class TestEma:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_ema("aapl")
        assert sp.client.last_path == "/v1/indicators/ema/AAPL"

    def test_returns_series(self) -> None:
        sp = StocksProvider(_indicator_raw())
        result = sp.stocks_ema("AAPL")
        assert isinstance(result, pd.Series)


class TestMacd:
    _raw = {
        "results": {
            "values": [
                {"timestamp": 1_700_000_000_000, "value": 1.5, "signal": 1.2, "histogram": 0.3},
            ]
        }
    }

    def test_correct_path(self) -> None:
        sp = StocksProvider(self._raw)
        sp.stocks_macd("aapl")
        assert sp.client.last_path == "/v1/indicators/macd/AAPL"

    def test_default_params(self) -> None:
        sp = StocksProvider(self._raw)
        sp.stocks_macd("AAPL")
        params = sp.client.last_params
        assert params is not None
        assert params["short_window"] == 12
        assert params["long_window"] == 26
        assert params["signal_window"] == 9

    def test_returns_dict_with_values_list(self) -> None:
        sp = StocksProvider(self._raw)
        result = sp.stocks_macd("AAPL")
        assert isinstance(result, dict)
        assert "values" in result
        assert isinstance(result["values"], list)
        entry = result["values"][0]
        assert "timestamp" in entry
        assert "value" in entry
        assert "signal" in entry
        assert "histogram" in entry


class TestRsi:
    def test_correct_path(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_rsi("aapl")
        assert sp.client.last_path == "/v1/indicators/rsi/AAPL"

    def test_default_window(self) -> None:
        sp = StocksProvider(_indicator_raw())
        sp.stocks_rsi("AAPL")
        assert sp.client.last_params is not None
        assert sp.client.last_params["window"] == 14

    def test_returns_series(self) -> None:
        sp = StocksProvider(_indicator_raw())
        result = sp.stocks_rsi("AAPL")
        assert isinstance(result, pd.Series)
