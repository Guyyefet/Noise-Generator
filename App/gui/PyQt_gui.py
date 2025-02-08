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
        
        # Add combo boxes at the top
        self._add_combo_boxes(layout)
        
        # Create container for parameter sliders
        self.param_container = QWidget()
        self.param_layout = QVBoxLayout(self.param_container)
        layout.addWidget(self.param_container)
        
        # Initialize with default filter parameters
        self._update_parameter_controls()
        
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
    
    def _add_combo_boxes(self, layout):
        """Add generator and filter type selectors."""
        # Add generator type selector
        generator_label = QLabel("Generator Type")
        layout.addWidget(generator_label)
        self.generator_combo = QComboBox()
        self.generator_combo.addItems(["XOR Shift Noise"])
        self.generator_combo.currentTextChanged.connect(self._on_selection_changed)
        layout.addWidget(self.generator_combo)
        
        # Add filter type selector
        filter_label = QLabel("Filter Type")
        layout.addWidget(filter_label)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Bandpass", "Lowpass"])
        self.filter_combo.currentTextChanged.connect(self._on_selection_changed)
        layout.addWidget(self.filter_combo)

    def _update_parameter_controls(self):
        """Update parameter controls based on current filter type."""
        # Clear existing controls
        while self.param_layout.count():
            child = self.param_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.sliders.clear()
        
        # Get current filter type
        filter_type = self.filter_combo.currentText()
        
        # Define filter-specific parameters
        filter_params = {
            "Bandpass": ["bandwidth"],
            "Lowpass": ["resonance", "poles"]
        }
        
        # Common parameters for all filters
        common_params = ["cutoff", "volume"]
        
        # Combine filter-specific and common parameters
        params_to_show = filter_params[filter_type] + common_params
        
        # Create sliders for selected parameters
        for param_name in params_to_show:
            definition = self.registry.get_definition(param_name)
            
            # Create label
            label_text = f"{definition.display_name}"
            if definition.units:
                label_text += f" ({definition.units})"
            label = QLabel(label_text)
            self.param_layout.addWidget(label)
            
            # Create slider
            slider = QSlider(Qt.Orientation.Horizontal)
            
            if definition.range:
                min_val = definition.range.min_value
                max_val = definition.range.max_value
                resolution = 1000
                slider.setMinimum(0)
                slider.setMaximum(resolution)
                # Get current value from parameters if it exists, otherwise use default
                current_value = self.parameters.get_parameter(param_name, definition.default_value)
                slider.setValue(int(
                    (current_value - min_val) / 
                    (max_val - min_val) * resolution
                ))
                slider.setPageStep(0)
                
                self.sliders[param_name] = slider
                slider.valueChanged.connect(self._on_slider_changed)
                self.param_layout.addWidget(slider)

    def _on_selection_changed(self):
        """Handle combo box selection changes."""
        # First update the UI to show correct parameters
        self._update_parameter_controls()
        
        # Get current values for all visible parameters
        params = {
            "generator_type": self.generator_combo.currentText(),
            "filter_type": self.filter_combo.currentText()
        }
        
        # Add current values from all visible sliders
        for param_name, slider in self.sliders.items():
            definition = self.registry.get_definition(param_name)
            if definition.range:
                min_val = definition.range.min_value
                max_val = definition.range.max_value
                resolution = slider.maximum()
                value = min_val + (slider.value() / resolution) * (max_val - min_val)
                params[param_name] = value
                
        # Update all parameters at once
        self._update_parameters(params)
    
    def _update_parameters(self, params: Dict[str, Any]):
        """Update parameters with validation."""
        try:
            self.parameters.update_parameters(**params)
        except (ValueError, KeyError) as e:
            # Log error but continue with valid parameters
            print(f"Parameter update error: {str(e)}")
