from app.models import Failure,DiagnosticResult
from app.rules import analyze_failure,classify_diagnostic


def test_http_api_failure_analysis():
    failure = Failure(
        failure_type="http_api_failure",
        component="OrderService",
        error_message="API request failed",
        evidence=["HTTP status: 401"],
    )

    analysis = analyze_failure(failure)

    assert analysis.classification == "http_api_failure"
    assert analysis.confidence == "high"
    assert "unsuccessful HTTP response" in analysis.hypothesis
    assert "HTTP status: 401" in analysis.evidence
    assert len(analysis.next_verification) >= 2

def test_build_failure_analysis():
    failure = Failure(
        failure_type="build_failure",
        component="Gradle",
        error_message="Build failed",
        evidence=["Kotlin unresolved reference detected"],
    )

    analysis = analyze_failure(failure)

    assert analysis.classification == "build_failure"
    assert analysis.confidence == "high"
    assert "unresolved reference" in analysis.hypothesis
    assert "Kotlin unresolved reference detected" in analysis.evidence
    assert len(analysis.next_verification) >= 2
def test_classify_unreachable_port():
    result = DiagnosticResult(
        host="localhost",
        port=5432,
        reachable=False,
        message="Port 5432 on localhost is unreachable.",
    )

    failure = classify_diagnostic(result)

    assert failure.failure_type == "database_connection"
    assert failure.component == "localhost:5432"
    assert failure.error_message == "Port 5432 on localhost is unreachable."
    assert failure.evidence == [
        "Port 5432 on localhost is unreachable."
    ]
def test_classify_unreachable_port():
    result = DiagnosticResult(
        host="localhost",
        port=5432,
        reachable=False,
        message="Port 5432 on localhost is unreachable.",
    )

    failure = classify_diagnostic(result)

    assert failure.failure_type == "database_connection"
    assert failure.component == "localhost:5432"
    assert failure.error_message == "Port 5432 on localhost is unreachable."
    assert failure.evidence == [
        "Port 5432 on localhost is unreachable."
    ]
def test_classify_reachable_port():
    result = DiagnosticResult(
        host="localhost",
        port=5432,
        reachable=True,
        message="Port 5432 on localhost is reachable.",
    )

    failure = classify_diagnostic(result)

    assert failure.failure_type == "database_connection"
    assert failure.component == "localhost:5432"
    assert failure.error_message == "Port 5432 on localhost is reachable."
    assert failure.evidence == [
        "Port 5432 on localhost is reachable."
    ]