from abc import ABC, abstractmethod
from typing import Dict, List
from App.core.parameters.notification.event_types import ParameterEvent

class ParameterObserver(ABC):
    """Interface for parameter change observers"""
    
    @abstractmethod
    def on_parameter_changed(self, event: ParameterEvent):
        """Called when a parameter changes
        
        Args:
            event: The parameter change event containing details
        """
        pass

class ParameterSubject:
    """Base class for observable parameters"""
    
    def __init__(self):
        self._observers: Dict[str, List[ParameterObserver]] = {}
        
    def add_observer(self, parameter_name: str, observer: ParameterObserver):
        """Add an observer for a specific parameter"""
        if parameter_name not in self._observers:
            self._observers[parameter_name] = []
        self._observers[parameter_name].append(observer)
        
    def remove_observer(self, parameter_name: str, observer: ParameterObserver):
        """Remove an observer for a specific parameter"""
        if parameter_name in self._observers:
            self._observers[parameter_name].remove(observer)
            if not self._observers[parameter_name]:
                del self._observers[parameter_name]
                
    def notify_observers(self, event: ParameterEvent):
        """Notify all observers of a parameter change"""
        if event.parameter_name in self._observers:
            for observer in self._observers[event.parameter_name]:
                observer.on_parameter_changed(event)
