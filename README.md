# FixTrace

FixTrace is a deterministic failure-diagnosis CLI with a controlled AI explanation layer.

It analyzes application and build logs, classifies failures using deterministic rules, presents supporting evidence, and uses a local LLM only to explain the already-determined diagnosis.

## Architecture

### Log Analysis

```text
Log File
   |
   v
Parser
   |
   v
Deterministic Failure Classification
   |
   v
Deterministic Analysis
   |
   +-------------> Evidence
   |
   +-------------> Hypothesis
   |
   +-------------> Verification Steps
                       |
                       v
                AI Explanation
                       |
                       v
                  Final Report
Diagnostic Tool Authorization
CLI
 |
 v
ToolRequest
 |
 v
Cedar Authorization
 |
 +-- DENY --> No tool execution
 |
 +-- ALLOW
       |
       v
   check_port
       |
       v
 DiagnosticResult
Key Design Principles
Deterministic Diagnosis

Failure classification and analysis are performed by application rules rather than the LLM.

Current classifications:

database_connection_failure
http_api_failure
build_failure
unknown
Controlled AI Explanation

The AI receives only:

classification
hypothesis

Evidence, confidence, and verification steps are not passed to the AI explanation component.

The AI output is therefore non-authoritative.

If the AI service fails, FixTrace preserves the deterministic diagnosis and reports:

AI explanation unavailable.
Authorization Boundary

Diagnostic tool execution is protected by Cedar authorization.

Unauthorized requests are denied before check_port executes.

Root-Cause Discipline

FixTrace distinguishes between a hypothesis and a proven root cause.

Every report explicitly states:

ROOT CAUSE
Not proven — verification required.
CLI
Analyze a Log
fixtrace analyze examples/database_error.log
fixtrace analyze examples/api_error.log
fixtrace analyze examples/gradle_error.log
Diagnose a TCP Port
fixtrace diagnose-port localhost 5432
Help
fixtrace --help
Example Output

For a database connection failure:

FAILURE
database_connection_failure

CONFIDENCE
high

HYPOTHESIS
The application could not establish a connection to the configured database endpoint.

AI EXPLANATION
...

ROOT CAUSE
Not proven — verification required.
Project Structure
fixtrace/
├── app/
│   ├── agent.py
│   ├── authorization.py
│   ├── cli.py
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   ├── report.py
│   ├── rules.py
│   └── tools.py
├── examples/
│   ├── api_error.log
│   ├── database_error.log
│   └── gradle_error.log
├── policies/
│   ├── allow-request.json
│   ├── entities.json
│   ├── fixtrace.cedar
│   └── fixtrace.cedarschema
├── tests/
└── pyproject.toml
Testing

Run the complete test suite:

python -m pytest -q

Current test suite:

50 passed

Also verify:

git diff --check
Safety and Trust Boundaries

FixTrace is designed so that:

Deterministic rules establish the diagnosis.
Evidence remains outside the AI explanation input.
Verification steps remain outside the AI explanation input.
AI output does not replace the deterministic hypothesis.
AI failures do not prevent deterministic diagnosis.
Prompt-injection content in logs cannot override deterministic classification.
Unauthorized diagnostic requests cannot execute the diagnostic tool.
Diagnostic socket resources are closed after use.
Root causes are not presented as proven without verification.
Limitations

FixTrace currently provides rule-based diagnosis for the failure patterns implemented in the parser and rules modules.

The AI component provides explanation only; it does not independently establish the root cause.

Development

Run the test suite after changes:

python -m pytest -q

Check the working tree:

git status

Check whitespace errors:

git diff --check
