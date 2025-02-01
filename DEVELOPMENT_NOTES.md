# Noise Playground Development Notes

## Audio Engine Architecture

### Design Patterns
- Observer Pattern:
  - NoiseParameters acts as Subject
  - GUI components observe parameter changes
  - Ensures UI stays in sync with audio engine
  - Decouples parameter management from audio processing

- Strategy Pattern:
  - Modular audio processing components
  - Separate generators and filters
  - Easy to extend with new noise types
  - Clean separation of concerns

### Core Components
- NoiseGenerator (Strategy):
  - Abstract base class for noise generation
  - XorShift implementation for white noise
  - Normalized to [-1, 1] range

- AudioFilter (Strategy):
  - Abstract base class for audio processing
  - Bandpass implementation:
    - Cascaded high-pass and low-pass filters
    - Filter coefficients properly normalized
    - High-pass: y[n] = x[n] - x[n-1] + (1-alpha) * y[n-1]
    - Low-pass: y[n] = alpha * x[n] + (1-alpha) * y[n-1]
    - Base gain (1.5x) with small bandwidth-dependent boost
    - Narrow bandwidth gets slightly more gain (+0.2x)

### Signal Chain
1. Parameter Updates (Observer pattern)
2. Noise Generation (Strategy pattern)
3. Filter Processing (Strategy pattern)
4. Volume Control
5. Clip Protection

## Future Ideas


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
- Add more generator types (e.g., colored noise)
- Implement additional filter types
- Add preset management system
