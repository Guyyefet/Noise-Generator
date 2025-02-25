# Parameter System Architecture

## Overview

The parameter system is designed to manage audio processing parameters across both the core audio engine and the GUI. It's currently in a transitional state as part of a larger refactoring effort to make the system more modular and flexible.

## Core vs. GUI Parameter Components

### Core Parameter Components

1. **App/core/parameters/parameter_builder.py**:
   - Defines `ParameterDefinitionBuilder` for fluent parameter definition
   - Creates a `ParameterRange` dataclass for parameter constraints
   - Provides a builder pattern for creating parameter definitions
   - Example: `Param().float().default(0.5).range(0, 1).display("Volume").build()`

2. **App/core/parameters/parameter_registry.py**:
   - Implements `ParameterRegistry` class that extends `Subject` for observer pattern
   - Manages parameter definitions and their registration
   - Provides methods to set processor type and get parameter info
   - Notifies observers when parameters change

3. **App/core/parameters/validation.py**:
   - Defines validation functions for parameter types, ranges, and enums
   - Implements a callable `ParameterRange` class for range validation
   - Provides a unified validation interface for all parameter types

4. **App/core/parameters/common_parameters.py**:
   - Defines common parameters used across different processors
   - Provides helper functions to get individual or multiple parameters
   - Centralizes parameter definitions to reduce duplication

### GUI Parameter Components

1. **App/gui/parameters/parameter_registry.py**:
   - Defines a GUI-specific `ParameterRegistry` class
   - Creates a `ParameterDefinition` dataclass for GUI parameter metadata
   - Provides methods to register and retrieve parameter definitions
   - Focused on GUI-specific parameter handling

2. **App/gui/parameters/parameter_definitions.py**:
   - Creates a global GUI parameter registry instance
   - Imports and registers common parameters from the core system
   - Provides a getter function to access the registry
   - Acts as a bridge between core parameters and GUI components

3. **App/gui/parameters/validation.py**:
   - Simply imports validation functions from the core system
   - Reuses the core validation system for consistency
   - Doesn't implement any GUI-specific validation logic

## Parameter Flow

The current parameter flow is fragmented and not fully connected:

1. **GUI Controls** update parameters in the GUI parameter registry
2. These changes should propagate to the core `ParameterRegistry`
3. The core registry should notify observers (including `AudioParameterObserver`)
4. `AudioParameterObserver` should update the `AudioEngine`
5. `AudioEngine` should apply parameters to the active processors

However, there are disconnections in this flow:
- GUI controls don't properly update the parameter registry
- Changes don't consistently propagate between GUI and core
- Observer notifications aren't always triggered correctly

## Validation System

The parameter validation system is designed to ensure parameters meet their defined constraints:

1. **Type Validation**: Ensures parameters are of the correct type (float, int, string, etc.)
2. **Range Validation**: Verifies numeric parameters are within their defined min/max range
3. **Enum Validation**: Checks that enum parameters have valid values from their defined set

The validation system was recently fixed to handle different implementations of `ParameterRange`:
- Core implementation with `__call__` method
- Dataclass implementation from parameter_builder.py
- Dictionary representation with min/max values

## Current Issues

1. **Circular Dependencies**:
   - `parameter_system.py` imports from GUI modules
   - This creates circular dependencies that complicate the architecture

2. **Duplicate Implementations**:
   - Both core and GUI have their own parameter registry implementations
   - This leads to inconsistencies and maintenance challenges

3. **Disconnected Flow**:
   - Parameter changes don't properly propagate through the system
   - Observer pattern implementation is incomplete

## Future Improvements

1. **Unified Parameter System**:
   - Move all parameter system code to core
   - Create proper interfaces for GUI to use
   - Eliminate circular dependencies

2. **Consistent Validation**:
   - Centralize validation in one place
   - Ensure all parameter access goes through validation

3. **Complete Observer Pattern**:
   - Ensure all parameter changes notify observers
   - Implement proper update methods in all observers

4. **Simplified API**:
   - Create a clean, consistent API for parameter access
   - Document the parameter flow for developers

## Relationship to GUI

The GUI interacts with the parameter system through:

1. **Control Widgets**: Sliders, knobs, and other controls that modify parameters
2. **Parameter Display**: UI elements that show current parameter values
3. **Processor Selection**: UI for selecting different generators and filters

The GUI should:
1. Update the parameter registry when controls change
2. Observe parameter changes to update the display
3. Update processor selection in the audio engine

Currently, these connections are incomplete or broken, which is a focus of the ongoing refactoring effort.
