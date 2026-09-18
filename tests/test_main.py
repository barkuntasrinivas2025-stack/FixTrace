from app.main import diagnose_port, run


def test_diagnose_port_requires_authorization(monkeypatch):
    def deny(_request):
        return False

    def should_not_execute(*args, **kwargs):
        raise AssertionError(
            "check_port must not execute when authorization is denied"
        )

    monkeypatch.setattr("app.tools.authorize", deny)
    monkeypatch.setattr("app.tools.check_port", should_not_execute)

    try:
        diagnose_port("localhost", 5432)
        assert False, "diagnose_port should reject unauthorized tool execution"
    except PermissionError as exc:
        assert "DENIED" in str(exc)


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

def test_diagnose_port_propagates_invalid_port():
    try:
        diagnose_port("localhost", 0)
        assert False, "diagnose_port should reject invalid ports"
    except ValueError as exc:
        assert "port" in str(exc).lower()


def test_diagnose_port_converts_unexpected_tool_result_to_permission_error(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.main.execute_tool",
        lambda request, host, port: "DENIED: test denial",
    )

    try:
        diagnose_port("localhost", 5432)
        assert False, "diagnose_port should reject non-diagnostic results"
    except PermissionError as exc:
        assert "DENIED: test denial" in str(exc)