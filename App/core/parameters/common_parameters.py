from App.core.parameters.parameter_builder import ParameterDefinitionBuilder as Param

COMMON_PARAMS = {
    "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain")
        .control_type("slider").tooltip("Main output volume").step_size(0.01).build(),
    
    # Filter parameters
    "cutoff": Param().float().default(0.5).range(0, 1).display("Filter Cutoff").units("normalized")
        .control_type("slider").tooltip("Filter cutoff frequency").step_size(0.001).build(),
    "resonance": Param().float().default(0.0).range(0, 1).display("Resonance")
        .control_type("slider").tooltip("Filter resonance amount").step_size(0.01).build(),
    "bandwidth": Param().float().default(0.5).range(0, 1).display("Bandwidth")
        .control_type("slider").tooltip("Filter bandwidth").step_size(0.01).build(),
    "poles": Param().int().default(1).range(1, 4).display("Poles")
        .control_type("slider").tooltip("Number of filter poles").step_size(1).build(),
    
    # Fractal noise parameters
    "octave_count": Param().int().default(4).range(4, 8).display("Octave Count")
        .control_type("slider").tooltip("Number of noise octaves").step_size(1).build(),
    "persistence": Param().float().default(0.5).range(0.5, 0.8).display("Persistence")
        .control_type("slider").tooltip("Noise persistence").step_size(0.01).build(),
    "lacunarity": Param().float().default(2.0).range(1.0, 4.0).display("Lacunarity")
        .control_type("slider").tooltip("Noise lacunarity").step_size(0.1).build(),
    "scale": Param().float().default(1.0).range(0.1, 10.0).display("Scale")
        .control_type("slider").tooltip("Noise scale").step_size(0.1).build()
}

def get_param(name: str):
    """Get a common parameter definition by name."""
    return COMMON_PARAMS.get(name)

def get_params(*names: str):
    """Get multiple parameter definitions by name."""
    return {name: COMMON_PARAMS[name] for name in names}
