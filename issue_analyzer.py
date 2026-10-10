# ============================================================
# ISSUE SEVERITY
# ============================================================

def determine_severity(
    column,
    rule,
    failed_count,
    total_rows
):
    """
    Determine issue severity based on the type and
    percentage of affected records.
    """

    if total_rows <= 0:
        return "LOW"

    affected_percentage = (
        failed_count
        / total_rows
    ) * 100

    # --------------------------------------------------------
    # HIGH SEVERITY
    # --------------------------------------------------------

    if rule == "gender_validation_check":

        return "HIGH"

    if rule == "duplicate_value_check":

        return "HIGH"

    if affected_percentage >= 20:

        return "HIGH"

    # --------------------------------------------------------
    # MEDIUM SEVERITY
    # --------------------------------------------------------

    if rule == "missing_check":

        if affected_percentage >= 5:
            return "MEDIUM"

        return "LOW"

    if rule == "invalid_date_check":

        return "MEDIUM"

    if rule == "future_date_check":

        return "MEDIUM"

    if rule == "range_check":

        return "MEDIUM"

    # --------------------------------------------------------
    # LOW SEVERITY
    # --------------------------------------------------------

    if rule == "outlier_check":

        return "LOW"

    if rule == "whitespace_check":

        return "LOW"

    if rule == "category_consistency_check":

        return "LOW"

    return "LOW"


# ============================================================
# ISSUE FINDING
# ============================================================

def generate_finding(
    column,
    rule,
    failed_count
):

    if rule == "missing_check":

        return (
            f"{failed_count} records contain "
            f"missing values in {column}."
        )

    if rule == "duplicate_value_check":

        return (
            f"{failed_count} records contain "
            f"duplicate values in {column}."
        )

    if rule == "whitespace_check":

        return (
            f"{failed_count} values in {column} "
            f"contain leading or trailing whitespace."
        )

    if rule == "gender_validation_check":

        return (
            f"{failed_count} values in {column} "
            f"do not match the allowed gender values."
        )

    if rule == "category_consistency_check":

        return (
            f"{failed_count} inconsistent categorical "
            f"representations were detected in {column}."
        )

    if rule == "invalid_date_check":

        return (
            f"{failed_count} invalid date values "
            f"were detected in {column}."
        )

    if rule == "future_date_check":

        return (
            f"{failed_count} future date values "
            f"were detected in {column}."
        )

    if rule == "outlier_check":

        return (
            f"{failed_count} statistical outliers "
            f"were detected in {column}."
        )

    if rule == "range_check":

        return (
            f"{failed_count} values outside the "
            f"allowed numeric range were detected in {column}."
        )

    return (
        f"{failed_count} quality issues were "
        f"detected in {column}."
    )


# ============================================================
# ROOT CAUSE
# ============================================================

def generate_root_cause(
    column,
    rule
):

    if rule == "missing_check":

        return (
            "Source records contain missing or "
            "unpopulated values."
        )

    if rule == "duplicate_value_check":

        return (
            "The identifier contains duplicate "
            "records or duplicate identifier values."
        )

    if rule == "whitespace_check":

        return (
            "Text values contain inconsistent "
            "leading or trailing spaces."
        )

    if rule == "gender_validation_check":

        return (
            "Gender values do not follow the "
            "defined business standard."
        )

    if rule == "category_consistency_check":

        return (
            "Categorical values use inconsistent "
            "representations or formatting."
        )

    if rule == "invalid_date_check":

        return (
            "Some date values cannot be interpreted "
            "as valid dates."
        )

    if rule == "future_date_check":

        return (
            "Some records contain dates later than "
            "the current date."
        )

    if rule == "outlier_check":

        return (
            "Some numeric values are statistically "
            "far from the normal distribution."
        )

    if rule == "range_check":

        return (
            "Some numeric values violate the "
            "expected business range."
        )

    return (
        "The underlying data does not satisfy "
        "the configured validation rule."
    )


# ============================================================
# BUSINESS IMPACT
# ============================================================

