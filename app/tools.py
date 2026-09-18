from dataclasses import dataclass


@dataclass(frozen=True)
class ToolRequest:
    principal: str
    action: str
    resource: str


def check_port(host: str, port: int) -> str:
    """
    Diagnostic operation.

    This function performs the diagnostic operation.
    Authorization is handled before this function is called.
    """
    return f"Port check requested for {host}:{port}"


def execute_tool(request: ToolRequest, host: str, port: int) -> str:
    from app.authorization import authorize

    if request.action != "check_port":
        if request.principal == "fixtrace-agent":
            return "DENIED: unsupported diagnostic action."

        return "DENIED: diagnostic action is not authorized."

    if not authorize(request):
        return "DENIED: diagnostic action is not authorized."

    return check_port(host, port)