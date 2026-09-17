from pathlib import Path

from app.parser import parse_log
from app.rules import analyze_failure


def test_database_connection_failure():
    log = Path("examples/database_error.log").read_text()
    failure = parse_log(log)

    assert failure.failure_type == "database_connection"
    assert failure.component == "PaymentService"
    assert "Connection refused" in failure.evidence
    assert "Port: 5432" in failure.evidence


def test_database_connection_analysis():
    log = Path("examples/database_error.log").read_text()
    failure = parse_log(log)
    analysis = analyze_failure(failure)

    assert analysis.classification == "database_connection_failure"
    assert analysis.confidence == "high"
    assert "database endpoint" in analysis.hypothesis
    assert len(analysis.next_verification) >= 2
def test_http_api_failure():
    log = """
2026-09-17 15:10:22 ERROR OrderService - API request failed
java.net.HttpRetryException: cannot retry due to server authentication, status code: 401
Method: POST
Endpoint: /api/orders
Status: 401
"""
    failure = parse_log(log)

    assert failure.failure_type == "http_api_failure"
    assert failure.component == "OrderService"
    assert "HTTP status: 401" in failure.evidence
    assert "HTTP exception detected" in failure.evidence
def test_gradle_build_failure():
    log = Path("examples/gradle_error.log").read_text()
    failure = parse_log(log)

    assert failure.failure_type == "build_failure"
    assert failure.component == "Gradle"
    assert "Kotlin unresolved reference detected" in failure.evidence