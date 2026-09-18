from app.models import DiagnosticResult,ToolRequest
from app.tools import execute_tool


def test_authorized_request_executes_tool():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="diagnostic",
    )

    result = execute_tool(request, "localhost", 5432)
    assert result.host == "localhost"
    assert result.port == 5432
    assert result.reachable is True
    assert result.message == "Port 5432 on localhost is reachable."
    assert isinstance(result, DiagnosticResult)


def test_unauthorized_request_is_blocked():
    request = ToolRequest(
        principal="unknown-agent",
        action="check_port",
        resource="diagnostic",
    )

    result = execute_tool(request, "localhost", 5432)

    assert result == "DENIED: diagnostic action is not authorized."


def test_unsupported_action_is_blocked():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="delete_database",
        resource="diagnostic",
    )

    result = execute_tool(request, "localhost", 5432)

    assert result == "DENIED: diagnostic action is not authorized."

def test_unauthorized_request_never_executes_tool(monkeypatch):
    request = ToolRequest(
        principal="unknown-agent",
        action="check_port",
        resource="diagnostic",
    )

    def should_not_execute(*args, **kwargs):
        raise AssertionError("check_port must not execute")

    monkeypatch.setattr("app.tools.check_port", should_not_execute)

    result = execute_tool(request, "localhost", 5432)

    assert result == "DENIED: diagnostic action is not authorized."