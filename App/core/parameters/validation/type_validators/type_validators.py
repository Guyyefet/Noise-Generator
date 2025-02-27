from App.core.parameters.validation.validator import BaseParameterValidator
from App.core.parameters.base.parameter import Parameter
from typing import Optional, Union

class FloatParameterValidator(BaseParameterValidator):
    """Validator for float parameters"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate float parameter value"""
        super().validate(parameter)
        if not isinstance(parameter.value, float):
            raise TypeError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"must be of type float"
            )

class IntParameterValidator(BaseParameterValidator):
    """Validator for integer parameters"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate integer parameter value"""
        super().validate(parameter)
        if not isinstance(parameter.value, int):
            raise TypeError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"must be of type int"
            )

class StringParameterValidator(BaseParameterValidator):
    """Validator for string parameters"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate string parameter value"""
        super().validate(parameter)
        if not isinstance(parameter.value, str):
            raise TypeError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"must be of type str"
            )

class EnumParameterValidator(BaseParameterValidator):
    """Validator for enum parameters"""
    
    def validate(self, parameter: Parameter) -> None:
        """Validate enum parameter value"""
        super().validate(parameter)
        if parameter.enum_values is None:
            raise ValueError(
                f"Parameter {parameter.name} must have enum_values defined"
            )
            
        if parameter.value not in parameter.enum_values:
            raise ValueError(
                f"Parameter {parameter.name} value {parameter.value} "
                f"must be one of {parameter.enum_values}"
            )
