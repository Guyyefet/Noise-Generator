from typing import Type, Dict, Any
from .strategies.base import NoiseEngineStrategy

class AudioProcessorFactory:
    """Factory for creating audio processor components."""
    
    _processors: Dict[str, Type[NoiseEngineStrategy]] = {}
    
    @classmethod
    def register(cls, name: str, processor_class: Type[NoiseEngineStrategy]) -> None:
        """Register a processor class with the factory.
        
        Args:
            name: Unique identifier for the processor type
            processor_class: Class to instantiate for this processor type
        """
        cls._processors[name] = processor_class
        
    @classmethod
    def create(cls, name: str, **params) -> NoiseEngineStrategy:
        """Create a new processor instance.
        
        Args:
            name: Identifier of the processor type to create
            **params: Parameters to pass to the processor constructor
            
        Returns:
            New processor instance
            
        Raises:
            KeyError: If processor type is not registered
        """
        if name not in cls._processors:
            raise KeyError(f"Unknown processor type: {name}")
            
        return cls._processors[name](**params)
        
    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Get list of registered processor types.
        
        Returns:
            List of processor type names
        """
        return list(cls._processors.keys())
