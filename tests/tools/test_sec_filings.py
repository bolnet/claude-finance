"""Tests for SEC filings tools — TDD-first."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from finance_mcp.output import DISCLAIMER
from finance_mcp.providers.base import Capability


def _make_provider(capabilities: set[Capability]) -> MagicMock:
    provider = MagicMock()
    provider.capabilities = frozenset(capabilities)
    return provider


SAMPLE_FILINGS = [
    {"type": "10-K", "date": "2024-02-15", "company": "Apple Inc."},
    {"type": "10-Q", "date": "2024-05-01", "company": "Apple Inc."},
    {"type": "8-K", "date": "2024-03-10", "company": "Apple Inc."},
]

SAMPLE_RISK_FACTORS = (
    "Risk Factor 1: Competition in the technology market is intense.\n"
    "Risk Factor 2: Supply chain disruptions may affect production."
)


def test_get_sec_filings_returns_string():
    """get_sec_filings returns a non-empty string."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        result = get_sec_filings(ticker="AAPL", filing_type="10-K", limit=10)

    assert isinstance(result, str)
    assert len(result) > 0


def test_get_sec_filings_contains_filing_types():
    """get_sec_filings output includes filing type column data."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        result = get_sec_filings(ticker="AAPL", limit=10)

    assert "10-K" in result
    assert "10-Q" in result


def test_get_sec_filings_contains_company():
    """get_sec_filings output includes company names."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        result = get_sec_filings(ticker="AAPL", limit=10)

    assert "Apple" in result


def test_get_sec_filings_ends_with_disclaimer():
    """get_sec_filings output ends with the standard disclaimer."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        result = get_sec_filings(ticker="AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_sec_filings_capability_missing_raises():
    """get_sec_filings raises ToolError when provider lacks SEC_FILINGS capability."""
    from fastmcp.exceptions import ToolError
    provider = _make_provider(set())
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        with pytest.raises(ToolError):
            get_sec_filings(ticker="AAPL")


def test_get_sec_filings_calls_provider_with_args():
    """get_sec_filings passes ticker, filing_type, and limit to provider."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        get_sec_filings(ticker="AAPL", filing_type="10-K", limit=5)

    provider.sec_filings.assert_called_once_with("AAPL", "10-K", 5)


def test_get_risk_factors_returns_string():
    """get_risk_factors returns a non-empty string."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_risk_factors.return_value = SAMPLE_RISK_FACTORS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_risk_factors
        result = get_risk_factors(ticker="AAPL")

    assert isinstance(result, str)
    assert len(result) > 0


def test_get_risk_factors_contains_risk_text():
    """get_risk_factors output includes the risk factor content from provider."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_risk_factors.return_value = SAMPLE_RISK_FACTORS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_risk_factors
        result = get_risk_factors(ticker="AAPL")

    assert "Competition" in result or "Supply chain" in result


def test_get_risk_factors_ends_with_disclaimer():
    """get_risk_factors output ends with the standard disclaimer."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_risk_factors.return_value = SAMPLE_RISK_FACTORS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_risk_factors
        result = get_risk_factors(ticker="AAPL")

    assert result.strip().endswith(DISCLAIMER)


def test_get_risk_factors_capability_missing_raises():
    """get_risk_factors raises ToolError when provider lacks SEC_FILINGS capability."""
    from fastmcp.exceptions import ToolError
    provider = _make_provider(set())
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_risk_factors
        with pytest.raises(ToolError):
            get_risk_factors(ticker="AAPL")


def test_get_risk_factors_calls_provider_with_ticker():
    """get_risk_factors passes the ticker to provider.sec_risk_factors."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_risk_factors.return_value = SAMPLE_RISK_FACTORS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_risk_factors
        get_risk_factors(ticker="MSFT")

    provider.sec_risk_factors.assert_called_once_with("MSFT")


def test_get_sec_filings_plain_english_first():
    """get_sec_filings output starts with an alphabetical character."""
    provider = _make_provider({Capability.SEC_FILINGS})
    provider.sec_filings.return_value = SAMPLE_FILINGS
    with patch("finance_mcp.tools.sec_filings.get_provider", return_value=provider):
        from finance_mcp.tools.sec_filings import get_sec_filings
        result = get_sec_filings(ticker="AAPL")

    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"
