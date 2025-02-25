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

- Builder Pattern:
  - ParameterDefinitionBuilder for fluent parameter definition
  - Improves readability and maintainability
  - Reduces parameter definition boilerplate

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

- AudioProcessorFactory:
  - Central registry for all audio processors
  - Handles parameter validation and processor instantiation
  - Supports categorization (noise, filter, etc.)
  - Provides detailed parameter metadata

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

2. AudioChain Implementation
The proposed AudioChain would address these limitations with:

Dynamic Processor Ordering:

Add/remove/reorder processors at runtime
Enable/disable specific processors without removing them
Support for processor groups (parallel processing paths)
Processor Lifecycle Management:

Proper initialization and cleanup of processors
Resource management for processors that need it
Hot-swapping processors without audio interruption
Targeted Parameter Routing:

Route parameters to specific processors
Support for processor-specific parameter namespaces
Parameter inheritance and overrides between processors
Advanced Signal Flow:

Support for side-chains and feedback loops
Split/merge audio paths for parallel processing
Conditional processing based on audio characteristics
Processor Communication:

Inter-processor messaging system
Shared state between related processors
Event notifications for significant changes

### Phase 3: Advanced Features
   Enhance GUI Integration:
   - Update GUI for dynamic parameters
   - Add component controls

### Current Implementation Status (as of latest commit)

1. Completed:
   - Phase 1.1: Dictionary-based Parameters
   - Phase 1.2: Parameter Registry System
   - Phase 2.1: Component Factories
     - Implemented AudioProcessorFactory with robust parameter validation
     - Created ParameterDefinitionBuilder with fluent API
     - Implemented common parameter definitions for reuse
     - Set up proper component registration with parameter metadata
   - Parameter Validation Fix:
     - Updated validation.py to handle different ParameterRange implementations
     - Made ParameterRange properly callable
     - Ensured consistent validation across core and GUI components

2. Key Improvements:
   - Parameter Builder Pattern:
     - Fluent API for defining parameters: `Param().float().default(0.5).range(0, 1).display("Volume").build()`
     - Type-safe parameter definitions
     - Reusable parameter definitions via common_parameters.py
     - Reduced duplication and improved maintainability

   - Enhanced Processor Factory:
     - Robust parameter validation (type checking, range validation)
     - Improved error messages for invalid parameters
     - Better separation of concerns between registration and instantiation
     - Support for enum parameters and proper validation

   - GUI Integration:
     - Updated to work with the new parameter system
     - Dynamic control creation based on processor parameters
     - Proper handling of different parameter types (float, int, enum)

3. Current Challenges:
   - Parameter System Architecture:
     - Disconnected parameter flow between GUI and core
     - Inconsistent parameter access patterns
     - Circular dependencies between core and GUI modules
     - Duplicate parameter registries in core and GUI

   - Integration Issues:
     - Processor selection not properly connected to audio engine
     - Parameter validation duplicated in multiple places
     - Missing event handlers for GUI controls

4. Next Steps (Detailed):
   - Phase 2.2: Resolve Circular Dependencies
     - Move all parameter system code to core
     - Remove GUI imports from core modules
     - Create proper interfaces for parameter access
     - Consolidate core and GUI parameter registries

   - Phase 2.3: Implement Unified Parameter Flow
     - Fix NoiseControlsWidget event handlers
     - Update NoiseParameters to handle processor type changes
     - Refine AudioEngine to handle parameter updates properly

   - Phase 2.4: Clean Up and Optimize
     - Create consistent parameter access patterns
     - Improve error handling for parameter validation
     - Optimize parameter update performance

   - Phase 3: Advanced Features
     - Implement parameter presets system
     - Add parameter automation capabilities
     - Create parameter grouping and relationships
     - Implement parameter persistence (save/load settings)

### Implementation Strategy
1. Current Focus: Begin Phase 2.2
   - Implement AudioChain class
   - Support dynamic processor ordering
   - Add processor lifecycle management

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
