"""Polygon.io indices endpoints mixin.

Provides methods for index tickers using the I: prefix convention.
All ticker values are passed as-is (no additional uppercasing).
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from finance_mcp.providers.polygon.mappers import (
    aggs_to_dataframe,
    indicator_to_series,
    prev_close_to_dict,
)


class IndicesMixin:
    """Mixin providing Polygon.io indices API endpoints.

    Requires ``self.client`` to be a PolygonClient instance (or compatible
    duck-typed object exposing a ``get(path, params)`` method).
    """

    client: Any  # bound by the concrete class

    # ------------------------------------------------------------------
    # Previous close
    # ------------------------------------------------------------------

    def indices_prev_close(self, ticker: str) -> dict[str, Any]:
        """Return the previous day's OHLCV data for an index.

        Args:
            ticker: Index ticker symbol (e.g. ``"I:SPX"``). Passed as-is.

        Returns:
            Dict with keys: ticker, open, high, low, close, volume, timestamp.
        """
        path = f"/v2/aggs/ticker/{ticker}/prev"
        raw = self.client.get(path)
        return prev_close_to_dict(raw)

    # ------------------------------------------------------------------
    # Aggregate bars
    # ------------------------------------------------------------------

    def indices_bars(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
        sort: str = "asc",
        limit: int = 50000,
    ) -> pd.DataFrame:
        """Return OHLCV aggregate bars for an index.

        Args:
            ticker: Index ticker symbol (e.g. ``"I:SPX"``).
            multiplier: Size of the aggregate time window.
            timespan: Unit of the aggregate window (``"day"``, ``"minute"`` …).
            from_date: Start date as ``"YYYY-MM-DD"``.
            to_date: End date as ``"YYYY-MM-DD"``.
            sort: Sort order — ``"asc"`` (default) or ``"desc"``.
            limit: Maximum number of bars to return (default 50,000).

        Returns:
            DataFrame with columns Open, High, Low, Close, Volume and a UTC
            DatetimeIndex.
        """
        path = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params: dict[str, Any] = {"sort": sort, "limit": limit}
        raw = self.client.get(path, params=params)
        return aggs_to_dataframe(raw)

    # ------------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------------

    def indices_snapshot(self, tickers: list[str]) -> list[dict[str, Any]]:
        """Return a snapshot for one or more indices.

        Args:
            tickers: List of index ticker symbols (e.g. ``["I:SPX", "I:NDX"]``).

        Returns:
            Raw ``results`` list from the Polygon response.
        """
        path = "/v3/snapshot/indices"
        params: dict[str, Any] = {"ticker.any_of": ",".join(tickers)}
        raw = self.client.get(path, params=params)
        return raw.get("results") or []

    def indices_unified_snapshot(self, tickers: list[str]) -> list[dict[str, Any]]:
        """Return a unified snapshot for one or more indices.

        Args:
            tickers: List of index ticker symbols.

        Returns:
            Raw ``results`` list from the Polygon response.
        """
        path = "/v3/snapshot"
        params: dict[str, Any] = {"ticker.any_of": ",".join(tickers)}
        raw = self.client.get(path, params=params)
        return raw.get("results") or []

    # ------------------------------------------------------------------
    # Daily open/close
    # ------------------------------------------------------------------

    def indices_daily_ohlc(self, ticker: str, date: str) -> dict[str, Any]:
        """Return open/close data for an index on a specific date.

        Args:
            ticker: Index ticker symbol (e.g. ``"I:SPX"``).
            date: Date as ``"YYYY-MM-DD"``.

        Returns:
            Dict with keys: symbol, date, open, high, low, close, volume.
        """
        path = f"/v1/open-close/{ticker}/{date}"
        raw = self.client.get(path)
        return {
            "symbol": raw.get("symbol"),
            "date": raw.get("from"),
            "open": raw.get("open"),
            "high": raw.get("high"),
            "low": raw.get("low"),
            "close": raw.get("close"),
            "volume": raw.get("volume"),
        }

    # ------------------------------------------------------------------
    # Technical indicators
    # ------------------------------------------------------------------

    def indices_sma(
        self,
        ticker: str,
        window: int = 50,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return the Simple Moving Average series for an index.

        Args:
            ticker: Index ticker symbol.
            window: Number of periods for the moving average (default 50).
            timespan: Aggregate time window (default ``"day"``).
            series_type: Price field to calculate on (default ``"close"``).

        Returns:
            pd.Series with UTC DatetimeIndex and float values.
        """
        path = f"/v1/indicators/sma/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params=params)
        return indicator_to_series(raw)

    def indices_ema(
        self,
        ticker: str,
        window: int = 50,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return the Exponential Moving Average series for an index.

        Args:
            ticker: Index ticker symbol.
            window: Number of periods (default 50).
            timespan: Aggregate time window (default ``"day"``).
            series_type: Price field to calculate on (default ``"close"``).

        Returns:
            pd.Series with UTC DatetimeIndex and float values.
        """
        path = f"/v1/indicators/ema/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params=params)
        return indicator_to_series(raw)

    def indices_rsi(
        self,
        ticker: str,
        window: int = 14,
        timespan: str = "day",
        series_type: str = "close",
    ) -> pd.Series:
        """Return the Relative Strength Index series for an index.

        Args:
            ticker: Index ticker symbol.
            window: RSI look-back period (default 14).
            timespan: Aggregate time window (default ``"day"``).
            series_type: Price field to calculate on (default ``"close"``).

        Returns:
            pd.Series with UTC DatetimeIndex and float values.
        """
        path = f"/v1/indicators/rsi/{ticker}"
        params: dict[str, Any] = {
            "window": window,
            "timespan": timespan,
            "series_type": series_type,
        }
        raw = self.client.get(path, params=params)
        return indicator_to_series(raw)
