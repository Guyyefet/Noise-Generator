from App.core.parameters.observer import Subject
from typing import Any, Dict, Optional, Union
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
    gui_metadata: Optional[Dict[str, Any]] = None

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
            description=param_def.get("description"),
            gui_metadata=param_def.get("gui_metadata")
        )
        
        self._parameters[name] = definition
        self.notify()
        
    def get_definition(self, *names: str) -> Union[ParameterDefinition, Dict[str, ParameterDefinition]]:
        """Get parameter definition(s) by name(s).
        
        Args:
            *names: Names of parameters to retrieve. If no names provided,
                    returns all definitions.
                    
        Returns:
            If no names provided: Dictionary of all parameter definitions
            If single name provided: Single parameter definition
            If multiple names provided: Dictionary of requested parameter definitions
            
        Raises:
            KeyError: If any requested parameter is not found
        """
        if not names:
            return self._parameters.copy()
            
        missing = [name for name in names if name not in self._parameters]
        if missing:
            raise KeyError(f"Parameters not found: {', '.join(missing)}")
            
        result = {name: self._parameters[name] for name in names}
        
        # Return single value if only one name requested
        if len(names) == 1:
            return result[names[0]]
            
        return result
        
    def notify(self, _ = None):
        """Notify observers with current parameter definitions."""
        for observer in self.observers:
            observer.update(self._parameters)
