from abc import ABC, abstractmethod
from typing import Any

class ParameterInterface(ABC):
    """Interface defining the contract for all parameter types"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get parameter name"""
        pass

    @property
    @abstractmethod
    def value(self) -> Any:
        """Get current parameter value"""
        pass

    @value.setter
    @abstractmethod
    def value(self, value: Any) -> None:
        """Set parameter value"""
        pass

    @property
    @abstractmethod
    def default(self) -> Any:
        """Get default parameter value"""
        pass

    @property
    @abstractmethod
    def min_value(self) -> Any:
        """Get minimum allowed value"""
        pass

    @property
    @abstractmethod
    def max_value(self) -> Any:
        """Get maximum allowed value"""
        pass

    @property
    @abstractmethod
    def step_size(self) -> Any:
        """Get value step size"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get parameter description"""
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        """Get parameter unit"""
        pass

    @property
    @abstractmethod
    def is_readonly(self) -> bool:
        """Check if parameter is read-only"""
        pass
