import numpy as np
from abc import ABC, abstractmethod

class NoiseGenerator(ABC):
    """Base class for noise generation algorithms."""
    
    @abstractmethod
    def generate(self, frames: int) -> np.ndarray:
        """Generate noise frames.
        
        Args:
            frames: Number of frames to generate
            
        Returns:
            numpy.ndarray: Generated noise frames in [-1, 1] range
        """
        pass

class XorShiftGenerator(NoiseGenerator):
    """XOR shift noise generator."""
    
    def __init__(self, seed: int = 12345):
        self.seed = seed
    
    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF
    
    def generate(self, frames: int) -> np.ndarray:
        """Generate white noise using XOR shift."""
        noise = np.zeros(frames)
        for i in range(frames):
            self.seed = self._xor_shift(self.seed)
            # Normalize to range [-1, 1]
            noise[i] = (self.seed / 0x7FFFFFFF) - 1.0
        return noise
