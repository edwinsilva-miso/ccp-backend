import unittest
from unittest.mock import Mock, patch
import uuid
import logging

from src.application.get_orders_by_salesman_id import GetOrderBySalesmanId
from src.domain.entities.order_dto import OrderDTO
from src.application.errors.errors import OrderNotExistsError


class TestGetOrderBySalesmanId(unittest.TestCase):
    def setUp(self):
        # Mock the repository
        self.order_repository = Mock()

        # Initialize the use case
        self.get_orders_by_salesman = GetOrderBySalesmanId(self.order_repository)

        # Create a sample salesman ID
        self.sample_salesman_id = str(uuid.uuid4())

        # Create sample orders for test data
        self.mock_orders = [
            Mock(spec=OrderDTO) for _ in range(3)
        ]

        # Configure each mock order with test data
        for i, order in enumerate(self.mock_orders):
            order.id = str(uuid.uuid4())
            order.salesman_id = self.sample_salesman_id
            order.client_id = f"client{i + 1}"
            order.status = "COMPLETADO"

    def test_execute_returns_orders_when_exist(self):
        # Setup
        self.order_repository.get_orders_by_salesman.return_value = self.mock_orders

        # Execute
        result = self.get_orders_by_salesman.execute(self.sample_salesman_id)

        # Verify
        self.order_repository.get_orders_by_salesman.assert_called_once_with(self.sample_salesman_id)
        self.assertEqual(result, self.mock_orders)
        self.assertEqual(len(result), 3)

        # Verify that all returned orders have the correct salesman ID
        for order in result:
            self.assertEqual(order.salesman_id, self.sample_salesman_id)

    def test_execute_raises_error_when_no_orders_exist(self):
        # Setup
        self.order_repository.get_orders_by_salesman.return_value = []

        # Execute and verify
        with self.assertRaises(OrderNotExistsError):
            self.get_orders_by_salesman.execute(self.sample_salesman_id)

        # Ensure repository was called with correct ID
        self.order_repository.get_orders_by_salesman.assert_called_once_with(self.sample_salesman_id)

    @patch('src.application.get_orders_by_salesman_id.logger')
    def test_execute_logs_debug_messages(self, mock_logger):
        # Setup
        self.order_repository.get_orders_by_salesman.return_value = self.mock_orders

        # Execute
        self.get_orders_by_salesman.execute(self.sample_salesman_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting process to get order by salesman...")
        mock_logger.debug.assert_any_call(f"Order fetched successfully: {self.mock_orders}")

    @patch('src.application.get_orders_by_salesman_id.logger')
    def test_execute_logs_not_found_message(self, mock_logger):
        # Setup
        self.order_repository.get_orders_by_salesman.return_value = []

        # Execute with expectation of error
        with self.assertRaises(OrderNotExistsError):
            self.get_orders_by_salesman.execute(self.sample_salesman_id)

        # Verify logging
        mock_logger.debug.assert_any_call("Starting process to get order by salesman...")
        mock_logger.debug.assert_any_call(f"Order associated to salesman {self.sample_salesman_id} not found.")

    def test_execute_with_empty_salesman_id(self):
        # Setup
        empty_id = ""
        self.order_repository.get_orders_by_salesman.return_value = []

        # Execute and verify
        with self.assertRaises(OrderNotExistsError):
            self.get_orders_by_salesman.execute(empty_id)

        # Ensure repository was called with empty ID
        self.order_repository.get_orders_by_salesman.assert_called_once_with(empty_id)


if __name__ == '__main__':
    unittest.main()