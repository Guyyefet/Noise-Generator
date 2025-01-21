from audio_engine import AudioEngine
from audio_stream import AudioStream
from audio_parameter_observer import AudioParameterObserver
from gui import NoiseGUI
import signal
import sys

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    print("\nSignal received. Cleaning up...")
    sys.exit(0)

def main():
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Create audio components
        audio_engine = AudioEngine()
        audio_stream = AudioStream(lambda x: None)  # Placeholder callback, will be set by observer
        
        # Create observer and connect it to audio components
        audio_observer = AudioParameterObserver(audio_engine, audio_stream)
        
        # Create GUI and attach observer
        gui = NoiseGUI()
        gui.attach(audio_observer)
        
        # Start audio processing
        audio_observer.start()
        
        # Initial parameter notification
        gui.notify()
        
        # Show GUI (this will block until window is closed)
        gui.show()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        audio_observer.stop()
        gui.close()

if __name__ == "__main__":
    main()
