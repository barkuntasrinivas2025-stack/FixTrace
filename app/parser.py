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
    status_match = re.search(r"Status:\s*(\d{3})", log, re.IGNORECASE)
    status_code = status_match.group(1) if status_match else None

    if status_code:
        evidence.append(f"HTTP status: {status_code}")

    if re.search(r"HttpRetryException|HTTP request failed", log, re.IGNORECASE):
        evidence.append("HTTP exception detected")

    if re.search(r"Connection refused", log, re.IGNORECASE):
        evidence.append("Connection refused")

    port_match = re.search(r"Port:\s*(\d+)", log, re.IGNORECASE)
    if port_match:
        evidence.append(f"Port: {port_match.group(1)}")

    if re.search(r"SQLException|ConnectException", log):
        evidence.append("Database/network exception detected")
    if re.search(r"Unresolved reference", log, re.IGNORECASE):
        evidence.append("Kotlin unresolved reference detected")

    has_database_signal = re.search(
        r"SQLException|ConnectException|Connection refused|database\s+connection",
        log,
        re.IGNORECASE,
    )

    if status_code:
        failure_type = "http_api_failure"
    elif has_database_signal:
        failure_type = "database_connection"
    elif re.search(r"Unresolved reference", log, re.IGNORECASE):
        failure_type = "build_failure"
    else:
        failure_type = "unknown"

    return Failure(
        failure_type=failure_type,
        component=component,
        error_message=error_message,
        evidence=evidence,
    )