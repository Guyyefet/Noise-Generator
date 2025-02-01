from abc import ABC, abstractmethod
import numpy as np

class NoiseEngineStrategy(ABC):
    """Base class for noise generation strategies."""
    
    @abstractmethod
    def process_audio(self, frames: int, parameters: dict) -> np.ndarray:
        """Process audio with given parameters.
        
        Args:
            frames: Number of audio frames to generate
            parameters: Dictionary of parameters for the strategy
                       (e.g., volume, cutoff, bandwidth)
        
        Returns:
            numpy.ndarray: Generated audio frames
        """
        pass
