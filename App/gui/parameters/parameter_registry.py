from typing import Any, Dict, Optional, List
from App.core.parameters.base_registry import BaseParameterRegistry, ParameterDefinition

class ParameterRegistry(BaseParameterRegistry):
    """Manages GUI-specific parameter definitions and registration."""
    
    def __init__(self):
        super().__init__()
        self._gui_metadata: Dict[str, Dict[str, Any]] = {}
        
    def register_gui_parameter(self, name: str, display_name: str, tooltip: str = "", 
                             control_type: str = "slider", options: Optional[List[str]] = None):
        """Register GUI-specific metadata for a parameter."""
        if name not in self._definitions:
            raise KeyError(f"Parameter {name} not found in core registry")
            
        self._gui_metadata[name] = {
            'display_name': display_name,
            'tooltip': tooltip,
            'control_type': control_type,
            'options': options
        }
        
    def get_gui_metadata(self, name: str) -> Dict[str, Any]:
        """Get GUI metadata for a parameter."""
        if name not in self._gui_metadata:
            raise KeyError(f"No GUI metadata found for parameter {name}")
        return self._gui_metadata[name]
        
    def get_all_gui_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered GUI metadata."""
        return self._gui_metadata.copy()
        
    def bind_control(self, name: str, control: Any):
        """Bind a GUI control to a parameter."""
        if name not in self._definitions:
            raise KeyError(f"Parameter {name} not found")
            
        # Store control reference
        self._gui_metadata[name]['control'] = control
        
    def update_from_control(self, name: str, value: Any):
        """Update parameter value from GUI control."""
        if name not in self._definitions:
            raise KeyError(f"Parameter {name} not found")
            
        # Validate and update parameter
        self.update_parameter(name, value)
        
    def notify_controls(self):
        """Notify all bound controls of parameter changes."""
        for name, metadata in self._gui_metadata.items():
            if 'control' in metadata:
                control = metadata['control']
                value = self.get_parameter(name)
                control.setValue(value)
