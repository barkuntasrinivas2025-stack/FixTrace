from pathlib import Path

from app.agent import explain_with_agent
# from app.llm import LocalLLMProvider
from app.parser import parse_log
from app.report import build_report
from app.rules import analyze_failure


def run(log_path: str) -> str:
    # 1. Read raw log
    log = Path(log_path).read_text()

    # 2. Parse deterministic facts
    failure = parse_log(log)

    # 3. Deterministic analysis
    analysis = analyze_failure(failure)

    # 4. AI explanation only
    # llm = LocalLLMProvider()
    explanation = explain_with_agent(analysis)

    # 5. Build authoritative report
    return build_report(analysis, explanation)


if __name__ == "__main__":
    report = run("examples/database_error.log")
    print(report)