from App.core.processors.processor_factory import AudioProcessorFactory
from App.core.noise.base import NoiseGenerator
from App.core.filters.base import FilterBase
from unittest.mock import Mock
import pytest

class MockGenerator(NoiseGenerator):
    """Mock noise generator for testing."""
    def __init__(self, **params):
        self.params = params
    
    def generate_noise(self, num_frames):
        return [0] * num_frames

class MockFilter(FilterBase):
    """Mock filter for testing."""
    def __init__(self, **params):
        self.params = params
    
    def process_audio(self, audio_data):
        return audio_data

class TestAudioProcessorFactory:
    @pytest.fixture(autouse=True)
    def clear_registry(self):
        """Clear factory registry before each test."""
        AudioProcessorFactory._noise_generators = {}
        AudioProcessorFactory._filters = {}
        yield
        AudioProcessorFactory._noise_generators = {}
        AudioProcessorFactory._filters = {}
    
    def test_register_generator(self):
        """Test noise generator registration."""
        AudioProcessorFactory.register_generator("test", MockGenerator)
        assert "test" in AudioProcessorFactory._noise_generators
        assert AudioProcessorFactory._noise_generators["test"] == MockGenerator
    
    def test_register_filter(self):
        """Test filter registration."""
        AudioProcessorFactory.register_filter("test", MockFilter)
        assert "test" in AudioProcessorFactory._filters
        assert AudioProcessorFactory._filters["test"] == MockFilter
    
    def test_register_generator_overwrite(self):
        """Test overwriting existing generator registration."""
        # Register first generator
        AudioProcessorFactory.register_generator("test", MockGenerator)
        
        # Create new generator type
        class NewGenerator(NoiseGenerator):
            def generate_noise(self, num_frames):
                return [1] * num_frames
        
        # Register with same name
        AudioProcessorFactory.register_generator("test", NewGenerator)
        
        # Verify overwritten
        assert AudioProcessorFactory._noise_generators["test"] == NewGenerator
    
    def test_register_filter_overwrite(self):
        """Test overwriting existing filter registration."""
        # Register first filter
        AudioProcessorFactory.register_filter("test", MockFilter)
        
        # Create new filter type
        class NewFilter(FilterBase):
            def process_audio(self, audio_data):
                return [x * 2 for x in audio_data]
        
        # Register with same name
        AudioProcessorFactory.register_filter("test", NewFilter)
        
        # Verify overwritten
        assert AudioProcessorFactory._filters["test"] == NewFilter
    
    def test_create_noise_generator(self):
        """Test noise generator creation."""
        params = {"seed": 42}
        processor = AudioProcessorFactory.create("noise", **params)
        
        assert isinstance(processor, NoiseGenerator)
        assert hasattr(processor, "generate")  # XorShiftGenerator uses generate() method
        assert hasattr(processor, "process_audio")  # All processors must have process_audio()
        assert processor.seed == 42
    
    def test_create_filter(self):
        """Test filter creation."""
        processor = AudioProcessorFactory.create("bandpass")  # BandpassFilter takes no init params
        
        assert isinstance(processor, FilterBase)
        assert hasattr(processor, "process_audio")
    
    def test_create_unknown_processor(self):
        """Test error handling for unknown processor type."""
        with pytest.raises(KeyError, match="Unknown processor type: unknown"):
            AudioProcessorFactory.create("unknown")
