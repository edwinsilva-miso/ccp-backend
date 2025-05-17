import unittest
from unittest.mock import patch, MagicMock
import json

from flask import Flask
from src.blueprints.orders_blueprint import orders_blueprint


class TestOrdersBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(orders_blueprint)
        self.client = self.app.test_client()
        self.test_jwt = "test_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.test_jwt}'}

    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_get_all_orders_success(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.list_orders.return_value = (
            {"orders": [{"id": 1}, {"id": 2}]},
            200
        )

        # Act
        response = self.client.get('/bff/v1/web/orders', headers=self.auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"orders": [{"id": 1}, {"id": 2}]})
        mock_adapter.list_orders.assert_called_once_with(self.test_jwt)

    def test_get_all_orders_missing_token(self):
        # Act
        response = self.client.get('/bff/v1/web/orders')

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'msg': 'Unauthorized'})

    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_get_order_by_id_success(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_order_by_id.return_value = (
            {"id": 1, "orderItems": [{"productId": 101, "productName": "Test Product"}]},
            200
        )

        # Act
        response = self.client.get('/bff/v1/web/orders/1', headers=self.auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": 1,
            "orderItems": [{"productId": 101, "productName": "Test Product"}]
        })
        mock_adapter.get_order_by_id.assert_called_once_with(self.test_jwt, "1")

    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_get_order_by_id_not_found(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_order_by_id.return_value = ({"msg": "Order not found"}, 404)

        # Act
        response = self.client.get('/bff/v1/web/orders/999', headers=self.auth_header)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"msg": "Order not found"})
        mock_adapter.get_order_by_id.assert_called_once_with(self.test_jwt, "999")

    def test_get_order_by_id_missing_token(self):
        # Act
        response = self.client.get('/bff/v1/web/orders/1')

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'msg': 'Unauthorized'})

    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_token_without_bearer_prefix(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.list_orders.return_value = ({"orders": []}, 200)

        # Act
        response = self.client.get(
            '/bff/v1/web/orders',
            headers={'Authorization': self.test_jwt}  # No 'Bearer ' prefix
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_adapter.list_orders.assert_called_once_with(self.test_jwt)

    @patch('src.blueprints.orders_blueprint.logger')
    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_logging_in_get_all_orders(self, mock_adapter_class, mock_logger):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.list_orders.return_value = ({"orders": []}, 200)

        # Act
        self.client.get('/bff/v1/web/orders', headers=self.auth_header)

        # Assert
        mock_logger.debug.assert_any_call("Received request to get all orders.")
        mock_logger.debug.assert_any_call("Retrieving all orders from BFF Web.")

    @patch('src.blueprints.orders_blueprint.logger')
    @patch('src.blueprints.orders_blueprint.OrdersAdapter')
    def test_logging_in_get_order_by_id(self, mock_adapter_class, mock_logger):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_order_by_id.return_value = ({"id": 1}, 200)

        # Act
        self.client.get('/bff/v1/web/orders/1', headers=self.auth_header)

        # Assert
        mock_logger.debug.assert_any_call("Received request to get order with ID: 1")
        mock_logger.debug.assert_any_call("Retrieving order by ID from BFF Web.")