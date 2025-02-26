from App.core.parameters.observer import Subject
from App.core.parameters.gui_interface import ParameterGUIInterface
from typing import Any, Dict, List, Optional, Union

class ParameterSystem(Subject, ParameterGUIInterface):
    """Unified parameter management system with observer pattern support."""
    
    def __init__(self):
        self._parameters = {}
        self.observers = []
        self._parameter_definitions: Dict[str, Dict] = {}
        self._processor_type: Optional[str] = None

    def register(self, name: str, param_dict: Dict):
        """Register a new parameter definition.
        
        Args:
            name: Parameter name
            param_dict: Dictionary containing parameter configuration
                        Required keys: default_value, min_value, max_value
                        Optional keys: step_size, metadata
            
        Raises:
            ValueError: If parameter already exists or required keys are missing
        """
        if name in self._parameter_definitions:
            raise ValueError(f"Parameter {name} already registered")
            
        # Validate required keys
        required_keys = {'default_value', 'min_value', 'max_value'}
        if not required_keys.issubset(param_dict.keys()):
            raise ValueError(f"Parameter {name} missing required keys: {required_keys}")
            
        self._parameter_definitions[name] = param_dict
        self._parameters[name] = param_dict['default_value']
        
    def set_processor_type(self, processor_type: str):
        """Set the current processor type and initialize parameters."""
        self._processor_type = processor_type
        self._parameters = {
            name: param_def['default_value']
            for name, param_def in self._parameter_definitions.items()
        }
    
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
                
            param_data = {
                'value': self._parameters[name],
                'definition': self._parameter_definitions[name]
            }
            
            if fields:
                return {field: param_data[field] for field in fields 
                       if field in param_data}
            return param_data
            
        # Get all parameters
        return {
            name: {
                'value': value,
                'definition': self._parameter_definitions[name]
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
                
            param_def = self._parameter_definitions[name]
            
            # Validate value against min/max
            if value < param_def['min_value'] or value > param_def['max_value']:
                raise ValueError(
                    f"Value {value} for parameter {name} must be between "
                    f"{param_def['min_value']} and {param_def['max_value']}"
                )
            
            self._parameters[name] = value
            
        self.notify(self._parameters)
        self.notify_controls()

    def get_metadata(self, name: Optional[str] = None, 
                   fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get parameter metadata with optional filtering.
        
        Args:
            name: Parameter name (None for all parameters)
            fields: List of specific metadata fields to return
            
        Returns:
            Dict of metadata for single parameter or all parameters
        """
        if name:
            if name not in self._parameter_definitions:
                raise KeyError(f"Parameter {name} not found")
                
            metadata = self._parameter_definitions[name].get('metadata', {})
            return {k: v for k, v in metadata.items() if not fields or k in fields}
            
        return {
            param_name: {k: v for k, v in (defn.get('metadata', {})).items() 
                        if not fields or k in fields}
            for param_name, defn in self._parameter_definitions.items()
        }
        
    def bind_control(self, name: str, control: Any):
        """Bind a GUI control to a parameter."""
        if name not in self._parameter_definitions:
            raise KeyError(f"Parameter {name} not found")
            
        # Initialize metadata if it doesn't exist
        if 'metadata' not in self._parameter_definitions[name]:
            self._parameter_definitions[name]['metadata'] = {}
            
        # Store control reference in metadata
        self._parameter_definitions[name]['metadata']['control'] = control
        
    def update_from_control(self, name: str, value: Any):
        """Update parameter value from GUI control."""
        self.update_parameters(**{name: value})
        
    def notify_controls(self):
        """Notify all bound controls of parameter changes."""
        for name, param_def in self._parameter_definitions.items():
            metadata = param_def.get('metadata', {})
            if 'control' in metadata:
                control = metadata['control']
                value = self._parameters[name]
                control.setValue(value)
