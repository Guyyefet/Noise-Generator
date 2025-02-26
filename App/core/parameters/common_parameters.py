from App.core.parameters.parameter_system import ParameterSystem
from typing import Dict, Any

# Create registry instance
common_parameter_registry = ParameterSystem()

# Register common parameters
COMMON_PARAMS = {
    "volume": {
        "default_value": 0.5,
        "min_value": 0,
        "max_value": 1,
        "metadata": {
            "display": "Volume",
            "units": "gain",
            "control_type": "slider",
            "tooltip": "Main output volume",
            "step_size": 0.01
        }
    },
    "cutoff": {
        "default_value": 0.5,
        "min_value": 0,
        "max_value": 1,
        "metadata": {
            "display": "Filter Cutoff",
            "units": "normalized",
            "control_type": "slider",
            "tooltip": "Filter cutoff frequency",
            "step_size": 0.001
        }
    },
    "resonance": {
        "default_value": 0.0,
        "min_value": 0,
        "max_value": 1,
        "metadata": {
            "display": "Resonance",
            "control_type": "slider",
            "tooltip": "Filter resonance amount",
            "step_size": 0.01
        }
    },
    "bandwidth": {
        "default_value": 0.5,
        "min_value": 0,
        "max_value": 1,
        "metadata": {
            "display": "Bandwidth",
            "control_type": "slider",
            "tooltip": "Filter bandwidth",
            "step_size": 0.01
        }
    },
    "poles": {
        "default_value": 1,
        "min_value": 1,
        "max_value": 4,
        "metadata": {
            "display": "Poles",
            "control_type": "slider",
            "tooltip": "Number of filter poles",
            "step_size": 1
        }
    },
    "octave_count": {
        "default_value": 4,
        "min_value": 4,
        "max_value": 8,
        "metadata": {
            "display": "Octave Count",
            "control_type": "slider",
            "tooltip": "Number of noise octaves",
            "step_size": 1
        }
    },
    "persistence": {
        "default_value": 0.5,
        "min_value": 0.5,
        "max_value": 0.8,
        "metadata": {
            "display": "Persistence",
            "control_type": "slider",
            "tooltip": "Noise persistence",
            "step_size": 0.01
        }
    },
    "lacunarity": {
        "default_value": 2.0,
        "min_value": 1.0,
        "max_value": 4.0,
        "metadata": {
            "display": "Lacunarity",
            "control_type": "slider",
            "tooltip": "Noise lacunarity",
            "step_size": 0.1
        }
    },
    "scale": {
        "default_value": 1.0,
        "min_value": 0.1,
        "max_value": 10.0,
        "metadata": {
            "display": "Scale",
            "control_type": "slider",
            "tooltip": "Noise scale",
            "step_size": 0.1
        }
    }
}

# Register all common parameters
for name, param in COMMON_PARAMS.items():
    common_parameter_registry.register(name, param)

def get_params(*names: str) -> Dict[str, Any]:
    """Get common parameter definitions by name(s).
    
    Args:
        *names: Names of parameters to retrieve. If no names provided,
                returns all definitions.
                
    Returns:
        Dictionary of parameter definitions.
        
    Raises:
        KeyError: If any requested parameter is not found
    """
    if not names:
        return common_parameter_registry._parameter_definitions
        
    result = {}
    for name in names:
        if name not in common_parameter_registry._parameter_definitions:
            raise KeyError(f"Parameter {name} not found")
        result[name] = common_parameter_registry._parameter_definitions[name]
        
    return result
