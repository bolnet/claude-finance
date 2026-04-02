"""Tests for BlockedEndpointsMixin – all 10 blocked stubs."""
from __future__ import annotations

import pytest

from finance_mcp.providers.massive.stubs import BlockedEndpointsMixin


class ConcreteProvider(BlockedEndpointsMixin):
    """Minimal concrete class to instantiate the mixin."""


@pytest.fixture()
def provider() -> ConcreteProvider:
    return ConcreteProvider()


# ---------------------------------------------------------------------------
# Stocks-tier blocked endpoints
# ---------------------------------------------------------------------------


def test_nbbo_quotes_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Stocks Advanced"):
        provider.nbbo_quotes("AAPL")


def test_balance_sheets_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Stocks Business"):
        provider.balance_sheets("AAPL")


def test_income_statements_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Stocks Business"):
        provider.income_statements("AAPL")


def test_financial_ratios_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Stocks Business"):
        provider.financial_ratios("AAPL")


# ---------------------------------------------------------------------------
# Options-tier blocked endpoints
# ---------------------------------------------------------------------------


def test_options_trades_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Options Developer"):
        provider.options_trades("O:AAPL251219C00150000")


def test_options_quotes_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Options Developer"):
        provider.options_quotes("O:AAPL251219C00150000")


def test_options_last_trade_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Options Developer"):
        provider.options_last_trade("O:AAPL251219C00150000")


# ---------------------------------------------------------------------------
# Partner / add-on blocked endpoints
# ---------------------------------------------------------------------------


def test_benzinga_partner_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Benzinga"):
        provider.benzinga_partner()


def test_tmx_partner_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="TMX"):
        provider.tmx_partner()


# ---------------------------------------------------------------------------
# Currencies-tier blocked endpoint
# ---------------------------------------------------------------------------


def test_crypto_trades_raises(provider: ConcreteProvider) -> None:
    with pytest.raises(NotImplementedError, match="Currencies Developer"):
        provider.crypto_trades("X:BTCUSD")


# ---------------------------------------------------------------------------
# AVAILABLE_EXPANSIONS constant
# ---------------------------------------------------------------------------


def test_available_expansions_has_13_entries() -> None:
    from finance_mcp.providers.massive.stubs import AVAILABLE_EXPANSIONS

    assert len(AVAILABLE_EXPANSIONS) == 13


def test_available_expansions_have_required_keys() -> None:
    from finance_mcp.providers.massive.stubs import AVAILABLE_EXPANSIONS

    for entry in AVAILABLE_EXPANSIONS:
        assert "name" in entry
        assert "price" in entry
        assert "description" in entry


def test_available_expansions_price_format() -> None:
    from finance_mcp.providers.massive.stubs import AVAILABLE_EXPANSIONS

    for entry in AVAILABLE_EXPANSIONS:
        assert entry["price"] == "$99/mo"
