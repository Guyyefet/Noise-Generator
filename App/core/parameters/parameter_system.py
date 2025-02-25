from typing import Any, Dict, Optional, Union
from App.core.parameters.observer import Subject
from App.core.parameters.parameter_registry import ParameterRegistry, ParameterDefinition
from App.core.parameters.parameter_builder import ParameterRange

class ParameterSystem(Subject):
    """Unified parameter management system with observer pattern support."""
    
    def __init__(self, registry: ParameterRegistry):
        self._registry = registry
        self._parameters: Dict[str, Any] = {}
        self._processor_type: Optional[str] = None
        
    def set_processor_type(self, processor_type: str):
        """Set the current processor type and initialize parameters."""
        self._processor_type = processor_type
        self._parameters = {
            name: definition.default_value
            for name, definition in self.get_parameter_definitions().items()
        }
        
    def update_parameters(self, **kwargs):
        """
        Update parameters and notify observers.
        
        Args:
            **kwargs: Parameter key-value pairs to update
            
        Raises:
            KeyError: If an unknown parameter is provided
            ValueError: If a parameter value is invalid
        """
        # Validate parameters first
        validated = self.validate_parameters(kwargs)
        
        # Update parameters
        self._parameters.update(validated)
        
        # Notify observers with updated parameters
        self.notify(self._parameters)
    
    def register_processor_parameters(self, processor_type: str, parameters: Dict[str, ParameterDefinition]):
        """
        Register parameters for a specific processor type.
        
        Args:
            processor_type: The processor type these parameters belong to
            parameters: Dictionary of parameter definitions
            
        Raises:
            ValueError: If any parameter is already registered
        """
        self._registry.register_parameters(processor_type, parameters)
    
    def get_definition(self, name: str) -> ParameterDefinition:
        """
        Get a parameter definition by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter definition object
            
        Raises:
            KeyError: If parameter not found
        """
        return self._registry.get_parameter_definition(name)
    
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
            definition = self._registry.get_parameter_definition(name)
            
            # Type validation
            if definition.type == "float" and not isinstance(value, (int, float)):
                raise TypeError(f"Parameter '{name}' must be a number")
            elif definition.type == "int" and not isinstance(value, int):
                raise TypeError(f"Parameter '{name}' must be an integer")
            elif definition.type == "enum" and value not in definition.enum_values:
                raise ValueError(f"Invalid value for enum parameter '{name}': {value}")
                
            # Range validation
            if definition.range:
                if not definition.range.validate_value(value):
                    raise ValueError(
                        f"Parameter '{name}' value {value} is outside valid range "
                        f"[{definition.range.min_value}, {definition.range.max_value}]"
                    )
            
            validated[name] = value
            
        return validated
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get dictionary of all current parameter values."""
        return self._parameters.copy()
        
    def get_parameter_definitions(self) -> Dict[str, ParameterDefinition]:
        """Get dictionary of all registered parameter definitions."""
        return self._registry.get_all_parameter_definitions()
        
    def get_parameter(self, name: str, default: Optional[Any] = None) -> Any:
        """
        Get a parameter value.
        
        Args:
            name: Parameter name
            default: Default value if parameter doesn't exist
            
        Returns:
            Parameter value or default if not found
            
        Raises:
            KeyError: If parameter not found and no default provided
        """
        if name not in self._parameters:
            if default is not None:
                return default
            raise KeyError(f"Parameter {name} not found")
        return self._parameters[name]
        
    def get_parameter_definition(self, name: str) -> ParameterDefinition:
        """
        Get a parameter definition by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter definition object
            
        Raises:
            KeyError: If parameter not found
        """
        return self._registry.get_parameter_definition(name)
