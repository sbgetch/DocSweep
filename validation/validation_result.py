from dataclasses import dataclass, field


@dataclass
class ValidationResult:

    success: bool

    errors: list[str] = field(default_factory=list)