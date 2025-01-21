from observer import Observer
from audio_engine import AudioEngine
from audio_stream import AudioStream

class AudioParameterObserver(Observer):
    """Observes GUI parameter changes and coordinates audio components."""
    
    def __init__(self, audio_engine: AudioEngine, audio_stream: AudioStream):
        """
        Initialize with audio components.
        
        Args:
            audio_engine: Component that generates audio
            audio_stream: Component that handles audio output
        """
        self._audio_engine = audio_engine
        self._audio_stream = audio_stream
        
        # Connect audio engine to stream
        self._audio_stream._generate_audio = self._audio_engine.generate_noise

    def update(self, color_param: float, volume: float) -> None:
        """Update audio parameters when notified by GUI (Subject)."""
        self._audio_engine.set_parameters(color_param, volume)

    def start(self) -> None:
        """Start audio streaming."""
        self._audio_stream.start()

    def stop(self) -> None:
        """Stop audio streaming."""
        self._audio_stream.stop()
