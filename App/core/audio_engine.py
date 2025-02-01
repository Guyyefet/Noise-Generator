from .strategies.bandpass import BandpassStrategy

class AudioEngine:
    """Handles audio generation using configurable strategies."""
    
    def __init__(self):
        # Initialize with default bandpass strategy
        self.strategy = BandpassStrategy()
        self.parameters = {
            'volume': 0.5,
            'cutoff': 0.5,
            'bandwidth': 0.5
        }

    def set_parameters(self, color: float, volume: float, cutoff: float, bandwidth: float):
        """Set sound generation parameters."""
        self.parameters.update({
            'volume': volume,
            'cutoff': cutoff,
            'bandwidth': bandwidth
        })

    def generate_noise(self, frames: int):
        """Generate noise using current strategy."""
        return self.strategy.process_audio(frames, self.parameters)
