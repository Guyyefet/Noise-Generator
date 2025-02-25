import pytest
from App.core.processors.processor_factory import AudioProcessorFactory
from App.core.parameters.parameter_builder import ParameterDefinitionBuilder as Param

class MockProcessor:
    def __init__(self, **kwargs):
        self.params = kwargs

def test_register_processor():
    AudioProcessorFactory._registry.clear()  # Reset registry for test
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build(),
        "frequency": Param().float().default(440).range(20, 20000).display("Frequency").units("Hz").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    assert "test_processor" in AudioProcessorFactory._registry
    reg = AudioProcessorFactory._registry["test_processor"]
    assert reg.name == "test_processor"
    assert reg.processor_class == MockProcessor
    assert reg.description == "Test processor"
    assert reg.category == "test"
    assert reg.parameters == parameters

def test_create_processor():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    processor = AudioProcessorFactory.create("test_processor", volume=0.7)
    assert isinstance(processor, MockProcessor)
    assert processor.params["volume"] == 0.7

def test_create_processor_with_invalid_param():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    with pytest.raises(ValueError) as exc:
        AudioProcessorFactory.create("test_processor", volume=1.5)
    assert "outside valid range" in str(exc.value)

def test_create_processor_with_unknown_param():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    with pytest.raises(ValueError) as exc:
        AudioProcessorFactory.create("test_processor", unknown_param=0.5)
    assert "Unknown parameter" in str(exc.value)

def test_create_processor_with_wrong_type():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    with pytest.raises(TypeError) as exc:
        AudioProcessorFactory.create("test_processor", volume="not a number")
    assert "must be a number" in str(exc.value)

def test_get_processors_by_category():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "volume": Param().float().default(0.5).range(0, 1).display("Volume").units("gain").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor1",
        processor_class=MockProcessor,
        description="Test processor 1",
        category="test",
        parameters=parameters
    )
    
    AudioProcessorFactory.register(
        name="test_processor2",
        processor_class=MockProcessor,
        description="Test processor 2",
        category="test",
        parameters=parameters
    )
    
    AudioProcessorFactory.register(
        name="other_processor",
        processor_class=MockProcessor,
        description="Other processor",
        category="other",
        parameters=parameters
    )
    
    test_processors = AudioProcessorFactory.get_processors_by_category("test")
    assert len(test_processors) == 2
    assert all(p.category == "test" for p in test_processors)

def test_enum_parameter():
    AudioProcessorFactory._registry.clear()
    
    parameters = {
        "mode": Param().enum(["sine", "square", "triangle"]).default("sine").display("Waveform").build()
    }
    
    AudioProcessorFactory.register(
        name="test_processor",
        processor_class=MockProcessor,
        description="Test processor",
        category="test",
        parameters=parameters
    )
    
    # Valid enum value
    processor = AudioProcessorFactory.create("test_processor", mode="square")
    assert processor.params["mode"] == "square"
    
    # Invalid enum value
    with pytest.raises(ValueError) as exc:
        AudioProcessorFactory.create("test_processor", mode="invalid")
    assert "Invalid value for enum parameter" in str(exc.value)
