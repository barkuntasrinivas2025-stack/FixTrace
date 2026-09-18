from dataclasses import dataclass, field


@dataclass
class Failure:
    failure_type: str
    component: str | None
    error_message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class Analysis:
    classification: str
    confidence: str
    hypothesis: str
    evidence: list[str] = field(default_factory=list)
    next_verification: list[str] = field(default_factory=list)
    
@dataclass(frozen=True)
class ToolRequest:
    principal: str
    action: str
    resource: str