import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from observer import Subject, Observer

class NoiseGUI(Subject):
    def __init__(self):
        super().__init__()  # Initialize Subject's observer list
        
        # Create Matplotlib figure
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.5)

        self.ax.set_title("Noise Generator Parameters")
        self.ax.axis("off")

        # Color parameter slider (affects Markov chain behavior)
        ax_color = plt.axes([0.25, 0.25, 0.65, 0.03])
        self.color_slider = Slider(ax_color, "Color", 0.0, 1.0, valinit=0.0)

        # Volume slider
        ax_volume = plt.axes([0.25, 0.15, 0.65, 0.03])
        self.volume_slider = Slider(ax_volume, "Volume", 0.0, 1.0, valinit=0.5)

        # Register update callback
        self.color_slider.on_changed(self._on_parameter_change)
        self.volume_slider.on_changed(self._on_parameter_change)

    def notify(self) -> None:
        """Notify all observers with current parameter values."""
        for observer in self._observers:
            observer.update(self.color_slider.val, self.volume_slider.val)

    def _on_parameter_change(self, _) -> None:
        """Called when any slider value changes."""
        self.notify()

    def show(self) -> None:
        """Display the GUI."""
        plt.show()

    def close(self) -> None:
        """Close the GUI window."""
        plt.close(self.fig)
