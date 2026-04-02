"""MassiveProvider - composes all Massive mixins into a single DataProvider.

This class satisfies the :class:`~finance_mcp.providers.base.DataProvider`
Protocol by implementing the three required methods on top of the Massive
aggregate bars endpoint, and inheriting the full set of Massive-specific
methods from the mixin classes.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta

import pandas as pd

from finance_mcp.providers.base import Capability
from finance_mcp.providers.massive.client import MassiveClient
from finance_mcp.providers.massive.currencies import CurrenciesMixin
from finance_mcp.providers.massive.indices import IndicesMixin
from finance_mcp.providers.massive.options import OptionsMixin
from finance_mcp.providers.massive.stocks import StocksMixin
from finance_mcp.providers.massive.stubs import BlockedEndpointsMixin

# ---------------------------------------------------------------------------
# Period -> days mapping (yfinance-style shorthand)
# ---------------------------------------------------------------------------

_PERIOD_DAYS: dict[str, int] = {
    "1mo": 30,
    "3mo": 90,
    "6mo": 180,
    "1y": 365,
    "2y": 730,
    "5y": 1825,
}


class MassiveProvider(
    StocksMixin,
    OptionsMixin,
    IndicesMixin,
    CurrenciesMixin,
    BlockedEndpointsMixin,
):
    """DataProvider backed by Massive, composing all mixin endpoint groups.

    Satisfies the :class:`~finance_mcp.providers.base.DataProvider` Protocol
    with ``fetch_price_history``, ``get_adjusted_prices``, and
    ``fetch_multi_ticker``, delegating to the underlying ``stocks_bars`` method
    from :class:`StocksMixin`.

    Args:
        api_key: Massive API key.
        base_url: Optional override for the Massive REST base URL.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.polygon.io",
    ) -> None:
        self.client = MassiveClient(api_key=api_key, base_url=base_url)

    @property
    def capabilities(self) -> frozenset[Capability]:
        """Return all 11 Capability flags."""
        return frozenset(Capability)

    def fetch_price_history(
        self,
        ticker: str,
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> pd.DataFrame:
        """Fetch adjusted daily OHLCV bars from Massive for a single ticker.

        If *end* is not provided, *period* is used to compute it relative to
        *start*. If both are provided, *end* takes precedence.

        Args:
            ticker: Ticker symbol (e.g. "AAPL").
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Overrides *period* when provided.
            period: yfinance-style period string (e.g. "1y"). Supported values:
                ``1mo``, ``3mo``, ``6mo``, ``1y``, ``2y``, ``5y``.

        Returns:
            DataFrame with DatetimeIndex and OHLCV columns.
        """
        to_date = end
        if to_date is None and period is not None:
            days = _PERIOD_DAYS.get(period, 365)
            start_date = date.fromisoformat(start)
            to_date = (start_date + timedelta(days=days)).isoformat()
        if to_date is None:
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

        Args:
            df: DataFrame returned by ``fetch_price_history``.

        Returns:
            pd.Series with DatetimeIndex representing adjusted close prices.
        """
        return df["Close"]

    def fetch_multi_ticker(
        self,
        tickers: list[str],
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> dict[str, pd.Series]:
        """Fetch adjusted close price series for multiple tickers.

        Failures for individual tickers are logged to *stderr* and skipped so
        that a single bad ticker does not abort the entire batch.

        Args:
            tickers: List of ticker symbols.
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: yfinance-style period string. Optional.

        Returns:
            Dict mapping ticker symbol -> pd.Series of adjusted closing prices.
        """
        result: dict[str, pd.Series] = {}
        for ticker in tickers:
            try:
                df = self.fetch_price_history(ticker, start=start, end=end, period=period)
                result[ticker] = self.get_adjusted_prices(df)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[massive] fetch_multi_ticker: skipping {ticker!r} - {exc}",
                    file=sys.stderr,
                )
        return result

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.client.close()
