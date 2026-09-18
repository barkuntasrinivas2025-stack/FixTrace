from app.cli import main


def test_analyze_command(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["fixtrace", "analyze", "examples/api_error.log"],
    )

    main()

    output = capsys.readouterr().out

    assert "FIXTRACE" in output
    assert "http_api_failure" in output
    assert "Not proven" in output


def test_diagnose_port_command(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["fixtrace", "diagnose-port", "localhost", "5432"],
    )

    main()

    output = capsys.readouterr().out

    assert "database_connection_failure" in output
    assert "high" in output
    assert "configured database endpoint" in output
