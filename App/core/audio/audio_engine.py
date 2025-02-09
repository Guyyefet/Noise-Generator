from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any, List
from ..processors.processor_factory import AudioProcessorFactory
from ..noise.base import NoiseGenerator
from ..filters.base import FilterBase

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

class AudioEngine(AudioEngineBase):
    """Modular audio engine that can use any combination of generators and filters."""
    
    DEFAULT_CONFIG = {
        "processors": [
            {"type": "noise"},
            {"type": "bandpass"}
        ]
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize audio engine with configurable components.
        
        Args:
            config: Configuration dictionary specifying:
                   - generator: Type of noise generator to use
                   - filters: List of filter types to apply in order
                   If None, uses DEFAULT_CONFIG.
        """
        if config is None:
            config = self.DEFAULT_CONFIG
            
        self.parameters = {}
        self.generator = AudioProcessorFactory.create("noise")
        self.filter = AudioProcessorFactory.create("bandpass")  # Default filter

    def set_parameters(self, **parameters):
        """Set parameters for all components.
        
        Args:
            **parameters: Dictionary of parameter key-value pairs
        """
        self.parameters = parameters

    def generate_noise(self, frames: int) -> np.ndarray:
        """Generate and process audio through component chain.
        
        Args:
            frames: Number of frames to generate
            
        Returns:
            Processed audio data
        """
        # Generate base noise
        audio = self.generator.process_audio(frames, self.parameters)
        
        # Check if filter type has changed
        filter_type = self.parameters.get("filter_type", "bandpass")
        if not hasattr(self, '_current_filter_type') or self._current_filter_type != filter_type:
            self.filter = AudioProcessorFactory.create(filter_type)
            self._current_filter_type = filter_type
            
        # Apply filter
        audio = self.filter.process_audio(audio, self.parameters)
        return audio
