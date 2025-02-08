from ..base import FilterBase
import numpy as np

class LowPassFilter(FilterBase):
    """Low-pass filter implementation with variable pole count and resonance."""
    
    def __init__(self):
        super().__init__()
        # Initialize state arrays for maximum possible poles (4)
        self.prev_x = np.zeros(4)
        self.prev_y = np.zeros(4)
    
    def process_audio(self, audio: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply multi-pole low-pass filter to input signal.
        
        Args:
            audio: Input audio frames
            parameters: Dictionary of parameter key-value pairs containing:
                - cutoff: Filter cutoff frequency (0-1 range)
                - resonance: Filter resonance at cutoff (0-1 range)
                - poles: Number of filter poles (1-4, integer)
                - volume: Output volume scaling (optional)
                
        Returns:
            Filtered audio data
        """
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        resonance = parameters.get('resonance', 0.0)
        poles = int(parameters.get('poles', 1))
        
        # Validate pole count
        if poles < 1 or poles > 4:
            raise ValueError("Pole count must be between 1 and 4")
            
        # Map cutoff with exponential curve for better control
        alpha = 0.001 + np.power(cutoff, 3.0) * 0.999  # More aggressive curve
        
        # Calculate coefficients with steeper rolloff per pole
        pole_alphas = []
        for p in range(poles):
            # Much steeper reduction per pole for better attenuation
            pole_alpha = alpha / (5.0 ** p)  # Increased from 3.0 to 5.0
            pole_alphas.append(pole_alpha)
        
        # Resonance increases with pole count for stronger effect
        max_resonance = 0.95 + (poles * 0.01)  # More resonance for more poles
        feedback = resonance * max_resonance
        
        # Initialize output array
        output = np.zeros_like(audio)
        current = audio.copy()
        
        # Process each pole
        for p in range(poles):
            a = pole_alphas[p]
            one_minus_a = 1.0 - a
            
            for i in range(len(current)):
                input_sample = current[i]
                
                # Apply feedback only on final pole
                if p == poles - 1 and feedback > 0:
                    input_sample += feedback * self.prev_y[p]
                
                # Basic one-pole filter
                output[i] = a * input_sample + one_minus_a * self.prev_y[p]
                
                # Update states
                self.prev_x[p] = input_sample
                self.prev_y[p] = output[i]
            
            # Output becomes input to next stage
            current = output.copy()
        
        # Multi-stage DC offset removal
        # 1. Remove mean
        output = output - np.mean(output)
        
        # 2. Apply windowed DC removal
        window_size = min(64, len(output))
        if window_size > 1:
            window = np.ones(window_size) / window_size
            dc_trend = np.convolve(output, window, mode='same')
            output = output - dc_trend
        
        # 3. Ensure first sample starts at zero
        output = output - output[0]
        
        # Apply gain compensation
        base_gain = 1.0 + (0.05 * poles)  # Further reduced base gain
        resonance_boost = 1.0
        if feedback > 0:
            resonance_boost = 1.0 + (feedback * 0.2)  # Further reduced resonance boost
        
        # Apply gain after DC removal
        output = output * base_gain * resonance_boost
        
        # Final DC check and removal
        if abs(np.mean(output)) >= 0.001:
            output = output - np.mean(output)
        
        # Apply volume and clip
        output = self._apply_volume(output, parameters)
        return self._clip_output(output)
