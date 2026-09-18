from pathlib import Path

from app.agent import explain_with_agent
from app.parser import parse_log
from app.report import build_report
from app.rules import analyze_failure, classify_diagnostic
from app.tools import check_port
from app.models import Analysis

def diagnose_port(host: str, port: int) -> Analysis:
    result = check_port(host, port)
    failure = classify_diagnostic(result)
    return analyze_failure(failure)

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
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m app.main <log_file>")
        raise SystemExit(1)

    report = run(sys.argv[1])
    print(report)