from typing import List, Any

class Observer:
    def update(self, *args, **kwargs):
        """Receive updates from subject."""
        pass

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
    
    def notify(self, _ = None):
        """Notify all observers about state changes."""
        for observer in self.observers:
            observer.update()
