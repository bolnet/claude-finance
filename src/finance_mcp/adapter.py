"""
yfinance adapter layer — single point of change for all Yahoo Finance API calls.

CRITICAL: This is the ONLY module in finance_mcp that may import yfinance directly.
All other modules must import from this adapter, never from yfinance directly.

yfinance 0.2.54+ behavior (DEFAULT auto_adjust=True):
  - 'Close' column IS the split-and-dividend-adjusted price
  - 'Adj Close' column does NOT exist (dropped in 0.2.54)
  - DO NOT reference df['Adj Close'] — it will raise KeyError

Reference: yfinance GitHub issue #2283
"""
import sys
from typing import Optional

import yfinance as yf
import pandas as pd

from finance_mcp.validators import validate_dataframe, ValidationError


class DataFetchError(Exception):
    """User-facing error for data fetch failures. Message is shown to the user."""
    pass


def fetch_price_history(
    ticker: str,
    start: str,
    end: Optional[str] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch adjusted daily price history for a single ticker.

    Returns a DataFrame with DatetimeIndex and columns: Open, High, Low, Close, Volume.
    'Close' is the split-and-dividend-adjusted price (auto_adjust=True default).

    Args:
        ticker: Yahoo Finance ticker symbol (e.g. "AAPL", "MSFT")
        start: Start date as ISO string "YYYY-MM-DD". Required unless period is given.
        end: End date as ISO string "YYYY-MM-DD". Optional; defaults to today.
        period: yfinance period string e.g. "1y", "6mo". If given, start/end are ignored.

    Raises:
        DataFetchError: With a user-readable message if fetch fails, ticker invalid,
                        date range empty, or DataFrame is empty.
    """
    ticker_upper = ticker.strip().upper()
    try:
        kwargs: dict = {"auto_adjust": True, "progress": False}
        if period:
            kwargs["period"] = period
        else:
            kwargs["start"] = start
            if end:
                kwargs["end"] = end
        df = yf.download(ticker_upper, **kwargs)
    except Exception as exc:
        raise DataFetchError(
            f"Could not fetch data for '{ticker_upper}'. "
            f"Check that the ticker is valid and your internet connection is active. "
            f"(Details: {exc})"
        ) from exc

    # Flatten MultiIndex columns produced for single-ticker downloads in some yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    if df.empty:
        raise DataFetchError(
            f"No price data returned for '{ticker_upper}'. "
            f"The ticker may be delisted, misspelled, or the date range contains no trading days."
        )

    # Validate column presence and data quality
    try:
        validate_dataframe(df, ticker=ticker_upper)
    except ValidationError as exc:
        raise DataFetchError(str(exc)) from exc

    print(
        f"[finance-mcp] Fetched {len(df)} rows for {ticker_upper}",
        file=sys.stderr,
    )
    return df


def get_adjusted_prices(df: pd.DataFrame) -> pd.Series:
    """
    Extract the adjusted closing price series from a fetched DataFrame.

    With auto_adjust=True (our standard), 'Close' IS the adjusted price.
    Use this accessor everywhere — never reference df['Close'] directly in callers.

    Returns: pd.Series with DatetimeIndex and name='Close'
    """
    return df["Close"]


def fetch_multi_ticker(
    tickers: list[str],
    start: str,
    end: Optional[str] = None,
    period: Optional[str] = None,
) -> dict[str, pd.Series]:
    """
    Fetch adjusted close price series for multiple tickers.

    Returns a dict mapping ticker symbol → pd.Series of adjusted closing prices.
    Tickers that fail to fetch are omitted from the result (error logged to stderr).

    Args:
        tickers: List of ticker symbols.
        start: Start date "YYYY-MM-DD". Required unless period given.
        end: End date "YYYY-MM-DD". Optional.
        period: yfinance period string. If given, start/end ignored.
    """
    tickers_upper = [t.strip().upper() for t in tickers]
    result: dict[str, pd.Series] = {}
    for ticker in tickers_upper:
        try:
            df = fetch_price_history(ticker, start=start, end=end, period=period)
            result[ticker] = get_adjusted_prices(df)
        except DataFetchError as exc:
            print(f"[finance-mcp] Skipping {ticker}: {exc}", file=sys.stderr)
    return result
