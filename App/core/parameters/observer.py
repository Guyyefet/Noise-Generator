from typing import List, Any, Dict, Callable

class Observer:
    def update(self, *args, **kwargs):
        """Receive updates from subject."""
        pass

class ParameterObserver(Observer):
    """Specialized observer for parameter changes."""
    
    def __init__(self, callback: Callable[[Dict[str, Any]], None]):
        self.callback = callback
        
    def update(self, params: Dict[str, Any]) -> None:
        """Handle parameter updates."""
        self.callback(params)

class Subject:
    def __init__(self):
        self.observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer to the subject."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer from the subject."""
        self.observers.remove(observer)
    
    def notify(self, params: Dict[str, Any] = None):
        """Notify all observers about state changes."""
        for observer in self.observers:
            if params:
                observer.update(params)
            else:
                observer.update()
