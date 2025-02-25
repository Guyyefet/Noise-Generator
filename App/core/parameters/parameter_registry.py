from typing import Dict, Any, Optional
from .parameter_system import ParameterSystem
from .observer import Subject
from ..processors.processor_factory import AudioProcessorFactory
from .validation import validate_parameter

class ParameterRegistry(Subject):
    """Manages parameter definitions and their registration, with notification support."""
    
    def __init__(self):
        super().__init__()
        self.parameters: Dict[str, Any] = {}
        self._processor_type: Optional[str] = None
        
    def register(self, name: str, definition: Any):
        """Register a new parameter definition."""
        if not validate_parameter(definition.get("default_value"), definition):
            raise ValueError(f"Invalid default value for parameter {name}")
        self.parameters[name] = definition
        self.notify()
        
    def get(self, name: str) -> Any:
        """Get a parameter definition by name."""
        return self.parameters.get(name)
        
    def set_processor_type(self, processor_type: str):
        """Set the current processor type and register its parameters."""
        self._processor_type = processor_type
        processor_info = AudioProcessorFactory.get_processor_info(processor_type)
        if processor_info:
            for name, param_def in processor_info.parameters.items():
                self.register(name, param_def)
        self.notify()
        
    def get_parameter_info(self, name: str) -> Dict[str, Any]:
        """Get parameter metadata including type, range, and current value."""
        if self._processor_type is None:
            raise ValueError("No processor type set")
            
        processor_info = AudioProcessorFactory.get_processor_info(self._processor_type)
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
            "current_value": self.parameters.get(name)
        }
        
    def notify(self, _ = None):
        """Notify observers with current parameter values."""
        for observer in self.observers:
            observer.update(self.parameters)
