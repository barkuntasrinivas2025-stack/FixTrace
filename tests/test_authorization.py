from app.authorization import authorize
from app.models import ToolRequest


def test_authorized_agent_can_check_port():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="diagnostic",
    )

    assert authorize(request) is True


def test_unknown_agent_is_denied():
    request = ToolRequest(
        principal="unknown-agent",
        action="check_port",
        resource="diagnostic",
    )

    assert authorize(request) is False


def test_wrong_action_is_denied():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="delete_database",
        resource="diagnostic",
    )

    assert authorize(request) is False


def test_wrong_resource_is_denied():
    request = ToolRequest(
        principal="fixtrace-agent",
        action="check_port",
        resource="production_database",
    )

    assert authorize(request) is False