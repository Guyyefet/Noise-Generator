from core.observer import Subject

class NoiseParameters(Subject):
    """Manages noise generation parameters and notifies observers of changes."""
    
    def __init__(self):
        super().__init__()
        # Initialize default parameter values
        self.generator_type = "White Noise"
        self.filter_type = "Bandpass"
        self.volume = 0.5
        self.cutoff = 0.5
        self.bandwidth = 0.5
    
    def update_parameters(self, generator_type: str, filter_type: str, 
                         volume: float, cutoff: float, bandwidth: float):
        """Update all parameters and notify observers."""
        self.generator_type = generator_type
        self.filter_type = filter_type
        self.volume = volume
        self.cutoff = cutoff
        self.bandwidth = bandwidth
        self.notify()
    
    def notify(self, _ = None):
        """Notify observers with current parameter values."""
        for observer in self.observers:
            observer.update(
                self.generator_type,
                self.filter_type,
                self.volume,
                self.cutoff,
                self.bandwidth
            )
