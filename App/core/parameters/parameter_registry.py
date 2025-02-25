from App.core.parameters.base_registry import BaseParameterRegistry, ParameterDefinition
from App.core.processors.processor_factory import AudioProcessorFactory
from App.core.parameters.validation import validate_parameter
from typing import Dict, Any, Optional

class ParameterRegistry(BaseParameterRegistry):
    """Manages processor-specific parameter definitions and registration."""
    
    def __init__(self):
        super().__init__()
        self._processor_type: Optional[str] = None
        
        
    def set_processor_type(self, processor_type: str):
        """Set the current processor type and register its parameters."""
        self._processor_type = processor_type
        processor_info = AudioProcessorFactory.get_processor_info(processor_type)
        if processor_info:
            for name, param_def in processor_info.parameters.items():
                if not validate_parameter(param_def.get("default_value"), param_def):
                    raise ValueError(f"Invalid default value for parameter {name}")
                super().register(name, param_def)
        
    def get_parameter_info(self, name: str) -> Dict[str, Any]:
        """Get parameter metadata including type, range, and current value."""
        if self._processor_type is None:
            raise ValueError("No processor type set")
            
        processor_info = AudioProcessorFactory.get_processor_info(self._processor_type)
        if not processor_info or name not in processor_info.parameters:
            raise KeyError(f"Parameter {name} not found")
            
        param_def = self.get_definition(name)
        return {
            "name": name,
            "type": param_def.type,
            "display_name": param_def.display_name or name,
            "units": param_def.units,
            "range": {
                "min": param_def.range.min_value,
                "max": param_def.range.max_value
            } if param_def.range else None,
            "current_value": param_def.default_value
        }
