from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    is_valid: bool
    error_message: Optional[str] = None
    corrected_value: Optional[str] = None
