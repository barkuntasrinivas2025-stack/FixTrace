from app.main import diagnose_port


def test_diagnose_port_unreachable():
    analysis = diagnose_port("localhost", 5432)

    assert analysis.classification == "database_connection_failure"
    assert analysis.confidence == "high"