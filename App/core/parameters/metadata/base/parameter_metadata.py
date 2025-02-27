from dataclasses import dataclass
from typing import Any, Dict, Optional
from enum import Enum
from App.core.parameters.validation.validator import BaseParameterValidator

class ParameterType(Enum):
    """Defines supported parameter types."""
    FLOAT = 'float'
    INT = 'int'
    BOOL = 'bool'
    STRING = 'string'
    ENUM = 'enum'

@dataclass
class ParameterMetadata:
    """Base class for parameter metadata."""
    name: str
    type: ParameterType
    description: str
    unit: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    group: Optional[str] = None
    is_required: bool = True
    default_value: Optional[Any] = None
    validator: Optional[BaseParameterValidator] = None
    gui_hints: Optional[Dict[str, Any]] = None

    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules for this parameter.
        
        Returns:
            Dict[str, Any]: Dictionary of validation rules where keys are rule names
            and values are validation functions or constraints
        """
        if hasattr(self, 'validation_rules'):
            return self.validation_rules
        return {}
