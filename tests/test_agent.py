from app.agent import build_agent_prompt
from app.models import Analysis


def test_agent_prompt_contains_only_allowed_fields():
    analysis = Analysis(
        classification="database_connection_failure",
        confidence="high",
        hypothesis="The database endpoint could not be reached.",
        evidence=["SECRET EVIDENCE"],
        next_verification=["SECRET VERIFICATION"],
    )

    prompt = build_agent_prompt(analysis)

    assert "database_connection_failure" in prompt
    assert "The database endpoint could not be reached." in prompt

    assert "high" not in prompt
    assert "SECRET EVIDENCE" not in prompt
    assert "SECRET VERIFICATION" not in prompt