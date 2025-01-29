import numpy as np

class AudioEngine:
    """Handles pure sound generation logic."""
    
    def __init__(self):
        self.seed = 12345
        self.color_param = 0.0
        self.volume = 0.5

    def set_parameters(self, color: float, volume: float):
        """Set sound generation parameters."""
        self.color_param = color
        self.volume = volume

    def _xor_shift(self, seed: int):
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF

    def generate_noise(self, frames: int):
        """Generate noise with Markov chain-like behavior."""
        noise = np.zeros(frames)

        for i in range(frames):
            self.seed = self._xor_shift(self.seed)
            raw_value = (self.seed / 0x7FFFFFFF) - 1.0  # Normalize to range [-1, 1]

            if i == 0:
                noise[i] = raw_value  # Initial value (no previous state)
            else:
                # Markov chain influence: more influence with higher color_param
                noise[i] = raw_value * self.color_param + noise[i - 1] * (1 - self.color_param)

        # Apply volume
        return noise * self.volume
