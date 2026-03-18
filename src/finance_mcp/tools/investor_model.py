"""
Investor segment classifier tools for ML workflow pipeline.

Provides two MCP tools:
  - investor_classifier: Train a RandomForest classifier on investor CSV data
    using feature engineering, stratified split, and GridSearchCV.
  - classify_investor: Predict segment for a new investor using the trained model.

Import order is CRITICAL: finance_mcp.output must be imported first
to ensure matplotlib Agg backend is set before pyplot loads.
"""
from finance_mcp.output import format_output, save_chart, ensure_output_dirs
from finance_mcp.tools.csv_ingest import _detect_structure, _clean_dataframe

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from fastmcp.exceptions import ToolError

MODEL_DIR = os.path.join("finance_output", "models")
INVESTOR_MODEL_PATH = os.path.join(MODEL_DIR, "investor_pipeline.joblib")

# Known target column keyword hints for auto-detection
_TARGET_KEYWORDS = ("segment", "class", "label", "type", "category")


def investor_classifier(csv_path: str, target_column: str = "segment") -> str:
    """
    Train an investor segment classifier from a CSV file using RandomForest with GridSearchCV.

    Performs feature engineering (dummy variables), stratified split, cross-validation,
    hyperparameter search, and outputs confusion matrix, classification report, and feature importance.

    Args:
        csv_path: Absolute or relative path to the investor CSV file.
        target_column: Column name to predict. Defaults to 'segment'.
                       Auto-detects if not found: column containing 'segment'/'class'/'label'/'type'.

    Returns:
        Formatted plain-English output with confusion matrix, classification report,
        feature importance chart paths, and the standard investment disclaimer.

    Raises:
        ToolError: If the CSV file does not exist, or if no target column can be detected.
    """
    # Step 1: Validate path
    if not os.path.exists(csv_path):
        raise ToolError(f"The file '{csv_path}' was not found. Check the path and try again.")

    # Step 2: Load CSV
    df = pd.read_csv(csv_path)

    # Step 3: Auto-detect target column if not in df.columns
    if target_column not in df.columns:
        detected = None
        for col in df.columns:
            if any(kw in col.lower() for kw in _TARGET_KEYWORDS):
                detected = col
                break
        if detected is None:
            raise ToolError(
                f"Could not find target column '{target_column}' or any column containing "
                f"'segment', 'class', 'label', 'type', 'category'. "
                f"Available columns: {list(df.columns)}"
            )
        target_column = detected

    # Step 4-5: Detect structure and clean
    structure = _detect_structure(df)
    df_clean = _clean_dataframe(df, structure["numeric_cols"])

    # Step 6: Feature engineering (INVX-02 — curriculum approach, NOT ColumnTransformer)
    y = df_clean[target_column]
    df_features = df_clean.drop(columns=[target_column])
    # get_dummies creates bool dtype for dummy columns in pandas 3.x — sklearn accepts bool
    df_encoded = pd.get_dummies(df_features, drop_first=True)

    # Step 7: Stratified split (INVX-03)
    X_train, X_test, y_train, y_test = train_test_split(
        df_encoded, y, test_size=0.2, stratify=y, random_state=42
    )

    # Step 8: Build pipeline (StandardScaler handles numeric + bool columns)
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(random_state=42)),
    ])

    # Step 9: GridSearchCV (INVX-04) — 3 x 3 x 2 = 18 combinations
    param_grid = {
        "classifier__n_estimators": [50, 100, 200],
        "classifier__max_depth": [3, 5, 10],
        "classifier__min_samples_split": [2, 5],
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    gs = GridSearchCV(pipe, param_grid, cv=cv, scoring="accuracy", n_jobs=-1)
    gs.fit(X_train, y_train)
    best_pipe = gs.best_estimator_

    # Step 10: Cross-validation score on best estimator
    cv_scores = cross_val_score(best_pipe, X_train, y_train, cv=cv, scoring="accuracy")

    # Step 11: Evaluate on test set
    y_pred = best_pipe.predict(X_test)
    test_accuracy = float((y_pred == y_test).mean())

    # Step 12: Confusion matrix chart (INVX-05)
    ensure_output_dirs()
    cm = confusion_matrix(y_test, y_pred, labels=best_pipe.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_pipe.classes_)
    fig, ax = plt.subplots(figsize=(8, 6))
    disp.plot(ax=ax, colorbar=True)
    ax.set_title("Investor Segment Confusion Matrix")
    cm_path = save_chart(fig, "confusion_matrix.png")

    # Step 13: Classification report
    report = classification_report(y_test, y_pred)

    # Step 14: Feature importance chart
    feature_names = df_encoded.columns.tolist()
    importances = best_pipe.named_steps["classifier"].feature_importances_
    importance_series = (
        pd.Series(importances, index=feature_names)
        .sort_values(ascending=False)
        .head(10)
    )
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    importance_series.plot(kind="bar", ax=ax2)
    ax2.set_title("Top 10 Feature Importances")
    ax2.set_xlabel("Feature")
    ax2.set_ylabel("Importance")
    plt.tight_layout()
    fi_path = save_chart(fig2, "feature_importance.png")

    # Step 15: Persist model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_pipe, INVESTOR_MODEL_PATH)

    # Step 16: Build plain-English interpretation
    top_feature = importance_series.index[0]
    second_feature = importance_series.index[1] if len(importance_series) > 1 else "N/A"

    performance_note = (
        "This is strong classification performance."
        if test_accuracy >= 0.8
        else "Consider reviewing feature quality or collecting more data per class."
    )

    plain_english = (
        f"The model correctly identifies investor segments {test_accuracy * 100:.1f}% of the time "
        f"on unseen data. "
        f"Best parameters found: {gs.best_params_}. "
        f"Cross-validation accuracy: {cv_scores.mean() * 100:.1f}% "
        f"\u00b1 {cv_scores.std() * 100:.1f}% across 5 folds \u2014 "
        f"this shows how consistent the model is. "
        f"The most important factor for segment classification is '{top_feature}', "
        f"followed by '{second_feature}'. "
        f"{performance_note} "
        f"The confusion matrix below shows prediction accuracy per segment."
    )

    # Step 17: Data section
    data_section = (
        "Classification Report:\n"
        + report
        + "\nBest Parameters: "
        + str(gs.best_params_)
    )

    # Step 18: Return formatted output
    return format_output(plain_english, data_section, [cm_path, fi_path])


def classify_investor(
    age: float,
    income: float,
    risk_tolerance: float,
    product_preference: str,
    model_path: str = "",
) -> str:
    """
    Classify a new investor into a segment using the previously trained model.

    The investor_classifier tool must be run first to train and save the model.

    Args:
        age: Investor age in years (e.g. 35).
        income: Annual income in dollars (e.g. 75000).
        risk_tolerance: Risk tolerance as decimal 0.0-1.0 (e.g. 0.6 for moderate-high).
        product_preference: Preferred product type (e.g. "stocks", "bonds", "mixed").
        model_path: Optional override for model file path.

    Returns:
        Formatted plain-English classification result with segment label, confidence,
        and top feature explanations.

    Raises:
        ToolError: If no trained model is found at the expected path.
    """
    # Step 1-2: Load model
    path = model_path or INVESTOR_MODEL_PATH
    if not os.path.exists(path):
        raise ToolError(
            f"No trained model found at '{path}'. "
            "Run investor_classifier first to train and save the model."
        )
    best_pipe = joblib.load(path)

    # Step 4: Build input DataFrame
    new_data = pd.DataFrame([{
        "age": float(age),
        "income": float(income),
        "risk_tolerance": float(risk_tolerance),
        "product_preference": str(product_preference),
    }])

    # Step 5: Encode new data with same get_dummies approach
    new_encoded = pd.get_dummies(new_data, drop_first=True)

    # Step 6: Align columns with training data
    train_cols = best_pipe.named_steps["scaler"].feature_names_in_
    new_encoded = new_encoded.reindex(columns=train_cols, fill_value=0)

    # Step 7-11: Predict and get probabilities
    segment = best_pipe.predict(new_encoded)[0]
    proba = best_pipe.predict_proba(new_encoded)[0]
    confidence = float(max(proba))
    classes = best_pipe.classes_
    proba_dict = dict(zip(classes, proba))

    # Step 12: Top features from classifier
    importances = best_pipe.named_steps["classifier"].feature_importances_
    top_features = sorted(
        zip(train_cols, importances), key=lambda x: x[1], reverse=True
    )[:3]
    feature_text = ", ".join(
        [f"{f[0]} (importance: {f[1]:.2f})" for f in top_features]
    )

    # Step 13: Segment context
    segment_contexts = {
        "conservative": "Conservative investors typically prefer lower-risk, stable return products.",
        "moderate": "Moderate investors balance growth with capital preservation.",
        "aggressive": "Aggressive investors prioritize high growth and can tolerate higher volatility.",
    }
    segment_context = segment_contexts.get(
        str(segment).lower(),
        f"This investor profile matches the '{segment}' segment."
    )

    # Plain-English output
    plain_english = (
        f"Based on the provided attributes, this investor is classified as '{segment}' "
        f"with {confidence * 100:.1f}% confidence. "
        f"The top factors driving this classification are: {feature_text}. "
        f"{segment_context}"
    )

    # Step 14: Probability breakdown table
    proba_lines = ["Segment probabilities:"]
    for cls, prob in sorted(proba_dict.items(), key=lambda x: x[1], reverse=True):
        proba_lines.append(f"  {cls}: {prob * 100:.1f}%")
    data_section = "\n".join(proba_lines)

    # Step 15: Return formatted output
    return format_output(plain_english, data_section)
