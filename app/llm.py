from abc import ABC, abstractmethod
import json
import urllib.request

from app.models import Analysis


class LLMProvider(ABC):
    """Interface for FixTrace language model providers."""

    @abstractmethod
    def explain(self, analysis: Analysis) -> str:
        """Generate a developer-facing explanation."""
        raise NotImplementedError


class LocalLLMProvider(LLMProvider):
    """Local Ollama provider used only for explanation."""

    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def explain(self, analysis: Analysis) -> str:
        # Only these fields are allowed to reach the LLM.
        llm_input = {
            "classification": analysis.classification,
            "hypothesis": analysis.hypothesis,
        }

        prompt = f"""
You are the explanation component of FixTrace.

Your ONLY job is to rewrite the supplied hypothesis
into a short, clear explanation for a software developer.

STRICT RULES:
- Use ONLY the supplied classification and hypothesis.
- Do not add facts.
- Do not add evidence.
- Do not add causes.
- Do not add troubleshooting steps.
- Do not add recommendations.
- Do not add technologies.
- Do not use outside knowledge.
- Do not strengthen the hypothesis.
- Do not weaken the hypothesis.
- Do not turn a hypothesis into a confirmed fact.
- Return only 1-2 sentences.
- Do not use bullets, headings, or lists.

INPUT:
{json.dumps(llm_input, indent=2)}
"""

        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
            },
        }).encode("utf-8")

        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["response"].strip()