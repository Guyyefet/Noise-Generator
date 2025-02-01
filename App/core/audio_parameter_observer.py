from core.observer import Observer
from core.audio_engine import AudioEngineBase
from core.audio_stream import AudioStream

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

    def update(self, parameters: dict):
        """
        Update audio parameters when notified by GUI (Subject).
        
        Args:
            parameters: Dictionary of parameter key-value pairs
        """
        # Pass through all parameters directly to the engine
        self.audio_engine.set_parameters(**parameters)

    def start(self):
        """Start audio streaming."""
        self.audio_stream.start()

    def stop(self):
        """Stop audio streaming."""
        self.audio_stream.stop()
