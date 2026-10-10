import json
import urllib.request
import urllib.error


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"


# ============================================================
# CREATE ISSUE PROMPT
# ============================================================

def create_issue_prompt(issue):

    prompt = f"""
You are an AI Data Quality Analyst.

Analyze the following data quality issue.

Column:
{issue['column']}

Validation Rule:
{issue['rule']}

Severity:
{issue['severity']}

Failed Records:
{issue['failed_count']}

Affected Percentage:
{issue['affected_percentage']}%

Finding:
{issue['finding']}

Current Root Cause:
{issue['root_cause']}

Current Business Impact:
{issue['business_impact']}

Current Recommendation:
{issue['recommendation']}

Your task is to provide a concise business-oriented analysis.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "ai_explanation": "",
    "ai_root_cause": "",
    "ai_business_impact": "",
    "ai_recommendation": "",
    "ai_priority": ""
}}

Rules for ai_priority:

HIGH
MEDIUM
LOW

Do not invent data values.
Use only the information provided above.
"""


    return prompt


# ============================================================
# CALL LOCAL OLLAMA
# ============================================================

def call_ollama(prompt):

    request_data = {

        "model": OLLAMA_MODEL,

        "prompt": prompt,

        "stream": False,

        "format": "json",

        "options": {
            "temperature": 0.2
        }
    }

    request_body = json.dumps(
        request_data
    ).encode("utf-8")


    request = urllib.request.Request(

        OLLAMA_URL,

        data=request_body,

        headers={
            "Content-Type": "application/json"
        },

        method="POST"
    )


    try:

        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            response_data = response.read().decode(
                "utf-8"
            )

        response_json = json.loads(
            response_data
        )

        return response_json.get(
            "response",
            ""
        )


    except urllib.error.URLError as error:

        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running on your computer.\n"
            f"Details: {error}"
        )


    except Exception as error:

        raise RuntimeError(
            f"Ollama request failed: {error}"
        )


# ============================================================
# ANALYZE ONE ISSUE
# ============================================================

def analyze_issue_with_ai(issue):

    prompt = create_issue_prompt(
        issue
    )


    response_text = call_ollama(
        prompt
    )


    try:

        ai_result = json.loads(
            response_text
        )


    except json.JSONDecodeError:

        ai_result = {

            "ai_explanation": response_text,

            "ai_root_cause": "",

            "ai_business_impact": "",

            "ai_recommendation": "",

            "ai_priority": issue["severity"]
        }


    # --------------------------------------------------------
    # Ensure all expected fields exist
    # --------------------------------------------------------

    ai_result.setdefault(
        "ai_explanation",
        ""
    )

    ai_result.setdefault(
        "ai_root_cause",
        ""
    )

    ai_result.setdefault(
        "ai_business_impact",
        ""
    )

    ai_result.setdefault(
        "ai_recommendation",
        ""
    )

    ai_result.setdefault(
        "ai_priority",
        issue["severity"]
    )


    # --------------------------------------------------------
    # Validate AI priority
    # --------------------------------------------------------

    valid_priorities = {
        "HIGH",
        "MEDIUM",
        "LOW"
    }


    ai_priority = str(
        ai_result["ai_priority"]
    ).upper().strip()


    if ai_priority not in valid_priorities:

        ai_priority = issue["severity"]


    ai_result["ai_priority"] = ai_priority


    return ai_result


# ============================================================
# ANALYZE ALL ISSUES
# ============================================================

def analyze_issues_with_ai(
    issues
):

    analyzed_issues = []


    if not issues:

        return analyzed_issues


    print("\nConnecting to local Ollama AI...")

    print(
        f"Model: {OLLAMA_MODEL}"
    )


    for issue in issues:

        print(
            f"\nAI analyzing: "
            f"{issue['column']} "
            f"-> "
            f"{issue['rule']}"
        )


        ai_result = analyze_issue_with_ai(
            issue
        )


        combined_issue = {

            **issue,

            **ai_result
        }


        analyzed_issues.append(
            combined_issue
        )


    return analyzed_issues


# ============================================================
# DISPLAY AI ANALYSIS
# ============================================================

def display_ai_analysis(
    analyzed_issues
):

    print("\n" + "=" * 70)

    print(
        "AI DATA QUALITY ANALYSIS"
    )

    print("=" * 70)


    if not analyzed_issues:

        print(
            "No issues were found for AI analysis."
        )

        return


    for issue in analyzed_issues:

        print(
            f"\nColumn: "
            f"{issue['column']}"
        )


        print(
            f"Rule: "
            f"{issue['rule']}"
        )


        print(
            f"AI Priority: "
            f"{issue['ai_priority']}"
        )


        print(
            "\nAI Explanation:"
        )

        print(
            issue["ai_explanation"]
        )


        print(
            "\nAI Root Cause:"
        )

        print(
            issue["ai_root_cause"]
        )


        print(
            "\nAI Business Impact:"
        )

        print(
            issue["ai_business_impact"]
        )


        print(
            "\nAI Recommendation:"
        )

        print(
            issue["ai_recommendation"]
        )


# ============================================================
# END OF ai_analyzer.py
# ============================================================