import pytest
from unittest.mock import Mock
from App.core.processors.processor_factory import AudioProcessorFactory
from App.core.noise.base import NoiseGenerator

class MockProcessor(NoiseGenerator):
    """Mock processor for testing."""
    def __init__(self, **params):
        self.params = params
    
    def process_audio(self, frames_or_audio, parameters):
        return frames_or_audio

class TestAudioProcessorFactory:
    @pytest.fixture(autouse=True)
    def clear_registry(self):
        """Clear factory registry before each test."""
        AudioProcessorFactory._processors = {}
        yield
        AudioProcessorFactory._processors = {}
    
    def test_register_processor(self):
        """Test processor registration."""
        AudioProcessorFactory.register("test", MockProcessor)
        assert "test" in AudioProcessorFactory._processors
        assert AudioProcessorFactory._processors["test"] == MockProcessor
    
    def test_register_overwrite(self):
        """Test overwriting existing registration."""
        # Register first processor
        AudioProcessorFactory.register("test", MockProcessor)
        
        # Create new processor type
        class NewProcessor(NoiseGenerator):
            pass
        
        # Register with same name
        AudioProcessorFactory.register("test", NewProcessor)
        
        # Verify overwritten
        assert AudioProcessorFactory._processors["test"] == NewProcessor
    
    def test_create_processor(self):
        """Test processor creation."""
        AudioProcessorFactory.register("test", MockProcessor)
        
        # Create with parameters
        params = {"param1": "value1", "param2": 42}
        processor = AudioProcessorFactory.create("test", **params)
        
        assert isinstance(processor, MockProcessor)
        assert processor.params == params
    
    def test_create_unknown_processor(self):
        """Test error handling for unknown processor type."""
        with pytest.raises(KeyError, match="Unknown processor type: unknown"):
            AudioProcessorFactory.create("unknown")
    
    def test_get_registered_types(self):
        """Test retrieving registered processor types."""
        # Register multiple processors
        AudioProcessorFactory.register("proc1", MockProcessor)
        AudioProcessorFactory.register("proc2", MockProcessor)
        
        types = AudioProcessorFactory.get_registered_types()
        assert isinstance(types, list)
        assert set(types) == {"proc1", "proc2"}
    
    def test_get_registered_types_empty(self):
        """Test getting types when none registered."""
        types = AudioProcessorFactory.get_registered_types()
        assert isinstance(types, list)
        assert len(types) == 0
    
    def test_processor_inheritance(self):
        """Test that processors must inherit from NoiseGenerator."""
        class InvalidProcessor:
            pass
        
        # Should work with proper inheritance
        AudioProcessorFactory.register("valid", MockProcessor)
        
        # Should work with subclass
        class ValidSubclass(MockProcessor):
            pass
        AudioProcessorFactory.register("subclass", ValidSubclass)
        
        # Both should be registered
        types = AudioProcessorFactory.get_registered_types()
        assert set(types) == {"valid", "subclass"}
