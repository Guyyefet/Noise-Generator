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
    def set_parameters(self, color: float, volume: float, cutoff: float, bandwidth: float):
        """Set engine parameters.
        
        Args:
            color: Noise color parameter
            volume: Output volume (0.0 to 1.0)
            cutoff: Filter cutoff frequency (0.0 to 1.0)
            bandwidth: Filter bandwidth (0.0 to 1.0)
        """
        pass

class BandpassAudioEngine(AudioEngineBase):
    """Handles audio generation using configurable strategies."""
    
    def __init__(self):
        # Initialize with default bandpass strategy
        self.strategy = BandpassStrategy()
        self.parameters = {
            'volume': 0.5,
            'cutoff': 0.5,
            'bandwidth': 0.5
        }

    def set_parameters(self, color: float, volume: float, cutoff: float, bandwidth: float):
        """Set sound generation parameters."""
        self.parameters.update({
            'volume': volume,
            'cutoff': cutoff,
            'bandwidth': bandwidth
        })

    def generate_noise(self, frames: int):
        """Generate noise using current strategy."""
        return self.strategy.process_audio(frames, self.parameters)
