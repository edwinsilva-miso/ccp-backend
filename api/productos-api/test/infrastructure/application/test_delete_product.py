import pytest
from unittest.mock import Mock, patch

from src.application.delete_product import DeleteProduct
from src.application.errors.errors import ProductNotExistsError


class TestDeleteProduct:
    def setup_method(self):
        """Set up test environment before each test method"""
        self.mock_repository = Mock()
        self.delete_product_use_case = DeleteProduct(self.mock_repository)
        self.product_id = "test-product-id-123"

    def test_delete_product_successfully(self):
        """Test successful product deletion"""
        # Configure mock to return an existing product
        mock_product = Mock()
        self.mock_repository.get_by_id.return_value = mock_product

        # Execute the use case
        self.delete_product_use_case.execute(self.product_id)

        # Verify repository interactions
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)
        self.mock_repository.delete.assert_called_once_with(self.product_id)

    def test_delete_nonexistent_product(self):
        """Test deleting a product that doesn't exist"""
        # Configure mock to return None (product doesn't exist)
        self.mock_repository.get_by_id.return_value = None

        # Verify ProductNotExistsError is raised
        with pytest.raises(ProductNotExistsError):
            self.delete_product_use_case.execute(self.product_id)

        # Verify repository was called to check for existing product but not to delete
        self.mock_repository.get_by_id.assert_called_once_with(self.product_id)
        self.mock_repository.delete.assert_not_called()

