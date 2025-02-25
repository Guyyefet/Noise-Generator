from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

@dataclass
class ParameterRange:
    min_value: float
    max_value: float

@dataclass
class ParameterDefinition:
    type: str
    default_value: Any
    range: Optional[ParameterRange] = None
    enum_values: Optional[List[str]] = None
    display_name: Optional[str] = None
    units: Optional[str] = None

class ParameterDefinitionBuilder:
    def __init__(self):
        self._type = None
        self._default_value = None
        self._range = None
        self._enum_values = None
        self._display_name = None
        self._units = None

    def float(self):
        self._type = "float"
        return self

    def int(self):
        self._type = "int"
        return self

    def string(self):
        self._type = "string"
        return self

    def boolean(self):
        self._type = "boolean"
        return self

    def enum(self, values: List[str]):
        self._type = "enum"
        self._enum_values = values
        return self

    def default(self, value: Any):
        self._default_value = value
        return self

    def range(self, min_val: float, max_val: float):
        self._range = ParameterRange(min_val, max_val)
        return self

    def display(self, name: str):
        self._display_name = name
        return self

    def units(self, units: str):
        self._units = units
        return self

    def build(self) -> Dict[str, Any]:
        if not self._type or self._default_value is None:
            raise ValueError("Type and default value must be specified")
            
        return {
            "type": self._type,
            "default_value": self._default_value,
            "range": self._range,
            "enum_values": self._enum_values,
            "display_name": self._display_name,
            "units": self._units
        }
