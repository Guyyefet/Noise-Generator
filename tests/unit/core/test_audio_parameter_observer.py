from App.core.audio.audio_parameter_observer import AudioParameterObserver
from App.core.audio.audio_engine import AudioEngineBase
from App.core.audio.audio_stream import AudioStream
from unittest.mock import Mock, patch, call
import pytest
import logging

class TestAudioParameterObserver:
    @pytest.fixture
    def mock_audio_engine(self):
        """Create a mock audio engine."""
        engine = Mock(spec=AudioEngineBase)
        engine.generate_noise = Mock(return_value=None)
        return engine
    
    @pytest.fixture
    def mock_audio_stream(self):
        """Create a mock audio stream."""
        return Mock(spec=AudioStream)
    
    @pytest.fixture
    def observer(self, mock_audio_engine, mock_audio_stream):
        """Create an observer instance with mock components."""
        return AudioParameterObserver(mock_audio_engine, mock_audio_stream)
    
    def test_initialization(self, observer, mock_audio_engine, mock_audio_stream):
        """Test observer initialization."""
        assert observer.audio_engine == mock_audio_engine
        assert observer.audio_stream == mock_audio_stream
        assert observer.audio_stream.generate_audio == mock_audio_engine.generate_noise
        assert isinstance(observer.logger, logging.Logger)
    
    def test_update_parameters(self, observer, mock_audio_engine):
        """Test parameter updates are passed to engine."""
        params = {'cutoff': 0.5, 'bandwidth': 0.3}
        observer.update(params)
        mock_audio_engine.set_parameters.assert_called_once_with(**params)
    
    def test_update_parameters_error(self, observer, mock_audio_engine):
        """Test parameter update error handling."""
        # Mock engine to raise error
        mock_audio_engine.set_parameters.side_effect = ValueError("Invalid parameter")
        
        # Should log error but not raise
        with patch.object(observer.logger, 'error') as mock_logger:
            observer.update({'invalid': 'value'})
            mock_logger.assert_called_once_with("Parameter validation error: Invalid parameter")
    
    def test_start_audio(self, observer, mock_audio_stream):
        """Test starting audio stream."""
        observer.start()
        mock_audio_stream.start.assert_called_once()
    
    def test_start_audio_error(self, observer, mock_audio_stream):
        """Test error handling when starting stream."""
        mock_audio_stream.start.side_effect = Exception("Start failed")
        
        with pytest.raises(Exception, match="Start failed"):
            with patch.object(observer.logger, 'error') as mock_logger:
                observer.start()
                mock_logger.assert_called_once_with("Failed to start audio stream: Start failed")
    
    def test_stop_audio(self, observer, mock_audio_stream):
        """Test stopping audio stream."""
        observer.stop()
        mock_audio_stream.stop.assert_called_once()
    
    def test_stop_audio_error(self, observer, mock_audio_stream):
        """Test error handling when stopping stream."""
        mock_audio_stream.stop.side_effect = Exception("Stop failed")
        
        with pytest.raises(Exception, match="Stop failed"):
            with patch.object(observer.logger, 'error') as mock_logger:
                observer.stop()
                mock_logger.assert_called_once_with("Failed to stop audio stream: Stop failed")
    
    def test_parameter_key_error(self, observer, mock_audio_engine):
        """Test handling of KeyError in parameter updates."""
        mock_audio_engine.set_parameters.side_effect = KeyError("Missing required parameter")
        
        with patch.object(observer.logger, 'error') as mock_logger:
            observer.update({})
            mock_logger.assert_called_once_with(
                "Parameter validation error: 'Missing required parameter'"
            )
            
    @pytest.mark.parametrize("params,expected_call", [
        ({}, {}),  # Empty dictionary
        ({'cutoff': 0.5}, {'cutoff': 0.5}),  # Single parameter
        ({'cutoff': 0.5, 'bandwidth': 0.3}, {'cutoff': 0.5, 'bandwidth': 0.3}),  # Multiple parameters
    ])
    def test_update_with_different_params(self, observer, mock_audio_engine, params, expected_call):
        """Test update with different parameter combinations."""
        observer.update(params)
        mock_audio_engine.set_parameters.assert_called_once_with(**expected_call)
        
    def test_update_with_none_value(self, observer, mock_audio_engine):
        """Test update with None value in parameters."""
        params = {'cutoff': None}
        observer.update(params)
        mock_audio_engine.set_parameters.assert_called_once_with(**params)
        
    def test_multiple_error_logging(self, observer, mock_audio_engine):
        """Test multiple consecutive errors are logged."""
        errors = [
            ValueError("First error"),
            ValueError("Second error")
        ]
        mock_audio_engine.set_parameters.side_effect = errors
        
        with patch.object(observer.logger, 'error') as mock_logger:
            observer.update({'param1': 1})
            observer.update({'param2': 2})
            
            assert mock_logger.call_count == 2
            mock_logger.assert_has_calls([
                call("Parameter validation error: First error"),
                call("Parameter validation error: Second error")
            ], any_order=True)
            
    def test_generate_audio_callback_maintained(self, observer, mock_audio_engine, mock_audio_stream):
        """Test generate_audio callback remains correctly bound after updates."""
        # Initial check
        assert observer.audio_stream.generate_audio == mock_audio_engine.generate_noise
        
        # Update parameters and verify callback is still correct
        observer.update({'param': 'value'})
        assert observer.audio_stream.generate_audio == mock_audio_engine.generate_noise
        
    def test_start_already_started(self, observer, mock_audio_stream):
        """Test starting stream when it's already started."""
        # First start
        observer.start()
        mock_audio_stream.start.assert_called_once()
        
        # Reset mock and start again
        mock_audio_stream.start.reset_mock()
        observer.start()
        mock_audio_stream.start.assert_called_once()
        
    def test_stop_already_stopped(self, observer, mock_audio_stream):
        """Test stopping stream when it's already stopped."""
        # First stop
        observer.stop()
        mock_audio_stream.stop.assert_called_once()
        
        # Reset mock and stop again
        mock_audio_stream.stop.reset_mock()
        observer.stop()
        mock_audio_stream.stop.assert_called_once()
