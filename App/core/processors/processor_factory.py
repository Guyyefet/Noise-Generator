from typing import Type, Dict, Any, Union
from ..noise.base import NoiseGenerator
from ..noise.implementations.xorshift import XorShiftGenerator
from ..filters.base import FilterBase
from ..filters.implementations.bandpass import BandpassFilter

class AudioProcessorFactory:
    """Factory for creating audio processor components."""
    
    _noise_generators: Dict[str, Type[NoiseGenerator]] = {}
    _filters: Dict[str, Type[FilterBase]] = {}
    
    @classmethod
    def register_generator(cls, name: str, generator_class: Type[NoiseGenerator]) -> None:
        """Register a noise generator class.
        
        Args:
            name: Unique identifier for the generator type
            generator_class: Class to instantiate for this generator type
        """
        cls._noise_generators[name] = generator_class
        
    @classmethod
    def register_filter(cls, name: str, filter_class: Type[FilterBase]) -> None:
        """Register a filter class.
        
        Args:
            name: Unique identifier for the filter type
            filter_class: Class to instantiate for this filter type
        """
        cls._filters[name] = filter_class
        
    @classmethod
    def create(cls, processor_type: str, **params) -> Union[NoiseGenerator, FilterBase]:
        """Create a new processor instance.
        
        Args:
            processor_type: Type of processor to create ('noise' or 'bandpass')
            **params: Parameters to pass to the processor constructor
            
        Returns:
            New processor instance
            
        Raises:
            KeyError: If processor type is not supported
        """
        if processor_type == 'noise':
            return XorShiftGenerator(**params)
        elif processor_type == 'bandpass':
            return BandpassFilter(**params)
        else:
            raise KeyError(f"Unknown processor type: {processor_type}")

# Register default implementations
AudioProcessorFactory.register_generator('xorshift', XorShiftGenerator)
AudioProcessorFactory.register_filter('bandpass', BandpassFilter)
