from ..base import FilterBase
import numpy as np

class CascadedOnePoleLowPassV2(FilterBase):
    """Low-pass filter implementation using cascaded one-pole stages with simplified design."""
    
    def __init__(self):
        super().__init__()
        # Initialize state array for maximum possible poles (4) using float32
        self.prev_y = np.zeros(4, dtype=np.float32)
    
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
            
        # Map cutoff frequency with better control
        alpha = 0.005 + np.power(cutoff, 2.0) * 0.495  # More stable range
        
        # Calculate resonance feedback for self-oscillation
        feedback = resonance  # Allow full resonance for self-oscillation
        
        # Initialize arrays
        output = np.zeros_like(audio, dtype=np.float32)
        current = audio.astype(np.float32)
        
        # Calculate filter coefficients
        base_alpha = np.clip(alpha, 0.005, 0.5)  # Limit range for stability
        pole_alphas = []
        for p in range(poles):
            # Less aggressive reduction per pole
            pole_alpha = base_alpha / (1.3 ** p)
            pole_alphas.append(pole_alpha)
        pole_alphas = np.array(pole_alphas, dtype=np.float32)
        one_minus_alphas = 1.0 - pole_alphas
        
        # Resonance increases with pole count but stays controlled
        feedback_scale = 1.0
        if poles > 1:
            feedback_scale = 1.0 + (0.1 * (poles - 1))  # 10% increase per additional pole
        scaled_feedback = feedback * feedback_scale if feedback > 0 else 0.0
        
        # Process each pole
        for p in range(poles):
            a = pole_alphas[p]
            one_minus_a = one_minus_alphas[p]
            
            # Apply feedback only on final pole
            if p == poles - 1 and scaled_feedback > 0:
                # Feedback with stability control
                feedback_signal = scaled_feedback * self.prev_y[p]
                # Soft clip feedback for smoother resonance
                feedback_signal = np.tanh(feedback_signal)
                current = current + feedback_signal
            
            # Filter with stability checks
            output = np.zeros_like(current, dtype=np.float32)
            for i in range(len(current)):
                # Basic one-pole filter equation
                out = a * current[i] + one_minus_a * self.prev_y[p]
                # Soft clip to prevent instability
                out = np.tanh(out)
                output[i] = out
                self.prev_y[p] = out
            
            current = output
        
        # Gain compensation
        base_gain = 1.5  # Start with moderate gain
        if poles > 1:
            # Gentler gain boost per pole
            base_gain *= (1.0 + 0.2 * (poles - 1))  # 20% boost per additional pole
        
        # Compensate for resonance attenuation
        if feedback > 0:
            # Increase gain with resonance
            resonance_boost = 1.0 + (feedback * 0.5)  # Up to 50% boost at max resonance
            base_gain *= resonance_boost
        
        # Apply gain with soft clipping for smoother limiting
        output = np.tanh(output * base_gain)
        
        # DC offset removal
        mean_val = np.mean(output)
        if np.isfinite(mean_val):
            output = output - mean_val
        
        # Apply volume and ensure finite values
        output = self._apply_volume(output, parameters)
        output = np.nan_to_num(output, nan=0.0)  # Replace NaN with 0
        
        # Ensure float32 output and clip
        return self._clip_output(output.astype(np.float32))
