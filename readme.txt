# 🤖 AI Data Quality Agent

An intelligent and dynamic data quality analysis application built using Python and Streamlit.

The application allows users to upload CSV or Excel datasets and automatically performs data profiling, semantic analysis, validation, aggregation, issue detection, and data quality assessment.

---

## 🚀 Features

### 📁 Dataset Upload
- Upload CSV files
- Upload Excel files (`.xlsx`)
- Automatically reads the uploaded dataset

### 📊 Dataset Profiling
Automatically identifies:

- Data types
- Semantic types
- Numeric columns
- Categorical columns
- Date columns
- Identifier columns
- Missing values
- Empty columns
- Outliers

### 🧠 Semantic Type Detection

The system dynamically identifies columns such as:

- Unique Identifier
- Reference Identifier
- Name
- Gender
- Categorical
- Date
- Numeric Measure
- Boolean
- Text

### ⚙️ Dynamic Validation Rules

Validation rules are generated according to the detected semantic type.

Examples:

- Missing value check
- Duplicate identifier check
- Whitespace check
- Gender validation
- Category consistency check
- Invalid date check
- Future date check
- Outlier check
- Numeric range check

### 📈 Aggregation Explorer

Select any column and view relevant statistics.

For numeric columns:

- Sum
- Mean
- Median
- Minimum
- Maximum
- Standard Deviation
- Q1
- Q3
- IQR

For Boolean columns:

- True Count
- False Count
- True Percentage
- False Percentage

For categorical/text columns:

- Top Value
- Top Value Count
- Top Value Percentage

For date columns:

- Minimum Date
- Maximum Date

### ⚠️ Issue Detection

The application identifies failed validation rules and provides:

- Column
- Validation rule
- Severity
- Failed count
- Affected percentage
- Finding
- Root cause
- Business impact
- Recommendation

### 📊 Data Quality Score

The system calculates an overall data quality score based on detected errors.

The application displays:

- Quality Score
- Total Errors
- Error Percentage
- Total Issues

### 🤖 AI Analysis

The project also includes an AI analysis module using local Ollama.

The AI component can analyze detected data quality issues and generate:

- AI explanation
- AI root cause
- AI business impact
- AI recommendation
- AI priority

> Note: The current Streamlit deployment version is designed to run the data quality analysis independently. Local Ollama running on a personal computer cannot be accessed directly by a cloud-hosted Streamlit application.

---

## 🏗️ Project Architecture

```text
CSV / Excel Dataset
        ↓
Dataset Upload
        ↓
Dynamic Data Profiler
        ↓
Semantic Type Detection
        ↓
Dynamic Rule Generation
        ↓
Validation Engine
        ↓
Data Quality Results
        ↓
Issue Analyzer
        ↓
Severity / Root Cause / Impact / Recommendation
        ↓
Streamlit Dashboard