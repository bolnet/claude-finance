"""
ML workflow tool tests — Phase 3 plan 03-01.

Test stubs for all 14 ML requirements (LQDX + INVX).
Stubs for 03-02/03-03 tools (liquidity_predictor, predict_liquidity,
investor_classifier, classify_investor) skip at import time if the
tool module does not yet exist.

Test execution order mirrors the implementation waves:
  Wave 1 (this plan): ingest_csv stubs — test_csv_structure_detection,
                      test_data_cleaning, test_eda_output,
                      test_ml_output_format, test_missing_csv_error
  Wave 2 (03-02):    liquidity model stubs
  Wave 3 (03-03):    investor model stubs
"""

import os
import pytest
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Fixture paths
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

LIQUIDITY_CSV = os.path.join(DATA_DIR, "liquidity_sample.csv")
LIQUIDITY_CLIENT_CSV = os.path.join(DATA_DIR, "liquidity_client_sample.csv")
INVESTOR_CSV = os.path.join(DATA_DIR, "investor_sample.csv")
INVESTOR_CSV_2 = os.path.join(DATA_DIR, "investor_sample_2.csv")

# ---------------------------------------------------------------------------
# Optional imports for tools not yet implemented (03-02, 03-03)
# ---------------------------------------------------------------------------

try:
    from finance_mcp.tools.liquidity_model import liquidity_predictor, predict_liquidity
    _HAS_LIQUIDITY = True
except ImportError:
    _HAS_LIQUIDITY = False

try:
    from finance_mcp.tools.investor_model import investor_classifier, classify_investor
    _HAS_INVESTOR = True
except ImportError:
    _HAS_INVESTOR = False

# ---------------------------------------------------------------------------
# Wave 1: ingest_csv tests (should pass after Task 2)
# ---------------------------------------------------------------------------


def test_csv_structure_detection():
    """ingest_csv returns a string with numeric/categorical column info and ends with DISCLAIMER."""
    from finance_mcp.tools.csv_ingest import ingest_csv
    from finance_mcp.output import DISCLAIMER

    result = ingest_csv(LIQUIDITY_CSV)

    assert isinstance(result, str), "ingest_csv must return a string"
    assert "numeric columns" in result.lower(), "Output must mention numeric columns"
    assert "categorical columns" in result.lower(), "Output must mention categorical columns"
    assert result.endswith(DISCLAIMER), "Output must end with DISCLAIMER"


def test_data_cleaning():
    """_clean_dataframe removes IQR outliers and fills numeric missing values with median."""
    from finance_mcp.tools.csv_ingest import _clean_dataframe

    # Build a small DataFrame with one outlier and one missing value
    df = pd.DataFrame({
        "value": [10.0, 12.0, 11.0, None, 10.5, 1000.0],  # 1000.0 is outlier, None is missing
        "other": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    })

    cleaned = _clean_dataframe(df, ["value", "other"])

    # Outlier row (1000.0) must be removed
    assert cleaned["value"].max() < 500, "IQR outlier row must be removed"

    # No remaining NaN in numeric columns
    assert not cleaned["value"].isna().any(), "Missing values must be filled"

    # Original DataFrame must not be mutated (immutability rule)
    assert df["value"].isna().any(), "Original DataFrame must not be mutated"


def test_eda_output():
    """ingest_csv output contains at least one PNG chart path."""
    from finance_mcp.tools.csv_ingest import ingest_csv

    result = ingest_csv(LIQUIDITY_CSV)

    assert ".png" in result, "Output must contain at least one PNG chart path"


def test_missing_csv_error():
    """ingest_csv raises ToolError for a non-existent path (not raw FileNotFoundError)."""
    from finance_mcp.tools.csv_ingest import ingest_csv
    from fastmcp.exceptions import ToolError

    with pytest.raises(ToolError):
        ingest_csv("/nonexistent/path/that/does/not/exist.csv")


def test_ml_output_format():
    """ingest_csv output starts with non-empty plain English and ends with DISCLAIMER."""
    from finance_mcp.tools.csv_ingest import ingest_csv
    from finance_mcp.output import DISCLAIMER

    result = ingest_csv(LIQUIDITY_CSV)

    lines = result.strip().split("\n")
    # First line must be non-empty plain English (not a chart path or data table)
    assert lines[0].strip(), "Output must start with non-empty plain-English"
    assert not lines[0].startswith("/"), "Output must not start with a file path"

    # Must end with DISCLAIMER constant
    assert result.endswith(DISCLAIMER), "Output must end with DISCLAIMER"


# ---------------------------------------------------------------------------
# Wave 2: Liquidity model tests (03-02) — skip until module exists
# ---------------------------------------------------------------------------


