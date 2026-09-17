import json

from strands import Agent
from strands.models import OllamaModel

from app.models import Analysis


SYSTEM_PROMPT = """
You are the explanation component of FixTrace.

Your ONLY job is to rewrite the supplied hypothesis
into a short, clear explanation for a software developer.

Rules:
- Use only the supplied classification and hypothesis.
- Do not add facts.
- Do not add evidence.
- Do not add causes.
- Do not add troubleshooting steps.
- Do not add recommendations.
- Do not use outside knowledge.
- Do not strengthen or weaken the hypothesis.
- Do not present a hypothesis as a confirmed root cause.
- Return only 1-2 concise sentences.
"""


def build_agent_prompt(analysis: Analysis) -> str:
    """Build the only data allowed to cross into the LLM."""
    allowed_input = {
        "classification": analysis.classification,
        "hypothesis": analysis.hypothesis,
    }

    return (
        "Explain the following FixTrace analysis without adding information:\n\n"
        f"{json.dumps(allowed_input, indent=2)}"
    )


def create_agent() -> Agent:
    model = OllamaModel(
        host="http://localhost:11434",
        model_id="qwen2.5:1.5b",
        temperature=0,
    )

    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )


def explain_with_agent(analysis: Analysis) -> str:
    """Generate only the non-authoritative AI explanation."""
    agent = create_agent()
    prompt = build_agent_prompt(analysis)
    result = agent(prompt)

    return str(result).strip()