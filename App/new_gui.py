from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt
from noise_parameters import NoiseParameters

class NoiseControlsWidget(QWidget):
    """Widget containing noise parameter controls."""
    
    def __init__(self, parameters: NoiseParameters):
        super().__init__()
        self.parameters = parameters
        self.sliders = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Left, Top, Right, Bottom margins
        layout.setSpacing(10)  # Space between widgets
        
        # Create sliders with same ranges as current GUI
        slider_params = [
            ("Volume", 0.0, 1.0, 0.5),
            ("Filter cutoff", 0.0, 1.0, 0.5),
            ("Bandwidth", 0.0, 1.0, 0.5)
        ]
        
        for label_text, min_val, max_val, default in slider_params:
            # Create label
            label = QLabel(label_text)
            layout.addWidget(label)
            
            # Create slider
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(1000)  # Use finer resolution
            slider.setValue(int(default * 1000))
            slider.setPageStep(0)  # Make it continuous
            slider.valueChanged.connect(self._on_slider_changed)
            self.sliders.append(slider)
            layout.addWidget(slider)
        
        self.setLayout(layout)
    
    def _on_slider_changed(self):
        """Handle slider value changes."""
        # Convert slider integer values back to 0-1 range
        values = [slider.value() / 1000.0 for slider in self.sliders]
        self.parameters.update_parameters(*values)
