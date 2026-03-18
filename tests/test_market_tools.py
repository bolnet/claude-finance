"""Phase 2 market analysis tool tests — MKTX-01 through MKTX-07."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


def test_analyze_stock_returns_output():
    """analyze_stock returns formatted string starting with plain English, ending with DISCLAIMER."""
    from unittest.mock import patch
    from finance_mcp.output import DISCLAIMER

    # Synthetic price series: 10 trading days, starting at 100
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 110]}, index=dates)

    with patch("finance_mcp.tools.price_chart.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.price_chart import analyze_stock
        result = analyze_stock("AAPL", "2024-01-02", "2024-01-15")

    assert isinstance(result, str)
    # Must start with plain-English text (letter, not digit or special)
    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"
    assert result.strip().endswith(DISCLAIMER)


def test_analyze_stock_saves_chart(tmp_path, monkeypatch):
    """analyze_stock saves a PNG to finance_output/charts/."""
    import os

    # Redirect chart output to tmp_path
    monkeypatch.chdir(tmp_path)

    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 110]}, index=dates)

    with patch("finance_mcp.tools.price_chart.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.price_chart import analyze_stock
        result = analyze_stock("AAPL", "2024-01-02", "2024-01-15")

    chart_dir = tmp_path / "finance_output" / "charts"
    png_files = list(chart_dir.glob("*.png"))
    assert len(png_files) == 1, f"Expected 1 PNG in {chart_dir}, found {png_files}"


def test_get_returns_values():
    pytest.fail("stub — implement when tool is ready")


def test_get_returns_chart():
    pytest.fail("stub — implement when tool is ready")


def test_annualized_volatility_formula():
    pytest.fail("stub — implement when tool is ready")


def test_volatility_chart():
    pytest.fail("stub — implement when tool is ready")


def test_sharpe_sign():
    pytest.fail("stub — implement when tool is ready")


def test_max_drawdown_nonpositive():
    pytest.fail("stub — implement when tool is ready")


def test_beta_calculation():
    pytest.fail("stub — implement when tool is ready")


def test_normalized_prices_start_at_100():
    pytest.fail("stub — implement when tool is ready")


def test_compare_tickers_chart():
    pytest.fail("stub — implement when tool is ready")


def test_correlation_uses_returns():
    pytest.fail("stub — implement when tool is ready")


def test_correlation_map_chart():
    pytest.fail("stub — implement when tool is ready")


def test_output_plain_english_first():
    pytest.fail("stub — implement when tool is ready")


def test_output_ends_with_disclaimer():
    pytest.fail("stub — implement when tool is ready")
