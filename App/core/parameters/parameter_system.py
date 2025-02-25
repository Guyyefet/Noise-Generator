from App.core.parameters.parameter_registry import ParameterRegistry, ParameterDefinition
from App.core.parameters.parameter_builder import ParameterRange
from App.core.parameters.observer import Subject
from typing import Any, Dict, List, Optional, Union

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
    
    def get_parameter(self, name: Optional[str] = None, 
                    fields: Optional[List[str]] = None) -> Union[Dict[str, Any], Any]:
        """
        Get parameter data with optional filtering.
        
        Args:
            name: Parameter name (None for all parameters)
            fields: List of specific fields to return
            
        Returns:
            Single parameter value or dict of parameter data
            
        Raises:
            KeyError: If parameter not found
            ValueError: If invalid field requested
        """
        if name:
            # Get single parameter
            if name not in self._parameters:
                raise KeyError(f"Parameter {name} not found")
                
            definition = self._registry.get_parameter_definition(name)
            param_data = {
                'value': self._parameters[name],
                'definition': definition
            }
            
            if fields:
                return {field: param_data[field] for field in fields 
                       if field in param_data}
            return param_data
            
        # Get all parameters
        return {
            name: {
                'value': value,
                'definition': self._registry.get_parameter_definition(name)
            }
            for name, value in self._parameters.items()
        }
    
    def update_parameters(self, **kwargs):
        """
        Update parameters with validation and notification.
        
        Args:
            **kwargs: Parameter key-value pairs to update
            
        Raises:
            KeyError: If an unknown parameter is provided
            ValueError: If a parameter value is invalid
        """
        for name, value in kwargs.items():
            if name not in self._parameters:
                raise KeyError(f"Parameter {name} not found")
                
            definition = self._registry.get_parameter_definition(name)
            
            # Validate value
            if not definition.validate_value(value):
                raise ValueError(
                    f"Invalid value for parameter {name}: {value}"
                )
            
            self._parameters[name] = value
            
        self.notify(self._parameters)
