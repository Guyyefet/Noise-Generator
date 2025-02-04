from dataclasses import dataclass
from typing import Any, Dict, Optional, Type, Union, List
from enum import Enum

class ParameterType(Enum):
    """Supported parameter types."""
    FLOAT = "float"
    INT = "int"
    BOOL = "bool"
    STR = "str"

@dataclass
class Range:
    """Defines a valid range for numeric parameters."""
    min_value: Union[float, int]
    max_value: Union[float, int]

@dataclass
class ParameterDefinition:
    """Defines a parameter's properties and validation rules."""
    name: str
    param_type: ParameterType
    default_value: Any
    description: str
    range: Optional[Range] = None
    units: Optional[str] = None
    display_name: Optional[str] = None
    
    def __post_init__(self):
        """Validate the definition on creation."""
        self._validate_default_value()
        if self.range:
            self._validate_range()
    
    def _validate_default_value(self):
        """Ensure default value matches the parameter type."""
        type_map = {
            ParameterType.FLOAT: float,
            ParameterType.INT: int,
            ParameterType.BOOL: bool,
            ParameterType.STR: str
        }
        expected_type = type_map[self.param_type]
        if not isinstance(self.default_value, expected_type):
            raise ValueError(
                f"Default value {self.default_value} does not match type {self.param_type}"
            )
    
    def _validate_range(self):
        """Validate range if specified."""
        if self.param_type not in (ParameterType.FLOAT, ParameterType.INT):
            raise ValueError("Range can only be specified for numeric parameters")
        if self.range.min_value >= self.range.max_value:
            raise ValueError("Range min_value must be less than max_value")
        if not (self.range.min_value <= self.default_value <= self.range.max_value):
            raise ValueError("Default value must be within specified range")

    def validate_value(self, value: Any) -> Any:
        """
        Validate and potentially convert a value according to this definition.
        
        Args:
            value: Value to validate
            
        Returns:
            Validated and potentially converted value
            
        Raises:
            ValueError: If value is invalid
        """
        # Convert to correct type
        type_map = {
            ParameterType.FLOAT: float,
            ParameterType.INT: int,
            ParameterType.BOOL: bool,
            ParameterType.STR: str
        }
        try:
            value = type_map[self.param_type](value)
        except (ValueError, TypeError):
            raise ValueError(
                f"Cannot convert {value} to type {self.param_type}"
            )
        
        # Check range if applicable
        if self.range and self.param_type in (ParameterType.FLOAT, ParameterType.INT):
            if not (self.range.min_value <= value <= self.range.max_value):
                raise ValueError(
                    f"Value {value} outside valid range "
                    f"[{self.range.min_value}, {self.range.max_value}]"
                )
        
        return value

class ParameterRegistry:
    """Central registry for parameter definitions."""
    
    def __init__(self):
        self._definitions: Dict[str, ParameterDefinition] = {}
    
    def register(self, definition: ParameterDefinition):
        """
        Register a parameter definition.
        
        Args:
            definition: Parameter definition to register
            
        Raises:
            ValueError: If parameter name already registered
        """
        if definition.name in self._definitions:
            raise ValueError(f"Parameter {definition.name} already registered")
        self._definitions[definition.name] = definition
    
    def get_definition(self, name: str) -> ParameterDefinition:
        """
        Get a parameter definition by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter definition
            
        Raises:
            KeyError: If parameter not found
        """
        if name not in self._definitions:
            raise KeyError(f"Parameter {name} not registered")
        return self._definitions[name]
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a dictionary of parameters against their definitions.
        
        Args:
            parameters: Dictionary of parameter values
            
        Returns:
            Dictionary of validated parameter values
            
        Raises:
            KeyError: If an unknown parameter is provided
            ValueError: If a parameter value is invalid
        """
        validated = {}
        for name, value in parameters.items():
            if name not in self._definitions:
                raise KeyError(f"Unknown parameter: {name}")
            validated[name] = self._definitions[name].validate_value(value)
        return validated
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get dictionary of default values for all registered parameters."""
        return {
            name: definition.default_value 
            for name, definition in self._definitions.items()
        }
    
    def get_all_definitions(self) -> List[ParameterDefinition]:
        """Get list of all registered parameter definitions."""
        return list(self._definitions.values())
