"""
Live integration tests for all 6 market analysis MCP tools.

These tests call the actual tool functions with real Yahoo Finance data.
No mocks. They prove each tool produces correct formatted output with charts
before the human verification step.

TDD: Plan 06-01 — created in RED phase before implementation exists.
"""
import sys
import datetime

import pytest

# Ensure src/ is importable
sys.path.insert(0, "src")

from finance_mcp.tools.price_chart import analyze_stock
from finance_mcp.tools.returns import get_returns
from finance_mcp.tools.volatility import get_volatility
from finance_mcp.tools.risk_metrics import get_risk_metrics
from finance_mcp.tools.comparison import compare_tickers
from finance_mcp.tools.correlation import correlation_map


# ---------------------------------------------------------------------------
# Date helpers (computed once per session)
# ---------------------------------------------------------------------------

def _date_str(days_back: int) -> str:
    """Return ISO date string N days before today."""
    return (datetime.date.today() - datetime.timedelta(days=days_back)).isoformat()


START_90D = _date_str(90)
START_365D = _date_str(365)


# ---------------------------------------------------------------------------
# Test 1: analyze_stock
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_analyze_stock_live():
    """analyze_stock returns a non-empty string with chart path and ticker reference."""
    result = analyze_stock("AAPL", START_90D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    assert "AAPL" in result, "Output must reference the requested ticker"
    assert "Chart saved" in result or ".png" in result, (
        "Output must include a chart path (Chart saved ... .png)"
    )


# ---------------------------------------------------------------------------
# Test 2: get_returns
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_get_returns_live():
    """get_returns returns a non-empty string with ticker reference and return keyword."""
    result = get_returns("AAPL", START_90D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    assert "AAPL" in result, "Output must reference the requested ticker"
    assert "return" in result.lower(), "Output must mention 'return'"
    assert ".png" in result, "Output must include a chart path"


# ---------------------------------------------------------------------------
# Test 3: get_volatility
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_get_volatility_live():
    """get_volatility returns a non-empty string with ticker reference and volatility keyword."""
    result = get_volatility("AAPL", START_90D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    assert "AAPL" in result, "Output must reference the requested ticker"
    assert "volatility" in result.lower(), "Output must mention 'volatility'"
    assert ".png" in result, "Output must include a chart path"


# ---------------------------------------------------------------------------
# Test 4: get_risk_metrics
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_get_risk_metrics_live():
    """get_risk_metrics returns output with all three metric names: Sharpe, drawdown, beta."""
    result = get_risk_metrics("AAPL", START_365D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    result_lower = result.lower()
    assert "sharpe" in result_lower, "Output must mention Sharpe ratio"
    assert "drawdown" in result_lower, "Output must mention max drawdown"
    assert "beta" in result_lower, "Output must mention beta"


# ---------------------------------------------------------------------------
# Test 5: compare_tickers
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_compare_tickers_live():
    """compare_tickers returns a non-empty string with a chart path."""
    result = compare_tickers("AAPL,MSFT", START_90D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    assert "Chart saved" in result or "chart" in result.lower() or ".png" in result, (
        "Output must include a chart path"
    )


# ---------------------------------------------------------------------------
# Test 6: correlation_map
# ---------------------------------------------------------------------------


@pytest.mark.network
@pytest.mark.xfail(reason="network — Yahoo Finance may be unreachable")
def test_correlation_map_live():
    """correlation_map returns a non-empty string with correlation or heatmap keyword."""
    result = correlation_map("AAPL,MSFT,GOOGL", START_90D)
    assert isinstance(result, str) and len(result) > 0, "Expected non-empty string output"
    result_lower = result.lower()
    assert "correlation" in result_lower or "heatmap" in result_lower, (
        "Output must mention 'correlation' or 'heatmap'"
    )
    assert ".png" in result, "Output must include a chart path"
