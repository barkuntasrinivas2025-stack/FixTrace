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