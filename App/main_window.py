from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from new_gui import NoiseControlsWidget
from noise_parameters import NoiseParameters

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, parameters: NoiseParameters):
        super().__init__()
        self.setWindowTitle("Noise Playground")
        self.resize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add noise controls
        controls = NoiseControlsWidget(parameters)
        layout.addWidget(controls)
        
        # Future: Add visualization widget here
