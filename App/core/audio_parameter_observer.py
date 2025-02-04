from .observer import Observer
from .audio_engine import AudioEngineBase
from .audio_stream import AudioStream
import logging
from typing import Dict, Any

class AudioParameterObserver(Observer):
    """Observes GUI parameter changes and coordinates audio components."""
    
    def __init__(self, audio_engine: AudioEngineBase, audio_stream: AudioStream):
        """
        Initialize with audio components.
        
        Args:
            audio_engine: Component that generates audio
            audio_stream: Component that handles audio output
        """
        self.audio_engine = audio_engine
        self.audio_stream = audio_stream
        
        # Connect audio engine to stream
        self.audio_stream.generate_audio = self.audio_engine.generate_noise
        
        # Set up logging
        self.logger = logging.getLogger(__name__)

    def update(self, parameters: Dict[str, Any]):
        """
        Update audio parameters when notified by GUI (Subject).
        
        Args:
            parameters: Dictionary of parameter key-value pairs
        """
        try:
            # Pass validated parameters to the engine
            self.audio_engine.set_parameters(**parameters)
        except (ValueError, KeyError) as e:
            # Log validation errors but continue with valid parameters
            self.logger.error(f"Parameter validation error: {str(e)}")
            # Could add GUI feedback here in the future

    def start(self):
        """Start audio streaming."""
        try:
            self.audio_stream.start()
        except Exception as e:
            self.logger.error(f"Failed to start audio stream: {str(e)}")
            raise

    def stop(self):
        """Stop audio streaming."""
        try:
            self.audio_stream.stop()
        except Exception as e:
            self.logger.error(f"Failed to stop audio stream: {str(e)}")
            raise
