import unittest
from unittest.mock import MagicMock, patch

from src.application.create_many_products import CreateManyProducts


class TestCreateManyProducts(unittest.TestCase):

    def setUp(self):
        self.repository = MagicMock()
        self.use_case = CreateManyProducts(self.repository)

    @patch('src.application.create_many_products.ProductsJsonMapper')
    def test_process_successful(self, mock_mapper):
        # Arrange
        test_products = [
            MagicMock(),
            MagicMock()
        ]
        mock_mapper.from_json_to_dto_list.return_value = test_products
        test_message = {"products": [{"name": "Product 1"}, {"name": "Product 2"}]}

        # Act
        self.use_case.process(test_message)

        # Assert
        mock_mapper.from_json_to_dto_list.assert_called_once_with(test_message)
        self.repository.add_all.assert_called_once_with(test_products)

    @patch('src.application.create_many_products.ProductsJsonMapper')
    def test_process_empty_product_list(self, mock_mapper):
        # Arrange
        mock_mapper.from_json_to_dto_list.return_value = []
        test_message = {"products": []}

        # Act
        self.use_case.process(test_message)

        # Assert
        mock_mapper.from_json_to_dto_list.assert_called_once_with(test_message)
        self.repository.add_all.assert_not_called()

    @patch('src.application.create_many_products.ProductsJsonMapper')
    @patch('src.application.create_many_products.logging')
    def test_process_logs_correctly(self, mock_logging, mock_mapper):
        # Arrange
        test_products = [MagicMock(), MagicMock()]
        mock_mapper.from_json_to_dto_list.return_value = test_products
        test_message = {"products": [{"name": "Product 1"}, {"name": "Product 2"}]}

        # Act
        self.use_case.process(test_message)

        # Assert
        self.assertEqual(mock_logging.debug.call_count, 4)
        mock_logging.debug.assert_any_call("Begin creating multiple products...")
        mock_logging.debug.assert_any_call(f"Converting message to product list {test_message}...")
        mock_logging.debug.assert_any_call(f"Creating {len(test_products)} products...")
        mock_logging.debug.assert_any_call("End creating multiple products...")

    @patch('src.application.create_many_products.ProductsJsonMapper')
    @patch('src.application.create_many_products.logging')
    def test_process_logs_error_when_no_products(self, mock_logging, mock_mapper):
        # Arrange
        mock_mapper.from_json_to_dto_list.return_value = []
        test_message = {"products": []}

        # Act
        self.use_case.process(test_message)

        # Assert
        mock_logging.error.assert_called_once_with("No products found in the message.")

    @patch('src.application.create_many_products.ProductsJsonMapper')
    def test_process_handles_none_message(self, mock_mapper):
        # Arrange
        mock_mapper.from_json_to_dto_list.return_value = []
        test_message = None

        # Act
        self.use_case.process(test_message)

        # Assert
        mock_mapper.from_json_to_dto_list.assert_called_once_with(None)
        self.repository.add_all.assert_not_called()

    @patch('src.application.create_many_products.ProductsJsonMapper')
    def test_repository_error_propagates(self, mock_mapper):
        # Arrange
        test_products = [MagicMock()]
        mock_mapper.from_json_to_dto_list.return_value = test_products
        self.repository.add_all.side_effect = Exception("Database error")
        test_message = {"products": [{"name": "Product 1"}]}

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.use_case.process(test_message)

        self.assertEqual(str(context.exception), "Database error")


if __name__ == '__main__':
    unittest.main()