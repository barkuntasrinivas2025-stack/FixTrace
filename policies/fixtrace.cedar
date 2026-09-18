permit (
    principal == FixTrace::User::"fixtrace-agent",
    action == FixTrace::Action::"check_port",
    resource == FixTrace::Diagnostic::"diagnostic"
);
