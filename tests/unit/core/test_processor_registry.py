from App.core.processors.processor_registry import register_processors
from App.core.noise.implementations.xorshift import XorShiftGenerator
from App.core.filters.implementations.bandpass import BandpassFilter
from unittest.mock import patch, Mock
import pytest

class TestProcessorRegistry:
    @pytest.fixture
    def mock_factory(self):
        """Mock the AudioProcessorFactory."""
        with patch('App.core.processors.processor_registry.AudioProcessorFactory') as factory:
            yield factory
    
    def test_register_processors(self, mock_factory):
        """Test that all processors are registered with factory."""
        # Call registration function
        register_processors()
        
        # Verify noise generator registration
        mock_factory.register_generator.assert_called_once_with("noise", XorShiftGenerator)
        
        # Verify filter registration
        mock_factory.register_filter.assert_called_once_with("bandpass", BandpassFilter)
    
    def test_processor_types(self):
        """Test that registered processor types are valid."""
        # Verify noise generator implements required interface
        generator = XorShiftGenerator()
        assert hasattr(generator, 'process_audio')
        
        # Verify filter implements required interface
        filter = BandpassFilter()
        assert hasattr(filter, 'process_audio')
    
    def test_registration_order(self, mock_factory):
        """Test that processors are registered in correct order."""
        # Track registration order
        registrations = []
        def track_register_generator(name, cls):
            registrations.append(("generator", name, cls))
        def track_register_filter(name, cls):
            registrations.append(("filter", name, cls))
            
        mock_factory.register_generator.side_effect = track_register_generator
        mock_factory.register_filter.side_effect = track_register_filter
        
        # Register processors
        register_processors()
        
        # Verify order - generators registered before filters
        assert registrations == [
            ("generator", "noise", XorShiftGenerator),
            ("filter", "bandpass", BandpassFilter)
        ]
    
    def test_duplicate_registration(self, mock_factory):
        """Test handling of duplicate registrations."""
        # Register processors twice
        register_processors()
        register_processors()
        
        # Verify each registration method called twice
        assert mock_factory.register_generator.call_count == 2
        assert mock_factory.register_filter.call_count == 2
        
        # Verify final registrations
        mock_factory.register_generator.assert_called_with("noise", XorShiftGenerator)
        mock_factory.register_filter.assert_called_with("bandpass", BandpassFilter)
