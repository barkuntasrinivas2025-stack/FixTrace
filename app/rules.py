from app.models import Analysis, Failure, DiagnosticResult

def classify_diagnostic(result: DiagnosticResult) -> Failure:
    if not result.reachable:
        return Failure(
            failure_type="database_connection",
            component=f"{result.host}:{result.port}",
            error_message=result.message,
            evidence=[result.message],
        )

    return Failure(
        failure_type="database_connection",
        component=f"{result.host}:{result.port}",
        error_message=result.message,
        evidence=[result.message],
    )

def analyze_failure(failure: Failure) -> Analysis:
    if failure.failure_type == "database_connection":
        return Analysis(
            classification = "database_connection_failure",
            confidence = "high",
            hypothesis = (
                "The application could not establish a connection "
                "to the configured database endpoint."
            ),
            evidence=failure.evidence,
            next_verification= [
                "Check whether the database service is running.",
                "Check whether port 5432 is accepting connections.",
                "Verify the configured database host and port.",
            ],
        )
    if failure.failure_type == "http_api_failure":
        return Analysis(
            classification="http_api_failure",
            confidence="high",
            hypothesis=(
                "The application received an unsuccessful HTTP response "
                "from the requested API endpoint."
            ),
            evidence=failure.evidence,
            next_verification=[
                "Verify the API authentication credentials.",
                "Check whether the request has the required authorization.",
                "Inspect the API response and server logs for the request.",
            ],
        )
    if failure.failure_type == "build_failure":
        return Analysis(
            classification="build_failure",
            confidence="high",
            hypothesis=(
                "The build failed because the Kotlin compiler "
                "reported an unresolved reference."
            ),
            evidence=failure.evidence,
            next_verification=[
                "Check whether the referenced symbol is defined.",
                "Verify the required import or dependency is available.",
                "Inspect the source location reported by the compiler.",
            ],
        )
    return Analysis(
        classification = "unknown",
        confidence = "low",
        hypothesis = "The available evidence is insufficient to classify the failure.",
        evidence=failure.evidence,
        next_verification = [
            "Collect additional application and system logs."
        ],
    )

