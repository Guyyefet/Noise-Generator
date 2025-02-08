import pytest
from App.core.parameters.noise_parameters import NoiseParameters
from App.core.parameters.observer import Observer

@pytest.fixture
def test_observer():
    class TestObserver(Observer):
        def __init__(self):
            self.last_update = None
            self.update_count = 0
        
        def update(self, parameters):
            self.last_update = parameters
            self.update_count += 1
    return TestObserver()

@pytest.fixture
def noise_parameters():
    """Create a NoiseParameters instance for testing."""
    return NoiseParameters()

class TestNoiseParameters:
    def test_initialization(self, noise_parameters):
        """Test that NoiseParameters initializes with default values."""
        assert isinstance(noise_parameters, NoiseParameters)
        assert "volume" in noise_parameters.parameters
        assert noise_parameters.parameters["volume"] == 0.5

    def test_update_parameters(self, noise_parameters):
        """Test parameter updates with valid values."""
        noise_parameters.update_parameters(volume=0.8)
        assert noise_parameters.parameters["volume"] == 0.8

    def test_update_invalid_parameter(self, noise_parameters):
        """Test that updating with invalid parameter raises KeyError."""
        with pytest.raises(KeyError):
            noise_parameters.update_parameters(invalid_param=1.0)

    def test_update_invalid_value(self, noise_parameters):
        """Test that updating with invalid value raises ValueError."""
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(volume=1.5)  # Outside valid range

    def test_get_parameter(self, noise_parameters):
        """Test getting parameter values."""
        assert noise_parameters.get_parameter("volume") == 0.5
        assert noise_parameters.get_parameter("nonexistent", default=1.0) == 1.0
        with pytest.raises(KeyError):
            noise_parameters.get_parameter("nonexistent")

    def test_get_parameter_info(self, noise_parameters):
        """Test getting parameter metadata."""
        info = noise_parameters.get_parameter_info("volume")
        assert info["name"] == "volume"
        assert info["type"] == "float"
        assert info["units"] is None
        assert info["display_name"] == "Volume"
        assert info["range"]["min"] == 0.0
        assert info["range"]["max"] == 1.0
        assert info["current_value"] == 0.5

    def test_observer_notification(self, noise_parameters, test_observer):
        """Test that observers are notified of parameter updates."""
        observer = test_observer
        noise_parameters.attach(observer)

        # Test initial update count
        assert observer.update_count == 0
        assert observer.last_update is None

        # Update parameter and verify notification
        noise_parameters.update_parameters(volume=0.7)
        assert observer.update_count == 1
        assert observer.last_update["volume"] == 0.7

        # Update again and verify second notification
        noise_parameters.update_parameters(volume=0.3)
        assert observer.update_count == 2
        assert observer.last_update["volume"] == 0.3

        # Detach observer and verify no more notifications
        noise_parameters.detach(observer)
        noise_parameters.update_parameters(volume=0.1)
        assert observer.update_count == 2  # Count should not increase after detachment

    def test_multiple_parameter_update(self, noise_parameters):
        """Test updating multiple parameters at once."""
        noise_parameters.update_parameters(volume=0.6, cutoff=0.8)
        assert noise_parameters.parameters["volume"] == 0.6
        assert noise_parameters.parameters["cutoff"] == 0.8

        # Test that all parameters are validated
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(volume=1.5, cutoff=0.8)  # Invalid volume
        # Verify no parameters were updated after failed validation
        assert noise_parameters.parameters["volume"] == 0.6
        assert noise_parameters.parameters["cutoff"] == 0.8

    def test_parameter_info_retrieval(self, noise_parameters):
        """Test parameter info retrieval."""
        # Test parameter with range
        info = noise_parameters.get_parameter_info("volume")
        assert info["range"] is not None
        assert info["type"] == "float"
        assert info["display_name"] == "Volume"
        assert info["description"] == "Output volume level"
        assert info["range"]["min"] == 0.0
        assert info["range"]["max"] == 1.0

        # Test nonexistent parameter
        with pytest.raises(KeyError):
            noise_parameters.get_parameter_info("nonexistent")

    def test_notify_without_observers(self, noise_parameters):
        """Test notification behavior without observers."""
        # Should not raise any errors
        noise_parameters.notify()
        noise_parameters.update_parameters(volume=0.4)

    def test_parameter_type_validation(self, noise_parameters):
        """Test validation of different parameter types."""
        # Test float parameters
        noise_parameters.update_parameters(volume=0.75)
        assert isinstance(noise_parameters.get_parameter("volume"), float)
        
        noise_parameters.update_parameters(cutoff=0.3)
        assert isinstance(noise_parameters.get_parameter("cutoff"), float)
        
        noise_parameters.update_parameters(bandwidth=0.4)
        assert isinstance(noise_parameters.get_parameter("bandwidth"), float)

        # Test invalid type conversions
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(volume="not a number")
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(cutoff={})  # Invalid type - dictionary
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(bandwidth=[])  # Invalid type - list

    def test_parameter_range_validation(self, noise_parameters):
        """Test parameter range validation."""
        # Test at range boundaries for volume
        noise_parameters.update_parameters(volume=0.0)  # Min value
        noise_parameters.update_parameters(volume=1.0)  # Max value

        # Test slightly outside range for volume
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(volume=-0.001)
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(volume=1.001)

        # Test at range boundaries for cutoff
        noise_parameters.update_parameters(cutoff=0.0)  # Min value
        noise_parameters.update_parameters(cutoff=1.0)  # Max value
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(cutoff=-0.1)
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(cutoff=1.1)

        # Test at range boundaries for bandwidth
        noise_parameters.update_parameters(bandwidth=0.0)  # Min value
        noise_parameters.update_parameters(bandwidth=1.0)  # Max value
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(bandwidth=-0.1)
        with pytest.raises(ValueError):
            noise_parameters.update_parameters(bandwidth=1.1)

    def test_parameter_defaults(self, noise_parameters):
        """Test that parameters initialize with correct defaults."""
        assert noise_parameters.get_parameter("volume") == 0.5
        assert noise_parameters.get_parameter("cutoff") == 0.5
        assert noise_parameters.get_parameter("bandwidth") == 0.5

    def test_parameter_units(self, noise_parameters):
        """Test parameter units information."""
        for param in ["volume", "cutoff", "bandwidth"]:
            info = noise_parameters.get_parameter_info(param)
            assert "units" in info
            assert info["units"] is None  # Current parameters don't have units defined

    def test_parameter_persistence_across_filter_switch(self, noise_parameters):
        """Test that common parameters persist when switching between filters."""
        # Set initial parameters for bandpass
        noise_parameters.update_parameters(
            filter_type="Bandpass",
            cutoff=0.7,
            bandwidth=0.3,
            volume=0.8
        )
        
        # Verify bandpass parameters are set
        assert noise_parameters.get_parameter("filter_type") == "Bandpass"
        assert noise_parameters.get_parameter("cutoff") == 0.7
        assert noise_parameters.get_parameter("bandwidth") == 0.3
        assert noise_parameters.get_parameter("volume") == 0.8
        
        # Switch to lowpass, keeping common parameters
        noise_parameters.update_parameters(
            filter_type="Lowpass",
            resonance=0.4,
            poles=2
        )
        
        # Verify common parameters persisted
        assert noise_parameters.get_parameter("filter_type") == "Lowpass"
        assert noise_parameters.get_parameter("cutoff") == 0.7  # Should persist
        assert noise_parameters.get_parameter("volume") == 0.8  # Should persist
        assert noise_parameters.get_parameter("resonance") == 0.4
        assert noise_parameters.get_parameter("poles") == 2
        
        # Switch back to bandpass
        noise_parameters.update_parameters(
            filter_type="Bandpass",
            bandwidth=0.5
        )
        
        # Verify common parameters still persist
        assert noise_parameters.get_parameter("filter_type") == "Bandpass"
        assert noise_parameters.get_parameter("cutoff") == 0.7  # Should still persist
        assert noise_parameters.get_parameter("volume") == 0.8  # Should still persist
        assert noise_parameters.get_parameter("bandwidth") == 0.5
