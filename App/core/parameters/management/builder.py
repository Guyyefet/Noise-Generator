from typing import Any, Dict, List, Optional, Type
from App.core.parameters.base.parameter import Parameter
from App.core.parameters.validation.validator import BaseParameterValidator
from App.core.parameters.notification.observer import ParameterObserver

class ParameterDefinitionBuilder:
    def __init__(self, name: str):
        self._name = name
        self._type: Optional[Type[Parameter]] = None
        self._default_value: Any = None
        self._min_value: Optional[float] = None
        self._max_value: Optional[float] = None
        self._step_size: Optional[float] = None
        self._options: Optional[List[str]] = None
        self._observers: List[ParameterObserver] = []
        self._validator: Optional[BaseParameterValidator] = None

    def set_type(self, parameter_type: Type[Parameter]):
        """Set the parameter type."""
        self._type = parameter_type
        return self

    def set_default_value(self, value: Any):
        """Set the default value."""
        self._default_value = value
        return self

    def set_min_value(self, value: float):
        """Set the minimum value."""
        self._min_value = value
        return self

    def set_max_value(self, value: float):
        """Set the maximum value."""
        self._max_value = value
        return self

    def set_step_size(self, step: float):
        """Set the step size."""
        self._step_size = step
        return self

    def set_options(self, options: List[str]):
        """Set available options for enum parameters."""
        self._options = options
        return self

    def add_observer(self, observer: ParameterObserver):
        """Add a parameter observer."""
        self._observers.append(observer)
        return self

    def set_validator(self, validator: BaseParameterValidator):
        """Set a custom validator."""
        self._validator = validator
        return self

    def build(self) -> Dict[str, Any]:
        """Build the parameter definition."""
        if not self._type:
            raise ValueError("Parameter type must be specified")
        if self._default_value is None:
            raise ValueError("Default value must be specified")

        return {
            "name": self._name,
            "type": self._type,
            "default_value": self._default_value,
            "min_value": self._min_value,
            "max_value": self._max_value,
            "step_size": self._step_size,
            "options": self._options,
            "observers": self._observers,
            "validator": self._validator
        }
