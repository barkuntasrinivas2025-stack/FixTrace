from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policies" / "fixtrace.cedar"
SCHEMA = ROOT / "policies" / "fixtrace.cedarschema"
ENTITIES = ROOT / "policies" / "entities.json"


def run_cedar(*args):
    return subprocess.run(
        ["cedar", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cedar_policy_validates():
    result = run_cedar(
        "validate",
        "--schema", str(SCHEMA),
        "--policies", str(POLICY),
    )

    assert result.returncode == 0
    assert "policy set validation passed" in result.stdout


def test_cedar_allows_authorized_agent():
    result = run_cedar(
        "authorize",
        "--policies", str(POLICY),
        "--schema", str(SCHEMA),
        "--entities", str(ENTITIES),
        "--principal", 'FixTrace::User::"fixtrace-agent"',
        "--action", 'FixTrace::Action::"check_port"',
        "--resource", 'FixTrace::Diagnostic::"diagnostic"',
    )

    assert result.returncode == 0
    assert "ALLOW" in result.stdout


def test_cedar_denies_unknown_agent():
    result = run_cedar(
        "authorize",
        "--policies", str(POLICY),
        "--schema", str(SCHEMA),
        "--entities", str(ENTITIES),
        "--principal", 'FixTrace::User::"unknown-agent"',
        "--action", 'FixTrace::Action::"check_port"',
        "--resource", 'FixTrace::Diagnostic::"diagnostic"',
    )

    assert result.returncode == 2
    assert "DENY" in result.stdout
