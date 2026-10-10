import pandas as pd
from datetime import datetime


# ============================================================
# 1. MISSING VALUE CHECK
# ============================================================

def missing_check(df, column):

    missing_count = int(
        df[column].isna().sum()
    )

    return {
        "column": column,
        "rule": "missing_check",
        "failed_count": missing_count,
        "status": (
            "PASS"
            if missing_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 2. DUPLICATE VALUE CHECK
# ============================================================

def duplicate_value_check(df, column):

    series = df[column]

    duplicate_count = int(
        series.duplicated(
            keep=False
        ).sum()
    )

    return {
        "column": column,
        "rule": "duplicate_value_check",
        "failed_count": duplicate_count,
        "status": (
            "PASS"
            if duplicate_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 3. WHITESPACE CHECK
# ============================================================

def whitespace_check(df, column):

    series = df[column].dropna()

    whitespace_count = 0

    for value in series:

        text = str(value)

        if text != text.strip():
            whitespace_count += 1

    return {
        "column": column,
        "rule": "whitespace_check",
        "failed_count": int(
            whitespace_count
        ),
        "status": (
            "PASS"
            if whitespace_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 4. GENDER VALIDATION
# ============================================================

def gender_validation_check(df, column):

    """
    Current business rule:

    Valid values:
        Male
        Female
        M
        F

    Case and surrounding whitespace are ignored.

    Examples accepted:
        Male
        male
        MALE
        Male
        M
        m
        F
        f

    Examples rejected:
        Non-Binary
        Non-Binary
        Unknown
        Other
        X
        N/A
    """

    allowed_values = {
        "male",
        "female",
        "m",
        "f"
    }

    invalid_count = 0

    for value in df[column].dropna():

        normalized_value = (
            str(value)
            .strip()
            .lower()
        )

        if normalized_value not in allowed_values:
            invalid_count += 1

    return {
        "column": column,
        "rule": "gender_validation_check",
        "failed_count": int(
            invalid_count
        ),
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 5. CATEGORY CONSISTENCY CHECK
# ============================================================

def category_consistency_check(df, column):

    series = df[column].dropna()

    normalized_values = (
        series
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Count possible formatting duplicates.
    # Example:
    # "Remote"
    # "remote"
    # " Remote "
    #
    # They are treated as the same normalized category.

    original_unique = series.astype(str).nunique()
    normalized_unique = normalized_values.nunique()

    inconsistent_count = max(
        0,
        original_unique - normalized_unique
    )

    return {
        "column": column,
        "rule": "category_consistency_check",
        "failed_count": int(
            inconsistent_count
        ),
        "status": (
            "PASS"
            if inconsistent_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 6. INVALID DATE CHECK
# ============================================================

def invalid_date_check(df, column):

    original_series = df[column]

    converted_dates = pd.to_datetime(
        original_series,
        format="mixed",
        errors="coerce"
    )

    invalid_mask = (
        original_series.notna()
        & converted_dates.isna()
    )

    invalid_count = int(
        invalid_mask.sum()
    )

    return {
        "column": column,
        "rule": "invalid_date_check",
        "failed_count": invalid_count,
        "status": (
            "PASS"
            if invalid_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 7. FUTURE DATE CHECK
# ============================================================

def future_date_check(df, column):

    converted_dates = pd.to_datetime(
        df[column],
        format="mixed",
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    future_mask = (
        converted_dates.notna()
        & (converted_dates > today)
    )

    future_count = int(
        future_mask.sum()
    )

    return {
        "column": column,
        "rule": "future_date_check",
        "failed_count": future_count,
        "status": (
            "PASS"
            if future_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 8. OUTLIER CHECK
# ============================================================

def outlier_check(df, column):

    # Get the original column
    original_series = df[column]

    # -------------------------------------------------
    # Boolean columns are not suitable for IQR
    # outlier detection.
    # -------------------------------------------------

    if pd.api.types.is_bool_dtype(original_series):
        return {
            "column": column,
            "rule": "outlier_check",
            "failed_count": 0,
            "status": "PASS"
        }

    # -------------------------------------------------
    # Convert values safely to numeric
    # -------------------------------------------------

    series = pd.to_numeric(
        original_series,
        errors="coerce"
    ).dropna()

    # -------------------------------------------------
    # Force numeric values to float
    # -------------------------------------------------

    try:
        series = series.astype(float)
    except (TypeError, ValueError):

        return {
            "column": column,
            "rule": "outlier_check",
            "failed_count": 0,
            "status": "PASS"
        }

    if series.empty:

        return {
            "column": column,
            "rule": "outlier_check",
            "failed_count": 0,
            "status": "PASS"
        }

    # -------------------------------------------------
    # Calculate IQR
    # -------------------------------------------------

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)

    upper_bound = q3 + (1.5 * iqr)

    # -------------------------------------------------
    # Find outliers
    # -------------------------------------------------

    outlier_mask = (
        (series < lower_bound)
        |
        (series > upper_bound)
    )

    outlier_count = int(
        outlier_mask.sum()
    )

    return {
        "column": column,
        "rule": "outlier_check",
        "failed_count": outlier_count,
        "status": (
            "PASS"
            if outlier_count == 0
            else "FAIL"
        )
    }

# ============================================================
# 9. RANGE CHECK
# ============================================================

def range_check(df, column):

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    negative_count = int(
        (series < 0).sum()
    )

    return {
        "column": column,
        "rule": "range_check",
        "failed_count": negative_count,
        "status": (
            "PASS"
            if negative_count == 0
            else "FAIL"
        )
    }


# ============================================================
# 10. RULE EXECUTION
# ============================================================

def execute_rule(
    df,
    column,
    rule
):
    """
    Execute one validation rule.
    """

    if rule == "missing_check":

        return missing_check(
            df,
            column
        )

    elif rule == "duplicate_value_check":

        return duplicate_value_check(
            df,
            column
        )

    elif rule == "whitespace_check":

        return whitespace_check(
            df,
            column
        )

    elif rule == "gender_validation_check":

        return gender_validation_check(
            df,
            column
        )

    elif rule == "category_consistency_check":

        return category_consistency_check(
            df,
            column
        )

    elif rule == "invalid_date_check":

        return invalid_date_check(
            df,
            column
        )

    elif rule == "future_date_check":

        return future_date_check(
            df,
            column
        )

    elif rule == "outlier_check":

        return outlier_check(
            df,
            column
        )

    elif rule == "range_check":

        return range_check(
            df,
            column
        )

    else:

        return {
            "column": column,
            "rule": rule,
            "failed_count": 0,
            "status": "SKIPPED"
        }


# ============================================================
# 11. VALIDATE DATASET
# ============================================================

def validate_dataset(
    df,
    validation_rules
):
    """
    Execute all generated validation rules.
    """

    validation_results = []

    for rule_definition in validation_rules:

        column = rule_definition["column"]
        rule = rule_definition["rule"]

        result = execute_rule(
            df,
            column,
            rule
        )

        validation_results.append(
            result
        )

    return validation_results


# ============================================================
# 12. QUALITY SUMMARY
# ============================================================

def generate_quality_summary(
    validation_results,
    total_rows,
    total_columns=None,
    total_cells=None
):
    """
    Generate overall data quality score.

    Cell errors are calculated from all failed
    validation rules.

    Structural errors are reserved for future
    dataset-level structural checks.
    """

    if total_cells is None:

        total_cells = (
            total_rows
            * total_columns
        )

    cell_errors = 0

    structural_errors = 0

    for result in validation_results:

        if result["status"] == "FAIL":

            cell_errors += int(
                result["failed_count"]
            )

    total_errors = (
        cell_errors
        + structural_errors
    )

    if total_cells > 0:

        error_percentage = (
            total_errors
            / total_cells
        ) * 100

        quality_score = max(
            0,
            100 - error_percentage
        )

    else:

        error_percentage = 0.0
        quality_score = 100.0

    return {
        "quality_score": round(
            quality_score,
            2
        ),
        "cell_errors": int(
            cell_errors
        ),
        "structural_errors": int(
            structural_errors
        ),
        "total_errors": int(
            total_errors
        ),
        "total_rows": int(
            total_rows
        ),
        "total_columns": int(
            total_columns
        ),
        "total_cells": int(
            total_cells
        ),
        "error_percentage": round(
            error_percentage,
            2
        )
    }


# ============================================================
# 13. PRINT VALIDATION RESULTS
# ============================================================

def display_validation_results(
    validation_results
):

    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)

    for result in validation_results:

        print(
            f"{result['column']} "
            f"-> {result['rule']} "
            f"-> {result['status']} "
            f"-> {result['failed_count']}"
        )


# ============================================================
# END OF validation_engine.py
# ============================================================