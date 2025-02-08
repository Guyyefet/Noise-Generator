from .parameter_system import ParameterRegistry, ParameterDefinition, ParameterType, Range

# Global registry instance
registry = ParameterRegistry()

# Register all parameter definitions
registry.register(ParameterDefinition(
    name="generator_type",
    param_type=ParameterType.STR,
    default_value="XOR Shift Noise",
    description="Type of noise generator to use",
    display_name="Generator Type"
))

registry.register(ParameterDefinition(
    name="filter_type",
    param_type=ParameterType.STR,
    default_value="Bandpass",
    description="Type of filter to apply",
    display_name="Filter Type"
))

# Bandpass filter parameters
registry.register(ParameterDefinition(
    name="cutoff",
    param_type=ParameterType.FLOAT,
    default_value=0.5,
    description="Center frequency of bandpass filter",
    range=Range(0.0, 1.0),
    display_name="Filter Cutoff"
))

registry.register(ParameterDefinition(
    name="bandwidth",
    param_type=ParameterType.FLOAT,
    default_value=0.5,
    description="Width of the frequency band",
    range=Range(0.0, 1.0),
    display_name="Bandwidth"
))

# Lowpass filter parameters
registry.register(ParameterDefinition(
    name="resonance",
    param_type=ParameterType.FLOAT,
    default_value=0.0,
    description="Filter resonance at cutoff frequency",
    range=Range(0.0, 1.0),
    display_name="Resonance"
))

registry.register(ParameterDefinition(
    name="poles",
    param_type=ParameterType.INT,
    default_value=1,
    description="Number of filter poles (affects slope)",
    range=Range(1, 4),
    display_name="Poles"
))

registry.register(ParameterDefinition(
    name="volume",
    param_type=ParameterType.FLOAT,
    default_value=0.5,
    description="Output volume level",
    range=Range(0.0, 1.0),
    display_name="Volume"
))

# Export the registry instance
def get_registry() -> ParameterRegistry:
    """Get the global parameter registry instance."""
    return registry