def generate_business_impact(
    column,
    rule
):

    if rule == "missing_check":

        return (
            "Missing data may reduce the completeness "
            "of reporting and downstream analysis."
        )

    if rule == "duplicate_value_check":

        return (
            "Duplicate identifiers may cause duplicate "
            "records, incorrect counts and reporting errors."
        )

    if rule == "whitespace_check":

        return (
            "Whitespace inconsistencies may affect "
            "matching, grouping and data integration."
        )

    if rule == "gender_validation_check":

        return (
            "Invalid gender values can affect demographic "
            "analysis, reporting and segmentation."
        )

    if rule == "category_consistency_check":

        return (
            "Inconsistent categories can split the same "
            "business category into multiple groups."
        )

    if rule == "invalid_date_check":

        return (
            "Invalid dates can affect time-based analysis, "
            "reporting and trend calculations."
        )

    if rule == "future_date_check":

        return (
            "Future dates may produce incorrect time-based "
            "metrics and reporting."
        )

    if rule == "outlier_check":

        return (
            "Extreme values may distort averages, "
            "statistics and analytical models."
        )

    if rule == "range_check":

        return (
            "Out-of-range values may represent invalid "
            "business records and affect calculations."
        )

    return (
        "The issue may affect data reliability "
        "and downstream analysis."
    )


# ============================================================
# RECOMMENDATION
# ============================================================

def generate_recommendation(
    column,
    rule
):

    if rule == "missing_check":

        return (
            f"Investigate the source of missing values "
            f"in {column} and populate them where appropriate."
        )

    if rule == "duplicate_value_check":

        return (
            f"Remove duplicate records or enforce "
            f"uniqueness constraints on {column}."
        )

    if rule == "whitespace_check":

        return (
            f"Apply TRIM/strip normalization to "
            f"{column} before storing or processing values."
        )

    if rule == "gender_validation_check":

        return (
            f"Standardize {column} using the approved "
            f"values: Male, Female, M and F."
        )

    if rule == "category_consistency_check":

        return (
            f"Standardize categorical values in {column} "
            f"using a controlled list of approved categories."
        )

    if rule == "invalid_date_check":

        return (
            f"Validate and standardize date formats "
            f"before loading {column}."
        )

    if rule == "future_date_check":

        return (
            f"Review future dates in {column} and "
            f"correct records that should represent past events."
        )

    if rule == "outlier_check":

        return (
            f"Review extreme values in {column} and "
            f"confirm whether they are genuine business values "
            f"or data-entry errors."
        )

    if rule == "range_check":

        return (
            f"Apply business range validation to {column} "
            f"before accepting the record."
        )

    return (
        f"Review and correct the affected values "
        f"in {column}."
    )


# ============================================================
# ANALYZE SINGLE ISSUE
# ============================================================

def analyze_issue(
    validation_result,
    total_rows
):
    """
    Convert one failed validation result into
    a business-oriented issue.
    """

    column = validation_result["column"]
    rule = validation_result["rule"]
    failed_count = validation_result["failed_count"]

    severity = determine_severity(
        column,
        rule,
        failed_count,
        total_rows
    )

    finding = generate_finding(
        column,
        rule,
        failed_count
    )

    root_cause = generate_root_cause(
        column,
        rule
    )

    business_impact = generate_business_impact(
        column,
        rule
    )

    recommendation = generate_recommendation(
        column,
        rule
    )

    if total_rows > 0:

        affected_percentage = (
            failed_count
            / total_rows
        ) * 100

    else:

        affected_percentage = 0.0

    return {
        "column": column,
        "rule": rule,
        "severity": severity,
        "failed_count": int(
            failed_count
        ),
        "affected_percentage": round(
            affected_percentage,
            2
        ),
        "finding": finding,
        "root_cause": root_cause,
        "business_impact": business_impact,
        "recommendation": recommendation
    }


# ============================================================
# ANALYZE ALL ISSUES
# ============================================================

def analyze_all_issues(
    validation_results,
    total_rows
):
    """
    Analyze all failed validation rules.
    """

    issues = []

    for result in validation_results:

        if result["status"] != "FAIL":
            continue

        issue = analyze_issue(
            result,
            total_rows
        )

        issues.append(issue)

    return issues


# ============================================================
# DISPLAY ISSUES
# ============================================================

def display_issues(issues):

    print("\n" + "=" * 70)
    print("ISSUE ANALYSIS")
    print("=" * 70)

    if not issues:

        print("No data quality issues found.")

        return

    for issue in issues:

        print(
            f"\nColumn       : "
            f"{issue['column']}"
        )

        print(
            f"Rule         : "
            f"{issue['rule']}"
        )

        print(
            f"Severity     : "
            f"{issue['severity']}"
        )

        print(
            f"Failed Count : "
            f"{issue['failed_count']}"
        )

        print(
            f"Impact %     : "
            f"{issue['affected_percentage']}%"
        )

        print(
            f"Finding      : "
            f"{issue['finding']}"
        )

        print(
            f"Root Cause   : "
            f"{issue['root_cause']}"
        )

        print(
            f"Business     : "
            f"{issue['business_impact']}"
        )

        print(
            f"Recommendation: "
            f"{issue['recommendation']}"
        )


# ============================================================
# END OF issue_analyzer.py
# ============================================================