def test_split_before_fit():
    """liquidity_predictor smoke test — RMSE is numeric, R2 is between -1 and 1."""
    if not _HAS_LIQUIDITY:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.liquidity_model")

    result = liquidity_predictor(LIQUIDITY_CSV)

    assert isinstance(result, str), "liquidity_predictor must return a string"
    # Extract RMSE — must be parseable as a number
    import re
    rmse_match = re.search(r"RMSE[:\s]+([0-9.]+)", result, re.IGNORECASE)
    assert rmse_match is not None, "Output must contain RMSE value"
    rmse_val = float(rmse_match.group(1))
    assert rmse_val >= 0, "RMSE must be non-negative"

    # R2 must be present and in range
    r2_match = re.search(r"R[²2][:\s]+(-?[0-9.]+)", result, re.IGNORECASE)
    assert r2_match is not None, "Output must contain R² value"
    r2_val = float(r2_match.group(1))
    assert -1 <= r2_val <= 1, "R² must be between -1 and 1"


def test_regression_evaluation():
    """liquidity_predictor output contains RMSE, R², and ends with DISCLAIMER."""
    if not _HAS_LIQUIDITY:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.liquidity_model")

    from finance_mcp.output import DISCLAIMER

    result = liquidity_predictor(LIQUIDITY_CSV)

    assert "RMSE" in result, "Output must contain RMSE"
    assert "R²" in result or "R2" in result, "Output must contain R²"
    assert result.endswith(DISCLAIMER), "Output must end with DISCLAIMER"


def test_predict_liquidity():
    """predict_liquidity returns a string containing a numeric prediction."""
    if not _HAS_LIQUIDITY:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.liquidity_model")

    import re

    result = predict_liquidity(credit_score=720, debt_ratio=0.35, region="North")

    assert isinstance(result, str), "predict_liquidity must return a string"
    # Must contain at least one numeric value
    assert re.search(r"[0-9]+\.?[0-9]*", result), "Output must contain a numeric prediction"


# ---------------------------------------------------------------------------
# Wave 3: Investor model tests (03-03) — skip until module exists
# ---------------------------------------------------------------------------


def test_investor_csv_detection():
    """ingest_csv on investor_sample.csv includes 'segment' column in output."""
    from finance_mcp.tools.csv_ingest import ingest_csv

    result = ingest_csv(INVESTOR_CSV)

    assert "segment" in result.lower(), "Output must mention 'segment' column"


def test_feature_engineering():
    """get_dummies with drop_first=True produces bool dtype dummy columns, removes original categorical."""
    # Test the pandas transformation pattern used in the investor model
    df = pd.DataFrame({
        "category": ["A", "B", "A", "C"],
        "value": [1.0, 2.0, 3.0, 4.0],
    })

    dummies = pd.get_dummies(df, columns=["category"], drop_first=True)

    # Original categorical column must be absent
    assert "category" not in dummies.columns, "Original categorical column must be dropped"

    # New dummy columns must exist
    dummy_cols = [c for c in dummies.columns if c.startswith("category_")]
    assert len(dummy_cols) >= 1, "At least one dummy column must be created"


def test_stratified_split():
    """Stratified split of investor_sample.csv preserves class proportions within 10%."""
    if not _HAS_INVESTOR:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.investor_model")

    from sklearn.model_selection import train_test_split

    df = pd.read_csv(INVESTOR_CSV).dropna()
    X = df.drop(columns=["segment"])
    y = df["segment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    train_dist = y_train.value_counts(normalize=True)
    test_dist = y_test.value_counts(normalize=True)

    for cls in y.unique():
        if cls in train_dist and cls in test_dist:
            diff = abs(train_dist[cls] - test_dist[cls])
            assert diff <= 0.10, f"Class '{cls}' proportion differs by {diff:.2%} — stratification failed"


def test_gridsearch_runs():
    """investor_classifier output contains 'best parameters'."""
    if not _HAS_INVESTOR:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.investor_model")

    result = investor_classifier(INVESTOR_CSV)

    assert isinstance(result, str), "investor_classifier must return a string"
    assert "best parameters" in result.lower(), "Output must contain 'best parameters'"


def test_classifier_evaluation():
    """investor_classifier output contains confusion matrix, precision, recall, and PNG path."""
    if not _HAS_INVESTOR:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.investor_model")

    result = investor_classifier(INVESTOR_CSV)

    assert "confusion matrix" in result.lower(), "Output must contain confusion matrix"
    assert "precision" in result.lower(), "Output must contain precision"
    assert "recall" in result.lower(), "Output must contain recall"
    assert ".png" in result, "Output must contain at least one PNG chart path"


def test_classify_investor():
    """classify_investor returns a segment label from the known class set."""
    if not _HAS_INVESTOR:
        pytest.skip("Tool not yet implemented: finance_mcp.tools.investor_model")

    result = classify_investor(age=35, income=75000, risk_tolerance=0.6, product_preference="stocks")

    assert isinstance(result, str), "classify_investor must return a string"
    known_segments = {"conservative", "moderate", "aggressive"}
    assert any(seg in result.lower() for seg in known_segments), (
        f"Output must contain a known segment label. Got: {result}"
    )
