from unittest.mock import Mock

from src.application.get_all_products import GetAllProducts
from src.domain.entities.product_dto import ProductDTO


class TestGetAllProducts:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.get_all_products_use_case = GetAllProducts(self.mock_repository)

        # Sample product data for testing
        self.sample_products = [
            ProductDTO(
                id="product-1",
                name="Test Product 1",
                brand="Test Brand",
                manufacturer_id="manufacturer-1",
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
                manufacturer_id="manufacturer-2",
                description="Test Description 2",
                stock=20,
                details={"weight": "300g", "color": "blue"},
                storage_conditions="Refrigerated",
                price=150.0,
                currency="USD",
                delivery_time=5,
                images=["image3.jpg"]
            )
        ]

    def test_get_all_products_successfully(self):
        """Test successful retrieval of all products"""
        # Configure mock to return sample products
        self.mock_repository.get_all.return_value = self.sample_products

        # Execute the use case
        result = self.get_all_products_use_case.execute()

        # Verify repository interactions
        self.mock_repository.get_all.assert_called_once()

        # Verify result
        assert len(result) == 2
        assert result[0].id == "product-1"
        assert result[1].id == "product-2"
        assert result == self.sample_products

    def test_get_all_products_empty_result(self):
        """Test retrieval when no products exist"""
        # Configure mock to return empty list
        self.mock_repository.get_all.return_value = []

        # Execute the use case
        result = self.get_all_products_use_case.execute()

        # Verify repository interactions
        self.mock_repository.get_all.assert_called_once()

        # Verify result is an empty list
        assert isinstance(result, list)
        assert len(result) == 0
