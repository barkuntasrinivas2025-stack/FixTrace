from pathlib import Path
import shutil
import subprocess

from app.models import ToolRequest


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policies" / "fixtrace.cedar"
SCHEMA = ROOT / "policies" / "fixtrace.cedarschema"
ENTITIES = ROOT / "policies" / "entities.json"


def authorize(request: ToolRequest) -> bool:
    """
    Authorize a tool request using the FixTrace Cedar policy.

    Authorization fails closed: if Cedar cannot be executed or the
    authorization request cannot be evaluated, the request is denied.
    """
    cedar = shutil.which("cedar")

    if cedar is None:
        return False

    try:
        result = subprocess.run(
            [
                cedar,
                "authorize",
                "--policies",
                str(POLICY),
                "--schema",
                str(SCHEMA),
                "--entities",
                str(ENTITIES),
                "--principal",
                f'FixTrace::User::"{request.principal}"',
                "--action",
                f'FixTrace::Action::"{request.action}"',
                "--resource",
                f'FixTrace::Diagnostic::"{request.resource}"',
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return False

    return result.returncode == 0 and result.stdout.strip() == "ALLOW"