import numpy as np
import sounddevice as sd
from threading import Thread, Event
from observer import Observer

class NoiseEngine(Observer):
    def __init__(self):
        self._seed = 12345
        self._color_param = 0.0
        self._volume = 0.5
        self._stream = None
        self._stop_event = Event()
        self._audio_thread = None

    def update(self, color_param: float, volume: float) -> None:
        """Update parameters when notified by the GUI (Subject)."""
        self._color_param = color_param
        self._volume = volume

    def _xor_shift(self, seed: int) -> int:
        """Generate a single XOR-shift pseudorandom number."""
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF
        return seed & 0xFFFFFFFF

    def _generate_markov_noise(self, frames: int) -> np.ndarray:
        """Generate noise with Markov chain-like behavior."""
        noise = np.zeros(frames)

        for i in range(frames):
            self._seed = self._xor_shift(self._seed)
            raw_value = (self._seed / 0x7FFFFFFF) - 1.0  # Normalize to range [-1, 1]

            if i == 0:
                noise[i] = raw_value  # Initial value (no previous state)
            else:
                # Markov chain influence: more influence with higher color_param
                noise[i] = raw_value * self._color_param + noise[i - 1] * (1 - self._color_param)

        return noise

    def _audio_callback(self, outdata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
        """Audio callback for real-time noise generation."""
        if status:
            print("Stream status:", status)

        if self._stop_event.is_set():
            raise sd.CallbackStop()

        noise = self._generate_markov_noise(frames)
        outdata[:] = (noise * self._volume).reshape(-1, 1)

    def _audio_stream_thread(self) -> None:
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
        """Start noise generation in a separate thread."""
        if self._audio_thread is None or not self._audio_thread.is_alive():
            self._stop_event.clear()
            self._audio_thread = Thread(target=self._audio_stream_thread, daemon=True)
            self._audio_thread.start()

    def stop(self) -> None:
        """Stop noise generation and cleanup."""
        if self._audio_thread and self._audio_thread.is_alive():
            self._stop_event.set()
            self._audio_thread.join(timeout=1.0)  # Wait for thread to finish
            if self._stream:
                self._stream.close()
                self._stream = None
