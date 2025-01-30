# Noise Playground Development Notes

## Audio Engine Implementation

### Noise Generation
- Using XOR shift algorithm for pseudo-random number generation
- Normalized to [-1, 1] range
- Original implementation included Markov chain for colored noise (currently disabled)

### Bandpass Filter
- Implemented as cascaded high-pass and low-pass filters
- Filter coefficients properly normalized for unity gain
- High-pass: y[n] = x[n] - x[n-1] + (1-alpha) * y[n-1]
- Low-pass: y[n] = alpha * x[n] + (1-alpha) * y[n-1]
- Single gain compensation (1.5x) after filtering
- Cutoff frequency and bandwidth controls

### Signal Chain
1. Noise Generation ([-1,1])
2. Bandpass Filter (normalized coefficients)
3. Gain Compensation (1.5x)
4. Volume Control
5. Clip Protection

## Future Ideas

### GUI Improvements
- Consider switching from matplotlib to PyQt/pyqtgraph for:
  - Better real-time performance
  - More flexible layouts
  - Native-looking controls
  - Easier component management

### Visualization Plans
1. Time Domain Plot
   - Show waveform in real-time
   - Display both pre and post-filter signals
   - Help visualize filter effects

2. Future Visualization Options
   - Frequency Domain Plot (spectrum analysis)
   - Spectrogram (time-frequency visualization)

### Feature Ideas
- Re-enable colored noise with improved implementation

### TODO

- maybe we should have better gain staging when the filter cutoff is low,
  the volume decrease quite abit there 
- switch to QT lib for GUI and visualization

### Architecture Changes:
Split current NoiseGUI into separate components:
NoiseParameters (Subject): Manages state and core logic
NoiseGUI: Handles parameter controls (sliders)
WaveformView: Handles visualization
MainWindow: Composes all components together
GUI Framework:
Moving from matplotlib to Qt + pyqtgraph
Better performance for real-time updates
Native Qt integration
More responsive visualization
Observer Pattern:
Keeping our current observer pattern for audio parameters
NoiseParameters remains as Subject
AudioParameterObserver stays unchanged
Clean separation between GUI and audio logic
Data Flow:
User Input → NoiseGUI → NoiseParameters (Subject)
                              ↓
                    AudioParameterObserver
                              ↓
                        AudioEngine
                              ↓
                        WaveformView
Benefits:
Better separation of concerns
Each class has a single responsibility
More maintainable and testable
Improved visualization performance
Cleaner architecture overall

