import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Global seed for XOR-shift
seed = 12345

# XOR-shift function
def xor_shift(seed):
    """Generate a single XOR-shift pseudorandom number."""
    seed ^= (seed << 13) & 0xFFFFFFFF
    seed ^= (seed >> 17) & 0xFFFFFFFF
    seed ^= (seed << 5) & 0xFFFFFFFF
    return seed & 0xFFFFFFFF

# Generate noise with Markov chain-like behavior
def generate_markov_noise(frames, color_param):
    global seed
    noise = np.zeros(frames)

    for i in range(frames):
        seed = xor_shift(seed)
        raw_value = (seed / 0x7FFFFFFF) - 1.0  # Normalize to range [-1, 1]

        if i == 0:
            noise[i] = raw_value  # Initial value (no previous state)
        else:
            # Markov chain influence: more influence with higher color_param
            noise[i] = raw_value * color_param + noise[i - 1] * (1 - color_param)

    return noise

# Audio callback with sliders
def audio_callback(outdata, frames, time, status, sliders, sample_rate):
    global seed
    if status:
        print("Stream status:", status)

    # Fetch slider values dynamically
    color_param = sliders["color"].val
    volume = sliders["volume"].val

    # Generate noise using Markov chain-like behavior
    noise = generate_markov_noise(frames, color_param)

    # Apply volume control
    outdata[:] = (noise * volume).reshape(-1, 1)

# Real-time noise generator
def play_noise(sliders):
    """Stream noise in real-time."""
    sample_rate = 44100
    with sd.OutputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        callback=lambda outdata, frames, time, status: audio_callback(outdata, frames, time, status, sliders, sample_rate),
        blocksize=1024,
    ):
        print("Playing noise. Adjust the sliders.")
        plt.show()  # Block here to keep GUI open

# GUI for controlling parameters
def create_gui():
    # Create Matplotlib figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.5)

    ax.set_title("Noise Generator Parameters")
    ax.axis("off")

    # Color parameter slider (affects Markov chain behavior)
    ax_color = plt.axes([0.25, 0.25, 0.65, 0.03])
    color_slider = Slider(ax_color, "Color", 0.0, 1.0, valinit=0.0)

    # Volume slider
    ax_volume = plt.axes([0.25, 0.15, 0.65, 0.03])
    volume_slider = Slider(ax_volume, "Volume", 0.0, 1.0, valinit=0.5)

    # Store sliders in a dictionary for easy access
    sliders = {
        "color": color_slider,
        "volume": volume_slider,
    }

    # Start real-time noise generation with slider references
    play_noise(sliders)

# Main entry point
if __name__ == "__main__":
    create_gui()
