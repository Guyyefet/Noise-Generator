import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import threading
import time
from App.core.audio_stream import AudioStream

class TestAudioStream:
    @pytest.fixture
    def mock_callback(self):
        """Create a mock audio generation callback."""
        def callback(frames):
            return np.zeros(frames)
        return Mock(side_effect=callback)
    
    @pytest.fixture
    def mock_waveform_view(self):
        """Create a mock waveform view."""
        return Mock()
    
    @pytest.fixture
    def mock_sounddevice(self):
        """Mock the sounddevice module."""
        with patch('App.core.audio_stream.sd') as mock_sd:
            # Mock OutputStream context manager
            mock_stream = MagicMock()
            mock_sd.OutputStream.return_value.__enter__.return_value = mock_stream
            yield mock_sd
    
    def test_initialization(self, mock_callback, mock_waveform_view):
        """Test stream initialization."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        
        assert stream.generate_audio == mock_callback
        assert stream.waveform_view == mock_waveform_view
        assert stream.stream is None
        assert isinstance(stream.stop_event, threading.Event)
        assert not stream.stop_event.is_set()
        assert stream.audio_thread is None
    
    def test_audio_callback(self, mock_callback, mock_waveform_view):
        """Test audio callback behavior."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        frames = 1000
        outdata = np.zeros((frames, 1))
        time_info = 0.0
        status = None
        
        # Test normal callback
        stream.audio_callback(outdata, frames, time_info, status)
        mock_callback.assert_called_once_with(frames)
        mock_waveform_view.update_waveform.assert_called_once()
        
        # Test callback with stop event set
        stream.stop_event.set()
        with pytest.raises(Exception):  # Should raise CallbackStop
            stream.audio_callback(outdata, frames, time_info, status)
    
    def test_stream_thread(self, mock_callback, mock_sounddevice):
        """Test audio streaming thread."""
        stream = AudioStream(mock_callback)
        
        # Start stream in background
        stream.start()
        time.sleep(0.1)  # Give thread time to start
        assert stream.audio_thread.is_alive()
        
        # Get the args from the actual call
        assert mock_sounddevice.OutputStream.call_count == 1
        call_args = mock_sounddevice.OutputStream.call_args
        
        # Verify sounddevice configuration
        assert call_args.kwargs['samplerate'] == 44100
        assert call_args.kwargs['channels'] == 1
        assert call_args.kwargs['dtype'] == "float32"
        assert call_args.kwargs['callback'] == stream.audio_callback
        assert call_args.kwargs['blocksize'] == 2048
        assert call_args.kwargs['latency'] == 'high'
        
        # Get mock stream and verify it started
        mock_stream = mock_sounddevice.OutputStream.return_value.__enter__.return_value
        mock_stream.start.assert_called_once()
        
        # Stop stream and verify cleanup
        stream.stop()
        time.sleep(0.1)  # Give thread time to stop
        assert not stream.audio_thread.is_alive()
        assert stream.stream is None
    
    def test_start_stop(self, mock_callback, mock_sounddevice):
        """Test start/stop behavior."""
        stream = AudioStream(mock_callback)
        
        # Test start
        stream.start()
        assert stream.audio_thread.is_alive()
        assert not stream.stop_event.is_set()
        
        # Test second start (should not create new thread)
        original_thread = stream.audio_thread
        stream.start()
        assert stream.audio_thread == original_thread
        
        # Test stop
        stream.stop()
        assert not stream.audio_thread.is_alive()
        assert stream.stop_event.is_set()
        assert stream.stream is None
    
    def test_error_handling(self, mock_callback):
        """Test error handling in stream thread."""
        stream = AudioStream(mock_callback)
        
        # Mock sounddevice to raise an error
        with patch('App.core.audio_stream.sd.OutputStream') as mock_output_stream:
            mock_output_stream.side_effect = Exception("Test error")
            
            # Start stream (should handle error gracefully)
            stream.start()
            time.sleep(0.1)  # Give thread time to run
            
            assert stream.stream is None
            stream.stop()  # Cleanup
    
    def test_waveform_update(self, mock_callback, mock_waveform_view):
        """Test waveform view updates."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        frames = 1000
        outdata = np.zeros((frames, 1))
        
        # Test callback with waveform view
        stream.audio_callback(outdata, frames, 0.0, None)
        mock_waveform_view.update_waveform.assert_called_once()
        
        # Test callback without waveform view
        stream.waveform_view = None
        stream.audio_callback(outdata, frames, 0.0, None)
        # Should not cause any errors
    
    def test_callback_error_handling(self, mock_callback, mock_waveform_view):
        """Test error handling in audio callback."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        frames = 1000
        outdata = np.zeros((frames, 1))
        
        # Test callback status error
        with patch('builtins.print') as mock_print:
            stream.audio_callback(outdata, frames, 0.0, "Error status")
            mock_print.assert_called_once_with("Stream status:", "Error status")
    
    def test_callback_data_handling(self, mock_callback, mock_waveform_view):
        """Test audio data handling in callback."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        frames = 1000
        outdata = np.zeros((frames, 1))
        
        # Configure callback to return specific data
        test_data = np.linspace(-1, 1, frames)
        mock_callback.side_effect = lambda x: test_data
        
        # Test data copying to output buffer
        stream.audio_callback(outdata, frames, 0.0, None)
        np.testing.assert_array_equal(outdata.flatten(), test_data)
    
    def test_thread_cleanup(self, mock_callback, mock_sounddevice):
        """Test thread cleanup on errors."""
        stream = AudioStream(mock_callback)
        
        # Configure stream to raise error during execution
        mock_stream = mock_sounddevice.OutputStream.return_value.__enter__.return_value
        mock_stream.start.side_effect = Exception("Stream error")
        
        # Start stream
        stream.start()
        time.sleep(0.1)  # Give thread time to run
        
        # Verify cleanup occurred
        assert not stream.audio_thread.is_alive()
        assert stream.stream is None
    
    def test_concurrent_start_stop(self, mock_callback, mock_sounddevice):
        """Test concurrent start/stop operations."""
        stream = AudioStream(mock_callback)
        
        # Start multiple times rapidly
        for _ in range(5):
            stream.start()
            time.sleep(0.01)
        
        # Verify only one thread running
        assert stream.audio_thread.is_alive()
        assert len([t for t in threading.enumerate() if t.name == 'AudioThread']) == 1
        
        # Stop multiple times rapidly
        for _ in range(5):
            stream.stop()
            time.sleep(0.01)
        
        # Verify cleanup
        assert not stream.audio_thread.is_alive()
        assert stream.stream is None
    
    def test_callback_thread_safety(self, mock_callback, mock_waveform_view):
        """Test thread safety of audio callback."""
        stream = AudioStream(mock_callback, mock_waveform_view)
        frames = 1000
        outdata = np.zeros((frames, 1))
        
        # Simulate concurrent callbacks
        def concurrent_callback():
            for _ in range(10):
                stream.audio_callback(outdata.copy(), frames, 0.0, None)
        
        threads = [threading.Thread(target=concurrent_callback) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify callback was called expected number of times
        assert mock_callback.call_count == 30  # 3 threads * 10 calls each
