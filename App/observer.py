from abc import ABC, abstractmethod
from typing import List, Any

class Observer(ABC):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        """Receive updates from subject."""
        pass

class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        self._observers.remove(observer)
    
    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about state changes."""
        pass
