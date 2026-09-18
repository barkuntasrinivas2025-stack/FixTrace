import socket
from app.models import DiagnosticResult

from app.tools import ToolRequest, check_port


def test_tool_request():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="localhost:5432",
    )

    assert request.principal == "fixtrace-agent"
    assert request.action == "check_port"
    assert request.resource == "localhost:5432"


def test_check_port_detects_reachable_port():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)

    host, port = server.getsockname()

    try:
        result = check_port(host, port)

        assert result.host == host
        assert result.port == port
        assert result.reachable is True
        assert result.message == f"Port {port} on {host} is reachable."
    finally:
        server.close()
def test_check_port_detects_unreachable_port():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))

    host, port = server.getsockname()
    server.close()

    result = check_port(host, port)

    assert result.host == host
    assert result.port == port
    assert result.reachable is False
    assert result.message == f"Port {port} on {host} is unreachable."

def test_DiagnosticResult():
    result = DiagnosticResult(
        host="127.0.0.1",
        port=5432,
        reachable=True,
        message="Port 5432 on 127.0.0.1 is reachable.",
    )

    assert result.host == "127.0.0.1"
    assert result.port == 5432
    assert result.reachable is True
    assert result.message == "Port 5432 on 127.0.0.1 is reachable."
