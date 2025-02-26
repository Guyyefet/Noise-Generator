from App.core.parameters.base_registry import BaseParameterRegistry, ParameterDefinition
from typing import Any, Dict, Optional, List

class ParameterRegistry(BaseParameterRegistry):
    """Manages GUI-specific parameter interactions."""
    
    def get_metadata(self, name: Optional[str] = None, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get parameter metadata with optional filtering.
        
        Args:
            name: Parameter name (None for all parameters)
            fields: List of specific metadata fields to return
            
        Returns:
            Dict of metadata for single parameter or all parameters
        """
        if name:
            definition = self.get_definition(name)
            metadata = definition.gui_metadata or {}
            return {k: v for k, v in metadata.items() if not fields or k in fields}
            
        return {
            param_name: {k: v for k, v in (defn.gui_metadata or {}).items() 
                        if not fields or k in fields}
            for param_name, defn in self.get_all_definitions().items()
        }
        
    def bind_control(self, name: str, control: Any):
        """Bind a GUI control to a parameter."""
        definition = self.get_definition(name)
        if not definition.gui_metadata:
            definition.gui_metadata = {}
        definition.gui_metadata['control'] = control
        
    def update_from_control(self, name: str, value: Any):
        """Update parameter value from GUI control."""
        self.update_parameter(name, value)
        
    def notify_controls(self):
        """Notify all bound controls of parameter changes."""
        for definition in self.get_all_definitions().values():
            if definition.gui_metadata and 'control' in definition.gui_metadata:
                control = definition.gui_metadata['control']
                value = self.get_parameter(definition.name)
                control.setValue(value)
