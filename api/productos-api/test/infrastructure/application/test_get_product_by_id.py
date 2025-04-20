from datetime import datetime

import pytest
from unittest.mock import Mock, patch

from src.application.get_product_by_id import GetProductById
from src.domain.entities.product_dto import ProductDTO
from src.application.errors.errors import ProductNotExistsError


class TestGetProductById:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.get_product_by_id_use_case = GetProductById(self.mock_repository)
        self.product_id = "test-product-id-123"

        # Sample product data for testing
        self.sample_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            details="{'test': 'details'}",
            storage_conditions="Test Storage Conditions",
            price=100.0,
            currency="USD",
            delivery_time=-5,
            images=["image1.jpg", "image2.jpg"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

    def test_get_product_by_id_successfully(self):
        """Test successful retrieval of product by ID"""
        # Configure mock to return sample product
        self.mock_repository.get_by_id.return_value = self.sample_product

        # Execute the use case
        result = self.get_product_by_id_use_case.execute(self.product_id)

        # Verify repository interactions
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)

        # Verify result
        assert result == self.sample_product
        assert result.id == self.product_id
        assert result.name == "Test Product"
        assert result.price == 100.0

    def test_get_nonexistent_product(self):
        """Test retrieving a product that doesn't exist"""
        # Configure mock to return None (product doesn't exist)
        self.mock_repository.get_by_id.return_value = None

        # Verify ProductNotExistsError is raised
        with pytest.raises(ProductNotExistsError):
            self.get_product_by_id_use_case.execute(self.product_id)

        # Verify repository was called
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)
