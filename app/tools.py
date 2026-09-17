from dataclasses import dataclass


@dataclass(frozen=True)
class ToolRequest:
    principal: str
    action: str
    resource: str


def check_port(host: str, port: int) -> str:
    """
    Diagnostic operation.

    The authorization layer must approve this operation
    before it is executed.
    """
    return f"Port check requested for {host}:{port}"