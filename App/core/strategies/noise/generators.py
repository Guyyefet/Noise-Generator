import numpy as np
from abc import ABC, abstractmethod

class NoiseGenerator(ABC):
    """Base class for noise generation algorithms."""
    
    @abstractmethod
    def generate(self, frames: int, parameters: dict = None) -> np.ndarray:
        """Generate noise frames.
        
        Args:
            frames: Number of frames to generate
            parameters: Dictionary of parameter key-value pairs
            
        Returns:
            numpy.ndarray: Generated noise frames in [-1, 1] range
        """
        pass

class XorShiftGenerator(NoiseGenerator):
    """XOR shift noise generator."""
    
    def __init__(self):
        self.seed = 12345  # Default seed, can be overridden by parameters
    
    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF
    
    def generate(self, frames: int, parameters: dict = None) -> np.ndarray:
        """Generate white noise using XOR shift.
        
        Args:
            frames: Number of frames to generate
            parameters: Dictionary containing optional parameters:
                - seed: Random seed value (int)
        """
        if parameters is not None:
            # Update seed if provided in parameters
            self.seed = parameters.get('seed', self.seed)
        noise = np.zeros(frames)
        for i in range(frames):
            self.seed = self._xor_shift(self.seed)
            # Normalize to range [-1, 1]
            noise[i] = (self.seed / 0x7FFFFFFF) - 1.0
        return noise
