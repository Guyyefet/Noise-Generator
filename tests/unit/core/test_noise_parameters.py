import pytest
from App.core.noise_parameters import NoiseParameters
from App.core.observer import Observer

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
