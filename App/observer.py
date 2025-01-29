from abc import ABC, abstractmethod
from typing import List, Any

class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        """Receive updates from subject."""
        pass

class Subject(ABC):
    def __init__(self):
        self.observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Attach an observer to the subject."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach(self, observer: Observer):
        """Detach an observer from the subject."""
        self.observers.remove(observer)
    
    @abstractmethod
    def notify(self):
        """Notify all observers about state changes."""
        pass
