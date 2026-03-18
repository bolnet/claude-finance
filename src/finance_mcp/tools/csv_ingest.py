"""
CSV ingestion tool for ML workflow pipeline.

Provides the ingest_csv MCP tool: loads a CSV, detects structure,
cleans outliers and missing values, generates EDA charts, and
returns a plain-English summary.

Import order is CRITICAL: finance_mcp.output must be imported first
to ensure matplotlib Agg backend is set before pyplot loads.
"""
from finance_mcp.output import format_output, save_chart, ensure_output_dirs

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fastmcp.exceptions import ToolError


def _detect_structure(df: pd.DataFrame) -> dict:
    """
    Detect column types and missing value counts from a DataFrame.

    Returns a dict with keys:
      - numeric_cols: list of column names with numeric dtype
      - cat_cols: list of column names with string/object dtype
      - missing: dict mapping column name -> missing value count
      - shape: (rows, cols) tuple
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # pandas 3.x: use 'object' for string columns (covers both str and object dtypes)
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    missing = {col: int(df[col].isna().sum()) for col in df.columns if df[col].isna().any()}
    return {
        "numeric_cols": numeric_cols,
        "cat_cols": cat_cols,
        "missing": missing,
        "shape": df.shape,
    }


def _clean_dataframe(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """
    Clean a DataFrame by removing IQR outliers and filling missing values.

    Uses the 1.5*IQR rule for outlier removal. Missing numeric values are
    filled with the column median AFTER outlier removal.

    Never mutates the original DataFrame (immutability rule).

    Args:
        df: Input DataFrame.
        numeric_cols: List of numeric column names to clean.

    Returns:
        New cleaned DataFrame.
    """
    cleaned = df.copy()

    for col in numeric_cols:
        q1 = cleaned[col].quantile(0.25)
        q3 = cleaned[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        # Filter to rows within IQR bounds (NaN rows pass through — handled separately)
        cleaned = cleaned[
            cleaned[col].isna() | ((cleaned[col] >= lower) & (cleaned[col] <= upper))
        ].copy()

    # Fill remaining missing values with column median
    for col in numeric_cols:
        median_val = cleaned[col].median()
        cleaned[col] = cleaned[col].fillna(median_val)

    return cleaned


def ingest_csv(csv_path: str, target_column: str = "") -> str:
    """
    Load a CSV file, detect its structure, clean outliers, generate EDA charts,
    and return a plain-English summary with statistics.

    Args:
        csv_path: Absolute or relative path to the CSV file to ingest.
        target_column: Optional target column name for ML workflows. If provided,
                       it will be highlighted in the summary.

    Returns:
        Formatted plain-English summary including column info, descriptive
        statistics, chart file paths, and the standard investment disclaimer.

    Raises:
        ToolError: If the CSV file does not exist at the given path.
    """
    if not os.path.exists(csv_path):
        raise ToolError(
            f"The file '{csv_path}' was not found. Check the path and try again."
        )

    df = pd.read_csv(csv_path)
    basename = os.path.basename(csv_path)

    structure = _detect_structure(df)
    numeric_cols = structure["numeric_cols"]
    cat_cols = structure["cat_cols"]
    missing = structure["missing"]
    n_rows, n_cols = structure["shape"]

    # Record row count before cleaning for reporting
    original_row_count = n_rows

    # Clean the data
    cleaned_df = _clean_dataframe(df, numeric_cols)
    removed_rows = original_row_count - len(cleaned_df)

    # Build missing values summary text
    if missing:
        missing_parts = [f"{col} ({cnt} missing)" for col, cnt in missing.items()]
        missing_summary = "Missing values found in: " + ", ".join(missing_parts) + ". Filled with column median."
    else:
        missing_summary = "No missing values detected."

    # Build plain-English summary
    target_note = f" Target column: '{target_column}'." if target_column else ""
    plain_english = (
        f"Loaded {original_row_count} rows and {n_cols} columns from {basename}."
        f" Found {len(numeric_cols)} numeric columns ({', '.join(numeric_cols) or 'none'})"
        f" and {len(cat_cols)} categorical columns ({', '.join(cat_cols) or 'none'})."
        f" Cleaned {removed_rows} outlier rows using the IQR method."
        f" {missing_summary}{target_note}"
    )

    # Generate EDA charts — up to 4 numeric columns
    ensure_output_dirs()
    chart_paths = []
    for col in numeric_cols[:4]:
        fig, ax = plt.subplots(figsize=(7, 4))
        cleaned_df[col].dropna().plot.hist(ax=ax, bins=20, edgecolor="black")
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")

        # Sanitize column name for filename
        safe_col = col.replace(" ", "_").replace("/", "_").lower()
        chart_name = f"eda_{safe_col}.png"
        path = save_chart(fig, chart_name)
        chart_paths.append(path)

    # Build descriptive statistics section
    data_section = cleaned_df.describe().to_string()

    return format_output(plain_english, data_section, chart_paths)
