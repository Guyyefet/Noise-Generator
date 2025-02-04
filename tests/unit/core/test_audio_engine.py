import pytest
import numpy as np
from unittest.mock import Mock, patch
from App.core.audio_engine import BandpassAudioEngine
from App.core.strategies.base import NoiseEngineStrategy

class MockProcessor(NoiseEngineStrategy):
    """Mock processor for testing."""
    def __init__(self, name="mock"):
        self.name = name
        self.process_calls = []
    
    def process_audio(self, frames_or_audio, parameters):
        self.process_calls.append((frames_or_audio, parameters))
        if isinstance(frames_or_audio, int):
            return np.zeros(frames_or_audio)
        return frames_or_audio

class TestBandpassAudioEngine:
    @pytest.fixture
    def mock_factory(self):
        """Mock the AudioProcessorFactory."""
        with patch('App.core.audio_engine.AudioProcessorFactory') as factory:
            # Create mock processors
            generator = MockProcessor("generator")
            filter = MockProcessor("filter")
            
            # Configure factory to return our mock processors
            factory.create.side_effect = lambda proc_type, **kwargs: {
                'noise': generator,
                'bandpass': filter
            }[proc_type]
            
            yield factory
    
    def test_initialization_default_config(self, mock_factory):
        """Test engine initializes with default config."""
        engine = BandpassAudioEngine()
        
        # Verify factory called correctly
        assert mock_factory.create.call_count == 2
        mock_factory.create.assert_any_call('noise')
        mock_factory.create.assert_any_call('bandpass')
        
        # Verify processors initialized
        assert len(engine.processors) == 2
        assert engine.parameters == {}
    
    def test_initialization_custom_config(self, mock_factory):
        """Test engine initializes with custom config."""
        config = {
            "processors": [
                {"type": "noise", "params": {"seed": 42}},
                {"type": "bandpass", "params": {"cutoff": 0.5}}
            ]
        }
        engine = BandpassAudioEngine(config)
        
        # Verify factory called with params
        mock_factory.create.assert_any_call('noise', seed=42)
        mock_factory.create.assert_any_call('bandpass', cutoff=0.5)
    
    def test_set_parameters(self, mock_factory):
        """Test parameter setting."""
        engine = BandpassAudioEngine()
        params = {'cutoff': 0.5, 'bandwidth': 0.3}
        
        engine.set_parameters(**params)
        assert engine.parameters == params
    
    def test_generate_noise(self, mock_factory):
        """Test noise generation and processing chain."""
        engine = BandpassAudioEngine()
        frames = 100
        params = {'cutoff': 0.5}
        engine.set_parameters(**params)
        
        # Generate noise
        output = engine.generate_noise(frames)
        
        # Verify output
        assert isinstance(output, np.ndarray)
        assert len(output) == frames
        
        # Verify processing chain
        generator = engine.processors[0]
        filter = engine.processors[1]
        
        # Generator should receive frame count
        assert generator.process_calls[0][0] == frames
        assert generator.process_calls[0][1] == params
        
        # Filter should receive generator output
        assert isinstance(filter.process_calls[0][0], np.ndarray)
        assert filter.process_calls[0][1] == params
    
    def test_processor_chain_order(self, mock_factory):
        """Test that processors are called in correct order."""
        engine = BandpassAudioEngine()
        
        # Create spy to track processing order
        process_order = []
        def spy_process(name, frames_or_audio, parameters):
            process_order.append(name)
            if isinstance(frames_or_audio, int):
                return np.zeros(frames_or_audio)
            return frames_or_audio
        
        # Patch processor process_audio methods with spy
        for proc in engine.processors:
            original_process = proc.process_audio
            proc.process_audio = lambda f, p, name=proc.name: spy_process(name, f, p)
        
        # Generate noise
        engine.generate_noise(100)
        
        # Verify order
        assert process_order == ['generator', 'filter']

    def test_invalid_processor_type(self, mock_factory):
        """Test error handling when config contains invalid processor type."""
        # Configure factory to raise for invalid type
        mock_factory.create.side_effect = ValueError("Invalid processor type")
        
        config = {
            "processors": [
                {"type": "invalid_type"}
            ]
        }
        
        with pytest.raises(ValueError, match="Invalid processor type"):
            BandpassAudioEngine(config)

    def test_processor_initialization_failure(self, mock_factory):
        """Test error handling when a processor fails to initialize."""
        # Configure factory to raise during initialization
        mock_factory.create.side_effect = RuntimeError("Initialization failed")
        
        with pytest.raises(RuntimeError, match="Initialization failed"):
            BandpassAudioEngine()

    def test_parameter_validation(self, mock_factory):
        """Test parameter validation across the processing chain."""
        engine = BandpassAudioEngine()
        
        # Mock processors to validate parameters
        def validate_params(frames_or_audio, parameters):
            if not isinstance(parameters.get('cutoff', 0), (int, float)):
                raise ValueError("Invalid cutoff type")
            if isinstance(frames_or_audio, int):
                return np.zeros(frames_or_audio)
            return frames_or_audio
            
        for proc in engine.processors:
            proc.process_audio = validate_params
        
        # Test invalid parameter type
        with pytest.raises(ValueError, match="Invalid cutoff type"):
            engine.set_parameters(cutoff="invalid")
            engine.generate_noise(100)

    def test_empty_processor_chain(self, mock_factory):
        """Test behavior with empty processor configuration."""
        config = {
            "processors": []
        }
        
        engine = BandpassAudioEngine(config)
        assert len(engine.processors) == 0
        
        # Should handle empty chain gracefully
        with pytest.raises(IndexError):
            engine.generate_noise(100)

    def test_audio_output_bounds(self, mock_factory):
        """Test that generated audio stays within [-1, 1] bounds."""
        engine = BandpassAudioEngine()
        
        # Configure first processor to generate out-of-bounds signal
        def generate_large_signal(frames, parameters):
            return np.ones(frames) * 2.0
            
        engine.processors[0].process_audio = generate_large_signal
        
        # Configure second processor to properly bound the signal
        def bound_signal(audio, parameters):
            return np.clip(audio, -1.0, 1.0)
            
        engine.processors[1].process_audio = bound_signal
        
        output = engine.generate_noise(100)
        assert np.all(output <= 1.0) and np.all(output >= -1.0)

    def test_processor_chain_modification(self, mock_factory):
        """Test adding/removing processors at runtime."""
        engine = BandpassAudioEngine()
        original_chain_length = len(engine.processors)
        
        # Add a new processor
        new_processor = MockProcessor("new")
        engine.processors.append(new_processor)
        
        assert len(engine.processors) == original_chain_length + 1
        
        # Verify new processor is included in chain
        process_order = []
        for proc in engine.processors:
            original_process = proc.process_audio
            proc.process_audio = lambda f, p, name=proc.name: process_order.append(name) or f
            
        engine.generate_noise(100)
        assert process_order == ['generator', 'filter', 'new']
