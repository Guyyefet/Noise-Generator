from App.core.parameters.observer import Subject
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class ParameterDefinition:
    """Standard parameter definition format for unified system."""
    name: str
    type: type
    display_name: Optional[str] = None
    units: Optional[str] = None
    range: Optional[Any] = None  # Will be ParameterRange after validation
    default_value: Optional[Any] = None
    valid_values: Optional[list] = None
    description: Optional[str] = None

class BaseParameterRegistry(Subject):
    """Base class for parameter registries with common functionality."""
    
    def __init__(self):
        super().__init__()
        self._parameters: Dict[str, ParameterDefinition] = {}
        
    def register(self, name: str, param_def: Dict[str, Any]) -> None:
        """Register a new parameter definition."""
        if name in self._parameters:
            raise ValueError(f"Parameter {name} already registered")
            
        definition = ParameterDefinition(
            name=name,
            type=param_def["type"],
            display_name=param_def.get("display_name"),
            units=param_def.get("units"),
            range=param_def.get("range"),
            default_value=param_def.get("default_value"),
            valid_values=param_def.get("valid_values"),
            description=param_def.get("description")
        )
        
        self._parameters[name] = definition
        self.notify()
        
    def get_definition(self, name: str) -> ParameterDefinition:
        """Get a parameter definition by name."""
        if name not in self._parameters:
            raise KeyError(f"Parameter {name} not found")
        return self._parameters[name]
        
    def get_all_definitions(self) -> Dict[str, ParameterDefinition]:
        """Get all registered parameter definitions."""
        return self._parameters.copy()
        
    def notify(self, _ = None):
        """Notify observers with current parameter definitions."""
        for observer in self.observers:
            observer.update(self._parameters)
