"""PolygonProvider — composes all Polygon.io mixins into a single DataProvider.

This class satisfies the :class:`~finance_mcp.providers.base.DataProvider`
Protocol by implementing the three required methods on top of the Polygon
aggregate bars endpoint, and inheriting the full set of Polygon-specific
methods from the mixin classes.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from typing import Any

import pandas as pd

from finance_mcp.providers.base import Capability
from finance_mcp.providers.polygon.client import PolygonClient
from finance_mcp.providers.polygon.currencies import CurrenciesMixin
from finance_mcp.providers.polygon.indices import IndicesMixin
from finance_mcp.providers.polygon.options import OptionsMixin
from finance_mcp.providers.polygon.stocks import StocksMixin


# All 11 Capability flags
_POLYGON_CAPABILITIES: frozenset[Capability] = frozenset(Capability)

# Mapping from period string to timedelta days offset from start
_PERIOD_DAYS: dict[str, int] = {
    "1d": 1,
    "5d": 5,
    "1mo": 30,
    "3mo": 90,
    "6mo": 180,
    "1y": 365,
    "2y": 730,
    "5y": 1825,
    "10y": 3650,
    "ytd": 365,
    "max": 3650,
}


class PolygonProvider(StocksMixin, OptionsMixin, IndicesMixin, CurrenciesMixin):
    """DataProvider backed by Polygon.io, composing all mixin endpoint groups.

    Satisfies the :class:`~finance_mcp.providers.base.DataProvider` Protocol
    with ``fetch_price_history``, ``get_adjusted_prices``, and
    ``fetch_multi_ticker``, delegating to the underlying ``stocks_bars`` method
    from :class:`StocksMixin`.

    Args:
        api_key: Polygon.io API key.
        base_url: Optional override for the Polygon REST base URL.
        timeout: HTTP timeout in seconds (default 30).
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.polygon.io",
        timeout: float = 30.0,
    ) -> None:
        self.client = PolygonClient(api_key=api_key, base_url=base_url, timeout=timeout)

    @property
    def capabilities(self) -> frozenset[Capability]:
        """Return the full set of capabilities supported by Polygon.io."""
        return _POLYGON_CAPABILITIES

    def fetch_price_history(
        self,
        ticker: str,
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> pd.DataFrame:
        """Fetch adjusted daily OHLCV bars from Polygon for a single ticker.

        ``end`` takes priority over ``period``.  When only ``period`` is given,
        the end date is computed by adding the period's day offset to ``start``.
        When neither is provided, today is used as the end date.

        Args:
            ticker: Ticker symbol (e.g. "AAPL").
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Takes priority over *period*.
            period: Period shorthand (e.g. "1mo", "1y"). Used only when *end*
                is not supplied.

        Returns:
            DataFrame with DatetimeIndex and OHLCV columns.
        """
        if end is not None:
            to_date = end
        elif period is not None:
            days = _PERIOD_DAYS.get(period, 365)
            start_dt = date.fromisoformat(start)
            to_date = (start_dt + timedelta(days=days)).isoformat()
        else:
            to_date = date.today().isoformat()

        return self.stocks_bars(
            ticker,
            multiplier=1,
            timespan="day",
            from_date=start,
            to_date=to_date,
        )

    def get_adjusted_prices(self, df: pd.DataFrame) -> pd.Series:
        """Extract the adjusted closing price series from a fetched DataFrame.

        Looks for a ``Close`` column (capital C) first, then ``close``,
        then falls back to the last column.

        Args:
            df: DataFrame returned by ``fetch_price_history``.

        Returns:
            pd.Series with DatetimeIndex representing adjusted close prices.
        """
        for col in ("Close", "close"):
            if col in df.columns:
                return df[col]
        return df.iloc[:, -1]

    def fetch_multi_ticker(
        self,
        tickers: list[str],
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> dict[str, pd.Series]:
        """Fetch adjusted close price series for multiple tickers.

        Failures for individual tickers are logged to stderr and skipped;
        the returned dict will contain only the tickers that succeeded.

        Args:
            tickers: List of ticker symbols.
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: Period shorthand. Optional.

        Returns:
            Dict mapping ticker symbol → pd.Series of adjusted closing prices.
        """
        result: dict[str, pd.Series] = {}
        for ticker in tickers:
            try:
                df = self.fetch_price_history(ticker, start=start, end=end, period=period)
                result[ticker] = self.get_adjusted_prices(df)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[PolygonProvider] fetch_multi_ticker: skipping {ticker} — {exc}",
                    file=sys.stderr,
                )
        return result

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        self.client.close()
