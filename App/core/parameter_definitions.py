from .parameter_system import ParameterRegistry, ParameterDefinition, ParameterType, Range

# Global registry instance
registry = ParameterRegistry()

# Register all parameter definitions
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
