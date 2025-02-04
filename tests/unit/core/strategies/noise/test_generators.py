import pytest
import numpy as np
from App.core.noise.implementations.xorshift import XorShiftGenerator

class TestXorShiftGenerator:
    @pytest.fixture
    def generator(self):
        """Create a fresh generator instance for each test."""
        return XorShiftGenerator()
    
    def test_initialization(self, generator):
        """Test generator initializes with default seed."""
        assert isinstance(generator, XorShiftGenerator)
        assert generator.seed == 12345  # Default seed
    
    def test_output_range(self, generator):
        """Test generator output stays within [-1, 1] range."""
        frames = 1000
        output = generator.process_audio(frames, None)
        assert isinstance(output, np.ndarray)
        assert output.shape == (frames,)
        assert np.all(output >= -1.0)
        assert np.all(output <= 1.0)
    
    def test_deterministic_output(self):
        """Test that same seed produces same output."""
        gen1 = XorShiftGenerator()
        gen2 = XorShiftGenerator()
        
        # Generate with default seed
        out1 = gen1.process_audio(100, None)
        out2 = gen2.process_audio(100, None)
        np.testing.assert_array_equal(out1, out2)
        
        # Generate with custom seed
        params = {'seed': 42}
        out3 = gen1.process_audio(100, params)
        out4 = gen2.process_audio(100, params)
        np.testing.assert_array_equal(out3, out4)
        
        # Verify different seeds produce different output
        assert not np.array_equal(out1, out3)
    
    def test_parameter_updates(self, generator):
        """Test that seed parameter updates affect output."""
        # Generate with default seed
        out1 = generator.process_audio(100, None)
        
        # Update seed and verify output changes
        out2 = generator.process_audio(100, {'seed': 42})
        assert not np.array_equal(out1, out2)
        
        # Verify same seed reproduces output
        out3 = generator.process_audio(100, {'seed': 42})
        np.testing.assert_array_equal(out2, out3)
    
    def test_audio_passthrough(self, generator):
        """Test that existing audio is passed through unchanged."""
        audio = np.array([0.5, -0.3, 0.1])
        output = generator.process_audio(audio, None)
        np.testing.assert_array_equal(audio, output)
