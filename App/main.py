from noise_engine import NoiseEngine
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
        # Create the GUI (Subject)
        gui = NoiseGUI()
        
        # Create the noise engine (Observer)
        noise_engine = NoiseEngine()
        
        # Attach noise engine as observer to GUI
        gui.attach(noise_engine)
        
        # Start noise generation (in separate thread)
        noise_engine.start()
        
        # Initial notification to set starting values
        gui.notify()
        
        # Show GUI (this will block until window is closed)
        gui.show()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        noise_engine.stop()
        gui.close()

if __name__ == "__main__":
    main()
