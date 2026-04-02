"""BlockedEndpointsMixin – stubs for Massive endpoints beyond current subscription.

Each method raises :class:`NotImplementedError` with a clear message indicating
the required subscription tier.
"""
from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Available expansions (add-on data packages)
# ---------------------------------------------------------------------------

AVAILABLE_EXPANSIONS: list[dict[str, str]] = [
    {
        "name": "TMX",
        "price": "$99/mo",
        "description": "Canadian equities and derivatives data from TMX Group.",
    },
    {
        "name": "Consumer Spending",
        "price": "$99/mo",
        "description": "Aggregated consumer spending trends and transaction data.",
    },
    {
        "name": "ETF Global – Holdings",
        "price": "$99/mo",
        "description": "ETF holdings data from ETF Global.",
    },
    {
        "name": "ETF Global – Index Constituents",
        "price": "$99/mo",
        "description": "Index constituent data for ETFs from ETF Global.",
    },
    {
        "name": "ETF Global – Mutual Fund Holdings",
        "price": "$99/mo",
        "description": "Mutual fund holdings data from ETF Global.",
    },
    {
        "name": "ETF Global – Benchmark",
        "price": "$99/mo",
        "description": "Benchmark comparison data from ETF Global.",
    },
    {
        "name": "ETF Global – Fund Flows",
        "price": "$99/mo",
        "description": "Fund flow analytics from ETF Global.",
    },
    {
        "name": "Benzinga – IPOs Calendar",
        "price": "$99/mo",
        "description": "Upcoming and historical IPO calendar data from Benzinga.",
    },
    {
        "name": "Benzinga – Conference Calls",
        "price": "$99/mo",
        "description": "Earnings and corporate conference call schedules from Benzinga.",
    },
    {
        "name": "Benzinga – Dividends Calendar",
        "price": "$99/mo",
        "description": "Dividend announcement and payment calendar from Benzinga.",
    },
    {
        "name": "Benzinga – Ratings",
        "price": "$99/mo",
        "description": "Analyst ratings and upgrades/downgrades from Benzinga.",
    },
    {
        "name": "Benzinga – Guidance",
        "price": "$99/mo",
        "description": "Corporate earnings guidance data from Benzinga.",
    },
    {
        "name": "Unusual Whales",
        "price": "$99/mo",
        "description": "Unusual options flow and dark-pool activity from Unusual Whales.",
    },
]


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------


class BlockedEndpointsMixin:
    """Stubs for endpoints blocked by current subscription tier.

    Each method raises :class:`NotImplementedError` with a message explaining
    which tier is required and what is currently active.
    """

    # ------------------------------------------------------------------
    # Stocks-tier blocked endpoints
    # ------------------------------------------------------------------

    def nbbo_quotes(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Stocks Advanced+ tier."""
        raise NotImplementedError(
            f"nbbo_quotes({ticker!r}) requires Stocks Advanced+ ($199/mo), "
            "current: Stocks Developer ($79/mo)"
        )

    def balance_sheets(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Stocks Business+ tier."""
        raise NotImplementedError(
            f"balance_sheets({ticker!r}) requires Stocks Business+ ($399/mo)"
        )

    def income_statements(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Stocks Business+ tier."""
        raise NotImplementedError(
            f"income_statements({ticker!r}) requires Stocks Business+ ($399/mo)"
        )

    def financial_ratios(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Stocks Business+ tier."""
        raise NotImplementedError(
            f"financial_ratios({ticker!r}) requires Stocks Business+ ($399/mo)"
        )

    # ------------------------------------------------------------------
    # Options-tier blocked endpoints
    # ------------------------------------------------------------------

    def options_trades(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Options Developer+ tier."""
        raise NotImplementedError(
            f"options_trades({ticker!r}) requires Options Developer+ ($79/mo), "
            "current: Options Starter ($29/mo)"
        )

    def options_quotes(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Options Developer+ tier."""
        raise NotImplementedError(
            f"options_quotes({ticker!r}) requires Options Developer+ ($79/mo), "
            "current: Options Starter ($29/mo)"
        )

    def options_last_trade(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Options Developer+ tier."""
        raise NotImplementedError(
            f"options_last_trade({ticker!r}) requires Options Developer+ ($79/mo), "
            "current: Options Starter ($29/mo)"
        )

    # ------------------------------------------------------------------
    # Partner / add-on blocked endpoints
    # ------------------------------------------------------------------

    def benzinga_partner(self, **kwargs: Any) -> Any:  # noqa: ANN401
        """Blocked: requires Benzinga add-on."""
        raise NotImplementedError(
            "benzinga_partner() requires Benzinga add-on ($99/mo)"
        )

    def tmx_partner(self, **kwargs: Any) -> Any:  # noqa: ANN401
        """Blocked: requires TMX add-on."""
        raise NotImplementedError(
            "tmx_partner() requires TMX add-on ($99/mo)"
        )

    # ------------------------------------------------------------------
    # Currencies-tier blocked endpoint
    # ------------------------------------------------------------------

    def crypto_trades(self, ticker: str) -> Any:  # noqa: ANN401
        """Blocked: requires Currencies Developer+ tier."""
        raise NotImplementedError(
            f"crypto_trades({ticker!r}) requires Currencies Developer+ ($79/mo), "
            "current: Currencies Starter ($49/mo)"
        )
