"""
Liquidity risk ML tools — regression pipeline with split-before-fit enforcement.

Provides two MCP tools:
  - liquidity_predictor: trains and evaluates a linear regression pipeline on a CSV
  - predict_liquidity: loads the persisted model and predicts for a single client

Import order is CRITICAL: finance_mcp.output must be imported first to ensure
the matplotlib Agg backend is set before pyplot loads.
"""
from finance_mcp.output import format_output, save_chart, ensure_output_dirs, DISCLAIMER
from finance_mcp.tools.csv_ingest import _detect_structure, _clean_dataframe

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
from fastmcp.exceptions import ToolError

MODEL_DIR = os.path.join("finance_output", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "liquidity_pipeline.joblib")


def liquidity_predictor(csv_path: str, target_column: str = "liquidity_risk") -> str:
    """
    Train and evaluate a liquidity risk regression model from a CSV file.

    Performs IQR cleaning, builds a linear regression pipeline (split before fit),
    evaluates with RMSE and R², saves a residual plot, and persists the model.

    Args:
        csv_path: Absolute or relative path to the liquidity CSV file.
        target_column: Column name to predict. Defaults to 'liquidity_risk'.
                       If not found, auto-detects: last numeric column or column
                       containing 'risk'/'score'.

    Returns:
        Plain-English evaluation summary with RMSE, R², residual plot path,
        and the standard investment disclaimer.

    Raises:
        ToolError: If the CSV file does not exist or no suitable target column found.
    """
    # Step 1: Validate path
    if not os.path.exists(csv_path):
        raise ToolError(
            f"The file '{csv_path}' was not found. Check the path and try again."
        )

    # Step 2: Load CSV
    df = pd.read_csv(csv_path)

    # Step 3: Auto-detect target_column if not present
    if target_column not in df.columns:
        # Try columns containing 'risk' or 'score'
        risk_cols = [c for c in df.columns if "risk" in c.lower() or "score" in c.lower()]
        if risk_cols:
            target_column = risk_cols[0]
        else:
            # Fall back to last numeric column
            numeric_cols_all = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols_all:
                target_column = numeric_cols_all[-1]
            else:
                raise ToolError(
                    f"Could not find target column '{target_column}' and no numeric "
                    f"columns available for auto-detection."
                )

    # Step 4: Detect structure
    structure = _detect_structure(df)

    # Step 5: Clean dataframe
    df_clean = _clean_dataframe(df, structure["numeric_cols"])

    # Step 6: Build feature/target arrays
    X = df_clean.drop(columns=[target_column])
    y = df_clean[target_column]

    # Step 7: Identify numeric and categorical feature columns (excluding target)
    num_features = [
        c for c in structure["numeric_cols"]
        if c != target_column and c in X.columns
    ]
    cat_features = structure["cat_cols"]

    # Step 8: MANDATORY SPLIT BEFORE FIT — train_test_split MUST come before pipe.fit()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Step 9: Build preprocessor
    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features),
        ],
        remainder="drop",
    )

    # Step 10: Build pipeline
    pipe = Pipeline([("preprocessor", preprocessor), ("regressor", LinearRegression())])

    # Step 11: Fit on train set ONLY
    pipe.fit(X_train, y_train)

    # Step 12: Predict on test set
    y_pred = pipe.predict(X_test)

    # Step 13: Compute RMSE
    rmse = root_mean_squared_error(y_test, y_pred)

    # Step 14: Compute R²
    r2 = r2_score(y_test, y_pred)

    # Step 15: Baseline RMSE (mean-prediction baseline)
    baseline_rmse = root_mean_squared_error(
        y_test, np.full_like(y_test, y_train.mean(), dtype=float)
    )

    # Step 16: Residual plot
    residuals = y_test - y_pred
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].scatter(y_pred, residuals, alpha=0.6, edgecolors="black", linewidths=0.5)
    axes[0].axhline(0, color="red", linestyle="--", linewidth=1)
    axes[0].set_title("Residuals vs Predicted")
    axes[0].set_xlabel("Predicted Values")
    axes[0].set_ylabel("Residuals")

    axes[1].hist(residuals, bins=20, edgecolor="black")
    axes[1].axvline(0, color="red", linestyle="--", linewidth=1)
    axes[1].set_title("Residuals Distribution")
    axes[1].set_xlabel("Residual Value")
    axes[1].set_ylabel("Frequency")

    fig.suptitle(f"Residual Analysis — {target_column} Prediction", fontsize=13)
    plt.tight_layout()
    residual_chart_path = save_chart(fig, "residual_plot.png")

    # Step 17: Persist model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)

    # Step 18: Plain-English interpretation
    if baseline_rmse > 0:
        improvement = (1 - rmse / baseline_rmse) * 100
    else:
        improvement = 0.0

    fit_quality = ""
    if r2 < 0.3:
        fit_quality = "This is a weak fit — consider adding more features or reviewing data quality."
    elif r2 >= 0.7:
        fit_quality = "This is a strong fit for a linear model."
    else:
        fit_quality = "This is a moderate fit."

    plain_english = (
        f"Liquidity risk regression model trained on {len(X_train)} samples "
        f"and evaluated on {len(X_test)} held-out samples.\n\n"
        f"The model achieved an RMSE of {rmse:.4f} — compared to a baseline "
        f"(always predict mean) RMSE of {baseline_rmse:.4f}, the model explains "
        f"{improvement:.1f}% of the baseline error.\n\n"
        f"R² score of {r2:.4f} means the model accounts for {r2 * 100:.1f}% of "
        f"the variance in {target_column}. {fit_quality}\n\n"
        f"Model saved to: {os.path.abspath(MODEL_PATH)}"
    )

    # Step 19: Data section table
    data_section = (
        f"{'Metric':<25} {'Value':<15}\n"
        f"{'-' * 40}\n"
        f"{'RMSE':<25} {rmse:.6f}\n"
        f"{'Baseline RMSE':<25} {baseline_rmse:.6f}\n"
        f"{'R²':<25} {r2:.6f}\n"
        f"{'Train size':<25} {len(X_train)}\n"
        f"{'Test size':<25} {len(X_test)}\n"
        f"{'Target column':<25} {target_column}"
    )

    # Step 20: Return formatted output
    return format_output(plain_english, data_section, [residual_chart_path])


