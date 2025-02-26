from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

class ParameterGUIInterface(ABC):
    """Abstract interface for GUI parameter interactions."""
    
    @abstractmethod
    def get_metadata(self, name: Optional[str] = None, 
                   fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get parameter metadata with optional filtering."""
        pass
        
    @abstractmethod 
    def bind_control(self, name: str, control: Any):
        """Bind a GUI control to a parameter."""
        pass
        
    @abstractmethod
    def update_from_control(self, name: str, value: Any):
        """Update parameter value from GUI control."""
        pass
        
    @abstractmethod
    def notify_controls(self):
        """Notify all bound controls of parameter changes."""
        pass
