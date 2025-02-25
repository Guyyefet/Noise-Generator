import pytest
import numpy as np
from App.core.filters.implementations.cascaded_onepole_lowpass_v2 import CascadedOnePoleLowPassV2

class TestCascadedOnePoleLowPassV2:
    @pytest.fixture
    def filter(self):
        """Create a fresh filter instance for each test."""
        return CascadedOnePoleLowPassV2()
    
    def test_initialization(self, filter):
        """Test filter initializes with zeroed states."""
        assert isinstance(filter, CascadedOnePoleLowPassV2)
        assert len(filter.prev_y) == 4
        assert all(y == 0.0 for y in filter.prev_y)
        # Verify float32 precision
        assert filter.prev_y.dtype == np.float32
    
    def test_float32_precision(self, filter):
        """Test that filter maintains float32 precision throughout."""
        input_signal = np.ones(100, dtype=np.float32)
        output = filter.process_audio(input_signal, {})
        assert output.dtype == np.float32
        assert filter.prev_y.dtype == np.float32
    
    def test_default_parameters(self, filter):
        """Test filter behavior with default parameters."""
        input_signal = np.array([1.0, -1.0, 1.0, -1.0], dtype=np.float32)
        output = filter.process_audio(input_signal, {})
        
        assert isinstance(output, np.ndarray)
        assert output.shape == input_signal.shape
        assert np.all(output >= -1.0)
        assert np.all(output <= 1.0)
        
        # Default parameters should let some signal through
        assert not np.allclose(output, 0)
    
    def test_parameter_ranges(self, filter):
        """Test filter with various parameter values."""
        input_signal = np.sin(np.linspace(0, 4*np.pi, 1000, dtype=np.float32))
        
        # Test extreme parameter values
        params = [
            {'cutoff': 0.0, 'resonance': 0.0, 'poles': 1},  # Minimum values
            {'cutoff': 1.0, 'resonance': 1.0, 'poles': 4},  # Maximum values
            {'cutoff': 0.5, 'resonance': 0.5, 'poles': 2},  # Middle values
        ]
        
        for p in params:
            output = filter.process_audio(input_signal, p)
            assert np.all(output >= -1.0)
            assert np.all(output <= 1.0)
    
    def test_pole_count_validation(self, filter):
        """Test that pole count is properly validated."""
        input_signal = np.array([1.0, -1.0, 1.0, -1.0], dtype=np.float32)
        
        # Test invalid pole counts
        invalid_poles = [0, 5, -1]
        for poles in invalid_poles:
            with pytest.raises(ValueError):
                filter.process_audio(input_signal, {'poles': poles})
    
    def test_filter_state_persistence(self, filter):
        """Test that filter state is maintained between calls."""
        # Process first chunk with different pole counts
        chunk1 = np.array([1.0, -1.0, 1.0], dtype=np.float32)
        
        for poles in range(1, 5):
            # Process first chunk
            out1 = filter.process_audio(chunk1, {'poles': poles})
            
            # Save filter states
            prev_y = filter.prev_y.copy()
            
            # Process second chunk
            chunk2 = np.array([-1.0, 1.0, -1.0], dtype=np.float32)
            out2 = filter.process_audio(chunk2, {'poles': poles})
            
            # Verify states changed
            assert not np.allclose(filter.prev_y[:poles], prev_y[:poles])
    
    def test_frequency_response(self, filter):
        """Test frequency response characteristics for different pole counts."""
        # Generate test signal with mixed frequencies
        t = np.linspace(0, 1, 1000, dtype=np.float32)
        low_freq = np.sin(2 * np.pi * 10 * t)   # 10 Hz
        high_freq = np.sin(2 * np.pi * 100 * t)  # 100 Hz
        mixed = (low_freq + high_freq).astype(np.float32)
        
        outputs = []
        
        # Test increasing attenuation with more poles
        for poles in range(1, 5):
            output = filter.process_audio(mixed, {
                'cutoff': 0.3,  # Set cutoff below high frequency
                'poles': poles
            })
            outputs.append(output)
            
            if poles > 1:
                # Calculate RMS of high frequency content
                curr_high = np.sqrt(np.mean((output - low_freq)**2))
                prev_high = np.sqrt(np.mean((outputs[-2] - low_freq)**2))
                
                # Each additional pole should increase attenuation
                assert curr_high < prev_high
    
    def test_resonance_behavior(self, filter):
        """Test resonance behavior at cutoff frequency."""
        # Generate sine sweep around cutoff
        t = np.linspace(0, 2, 2000, dtype=np.float32)
        sweep = np.sin(2 * np.pi * (10 + 5 * t) * t)
        
        # Test with increasing resonance
        outputs = []
        resonances = [0.0, 0.5, 0.9, 1.0]
        for res in resonances:
            output = filter.process_audio(sweep, {
                'cutoff': 0.5,
                'resonance': res,
                'poles': 4
            })
            outputs.append(output)
            
        # Calculate RMS values
        rms_values = [np.sqrt(np.mean(out**2)) for out in outputs]
        
        # Check increasing resonance leads to increasing output levels
        for i in range(1, len(rms_values)):
            assert rms_values[i] > rms_values[i-1]
            
        # Test self-oscillation at max resonance
        max_res_output = filter.process_audio(np.zeros(1000, dtype=np.float32), {
            'cutoff': 0.5,
            'resonance': 1.0,
            'poles': 4
        })
        
        # Should have significant output even with zero input
        assert np.max(np.abs(max_res_output)) > 0.1
    
    def test_volume_scaling(self, filter):
        """Test volume scaling with different pole counts."""
        # Generate test signal
        t = np.linspace(0, 1, 1000, dtype=np.float32)
        input_signal = np.sin(2 * np.pi * 10 * t)
        
        # Test output levels for different pole counts
        base_rms = None
        for poles in range(1, 5):
            output = filter.process_audio(input_signal, {
                'cutoff': 0.5,
                'poles': poles
            })
            
            rms = np.sqrt(np.mean(output**2))
            
            if base_rms is None:
                base_rms = rms
            else:
                # Output level should stay within 3dB (factor of ~0.7-1.4)
                assert 0.7 * base_rms <= rms <= 1.4 * base_rms
    
    def test_dc_offset(self, filter):
        """Test that filter doesn't introduce DC offset."""
        # Create test signal with zero mean
        t = np.linspace(0, 1, 1000, dtype=np.float32)
        input_signal = np.sin(2 * np.pi * 10 * t)
        assert abs(np.mean(input_signal)) < 1e-10  # Verify input has no DC
        
        # Test with different pole configurations
        for poles in range(1, 5):
            output = filter.process_audio(input_signal, {
                'cutoff': 0.5,
                'resonance': 0.5,
                'poles': poles
            })
            
            # Output should also have negligible DC
            assert abs(np.mean(output)) < 1e-3
