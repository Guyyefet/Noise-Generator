import numpy as np
from .base import NoiseEngineStrategy
from .generators import XorShiftGenerator
from .filters import BandpassFilter

class BandpassStrategy(NoiseEngineStrategy):
    """Bandpass filtered noise generation strategy."""
    
    def __init__(self):
        self.generator = XorShiftGenerator()
        self.filter = BandpassFilter()
    
    def process_audio(self, frames: int, parameters: dict) -> np.ndarray:
        """Generate and process noise with bandpass filter.
        
        Args:
            frames: Number of audio frames to generate
            parameters: Dictionary containing:
                - volume: Output volume (0.0 to 1.0)
                - cutoff: Filter cutoff frequency (0.0 to 1.0)
                - bandwidth: Filter bandwidth (0.0 to 1.0)
        """
        # Generate raw noise
        noise = self.generator.generate(frames)
        
        # Apply filter
        filtered = self.filter.process(noise, parameters)
        
        # Apply volume
        return filtered * parameters['volume']
