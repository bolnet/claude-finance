"""
Schema validation tests for demo/sample_portfolio.csv.

Verifies the sample CSV satisfies the column schemas required by:
  - liquidity_model.py (credit_score, debt_ratio, region, liquidity_risk)
  - investor_model.py (age, income, risk_tolerance, product_preference, segment)
  - csv_ingest.py (any CSV with numeric/categorical columns)
"""
import os
import pandas as pd
import pytest


CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "demo", "sample_portfolio.csv")
REQUIRED_COLUMNS = [
    "credit_score",
    "debt_ratio",
    "region",
    "liquidity_risk",
    "age",
    "income",
    "risk_tolerance",
    "product_preference",
    "segment",
]
VALID_REGIONS = {"Northeast", "South", "Midwest", "West"}
VALID_PRODUCT_PREFERENCES = {"stocks", "bonds", "mixed", "equities"}
VALID_SEGMENTS = {"conservative", "moderate", "aggressive"}


@pytest.fixture(scope="module")
def df():
    """Load the sample CSV once for the test module."""
    return pd.read_csv(CSV_PATH)


def test_csv_exists_and_loads():
    """Test 1: demo/sample_portfolio.csv exists and loads via pd.read_csv without error."""
    assert os.path.exists(CSV_PATH), f"CSV not found at {CSV_PATH}"
    df = pd.read_csv(CSV_PATH)
    assert isinstance(df, pd.DataFrame)


def test_csv_has_required_columns(df):
    """Test 2: CSV has exactly the required 9 columns."""
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    assert not missing, f"Missing columns: {missing}"


def test_csv_has_minimum_rows(df):
    """Test 3: CSV has at least 50 rows (enough for 80/20 train/test split)."""
    assert len(df) >= 50, f"CSV has only {len(df)} rows — need at least 50"


def test_credit_score_range(df):
    """Test 4: credit_score values are numeric between 300-850."""
    assert pd.api.types.is_numeric_dtype(df["credit_score"]), "credit_score is not numeric"
    assert df["credit_score"].between(300, 850).all(), (
        f"credit_score out of range [300, 850]: "
        f"min={df['credit_score'].min()}, max={df['credit_score'].max()}"
    )


def test_debt_ratio_range(df):
    """Test 5: debt_ratio values are numeric between 0.0-1.0."""
    assert pd.api.types.is_numeric_dtype(df["debt_ratio"]), "debt_ratio is not numeric"
    assert df["debt_ratio"].between(0.0, 1.0).all(), (
        f"debt_ratio out of range [0.0, 1.0]: "
        f"min={df['debt_ratio'].min()}, max={df['debt_ratio'].max()}"
    )


def test_region_valid_values(df):
    """Test 6: region values are strings from the valid set."""
    invalid = set(df["region"].unique()) - VALID_REGIONS
    assert not invalid, f"Invalid region values: {invalid}"


def test_liquidity_risk_range(df):
    """Test 7: liquidity_risk values are numeric between 0.0-1.0."""
    assert pd.api.types.is_numeric_dtype(df["liquidity_risk"]), "liquidity_risk is not numeric"
    assert df["liquidity_risk"].between(0.0, 1.0).all(), (
        f"liquidity_risk out of range [0.0, 1.0]: "
        f"min={df['liquidity_risk'].min()}, max={df['liquidity_risk'].max()}"
    )


def test_age_range(df):
    """Test 8: age values are numeric between 18-80."""
    assert pd.api.types.is_numeric_dtype(df["age"]), "age is not numeric"
    assert df["age"].between(18, 80).all(), (
        f"age out of range [18, 80]: "
        f"min={df['age'].min()}, max={df['age'].max()}"
    )


def test_income_range(df):
    """Test 9: income values are numeric between 20000-500000."""
    assert pd.api.types.is_numeric_dtype(df["income"]), "income is not numeric"
    assert df["income"].between(20000, 500000).all(), (
        f"income out of range [20000, 500000]: "
        f"min={df['income'].min()}, max={df['income'].max()}"
    )


def test_risk_tolerance_range(df):
    """Test 10: risk_tolerance values are numeric between 0.0-1.0."""
    assert pd.api.types.is_numeric_dtype(df["risk_tolerance"]), "risk_tolerance is not numeric"
    assert df["risk_tolerance"].between(0.0, 1.0).all(), (
        f"risk_tolerance out of range [0.0, 1.0]: "
        f"min={df['risk_tolerance'].min()}, max={df['risk_tolerance'].max()}"
    )


def test_product_preference_valid_values(df):
    """Test 11: product_preference values are strings from the valid set."""
    invalid = set(df["product_preference"].unique()) - VALID_PRODUCT_PREFERENCES
    assert not invalid, f"Invalid product_preference values: {invalid}"


def test_segment_valid_values(df):
    """Test 12: segment values are strings from the valid set."""
    invalid = set(df["segment"].unique()) - VALID_SEGMENTS
    assert not invalid, f"Invalid segment values: {invalid}"


def test_segment_class_balance(df):
    """Test 13: Each segment has at least 10 rows (enough for stratified split)."""
    counts = df["segment"].value_counts()
    for segment in VALID_SEGMENTS:
        count = counts.get(segment, 0)
        assert count >= 10, f"Segment '{segment}' has only {count} rows — need at least 10"
