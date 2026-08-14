# External Data Source Interface Abstraction

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ExternalDataSource(ABC):
    """Abstract Base Class for all external legal & property source adapters."""

    @abstractmethod
    def search(self, query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def fetch(self, record_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        pass
