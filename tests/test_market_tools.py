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
    """Daily returns are pct_change; cumulative is compound product."""
    import pandas as pd
    import numpy as np
    from unittest.mock import patch

    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    # Uniform 1% daily increases: price[i] = 100 * 1.01^i
    prices = pd.Series([100 * (1.01 ** i) for i in range(10)], index=dates)
    mock_df = pd.DataFrame({"Close": prices})

    with patch("finance_mcp.tools.returns.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.returns import get_returns
        result = get_returns("TEST", "2024-01-02", "2024-01-15")

    # Verify result is a string containing return data
    assert isinstance(result, str)
    assert "%" in result  # return percentages present
    # Cumulative return after 9 steps of 1% = (1.01^9 - 1) ≈ 9.37%
    expected_total = (1.01 ** 9 - 1) * 100
    assert str(round(expected_total, 0))[:2] in result or "9." in result  # ~9.4% mentioned


def test_get_returns_chart(tmp_path, monkeypatch):
    """get_returns saves a PNG to finance_output/charts/."""
    import pandas as pd
    from unittest.mock import patch

    monkeypatch.chdir(tmp_path)
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100 + i for i in range(10)]}, index=dates)

    with patch("finance_mcp.tools.returns.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.returns import get_returns
        get_returns("TEST", "2024-01-02", "2024-01-15")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


def test_annualized_volatility_formula():
    """Annualized vol = daily_std * sqrt(252) to float precision."""
    import pandas as pd
    import numpy as np
    from unittest.mock import patch

    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    # Construct returns with known std = 0.01
    np.random.seed(42)
    daily_rets = pd.Series(np.random.normal(0, 0.01, 30), index=dates)
    prices = (1 + daily_rets).cumprod() * 100
    mock_df = pd.DataFrame({"Close": prices})

    # Compute expected value independently
    actual_daily_rets = prices.pct_change().dropna()
    expected_vol = actual_daily_rets.std() * np.sqrt(252)

    with patch("finance_mcp.tools.volatility.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.volatility import get_volatility
        result = get_volatility("TEST", "2024-01-02", "2024-02-15")

    # The expected vol in % should appear in the output
    expected_pct = f"{expected_vol * 100:.2f}%"
    assert expected_pct in result, f"Expected {expected_pct} in output, got snippet: {result[:200]}"


def test_volatility_chart(tmp_path, monkeypatch):
    """get_volatility saves a PNG to finance_output/charts/."""
    import pandas as pd
    import numpy as np
    from unittest.mock import patch

    monkeypatch.chdir(tmp_path)
    np.random.seed(0)
    dates = pd.date_range("2024-01-02", periods=40, freq="B")
    prices = (1 + pd.Series(np.random.normal(0, 0.01, 40), index=dates)).cumprod() * 100
    mock_df = pd.DataFrame({"Close": prices})

    with patch("finance_mcp.tools.volatility.fetch_price_history", return_value=mock_df):
        from finance_mcp.tools.volatility import get_volatility
        get_volatility("TEST", "2024-01-02", "2024-03-01")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


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
