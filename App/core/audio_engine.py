from abc import ABC, abstractmethod
import numpy as np
from .strategies.filters.bandpass import BandpassStrategy

class AudioEngineBase(ABC):
    """Base class for audio engine implementations."""
    
    @abstractmethod
    def generate_noise(self, frames: int) -> np.ndarray:
        """Generate audio frames.
        
        Args:
            frames: Number of audio frames to generate
            
        Returns:
            numpy.ndarray: Generated audio frames
        """
        pass
    
    @abstractmethod
    def set_parameters(self, **parameters):
        """Set engine parameters.
        
        Args:
            **parameters: Dictionary of parameter key-value pairs
        """
        pass

class BandpassAudioEngine(AudioEngineBase):
    """Handles audio generation using configurable strategies."""
    
    def __init__(self):
        # Initialize with default bandpass strategy
        self.strategy = BandpassStrategy()
        self.parameters = {}

    def set_parameters(self, **parameters):
        """
        Set sound generation parameters.
        
        Args:
            **parameters: Dictionary of parameter key-value pairs that will be passed
                         through to the strategy
        """
        # Store all parameters without assumptions about their names/types
        self.parameters = parameters  # Replace instead of update to avoid parameter accumulation

    def generate_noise(self, frames: int):
        """Generate noise using current strategy."""
        return self.strategy.process_audio(frames, self.parameters)
