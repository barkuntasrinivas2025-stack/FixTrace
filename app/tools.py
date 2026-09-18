import socket
from dataclasses import dataclass
from app.models import DiagnosticResult

@dataclass(frozen=True)
class ToolRequest:
    principal: str
    action: str
    resource: str


def check_port(host: str, port: int) -> DiagnosticResult:
    """
    Diagnostic operation.

    This function performs the diagnostic operation.
    Authorization is handled before this function is called.
    """
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
def execute_tool(request: ToolRequest, host: str, port: int) -> str:
    from app.authorization import authorize

    if request.action != "check_port":
        if request.principal == "fixtrace-agent":
            return "DENIED: unsupported diagnostic action."

        return "DENIED: diagnostic action is not authorized."

    if not authorize(request):
        return "DENIED: diagnostic action is not authorized."

    return check_port(host, port)