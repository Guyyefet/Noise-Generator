from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSlot, QTimer
import pyqtgraph as pg
import numpy as np

class WaveformView(QWidget):
    """Widget for displaying the audio waveform."""
    
    def __init__(self):
        super().__init__()
        
        # Buffer for storing waveform data (match audio blocksize)
        self.buffer_size = 2048
        self.time_data = np.linspace(0, self.buffer_size, self.buffer_size)
        self.waveform_buffer = np.zeros(self.buffer_size)
        
        # Set up update timer with lower rate
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_plot)
        self.update_timer.start(50)  # 20 FPS
        
        # Downsample factor for visualization
        self.downsample = 2  # Show every 2nd sample
        
        # Pre-allocate numpy array for efficiency
        self.plot_data = np.zeros(self.buffer_size)
        
        # Flag for new data
        self.has_new_data = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create plot widget with disabled interactions
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # White background
        self.plot_widget.setMouseEnabled(x=False, y=False)  # Disable mouse interactions
        self.plot_widget.getViewBox().setMenuEnabled(False)  # Disable right-click menu
        
        # Set up axis labels and fixed ranges
        self.plot_widget.setLabel('left', 'Amplitude (dB)')
        self.plot_widget.setLabel('bottom', 'Time (ms)')
        self.plot_widget.setYRange(-60, 0, padding=0)  # -60dB to 0dB range without padding
        self.plot_widget.getViewBox().setLimits(xMin=0, yMin=-60, yMax=0)  # Lock axis limits
        
        # Configure grid with common dB intervals
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        y_axis = self.plot_widget.getAxis('left')
        y_ticks = [-60, -48, -36, -24, -12, 0]  # Common dB intervals
        y_axis.setTicks([[(v, str(v)) for v in y_ticks]])
        
        # Calculate time in milliseconds (assuming 44.1kHz sample rate)
        ms_per_sample = 1000 / 44100  # milliseconds per sample
        self.time_data = np.linspace(0, self.buffer_size * ms_per_sample, self.buffer_size)
        
        # Create plot curve
        pen = pg.mkPen(color='b', width=2)
        self.curve = self.plot_widget.plot(pen=pen)
        
        # Create downsampled arrays
        self.display_size = self.buffer_size // self.downsample
        self.display_time = np.linspace(0, self.buffer_size * ms_per_sample, self.display_size)
        self.display_data = np.zeros(self.display_size)
        
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
    
    
    def update_waveform(self, data: np.ndarray):
        """Update the waveform display with new data."""
        if not self.isVisible():
            return
            
        # Update buffer with new data
        self.waveform_buffer = np.roll(self.waveform_buffer, -len(data))
        self.waveform_buffer[-len(data):] = data
        self.has_new_data = True
    
    def _update_plot(self):
        """Update the plot if there's new data."""
        if self.has_new_data and self.isVisible():
            # Downsample data for display
            self.display_data = self.waveform_buffer[::self.downsample]
            
            # Convert to dB (20 * log10(abs(amplitude)))
            # Use clip to avoid log(0), and set minimum to -60dB
            db_data = 20 * np.log10(np.clip(np.abs(self.display_data), 1e-3, None))
            db_data = np.clip(db_data, -60, 0)
            
            self.curve.setData(self.display_time, db_data)
            self.has_new_data = False
