from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np
from core.parameters.observer import Observer

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
        
        # Create plot widget with dark theme
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#2b2b2b')
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.getViewBox().setMenuEnabled(False)
        
        # Set up axis labels and ranges with custom style
        label_style = {'color': '#8f8f8f', 'font-size': '10pt'}
        self.plot_widget.setLabel('left', 'dB', **label_style)
        self.plot_widget.setLabel('bottom', 'Hz', **label_style)
        
        # Configure frequency axis (logarithmic)
        major_freqs = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        minor_freqs = []
        for i in range(len(major_freqs)-1):
            f1, f2 = major_freqs[i], major_freqs[i+1]
            if f2/f1 > 2:
                minor_freqs.extend([f1*1.5, f1*2, f1*3, f1*4])
        
        x_axis = self.plot_widget.getAxis('bottom')
        major_ticks = [(np.log10(f), str(f) if f < 1000 else f'{f//1000}k') for f in major_freqs]
        minor_ticks = [(np.log10(f), '') for f in minor_freqs]
        x_axis.setTicks([major_ticks, minor_ticks])
        self.plot_widget.setLogMode(x=True, y=False)
        self.plot_widget.setXRange(np.log10(20), np.log10(20000))
        
        # Configure amplitude axis
        y_axis = self.plot_widget.getAxis('left')
        major_dbs = [-60, -48, -36, -24, -12, 0, 6, 12, 24]
        minor_dbs = [-54, -42, -30, -18, -6, 3, 12]
        major_ticks = [(db, str(db)) for db in major_dbs]
        minor_ticks = [(db, '') for db in minor_dbs]
        y_axis.setTicks([major_ticks, minor_ticks])
        self.plot_widget.setYRange(-60, 24)
        
        # Configure grid with major and minor lines
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        
        # Add minor grid lines
        for freq in minor_freqs:
            line = pg.InfiniteLine(angle=90, pos=np.log10(freq), pen=pg.mkPen('#3f3f3f', width=0.5))
            self.plot_widget.addItem(line)
        for db in minor_dbs:
            line = pg.InfiniteLine(angle=0, pos=db, pen=pg.mkPen('#3f3f3f', width=0.5))
            self.plot_widget.addItem(line)
        
        # Create spectrum curve with blue color
        pen = pg.mkPen(color='#4a9eff', width=2)
        self.spectrum_curve = self.plot_widget.plot(pen=pen)
        
        # Create filter response curve with red color
        filter_pen = pg.mkPen(color='#ff4a4a', width=3)
        self.filter_curve = self.plot_widget.plot(pen=filter_pen)
        
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)
        
        # Initialize filter response with defaults after UI setup
        self.update({
            'generator_type': 'White Noise',
            'filter_type': 'Bandpass',
            'volume': 0.5,
            'cutoff': 0.5,
            'bandwidth': 0.5
        })
    
    def update_waveform(self, data: np.ndarray):
        """Update the waveform display with new data."""
        if not self.isVisible():
            return
            
        # Update buffer with new data
        self.waveform_buffer = np.roll(self.waveform_buffer, -len(data))
        self.waveform_buffer[-len(data):] = data
        self.has_new_data = True
    
    def update(self, parameters: dict):
        """Update from NoiseParameters (Observer pattern)."""
        # Get parameters with defaults
        cutoff = parameters.get('cutoff', 0.5)
        bandwidth = parameters.get('bandwidth', 0.5)
        
        # Map cutoff from 0-1 to center frequency (20Hz-20kHz)
        self.center_freq = 20 * (20000/20)**cutoff
        
        # Map bandwidth to octave spread
        min_spread = 0.5  # minimum 1/2 octave
        max_spread = 4.0  # maximum 4 octaves
        self.octave_spread = min_spread + bandwidth * (max_spread - min_spread)
        
        self._update_filter_response()
    
    def _update_filter_response(self):
        """Update the filter response curve."""
        # Generate frequency response points
        freqs = np.logspace(np.log10(20), np.log10(20000), 1000)
        
        # Calculate bandpass response in octaves
        octaves_from_center = np.abs(np.log2(freqs/self.center_freq))
        
        # Create smooth bandpass shape with steeper falloff
        response = np.exp(-2.0 * (octaves_from_center/self.octave_spread)**2)
        
        # Convert to dB with proper range (+6dB peak)
        response_db = 6 - 12 * (1 - response)  # Peak at +6dB, min at -60dB
        response_db = np.clip(response_db, -60, 24)
        
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
            fft_db = 20 * np.log10(np.clip(fft_smoothed * 2, 1e-3, None))  # *2 to match RMS scaling
            fft_db = np.clip(fft_db, -60, 24)  # Allow peaks up to +6dB
            
            # Update spectrum curve (skip DC and nyquist)
            valid_freqs = (self.freq_data > 20) & (self.freq_data < 20000)
            self.spectrum_curve.setData(self.freq_data[valid_freqs], fft_db[valid_freqs])
            self.has_new_data = False
