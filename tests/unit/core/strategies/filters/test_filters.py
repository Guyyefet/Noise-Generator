import pytest
import numpy as np
from App.core.filters.implementations.bandpass import BandpassFilter

class TestBandpassFilter:
    @pytest.fixture
    def filter(self):
        """Create a fresh filter instance for each test."""
        return BandpassFilter()
    
    def test_initialization(self, filter):
        """Test filter initializes with zeroed states."""
        assert isinstance(filter, BandpassFilter)
        assert filter.hp_prev_x == 0.0
        assert filter.hp_prev_y == 0.0
        assert filter.lp_prev_y == 0.0
    
    def test_default_parameters(self, filter):
        """Test filter behavior with default parameters."""
        # Create simple input signal
        input_signal = np.array([1.0, -1.0, 1.0, -1.0])
        output = filter.process_audio(input_signal, {})
        
        assert isinstance(output, np.ndarray)
        assert output.shape == input_signal.shape
        assert np.all(output >= -1.0)
        assert np.all(output <= 1.0)
        
        # Default parameters should let some signal through
        assert not np.allclose(output, 0)
    
    def test_parameter_ranges(self, filter):
        """Test filter with various parameter values."""
        input_signal = np.sin(np.linspace(0, 4*np.pi, 1000))
        
        # Test extreme parameter values
        params = [
            {'cutoff': 0.0, 'bandwidth': 0.0},  # Minimum values
            {'cutoff': 1.0, 'bandwidth': 1.0},  # Maximum values
            {'cutoff': 0.5, 'bandwidth': 0.5},  # Middle values
        ]
        
        for p in params:
            output = filter.process_audio(input_signal, p)
            assert np.all(output >= -1.0)
            assert np.all(output <= 1.0)
    
    def test_filter_state_persistence(self, filter):
        """Test that filter state is maintained between calls."""
        # Process first chunk
        chunk1 = np.array([1.0, -1.0, 1.0])
        out1 = filter.process_audio(chunk1, {'cutoff': 0.5, 'bandwidth': 0.5})
        
        # Save filter states
        hp_x = filter.hp_prev_x
        hp_y = filter.hp_prev_y
        lp_y = filter.lp_prev_y
        
        # Process second chunk
        chunk2 = np.array([-1.0, 1.0, -1.0])
        out2 = filter.process_audio(chunk2, {'cutoff': 0.5, 'bandwidth': 0.5})
        
        # Verify states changed
        assert filter.hp_prev_x != hp_x or filter.hp_prev_y != hp_y or filter.lp_prev_y != lp_y
    
    def test_gain_compensation(self, filter):
        """Test gain compensation behavior."""
        input_signal = np.array([1.0, -1.0, 1.0, -1.0])
        
        # Test with different bandwidths
        narrow = filter.process_audio(input_signal, {'bandwidth': 0.0})  # Should have more gain
        wide = filter.process_audio(input_signal, {'bandwidth': 1.0})    # Should have less gain
        
        # Calculate RMS values
        narrow_rms = np.sqrt(np.mean(narrow**2))
        wide_rms = np.sqrt(np.mean(wide**2))
        
        # Narrow bandwidth should have higher gain
        assert narrow_rms > wide_rms
    
    def test_filter_response(self, filter):
        """Test basic frequency response characteristics."""
        # Generate test signal with mixed frequencies
        t = np.linspace(0, 1, 1000)
        low_freq = np.sin(2 * np.pi * 10 * t)   # 10 Hz
        high_freq = np.sin(2 * np.pi * 100 * t)  # 100 Hz
        mixed = low_freq + high_freq
        
        # Apply filter with middle cutoff
        output = filter.process_audio(mixed, {'cutoff': 0.5, 'bandwidth': 0.5})
        
        # Output should be different from input due to filtering
        assert not np.allclose(output, mixed)
        # Output should still contain signal (not all filtered out)
        assert not np.allclose(output, 0)
