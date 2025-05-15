import unittest
from unittest.mock import Mock, patch
import uuid
import logging

from src.application.get_order_by_id import GetOrderById
from src.domain.entities.order_dto import OrderDTO
from src.application.errors.errors import OrderNotExistsError


class TestGetOrderById(unittest.TestCase):
    def setUp(self):
        # Mock the repository
        self.order_repository = Mock()

        # Initialize the use case
        self.get_order_by_id = GetOrderById(self.order_repository)

        # Create a sample order ID and mock order
        self.sample_order_id = str(uuid.uuid4())
        self.mock_order = Mock(spec=OrderDTO)
        self.mock_order.id = self.sample_order_id
        self.mock_order.client_id = "client123"
        self.mock_order.status = "COMPLETADO"

    def test_execute_returns_order_when_exists(self):
        # Setup
        self.order_repository.get_by_id.return_value = self.mock_order

        # Execute
        result = self.get_order_by_id.execute(self.sample_order_id)

        # Verify
        self.order_repository.get_by_id.assert_called_once_with(self.sample_order_id)
        self.assertEqual(result, self.mock_order)
        self.assertEqual(result.id, self.sample_order_id)
        self.assertEqual(result.client_id, "client123")
        self.assertEqual(result.status, "COMPLETADO")

    def test_execute_raises_error_when_order_not_exists(self):
        # Setup
        self.order_repository.get_by_id.return_value = None

        # Execute and verify
        with self.assertRaises(OrderNotExistsError):
            self.get_order_by_id.execute(self.sample_order_id)

        # Ensure repository was called with correct ID
        self.order_repository.get_by_id.assert_called_once_with(self.sample_order_id)

    @patch('src.application.get_order_by_id.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Setup
        self.order_repository.get_by_id.return_value = self.mock_order

        # Execute
        self.get_order_by_id.execute(self.sample_order_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting process to get order by ID...")
        mock_logger.debug.assert_any_call(f"Order fetched successfully: {self.mock_order}")

    @patch('src.application.get_order_by_id.logger')
    def test_execute_logs_not_found_message(self, mock_logger):
        # Setup
        self.order_repository.get_by_id.return_value = None

        # Execute with expectation of error
        with self.assertRaises(OrderNotExistsError):
            self.get_order_by_id.execute(self.sample_order_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting process to get order by ID...")
        mock_logger.debug.assert_any_call(f"Order with ID {self.sample_order_id} not found.")

    def test_execute_with_empty_id(self):
        # Setup
        empty_id = ""
        self.order_repository.get_by_id.return_value = None

        # Execute and verify
        with self.assertRaises(OrderNotExistsError):
            self.get_order_by_id.execute(empty_id)

        # Ensure repository was called with empty ID
        self.order_repository.get_by_id.assert_called_once_with(empty_id)


if __name__ == '__main__':
    unittest.main()