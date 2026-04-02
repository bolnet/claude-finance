"""Massive options endpoints mixin.

Provides four options-related methods that delegate HTTP calls to
``self.client`` (a :class:`~finance_mcp.providers.massive.client.MassiveClient`
or any object exposing the same ``get`` interface).
"""
from __future__ import annotations

from typing import Any

from finance_mcp.providers.massive.mappers import (
    options_chain_to_list,
    prev_close_to_dict,
)


class OptionsMixin:
    """Mixin that adds options data methods to a Massive provider.

    Expects the host class to expose ``self.client`` with a
    ``get(path, params=None)`` method returning a raw JSON dict.
    """

    client: Any  # typed as Any to avoid circular imports; real type is MassiveClient

    # ------------------------------------------------------------------
    # 1. Options contracts reference data
    # ------------------------------------------------------------------

    def options_contracts(
        self,
        underlying_ticker: str,
        contract_type: str | None = None,
        expiration_date: str | None = None,
        strike_price: float | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch options contracts for an underlying ticker.

        Args:
            underlying_ticker: The stock ticker (e.g. ``"AAPL"``).
            contract_type: ``"call"`` or ``"put"`` filter, or ``None`` for all.
            expiration_date: ISO 8601 date string filter (``"YYYY-MM-DD"``).
            strike_price: Strike price filter.
            limit: Maximum number of results. Defaults to 100.

        Returns:
            Raw list of contract dicts from the ``results`` key.
        """
        params: dict[str, Any] = {
            "underlying_ticker": underlying_ticker,
            "limit": limit,
        }
        if contract_type is not None:
            params["contract_type"] = contract_type
        if expiration_date is not None:
            params["expiration_date"] = expiration_date
        if strike_price is not None:
            params["strike_price"] = strike_price

        raw = self.client.get("/v3/reference/options/contracts", params=params)
        return (raw.get("results") or [])

    # ------------------------------------------------------------------
    # 2. Options previous close
    # ------------------------------------------------------------------

    def options_prev_close(self, options_ticker: str) -> dict[str, Any]:
        """Fetch the previous-day close for a specific options contract.

        Args:
            options_ticker: The options contract ticker (e.g.
                ``"O:AAPL230616C00150000"``).

        Returns:
            Dict with keys: ticker, open, high, low, close, volume, timestamp.
        """
        path = f"/v2/aggs/ticker/{options_ticker}/prev"
        raw = self.client.get(path)
        return prev_close_to_dict(raw)

    # ------------------------------------------------------------------
    # 3. Options chain snapshot
    # ------------------------------------------------------------------

    def options_chain_snapshot(
        self,
        underlying_ticker: str,
        contract_type: str | None = None,
        expiration_date: str | None = None,
        strike_price: float | None = None,
        limit: int = 250,
    ) -> list[dict[str, Any]]:
        """Fetch the full options chain snapshot for an underlying ticker.

        Args:
            underlying_ticker: The stock ticker (e.g. ``"AAPL"``).
            contract_type: ``"call"`` or ``"put"`` filter.
            expiration_date: ISO 8601 date string filter.
            strike_price: Strike price filter.
            limit: Maximum number of results. Defaults to 250.

        Returns:
            List of flat contract dicts including greeks and market data.
        """
        params: dict[str, Any] = {"limit": limit}
        if contract_type is not None:
            params["contract_type"] = contract_type
        if expiration_date is not None:
            params["expiration_date"] = expiration_date
        if strike_price is not None:
            params["strike_price"] = strike_price

        path = f"/v3/snapshot/options/{underlying_ticker}"
        raw = self.client.get(path, params=params)
        return options_chain_to_list(raw)

    # ------------------------------------------------------------------
    # 4. Single options contract snapshot
    # ------------------------------------------------------------------

    def options_single_snapshot(
        self,
        underlying_ticker: str,
        option_contract: str,
    ) -> dict[str, Any]:
        """Fetch a snapshot for a single options contract.

        Args:
            underlying_ticker: The underlying stock ticker (e.g. ``"AAPL"``).
            option_contract: The options contract ticker (e.g.
                ``"O:AAPL230616C00150000"``).

        Returns:
            Dict with keys: details, greeks, implied_volatility, open_interest,
            last_price, volume.
        """
        path = f"/v3/snapshot/options/{underlying_ticker}/{option_contract}"
        raw = self.client.get(path)
        result: dict[str, Any] = raw.get("results") or {}

        last_quote: dict[str, Any] = result.get("last_quote") or {}
        day: dict[str, Any] = result.get("day") or {}

        return {
            "details": result.get("details"),
            "greeks": result.get("greeks"),
            "implied_volatility": result.get("implied_volatility"),
            "open_interest": result.get("open_interest"),
            "last_price": last_quote.get("last_price"),
            "volume": day.get("volume"),
        }
