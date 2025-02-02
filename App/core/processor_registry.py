"""Module for registering audio processors with the factory."""

from .processor_factory import AudioProcessorFactory
from .strategies.noise.generators import XorShiftGenerator
from .strategies.filters.filters import BandpassFilter

def register_processors():
    """Register all available processor types with the factory."""
    
    # Register noise generators
    AudioProcessorFactory.register("noise", XorShiftGenerator)
    
    # Register filters
    AudioProcessorFactory.register("bandpass", BandpassFilter)
