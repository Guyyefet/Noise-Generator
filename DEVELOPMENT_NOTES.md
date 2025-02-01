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
- Base gain (1.5x) with small bandwidth-dependent boost
- Narrow bandwidth gets slightly more gain (+0.2x)
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

### Audio Engine Improvements
- Re-enable colored noise with improved implementation
- Improve low frequency response with either:
  1. Frequency-dependent gain compensation:
     - Add additional gain boost below 200Hz
     - Scale boost inversely with frequency
     - Pros: Simpler implementation, easier to tune
     - Cons: May increase noise floor at low frequencies
  
  2. Logarithmic filter coefficient mapping:
     - Replace linear cutoff-to-alpha mapping with logarithmic scale
     - Implement gentler high-pass filter slope
     - Pros: More natural frequency response, better precision at low frequencies
     - Cons: Requires significant filter implementation changes

### TODO