def predict_liquidity(
    credit_score: float,
    debt_ratio: float,
    region: str,
    model_path: str = "",
) -> str:
    """
    Predict liquidity risk for a single client using a previously trained model.

    The liquidity_predictor tool must be run first to train and save the model.

    Args:
        credit_score: Client credit score (e.g. 650).
        debt_ratio: Debt-to-income ratio as a decimal (e.g. 0.4 for 40%).
        region: Geographic region (e.g. "North", "South", "East", "West").
        model_path: Optional override for model file path.
                    Defaults to finance_output/models/liquidity_pipeline.joblib.

    Returns:
        Plain-English prediction with risk context and the standard disclaimer.

    Raises:
        ToolError: If no trained model file is found at the expected path.
    """
    # Step 1: Resolve model path
    path = model_path or MODEL_PATH

    # Step 2: Validate model exists
    if not os.path.exists(path):
        raise ToolError(
            f"No trained model found at '{path}'. "
            f"Run liquidity_predictor first to train the model."
        )

    # Step 3: Load model
    pipe = joblib.load(path)

    # Step 4: Build input DataFrame
    new_data = pd.DataFrame([{
        "credit_score": float(credit_score),
        "debt_ratio": float(debt_ratio),
        "region": str(region),
    }])

    # Step 5: Generate prediction
    prediction = pipe.predict(new_data)[0]

    # Step 6: Build risk context
    if prediction >= 0.7:
        risk_level = "HIGH risk"
        risk_context = (
            "This client shows a high estimated liquidity risk. "
            "Closer scrutiny of debt obligations and cash reserves is recommended."
        )
    elif prediction >= 0.4:
        risk_level = "MODERATE risk"
        risk_context = (
            "This client shows a moderate estimated liquidity risk. "
            "Standard monitoring protocols apply."
        )
    else:
        risk_level = "LOW risk"
        risk_context = (
            "This client shows a low estimated liquidity risk. "
            "No immediate liquidity concerns indicated."
        )

    confidence_note = (
        "Prediction confidence: the model's test-set RMSE provides the uncertainty range. "
        "Re-run liquidity_predictor to see current RMSE."
    )

    # Step 7: Plain-English summary
    plain_english = (
        f"Based on the trained model, this client has an estimated liquidity risk "
        f"of {prediction:.4f} ({risk_level}).\n\n"
        f"{risk_context}\n\n"
        f"Input: credit_score={credit_score}, debt_ratio={debt_ratio}, region='{region}'\n\n"
        f"{confidence_note}"
    )

    # Step 8: Return formatted output
    return format_output(plain_english)
