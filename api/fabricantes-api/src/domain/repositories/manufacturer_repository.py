from abc import ABC, abstractmethod

from ..entities.manufacturer_dto import ManufacturerDTO


class ManufacturerRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[ManufacturerDTO]:
        """Get all manufacturers"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> ManufacturerDTO:
        """Get manufacturer by ID"""
        pass

    @abstractmethod
    def get_by_nit(self, nit: str) -> ManufacturerDTO:
        """Get manufacturer by NIT"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> ManufacturerDTO:
        """Get manufacturer by EMAIL"""
        pass


    @abstractmethod
    def add(self, manufacturer: ManufacturerDTO) -> str:
        """Add a new manufacturer"""
        pass

    @abstractmethod
    def update(self, manufacturer: ManufacturerDTO) -> ManufacturerDTO:
        """Update an existing manufacturer"""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete a manufacturer by ID"""
        pass
