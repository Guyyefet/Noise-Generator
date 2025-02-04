from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any, List
from .processor_factory import AudioProcessorFactory
from .noise.base import NoiseGenerator
from .filters.base import FilterBase

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
            
        # Initialize processor chain from config
        self.processors = [
            AudioProcessorFactory.create(proc["type"], **proc.get("params", {}))
            for proc in config["processors"]
        ]
        
        self.parameters = {}

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
        # Start with first processor (generator)
        audio = self.processors[0].process_audio(frames, self.parameters)
        
        # Pass through remaining processors in chain
        for processor in self.processors[1:]:
            audio = processor.process_audio(audio, self.parameters)
            
        return audio
