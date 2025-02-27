from typing import Any, Optional, Dict, Callable
from dataclasses import dataclass, field
from .parameter_interface import ParameterInterface
from ..notification.observer import ParameterSubject
from ..notification.event_types import ParameterEvent, ParameterEventType

@dataclass
class Parameter(ParameterInterface, ParameterSubject):
    """Base class for all parameter types with notification support"""
    name: str
    value: Any
    default: Any
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    step_size: Optional[Any] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    is_readonly: bool = False
    validation_rules: Dict[str, Callable[[Any], bool]] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize the parameter subject"""
        ParameterSubject.__init__(self)
        
    def set_value(self, new_value: Any):
        """Set parameter value with notification"""
        old_value = self.value
        self.value = new_value
        self._notify_value_change(old_value, new_value)
        
    def set_range(self, min_value: Any, max_value: Any):
        """Set parameter range with notification"""
        old_min, old_max = self.min_value, self.max_value
        self.min_value = min_value
        self.max_value = max_value
        self._notify_range_change(old_min, old_max, min_value, max_value)
        
    def set_readonly(self, readonly: bool):
        """Set readonly state with notification"""
        old_state = self.is_readonly
        self.is_readonly = readonly
        self._notify_readonly_change(old_state, readonly)
        
    def _notify_value_change(self, old_value: Any, new_value: Any):
        """Notify observers of value change"""
        event = ParameterEvent(
            event_type=ParameterEventType.VALUE_CHANGED,
            parameter_name=self.name,
            old_value=old_value,
            new_value=new_value
        )
        self.notify_observers(event)
        
    def _notify_range_change(self, old_min: Any, old_max: Any, new_min: Any, new_max: Any):
        """Notify observers of range change"""
        event = ParameterEvent(
            event_type=ParameterEventType.RANGE_CHANGED,
            parameter_name=self.name,
            old_value=(old_min, old_max),
            new_value=(new_min, new_max)
        )
        self.notify_observers(event)
        
    def _notify_readonly_change(self, old_state: bool, new_state: bool):
        """Notify observers of readonly state change"""
        event = ParameterEvent(
            event_type=ParameterEventType.READONLY_CHANGED,
            parameter_name=self.name,
            old_value=old_state,
            new_value=new_state
        )
        self.notify_observers(event)
