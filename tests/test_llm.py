from app.llm import LocalLLMProvider
from app.models import Analysis


class FakeProvider(LocalLLMProvider):
    """Test provider that captures what would be sent to the LLM."""

    def explain(self, analysis: Analysis) -> str:
        llm_input = {
            "classification": analysis.classification,
            "hypothesis": analysis.hypothesis,
        }

        return str(llm_input)


def test_llm_receives_only_allowed_fields():
    analysis = Analysis(
        classification="database_connection_failure",
        confidence="high",
        hypothesis="The database endpoint could not be reached.",
        evidence=["SECRET EVIDENCE"],
        next_verification=["SECRET VERIFICATION"],
    )

    output = FakeProvider().explain(analysis)

    assert "database_connection_failure" in output
    assert "database endpoint could not be reached" in output

    assert "SECRET EVIDENCE" not in output
    assert "SECRET VERIFICATION" not in output