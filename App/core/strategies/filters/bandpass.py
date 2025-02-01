import numpy as np
from ..noise.generators import XorShiftGenerator
from .filters import BandpassFilter
from ..base import NoiseEngineStrategy

class BandpassStrategy(NoiseEngineStrategy):
    """Bandpass filtered noise generation strategy."""
    
    def __init__(self):
        self.generator = XorShiftGenerator()
        self.filter = BandpassFilter()
    
    def process_audio(self, frames: int, parameters: dict) -> np.ndarray:
        """Generate and process noise with bandpass filter.
        
        Args:
            frames: Number of audio frames to generate
            parameters: Dictionary of parameter key-value pairs that will be passed
                       to both generator and filter components
        """
        # Generate raw noise with parameters
        noise = self.generator.generate(frames, parameters)
        
        # Apply filter with parameters
        filtered = self.filter.process(noise, parameters)
        
        # Apply volume if specified
        volume = parameters.get('volume', 1.0)
        return filtered * volume
