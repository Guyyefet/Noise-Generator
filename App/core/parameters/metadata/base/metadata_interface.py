from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class IMetadata(ABC):
    """Interface defining the contract for parameter metadata operations."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve metadata value by key.
        
        Args:
            key: The metadata key to retrieve
            
        Returns:
            The metadata value or None if not found
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set metadata value for a given key.
        
        Args:
            key: The metadata key to set
            value: The value to associate with the key
        """
        pass
    
    @abstractmethod
    def remove(self, key: str) -> bool:
        """Remove metadata entry by key.
        
        Args:
            key: The metadata key to remove
            
        Returns:
            True if the key was found and removed, False otherwise
        """
        pass
    

