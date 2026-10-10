import os
import pandas as pd

from profiler import (
    profile_dataset,
    detect_semantic_types,
    analyze_numeric_columns,
    analyze_missing_values,
    analyze_empty_columns,
    analyze_categorical_columns,
    analyze_outliers
)

from rule_engine import (
    generate_validation_rules,
    display_rules
)

from validation_engine import (
    validate_dataset,
    display_validation_results,
    generate_quality_summary
)

from issue_analyzer import (
    analyze_all_issues,
    display_issues
)

from ai_analyzer import (
    analyze_issues_with_ai,
    display_ai_analysis
)

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# ============================================================
# LOAD DATASET
# ============================================================

# ============================================================
# INPUT CSV FILE
# ============================================================


def load_dataset(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".csv":

        print("Loading CSV dataset...")

        df = pd.read_csv(
            file_path
        )

    elif extension == ".xlsx":

        print("Loading Excel dataset...")

        df = pd.read_excel(
            file_path
        )

    elif extension == ".xls":

        print("Loading Excel dataset...")

        df = pd.read_excel(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file format.\n"
            "Supported formats: CSV, XLSX, XLS"
        )

    return df


# ============================================================
# DISPLAY DATASET PROFILE
# ============================================================

def display_profile(
    profile
):

    print("\n" + "=" * 70)
    print("DATASET PROFILE")
    print("=" * 70)

    for item in profile:

        print(
            f"{item['column']} "
            f"-> {item['data_type']}"
        )


# ============================================================
# DISPLAY SEMANTIC PROFILE
# ============================================================

def display_semantic_profile(
    semantic_profile
):

    print("\n" + "=" * 70)
    print("SEMANTIC PROFILE")
    print("=" * 70)

    for item in semantic_profile:

        print(
            f"{item['column']} "
            f"-> {item['semantic_type']}"
        )


# ============================================================
# DISPLAY MISSING VALUES
# ============================================================

def display_missing_analysis(
    missing_analysis
):

    print("\n" + "=" * 70)
    print("MISSING VALUE ANALYSIS")
    print("=" * 70)

    for item in missing_analysis:

        print(
            f"{item['column']} "
            f"-> {item['missing_count']} "
            f"missing "
            f"({item['missing_percentage']}%)"
        )


# ============================================================
# DISPLAY NUMERIC ANALYSIS
# ============================================================

def display_numeric_analysis(
    numeric_analysis
):

    print("\n" + "=" * 70)
    print("NUMERIC ANALYSIS")
    print("=" * 70)

    for item in numeric_analysis:

        print(
            f"{item['column']} "
            f"-> "
            f"Min: {item['min']} | "
            f"Max: {item['max']} | "
            f"Mean: {round(item['mean'], 2)} | "
            f"Median: {round(item['median'], 2)}"
        )


# ============================================================
# DISPLAY CATEGORICAL ANALYSIS
# ============================================================

def display_categorical_analysis(
    categorical_analysis
):

    print("\n" + "=" * 70)
    print("CATEGORICAL ANALYSIS")
    print("=" * 70)

    for item in categorical_analysis:

        print(
            f"\n{item['column']} "
            f"({item['semantic_type']})"
        )

        print(
            f"Unique Values: "
            f"{item['unique_count']}"
        )

        for value, count in (
            item["value_counts"]
            .items()
        ):

            print(
                f"  {value} -> {count}"
            )


# ============================================================
# DISPLAY OUTLIER ANALYSIS
# ============================================================

def display_outlier_analysis(
    outlier_analysis
):

    print("\n" + "=" * 70)
    print("OUTLIER ANALYSIS")
    print("=" * 70)

    for item in outlier_analysis:

        print(
            f"{item['column']} "
            f"-> "
            f"Outliers: {item['outlier_count']} | "
            f"Lower Bound: {round(item['lower_bound'], 2)} | "
            f"Upper Bound: {round(item['upper_bound'], 2)}"
        )


# ============================================================
# DISPLAY QUALITY SUMMARY
# ============================================================

def display_quality_summary(
    quality_summary
):

    print("\n" + "=" * 70)
    print("DATA QUALITY SUMMARY")
    print("=" * 70)

    print(
        f"Quality Score     : "
        f"{quality_summary['quality_score']} / 100"
    )

    print(
        f"Cell Errors       : "
        f"{quality_summary['cell_errors']}"
    )

    print(
        f"Structural Errors : "
        f"{quality_summary['structural_errors']}"
    )

    print(
        f"Total Errors      : "
        f"{quality_summary['total_errors']}"
    )

    print(
        f"Total Rows        : "
        f"{quality_summary['total_rows']}"
    )

    print(
        f"Total Columns     : "
        f"{quality_summary['total_columns']}"
    )

    print(
        f"Total Cells       : "
        f"{quality_summary['total_cells']}"
    )

    print(
        f"Error Percentage  : "
        f"{quality_summary['error_percentage']}%"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("AI-POWERED DATA QUALITY AGENT")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: LOAD DATASET
    # --------------------------------------------------------

    df, file_path = load_dataset()

    # --------------------------------------------------------
    # STEP 2: BASIC PROFILE
    # --------------------------------------------------------

    profile = profile_dataset(
        df
    )

    display_profile(
        profile
    )

    # --------------------------------------------------------
    # STEP 3: SEMANTIC DETECTION
    # --------------------------------------------------------

    semantic_profile = detect_semantic_types(
        df
    )

    display_semantic_profile(
        semantic_profile
    )

    # --------------------------------------------------------
    # STEP 4: NUMERIC ANALYSIS
    # --------------------------------------------------------

    numeric_analysis = analyze_numeric_columns(
        df
    )

    display_numeric_analysis(
        numeric_analysis
    )

    # --------------------------------------------------------
    # STEP 5: MISSING VALUE ANALYSIS
    # --------------------------------------------------------

    missing_analysis = analyze_missing_values(
        df
    )

    display_missing_analysis(
        missing_analysis
    )

    # --------------------------------------------------------
    # STEP 6: EMPTY COLUMN ANALYSIS
    # --------------------------------------------------------

    empty_columns = analyze_empty_columns(
        df
    )

    print("\n" + "=" * 70)
    print("EMPTY COLUMNS")
    print("=" * 70)

    if empty_columns:

        for column in empty_columns:
            print(column)

    else:

        print("No completely empty columns found.")

    # --------------------------------------------------------
    # STEP 7: CATEGORICAL ANALYSIS
    # --------------------------------------------------------

    categorical_analysis = (
        analyze_categorical_columns(
            df,
            semantic_profile
        )
    )

    display_categorical_analysis(
        categorical_analysis
    )

    # --------------------------------------------------------
    # STEP 8: OUTLIER ANALYSIS
    # --------------------------------------------------------

    outlier_analysis = analyze_outliers(
        df,
        semantic_profile
    )

    display_outlier_analysis(
        outlier_analysis
    )

    # --------------------------------------------------------
    # STEP 9: GENERATE VALIDATION RULES
    # --------------------------------------------------------

    validation_rules = (
        generate_validation_rules(
            df,
            semantic_profile
        )
    )

    display_rules(
        validation_rules
    )

    # --------------------------------------------------------
    # STEP 10: EXECUTE VALIDATION
    # --------------------------------------------------------

    validation_results = validate_dataset(
        df,
        validation_rules
    )

    display_validation_results(
        validation_results
    )

    # --------------------------------------------------------
    # STEP 11: QUALITY SUMMARY
    # --------------------------------------------------------

    total_rows = len(df)

    total_columns = len(
        df.columns
    )

    total_cells = (
        total_rows
        * total_columns
    )

    quality_summary = (
        generate_quality_summary(
            validation_results,
            total_rows=total_rows,
            total_columns=total_columns,
            total_cells=total_cells
        )
    )

    display_quality_summary(
        quality_summary
    )

    # --------------------------------------------------------
    # STEP 12: ISSUE ANALYSIS
    # --------------------------------------------------------

    issues = analyze_all_issues(
        validation_results,
        total_rows
    )

    display_issues(
        issues
    )
    # --------------------------------------------------------
# STEP 13: AI ANALYSIS
# --------------------------------------------------------

    ai_analyzed_issues = analyze_issues_with_ai(
    issues
)

    display_ai_analysis(
    ai_analyzed_issues
)
    # --------------------------------------------------------
    # FINAL MESSAGE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATA QUALITY ANALYSIS COMPLETED")
    print("=" * 70)

    print(
        f"Dataset: "
        f"{os.path.basename(file_path)}"
    )

    print(
        f"Final Quality Score: "
        f"{quality_summary['quality_score']} / 100"
    )

    print(
        f"Total Issues: "
        f"{len(issues)}"
    )

    print("=" * 70)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()