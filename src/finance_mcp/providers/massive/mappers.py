"""Pure data transformation functions: Massive JSON → pandas / plain Python.

No API calls are made here. Each function accepts a raw response dict
(as returned by the Massive REST API) and returns a pandas DataFrame,
Series, or plain Python dict / list.
"""
from __future__ import annotations

from typing import Any

import pandas as pd


# ---------------------------------------------------------------------------
# Aggregates (OHLCV bars)
# ---------------------------------------------------------------------------

_AGG_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def aggs_to_dataframe(raw: dict[str, Any]) -> pd.DataFrame:
    """Convert a Massive aggregates response to a DataFrame.

    Timestamp column ``t`` (milliseconds, UTC) becomes the DatetimeIndex.
    Returns an empty DataFrame with the correct column schema when there are
    no results.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    if not results:
        return pd.DataFrame(columns=_AGG_COLUMNS)

    records = [
        {
            "timestamp": bar["t"],
            "Open": bar["o"],
            "High": bar["h"],
            "Low": bar["l"],
            "Close": bar["c"],
            "Volume": bar["v"],
        }
        for bar in results
    ]
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp")
    df.index.name = None
    return df[_AGG_COLUMNS]


# ---------------------------------------------------------------------------
# Previous Close
# ---------------------------------------------------------------------------


def prev_close_to_dict(raw: dict[str, Any]) -> dict[str, Any]:
    """Extract the first entry from a prev-close results list.

    Returns a dict with snake_case keys: ticker, open, high, low, close,
    volume, timestamp.
    """
    result: dict[str, Any] = (raw.get("results") or [{}])[0]
    return {
        "ticker": result.get("T"),
        "open": result.get("o"),
        "high": result.get("h"),
        "low": result.get("l"),
        "close": result.get("c"),
        "volume": result.get("v"),
        "timestamp": result.get("t"),
    }


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------


def _extract_snapshot_item(item: dict[str, Any]) -> dict[str, Any]:
    """Convert a single ticker snapshot object to a flat dict."""
    day: dict[str, Any] = item.get("day") or {}
    prev_day: dict[str, Any] = item.get("prevDay") or {}
    return {
        "ticker": item.get("ticker"),
        "change": item.get("todaysChange"),
        "change_percent": item.get("todaysChangePerc"),
        "open": day.get("o"),
        "high": day.get("h"),
        "low": day.get("l"),
        "close": day.get("c"),
        "volume": day.get("v"),
        "prev_close": prev_day.get("c"),
    }


def snapshot_to_dict(raw: dict[str, Any]) -> dict[str, Any]:
    """Convert a single-ticker or multi-ticker snapshot response to a dict.

    Handles both ``{"ticker": {...}}`` and ``{"tickers": [...]}`` shapes.
    When the tickers list shape is provided the first entry is used.
    """
    if "ticker" in raw:
        item: dict[str, Any] = raw["ticker"]
    else:
        tickers: list[dict[str, Any]] = raw.get("tickers") or []
        item = tickers[0] if tickers else {}
    return _extract_snapshot_item(item)


def snapshots_to_list(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a multi-ticker snapshot response to a list of dicts."""
    tickers: list[dict[str, Any]] = raw.get("tickers") or []
    return [_extract_snapshot_item(item) for item in tickers]


# ---------------------------------------------------------------------------
# News
# ---------------------------------------------------------------------------


