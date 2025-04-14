from abc import ABC, abstractmethod

from ..entities.provider_dto import ProviderDTO


class ProviderRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[ProviderDTO]:
        """Get all providers"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> ProviderDTO:
        """Get provider by ID"""
        pass

    @abstractmethod
    def get_by_nit(self, nit: str) -> ProviderDTO:
        """Get provider by NIT"""
        pass

    @abstractmethod
    def add(self, provider: ProviderDTO) -> str:
        """Add a new provider"""
        pass

    @abstractmethod
    def update(self, provider: ProviderDTO) -> ProviderDTO:
        """Update an existing provider"""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete a provider by ID"""
        pass
