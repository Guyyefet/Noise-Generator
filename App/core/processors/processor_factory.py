from typing import Any, Dict, List, Type, Optional
from dataclasses import dataclass

@dataclass
class ProcessorRegistration:
    """Data class holding processor registration information."""
    name: str
    processor_class: Type
    description: str
    category: str
    parameters: Dict[str, Dict[str, Any]]

class AudioProcessorFactory:
    """Factory for creating audio processor instances."""
    _registry: Dict[str, ProcessorRegistration] = {}

    @classmethod
    def register(cls, name: str, processor_class: Type, description: str, 
                category: str, parameters: Dict[str, Dict[str, Any]]) -> None:
        """Register a new processor type."""
        if name in cls._registry:
            raise ValueError(f"Processor '{name}' is already registered")
            
        registration = ProcessorRegistration(
            name=name,
            processor_class=processor_class,
            description=description,
            category=category,
            parameters=parameters
        )
        cls._registry[name] = registration

    @classmethod
    def create(cls, name: str, **kwargs) -> Any:
        """Create a new processor instance."""
        if name not in cls._registry:
            raise ValueError(f"Unknown processor type: {name}")
            
        registration = cls._registry[name]
        
        # Validate parameters against registered definitions
        for param_name, param_value in kwargs.items():
            if param_name not in registration.parameters:
                raise ValueError(f"Unknown parameter '{param_name}' for processor '{name}'")
            
            param_def = registration.parameters[param_name]
            
            # Type validation
            if param_def["type"] == "float" and not isinstance(param_value, (int, float)):
                raise TypeError(f"Parameter '{param_name}' must be a number")
            elif param_def["type"] == "int" and not isinstance(param_value, int):
                raise TypeError(f"Parameter '{param_name}' must be an integer")
            elif param_def["type"] == "string" and not isinstance(param_value, str):
                raise TypeError(f"Parameter '{param_name}' must be a string")
            elif param_def["type"] == "boolean" and not isinstance(param_value, bool):
                raise TypeError(f"Parameter '{param_name}' must be a boolean")
            elif param_def["type"] == "enum" and param_value not in param_def["enum_values"]:
                raise ValueError(f"Invalid value for enum parameter '{param_name}': {param_value}")
            
            # Range validation
            if param_def["range"] is not None:
                if param_value < param_def["range"].min_value or param_value > param_def["range"].max_value:
                    raise ValueError(
                        f"Parameter '{param_name}' value {param_value} is outside valid range "
                        f"[{param_def['range'].min_value}, {param_def['range'].max_value}]"
                    )

        # Create instance with validated parameters
        return registration.processor_class(**kwargs)

    @classmethod
    def get_registered_processors(cls) -> List[ProcessorRegistration]:
        """Get list of all registered processors."""
        return list(cls._registry.values())

    @classmethod
    def get_processor_info(cls, name: str) -> Optional[ProcessorRegistration]:
        """Get registration info for a specific processor."""
        return cls._registry.get(name)

    @classmethod
    def get_processors_by_category(cls, category: str) -> List[ProcessorRegistration]:
        """Get all processors in a specific category."""
        return [reg for reg in cls._registry.values() if reg.category == category]
