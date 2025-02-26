"""Bandpass filter frequency response visualization."""

from App.core.visualization.filter_response_base import FilterResponseVisualizer
import numpy as np

class BandpassResponseVisualizer(FilterResponseVisualizer):
    def calculate_response(self, freqs: np.ndarray, parameters: dict) -> np.ndarray:
        """Calculate bandpass filter frequency response.
        
        Args:
            freqs: Array of frequencies to calculate response for
            parameters: Dictionary containing:
                - cutoff: Center frequency control (0-1)
                - bandwidth: Filter bandwidth control (0-1)
                
        Returns:
            Array of response values in dB
        """
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        bandwidth = parameters.get('bandwidth', 0.5)
        
        # Map cutoff to center frequency (20Hz-20kHz)
        center_freq = 20 * (20000/20)**cutoff
        
        # Map bandwidth to octave spread
        min_spread = 0.5  # minimum 1/2 octave
        max_spread = 4.0  # maximum 4 octaves
        octave_spread = min_spread + bandwidth * (max_spread - min_spread)
        
        # Calculate bandpass response in octaves
        octaves_from_center = np.abs(np.log2(freqs/center_freq))
        
        # Create smooth bandpass shape with steeper falloff
        response = np.exp(-2.0 * (octaves_from_center/octave_spread)**2)
        
        # Convert to dB with proper range (+6dB peak)
        response_db = 6 - 12 * (1 - response)  # Peak at +6dB, min at -60dB
        return np.clip(response_db, -60, 24)
