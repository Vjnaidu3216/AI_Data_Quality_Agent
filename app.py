import streamlit as st
import pandas as pd

from profiler import (
    profile_dataset,
    detect_semantic_types,
    analyze_numeric_columns,
    analyze_missing_values,
    analyze_empty_columns,
    analyze_categorical_columns,
    analyze_outliers,
)

from rule_engine import generate_validation_rules

from validation_engine import (
    validate_dataset,
    generate_quality_summary,
)

from issue_analyzer import analyze_all_issues


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Data Quality Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# THEME (colors live here so they are easy to change)
# =========================================================

INK = "#0F2A43"        # headings, hero background
TEAL = "#0E9AA7"       # primary accent
TEAL_SOFT = "#E3F4F6"  # light accent background
PAGE_BG = "#F5F9FB"    # page background
PASS = "#1E9E6A"       # good / passed
WARN = "#E8A317"       # needs attention
FAIL = "#D64545"       # failed / error

st.markdown(
    f"""
    <style>
    .stApp {{ background: {PAGE_BG}; }}
    [data-testid="stHeader"] {{ background: transparent; }}

    /* ---------- Hero banner ---------- */
    .hero {{
        background: linear-gradient(120deg, {INK} 0%, #174A6B 60%, {TEAL} 100%);
        border-radius: 18px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.2rem;
        color: #ffffff;
    }}
    .hero h1 {{ color: #ffffff; margin: 0 0 .35rem 0; font-size: 2.2rem; }}
    .hero p  {{ color: #D5E8F0; margin: 0; font-size: 1.05rem; }}

    /* ---------- Metric cards ---------- */
    [data-testid="stMetric"] {{
        background: #ffffff;
        border: 1px solid #DCE8EE;
        border-left: 5px solid {TEAL};
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(15, 42, 67, .06);
    }}
    [data-testid="stMetricLabel"] p {{ color: #5B7184 !important; font-weight: 600; }}
    [data-testid="stMetricValue"]   {{ color: {INK} !important; }}

    /* ---------- Score card ---------- */
    .score-card {{
        background: #ffffff;
        border: 1px solid #DCE8EE;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        height: 100%;
    }}
    .score-card .label {{ color: #5B7184; font-weight: 600; margin-bottom: .2rem; }}
    .score-card .value {{ font-size: 3rem; font-weight: 800; line-height: 1.1; }}
    .score-card .verdict {{ color: {INK}; margin-top: .3rem; }}
    .bar-track {{
        background: #E6EEF3; border-radius: 999px; height: 12px;
        margin-top: .8rem; overflow: hidden;
    }}
    .bar-fill {{ height: 100%; border-radius: 999px; }}

    /* ---------- Section headings ---------- */
    h2, h3 {{ color: {INK}; }}

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {{ gap: 6px; }}
    .stTabs [data-baseweb="tab"] {{
        background: #ffffff;
        border: 1px solid #DCE8EE;
        border-radius: 10px 10px 0 0;
        padding: 8px 16px;
        color: #38566D;
    }}
    .stTabs [aria-selected="true"] {{
        background: {TEAL_SOFT};
        border-bottom: 3px solid {TEAL};
        color: {INK};
        font-weight: 700;
    }}

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {{ background: {INK}; }}
    [data-testid="stSidebar"] * {{ color: #E8F2F7; }}
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{ color: {INK}; }}
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{ background: #ffffff; }}

    /* ---------- Buttons ---------- */
    .stDownloadButton button {{
        background: {TEAL}; color: #ffffff; border: none; border-radius: 10px;
        font-weight: 600;
    }}
    .stDownloadButton button:hover {{ background: #0B7F8A; color: #ffffff; }}

    /* ---------- Welcome cards ---------- */
    .step-card {{
        background: #ffffff; border: 1px solid #DCE8EE; border-radius: 14px;
        padding: 1.1rem 1.2rem; height: 100%;
    }}
    .step-card h4 {{ color: {INK}; margin: 0 0 .3rem 0; }}
    .step-card p  {{ color: #5B7184; margin: 0; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def get_column_aggregations(df, column):
    series = df[column]

    result = {
        "Data Type": str(series.dtype),
        "Total Count": int(series.count()),
        "Missing Count": int(series.isna().sum()),
        "Unique Values": int(series.nunique(dropna=True)),
    }

    # Boolean columns
    if pd.api.types.is_bool_dtype(series):
        true_count = int(series.sum())
        false_count = int(series.notna().sum() - true_count)
        non_null_count = int(series.notna().sum())

        result["True Count"] = true_count
        result["False Count"] = false_count

        if non_null_count > 0:
            result["True %"] = round((true_count / non_null_count) * 100, 2)
            result["False %"] = round((false_count / non_null_count) * 100, 2)

        return result

    # Numeric columns
    if pd.api.types.is_numeric_dtype(series):
        numeric_series = pd.to_numeric(series, errors="coerce").dropna()

        if not numeric_series.empty:
            q1 = numeric_series.quantile(0.25)
            q3 = numeric_series.quantile(0.75)

            result["Sum"] = round(numeric_series.sum(), 2)
            result["Mean"] = round(numeric_series.mean(), 2)
            result["Median"] = round(numeric_series.median(), 2)
            result["Minimum"] = round(numeric_series.min(), 2)
            result["Maximum"] = round(numeric_series.max(), 2)
            result["Standard Deviation"] = round(numeric_series.std(), 2)
            result["Q1"] = round(q1, 2)
            result["Q3"] = round(q3, 2)
            result["IQR"] = round(q3 - q1, 2)

        return result

    # Date columns
    if pd.api.types.is_datetime64_any_dtype(series):
        date_series = pd.to_datetime(series, errors="coerce").dropna()

        if not date_series.empty:
            result["Minimum Date"] = str(date_series.min().date())
            result["Maximum Date"] = str(date_series.max().date())

        return result

    # Categorical / text columns
    non_null_series = series.dropna()

    if not non_null_series.empty:
        value_counts = non_null_series.astype(str).value_counts()

        result["Top Value"] = str(value_counts.index[0])
        result["Top Value Count"] = int(value_counts.iloc[0])
        result["Top Value %"] = round(
            (value_counts.iloc[0] / len(non_null_series)) * 100, 2
        )

    return result


def score_style(score):
    """Return (color, verdict) for a quality score."""
    if score >= 90:
        return PASS, "Excellent. This data is in good shape."
    if score >= 70:
        return WARN, "Fair. A few problems need attention."
    return FAIL, "Poor. This data needs cleaning before use."


def color_status(value):
    """Cell color for PASS / FAIL values."""
    text = str(value).upper()
    if text == "PASS":
        return f"background-color: #DDF3E9; color: {PASS}; font-weight: 700;"
    if text == "FAIL":
        return f"background-color: #FBE3E3; color: {FAIL}; font-weight: 700;"
    return ""


def color_severity(value):
    """Cell color for severity-like values (High / Medium / Low)."""
    text = str(value).lower()
    if text in ("high", "critical"):
        return f"background-color: #FBE3E3; color: {FAIL}; font-weight: 700;"
    if text in ("medium", "moderate"):
        return f"background-color: #FDF1D6; color: #9A6B00; font-weight: 700;"
    if text == "low":
        return f"background-color: #DDF3E9; color: {PASS}; font-weight: 700;"
    return ""


def style_table(table):
    """Apply status and severity colors to any column that has them."""
    styler = table.style
    for col in table.columns:
        name = str(col).lower()
        if name == "status":
            styler = styler.map(color_status, subset=[col])
        elif name in ("severity", "priority", "level"):
            styler = styler.map(color_severity, subset=[col])
    return styler


@st.cache_data(show_spinner=False)
def load_dataset(file_bytes, file_name):
    import io

    buffer = io.BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        return pd.read_csv(buffer)
    return pd.read_excel(buffer)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 📁 Your Dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file",
        type=["csv", "xlsx"],
    )

    st.markdown("---")
    st.markdown("### ⚙️ Display Options")

    preview_rows = st.slider("Rows in preview", 5, 100, 20, step=5)
    show_only_failed = st.toggle("Show only failed checks", value=False)

    st.markdown("---")
    st.caption(
        "The agent profiles your data, creates validation rules, "
        "runs them, and lists every problem it finds."
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🤖 AI Data Quality Agent</h1>
        <p>Upload raw data and find missing values, outliers and invalid
        entries in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# WELCOME SCREEN (before upload)
# =========================================================

if uploaded_file is None:
    st.info("👈 Upload a CSV or Excel file in the sidebar to get started.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="step-card"><h4>🔍 1. Profile</h4>'
            "<p>Detects column types, missing values, outliers and "
            "empty columns.</p></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="step-card"><h4>✅ 2. Validate</h4>'
            "<p>Creates rules automatically and checks every row "
            "against them.</p></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="step-card"><h4>⚠️ 3. Fix</h4>'
            "<p>Shows a quality score and a clear list of the issues "
            "to fix.</p></div>",
            unsafe_allow_html=True,
        )
    st.stop()


# =========================================================
# PROCESS DATASET
# =========================================================

try:
    with st.spinner("Analyzing your data..."):

        df = load_dataset(uploaded_file.getvalue(), uploaded_file.name)

        total_rows = len(df)
        total_columns = len(df.columns)
        total_cells = total_rows * total_columns

        profile = profile_dataset(df)
        semantic_profile = detect_semantic_types(df)

        numeric_analysis = analyze_numeric_columns(df)
        missing_analysis = analyze_missing_values(df)
        empty_columns = analyze_empty_columns(df)
        categorical_analysis = analyze_categorical_columns(df, semantic_profile)
        outlier_analysis = analyze_outliers(df, semantic_profile)

        validation_rules = generate_validation_rules(df, semantic_profile)
        validation_results = validate_dataset(df, validation_rules)

        quality_summary = generate_quality_summary(
            validation_results,
            total_rows=total_rows,
            total_columns=total_columns,
            total_cells=total_cells,
        )

        issues = analyze_all_issues(validation_results, total_rows)

    st.success(f"Loaded **{uploaded_file.name}** and finished the analysis.")

    # -----------------------------------------------------
    # Derived values used by several tabs
    # -----------------------------------------------------

    try:
        quality_score = float(quality_summary["quality_score"])
    except (TypeError, ValueError):
        quality_score = 0.0

    score_color, score_verdict = score_style(quality_score)

    total_issues = sum(
        1 for result in validation_results if result["status"] == "FAIL"
    )

    # =====================================================
    # TABS
    # =====================================================

    tab_overview, tab_explorer, tab_profile, tab_validation, tab_issues, tab_preview = (
        st.tabs(
            [
                "📊 Overview",
                "🧮 Column Explorer",
                "🔍 Profiling",
                "✅ Validation",
                "⚠️ Issues",
                "👀 Data Preview",
            ]
        )
    )

    # -----------------------------------------------------
    # OVERVIEW
    # -----------------------------------------------------

    with tab_overview:

        left, right = st.columns([1, 2])

        with left:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="label">Quality Score</div>
                    <div class="value" style="color:{score_color};">
                        {quality_summary['quality_score']}%
                    </div>
                    <div class="verdict">{score_verdict}</div>
                    <div class="bar-track">
                        <div class="bar-fill"
                             style="width:{max(0, min(quality_score, 100))}%;
                                    background:{score_color};"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            m1, m2, m3 = st.columns(3)
            m1.metric("Rows", f"{total_rows:,}")
            m2.metric("Columns", f"{total_columns:,}")
            m3.metric("Total Cells", f"{total_cells:,}")

            m4, m5, m6 = st.columns(3)
            m4.metric("Total Errors", quality_summary["total_errors"])
            m5.metric("Error Percentage", f"{quality_summary['error_percentage']}%")
            m6.metric("Total Issues", total_issues)

        st.subheader("Missing values by column")

        missing_counts = df.isna().sum()
        missing_counts = missing_counts[missing_counts > 0].sort_values(
            ascending=False
        )

        if missing_counts.empty:
            st.success("No missing values found in any column.")
        else:
            missing_df = pd.DataFrame(
                {
                    "Column": missing_counts.index,
                    "Missing Values": missing_counts.values,
                    "Missing %": (missing_counts.values / max(total_rows, 1) * 100).round(2),
                }
            )

            chart_col, table_col = st.columns([2, 1])

            with chart_col:
                st.bar_chart(
                    missing_df.set_index("Column")["Missing Values"],
                    color=FAIL,
                )
            with table_col:
                st.dataframe(
                    missing_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Missing %": st.column_config.ProgressColumn(
                            "Missing %",
                            min_value=0,
                            max_value=100,
                            format="%.1f%%",
                        )
                    },
                )

    # -----------------------------------------------------
    # COLUMN EXPLORER
    # -----------------------------------------------------

    with tab_explorer:

        st.write("Pick a column to see its statistics.")

        selected_column = st.selectbox("Select a column", df.columns)

        if selected_column:
            aggregation_result = get_column_aggregations(df, selected_column)

            # Quick-glance cards for the first four facts
            keys = list(aggregation_result.keys())[:4]
            cards = st.columns(len(keys))
            for card, key in zip(cards, keys):
                card.metric(key, aggregation_result[key])

            st.subheader(f"Full statistics for: {selected_column}")

            aggregation_df = pd.DataFrame(
                aggregation_result.items(),
                columns=["Aggregation", "Value"],
            )
            aggregation_df["Value"] = aggregation_df["Value"].astype(str)

            st.dataframe(
                aggregation_df,
                use_container_width=True,
                hide_index=True,
            )

            # Distribution chart for the selected column
            series = df[selected_column].dropna()
            if not series.empty:
                st.subheader("Distribution")
                if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series):
                    counts, bins = pd.cut(series, bins=20, retbins=True)
                    hist = counts.value_counts().sort_index()
                    hist.index = [f"{iv.left:.2f}" for iv in hist.index]
                    st.bar_chart(hist, color=TEAL)
                else:
                    top = series.astype(str).value_counts().head(15)
                    st.bar_chart(top, color=TEAL)

    # -----------------------------------------------------
    # PROFILING
    # -----------------------------------------------------

    with tab_profile:

        st.write("Detected type and details for every column.")

        profile_df = pd.DataFrame(semantic_profile)

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True,
        )

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    with tab_validation:

        validation_df = pd.DataFrame(validation_results)

        passed = int((validation_df["status"] == "PASS").sum()) if "status" in validation_df else 0
        failed = int((validation_df["status"] == "FAIL").sum()) if "status" in validation_df else 0

        v1, v2, v3 = st.columns(3)
        v1.metric("Checks run", len(validation_df))
        v2.metric("🟢 Passed", passed)
        v3.metric("🔴 Failed", failed)

        shown_df = validation_df
        if show_only_failed and "status" in validation_df:
            shown_df = validation_df[validation_df["status"] == "FAIL"]

        if shown_df.empty:
            st.success("No failed checks.")
        else:
            st.dataframe(
                style_table(shown_df),
                use_container_width=True,
                hide_index=True,
            )

        st.download_button(
            "⬇️ Download validation results (CSV)",
            data=validation_df.to_csv(index=False).encode("utf-8"),
            file_name="validation_results.csv",
            mime="text/csv",
        )

    # -----------------------------------------------------
    # ISSUES
    # -----------------------------------------------------

    with tab_issues:

        if issues:
            issues_df = pd.DataFrame(issues)

            st.warning(f"{len(issues_df)} issue(s) detected in this dataset.")

            # Optional text filter across every column
            search = st.text_input(
                "Filter issues",
                placeholder="Type a column name or keyword",
            )

            if search:
                mask = issues_df.astype(str).apply(
                    lambda col: col.str.contains(search, case=False, na=False)
                ).any(axis=1)
                issues_df = issues_df[mask]

            st.dataframe(
                style_table(issues_df),
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "⬇️ Download issues (CSV)",
                data=issues_df.to_csv(index=False).encode("utf-8"),
                file_name="detected_issues.csv",
                mime="text/csv",
            )
        else:
            st.success("🎉 No data quality issues detected.")

    # -----------------------------------------------------
    # DATA PREVIEW
    # -----------------------------------------------------

    with tab_preview:

        st.write(f"First {preview_rows} rows of your dataset.")

        st.dataframe(
            df.head(preview_rows),
            use_container_width=True,
            hide_index=True,
        )

except Exception as error:

    st.error(
        "Something went wrong while processing the dataset. "
        "Check that the file is a valid CSV or Excel file."
    )

    st.exception(error)