from ..noise.implementations.xorshift import XorShiftGenerator
from ..noise.implementations.fractal import FractalNoiseGenerator
from ..filters.implementations.bandpass import BandpassFilter
from ..filters.implementations.cascaded_onepole_lowpass import CascadedOnePoleLowPass
from ..filters.implementations.cascaded_onepole_lowpass_v2 import CascadedOnePoleLowPassV2
from .processor_factory import AudioProcessorFactory
from ..parameters.parameter_builder import ParameterDefinitionBuilder as Param
from ..parameters.common_parameters import get_params

def register_processors():
    """Register all available audio processors."""
    # Register noise generators
    AudioProcessorFactory.register(
        name="xorshift",
        processor_class=XorShiftGenerator,
        description="XOR shift random number generator",
        category="noise",
        parameters=get_params("volume")
    )

    AudioProcessorFactory.register(
        name="fractal",
        processor_class=FractalNoiseGenerator,
        description="Fractal noise generator with octaves",
        category="noise",
        parameters={
            **get_params("volume", "octave_count", "persistence", "lacunarity", "scale"),
            "noise_type": Param().enum(["XOR Shift"]).default("XOR Shift").display("Base Noise Type").build()
        }
    )

    # Register filters
    AudioProcessorFactory.register(
        name="bandpass",
        processor_class=BandpassFilter,
        description="Bandpass filter",
        category="filter",
        parameters=get_params("cutoff", "bandwidth")
    )

    AudioProcessorFactory.register(
        name="cascaded",
        processor_class=CascadedOnePoleLowPass,
        description="Cascaded one-pole lowpass filter",
        category="filter",
        parameters=get_params("cutoff", "resonance", "poles")
    )

    AudioProcessorFactory.register(
        name="cascaded_v2",
        processor_class=CascadedOnePoleLowPassV2,
        description="Improved cascaded one-pole lowpass filter",
        category="filter",
        parameters=get_params("cutoff", "resonance", "poles")
    )
