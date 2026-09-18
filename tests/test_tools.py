import socket

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
        assert result == f"Port {port} on {host} is reachable."
    finally:
        server.close()