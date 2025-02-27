from typing import Optional
from App.core.parameters.base.parameter import Parameter

class FloatParameter(Parameter):
    """Parameter implementation for floating-point values"""
    
    def __init__(
        self,
        name: str,
        value: float,
        default: float,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        step_size: Optional[float] = None,
        description: Optional[str] = None,
        unit: Optional[str] = None,
        is_readonly: bool = False
    ):
        super().__init__(
            name=name,
            value=value,
            default=default,
            min_value=min_value,
            max_value=max_value,
            step_size=step_size,
            description=description,
            unit=unit,
            is_readonly=is_readonly
        )
