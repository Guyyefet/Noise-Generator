from ..noise.base import NoiseGenerator
from ..filters.base import FilterBase
from typing import Type, Dict, Any, Union

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
            processor_type: Type of processor to create
            **params: Parameters to pass to the processor constructor
            
        Returns:
            New processor instance
            
        Raises:
            KeyError: If processor type is not supported
        """
        # Check if it's a noise generator
        if processor_type.lower() == 'noise':
            if not cls._noise_generators:
                raise KeyError("No noise generators registered")
            # Get first registered generator
            generator_class = next(iter(cls._noise_generators.values()))
            return generator_class(**params)
            
        # Check if it's a filter
        filter_type = processor_type.lower()
        if filter_type in cls._filters:
            return cls._filters[filter_type](**params)
            
        raise KeyError(f"Unknown processor type: {processor_type}")
