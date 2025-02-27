from enum import Enum, auto
from typing import Any

class ParameterEventType(Enum):
    """Types of parameter change events"""
    VALUE_CHANGED = auto()
    RANGE_CHANGED = auto()
    STEP_SIZE_CHANGED = auto()
    VALIDATION_RULES_CHANGED = auto()
    READONLY_CHANGED = auto()

class ParameterEvent:
    """Represents a parameter change event"""
    
    def __init__(self, 
                 event_type: ParameterEventType,
                 parameter_name: str,
                 old_value: Any = None,
                 new_value: Any = None):
        self.event_type = event_type
        self.parameter_name = parameter_name
        self.old_value = old_value
        self.new_value = new_value
        
    def __repr__(self):
        return (f"ParameterEvent(type={self.event_type.name}, "
                f"parameter={self.parameter_name}, "
                f"old={self.old_value}, new={self.new_value})")
