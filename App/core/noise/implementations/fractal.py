import numpy as np
from ..base import NoiseGenerator
from typing import Optional

class FractalNoiseGenerator(NoiseGenerator):
    """Fractal noise generator using XOR shift as base noise source."""
    
    def __init__(self, 
                 octave_count: int = 4,
                 persistence: float = 0.5,
                 lacunarity: float = 2.0,
                 scale: float = 1.0,
                 seed: Optional[int] = None):
        """
        Initialize fractal noise generator.
        
        Args:
            octave_count: Number of octaves (4-8)
            persistence: Amplitude decrease per octave (0.5-0.8)
            lacunarity: Frequency increase per octave (typically 2.0)
            scale: Overall frequency scale (0.1-10.0)
            seed: Optional random seed
        """
        self.octave_count = octave_count
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.scale = scale
        self.seed = seed if seed is not None else 12345
        
    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF
        
    def _generate_base_noise(self, frames: int) -> np.ndarray:
        """Generate base noise using XOR shift."""
        noise = np.zeros(frames)
        for i in range(frames):
            self.seed = self._xor_shift(self.seed)
            noise[i] = (self.seed / 0x7FFFFFFF) - 1.0
        return noise
        
    def process_audio(self, audio_data):
        """Process audio data (pass-through for noise generators)."""
        return audio_data
        
    def generate(self, frames: int) -> np.ndarray:
        """Generate fractal noise samples.
        
        Args:
            frames: Number of frames to generate
            
        Returns:
            numpy.ndarray: Generated noise samples in range [-1, 1]
        """
        noise = np.zeros(frames)
        amplitude = 1.0
        frequency = self.scale
        
        for _ in range(self.octave_count):
            # Generate base noise at current frequency
            base = self._generate_base_noise(frames)
            # Stretch and interpolate base noise
            x = np.linspace(0, 1, frames)
            xp = np.linspace(0, 1, len(base))
            octave = np.interp(x, xp, base)
            # Add to final noise with current amplitude
            noise += octave * amplitude
            # Update parameters for next octave
            amplitude *= self.persistence
            frequency *= self.lacunarity
            
        # Normalize final output
        return noise / np.max(np.abs(noise))
