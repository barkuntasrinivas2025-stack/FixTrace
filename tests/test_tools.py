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


def test_check_port_is_a_diagnostic_operation():
    result = check_port("localhost", 5432)

    assert result == "Port check requested for localhost:5432"