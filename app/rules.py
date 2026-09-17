from app.models import Analysis,Failure


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

    return Analysis(
        classification = "unknown",
        confidence = "low",
        hypothesis = "The available evidence is insufficient to classify the failure.",
        evidence=failure.evidence,
        next_verification = [
            "Collect additional application and system logs."
        ],
    )
