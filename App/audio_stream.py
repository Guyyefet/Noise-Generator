import sounddevice as sd
import numpy as np
from threading import Thread, Event
from typing import Callable, Optional

class AudioStream:
    def __init__(self, callback: Callable[[int], np.ndarray]):
        """
        Initialize audio stream with a callback that generates audio data.
        
        Args:
            callback: Function that takes number of frames and returns numpy array of audio data
        """
        self._generate_audio = callback
        self._stream: Optional[sd.OutputStream] = None
        self._stop_event = Event()
        self._audio_thread: Optional[Thread] = None
        
    def _audio_callback(self, outdata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
        """Audio callback for real-time audio generation."""
        if status:
            print("Stream status:", status)

        if self._stop_event.is_set():
            raise sd.CallbackStop()

        audio_data = self._generate_audio(frames)
        outdata[:] = audio_data.reshape(-1, 1)

    def _stream_thread(self) -> None:
        """Thread function for audio streaming."""
        try:
            with sd.OutputStream(
                samplerate=44100,
                channels=1,
                dtype="float32",
                callback=self._audio_callback,
                blocksize=1024,
            ) as stream:
                self._stream = stream
                stream.start()
                self._stop_event.wait()  # Wait until stop is requested
        except Exception as e:
            print(f"Audio stream error: {e}")
        finally:
            self._stream = None

    def start(self) -> None:
        """Start audio streaming in a separate thread."""
        if self._audio_thread is None or not self._audio_thread.is_alive():
            self._stop_event.clear()
            self._audio_thread = Thread(target=self._stream_thread, daemon=True)
            self._audio_thread.start()

    def stop(self) -> None:
        """Stop audio streaming and cleanup."""
        if self._audio_thread and self._audio_thread.is_alive():
            self._stop_event.set()
            self._audio_thread.join(timeout=1.0)  # Wait for thread to finish
            if self._stream:
                self._stream.close()
                self._stream = None
