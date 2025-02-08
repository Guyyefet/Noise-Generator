import pytest
from App.core.parameters.noise_parameters import NoiseParameters
from App.core.parameters.parameter_definitions import ParameterRegistry, ParameterDefinition, ParameterType
from App.core.parameters.parameter_system import Range

@pytest.fixture
def parameter_registry():
    registry = ParameterRegistry()
    registry.register(
        ParameterDefinition(
            name="volume",
            param_type=ParameterType.FLOAT,
            description="Output volume level",
            units=None,
            display_name="Volume",
            range=Range(0.0, 1.0),
            default_value=0.5
        )
    )
    return registry

@pytest.fixture
def noise_parameters(parameter_registry):
    return NoiseParameters()
