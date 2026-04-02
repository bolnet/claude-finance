"""StocksMixin – wraps Polygon.io stocks endpoints.

Assumes ``self.client`` is a :class:`~finance_mcp.providers.polygon.client.PolygonClient`
(or any object with a ``.get(path, params)`` method).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from finance_mcp.providers.polygon.mappers import (
    aggs_to_dataframe,
    dividends_to_list,
    indicator_to_series,
    news_to_list,
    prev_close_to_dict,
    snapshot_to_dict,
    snapshots_to_list,
    splits_to_list,
    ticker_details_to_dict,
    trades_to_dataframe,
)

if TYPE_CHECKING:
    from finance_mcp.providers.polygon.client import PolygonClient


class StocksMixin:
    """Mixin that adds 30 Polygon stocks methods.

    Requires ``self.client: PolygonClient`` to be set by the host class.
    """

    client: PolygonClient

    # -----------------------------------------------------------------------
    # Aggregates & OHLC
    # -----------------------------------------------------------------------

    def stocks_prev_close(self, ticker: str) -> dict[str, Any]:
        """Return the previous day's OHLCV for *ticker*."""
        ticker = ticker.upper()
        raw = self.client.get(f"/v2/aggs/ticker/{ticker}/prev")
        return prev_close_to_dict(raw)

    def stocks_bars(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
        adjusted: bool = True,
        sort: str = "asc",
        limit: int = 50_000,
    ) -> pd.DataFrame:
        """Return OHLCV bars for *ticker* over the given date range."""
        ticker = ticker.upper()
        path = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params: dict[str, Any] = {"adjusted": adjusted, "sort": sort, "limit": limit}
        raw = self.client.get(path, params)
        return aggs_to_dataframe(raw)

    def stocks_grouped_daily(
        self,
        date: str,
        adjusted: bool = True,
    ) -> pd.DataFrame:
        """Return all stocks' OHLCV for a single market day."""
        path = f"/v2/aggs/grouped/locale/us/market/stocks/{date}"
        params: dict[str, Any] = {"adjusted": adjusted}
        raw = self.client.get(path, params)
        return aggs_to_dataframe(raw)

    def stocks_daily_ohlc(
        self,
        ticker: str,
        date: str,
        adjusted: bool = True,
    ) -> dict[str, Any]:
        """Return the open/close data for *ticker* on a specific *date*."""
        ticker = ticker.upper()
        path = f"/v1/open-close/{ticker}/{date}"
        params: dict[str, Any] = {"adjusted": adjusted}
        raw = self.client.get(path, params)
        return {
            "symbol": raw.get("symbol"),
            "date": raw.get("from"),
            "open": raw.get("open"),
            "high": raw.get("high"),
            "low": raw.get("low"),
            "close": raw.get("close"),
            "volume": raw.get("volume"),
        }

    # -----------------------------------------------------------------------
    # Snapshots
    # -----------------------------------------------------------------------

    def stocks_snapshot(self, ticker: str) -> dict[str, Any]:
        """Return the real-time snapshot for a single *ticker*."""
        ticker = ticker.upper()
        path = f"/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}"
        raw = self.client.get(path)
        return snapshot_to_dict(raw)

    def stocks_snapshot_all(
        self,
        tickers: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return real-time snapshots for all (or selected) tickers."""
        path = "/v2/snapshot/locale/us/markets/stocks/tickers"
        params: dict[str, Any] | None = None
        if tickers:
            params = {"tickers": ",".join(t.upper() for t in tickers)}
        raw = self.client.get(path, params)
        return snapshots_to_list(raw)

    def stocks_gainers(self) -> list[dict[str, Any]]:
        """Return today's top-gaining stocks."""
        raw = self.client.get("/v2/snapshot/locale/us/markets/stocks/gainers")
        return snapshots_to_list(raw)

    def stocks_losers(self) -> list[dict[str, Any]]:
        """Return today's top-losing stocks."""
        raw = self.client.get("/v2/snapshot/locale/us/markets/stocks/losers")
        return snapshots_to_list(raw)

    # -----------------------------------------------------------------------
    # Trades
    # -----------------------------------------------------------------------

    def stocks_last_trade(self, ticker: str) -> dict[str, Any]:
        """Return the most recent trade for *ticker*."""
        ticker = ticker.upper()
        path = f"/v2/last/trade/{ticker}"
        raw = self.client.get(path)
        result: dict[str, Any] = raw.get("results") or {}
        return {
            "ticker": result.get("T"),
            "price": result.get("p"),
            "size": result.get("s"),
            "timestamp": result.get("t"),
            "exchange": result.get("x"),
        }

    def stocks_trades(
        self,
        ticker: str,
        timestamp: str | None = None,
        limit: int = 100,
    ) -> pd.DataFrame:
        """Return a DataFrame of recent trades for *ticker*."""
        ticker = ticker.upper()
        path = f"/v3/trades/{ticker}"
        params: dict[str, Any] = {"limit": limit}
        if timestamp is not None:
            params["timestamp"] = timestamp
        raw = self.client.get(path, params)
        return trades_to_dataframe(raw)

    # -----------------------------------------------------------------------
    # Reference data
    # -----------------------------------------------------------------------

    def ticker_details(self, ticker: str) -> dict[str, Any]:
        """Return detailed company information for *ticker*."""
        ticker = ticker.upper()
        path = f"/v3/reference/tickers/{ticker}"
        raw = self.client.get(path)
        return ticker_details_to_dict(raw)

    def ticker_search(
        self,
        search: str | None = None,
        ticker_type: str | None = None,
        market: str | None = None,
        active: bool = True,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Search for tickers by keyword, type, or market."""
        params: dict[str, Any] = {"active": active, "limit": limit}
        if search is not None:
            params["search"] = search
        if ticker_type is not None:
            params["type"] = ticker_type
        if market is not None:
            params["market"] = market
        raw = self.client.get("/v3/reference/tickers", params)
        return raw.get("results") or []

    def ticker_types(self) -> list[dict[str, Any]]:
        """Return all supported ticker types."""
        raw = self.client.get("/v3/reference/tickers/types")
        return raw.get("results") or []

    def exchanges(self) -> list[dict[str, Any]]:
        """Return all exchanges recognized by Polygon."""
        raw = self.client.get("/v3/reference/exchanges")
        return raw.get("results") or []

    def conditions(self) -> list[dict[str, Any]]:
        """Return all trade conditions."""
        raw = self.client.get("/v3/reference/conditions")
        return raw.get("results") or []

    def market_holidays(self) -> list[dict[str, Any]]:
        """Return upcoming market holidays.

        The endpoint returns a list directly, not wrapped in a ``results`` key.
        """
        raw = self.client.get("/v1/marketstatus/upcoming")
        # The endpoint returns a list, not a dict
        if isinstance(raw, list):
            return raw
        return raw.get("results") or []

    def news(
        self,
        ticker: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Return recent financial news articles."""
        params: dict[str, Any] = {"limit": limit}
        if ticker is not None:
            params["ticker"] = ticker.upper()
        raw = self.client.get("/v2/reference/news", params)
        return news_to_list(raw)

    def dividends(
        self,
        ticker: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Return dividend history for *ticker*."""
        params: dict[str, Any] = {"ticker": ticker.upper(), "limit": limit}
        raw = self.client.get("/v3/reference/dividends", params)
        return dividends_to_list(raw)

    def splits(
        self,
        ticker: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Return stock split history for *ticker*."""
        params: dict[str, Any] = {"ticker": ticker.upper(), "limit": limit}
        raw = self.client.get("/v3/reference/splits", params)
        return splits_to_list(raw)

    # -----------------------------------------------------------------------
    # Short interest & float
    # -----------------------------------------------------------------------

    def short_interest(self, ticker: str) -> dict[str, Any]:
        """Return the latest short interest data for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/short-interest/{ticker}"
        raw = self.client.get(path)
        results: list[dict[str, Any]] = raw.get("results") or []
        return results[0] if results else {}

    def short_volume(self, ticker: str) -> dict[str, Any]:
        """Return the latest short volume data for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/short-volume/{ticker}"
        raw = self.client.get(path)
        results: list[dict[str, Any]] = raw.get("results") or []
        return results[0] if results else {}

    def float_shares(self, ticker: str) -> dict[str, Any]:
        """Return float shares data for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/float/{ticker}"
        raw = self.client.get(path)
        results: list[dict[str, Any]] = raw.get("results") or []
        return results[0] if results else {}

    # -----------------------------------------------------------------------
    # SEC filings
    # -----------------------------------------------------------------------

    def sec_filings(
        self,
        ticker: str | None = None,
        filing_type: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Return SEC filings, optionally filtered by ticker or type."""
        params: dict[str, Any] = {"limit": limit}
        if ticker is not None:
            params["ticker"] = ticker.upper()
        if filing_type is not None:
            params["type"] = filing_type
        raw = self.client.get("/v1/sec/filings", params)
        return raw.get("results") or []

    def sec_risk_factors(self, ticker: str) -> dict[str, Any]:
        """Return the risk factors section from the latest 10-K for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/sec/risk-factors/{ticker}"
        raw = self.client.get(path)
        return raw.get("results") or {}

    def sec_10k_sections(self, ticker: str) -> dict[str, Any]:
        """Return key sections from the latest 10-K for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/sec/10k-sections/{ticker}"
        raw = self.client.get(path)
        return raw.get("results") or {}

    def sec_8k_text(self, ticker: str) -> dict[str, Any]:
        """Return the text of the latest 8-K filing for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/sec/8k-text/{ticker}"
        raw = self.client.get(path)
        return raw.get("results") or {}

    # -----------------------------------------------------------------------
    # Technical indicators
    # -----------------------------------------------------------------------

    def stocks_sma(
        self,
        ticker: str,
        window: int = 50,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return Simple Moving Average values for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/indicators/sma/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params)
        return indicator_to_series(raw)

    def stocks_ema(
        self,
        ticker: str,
        window: int = 50,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return Exponential Moving Average values for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/indicators/ema/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params)
        return indicator_to_series(raw)

    def stocks_macd(
        self,
        ticker: str,
        short_window: int = 12,
        long_window: int = 26,
        signal_window: int = 9,
        timespan: str = "day",
        series_type: str = "close",
    ) -> dict[str, Any]:
        """Return MACD values (value, signal, histogram) for *ticker*.

        Returns a dict with a ``values`` list, each entry having
        ``timestamp``, ``value``, ``signal``, and ``histogram`` keys.
        """
        ticker = ticker.upper()
        path = f"/v1/indicators/macd/{ticker}"
        params: dict[str, Any] = {
            "short_window": short_window,
            "long_window": long_window,
            "signal_window": signal_window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params)
        results: dict[str, Any] = raw.get("results") or {}
        raw_values: list[dict[str, Any]] = results.get("values") or []
        values = [
            {
                "timestamp": v.get("timestamp"),
                "value": v.get("value"),
                "signal": v.get("signal"),
                "histogram": v.get("histogram"),
            }
            for v in raw_values
        ]
        return {"values": values}

    def stocks_rsi(
        self,
        ticker: str,
        window: int = 14,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return Relative Strength Index values for *ticker*."""
        ticker = ticker.upper()
        path = f"/v1/indicators/rsi/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params)
        return indicator_to_series(raw)
