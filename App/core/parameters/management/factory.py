from App.core.parameters.base.parameter import Parameter
from App.core.parameters.base.parameter_interface import ParameterInterface
from App.core.parameters.validation.validator import BaseParameterValidator
from App.core.parameters.management.builder import ParameterDefinitionBuilder
from App.core.parameters.management.registry import ParameterRegistry
from typing import Dict, Type, Any

class ParameterFactory:
    """Creates and manages parameter instances."""
    
    def __init__(self, registry: ParameterRegistry):
        self.registry = registry
        self._parameter_types: Dict[str, Type[Parameter]] = {}
        self._validators: Dict[str, BaseParameterValidator] = {}
        
    def register_parameter_type(self, 
                             name: str,
                             parameter_class: Type[Parameter],
                             validator: BaseParameterValidator) -> None:
        """Register a new parameter type.
        
        Args:
            name: Name of parameter type
            parameter_class: Parameter class implementation
            validator: Validator for this parameter type
        """
        if name in self._parameter_types:
            raise ValueError(f"Parameter type '{name}' already registered")
            
        self._parameter_types[name] = parameter_class
        self._validators[name] = validator
        
    def create_parameter(self,
                       name: str,
                       parameter_type: Type[Parameter],
                       **kwargs) -> ParameterInterface:
        """Create a new parameter instance.
        
        Args:
            name: Name of parameter
            parameter_type: Type of parameter to create
            **kwargs: Additional parameter configuration
            
        Returns:
            New parameter instance
            
        Raises:
            ValueError: If parameter type not registered
        """
        if parameter_type not in self._parameter_types.values():
            raise ValueError(f"Unknown parameter type: {parameter_type.__name__}")
            
        # Create parameter using builder pattern
        builder = ParameterDefinitionBuilder(name)
        builder.set_type(parameter_type)
        
        # Configure parameter from kwargs
        if 'default_value' in kwargs:
            builder.set_default_value(kwargs['default_value'])
        if 'min_value' in kwargs:
            builder.set_min_value(kwargs['min_value'])
        if 'max_value' in kwargs:
            builder.set_max_value(kwargs['max_value'])
        if 'step_size' in kwargs:
            builder.set_step_size(kwargs['step_size'])
        if 'options' in kwargs:
            builder.set_options(kwargs['options'])
        if 'observers' in kwargs:
            for observer in kwargs['observers']:
                builder.add_observer(observer)
        if 'validator' in kwargs:
            builder.set_validator(kwargs['validator'])
            
        # Create and register parameter
        parameter_def = builder.build()
        parameter = parameter_type(parameter_def)
        self.registry.register(parameter)
        
        return parameter
        
    def get_validator(self, parameter_type: str) -> BaseParameterValidator:
        """Get validator for a parameter type.
        
        Args:
            parameter_type: Type of parameter to get validator for
            
        Returns:
            Validator instance
            
        Raises:
            ValueError: If parameter type not registered
        """
        if parameter_type not in self._validators:
            raise ValueError(f"No validator for parameter type: {parameter_type}")
        return self._validators[parameter_type]
