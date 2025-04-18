from abc import ABC, abstractmethod

from ..entities.product_dto import ProductDTO


class ProductDTORepository(ABC):

    @abstractmethod
    def get_all(self) -> list[ProductDTO]:
        """Get all products"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> ProductDTO:
        """Get product by ID"""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> ProductDTO:
        """Get product by name"""
        pass

    @abstractmethod
    def get_by_manufacturer(self, manufacturer_id: str) -> list[ProductDTO]:
        """Get products by manufacturer ID"""
        pass

    @abstractmethod
    def add(self, product: ProductDTO) -> str:
        """Add a new product"""
        pass

    def add_all(self, products: list[ProductDTO]):
        """Add multiple products"""
        pass

    @abstractmethod
    def update(self, product: ProductDTO) -> ProductDTO:
        """Update an existing product"""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete a product by ID"""
        pass
