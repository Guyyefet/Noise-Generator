from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from core.observer import Observer

class WaveformView(QWidget, Observer):
    """Widget for displaying frequency domain analysis and filter response."""
    
    def __init__(self):
        QWidget.__init__(self)
        Observer.__init__(self)
        
        # Buffer for storing waveform data
        self.buffer_size = 2048
        self.waveform_buffer = np.zeros(self.buffer_size)
        
        # Frequency domain settings
        self.sample_rate = 44100
        self.freq_data = np.fft.rfftfreq(self.buffer_size, d=1.0/self.sample_rate)
        
        # Filter parameters
        self.cutoff_freq = 1000  # Default cutoff frequency
        self.bandwidth = 0.5     # Default bandwidth
        
        # Set up update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_plot)
        self.update_timer.start(50)  # 20 FPS
        
        # Flag for new data
        self.has_new_data = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.getViewBox().setMenuEnabled(False)
        
        # Set up axis labels and ranges
        self.plot_widget.setLabel('left', 'Amplitude (dB)')
        self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        
        # Configure frequency axis (logarithmic)
        freq_ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        x_axis = self.plot_widget.getAxis('bottom')
        x_axis.setTicks([[(np.log10(f), str(f)) for f in freq_ticks]])
        self.plot_widget.setLogMode(x=True, y=False)
        self.plot_widget.setXRange(np.log10(20), np.log10(20000))
        
        # Configure amplitude axis
        y_axis = self.plot_widget.getAxis('left')
        y_ticks = [-60, -48, -36, -24, -12, 0]
        y_axis.setTicks([[(v, str(v)) for v in y_ticks]])
        self.plot_widget.setYRange(-60, 0)
        
        # Configure grid
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # Create spectrum curve
        pen = pg.mkPen(color='b', width=2)
        self.spectrum_curve = self.plot_widget.plot(pen=pen)
        
        # Create filter response curve with thicker line
        filter_pen = pg.mkPen(color='r', width=3, dash=[8,4])
        self.filter_curve = self.plot_widget.plot(pen=filter_pen)
        
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
        # Initialize filter response with defaults after UI setup
        self.update(0.5, 0.5, 0.5)  # Default volume, cutoff, bandwidth
    
    def update_waveform(self, data: np.ndarray):
        """Update the waveform display with new data."""
        if not self.isVisible():
            return
            
        # Update buffer with new data
        self.waveform_buffer = np.roll(self.waveform_buffer, -len(data))
        self.waveform_buffer[-len(data):] = data
        self.has_new_data = True
    
    def update(self, *args, **kwargs):
        """Update from NoiseParameters (Observer pattern)."""
        if len(args) == 3:  # volume, cutoff, bandwidth
            volume, cutoff, bandwidth = args
            # Convert normalized cutoff (0-1) to frequency (20Hz-20kHz)
            self.cutoff_freq = 20 * (20000/20)**(cutoff)
            self.q_factor = 0.1 + bandwidth * 2.9  # Map 0-1 to Q range 0.1-3.0
            self._update_filter_response()
    
    def _update_filter_response(self):
        """Update the filter response curve."""
        # Generate frequency response points
        freqs = np.logspace(np.log10(20), np.log10(20000), 1000)
        
        # Simple lowpass filter response (butterworth approximation)
        response = 1 / np.sqrt(1 + (freqs/self.cutoff_freq)**(2*2))
        
        # Convert to dB and apply window
        response_db = 20 * np.log10(np.clip(response, 1e-3, None))
        response_db = np.clip(response_db, -60, 0)
        
        # Update filter curve
        self.filter_curve.setData(freqs, response_db)
    
    def _update_plot(self):
        """Update the plot if there's new data."""
        if self.has_new_data and self.isVisible():
            # Apply window function to reduce spectral leakage
            window = np.hanning(len(self.waveform_buffer))
            windowed_data = self.waveform_buffer * window
            
            # Compute FFT
            fft = np.abs(np.fft.rfft(windowed_data))
            
            # Convert to dB with proper scaling and smoothing
            fft_smoothed = np.convolve(fft, np.hanning(5)/5, mode='same')  # Smooth the spectrum
            fft_db = 20 * np.log10(np.clip(fft_smoothed / len(fft), 1e-3, None))
            fft_db = np.clip(fft_db, -60, 0)
            
            # Update spectrum curve (skip DC and nyquist)
            valid_freqs = (self.freq_data > 20) & (self.freq_data < 20000)
            self.spectrum_curve.setData(self.freq_data[valid_freqs], fft_db[valid_freqs])
            self.has_new_data = False
