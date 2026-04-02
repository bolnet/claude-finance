"""YFinanceProvider — thin wrapper around finance_mcp.adapter for the DataProvider protocol."""
from __future__ import annotations

import pandas as pd

from finance_mcp import adapter
from finance_mcp.providers.base import Capability


_YFINANCE_CAPABILITIES: frozenset[Capability] = frozenset(
    {
        Capability.PRICE_HISTORY,
        Capability.NEWS,
        Capability.FUNDAMENTALS,
        Capability.TICKER_INFO,
    }
)


class YFinanceProvider:
    """DataProvider implementation backed by Yahoo Finance via yfinance.

    Delegates all data fetching to :mod:`finance_mcp.adapter`.  No additional
    logic is added here — this is intentionally a thin wrapper.
    """

    @property
    def capabilities(self) -> frozenset[Capability]:
        """Return the capabilities supported by the Yahoo Finance provider."""
        return _YFINANCE_CAPABILITIES

    def fetch_price_history(
        self,
        ticker: str,
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> pd.DataFrame:
        """Fetch adjusted daily price history via yfinance adapter.

        Args:
            ticker: Ticker symbol (e.g. "AAPL").
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: yfinance period string (e.g. "1y"). Optional.

        Returns:
            DataFrame with DatetimeIndex and OHLCV columns.
        """
        return adapter.fetch_price_history(ticker, start, end=end, period=period)

    def get_adjusted_prices(self, df: pd.DataFrame) -> pd.Series:
        """Extract the adjusted closing price series from a fetched DataFrame.

        Args:
            df: DataFrame returned by ``fetch_price_history``.

        Returns:
            pd.Series with DatetimeIndex representing adjusted close prices.
        """
        return adapter.get_adjusted_prices(df)

    def fetch_multi_ticker(
        self,
        tickers: list[str],
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> dict[str, pd.Series]:
        """Fetch adjusted close prices for multiple tickers via yfinance adapter.

        Args:
            tickers: List of ticker symbols.
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: yfinance period string. Optional.

        Returns:
            Dict mapping ticker symbol → pd.Series of adjusted closing prices.
        """
        return adapter.fetch_multi_ticker(tickers, start, end=end, period=period)
