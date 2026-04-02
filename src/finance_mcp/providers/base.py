"""DataProvider Protocol and Capability flags for the finance MCP server."""
from __future__ import annotations

import enum
from typing import Protocol, runtime_checkable

import pandas as pd


class Capability(enum.Enum):
    """Flags representing data capabilities a provider may support."""

    PRICE_HISTORY = "price_history"
    NEWS = "news"
    OPTIONS_CHAIN = "options_chain"
    FOREX = "forex"
    CRYPTO = "crypto"
    INDICES = "indices"
    TECHNICALS = "technicals"
    FUNDAMENTALS = "fundamentals"
    SEC_FILINGS = "sec_filings"
    MARKET_MOVERS = "market_movers"
    TICKER_INFO = "ticker_info"


@runtime_checkable
class DataProvider(Protocol):
    """Protocol for all data providers in the finance MCP server.

    Any class that implements the required methods and the ``capabilities``
    property satisfies this Protocol and can be used wherever a DataProvider
    is expected.
    """

    @property
    def capabilities(self) -> frozenset[Capability]:
        """Return the set of capabilities this provider supports."""
        ...

    def fetch_price_history(
        self,
        ticker: str,
        start: str,
        end: str | None = None,
        period: str | None = None,
    ) -> pd.DataFrame:
        """Fetch adjusted daily price history for a single ticker.

        Args:
            ticker: Ticker symbol (e.g. "AAPL").
            start: Start date as "YYYY-MM-DD".
            end: End date as "YYYY-MM-DD". Optional.
            period: Provider-specific period string (e.g. "1y"). Optional.

        Returns:
            DataFrame with DatetimeIndex and OHLCV columns.
        """
        ...

    def get_adjusted_prices(self, df: pd.DataFrame) -> pd.Series:
        """Extract the adjusted closing price series from a fetched DataFrame.

        Args:
            df: DataFrame returned by ``fetch_price_history``.

        Returns:
            pd.Series with DatetimeIndex representing adjusted close prices.
        """
        ...

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
            period: Provider-specific period string. Optional.

        Returns:
            Dict mapping ticker symbol → pd.Series of adjusted closing prices.
        """
        ...
