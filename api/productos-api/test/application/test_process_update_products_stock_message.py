import unittest
from unittest.mock import Mock, patch
from src.application.process_update_products_stock_message import ProcessUpdateProductsStockMessage
from src.domain.entities.product_dto import ProductDTO


class TestProcessUpdateProductsStockMessage(unittest.TestCase):
    def setUp(self):
        self.mock_product_repository = Mock()
        self.processor = ProcessUpdateProductsStockMessage(self.mock_product_repository)

    def test_process_empty_message(self):
        # Test with empty message
        message = {}
        self.processor.process(message)
        # Verify repository was not called
        self.mock_product_repository.get_by_id.assert_not_called()
        self.mock_product_repository.update.assert_not_called()

    def test_process_empty_products_list(self):
        # Test with empty products list
        message = {"products": []}
        self.processor.process(message)
        # Verify repository was not called
        self.mock_product_repository.get_by_id.assert_not_called()
        self.mock_product_repository.update.assert_not_called()

    def test_process_product_not_found(self):
        # Test when product is not found in repository
        message = {"products": [{"productId": "123", "quantity": 5}]}

        # Mock product not found
        self.mock_product_repository.get_by_id.return_value = None

        self.processor.process(message)

        # Verify repository calls
        self.mock_product_repository.get_by_id.assert_called_once_with("123")
        self.mock_product_repository.update.assert_not_called()

    def test_process_valid_message_single_product(self):
        # Test with single valid product
        message = {"products": [{"productId": "123", "quantity": 5}]}

        # Mock existing product
        mock_product = ProductDTO(
            id="123",
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="mfr1",
            description="description",
            stock=10,
            details={},
            storage_conditions="",
            price=100.0,
            currency="USD",
            delivery_time=3,
            images=[],
            created_at=None,
            updated_at=None
        )
        self.mock_product_repository.get_by_id.return_value = mock_product

        self.processor.process(message)

        # Verify repository calls
        self.mock_product_repository.get_by_id.assert_called_once_with("123")
        self.mock_product_repository.update.assert_called_once()

        # Verify stock was updated correctly
        updated_product = self.mock_product_repository.update.call_args[0][0]
        self.assertEqual(updated_product.stock, 5)

    def test_process_valid_message_multiple_products(self):
        # Test with multiple valid products
        message = {
            "products": [
                {"productId": "123", "quantity": 5},
                {"productId": "456", "quantity": 3}
            ]
        }

        # Mock existing products
        product1 = ProductDTO(
            id="123",
            name="Test Product 1",
            brand="Test Brand",
            manufacturer_id="mfr1",
            description="description",
            stock=10,
            details={},
            storage_conditions="",
            price=100.0,
            currency="USD",
            delivery_time=3,
            images=[],
            created_at=None,
            updated_at=None
        )

        product2 = ProductDTO(
            id="456",
            name="Test Product 2",
            brand="Test Brand",
            manufacturer_id="mfr2",
            description="description",
            stock=8,
            details={},
            storage_conditions="",
            price=200.0,
            currency="USD",
            delivery_time=5,
            images=[],
            created_at=None,
            updated_at=None
        )

        self.mock_product_repository.get_by_id.side_effect = lambda id: {
            "123": product1,
            "456": product2
        }.get(id)

        self.processor.process(message)

        # Verify repository calls
        self.assertEqual(self.mock_product_repository.get_by_id.call_count, 2)
        self.assertEqual(self.mock_product_repository.update.call_count, 2)

        # Get updated products
        calls = self.mock_product_repository.update.call_args_list
        updated_products = [call[0][0] for call in calls]

        # Verify stock was updated correctly for both products
        product1_updated = next(p for p in updated_products if p.id == "123")
        product2_updated = next(p for p in updated_products if p.id == "456")

        self.assertEqual(product1_updated.stock, 5)  # 10 - 5
        self.assertEqual(product2_updated.stock, 5)  # 8 - 3

    def test_process_missing_quantity(self):
        # Test with missing quantity
        message = {"products": [{"productId": "123"}]}

        # Mock existing product
        mock_product = ProductDTO(
            id="123",
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="mfr1",
            description="description",
            stock=10,
            details={},
            storage_conditions="",
            price=100.0,
            currency="USD",
            delivery_time=3,
            images=[],
            created_at=None,
            updated_at=None
        )
        self.mock_product_repository.get_by_id.return_value = mock_product

        with patch('logging.error') as mock_log:
            self.processor.process(message)
            # Since quantity is None, product should not be updated
            self.mock_product_repository.update.assert_not_called()


if __name__ == '__main__':
    unittest.main()