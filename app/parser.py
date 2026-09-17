import re

from app.models import Failure


def parse_log(log: str) -> Failure:
    error_match = re.search(
        r"ERROR\s+([A-Za-z0-9_-]+)\s*-\s*(.+)",
        log,
    )

    component = error_match.group(1) if error_match else None
    error_message = error_match.group(2) if error_match else "Unknown error"

    evidence = []

    if re.search(r"Connection refused", log, re.IGNORECASE):
        evidence.append("Connection refused")

    port_match = re.search(r"Port:\s*(\d+)", log, re.IGNORECASE)
    if port_match:
        evidence.append(f"Port: {port_match.group(1)}")

    if re.search(r"SQLException|ConnectException", log):
        evidence.append("Database/network exception detected")

    if "5432" in log:
        failure_type = "database_connection"
    else:
        failure_type = "unknown"

    return Failure(
        failure_type=failure_type,
        component=component,
        error_message=error_message,
        evidence=evidence,
    )