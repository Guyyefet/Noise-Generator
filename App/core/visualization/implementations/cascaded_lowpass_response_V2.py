"""Cascaded one-pole lowpass filter frequency response visualization."""

from App.core.visualization.filter_response_base import FilterResponseVisualizer
import numpy as np

class CascadedLowpassResponseV2Visualizer(FilterResponseVisualizer):
    def calculate_response(self, freqs: np.ndarray, parameters: dict) -> np.ndarray:
        """Calculate cascaded one-pole lowpass filter frequency response.
        
        Args:
            freqs: Array of frequencies to calculate response for
            parameters: Dictionary containing:
                - cutoff: Filter cutoff frequency (0-1 range)
                - resonance: Filter resonance at cutoff (0-1 range)
                - poles: Number of filter poles (1-4, integer)
                
        Returns:
            Array of response values in dB
        """
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        resonance = parameters.get('resonance', 0.0)
        poles = int(parameters.get('poles', 1))
        
        # Map cutoff like in CascadedOnePoleLowPassV2
        alpha = 0.001 + cutoff * 0.099
        cutoff_freq = alpha * 44100  # Approx cutoff in Hz
        
        # Calculate basic lowpass response for each pole
        response = 1 / (1 + (freqs/cutoff_freq)**(2*poles))
        
        # Add resonance peak (only applied to final stage)
        if resonance > 0:
            feedback = resonance * 0.9  # Max resonance of 0.9
            peak_gain = 1 + (feedback * 4)  # Resonance peak height
            q_factor = 0.5 + feedback * 4  # Peak sharpness
            peak = peak_gain / (1 + (q_factor * np.abs(freqs/cutoff_freq - 1))**2)
            response = response * peak
        
        # Apply gain compensation like in CascadedOnePoleLowPassV2
        base_gain = 1.5  # Base gain
        if poles > 1:
            base_gain += 0.2 * (poles - 1)  # Small boost per additional pole
        if resonance > 0:
            base_gain *= (1.0 - (resonance * 0.9 * 0.3))  # Reduce gain when resonance is high
        
        response = response * base_gain
        
        # Convert to dB
        response_db = 20 * np.log10(np.clip(response, 1e-6, None))
        return np.clip(response_db, -60, 24)
