from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QComboBox
from PyQt6.QtCore import Qt
from core.noise_parameters import NoiseParameters

class NoiseControlsWidget(QWidget):
    """Widget containing noise parameter controls."""
    
    def __init__(self, parameters: NoiseParameters):
        super().__init__()
        self.parameters = parameters
        self.sliders = []
        self.generator_combo = None
        self.filter_combo = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Left, Top, Right, Bottom margins
        layout.setSpacing(10)  # Space between widgets
        
        # Add generator type selector
        generator_label = QLabel("Generator Type")
        layout.addWidget(generator_label)
        self.generator_combo = QComboBox()
        self.generator_combo.addItems(["White Noise"])  # More types can be added later
        self.generator_combo.currentTextChanged.connect(self._on_selection_changed)
        layout.addWidget(self.generator_combo)
        
        # Add filter type selector
        filter_label = QLabel("Filter Type")
        layout.addWidget(filter_label)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Bandpass"])  # More types can be added later
        self.filter_combo.currentTextChanged.connect(self._on_selection_changed)
        layout.addWidget(self.filter_combo)
        
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
        self._update_all_parameters(values)
    
    def _on_selection_changed(self):
        """Handle combo box selection changes."""
        values = [slider.value() / 1000.0 for slider in self.sliders]
        self._update_all_parameters(values)
    
    def _update_all_parameters(self, slider_values):
        """Update all parameters including selections."""
        generator_type = self.generator_combo.currentText()
        filter_type = self.filter_combo.currentText()
        self.parameters.update_parameters(
            generator_type=generator_type,
            filter_type=filter_type,
            volume=slider_values[0],
            cutoff=slider_values[1],
            bandwidth=slider_values[2]
        )
