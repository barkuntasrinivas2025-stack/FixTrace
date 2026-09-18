from app.tools import ToolRequest


def authorize(request: ToolRequest) -> bool:
    return (
        request.principal == "fixtrace-agent"
        and request.action == "check_port"
        and request.resource == "diagnostic"
    )