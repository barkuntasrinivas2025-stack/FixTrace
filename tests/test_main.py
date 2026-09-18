from app.main import diagnose_port


def test_diagnose_port_reachable():
    analysis = diagnose_port("localhost", 5432)

    assert analysis.classification == "database_connection_failure"
    assert analysis.confidence == "high"
    assert "configured database endpoint" in analysis.hypothesis.lower()