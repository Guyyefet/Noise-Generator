import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from observer import Subject, Observer

class NoiseGUI(Subject):
    def __init__(self):
        super().__init__()  # Initialize Subject's observer list
        self.fig, self.ax = plt.subplots()  # Create basic figure
        self.sliders = []  # Initialize empty sliders list
        self._setup_figure()  # Configure figure
        self._setup_sliders()  # Create and configure sliders

    def _setup_figure(self):
        """Configure the matplotlib figure."""
        plt.subplots_adjust(left=0.25, bottom=0.5)
        self.ax.set_title("Noise Generator Parameters")
        self.ax.axis("off")

    def _setup_sliders(self):
        """Create and configure all sliders."""
        # Slider parameters: (label, min, max, initial value)
        slider_params = [
            ("Color", 0.0, 1.0, 0.0),  # Color parameter (affects Markov chain behavior)
            ("Volume", 0.0, 1.0, 0.5)   # Volume control
        ]

        for i, (label, valmin, valmax, valinit) in enumerate(slider_params):
            ax_pos = [0.25, 0.25 - i*0.1, 0.65, 0.03]
            slider = Slider(
                plt.axes(ax_pos), 
                label, 
                valmin, 
                valmax, 
                valinit=valinit,
                color='lightblue'
            )
            slider.on_changed(self.notify)
            self.sliders.append(slider)

    def notify(self):
        """Notify observers with current parameter values."""
        values = [slider.val for slider in self.sliders]
        for observer in self.observers:
            observer.update(*values)  # Pass all values as separate arguments

    def show(self):
        """Display the GUI."""
        plt.show()

    def close(self):
        """Close the GUI window."""
        plt.close(self.fig)
