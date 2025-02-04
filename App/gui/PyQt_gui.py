from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QComboBox
from PyQt6.QtCore import Qt
from core.parameters.noise_parameters import NoiseParameters
from core.parameters.parameter_definitions import get_registry
from typing import Dict, Any

class NoiseControlsWidget(QWidget):
    """Widget containing noise parameter controls."""
    
    def __init__(self, parameters: NoiseParameters):
        super().__init__()
        self.parameters = parameters
        self.registry = get_registry()
        self.sliders: Dict[str, QSlider] = {}
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
        
        # Create sliders based on parameter definitions
        for definition in self.registry.get_all_definitions():
            # Create label with display name and units
            label_text = f"{definition.display_name}"
            if definition.units:
                label_text += f" ({definition.units})"
            label = QLabel(label_text)
            layout.addWidget(label)
            
            # Create slider with proper range and resolution
            slider = QSlider(Qt.Orientation.Horizontal)
            
            # Set range based on parameter definition
            if definition.range:
                min_val = definition.range.min_value
                max_val = definition.range.max_value
                resolution = 1000  # Steps between min and max
                slider.setMinimum(0)
                slider.setMaximum(resolution)
                slider.setValue(int(
                    (definition.default_value - min_val) / 
                    (max_val - min_val) * resolution
                ))
                slider.setPageStep(0)  # Make it continuous
                
                # Store mapping from slider to parameter name
                self.sliders[definition.name] = slider
                slider.valueChanged.connect(self._on_slider_changed)
                layout.addWidget(slider)
        
        self.setLayout(layout)
    
    def _on_slider_changed(self):
        """Handle slider value changes."""
        params = {}
        for param_name, slider in self.sliders.items():
            definition = self.registry.get_definition(param_name)
            if definition.range:
                # Convert slider value back to parameter range
                min_val = definition.range.min_value
                max_val = definition.range.max_value
                resolution = slider.maximum()
                value = min_val + (slider.value() / resolution) * (max_val - min_val)
                params[param_name] = value
        self._update_parameters(params)
    
    def _on_selection_changed(self):
        """Handle combo box selection changes."""
        self._update_parameters({
            "generator_type": self.generator_combo.currentText(),
            "filter_type": self.filter_combo.currentText()
        })
    
    def _update_parameters(self, params: Dict[str, Any]):
        """Update parameters with validation."""
        try:
            self.parameters.update_parameters(**params)
        except (ValueError, KeyError) as e:
            # Log error but continue with valid parameters
            print(f"Parameter update error: {str(e)}")
