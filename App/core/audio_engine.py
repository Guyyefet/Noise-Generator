from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Any
from .processor_factory import AudioProcessorFactory
from .strategies.base import NoiseEngineStrategy

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
    """Handles audio generation using a configurable processing chain."""
    
    DEFAULT_CONFIG = {
        "processors": [
            {"type": "noise"},
            {"type": "bandpass"}
        ]
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize audio engine with processor chain.
        
        Args:
            config: Configuration dictionary specifying processor chain.
                   If None, uses DEFAULT_CONFIG.
        """
        if config is None:
            config = self.DEFAULT_CONFIG
            
        # Initialize processor chain from config
        self.processors: List[NoiseEngineStrategy] = [
            AudioProcessorFactory.create(proc["type"], **proc.get("params", {}))
            for proc in config["processors"]
        ]
        
        self.parameters = {}

    def set_parameters(self, **parameters):
        """Set parameters for all processors in chain.
        
        Args:
            **parameters: Dictionary of parameter key-value pairs that will be passed
                         through to all processors
        """
        self.parameters = parameters

    def generate_noise(self, frames: int) -> np.ndarray:
        """Generate and process audio through processor chain.
        
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
