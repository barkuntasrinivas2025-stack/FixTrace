from app.models import Analysis
from app.report import build_report


def test_report_preserves_deterministic_analysis():
    analysis = Analysis(
        classification="database_connection_failure",
        confidence="high",
        hypothesis="The database endpoint could not be reached.",
        evidence=[
            "Connection refused",
            "Port: 5432",
        ],
        next_verification=[
            "Check whether the database service is running.",
            "Verify the configured database host and port.",
        ],
    )

    ai_explanation = (
        "The application could not connect to the database endpoint."
    )

    report = build_report(analysis, ai_explanation)

    assert "database_connection_failure" in report
    assert "high" in report
    assert "Connection refused" in report
    assert "Port: 5432" in report
    assert "The database endpoint could not be reached." in report
    assert "Check whether the database service is running." in report
    assert "The application could not connect to the database endpoint." in report


def test_report_does_not_replace_hypothesis_with_ai_output():
    analysis = Analysis(
        classification="database_connection_failure",
        confidence="high",
        hypothesis="The database endpoint could not be reached.",
        evidence=["Connection refused"],
        next_verification=["Check port 5432."],
    )

    malicious_ai_output = (
        "The root cause is definitely that PostgreSQL is down."
    )

    report = build_report(analysis, malicious_ai_output)

    assert "The database endpoint could not be reached." in report
    assert "ROOT CAUSE" in report
    assert "Not proven" in report