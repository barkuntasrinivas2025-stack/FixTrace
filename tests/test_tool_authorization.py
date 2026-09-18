import socket
from app.models import DiagnosticResult,ToolRequest
from app.tools import execute_tool


def test_authorized_request_executes_tool():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    host, port = server.getsockname()

    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="diagnostic",
    )

    try:
        result = execute_tool(request, host, port)

        assert result.host == host
        assert result.port == port
        assert result.reachable is True
        assert result.message == f"Port {port} on {host} is reachable."
        assert isinstance(result, DiagnosticResult)
    finally:
        server.close()


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

def test_authorization_failure_never_executes_tool(monkeypatch):
    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="diagnostic",
    )

    monkeypatch.setattr("app.tools.authorize", lambda request: False)

    def should_not_execute(*args, **kwargs):
        raise AssertionError("check_port must not execute")

    monkeypatch.setattr("app.tools.check_port", should_not_execute)

    result = execute_tool(request, "localhost", 5432)

    assert result == "DENIED: diagnostic action is not authorized."
