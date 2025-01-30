from audio_engine import AudioEngine
from audio_stream import AudioStream
from audio_parameter_observer import AudioParameterObserver
from noise_parameters import NoiseParameters
from main_window import MainWindow
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
    
    # Create components
    parameters = NoiseParameters()
    audio_engine = AudioEngine()
    audio_stream = AudioStream(lambda x: None)
    audio_observer = AudioParameterObserver(audio_engine, audio_stream)
    parameters.attach(audio_observer)
    
    try:
        # Create and show main window
        window = MainWindow(parameters)
        window.show()
        
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
