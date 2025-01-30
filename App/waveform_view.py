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
        
        # # Peak level tracking
        # self.peak_level = -60
        # self.peak_decay = 0.5  # dB per update (faster decay)
        # self.peak_hold_time = 1000  # Hold peak for 1 second
        # self.peak_hold_timer = QTimer()
        # self.peak_hold_timer.timeout.connect(self._reset_peak)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # White background
        
        # Set up axis labels and ranges
        self.plot_widget.setLabel('left', 'Amplitude (dB)')
        self.plot_widget.setLabel('bottom', 'Time (ms)')
        self.plot_widget.setYRange(-60, 0)  # -60dB to 0dB range
        
        # Configure grid with common dB intervals
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        y_axis = self.plot_widget.getAxis('left')
        y_ticks = [-60, -48, -36, -24, -12, 0]  # Common dB intervals
        y_axis.setTicks([[(v, str(v)) for v in y_ticks]])
        
        # Calculate time in milliseconds (assuming 44.1kHz sample rate)
        ms_per_sample = 1000 / 44100  # milliseconds per sample
        self.time_data = np.linspace(0, self.buffer_size * ms_per_sample, self.buffer_size)
        
        # Create plot curves
        pen = pg.mkPen(color='b', width=2)
        self.curve = self.plot_widget.plot(pen=pen)
        
        # # Add peak level line
        # peak_pen = pg.mkPen(color='r', width=2)
        # self.peak_line = pg.InfiniteLine(pos=-60, angle=0, pen=peak_pen, 
        #                                label='Peak: {value:.1f} dB',
        #                                labelOpts={'position': 0.95, 'color': 'r', 'fill': 'w'})
        # self.plot_widget.addItem(self.peak_line)
        
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
            
            # Update curve
            self.curve.setData(self.display_time, db_data)
            
    #         # Update peak level with hold time
    #         current_peak = np.max(db_data)
    #         if current_peak > self.peak_level:
    #             self.peak_level = current_peak
    #             self.peak_hold_timer.start(self.peak_hold_time)
    #         elif not self.peak_hold_timer.isActive():
    #             self.peak_level = max(-60, self.peak_level - self.peak_decay)
                
    # def _reset_peak(self):
