from App.core.parameters.base_registry import BaseParameterRegistry
from App.core.parameters.common_parameters import COMMON_PARAMS

# Global registry instance
registry = BaseParameterRegistry()

# Register common parameters
for name, definition in COMMON_PARAMS.items():
    registry.register(name, definition)

def get_registry() -> BaseParameterRegistry:
    """Get the global parameter registry instance."""
    return registry
