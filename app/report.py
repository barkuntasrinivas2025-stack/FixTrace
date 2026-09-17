from app.models import Analysis


def build_report(analysis: Analysis, explanation: str) -> str:
    evidence = "\n".join(
        f"• {item}" for item in analysis.evidence
    )

    verification = "\n".join(
        f"• {item}" for item in analysis.next_verification
    )

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           FIXTRACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FAILURE
{analysis.classification}

CONFIDENCE
{analysis.confidence}

EVIDENCE
{evidence}

HYPOTHESIS
{analysis.hypothesis}

AI EXPLANATION
{explanation}

NEXT VERIFICATION
{verification}

⚠ ROOT CAUSE
Not proven — verification required.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()