"""Base class for filter frequency response visualization."""

from abc import ABC, abstractmethod
import numpy as np

class FilterResponseVisualizer(ABC):
    @abstractmethod
    def calculate_response(self, freqs: np.ndarray, parameters: dict) -> np.ndarray:
        """Calculate frequency response in dB for given frequencies and parameters.
        
        Args:
            freqs: Array of frequencies to calculate response for
            parameters: Dictionary of filter parameters (cutoff, bandwidth, etc.)
            
        Returns:
            Array of response values in dB
        """
        pass
