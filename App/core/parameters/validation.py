from typing import Any, Union, Optional
from numbers import Number

class ParameterRange:
    """Defines valid range for a parameter."""
    def __init__(self, min_value: Number, max_value: Number, step: Optional[Number] = None):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

    def __call__(self, value: Number) -> bool:
        """Validate if value is within range."""
        return self.min_value <= value <= self.max_value

def validate_type(value: Any, expected_type: Union[type, str]) -> bool:
    """Validate that value matches expected type."""
    # Handle string type identifiers from parameter definitions
    if isinstance(expected_type, str):
        type_map = {
            "float": float,
            "int": int,
            "string": str,
            "boolean": bool
        }
        if expected_type not in type_map:
            return False
        return isinstance(value, type_map[expected_type])
    
    # Handle actual type objects
    return isinstance(value, expected_type)

def validate_enum(value: Any, valid_values: list) -> bool:
    """Validate that value is in list of valid values."""
    return value in valid_values

def validate_range(value: Number, param_range: Any) -> bool:
    """Validate that value is within specified range."""
    # Handle different types of range objects
    if hasattr(param_range, '__call__'):
        # Our ParameterRange class with __call__ method
        return param_range(value)
    elif hasattr(param_range, 'min_value') and hasattr(param_range, 'max_value'):
        # ParameterRange dataclass from parameter_builder.py
        return param_range.min_value <= value <= param_range.max_value
    elif isinstance(param_range, dict):
        # Dictionary with min_value and max_value keys
        return param_range.get('min_value', float('-inf')) <= value <= param_range.get('max_value', float('inf'))
    else:
        # Unknown range type, assume valid
        return True

def validate_parameter(value: Any, param_def: dict) -> bool:
    """Validate parameter against its definition."""
    if not validate_type(value, param_def["type"]):
        return False
        
    if "range" in param_def and param_def["range"]:
        if not validate_range(value, param_def["range"]):
            return False
            
    if "valid_values" in param_def and param_def["valid_values"] is not None:
        if not validate_enum(value, param_def["valid_values"]):
            return False
            
    return True
