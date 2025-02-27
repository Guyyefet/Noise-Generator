from App.core.parameters.validation.validator import BaseParameterValidator
from App.core.parameters.base.parameter import Parameter
from typing import Optional, Callable

class RangeValidator(BaseParameterValidator):
    """Validator for parameter range constraints"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate parameter value against range constraints"""
        super().validate(parameter)
        self._validate_range(parameter)

class StepSizeValidator(BaseParameterValidator):
    """Validator for parameter step size constraints"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate parameter value against step size constraints"""
        super().validate(parameter)
        self._validate_step_size(parameter)

class CustomValidator(BaseParameterValidator):
    """Validator for custom validation rules"""
    
    def __init__(self, validation_fn: Callable[[Parameter], bool]):
        self._validation_fn = validation_fn
        
    def validate(self, parameter: Parameter) -> None:
        """Validate parameter using custom validation function"""
        super().validate(parameter)
        if not self._validation_fn(parameter):
            raise ValueError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"failed custom validation"
            )
