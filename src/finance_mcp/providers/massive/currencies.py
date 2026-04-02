"""CurrenciesMixin — Forex (8) and Crypto (7) endpoints for Massive."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from finance_mcp.providers.massive.mappers import (
    aggs_to_dataframe,
    prev_close_to_dict,
    snapshot_to_dict,
    snapshots_to_list,
)

if TYPE_CHECKING:
    from finance_mcp.providers.massive.client import MassiveClient


class CurrenciesMixin:
    """Mixin providing Forex and Crypto market data methods.

    Requires ``self.client`` to be a :class:`~finance_mcp.providers.massive.client.MassiveClient`
    (or any object that implements a compatible ``.get(path, params)`` interface).
    """

    client: MassiveClient

    # ------------------------------------------------------------------
    # Forex — 8 endpoints
    # ------------------------------------------------------------------

    def forex_prev_close(self, ticker: str) -> dict[str, Any]:
        """Return the previous day's OHLCV for a Forex ticker.

        Args:
            ticker: Forex ticker symbol, e.g. ``"C:EURUSD"``.

        Returns:
            Dict with keys: ticker, open, high, low, close, volume, timestamp.
        """
        path = f"/v2/aggs/ticker/{ticker}/prev"
        raw = self.client.get(path)
        return prev_close_to_dict(raw)

    def forex_bars(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
        sort: str = "asc",
        limit: int = 50000,
    ) -> pd.DataFrame:
        """Return OHLCV bars for a Forex ticker.

        Args:
            ticker: Forex ticker symbol, e.g. ``"C:EURUSD"``.
            multiplier: Size of the aggregate time window.
            timespan: Unit of the aggregate time window (``"minute"``, ``"hour"``, ``"day"`` …).
            from_date: Start date in ``YYYY-MM-DD`` format.
            to_date: End date in ``YYYY-MM-DD`` format.
            sort: ``"asc"`` (default) or ``"desc"``.
            limit: Maximum number of results (default 50 000).

        Returns:
            DataFrame with DatetimeIndex and columns: Open, High, Low, Close, Volume.
        """
        path = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        raw = self.client.get(path, params={"sort": sort, "limit": limit})
        return aggs_to_dataframe(raw)

    def forex_conversion(
        self,
        from_currency: str,
        to_currency: str,
        amount: float = 1.0,
    ) -> dict[str, Any]:
        """Convert an amount between two currencies using real-time rates.

        Args:
            from_currency: Source currency code, e.g. ``"USD"``.
            to_currency: Destination currency code, e.g. ``"EUR"``.
            amount: Amount to convert (default ``1.0``).

        Returns:
            Dict with keys: from, to, initial_amount, converted.
        """
        from_upper = from_currency.upper()
        to_upper = to_currency.upper()
        path = f"/v1/conversion/{from_upper}/{to_upper}"
        raw = self.client.get(path, params={"amount": amount})
        return {
            "from": raw.get("from"),
            "to": raw.get("to"),
            "initial_amount": raw.get("initialAmount"),
            "converted": raw.get("converted"),
        }

    def forex_last_quote(
        self,
        from_currency: str,
        to_currency: str,
    ) -> dict[str, Any]:
        """Return the last quote (bid/ask) for a currency pair.

        Args:
            from_currency: Source currency code, e.g. ``"USD"``.
            to_currency: Destination currency code, e.g. ``"EUR"``.

        Returns:
            Dict with keys: ask, bid, timestamp.
        """
        from_upper = from_currency.upper()
        to_upper = to_currency.upper()
        path = f"/v1/last_quote/currencies/{from_upper}/{to_upper}"
        raw = self.client.get(path)
        last: dict[str, Any] = raw.get("last") or {}
        return {
            "ask": last.get("ask"),
            "bid": last.get("bid"),
            "timestamp": last.get("timestamp"),
        }

    def forex_quotes(self, ticker: str, limit: int = 100) -> list[dict[str, Any]]:
        """Return recent quotes for a Forex ticker.

        Args:
            ticker: Forex ticker symbol, e.g. ``"C:EURUSD"``.
            limit: Maximum number of results (default 100).

        Returns:
            Raw list of quote dicts from the API response.
        """
        path = f"/v3/quotes/{ticker}"
        raw = self.client.get(path, params={"limit": limit})
        return raw.get("results") or []

    def forex_snapshot_all(
        self, tickers: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Return snapshots for all (or a subset of) Forex tickers.

        Args:
            tickers: Optional list of ticker symbols to filter by.

        Returns:
            List of snapshot dicts.
        """
        path = "/v2/snapshot/locale/global/markets/forex/tickers"
        params: dict[str, Any] = {}
        if tickers:
            params["tickers"] = ",".join(tickers)
        raw = self.client.get(path, params=params)
        return snapshots_to_list(raw)

    def forex_gainers(self) -> list[dict[str, Any]]:
        """Return the top Forex gainers.

        Returns:
            List of snapshot dicts for the biggest movers (up).
        """
        path = "/v2/snapshot/locale/global/markets/forex/gainers"
        raw = self.client.get(path)
        return snapshots_to_list(raw)

    def forex_losers(self) -> list[dict[str, Any]]:
        """Return the top Forex losers.

        Returns:
            List of snapshot dicts for the biggest movers (down).
        """
        path = "/v2/snapshot/locale/global/markets/forex/losers"
        raw = self.client.get(path)
        return snapshots_to_list(raw)

    # ------------------------------------------------------------------
    # Crypto — 7 endpoints
    # ------------------------------------------------------------------

    def crypto_prev_close(self, ticker: str) -> dict[str, Any]:
        """Return the previous day's OHLCV for a Crypto ticker.

        Args:
            ticker: Crypto ticker symbol, e.g. ``"X:BTCUSD"``.

        Returns:
            Dict with keys: ticker, open, high, low, close, volume, timestamp.
        """
        path = f"/v2/aggs/ticker/{ticker}/prev"
        raw = self.client.get(path)
        return prev_close_to_dict(raw)

    def crypto_bars(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
        sort: str = "asc",
        limit: int = 50000,
    ) -> pd.DataFrame:
        """Return OHLCV bars for a Crypto ticker.

        Args:
            ticker: Crypto ticker symbol, e.g. ``"X:BTCUSD"``.
            multiplier: Size of the aggregate time window.
            timespan: Unit of the aggregate time window.
            from_date: Start date in ``YYYY-MM-DD`` format.
            to_date: End date in ``YYYY-MM-DD`` format.
            sort: ``"asc"`` (default) or ``"desc"``.
            limit: Maximum number of results (default 50 000).

        Returns:
            DataFrame with DatetimeIndex and columns: Open, High, Low, Close, Volume.
        """
        path = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        raw = self.client.get(path, params={"sort": sort, "limit": limit})
        return aggs_to_dataframe(raw)

    def crypto_snapshot_all(
        self, tickers: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Return snapshots for all (or a subset of) Crypto tickers.

        Args:
            tickers: Optional list of ticker symbols to filter by.

        Returns:
            List of snapshot dicts.
        """
        path = "/v2/snapshot/locale/global/markets/crypto/tickers"
        params: dict[str, Any] = {}
        if tickers:
            params["tickers"] = ",".join(tickers)
        raw = self.client.get(path, params=params)
        return snapshots_to_list(raw)

    def crypto_snapshot(self, ticker: str) -> dict[str, Any]:
        """Return the current snapshot for a single Crypto ticker.

        Args:
            ticker: Crypto ticker symbol, e.g. ``"X:BTCUSD"``.

        Returns:
            Dict with ticker-level snapshot data.
        """
        path = f"/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}"
        raw = self.client.get(path)
        return snapshot_to_dict(raw)

    def crypto_gainers(self) -> list[dict[str, Any]]:
        """Return the top Crypto gainers.

        Returns:
            List of snapshot dicts for the biggest movers (up).
        """
        path = "/v2/snapshot/locale/global/markets/crypto/gainers"
        raw = self.client.get(path)
        return snapshots_to_list(raw)

    def crypto_losers(self) -> list[dict[str, Any]]:
        """Return the top Crypto losers.

        Returns:
            List of snapshot dicts for the biggest movers (down).
        """
        path = "/v2/snapshot/locale/global/markets/crypto/losers"
        raw = self.client.get(path)
        return snapshots_to_list(raw)

    def crypto_daily_ohlc(
        self,
        from_currency: str,
        to_currency: str,
        date: str,
    ) -> dict[str, Any]:
        """Return the daily open/close for a Crypto pair on a specific date.

        Args:
            from_currency: Base currency code, e.g. ``"BTC"``.
            to_currency: Quote currency code, e.g. ``"USD"``.
            date: Date in ``YYYY-MM-DD`` format.

        Returns:
            Dict with keys: symbol, date, open, high, low, close, volume.
        """
        from_upper = from_currency.upper()
        to_upper = to_currency.upper()
        path = f"/v1/open-close/crypto/{from_upper}/{to_upper}/{date}"
        raw = self.client.get(path)
        return {
            "symbol": raw.get("symbol"),
            "date": raw.get("day"),
            "open": raw.get("open"),
            "high": raw.get("high"),
            "low": raw.get("low"),
            "close": raw.get("close"),
            "volume": raw.get("volume"),
        }
