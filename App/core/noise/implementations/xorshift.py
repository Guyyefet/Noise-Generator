import numpy as np
from ..base import NoiseGenerator

class XorShiftGenerator(NoiseGenerator):
    """XOR shift noise generator."""
    
    def __init__(self, seed: int = 12345):
        """Initialize XOR shift generator.
        
        Args:
            seed: Initial seed value (default: 12345)
        """
        self.seed = seed
    
    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF
    
    def generate(self, frames: int) -> np.ndarray:
        """Generate noise samples.
        
        Args:
            frames: Number of frames to generate
            
        Returns:
            numpy.ndarray: Generated noise samples in range [-1, 1]
        """
        noise = np.zeros(frames)
        for i in range(frames):
            self.seed = self._xor_shift(self.seed)
            # Normalize to range [-1, 1]
            noise[i] = (self.seed / 0x7FFFFFFF) - 1.0
        return noise
        
    def process_audio(self, frames_or_audio: int | np.ndarray, parameters: dict) -> np.ndarray:
        """Generate or process audio.
        
        Args:
            frames_or_audio: Number of frames to generate (int) or audio data to process (np.ndarray)
            parameters: Dictionary containing optional parameters:
                - seed: Random seed value (int)
                
        Returns:
            Generated or processed audio data
        """
        if isinstance(frames_or_audio, int):
            # Update seed if provided in parameters
            if parameters is not None:
                self.seed = parameters.get('seed', self.seed)
            return self.generate(frames_or_audio)
        else:
            # Pass through audio unchanged (generators only modify new audio)
            return frames_or_audio
