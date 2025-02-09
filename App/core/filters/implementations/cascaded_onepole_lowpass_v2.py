from ..base import FilterBase
import numpy as np

class CascadedOnePoleLowPassV2(FilterBase):
    """Low-pass filter implementation using cascaded one-pole stages with simplified design."""
    
    def __init__(self):
        super().__init__()
        # Initialize state array for maximum possible poles (4)
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
            
        # Map cutoff to filter coefficient (similar to bandpass)
        alpha = 0.001 + cutoff * 0.099
        
        # Calculate resonance feedback (only applied to final stage)
        feedback = resonance * 0.9  # Max resonance of 0.9
        
        # Initialize output array
        output = np.zeros_like(audio)
        current = audio.copy()
        
        # Process each pole
        for p in range(poles):
            # Pre-calculate coefficient complement
            one_minus_alpha = 1.0 - alpha
            
            for i in range(len(current)):
                # Get input sample
                input_sample = current[i]
                
                # Apply feedback only on final pole
                if p == poles - 1 and feedback > 0:
                    input_sample += feedback * self.prev_y[p]
                
                # Basic one-pole filter equation
                output[i] = alpha * input_sample + one_minus_alpha * self.prev_y[p]
                
                # Update state
                self.prev_y[p] = output[i]
            
            # Output becomes input to next stage
            current = output.copy()
        
        # Apply gain compensation
        base_gain = 1.5  # Base gain like bandpass
        if poles > 1:
            base_gain += 0.2 * (poles - 1)  # Small boost per additional pole
        if feedback > 0:
            base_gain *= (1.0 - (feedback * 0.3))  # Reduce gain when resonance is high
        
        # Remove DC offset (single method)
        output = output - np.mean(output)
        
        # Apply final gain and volume
        output = output * base_gain
        output = self._apply_volume(output, parameters)
        return self._clip_output(output)
