from core.audio_engine import BandpassAudioEngine
from core.audio_stream import AudioStream
from core.audio_parameter_observer import AudioParameterObserver
from core.noise_parameters import NoiseParameters
from core.processor_registry import register_processors
from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import signal
import sys

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    print("\nSignal received. Cleaning up...")
    sys.exit(0)

def main():
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize Qt Application
    app = QApplication(sys.argv)
    
    # Register available processors
    register_processors()
    
    # Create components
    parameters = NoiseParameters()
    audio_engine = BandpassAudioEngine()  # Uses default noise+bandpass config
    
    # Create and show main window first to have access to waveform view
    window = MainWindow(parameters)
    window.show()
    
    # Create audio stream with waveform view
    audio_stream = AudioStream(lambda x: None, window.waveform_view)
    audio_observer = AudioParameterObserver(audio_engine, audio_stream)
    parameters.attach(audio_observer)
    
    try:
        
        # Start audio processing
        audio_observer.start()
        
        # Run Qt event loop
        app.exec()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup audio
        audio_observer.stop()

if __name__ == "__main__":
    main()
