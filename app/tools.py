import socket

from app.authorization import authorize
from app.models import DiagnosticResult, ToolRequest


def check_port(host: str, port: int) -> DiagnosticResult:
    """
    Low-level diagnostic operation.

    Authorization must happen before this function is called.
    """
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))

        return DiagnosticResult(
            host=host,
            port=port,
            reachable=True,
            message=f"Port {port} on {host} is reachable.",
        )

    except (ConnectionRefusedError, socket.gaierror, socket.timeout):
        return DiagnosticResult(
            host=host,
            port=port,
            reachable=False,
            message=f"Port {port} on {host} is unreachable.",
        )

    finally:
        sock.close()


def execute_tool(request: ToolRequest, host: str, port: int):
    """
    Authorized tool-execution boundary.

    No diagnostic operation is executed until the request
    has been authorized by Cedar.
    """
    if not authorize(request):
        return "DENIED: diagnostic action is not authorized."

    if request.action != "check_port":
        return "DENIED: unsupported diagnostic action."

    return check_port(host, port)