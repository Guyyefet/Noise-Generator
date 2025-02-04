"""Module for registering audio processors with the factory."""

from .processor_factory import AudioProcessorFactory
from ..noise.implementations.xorshift import XorShiftGenerator
from ..filters.implementations.bandpass import BandpassFilter

def register_processors():
    """Register all available processor types with the factory."""
    
    # Register noise generators
    AudioProcessorFactory.register_generator("noise", XorShiftGenerator)
    
    # Register filters
    AudioProcessorFactory.register_filter("bandpass", BandpassFilter)
