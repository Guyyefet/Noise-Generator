"""
Audio Stream Module - Handles real-time audio streaming using sounddevice library.
"""

import sounddevice as sd
import numpy as np
from threading import Thread, Event
from typing import Callable

class AudioStream:
    """Handles real-time audio streaming with callback-based audio generation."""
    
    def __init__(self, callback: Callable[[int], np.ndarray], waveform_view=None):
        """
        Initialize audio stream with callback function for audio generation.
        
        Args:
            callback: Function that generates audio data
            waveform_view: Optional WaveformView widget for visualization
        """
        self.generate_audio = callback
        self.stream = None
        self.stop_event = Event()
        self.audio_thread = None
        self.waveform_view = waveform_view
        
    def audio_callback(self, outdata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags):
        """
        Called by sounddevice to get audio data for playback.
        """
        if status:
            print("Stream status:", status)

        if self.stop_event.is_set():
            raise sd.CallbackStop()

        audio_data = self.generate_audio(frames)
        outdata[:] = audio_data.reshape(-1, 1)
        
        # Update waveform if view is available
        if self.waveform_view:
            self.waveform_view.update_waveform(audio_data)

    def stream_thread(self):
        """
        Runs the audio stream in a separate thread.
        """
        try:
            with sd.OutputStream(
                samplerate=44100,
                channels=1,
                dtype="float32",
                callback=self.audio_callback,
                blocksize=2048,  # Larger buffer for better performance
                latency='high',  # Prefer stability over low latency
            ) as stream:
                self.stream = stream
                stream.start()
                self.stop_event.wait()
        except Exception as e:
            print(f"Audio stream error: {e}")
        finally:
            self.stream = None

    def start(self):
        """Start audio streaming in a separate thread."""
        if self.audio_thread is None or not self.audio_thread.is_alive():
            self.stop_event.clear()
            self.audio_thread = Thread(
                target=self.stream_thread,
                daemon=True,
                name="AudioThread"
            )
            self.audio_thread.start()

    def stop(self):
        """Stop audio streaming and clean up resources."""
        if self.audio_thread and self.audio_thread.is_alive():
            self.stop_event.set()
            self.audio_thread.join(timeout=1.0)
            if self.stream:
                self.stream.close()
                self.stream = None
