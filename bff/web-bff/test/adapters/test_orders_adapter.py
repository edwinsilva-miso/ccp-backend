import unittest
from unittest.mock import patch, MagicMock

from src.adapters.orders_adapter import OrdersAdapter


class TestOrdersAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = OrdersAdapter()
        self.test_jwt = "test_jwt_token"

    @patch('src.adapters.orders_adapter.requests.get')
    def test_list_orders_success(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"orders": [{"id": 1}, {"id": 2}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result, status_code = self.adapter.list_orders(self.test_jwt)

        # Assert
        mock_get.assert_called_once_with(
            "http://localhost:5100/api/v1/orders",
            headers={'Authorization': 'Bearer test_jwt_token'}
        )
        self.assertEqual(result, {"orders": [{"id": 1}, {"id": 2}]})
        self.assertEqual(status_code, 200)

    @patch('src.adapters.orders_adapter.requests.get')
    def test_get_order_by_id_success(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 1,
            "orderItems": [{"productId": 101}]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock the _decorate_order method
        self.adapter._decorate_order = MagicMock(return_value={
            "id": 1,
            "orderItems": [{"productId": 101, "productName": "Test Product"}]
        })

        # Act
        result, status_code = self.adapter.get_order_by_id(self.test_jwt, 1)

        # Assert
        mock_get.assert_called_once_with(
            "http://localhost:5100/api/v1/orders/1",
            headers={'Authorization': 'Bearer test_jwt_token'}
        )
        self.adapter._decorate_order.assert_called_once_with(
            self.test_jwt, {"id": 1, "orderItems": [{"productId": 101}]}
        )
        self.assertEqual(result, {
            "id": 1,
            "orderItems": [{"productId": 101, "productName": "Test Product"}]
        })
        self.assertEqual(status_code, 200)

    @patch('src.adapters.orders_adapter.requests.get')
    def test_get_order_by_id_not_found(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "Order not found"}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Act
        result, status_code = self.adapter.get_order_by_id(self.test_jwt, 999)

        # Assert
        mock_get.assert_called_once_with(
            "http://localhost:5100/api/v1/orders/999",
            headers={'Authorization': 'Bearer test_jwt_token'}
        )
        self.assertEqual(result, None)
        self.assertEqual(status_code, 404)

    @patch('src.adapters.orders_adapter.ProductsAdapter')
    def test_decorate_order(self, mock_products_adapter_class):
        # Arrange
        mock_products_adapter = MagicMock()
        mock_products_adapter_class.return_value = mock_products_adapter

        # Mock product data returned by the product adapter
        mock_products_adapter.get_product_by_id.return_value = (
            {"id": 101, "name": "Test Product"},
            200
        )

        order_data = {
            "id": 1,
            "orderItems": [
                {"productId": 101},
                {"productId": 102}
            ]
        }

        # Act
        result = self.adapter._decorate_order(self.test_jwt, order_data)

        # Assert
        # Check that get_product_by_id was called twice (once for each product)
        self.assertEqual(mock_products_adapter.get_product_by_id.call_count, 2)
        mock_products_adapter.get_product_by_id.assert_any_call(self.test_jwt, 101)
        mock_products_adapter.get_product_by_id.assert_any_call(self.test_jwt, 102)

        # Check that the order was decorated with product names
        self.assertEqual(result["orderItems"][0]["productName"], "Test Product")
        self.assertEqual(result["orderItems"][1]["productName"], "Test Product")

    @patch('src.adapters.orders_adapter.requests.get')
    @patch('src.adapters.orders_adapter.logger')
    def test_list_orders_logs_debug_messages(self, mock_logger, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"orders": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        self.adapter.list_orders(self.test_jwt)

        # Assert
        mock_logger.debug.assert_any_call("Listing all orders")
        mock_logger.debug.assert_any_call("Response received from API: {'orders': []}")
