from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QSlider, QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from App.core.processors.processor_factory import AudioProcessorFactory
from App.core.parameters.parameter_system import ParameterRegistry

class NoiseControlsWidget(QWidget):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.parameter_controls = {}  # Store controls by parameter name
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add combo boxes for selecting generators and filters
        self._add_combo_boxes(layout)

        # Add parameter controls
        self._add_parameter_controls(layout)

    def _add_combo_boxes(self, layout):
        """Add combo boxes for selecting generators and filters."""
        # Generator selection
        generator_layout = QHBoxLayout()
        generator_label = QLabel("Generator:")
        self.generator_combo = QComboBox()
        generator_layout.addWidget(generator_label)
        generator_layout.addWidget(self.generator_combo)
        layout.addLayout(generator_layout)

        # Filter selection
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter:")
        self.filter_combo = QComboBox()
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        layout.addLayout(filter_layout)

        # Populate combo boxes
        self._populate_generators()
        self._populate_filters()

        # Connect signals
        self.generator_combo.currentTextChanged.connect(self._on_generator_changed)
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)

    def _populate_generators(self):
        """Populate the generator combo box."""
        noise_generators = AudioProcessorFactory.get_processors_by_category(category="noise")
        for generator in noise_generators:
            self.generator_combo.addItem(generator.name)

    def _populate_filters(self):
        """Populate the filter combo box."""
        filters = AudioProcessorFactory.get_processors_by_category(category="filter")
        for filter_proc in filters:
            self.filter_combo.addItem(filter_proc.name)

    def _add_parameter_controls(self, layout):
        """Add controls for adjusting parameters."""
        # Get initial processor parameters
        if self.generator_combo.currentText():
            processor_info = AudioProcessorFactory.get_processor_info(self.generator_combo.currentText())
            if processor_info:
                self._create_parameter_controls(layout, processor_info.parameters)

    def _create_parameter_controls(self, layout, parameters):
        """Create controls for a set of parameters."""
        # Clear existing controls
        for control in self.parameter_controls.values():
            control.setParent(None)
        self.parameter_controls.clear()

        # Create new controls
        for param_name, param_def in parameters.items():
            param_layout = QHBoxLayout()
            
            # Add label
            label = QLabel(param_def["display_name"] or param_name)
            param_layout.addWidget(label)
            
            # Create appropriate control based on parameter type
            control = self._create_parameter_control(param_name, param_def)
            if control:
                param_layout.addWidget(control)
                layout.addLayout(param_layout)
                self.parameter_controls[param_name] = control

    def _create_parameter_control(self, param_name, param_def):
        """Create an appropriate control widget for the parameter."""
        if param_def["type"] == "float":
            control = QDoubleSpinBox()
            if param_def["range"]:
                control.setRange(param_def["range"].min_value, param_def["range"].max_value)
            control.setValue(param_def["default_value"])
            if param_def["units"]:
                control.setSuffix(f" {param_def['units']}")
            return control
            
        elif param_def["type"] == "int":
            control = QSpinBox()
            if param_def["range"]:
                control.setRange(param_def["range"].min_value, param_def["range"].max_value)
            control.setValue(param_def["default_value"])
            if param_def["units"]:
                control.setSuffix(f" {param_def['units']}")
            return control
            
        elif param_def["type"] == "enum":
            control = QComboBox()
            control.addItems(param_def["enum_values"])
            index = control.findText(param_def["default_value"])
            if index >= 0:
                control.setCurrentIndex(index)
            return control
            
        return None

    def _on_generator_changed(self, generator_name):
        """Handle generator selection change."""
        if generator_name:
            processor_info = AudioProcessorFactory.get_processor_info(generator_name)
            if processor_info:
                self._create_parameter_controls(self.layout(), processor_info.parameters)

    def _on_filter_changed(self, filter_name):
        """Handle filter selection change."""
        if filter_name:
            processor_info = AudioProcessorFactory.get_processor_info(filter_name)
            if processor_info:
                self._create_parameter_controls(self.layout(), processor_info.parameters)
