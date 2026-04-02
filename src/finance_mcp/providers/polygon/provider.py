"""PolygonProvider — composes all Polygon.io mixins into a single DataProvider.

This class satisfies the :class:`~finance_mcp.providers.base.DataProvider`
Protocol by implementing the three required methods on top of the Polygon
aggregate bars endpoint, and inheriting the full set of Polygon-specific
methods from the mixin classes.
"""
from __future__ import annotations

import pandas as pd

from finance_mcp.providers.base import Capability
from finance_mcp.providers.polygon.client import PolygonClient
from finance_mcp.providers.polygon.currencies import CurrenciesMixin
from finance_mcp.providers.polygon.indices import IndicesMixin
from finance_mcp.providers.polygon.options import OptionsMixin
from finance_mcp.providers.polygon.stocks import StocksMixin


_POLYGON_CAPABILITIES: frozenset[Capability] = frozenset(
    {
        Capability.PRICE_HISTORY,
        Capability.NEWS,
        Capability.OPTIONS_CHAIN,
        Capability.FOREX,
        Capability.CRYPTO,
        Capability.INDICES,
        Capability.TECHNICALS,
        Capability.FUNDAMENTALS,
        Capability.MARKET_MOVERS,
        Capability.TICKER_INFO,
    }
)


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

        Args:
            ticker: Ticker symbol (e.g. "AAPL").
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Defaults to today if not supplied.
            period: Unused by Polygon (present for protocol compatibility).

        Returns:
            DataFrame with DatetimeIndex and OHLCV columns.
        """
        import datetime

        to_date = end or datetime.date.today().isoformat()
        return self.stocks_bars(
            ticker=ticker,
            multiplier=1,
            timespan="day",
            from_date=start,
            to_date=to_date,
            adjusted=True,
            sort="asc",
        )

    def get_adjusted_prices(self, df: pd.DataFrame) -> pd.Series:
        """Extract the adjusted closing price series from a fetched DataFrame.

        Args:
            df: DataFrame returned by ``fetch_price_history``.

        Returns:
            pd.Series with DatetimeIndex representing adjusted close prices.
        """
        col = "close" if "close" in df.columns else df.columns[-1]
        return df[col]

    def fetch_multi_ticker(
        self,
        tickers: list[str],
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> dict[str, pd.Series]:
        """Fetch adjusted close price series for multiple tickers.

        Args:
            tickers: List of ticker symbols.
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: Unused by Polygon (present for protocol compatibility).

        Returns:
            Dict mapping ticker symbol → pd.Series of adjusted closing prices.
        """
        result: dict[str, pd.Series] = {}
        for ticker in tickers:
            df = self.fetch_price_history(ticker, start=start, end=end)
            result[ticker] = self.get_adjusted_prices(df)
        return result
