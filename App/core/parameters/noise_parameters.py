from .observer import Subject
from .parameter_definitions import get_registry
from typing import Any, Dict, Optional

class NoiseParameters(Subject):
    """Manages noise generation parameters and notifies observers of changes."""
    
    def __init__(self):
        super().__init__()
        self._registry = get_registry()
        # Initialize with default values from registry
        self.parameters = self._registry.get_defaults()
    
    def update_parameters(self, **kwargs):
        """
        Update parameters and notify observers.
        
        Args:
            **kwargs: Parameter key-value pairs to update
            
        Raises:
            KeyError: If an unknown parameter is provided
            ValueError: If a parameter value is invalid
        """
        # Validate and update parameters
        validated = self._registry.validate_parameters(kwargs)
        self.parameters.update(validated)
        self.notify()
    
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
        if name not in self.parameters:
            if default is not None:
                return default
            raise KeyError(f"Parameter {name} not found")
        return self.parameters[name]
    
    def get_parameter_info(self, name: str) -> Dict[str, Any]:
        """
        Get parameter metadata.
        
        Args:
            name: Parameter name
            
        Returns:
            Dictionary containing parameter metadata
            
        Raises:
            KeyError: If parameter not found
        """
        definition = self._registry.get_definition(name)
        return {
            "name": definition.name,
            "type": definition.param_type.value,
            "description": definition.description,
            "units": definition.units,
            "display_name": definition.display_name,
            "range": {
                "min": definition.range.min_value,
                "max": definition.range.max_value
            } if definition.range else None,
            "current_value": self.parameters[name]
        }
    
    def notify(self, _ = None):
        """Notify observers with current parameter values."""
        for observer in self.observers:
            observer.update(self.parameters)
