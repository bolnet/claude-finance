"""
Data validation wrapper for finance DataFrames.

Provides user-friendly error messages for common data quality issues.
Called by adapter.py after every yfinance download.
"""
import pandas as pd


class ValidationError(Exception):
    """User-facing validation error. Message describes the data problem in plain English."""
    pass


def validate_dataframe(df: pd.DataFrame, ticker: str = "") -> None:
    """
    Validate a price DataFrame returned by yfinance.

    Checks:
    1. DataFrame is not empty — no data means bad ticker or empty date range
    2. 'Close' column is present — required for all return/price calculations
    3. DataFrame has at least 2 rows — single-row DataFrames can't compute returns

    Args:
        df: DataFrame to validate (from yf.download with auto_adjust=True)
        ticker: Ticker symbol for error messages. Optional.

    Returns:
        None if validation passes.

    Raises:
        ValidationError: With a plain-English message if any check fails.
    """
    label = f" for '{ticker}'" if ticker else ""

    if df is None or (hasattr(df, "empty") and df.empty):
        raise ValidationError(
            f"No data returned{label}. "
            f"The ticker may be delisted or the date range contains no trading days."
        )

    if not isinstance(df, pd.DataFrame):
        raise ValidationError(
            f"Expected a DataFrame{label} but got {type(df).__name__}."
        )

    if "Close" not in df.columns:
        raise ValidationError(
            f"Expected a 'Close' column{label} but got: {list(df.columns)}. "
            f"This may indicate a yfinance API change — check the adapter.py version note."
        )

    if len(df) < 2:
        raise ValidationError(
            f"Only {len(df)} row(s) returned{label}. "
            f"At least 2 trading days are needed to compute returns. "
            f"Try expanding the date range."
        )
