from .observer import Subject
from .parameter_builder import ParameterDefinitionBuilder as Param
from .common_parameters import get_params
from typing import Any, Dict, Optional
from ..processors.processor_factory import AudioProcessorFactory

class NoiseParameters(Subject):
    """Manages noise generation parameters and notifies observers of changes."""
    
    def __init__(self):
        super().__init__()
        # Get initial parameters from the default noise generator
        noise_generators = AudioProcessorFactory.get_processors_by_category("noise")
        if noise_generators:
            default_generator = noise_generators[0]  # Use first noise generator as default
            self.parameters = {
                name: param_def["default_value"]
                for name, param_def in default_generator.parameters.items()
            }
        else:
            self.parameters = {}
    
    def update_parameters(self, **kwargs):
        """
        Update parameters and notify observers.
        
        Args:
            **kwargs: Parameter key-value pairs to update
            
        Raises:
            KeyError: If an unknown parameter is provided
            ValueError: If a parameter value is invalid
        """
        # Get current processor info
        processor_name = self.parameters.get("processor_type", "xorshift")  # Default to xorshift
        processor_info = AudioProcessorFactory.get_processor_info(processor_name)
        
        if not processor_info:
            raise ValueError(f"Unknown processor: {processor_name}")
            
        # Validate parameters against processor's parameter definitions
        for name, value in kwargs.items():
            if name not in processor_info.parameters:
                raise KeyError(f"Unknown parameter: {name}")
                
            param_def = processor_info.parameters[name]
            
            # Type validation
            if param_def["type"] == "float" and not isinstance(value, (int, float)):
                raise TypeError(f"Parameter '{name}' must be a number")
            elif param_def["type"] == "int" and not isinstance(value, int):
                raise TypeError(f"Parameter '{name}' must be an integer")
            elif param_def["type"] == "enum" and value not in param_def["enum_values"]:
                raise ValueError(f"Invalid value for enum parameter '{name}': {value}")
                
            # Range validation
            if param_def["range"]:
                if value < param_def["range"].min_value or value > param_def["range"].max_value:
                    raise ValueError(
                        f"Parameter '{name}' value {value} is outside valid range "
                        f"[{param_def['range'].min_value}, {param_def['range'].max_value}]"
                    )
        
        # Update parameters and notify observers
        self.parameters.update(kwargs)
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
        processor_name = self.parameters.get("processor_type", "xorshift")
        processor_info = AudioProcessorFactory.get_processor_info(processor_name)
        
        if not processor_info or name not in processor_info.parameters:
            raise KeyError(f"Parameter {name} not found")
            
        param_def = processor_info.parameters[name]
        return {
            "name": name,
            "type": param_def["type"],
            "display_name": param_def["display_name"] or name,
            "units": param_def["units"],
            "range": {
                "min": param_def["range"].min_value,
                "max": param_def["range"].max_value
            } if param_def["range"] else None,
            "current_value": self.parameters[name]
        }
    
    def notify(self, _ = None):
        """Notify observers with current parameter values."""
        for observer in self.observers:
            observer.update(self.parameters)
