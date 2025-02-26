"""Lowpass filter frequency response visualization."""

from App.core.visualization.filter_response_base import FilterResponseVisualizer
import numpy as np

class CascadedLowpassResponseVisualizer(FilterResponseVisualizer):
    def calculate_response(self, freqs: np.ndarray, parameters: dict) -> np.ndarray:
        """Calculate lowpass filter frequency response.
        
        Args:
            freqs: Array of frequencies to calculate response for
            parameters: Dictionary containing:
                - cutoff: Filter cutoff frequency (0-1)
                - resonance: Filter resonance/Q (0-1)
                - poles: Number of filter poles (1-4)
                
        Returns:
            Array of response values in dB
        """
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        resonance = parameters.get('resonance', 0.0)
        poles = int(parameters.get('poles', 1))
        
        # Map cutoff like in CascadedOnePoleLowPassV2
        freq_mult = 0.001 + cutoff * 0.099
        cutoff_freq = freq_mult * 44100  # Approx cutoff in Hz
        
        # Calculate frequency response
        w = 2 * np.pi * freqs / 44100
        wc = 2 * np.pi * cutoff_freq / 44100
        
        # Basic lowpass response
        response = 1 / (1 + (freqs/cutoff_freq)**(2*poles))
        
        # Add resonance peak
        if resonance > 0:
            peak_gain = 1 + (resonance * 4)  # Up to +12dB peak
            q_factor = 0.5 + resonance * 4  # Sharper peak with higher resonance
            peak = peak_gain / (1 + (q_factor * np.abs(freqs/cutoff_freq - 1))**2)
            response = response * peak
        
        # Convert to dB
        response_db = 20 * np.log10(np.clip(response, 1e-6, None))
        return np.clip(response_db, -60, 24)