def news_to_list(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a news results list to plain Python dicts.

    Each dict contains: title, published_utc, article_url, author,
    description, tickers.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    return [
        {
            "title": article.get("title"),
            "published_utc": article.get("published_utc"),
            "article_url": article.get("article_url"),
            "author": article.get("author"),
            "description": article.get("description"),
            "tickers": article.get("tickers"),
        }
        for article in results
    ]


# ---------------------------------------------------------------------------
# Options Chain
# ---------------------------------------------------------------------------


def options_chain_to_list(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert an options chain response to a list of flat contract dicts.

    Each dict contains contract details, greeks (or None values), implied
    volatility, open interest, last price, and volume.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    contracts: list[dict[str, Any]] = []
    for entry in results:
        details: dict[str, Any] = entry.get("details") or {}
        greeks: dict[str, Any] = entry.get("greeks") or {}
        last_quote: dict[str, Any] = entry.get("last_quote") or {}
        day: dict[str, Any] = entry.get("day") or {}
        contracts.append(
            {
                # Contract details
                "strike_price": details.get("strike_price"),
                "expiration_date": details.get("expiration_date"),
                "contract_type": details.get("contract_type"),
                # Greeks (None when not available)
                "delta": greeks.get("delta"),
                "gamma": greeks.get("gamma"),
                "theta": greeks.get("theta"),
                "vega": greeks.get("vega"),
                # Other metrics
                "implied_volatility": entry.get("implied_volatility"),
                "open_interest": entry.get("open_interest"),
                "last_price": last_quote.get("last_price"),
                "volume": day.get("volume"),
            }
        )
    return contracts


# ---------------------------------------------------------------------------
# Trades
# ---------------------------------------------------------------------------

_TRADE_COLUMNS = ["price", "size", "timestamp", "exchange"]


def trades_to_dataframe(raw: dict[str, Any]) -> pd.DataFrame:
    """Convert a trades response to a DataFrame.

    Timestamp ``t`` (nanoseconds) is converted to a UTC-aware datetime column.
    Returns an empty DataFrame with the correct schema when there are no
    results.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    if not results:
        empty = pd.DataFrame(columns=_TRADE_COLUMNS)
        empty["timestamp"] = pd.Series(dtype="datetime64[ns, UTC]")
        return empty

    records = [
        {
            "price": trade["p"],
            "size": trade["s"],
            "timestamp": trade["t"],
            "exchange": trade.get("x"),
        }
        for trade in results
    ]
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns", utc=True)
    return df[_TRADE_COLUMNS]


# ---------------------------------------------------------------------------
# Technical Indicators
# ---------------------------------------------------------------------------


def indicator_to_series(raw: dict[str, Any]) -> pd.Series:
    """Convert a technical indicator response (e.g. SMA) to a Series.

    The index is a UTC DatetimeIndex derived from the ``timestamp`` field
    (milliseconds).  Returns an empty Series when there are no values.
    """
    results: dict[str, Any] = raw.get("results") or {}
    values: list[dict[str, Any]] = results.get("values") or [] if results else []
    if not values:
        return pd.Series(dtype=float)

    timestamps = pd.to_datetime(
        [v["timestamp"] for v in values], unit="ms", utc=True
    )
    data = [v["value"] for v in values]
    return pd.Series(data, index=timestamps, dtype=float)


# ---------------------------------------------------------------------------
# Dividends
# ---------------------------------------------------------------------------


def dividends_to_list(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a dividends response to a list of dicts.

    Each dict contains: ex_dividend_date, pay_date, cash_amount, frequency.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    return [
        {
            "ex_dividend_date": item.get("ex_dividend_date"),
            "pay_date": item.get("pay_date"),
            "cash_amount": item.get("cash_amount"),
            "frequency": item.get("frequency"),
        }
        for item in results
    ]


# ---------------------------------------------------------------------------
# Splits
# ---------------------------------------------------------------------------


def splits_to_list(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a stock splits response to a list of dicts.

    Each dict contains: execution_date, split_from, split_to.
    """
    results: list[dict[str, Any]] = raw.get("results") or []
    return [
        {
            "execution_date": item.get("execution_date"),
            "split_from": item.get("split_from"),
            "split_to": item.get("split_to"),
        }
        for item in results
    ]


# ---------------------------------------------------------------------------
# Ticker Details
# ---------------------------------------------------------------------------

_TICKER_DETAIL_FIELDS = (
    "ticker",
    "name",
    "market",
    "locale",
    "type",
    "currency_name",
    "market_cap",
    "description",
    "sic_code",
    "sic_description",
    "homepage_url",
    "total_employees",
    "list_date",
    "share_class_shares_outstanding",
    "weighted_shares_outstanding",
)


def ticker_details_to_dict(raw: dict[str, Any]) -> dict[str, Any]:
    """Convert a ticker details response to a flat dict.

    Missing optional fields are represented as ``None``.
    """
    results: dict[str, Any] = raw.get("results") or {}
    return {field: results.get(field) for field in _TICKER_DETAIL_FIELDS}
