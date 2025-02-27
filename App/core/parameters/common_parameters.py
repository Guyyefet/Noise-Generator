from App.core.parameters.management.registry import ParameterRegistry
from App.core.parameters.management.builder import ParameterDefinitionBuilder as Param

class CommonParameters:
    """Class containing common audio parameters"""
    
    def __init__(self):
        self.registry = ParameterRegistry()
        
    def add_parameter(self, parameter):
        """Add a parameter to the common parameters registry"""
        self.registry.register(parameter)

def get_params(*param_names):
    """Get a dictionary of common parameters by name"""
    params = {
        "volume": Param().float().min(0.0).max(1.0).default(0.5).step(0.01)
            .display("Volume").unit("").build(),
        "cutoff": Param().float().min(20.0).max(20000.0).default(1000.0).step(1.0)
            .display("Cutoff").unit("Hz").build(),
        "bandwidth": Param().float().min(0.1).max(5.0).default(1.0).step(0.1)
            .display("Bandwidth").unit("oct").build(),
        "resonance": Param().float().min(0.0).max(1.0).default(0.5).step(0.01)
            .display("Resonance").unit("").build(),
        "poles": Param().int().min(1).max(8).default(4).step(1)
            .display("Poles").unit("").build(),
        "octave_count": Param().int().min(1).max(16).default(8).step(1)
            .display("Octaves").unit("").build(),
        "persistence": Param().float().min(0.0).max(1.0).default(0.5).step(0.01)
            .display("Persistence").unit("").build(),
        "lacunarity": Param().float().min(1.0).max(4.0).default(2.0).step(0.1)
            .display("Lacunarity").unit("").build(),
        "scale": Param().float().min(0.01).max(10.0).default(1.0).step(0.01)
            .display("Scale").unit("").build()
    }
    
    return {name: params[name] for name in param_names}
