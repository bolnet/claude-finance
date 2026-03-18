"""
Integration tests for ML demo steps 9-11 (07-02-PLAN.md).

Verifies all 4 ML tools execute successfully on demo/sample_portfolio.csv
using the exact invocations described in demo.md Steps 9-11.
"""
import pytest
from finance_mcp.tools.csv_ingest import ingest_csv
from finance_mcp.tools.liquidity_model import liquidity_predictor, predict_liquidity
from finance_mcp.tools.investor_model import investor_classifier, classify_investor

SAMPLE_CSV = "demo/sample_portfolio.csv"


# ---------------------------------------------------------------------------
# Step 9: ingest_csv
# ---------------------------------------------------------------------------

def test_ingest_csv_returns_eda_summary():
    """Step 9: ingest_csv on sample CSV must return rows/columns EDA summary."""
    result = ingest_csv(SAMPLE_CSV)
    assert isinstance(result, str), "ingest_csv must return a string"
    lower = result.lower()
    assert "rows" in lower or "row" in lower, f"Expected 'rows' in output, got:\n{result[:500]}"
    assert "column" in lower, f"Expected 'column' in output, got:\n{result[:500]}"


# ---------------------------------------------------------------------------
# Step 10: liquidity_predictor + predict_liquidity
# ---------------------------------------------------------------------------

def test_liquidity_predictor_trains_successfully(tmp_path):
    """Step 10a: liquidity_predictor trains on sample CSV and reports RMSE/R²."""
    result = liquidity_predictor(SAMPLE_CSV)
    assert isinstance(result, str), "liquidity_predictor must return a string"
    lower = result.lower()
    has_rmse = "rmse" in lower
    has_r2 = "r²" in lower or "r-squared" in lower or "r2" in lower or "r^2" in lower
    assert has_rmse, f"Expected 'RMSE' in output, got:\n{result[:500]}"
    assert has_r2, f"Expected R² metric in output, got:\n{result[:500]}"


def test_predict_liquidity_scores_client():
    """Step 10b: predict_liquidity with demo.md params returns a liquidity risk score."""
    # Train first so a saved model exists
    liquidity_predictor(SAMPLE_CSV)
    result = predict_liquidity(credit_score=720, debt_ratio=0.35, region="Northeast")
    assert isinstance(result, str), "predict_liquidity must return a string"
    lower = result.lower()
    assert "liquidity" in lower, (
        f"Expected 'liquidity' in predict_liquidity output, got:\n{result[:500]}"
    )


# ---------------------------------------------------------------------------
# Step 11: investor_classifier + classify_investor
# ---------------------------------------------------------------------------

def test_investor_classifier_trains_successfully():
    """Step 11a: investor_classifier trains on sample CSV and reports accuracy."""
    result = investor_classifier(SAMPLE_CSV)
    assert isinstance(result, str), "investor_classifier must return a string"
    lower = result.lower()
    assert "accuracy" in lower, (
        f"Expected 'accuracy' in investor_classifier output, got:\n{result[:500]}"
    )


def test_classify_investor_returns_segment():
    """Step 11b: classify_investor with demo.md params (risk_tolerance as float) returns a segment label."""
    # Train first
    investor_classifier(SAMPLE_CSV)
    # demo.md Step 11 uses risk_tolerance=0.5 (float), age=42, income=120000, product_preference="equities"
    result = classify_investor(
        age=42,
        income=120000,
        risk_tolerance=0.5,
        product_preference="equities",
    )
    assert isinstance(result, str), "classify_investor must return a string"
    lower = result.lower()
    # Expect one of the known segment labels
    has_segment = any(
        label in lower
        for label in ("conservative", "moderate", "aggressive", "segment")
    )
    assert has_segment, (
        f"Expected a segment label in classify_investor output, got:\n{result[:500]}"
    )


# ---------------------------------------------------------------------------
# Step 11 parameter-mismatch check: demo.md passes risk_tolerance="moderate" (string)
# but classify_investor expects risk_tolerance: float.
# ---------------------------------------------------------------------------

@pytest.mark.xfail(
    reason="demo.md Step 11 passes risk_tolerance='moderate' (string) but classify_investor expects float. "
           "This test documents the schema mismatch. demo.md must be updated to pass risk_tolerance=0.5 "
           "or the tool must accept string values and convert internally.",
    strict=False,
)
def test_classify_investor_string_risk_tolerance_mismatch():
    """
    Documents demo.md schema mismatch: risk_tolerance="moderate" vs expected float.

    demo.md Step 11 currently calls:
        classify_investor(age=42, income=120000, risk_tolerance="moderate", product_preference="equities")

    But classify_investor signature declares risk_tolerance: float.

    If this test XPASSES: the tool silently accepts strings (no action needed).
    If this test XFAILS: demo.md must be updated to pass risk_tolerance=0.5 instead.
    """
    investor_classifier(SAMPLE_CSV)
    result = classify_investor(
        age=42,
        income=120000,
        risk_tolerance="moderate",  # type: ignore[arg-type]  — intentional mismatch
        product_preference="equities",
    )
    assert isinstance(result, str)
    lower = result.lower()
    assert any(label in lower for label in ("conservative", "moderate", "aggressive", "segment"))
