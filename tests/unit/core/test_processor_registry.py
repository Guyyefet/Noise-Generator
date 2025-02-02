import pytest
from unittest.mock import patch, Mock
from App.core.processor_registry import register_processors
from App.core.strategies.noise.generators import XorShiftGenerator
from App.core.strategies.filters.filters import BandpassFilter

class TestProcessorRegistry:
    @pytest.fixture
    def mock_factory(self):
        """Mock the AudioProcessorFactory."""
        with patch('App.core.processor_registry.AudioProcessorFactory') as factory:
            yield factory
    
    def test_register_processors(self, mock_factory):
        """Test that all processors are registered with factory."""
        # Call registration function
        register_processors()
        
        # Verify noise generator registration
        mock_factory.register.assert_any_call("noise", XorShiftGenerator)
        
        # Verify filter registration
        mock_factory.register.assert_any_call("bandpass", BandpassFilter)
        
        # Verify total number of registrations
        assert mock_factory.register.call_count == 2
    
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
        def track_register(name, cls):
            registrations.append((name, cls))
        mock_factory.register.side_effect = track_register
        
        # Register processors
        register_processors()
        
        # Verify order
        assert registrations == [
            ("noise", XorShiftGenerator),
            ("bandpass", BandpassFilter)
        ]
    
    def test_duplicate_registration(self, mock_factory):
        """Test handling of duplicate registrations."""
        # Mock register to track calls but allow duplicates
        registrations = {}
        def track_register(name, cls):
            registrations[name] = cls
        mock_factory.register.side_effect = track_register
        
        # Register processors twice
        register_processors()
        register_processors()
        
        # Verify only latest registration kept
        assert len(registrations) == 2
        assert registrations["noise"] == XorShiftGenerator
        assert registrations["bandpass"] == BandpassFilter
