from .parameter_system import ParameterRegistry
from .parameter_builder import ParameterDefinitionBuilder as Param
from .common_parameters import COMMON_PARAMS

# Global registry instance
registry = ParameterRegistry()

# Register common parameters
for name, definition in COMMON_PARAMS.items():
    registry.register(name, definition)

def get_registry() -> ParameterRegistry:
    """Get the global parameter registry instance."""
    return registry
