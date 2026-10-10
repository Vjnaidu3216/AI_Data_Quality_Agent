import pandas as pd


# ============================================================
# 1. GENERATE RULES FOR A COLUMN
# ============================================================

def generate_rules_for_column(
    df,
    column,
    data_type,
    semantic_type
):
    """
    Dynamically generate validation rules for a column
    based on its technical and semantic type.
    """

    rules = []

    # --------------------------------------------------------
    # COMMON RULE: MISSING VALUES
    # --------------------------------------------------------

    rules.append({
        "column": column,
        "rule": "missing_check",
        "description": "Check whether the column contains missing values"
    })

    # --------------------------------------------------------
    # UNIQUE IDENTIFIER
    # --------------------------------------------------------

    if semantic_type == "Unique Identifier":

        rules.append({
            "column": column,
            "rule": "duplicate_value_check",
            "description": "Check whether unique identifier contains duplicates"
        })

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    elif semantic_type == "Name":

        rules.append({
            "column": column,
            "rule": "whitespace_check",
            "description": "Check whether names contain leading or trailing whitespace"
        })

    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    elif semantic_type == "Gender":

        rules.append({
            "column": column,
            "rule": "gender_validation_check",
            "description": "Validate gender values against allowed business values"
        })

    # --------------------------------------------------------
    # CATEGORICAL
    # --------------------------------------------------------

    elif semantic_type == "Categorical":

        rules.append({
            "column": column,
            "rule": "category_consistency_check",
            "description": "Check for inconsistent categorical values"
        })

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    elif semantic_type == "Date":

        rules.append({
            "column": column,
            "rule": "invalid_date_check",
            "description": "Check whether date values are valid"
        })

        rules.append({
            "column": column,
            "rule": "future_date_check",
            "description": "Check whether dates are in the future"
        })

    # --------------------------------------------------------
    # NUMERIC MEASURE
    # --------------------------------------------------------

    elif semantic_type == "Numeric Measure":

        rules.append({
            "column": column,
            "rule": "outlier_check",
            "description": "Check for statistical outliers using IQR"
        })

        rules.append({
            "column": column,
            "rule": "range_check",
            "description": "Check whether numeric values contain invalid negative values"
        })

    return rules


# ============================================================
# 2. GENERATE RULES FOR COMPLETE DATASET
# ============================================================

def generate_validation_rules(
    df,
    semantic_profile
):
    """
    Generate validation rules dynamically for the
    complete dataset.
    """

    all_rules = []

    for item in semantic_profile:

        column = item["column"]
        data_type = item["data_type"]
        semantic_type = item["semantic_type"]

        column_rules = generate_rules_for_column(
            df,
            column,
            data_type,
            semantic_type
        )

        all_rules.extend(column_rules)

    return all_rules


# ============================================================
# 3. GET RULE NAMES
# ============================================================

def get_rule_names(rules):
    """
    Return unique validation rule names.
    """

    return list(
        dict.fromkeys(
            rule["rule"]
            for rule in rules
        )
    )


# ============================================================
# 4. DISPLAY RULES
# ============================================================

def display_rules(rules):
    """
    Display generated validation rules.
    """

    print("\n" + "=" * 70)
    print("GENERATED VALIDATION RULES")
    print("=" * 70)

    for rule in rules:

        print(
            f"{rule['column']} "
            f"-> {rule['rule']} "
            f"-> {rule['description']}"
        )


# ============================================================
# END OF rule_engine.py
# ============================================================