from abc import ABC, abstractmethod
from App.core.parameters.base.parameter import Parameter
from typing import Optional

class BaseParameterValidator(ABC):
    """Abstract base class for parameter validation"""
    
    @abstractmethod
    def validate(self, parameter: Parameter) -> None:
        """Validate a parameter's value against its constraints"""
        self._validate_range(parameter)
        self._validate_step_size(parameter)
        self._validate_custom_rules(parameter)
        
    def _validate_range(self, parameter: Parameter) -> None:
        """Validate that value is within min/max range"""
        if parameter.min_value is not None and parameter.value < parameter.min_value:
            raise ValueError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"is below minimum {parameter.min_value}"
            )
            
        if parameter.max_value is not None and parameter.value > parameter.max_value:
            raise ValueError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"is above maximum {parameter.max_value}"
            )

    def _validate_step_size(self, parameter: Parameter) -> None:
        """Validate that the value adheres to the step size constraint"""
        if parameter.step_size is not None:
            if parameter.step_size <= 0:
                raise ValueError("Step size must be greater than 0")
                
            if parameter.min_value is not None:
                steps = (parameter.value - parameter.min_value) / parameter.step_size
                if not steps.is_integer():
                    raise ValueError(
                        f"Parameter {parameter.name} value {parameter.value} "
                        f"is not a valid step from minimum {parameter.min_value} "
                        f"with step size {parameter.step_size}"
                    )

    def _validate_custom_rules(self, parameter: Parameter) -> None:
        """Validate against any custom validation rules"""
        for rule_name, rule_func in parameter.validation_rules.items():
            if not rule_func(parameter.value):
                raise ValueError(
                    f"Parameter {parameter.name} value {parameter.value} "
                    f"failed validation rule: {rule_name}"
                )
