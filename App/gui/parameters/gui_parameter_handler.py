from App.core.parameters.notification.observer import ParameterObserver
from App.core.parameters.notification.event_types import ParameterEvent
from App.core.parameters.management.registry import ParameterRegistry
from typing import Dict, Any, Callable, Optional
from enum import Enum
from dataclasses import dataclass
from PyQt6.QtCore import QObject

class ParameterType(Enum):
    FLOAT = 'float'
    INT = 'int'
    BOOL = 'bool'
    STRING = 'string'
    ENUM = 'enum'

@dataclass
class ParameterMetadata:
    """Stores metadata for a parameter."""
    name: str
    type: ParameterType
    description: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step_size: Optional[float] = None
    unit: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    group: Optional[str] = None

class GUIParameterHandler(QObject, ParameterObserver):
    """Handles parameter interactions between GUI and parameter system."""
    
    def __init__(self, registry: ParameterRegistry):
        super().__init__()
        self.registry = registry
        self._controls: Dict[str, Any] = {}
        self._metadata: Dict[str, ParameterMetadata] = {}
        
        # Register as observer for all parameters
        for param in self.registry.get_all().values():
            param.add_observer(param.name, self)
        
    def add_metadata(self, parameter_name: str, metadata: ParameterMetadata) -> None:
        """Add metadata for a parameter."""
        if parameter_name in self._metadata:
            raise ValueError(f"Metadata already exists for parameter '{parameter_name}'")
        self._metadata[parameter_name] = metadata
        
    def get_metadata(self, parameter_name: str) -> ParameterMetadata:
        """Get metadata for a parameter."""
        if parameter_name not in self._metadata:
            raise KeyError(f"No metadata found for parameter '{parameter_name}'")
        return self._metadata[parameter_name]
        
    def bind_control(self, parameter_name: str, control: Any, 
                    update_callback: Callable[[Any], None]) -> None:
        """Bind a GUI control to a parameter."""
        if parameter_name not in self.registry.get_all():
            raise ValueError(f"Parameter '{parameter_name}' not found")
            
        # Store control and setup connections
        self._controls[parameter_name] = {
            'control': control,
            'callback': update_callback
        }
        
        # Set initial value
        param_value = self.registry.get(parameter_name)
        control.setValue(param_value)
        
        # Configure control based on metadata
        if parameter_name in self._metadata:
            metadata = self._metadata[parameter_name]
            if hasattr(control, 'setMinimum') and metadata.min_value is not None:
                control.setMinimum(metadata.min_value)
            if hasattr(control, 'setMaximum') and metadata.max_value is not None:
                control.setMaximum(metadata.max_value)
            if hasattr(control, 'setSingleStep') and metadata.step_size is not None:
                control.setSingleStep(metadata.step_size)
            if hasattr(control, 'setToolTip'):
                control.setToolTip(metadata.description)
                
        # Connect control signals
        control.valueChanged.connect(update_callback)
        
    def on_parameter_changed(self, event: ParameterEvent):
        """Handle parameter change events from the parameter system."""
        if event.parameter_name in self._controls:
            control = self._controls[event.parameter_name]['control']
            control.blockSignals(True)
            
            # Handle different event types
            if event.event_type == ParameterEventType.VALUE_CHANGED:
                control.setValue(event.new_value)
            elif event.event_type == ParameterEventType.RANGE_CHANGED:
                if hasattr(control, 'setMinimum'):
                    control.setMinimum(event.new_value[0])
                if hasattr(control, 'setMaximum'):
                    control.setMaximum(event.new_value[1])
            elif event.event_type == ParameterEventType.READONLY_CHANGED:
                control.setEnabled(not event.new_value)
                
            control.blockSignals(False)
                
    def update_parameter(self, parameter_name: str, value: Any) -> None:
        """Update parameter value from GUI control."""
        if parameter_name not in self._controls:
            raise ValueError(f"No control bound for parameter '{parameter_name}'")
            
        self.registry.update(parameter_name, value)
