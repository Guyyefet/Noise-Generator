import numpy as np

class AudioEngine:
    """Handles pure sound generation logic."""
    
    def __init__(self):
        self.seed = 12345
        self.color_param = 0.0
        self.volume = 0.5
        self.cutoff = 0.5
        self.bandwidth = 0.5
        # Filter states
        self.hp_prev_x = 0.0
        self.hp_prev_y = 0.0
        self.lp_prev_y = 0.0

    def set_parameters(self, color: float, volume: float, cutoff: float, bandwidth: float):
        """Set sound generation parameters."""
        self.color_param = color
        self.volume = volume
        self.cutoff = cutoff
        self.bandwidth = bandwidth

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
        # Apply bandpass filter
        filtered = self._apply_bandpass(noise)
        return filtered * self.volume

    def _apply_bandpass(self, x: np.ndarray) -> np.ndarray:
        """Apply bandpass filter to input signal."""
        # Map cutoff from 0-1 to reasonable filter coefficient (0.001 to 0.1)
        base_alpha = 0.001 + self.cutoff * 0.099
        
        # Calculate high and low cutoffs based on bandwidth
        bandwidth_offset = self.bandwidth * 0.05  # Scale bandwidth effect
        high_alpha = min(0.1, base_alpha + bandwidth_offset)
        low_alpha = max(0.001, base_alpha - bandwidth_offset)
        
        # Initialize output arrays
        hp = np.zeros_like(x)
        lp = np.zeros_like(x)
        
        # High-pass filter with higher cutoff
        for i in range(len(x)):
            hp[i] = high_alpha * (self.hp_prev_y + x[i] - self.hp_prev_x)
            self.hp_prev_y = hp[i]
            self.hp_prev_x = x[i]
        
        # Low-pass filter with lower cutoff
        for i in range(len(hp)):
            lp[i] = (1 - low_alpha) * self.lp_prev_y + low_alpha * hp[i]
            self.lp_prev_y = lp[i]
        
        return lp
