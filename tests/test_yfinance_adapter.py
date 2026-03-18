"""
Tests for yfinance adapter layer.
Requirements: INFRA-03, INFRA-06

Wave 0: stubs only. Implementations land in plan 01-02 (adapter.py).
Full test commands:
  python3 -m pytest tests/test_yfinance_adapter.py -v
"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.mark.xfail(reason="adapter.py not yet implemented — lands in plan 01-02", strict=False)
def test_fetch_price_history_returns_dataframe(sample_price_df):
    """INFRA-03: fetch_price_history returns a DataFrame with Close column."""
    from finance_mcp.adapter import fetch_price_history
    with patch("finance_mcp.adapter.yf.download", return_value=sample_price_df):
        df = fetch_price_history("AAPL", start="2023-01-01")
    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns


@pytest.mark.xfail(reason="adapter.py not yet implemented — lands in plan 01-02", strict=False)
def test_fetch_price_history_raises_on_empty_df(empty_df):
    """INFRA-06: DataFetchError raised when yfinance returns empty DataFrame."""
    from finance_mcp.adapter import fetch_price_history, DataFetchError
    with patch("finance_mcp.adapter.yf.download", return_value=empty_df):
        with pytest.raises(DataFetchError):
            fetch_price_history("INVALID_TICKER_XYZ", start="2023-01-01")


@pytest.mark.xfail(reason="adapter.py not yet implemented — lands in plan 01-02", strict=False)
def test_no_direct_yfinance_imports_outside_adapter():
    """INFRA-03: Only adapter.py may import yfinance directly."""
    import ast
    import pathlib
    src_dir = pathlib.Path(__file__).parent.parent / "src" / "finance_mcp"
    violations = []
    for py_file in src_dir.glob("*.py"):
        if py_file.name == "adapter.py":
            continue
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in getattr(node, "names", [])]
                module = getattr(node, "module", "") or ""
                if "yfinance" in names or module.startswith("yfinance"):
                    violations.append(f"{py_file.name}: direct yfinance import")
    assert violations == [], f"Direct yfinance imports outside adapter.py: {violations}"


@pytest.mark.xfail(reason="adapter.py not yet implemented — lands in plan 01-02", strict=False)
def test_get_adjusted_prices_returns_series(sample_price_df):
    """INFRA-03: get_adjusted_prices returns the Close series (adjusted price)."""
    from finance_mcp.adapter import get_adjusted_prices
    result = get_adjusted_prices(sample_price_df)
    import pandas as pd
    assert isinstance(result, pd.Series)
    assert result.name == "Close"
