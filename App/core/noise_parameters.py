from core.observer import Subject

class NoiseParameters(Subject):
    """Manages noise generation parameters and notifies observers of changes."""
    
    def __init__(self):
        super().__init__()
        self.parameters = {}  # Empty dict - no default values
    
    def update_parameters(self, **kwargs):
        """
        Update parameters and notify observers.
        
        Args:
            **kwargs: Parameter key-value pairs to update
        """
        self.parameters.update(kwargs)
        self.notify()
    
    def get_parameter(self, name: str, default=None):
        """
        Get a parameter value.
        
        Args:
            name: Parameter name
            default: Default value if parameter doesn't exist
        
        Returns:
            Parameter value or default if not found
        """
        return self.parameters.get(name, default)
    
    def notify(self, _ = None):
        """Notify observers with current parameter values."""
        for observer in self.observers:
            observer.update(self.parameters)
