from unittest.mock import Mock

import pytest
from src.application.errors.errors import ProductNotExistsError
from src.application.get_product_by_manufacturer import GetProductByManufacturer
from src.domain.entities.product_dto import ProductDTO


class TestGetProductByManufacturer:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.get_product_by_manufacturer_use_case = GetProductByManufacturer(self.mock_repository)
        self.manufacturer_id = "test-manufacturer-id-123"

        # Sample product data for testing
        self.sample_products = [
            ProductDTO(
                id="product-1",
                name="Test Product 1",
                brand="Test Brand",
                manufacturer_id=self.manufacturer_id,
                description="Test Description 1",
                stock=10,
                details={"weight": "500g", "color": "red"},
                storage_conditions="Room temperature",
                price=100.0,
                currency="USD",
                delivery_time=3,
                images=["image1.jpg", "image2.jpg"]
            ),
            ProductDTO(
                id="product-2",
                name="Test Product 2",
                brand="Test Brand",
                manufacturer_id=self.manufacturer_id,
                stock=20,
                description="Test Description 2",
                details={"weight": "300g", "color": "blue"},
                storage_conditions="Refrigerated",
                price=150.0,
                currency="USD",
                delivery_time=5,
                images=["image3.jpg"]
            )
        ]

    def test_get_products_by_manufacturer_successfully(self):
        """Test successful retrieval of products by manufacturer ID"""
        # Configure mock to return sample products
        self.mock_repository.get_by_manufacturer.return_value = self.sample_products

        # Execute the use case
        result = self.get_product_by_manufacturer_use_case.execute(self.manufacturer_id)

        # Verify repository interactions
        self.mock_repository.get_by_manufacturer.assert_called_once_with(self.manufacturer_id)

        # Verify result
        assert len(result) == 2
        assert result[0].id == "product-1"
        assert result[1].id == "product-2"
        assert all(product.manufacturer_id == self.manufacturer_id for product in result)

    def test_get_products_manufacturer_no_products(self):
        """Test retrieving products for a manufacturer that doesn't exist"""
        # Configure mock to return an empty list
        self.mock_repository.get_by_manufacturer.return_value = None

        # Verify ProductNotExistsError is raised
        with pytest.raises(ProductNotExistsError):
            self.get_product_by_manufacturer_use_case.execute(self.manufacturer_id)

        # Verify repository was called
        self.mock_repository.get_by_manufacturer.assert_called_once_with(self.manufacturer_id)
