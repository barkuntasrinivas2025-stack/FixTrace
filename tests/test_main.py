from app.main import diagnose_port, run


def test_diagnose_port_reachable():
    analysis = diagnose_port("localhost", 5432)

    assert analysis.classification == "database_connection_failure"
    assert analysis.confidence == "high"
    assert "configured database endpoint" in analysis.hypothesis.lower()
def test_run_builds_complete_report(tmp_path, monkeypatch):
    log_file = tmp_path / "failure.log"

    log_file.write_text(
        "ERROR OrderService - API request failed\n"
        "Status: 401\n"
    )

    monkeypatch.setattr(
        "app.main.explain_with_agent",
        lambda analysis: "Mocked AI explanation.",
    )

    report = run(str(log_file))

    assert "http_api_failure" in report
    assert "high" in report
    assert "HTTP status: 401" in report
    assert "The application received an unsuccessful HTTP response" in report
    assert "Mocked AI explanation." in report
    assert "ROOT CAUSE" in report
    assert "Not proven" in report