import pandas as pd


# ============================================================
# 1. BASIC DATA TYPE DETECTION
# ============================================================

def detect_data_type(series):
    """Detect the basic technical data type of a pandas Series."""

    # Completely empty column
    if series.isna().all():
        return "Empty"

    non_null_series = series.dropna()

    # Numeric
    if pd.api.types.is_numeric_dtype(non_null_series):
        return "Numeric"

    # Date detection
    converted_dates = pd.to_datetime(
        non_null_series,
        format="mixed",
        errors="coerce"
    )

    if len(non_null_series) > 0:
        date_ratio = converted_dates.notna().mean()
    else:
        date_ratio = 0

    if date_ratio >= 0.80:
        return "Date"

    # Categorical
    unique_ratio = (
        non_null_series.nunique() / len(non_null_series)
    )

    if unique_ratio <= 0.20:
        return "Categorical"

    # Otherwise Text
    return "Text"

    if pd.api.types.is_bool_dtype(non_null_series):
     return "Boolean"


# ============================================================
# 2. DATASET PROFILING
# ============================================================

def profile_dataset(df):
    """Create a basic technical profile for every column."""

    profile = []

    for column in df.columns:
        data_type = detect_data_type(df[column])

        profile.append({
            "column": column,
            "data_type": data_type
        })

    return profile


# ============================================================
# 3. SEMANTIC TYPE DETECTION
# ============================================================

def detect_semantic_type(df, column, data_type):
    """Infer a business-oriented semantic type."""

    series = df[column]
    column_name = column.lower()

    # Completely empty
    if data_type == "Empty":
        return "Empty"

    # Date
    if data_type == "Date":
        return "Date"

    # Numeric columns
    if data_type == "Numeric":

        # Phone / mobile / contact numbers
        if (
            "phone" in column_name
            or "mobile" in column_name
            or "contact" in column_name
        ):
            return "Phone"

        # Identifier columns
        if (
            "id" in column_name
            or column_name.endswith("_no")
            or column_name.endswith("number")
        ):

            unique_count = series.nunique()
            non_null_count = series.notna().sum()

            # Completely unique non-null values
            if (
                non_null_count > 0
                and unique_count == non_null_count
            ):
                return "Unique Identifier"

            return "Reference Identifier"

        # Other numeric columns
        return "Numeric Measure"

    # Text / categorical columns
    if data_type in {"Text", "Categorical"}:

        # Email
        if (
            "mail" in column_name
            or "email" in column_name
        ):
            return "Email"

        # Phone stored as text
        if (
            "phone" in column_name
            or "mobile" in column_name
            or "contact" in column_name
        ):
            return "Phone"

        # Gender
        if (
            "gender" in column_name
            or column_name == "sex"
            or column_name.endswith("_sex")
        ):
            return "Gender"

        # Name
        if (
            "name" in column_name
            or column_name.endswith("_nm")
        ):
            return "Name"

        # Generic categorical
        if data_type == "Categorical":
            return "Categorical"

        # Generic text
        return "Text"

    return "Text"


# ============================================================
# 4. SEMANTIC PROFILE
# ============================================================

def detect_semantic_types(df):
    """Create technical and semantic profile for every column."""

    semantic_profile = []

    for column in df.columns:

        data_type = detect_data_type(
            df[column]
        )

        semantic_type = detect_semantic_type(
            df,
            column,
            data_type
        )

        semantic_profile.append({
            "column": column,
            "data_type": data_type,
            "semantic_type": semantic_type
        })

    return semantic_profile


# ============================================================
# 5. NUMERIC ANALYSIS
# ============================================================

def analyze_numeric_columns(df):
    """Calculate basic statistics for numeric columns."""

    results = []

    for column in df.columns:

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):
            continue

        # Skip completely empty numeric columns
        if series.isna().all():
            continue

        results.append({
            "column": column,
            "min": series.min(),
            "max": series.max(),
            "mean": series.mean(),
            "median": series.median()
        })

    return results


# ============================================================
# 6. MISSING VALUE ANALYSIS
# ============================================================

def analyze_missing_values(df):
    """Calculate missing counts and percentages."""

    results = []

    total_rows = len(df)

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        if total_rows > 0:
            missing_percentage = (
                missing_count / total_rows
            ) * 100
        else:
            missing_percentage = 0.0

        results.append({
            "column": column,
            "missing_count": missing_count,
            "missing_percentage": round(
                missing_percentage,
                2
            )
        })

    return results


# ============================================================
# 7. EMPTY COLUMN ANALYSIS
# ============================================================

def analyze_empty_columns(df):
    """Return columns where every value is missing."""

    empty_columns = []

    for column in df.columns:

        if df[column].isna().all():
            empty_columns.append(column)

    return empty_columns


# ============================================================
# 8. CATEGORICAL VALUE ANALYSIS
# ============================================================

def analyze_categorical_columns(
    df,
    semantic_profile
):
    """Analyze categorical and gender columns."""

    results = []

    for item in semantic_profile:

        column = item["column"]
        semantic_type = item["semantic_type"]

        # Only categorical and gender columns
        if semantic_type not in {
            "Categorical",
            "Gender"
        }:
            continue

        series = df[column].dropna()

        # Normalize spaces before counting
        value_counts = (
            series
            .astype(str)
            .str.strip()
            .value_counts()
        )

        results.append({
            "column": column,
            "semantic_type": semantic_type,
            "unique_count": int(
                len(value_counts)
            ),
            "value_counts": value_counts.to_dict()
        })

    return results


# ============================================================
# 9. OUTLIER ANALYSIS
# ============================================================

def analyze_outliers(
    df,
    semantic_profile
):
    results = []

    for item in semantic_profile:

        column = item["column"]
        semantic_type = item["semantic_type"]

        # Only numeric measures should have statistical outliers
        if semantic_type != "Numeric Measure":
            continue

        # Get the original column
        original_series = df[column]

        # -------------------------------------------------
        # IMPORTANT:
        # Boolean columns must never go through IQR
        # calculation.
        # -------------------------------------------------

        if pd.api.types.is_bool_dtype(original_series):
            continue

        # -------------------------------------------------
        # Convert to numeric
        # -------------------------------------------------

        series = pd.to_numeric(
            original_series,
            errors="coerce"
        ).dropna()

        # -------------------------------------------------
        # Force numeric values to float.
        # This prevents Boolean dtype from reaching
        # pandas/numpy quantile calculations.
        # -------------------------------------------------

        try:
            series = series.astype(float)
        except (TypeError, ValueError):
            continue

        if series.empty:
            continue

        # -------------------------------------------------
        # IQR calculation
        # -------------------------------------------------

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        # -------------------------------------------------
        # Detect outliers
        # -------------------------------------------------

        outliers = series[
            (series < lower_bound)
            |
            (series > upper_bound)
        ]

        results.append({
            "column": column,
            "semantic_type": semantic_type,
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": int(
                len(outliers)
            )
        })

    return results