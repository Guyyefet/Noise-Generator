import numpy as np
from ..base import NoiseEngineStrategy

class XorShiftGenerator(NoiseEngineStrategy):
    """XOR shift noise generator."""
    
    def __init__(self):
        self.seed = 12345  # Default seed, can be overridden by parameters
    
    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF
    
    def process_audio(self, frames_or_audio: int | np.ndarray, parameters: dict) -> np.ndarray:
        """Generate or process audio using XOR shift.
        
        Args:
            frames_or_audio: Number of frames to generate (int) or audio data to process (np.ndarray)
            parameters: Dictionary containing optional parameters:
                - seed: Random seed value (int)
                
        Returns:
            Generated or processed audio data
        """
        if isinstance(frames_or_audio, int):
            # Generate new noise
            frames = frames_or_audio
            if parameters is not None:
                # Update seed if provided in parameters
                self.seed = parameters.get('seed', self.seed)
            noise = np.zeros(frames)
            for i in range(frames):
                self.seed = self._xor_shift(self.seed)
                # Normalize to range [-1, 1]
                noise[i] = (self.seed / 0x7FFFFFFF) - 1.0
            return noise
        else:
            # Pass through audio unchanged (generators only modify new audio)
            return frames_or_audio
