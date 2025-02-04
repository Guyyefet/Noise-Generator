import numpy as np
from ..base import FilterBase

class BandpassFilter(FilterBase):
    """Bandpass filter implementation."""
    
    def __init__(self):
        super().__init__()
        # Additional filter states for bandpass
        self.hp_prev_x = 0.0
        self.hp_prev_y = 0.0
        self.lp_prev_y = 0.0
    
    def process_audio(self, audio: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply bandpass filter to input signal.
        
        Args:
            audio: Input audio frames
            parameters: Dictionary of parameter key-value pairs containing:
                - cutoff: Center frequency (0-1 range)
                - bandwidth: Filter bandwidth (0-1 range)
                - volume: Output volume scaling (optional)
                
        Returns:
            Filtered audio data
        """
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        bandwidth = parameters.get('bandwidth', 0.5)
        
        # Map cutoff from 0-1 to reasonable filter coefficient (0.001 to 0.1)
        base_alpha = 0.001 + cutoff * 0.099
        
        # Calculate high and low cutoffs based on bandwidth
        bandwidth_offset = bandwidth * 0.05
        high_alpha = min(0.1, base_alpha + bandwidth_offset)
        low_alpha = max(0.001, base_alpha - bandwidth_offset)
        
        # Initialize output arrays
        hp = np.zeros_like(audio)
        lp = np.zeros_like(audio)
        
        # High-pass filter
        for i in range(len(audio)):
            # y[n] = x[n] - x[n-1] + (1-alpha) * y[n-1]
            hp[i] = audio[i] - self.hp_prev_x + (1 - high_alpha) * self.hp_prev_y
            self.hp_prev_y = hp[i]
            self.hp_prev_x = audio[i]
        
        # Low-pass filter
        for i in range(len(hp)):
            # y[n] = alpha * x[n] + (1-alpha) * y[n-1]
            lp[i] = low_alpha * hp[i] + (1 - low_alpha) * self.lp_prev_y
            self.lp_prev_y = lp[i]
        
        # Base gain of 1.5x plus small bandwidth-dependent adjustment
        gain_compensation = 1.5 + (0.2 * (1.0 - bandwidth))  # More gain for narrow bandwidth
        lp *= gain_compensation
        
        # Apply volume and clip
        output = self._apply_volume(lp, parameters)
        return self._clip_output(output)
