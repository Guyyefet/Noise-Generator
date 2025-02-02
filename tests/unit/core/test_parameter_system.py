import pytest
from App.core.parameter_system import (
    ParameterType,
    Range,
    ParameterDefinition,
    ParameterRegistry
)

class TestParameterSystem:
    @pytest.fixture
    def numeric_range(self):
        """Create a valid numeric range."""
        return Range(min_value=0.0, max_value=1.0)
    
    @pytest.fixture
    def float_param(self, numeric_range):
        """Create a valid float parameter definition."""
        return ParameterDefinition(
            name="test_float",
            param_type=ParameterType.FLOAT,
            default_value=0.5,
            description="Test float parameter",
            range=numeric_range,
            units="Hz",
            display_name="Test Float"
        )
    
    @pytest.fixture
    def registry(self):
        """Create a fresh parameter registry."""
        return ParameterRegistry()
    
    def test_parameter_type_enum(self):
        """Test parameter type enumeration."""
        assert ParameterType.FLOAT.value == "float"
        assert ParameterType.INT.value == "int"
        assert ParameterType.BOOL.value == "bool"
        assert ParameterType.STR.value == "str"
    
    def test_range_validation(self):
        """Test range validation."""
        # Valid range
        range = Range(0, 10)
        assert range.min_value == 0
        assert range.max_value == 10
        
        # Invalid range (min >= max)
        with pytest.raises(ValueError):
            ParameterDefinition(
                name="test",
                param_type=ParameterType.FLOAT,
                default_value=5,
                description="test",
                range=Range(10, 0)
            )
    
    def test_parameter_definition_validation(self):
        """Test parameter definition validation."""
        # Valid definition
        param = ParameterDefinition(
            name="test",
            param_type=ParameterType.FLOAT,
            default_value=0.5,
            description="test",
            range=Range(0, 1)
        )
        assert param.name == "test"
        
        # Invalid type
        with pytest.raises(ValueError):
            ParameterDefinition(
                name="test",
                param_type=ParameterType.FLOAT,
                default_value="not a float",
                description="test"
            )
        
        # Invalid range for type
        with pytest.raises(ValueError):
            ParameterDefinition(
                name="test",
                param_type=ParameterType.STR,
                default_value="test",
                description="test",
                range=Range(0, 1)
            )
        
        # Default value outside range
        with pytest.raises(ValueError):
            ParameterDefinition(
                name="test",
                param_type=ParameterType.FLOAT,
                default_value=2.0,
                description="test",
                range=Range(0, 1)
            )
    
    def test_value_validation(self, float_param):
        """Test value validation."""
        # Valid value
        assert float_param.validate_value(0.5) == 0.5
        
        # Value conversion
        assert float_param.validate_value("0.5") == 0.5
        
        # Invalid type
        with pytest.raises(ValueError):
            float_param.validate_value("not a number")
        
        # Out of range
        with pytest.raises(ValueError):
            float_param.validate_value(2.0)
    
    def test_registry_registration(self, registry, float_param):
        """Test parameter registration."""
        registry.register(float_param)
        assert registry.get_definition("test_float") == float_param
        
        # Duplicate registration
        with pytest.raises(ValueError):
            registry.register(float_param)
    
    def test_registry_validation(self, registry, float_param):
        """Test parameter validation through registry."""
        registry.register(float_param)
        
        # Valid parameters
        validated = registry.validate_parameters({"test_float": 0.7})
        assert validated["test_float"] == 0.7
        
        # Unknown parameter
        with pytest.raises(KeyError):
            registry.validate_parameters({"unknown": 0.5})
        
        # Invalid value
        with pytest.raises(ValueError):
            registry.validate_parameters({"test_float": 2.0})
    
    def test_registry_defaults(self, registry, float_param):
        """Test getting default values."""
        registry.register(float_param)
        defaults = registry.get_defaults()
        assert defaults["test_float"] == 0.5
    
    def test_registry_all_definitions(self, registry, float_param):
        """Test getting all definitions."""
        registry.register(float_param)
        definitions = registry.get_all_definitions()
        assert float_param in definitions
        assert len(definitions) == 1
    
    def test_parameter_types(self, registry):
        """Test all parameter types."""
        params = [
            ParameterDefinition("float_param", ParameterType.FLOAT, 0.5, "test"),
            ParameterDefinition("int_param", ParameterType.INT, 42, "test"),
            ParameterDefinition("bool_param", ParameterType.BOOL, True, "test"),
            ParameterDefinition("str_param", ParameterType.STR, "test", "test")
        ]
        
        for param in params:
            registry.register(param)
        
        # Test validation for each type
        validated = registry.validate_parameters({
            "float_param": "0.5",
            "int_param": "42",
            "bool_param": "True",
            "str_param": "value"
        })
        
        assert isinstance(validated["float_param"], float)
        assert isinstance(validated["int_param"], int)
        assert isinstance(validated["bool_param"], bool)
        assert isinstance(validated["str_param"], str)
    
    def test_optional_fields(self):
        """Test optional parameter definition fields."""
        param = ParameterDefinition(
            name="test",
            param_type=ParameterType.FLOAT,
            default_value=0.5,
            description="test"
        )
        assert param.range is None
        assert param.units is None
        assert param.display_name is None
