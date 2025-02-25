from dataclasses import dataclass
from typing import Any, Dict, Optional, Type, Union, List
from enum import Enum

@dataclass
class ParameterRange:
    """Defines a valid range for numeric parameters."""
    min_value: Union[float, int]
    max_value: Union[float, int]

    def validate_value(self, value: Union[float, int]) -> bool:
        """Check if a value is within the range."""
        return self.min_value <= value <= self.max_value

class ParameterRegistry:
    """Central registry for parameter definitions."""
    
    def __init__(self):
        self._definitions: Dict[str, Dict[str, Any]] = {}
    
    def register(self, name: str, definition: Dict[str, Any]):
        """
        Register a parameter definition.
        
        Args:
            name: Parameter name
            definition: Parameter definition dictionary
            
        Raises:
            ValueError: If parameter name already registered
        """
        if name in self._definitions:
            raise ValueError(f"Parameter {name} already registered")
        self._definitions[name] = definition
    
    def get_definition(self, name: str) -> Dict[str, Any]:
        """
        Get a parameter definition by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter definition dictionary
            
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
                
            definition = self._definitions[name]
            
            # Type validation
            if definition["type"] == "float" and not isinstance(value, (int, float)):
                raise TypeError(f"Parameter '{name}' must be a number")
            elif definition["type"] == "int" and not isinstance(value, int):
                raise TypeError(f"Parameter '{name}' must be an integer")
            elif definition["type"] == "enum" and value not in definition["enum_values"]:
                raise ValueError(f"Invalid value for enum parameter '{name}': {value}")
                
            # Range validation
            if definition["range"]:
                if not definition["range"].validate_value(value):
                    raise ValueError(
                        f"Parameter '{name}' value {value} is outside valid range "
                        f"[{definition['range'].min_value}, {definition['range'].max_value}]"
                    )
            
            validated[name] = value
            
        return validated
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get dictionary of default values for all registered parameters."""
        return {
            name: definition["default_value"]
            for name, definition in self._definitions.items()
        }
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of all registered parameter definitions."""
        return self._definitions.copy()
