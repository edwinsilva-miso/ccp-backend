import unittest
from unittest.mock import Mock, patch
import uuid
import logging

from src.application.list_orders import ListOrders
from src.domain.entities.order_dto import OrderDTO
from src.application.errors.errors import OrdersNotFoundError


class TestListOrders(unittest.TestCase):
    def setUp(self):
        # Mock the repository
        self.order_repository = Mock()

        # Initialize the use case
        self.list_orders = ListOrders(self.order_repository)

        # Create a sample client ID
        self.sample_client_id = str(uuid.uuid4())

        # Create sample orders for test data
        self.mock_orders = [
            Mock(spec=OrderDTO) for _ in range(3)
        ]

        # Configure each mock order with test data
        for i, order in enumerate(self.mock_orders):
            order.id = str(uuid.uuid4())
            order.client_id = self.sample_client_id
            order.status = f"STATUS_{i+1}"
            order.total = 100 * (i+1)

    def test_execute_returns_orders_when_exist(self):
        # Setup
        self.order_repository.get_orders_by_client.return_value = self.mock_orders

        # Execute
        result = self.list_orders.execute(self.sample_client_id)

        # Verify
        self.order_repository.get_orders_by_client.assert_called_once_with(self.sample_client_id)
        self.assertEqual(result, self.mock_orders)
        self.assertEqual(len(result), 3)

        # Verify that all returned orders have the correct client ID
        for order in result:
            self.assertEqual(order.client_id, self.sample_client_id)

    def test_execute_raises_error_when_no_orders_exist(self):
        # Setup
        self.order_repository.get_orders_by_client.return_value = []

        # Execute and verify
        with self.assertRaises(OrdersNotFoundError):
            self.list_orders.execute(self.sample_client_id)

        # Ensure repository was called with correct ID
        self.order_repository.get_orders_by_client.assert_called_once_with(self.sample_client_id)

    @patch('src.application.list_orders.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Setup
        self.order_repository.get_orders_by_client.return_value = self.mock_orders

        # Execute
        self.list_orders.execute(self.sample_client_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting order listing process...")
        mock_logger.debug.assert_any_call(f"Orders fetched for client {self.sample_client_id}: {len(self.mock_orders)} orders found.")

    @patch('src.application.list_orders.logger')
    def test_execute_logs_not_found_message(self, mock_logger):
        # Setup
        self.order_repository.get_orders_by_client.return_value = []

        # Execute with expectation of error
        with self.assertRaises(OrdersNotFoundError):
            self.list_orders.execute(self.sample_client_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting order listing process...")
        mock_logger.debug.assert_any_call(f"No orders found for client {self.sample_client_id}.")

    def test_execute_with_empty_client_id(self):
        # Setup
        empty_id = ""
        self.order_repository.get_orders_by_client.return_value = []

        # Execute and verify
        with self.assertRaises(OrdersNotFoundError):
            self.list_orders.execute(empty_id)

        # Ensure repository was called with empty ID
        self.order_repository.get_orders_by_client.assert_called_once_with(empty_id)


if __name__ == '__main__':
    unittest.main()