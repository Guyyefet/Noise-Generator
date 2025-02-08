import numpy as np
from abc import ABC, abstractmethod

class FilterBase(ABC):
    """Base class for all audio filters."""
    
    def __init__(self):
        # Filter states
        self.prev_x = 0.0
        self.prev_y = 0.0
    
    @abstractmethod
    def process_audio(self, audio: np.ndarray, parameters: dict) -> np.ndarray:
        """Process audio through filter.
        
        Args:
            audio: Input audio data to filter
            parameters: Dictionary of parameter key-value pairs
            
        Returns:
            Filtered audio data
        """
        pass

    def _apply_volume(self, audio: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply volume scaling to audio.
        
        Args:
            audio: Input audio data
            parameters: Dictionary containing optional volume parameter
            
        Returns:
            Volume-adjusted audio data
        """
        volume = parameters.get('volume', 1.0)
        return audio * volume

    def _clip_output(self, audio: np.ndarray) -> np.ndarray:
        """Clip output to prevent overflow.
        
        Args:
            audio: Input audio data
            
        Returns:
            Clipped audio data in range [-1, 1]
        """
        return np.clip(audio, -1.0, 1.0)
