from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from core.noise_parameters import NoiseParameters
from gui.PyQt_gui import NoiseControlsWidget
from gui.waveform_view import WaveformView

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, parameters: NoiseParameters):
        super().__init__()
        self.setWindowTitle("Noise Playground")
        self.resize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Add noise controls
        controls = NoiseControlsWidget(parameters)
        left_layout.addWidget(controls)
        left_layout.addStretch()  # Push controls to top
        
        # Create waveform view
        self.waveform_view = WaveformView()
        
        # Add widgets to main layout
        main_layout.addWidget(left_panel, stretch=1)  # Controls take 1/4 of width
        main_layout.addWidget(self.waveform_view, stretch=3)  # Waveform takes 3/4 of width
