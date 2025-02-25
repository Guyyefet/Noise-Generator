from .parameter_builder import ParameterDefinitionBuilder as Param

COMMON_PARAMS = {
    "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build(),
    
    # Filter parameters
    "cutoff": Param().float().default(0.5).range(0, 1).display("Filter Cutoff").units("normalized").build(),
    "resonance": Param().float().default(0.0).range(0, 1).display("Resonance").build(),
    "bandwidth": Param().float().default(0.5).range(0, 1).display("Bandwidth").build(),
    "poles": Param().int().default(1).range(1, 4).display("Poles").build(),
    
    # Fractal noise parameters
    "octave_count": Param().int().default(4).range(4, 8).display("Octave Count").build(),
    "persistence": Param().float().default(0.5).range(0.5, 0.8).display("Persistence").build(),
    "lacunarity": Param().float().default(2.0).range(1.0, 4.0).display("Lacunarity").build(),
    "scale": Param().float().default(1.0).range(0.1, 10.0).display("Scale").build()
}

def get_param(name: str):
    """Get a common parameter definition by name."""
    return COMMON_PARAMS.get(name)

def get_params(*names: str):
    """Get multiple parameter definitions by name."""
    return {name: COMMON_PARAMS[name] for name in names}
