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

### Code Organization
- App/core/strategies/
  - noise/        # Noise generation strategies
    - base.py     # Base noise generator interface
    - xorshift.py # XOR shift implementation
  - filters/      # Audio filter strategies
    - base.py     # Base filter interface
    - bandpass.py # Bandpass filter implementation

### Filter Implementations

#### Low-Pass Filter Evolution
We've experimented with several low-pass filter implementations:

1. Simple One-Pole Cascade:
   - Basic IIR filter: y[n] = alpha * x[n] + (1-alpha) * y[n-1]
   - Cascaded multiple times for steeper slopes
   - Simple but less precise frequency control

2. Butterworth with Bilinear Transform:
   - Proper pole placement for maximally flat response
   - Used bilinear transform for coefficient calculation
   - More mathematically correct but complex implementation
   - Challenges with DC offset and stability

3. Cascaded One-Pole with Progressive Scaling (Current):
   - Enhanced one-pole design with progressive coefficient scaling
   - Resonance feedback on final stage
   - Balanced between simplicity and effectiveness
   - Features:
     * Variable pole count (6dB to 24dB/octave)
     * Resonance control at cutoff frequency
     * DC offset compensation
     * Adaptive gain compensation
   - Trade-offs:
     * Not mathematically perfect attenuation
     * But good enough for practical audio use
     * Simple, efficient implementation

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

## Refactoring Plan: Making the System More Flexible

### Phase 1: Parameter System Overhaul
1. Convert to Dictionary-based Parameters
   - Update NoiseParameters to use dictionary storage
   - Modify parameter passing throughout the system
   - Add basic parameter validation
   Benefits: 
   - Immediate flexibility in parameter handling
   - Foundation for future improvements
   - Minimal breaking changes

2. Implement Parameter Registry
   - Create ParameterDefinition class for metadata
   - Set up central parameter registry
   - Add type checking and validation
   Benefits:
   - Better parameter documentation
   - Runtime validation
   - Clear parameter contracts

### Phase 2: Dynamic Component System
1. Create Component Factories and Simplify Structure
   - Implement AudioStrategyFactory
   - Set up component registries
   - Create factory methods for each component type
   - Simplify component hierarchy:
     ```
     App/core/
     ├── filters/
     │   ├── base.py
     │   │   └── class FilterBase:
     │   │       - Parameter validation
     │   │       - Common filter operations
     │   │       - Audio processing interface
     │   └── implementations/
     │       └── bandpass.py
     │           └── class BandpassFilter(FilterBase)
     └── noise/
         ├── base.py
         │   └── class NoiseGeneratorBase:
         │       - Parameter validation
         │       - Common generator operations
         │       - Sample generation interface
         └── implementations/
             └── xorshift.py
                 └── class XorShiftGenerator(NoiseGeneratorBase)
     ```
   Benefits:
   - Easy addition of new generators/filters
   - Clean component instantiation
   - Better separation of concerns
   - Clearer inheritance hierarchy
   - Domain-specific base classes
   - More intuitive code organization

2. Implement Processing Chain
   - Create AudioChain class
   - Support dynamic processor ordering
   - Add processor lifecycle management
   Benefits:
   - Flexible effect chaining
   - Easy to add new effect types
   - Better audio pipeline control

### Phase 3: Advanced Features
   Enhance GUI Integration:
   - Update GUI for dynamic parameters
   - Add component controls

### Current Implementation Status (as of commit 308abd0)

1. Completed:
   - Phase 1.1: Dictionary-based Parameters
   - Phase 1.2: Parameter Registry System
   - Phase 2.1: Component Factories (partial)
     - Implemented AudioProcessorFactory
     - Set up basic component registration

2. Known Issues:
   - Volume slider not affecting output
     - Root cause: XorShiftGenerator not handling volume parameter
     - Potential fix: Add volume scaling in generator's process_audio method

3. Next Steps:
   - Fix volume control in XorShiftGenerator
   - Complete Phase 2.1 with proper component lifecycle management
   - Begin planning for Phase 2.2 (Processing Chain)

### Implementation Strategy
1. Current Focus: Complete Phase 2.1
   - Fix volume control
   - Ensure proper parameter handling
   - Maintain existing functionality

2. Evaluate after each sub-phase
   - Test thoroughly
   - Gather feedback
   - Adjust next steps as needed

3. Keep backward compatibility
   - Support existing features
   - Gradual deprecation of old systems
   - Smooth transition path

### Dependencies Between Phases
- Phase 1.1 required for all other phases
- Phase 1.2 enhances 1.1 but optional
- Phase 2 can start after 1.1
- Phase 3 requires Phase 2

### Risk Management
- Unit tests for each phase
- Feature flags for new capabilities
- Fallback paths for critical features
- Gradual rollout of changes
