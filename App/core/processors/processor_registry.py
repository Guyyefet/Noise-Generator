"""Module for registering audio processors with the factory."""

from .processor_factory import AudioProcessorFactory
from ..noise.implementations.xorshift import XorShiftGenerator
from ..filters.implementations.bandpass import BandpassFilter
from ..filters.implementations.cascaded_onepole_lowpass import LowPassFilter

def register_processors():
    """Register all available processor types with the factory."""
    
    # Register noise generators
    AudioProcessorFactory.register_generator("noise", XorShiftGenerator)
    
    # Register filters
    AudioProcessorFactory.register_filter("bandpass", BandpassFilter)
    AudioProcessorFactory.register_filter("lowpass", LowPassFilter)
