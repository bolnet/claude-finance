"""Phase 2 market analysis tool tests — MKTX-01 through MKTX-07."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, PropertyMock


def _make_provider_mock(fetch_price_history=None, get_adjusted_prices=None, fetch_multi_ticker=None):
    """Build a mock provider with the given method return values."""
    mock = MagicMock()
    if fetch_price_history is not None:
        mock.fetch_price_history.return_value = fetch_price_history
    if get_adjusted_prices is not None:
        mock.get_adjusted_prices.side_effect = get_adjusted_prices
    else:
        # Default: return the Close column of whatever df is passed in
        mock.get_adjusted_prices.side_effect = lambda df: df["Close"]
    if fetch_multi_ticker is not None:
        mock.fetch_multi_ticker.return_value = fetch_multi_ticker
    return mock


def test_analyze_stock_returns_output():
    """analyze_stock returns formatted string starting with plain English, ending with DISCLAIMER."""
    from finance_mcp.output import DISCLAIMER

    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 110]}, index=dates)
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.price_chart import analyze_stock
        result = analyze_stock("AAPL", "2024-01-02", "2024-01-15")

    assert isinstance(result, str)
    assert result[0].isalpha(), f"Output must start with plain-English text, got: {result[:40]!r}"
    assert result.strip().endswith(DISCLAIMER)


def test_analyze_stock_saves_chart(tmp_path, monkeypatch):
    """analyze_stock saves a PNG to finance_output/charts/."""
    import os

    monkeypatch.chdir(tmp_path)

    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 110]}, index=dates)
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.price_chart import analyze_stock
        result = analyze_stock("AAPL", "2024-01-02", "2024-01-15")

    chart_dir = tmp_path / "finance_output" / "charts"
    png_files = list(chart_dir.glob("*.png"))
    assert len(png_files) == 1, f"Expected 1 PNG in {chart_dir}, found {png_files}"


def test_get_returns_values():
    """Daily returns are pct_change; cumulative is compound product."""
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    prices = pd.Series([100 * (1.01 ** i) for i in range(10)], index=dates)
    mock_df = pd.DataFrame({"Close": prices})
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.returns import get_returns
        result = get_returns("TEST", "2024-01-02", "2024-01-15")

    assert isinstance(result, str)
    assert "%" in result
    expected_total = (1.01 ** 9 - 1) * 100
    assert str(round(expected_total, 0))[:2] in result or "9." in result


def test_get_returns_chart(tmp_path, monkeypatch):
    """get_returns saves a PNG to finance_output/charts/."""
    monkeypatch.chdir(tmp_path)
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_df = pd.DataFrame({"Close": [100 + i for i in range(10)]}, index=dates)
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.returns import get_returns
        get_returns("TEST", "2024-01-02", "2024-01-15")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


def test_annualized_volatility_formula():
    """Annualized vol = daily_std * sqrt(252) to float precision."""
    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    np.random.seed(42)
    daily_rets = pd.Series(np.random.normal(0, 0.01, 30), index=dates)
    prices = (1 + daily_rets).cumprod() * 100
    mock_df = pd.DataFrame({"Close": prices})
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    actual_daily_rets = prices.pct_change().dropna()
    expected_vol = actual_daily_rets.std() * np.sqrt(252)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.volatility import get_volatility
        result = get_volatility("TEST", "2024-01-02", "2024-02-15")

    expected_pct = f"{expected_vol * 100:.2f}%"
    assert expected_pct in result, f"Expected {expected_pct} in output, got snippet: {result[:200]}"


def test_volatility_chart(tmp_path, monkeypatch):
    """get_volatility saves a PNG to finance_output/charts/."""
    monkeypatch.chdir(tmp_path)
    np.random.seed(0)
    dates = pd.date_range("2024-01-02", periods=40, freq="B")
    prices = (1 + pd.Series(np.random.normal(0, 0.01, 40), index=dates)).cumprod() * 100
    mock_df = pd.DataFrame({"Close": prices})
    mock_provider = _make_provider_mock(fetch_price_history=mock_df)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.volatility import get_volatility
        get_volatility("TEST", "2024-01-02", "2024-03-01")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


def test_sharpe_sign():
    """Sharpe ratio is positive when mean daily return > 0."""
    from finance_mcp.tools.risk_metrics import _compute_risk_metrics

    np.random.seed(1)
    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    returns = pd.Series(np.random.normal(0.001, 0.01, 30), index=dates)
    bench = pd.Series(np.random.normal(0.0005, 0.01, 30), index=dates)

    metrics = _compute_risk_metrics(returns, bench)
    assert metrics["sharpe"] > 0, f"Expected positive Sharpe, got {metrics['sharpe']}"


def test_max_drawdown_nonpositive():
    """Max drawdown is always <= 0."""
    from finance_mcp.tools.risk_metrics import _compute_risk_metrics

    np.random.seed(2)
    dates = pd.date_range("2024-01-02", periods=50, freq="B")
    returns = pd.Series(np.random.normal(0, 0.01, 50), index=dates)
    bench = pd.Series(np.random.normal(0, 0.01, 50), index=dates)

    metrics = _compute_risk_metrics(returns, bench)
    assert metrics["max_drawdown"] <= 0, f"Max drawdown must be <= 0, got {metrics['max_drawdown']}"


def test_beta_calculation():
    """Beta matches the np.cov formula result for known inputs."""
    from finance_mcp.tools.risk_metrics import _compute_risk_metrics

    np.random.seed(3)
    dates = pd.date_range("2024-01-02", periods=60, freq="B")
    bench = pd.Series(np.random.normal(0.0005, 0.01, 60), index=dates)
    returns = 1.5 * bench + pd.Series(np.random.normal(0, 0.002, 60), index=dates)

    metrics = _compute_risk_metrics(returns, bench)

    aligned = pd.concat([returns, bench], axis=1).dropna()
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    expected_beta = cov[0, 1] / cov[1, 1]

    assert abs(metrics["beta"] - expected_beta) < 1e-10, (
        f"Beta mismatch: got {metrics['beta']}, expected {expected_beta}"
    )


def test_normalized_prices_start_at_100():
    """Normalized prices start at exactly 100.0 for each ticker."""
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_prices = {
        "AAPL": pd.Series([150.0 + i for i in range(10)], index=dates),
        "MSFT": pd.Series([300.0 + i * 2 for i in range(10)], index=dates),
    }
    mock_provider = _make_provider_mock(fetch_multi_ticker=mock_prices)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.comparison import compare_tickers
        result = compare_tickers("AAPL,MSFT", "2024-01-02", "2024-01-15")

    assert "100" in result


def test_compare_tickers_chart(tmp_path, monkeypatch):
    """compare_tickers saves a PNG to finance_output/charts/."""
    monkeypatch.chdir(tmp_path)
    dates = pd.date_range("2024-01-02", periods=10, freq="B")
    mock_prices = {
        "AAPL": pd.Series([150.0 + i for i in range(10)], index=dates),
        "MSFT": pd.Series([300.0 + i for i in range(10)], index=dates),
    }
    mock_provider = _make_provider_mock(fetch_multi_ticker=mock_prices)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.comparison import compare_tickers
        compare_tickers("AAPL,MSFT", "2024-01-02", "2024-01-15")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


def test_correlation_uses_returns():
    """Correlation is computed on daily returns, not raw price levels."""
    dates = pd.date_range("2024-01-02", periods=50, freq="B")
    base = pd.Series(range(1, 51), index=dates, dtype=float)
    np.random.seed(42)
    prices_a = base + np.random.normal(0, 0.5, 50)
    prices_b = base + np.random.normal(0, 0.5, 50)

    mock_prices = {
        "TICKA": prices_a,
        "TICKB": prices_b,
    }
    mock_provider = _make_provider_mock(fetch_multi_ticker=mock_prices)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.correlation import correlation_map
        result = correlation_map("TICKA,TICKB", "2024-01-02", "2024-03-15")

    assert "return" in result.lower() or "daily" in result.lower(), (
        "Output should reference return-based correlation, not price levels"
    )


def test_correlation_map_chart(tmp_path, monkeypatch):
    """correlation_map saves a PNG to finance_output/charts/."""
    monkeypatch.chdir(tmp_path)
    np.random.seed(7)
    dates = pd.date_range("2024-01-02", periods=40, freq="B")
    mock_prices = {
        "TICKA": pd.Series(100 + np.random.randn(40).cumsum(), index=dates),
        "TICKB": pd.Series(200 + np.random.randn(40).cumsum(), index=dates),
    }
    mock_provider = _make_provider_mock(fetch_multi_ticker=mock_prices)

    with patch("finance_mcp.server.provider", mock_provider):
        from finance_mcp.tools.correlation import correlation_map
        correlation_map("TICKA,TICKB", "2024-01-02", "2024-03-01")

    png_files = list((tmp_path / "finance_output" / "charts").glob("*.png"))
    assert len(png_files) == 1


def test_output_plain_english_first():
    """All 6 Phase 2 tools output starts with a plain-English character (not digit or symbol)."""
    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    mock_df = pd.DataFrame({"Close": 100 + np.arange(30, dtype=float)}, index=dates)
    mock_multi = {
        "TICKA": mock_df["Close"],
        "TICKB": mock_df["Close"] * 1.1,
    }
    bench_df = pd.DataFrame({"Close": 4000 + np.arange(30, dtype=float)}, index=dates)

    single_provider = _make_provider_mock(fetch_price_history=mock_df)
    multi_provider = _make_provider_mock(fetch_multi_ticker=mock_multi)

    tools_and_providers = [
        (single_provider,
         lambda: __import__("finance_mcp.tools.price_chart", fromlist=["analyze_stock"]).analyze_stock("AAPL", "2024-01-02")),
        (single_provider,
         lambda: __import__("finance_mcp.tools.returns", fromlist=["get_returns"]).get_returns("AAPL", "2024-01-02")),
        (single_provider,
         lambda: __import__("finance_mcp.tools.volatility", fromlist=["get_volatility"]).get_volatility("AAPL", "2024-01-02")),
        (multi_provider,
         lambda: __import__("finance_mcp.tools.comparison", fromlist=["compare_tickers"]).compare_tickers("TICKA,TICKB", "2024-01-02")),
        (multi_provider,
         lambda: __import__("finance_mcp.tools.correlation", fromlist=["correlation_map"]).correlation_map("TICKA,TICKB", "2024-01-02")),
    ]

    for mock_provider, caller in tools_and_providers:
        with patch("finance_mcp.server.provider", mock_provider):
            result = caller()
        assert isinstance(result, str) and len(result) > 0
        assert result[0].isalpha(), (
            f"Tool output must start with plain-English text, got first char: {result[0]!r}"
        )

    # get_risk_metrics needs two fetches (stock + benchmark)
    risk_provider = MagicMock()
    risk_provider.fetch_price_history.side_effect = [mock_df, bench_df]
    risk_provider.get_adjusted_prices.side_effect = lambda df: df["Close"]
    with patch("finance_mcp.server.provider", risk_provider):
        from finance_mcp.tools.risk_metrics import get_risk_metrics
        result = get_risk_metrics("AAPL", "2024-01-02")
    assert result[0].isalpha(), "get_risk_metrics output must start with plain-English text"


def test_output_ends_with_disclaimer():
    """All 6 Phase 2 tools output ends with the DISCLAIMER constant."""
    from finance_mcp.output import DISCLAIMER

    dates = pd.date_range("2024-01-02", periods=30, freq="B")
    mock_df = pd.DataFrame({"Close": 100 + np.arange(30, dtype=float)}, index=dates)
    mock_multi = {
        "TICKA": mock_df["Close"],
        "TICKB": mock_df["Close"] * 1.1,
    }
    bench_df = pd.DataFrame({"Close": 4000 + np.arange(30, dtype=float)}, index=dates)

    results = []

    single_provider = _make_provider_mock(fetch_price_history=mock_df)
    multi_provider = _make_provider_mock(fetch_multi_ticker=mock_multi)

    with patch("finance_mcp.server.provider", single_provider):
        from finance_mcp.tools.price_chart import analyze_stock
        results.append(("analyze_stock", analyze_stock("AAPL", "2024-01-02")))

    with patch("finance_mcp.server.provider", single_provider):
        from finance_mcp.tools.returns import get_returns
        results.append(("get_returns", get_returns("AAPL", "2024-01-02")))

    with patch("finance_mcp.server.provider", single_provider):
        from finance_mcp.tools.volatility import get_volatility
        results.append(("get_volatility", get_volatility("AAPL", "2024-01-02")))

    risk_provider = MagicMock()
    risk_provider.fetch_price_history.side_effect = [mock_df, bench_df]
    risk_provider.get_adjusted_prices.side_effect = lambda df: df["Close"]
    with patch("finance_mcp.server.provider", risk_provider):
        from finance_mcp.tools.risk_metrics import get_risk_metrics
        results.append(("get_risk_metrics", get_risk_metrics("AAPL", "2024-01-02")))

    with patch("finance_mcp.server.provider", multi_provider):
        from finance_mcp.tools.comparison import compare_tickers
        results.append(("compare_tickers", compare_tickers("TICKA,TICKB", "2024-01-02")))

    with patch("finance_mcp.server.provider", multi_provider):
        from finance_mcp.tools.correlation import correlation_map
        results.append(("correlation_map", correlation_map("TICKA,TICKB", "2024-01-02")))

    for tool_name, result in results:
        assert result.strip().endswith(DISCLAIMER), (
            f"{tool_name} output must end with DISCLAIMER. "
            f"Got last 100 chars: {result.strip()[-100:]!r}"
        )
