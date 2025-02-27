from typing import Dict, Any, Optional, Tuple
from App.core.parameters.notification.observer import ParameterSubject
from App.core.parameters.validation.validator import BaseParameterValidator
from App.core.parameters.metadata.base.parameter_metadata import ParameterMetadata

class ParameterRegistry(ParameterSubject):
    """Central registry for managing audio parameters and their metadata."""
    
    def __init__(self):
        super().__init__()
        self._parameters: Dict[str, Any] = {}
        self._metadata: Dict[str, ParameterMetadata] = {}
        self._validator = BaseParameterValidator()
        
    def register(self, name: str, parameter: Any, metadata: Optional[ParameterMetadata] = None) -> None:
        """Register a new parameter with optional metadata.
        
        Args:
            name: Unique name for the parameter
            parameter: Parameter object to register
            metadata: Optional metadata for the parameter
            
        Raises:
            ValueError: If parameter name already exists
        """
        if name in self._parameters:
            raise ValueError(f"Parameter '{name}' already registered")
            
        self._validator.validate(parameter)
        self._parameters[name] = parameter
        if metadata:
            self._metadata[name] = metadata
        self.notify({name: parameter})
        
    def get(self, name: str, include_metadata: bool = False) -> Any:
        """Get a registered parameter.
        
        Args:
            name: Name of parameter to retrieve
            include_metadata: If True, returns a tuple of (parameter, metadata)
            
        Returns:
            The registered parameter object or tuple of (parameter, metadata)
            
        Raises:
            KeyError: If parameter not found
        """
        if name not in self._parameters:
            raise KeyError(f"Parameter '{name}' not found")
            
        if include_metadata:
            return (self._parameters[name], self._metadata.get(name))
        return self._parameters[name]
        
    def get_all(self, include_metadata: bool = False) -> Dict[str, Any]:
        """Get all registered parameters.
        
        Args:
            include_metadata: If True, includes metadata in the returned dictionary
            
        Returns:
            Dictionary of all registered parameters, optionally with metadata
        """
        if include_metadata:
            return {
                name: (param, self._metadata.get(name))
                for name, param in self._parameters.items()
            }
        return self._parameters.copy()
        
    def get_metadata(self, name: str) -> Optional[ParameterMetadata]:
        """Get metadata for a specific parameter.
        
        Args:
            name: Name of parameter to retrieve metadata for
            
        Returns:
            The parameter's metadata if it exists, None otherwise
        """
        return self._metadata.get(name)
        
    def update_metadata(self, name: str, metadata: ParameterMetadata) -> None:
        """Update metadata for a parameter.
        
        Args:
            name: Name of parameter to update
            metadata: New metadata to store
            
        Raises:
            KeyError: If parameter not found
        """
        if name not in self._parameters:
            raise KeyError(f"Parameter '{name}' not found")
        self._metadata[name] = metadata
