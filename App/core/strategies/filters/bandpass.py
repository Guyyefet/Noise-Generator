import numpy as np
from .filters import BandpassFilter
from ..base import NoiseEngineStrategy

class BandpassStrategy(NoiseEngineStrategy):
    """Bandpass filter processor."""
    
    def __init__(self):
        self.filter = BandpassFilter()
    
    def process_audio(self, audio: np.ndarray, parameters: dict) -> np.ndarray:
        """Process audio through bandpass filter.
        
        Args:
            audio: Input audio data to filter
            parameters: Dictionary of parameter key-value pairs
            
        Returns:
            Filtered audio data
        """
        # Apply filter with parameters
        filtered = self.filter.process(audio, parameters)
        
        # Apply volume if specified (moved to end of chain)
        volume = parameters.get('volume', 1.0)
        return filtered * volume
