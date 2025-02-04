from abc import ABC, abstractmethod
import numpy as np

class NoiseGenerator(ABC):
    """Base class for noise generation strategies."""
    
    @abstractmethod
    def generate(self, frames: int) -> np.ndarray:
        """Generate noise samples.
        
        Args:
            frames: Number of frames to generate
            
        Returns:
            numpy.ndarray: Generated noise samples in range [-1, 1]
        """
        pass
