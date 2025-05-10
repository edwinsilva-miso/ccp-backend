import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from datetime import datetime, timedelta
from unittest.mock import patch, Mock, MagicMock

from freezegun import freeze_time
from src.adapters.clients_adapter import ClientsAdapter


class TestClientsAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = ClientsAdapter()
        self.mock_jwt = "mock_jwt_token"
        self.mock_client_id = "client123"
        self.mock_order_id = "order456"
        self.mock_order_data = {
            "clientId": self.mock_client_id,
            "orderDetails": [
                {"productId": "product789", "quantity": 2}
            ]
        }

    def test_create_order_success(self):
        # Mock both the client adapter's post and the product adapter's get
        with patch('src.adapters.clients_adapter.requests.post') as mock_post, \
                patch('src.adapters.products_adapter.requests.get') as mock_product_get:
            # Set up client order response
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": self.mock_order_id,
                "clientId": self.mock_client_id,
                "orderDetails": [
                    {"productId": "product789", "quantity": 2}
                ]
            }
            mock_post.return_value = mock_response

            # Set up product get response
            mock_product_response = Mock()
            mock_product_response.status_code = 200
            mock_product_response.json.return_value = {
                "id": "product789",
                "name": "Test Product",
                "brand": "Test Brand",
                "deliveryTime": 3
            }
            mock_product_get.return_value = mock_product_response

            # Call method
            result, status_code = self.adapter.create_order(self.mock_jwt, self.mock_order_data)

            # Assertions
            self.assertEqual(status_code, 201)
            self.assertEqual(result["id"], self.mock_order_id)
            mock_post.assert_called_once()
            # Don't need to assert on ProductsAdapter.get_product_by_id since we're mocking lower level

    def test_create_order_pending_payment(self):
        # Mock both the client adapter's post and the product adapter's get
        with patch('src.adapters.clients_adapter.requests.post') as mock_post, \
                patch('src.adapters.products_adapter.requests.get') as mock_product_get:
            # Set up client order response
            mock_response = Mock()
            mock_response.status_code = 402
            mock_response.json.return_value = {
                "id": self.mock_order_id,
                "clientId": self.mock_client_id,
                "orderDetails": [
                    {"productId": "product789", "quantity": 2}
                ]
            }
            mock_post.return_value = mock_response

            # Set up product get response
            mock_product_response = Mock()
            mock_product_response.status_code = 200
            mock_product_response.json.return_value = {
                "id": "product789",
                "name": "Test Product",
                "brand": "Test Brand",
                "deliveryTime": 3
            }
            mock_product_get.return_value = mock_product_response

            # Call method
            result, status_code = self.adapter.create_order(self.mock_jwt, self.mock_order_data)

            # Assertions
            self.assertEqual(status_code, 402)
            self.assertEqual(result["id"], self.mock_order_id)
            mock_post.assert_called_once()
            mock_product_get.assert_called_once()

    @patch('src.adapters.clients_adapter.requests.get')
    def test_lists_orders(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "order1", "clientId": self.mock_client_id},
            {"id": "order2", "clientId": self.mock_client_id}
        ]
        mock_get.return_value = mock_response

        # Call method
        result, status_code = self.adapter.lists_orders(self.mock_jwt, self.mock_client_id)

        # Assertions
        mock_get.assert_called_once_with(
            "http://localhost:5101/api/v1/clients/orders",
            headers={'Authorization': f'Bearer {self.mock_jwt}'},
            params={'clientId': self.mock_client_id}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(len(result), 2)

    def test_get_order_by_id(self):
        # Mock both the client adapter's get and the product adapter's get
        with patch('src.adapters.clients_adapter.requests.get') as mock_get, \
                patch('src.adapters.products_adapter.requests.get') as mock_product_get:
            # Set up client order response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": self.mock_order_id,
                "clientId": self.mock_client_id,
                "orderDetails": [
                    {"productId": "product789", "quantity": 2}
                ]
            }
            mock_get.return_value = mock_response

            # Set up product get response
            mock_product_response = Mock()
            mock_product_response.status_code = 200
            mock_product_response.json.return_value = {
                "id": "product789",
                "name": "Test Product",
                "brand": "Test Brand",
                "deliveryTime": 3
            }
            mock_product_get.return_value = mock_product_response

            # Call method
            result, status_code = self.adapter.get_order_by_id(self.mock_jwt, self.mock_order_id)

            # Assertions
            self.assertEqual(status_code, 200)
            self.assertEqual(result["id"], 'product789')  # Use self.mock_order_id, not 'product789'



    @freeze_time("2023-01-01")
    def test_enrich_product_information(self):
        # Setup test data
        order_data = {
            "orderDetails": [
                {"productId": "product789", "quantity": 2}
            ]
        }

        # Mock the product adapter's get
        with patch('src.adapters.products_adapter.requests.get') as mock_product_get:
            # Set up product get response
            mock_product_response = Mock()
            mock_product_response.status_code = 200
            mock_product_response.json.return_value = {
                "id": "product789",
                "name": "Test Product",
                "brand": "Test Brand",
                "deliveryTime": 3
            }
            mock_product_get.return_value = mock_product_response

            # Call method
            self.adapter._enrich_product_information(self.mock_jwt, order_data, 201)

            # Assertions
            self.assertEqual(order_data["orderDetails"][0]["name"], "Test Product")
            self.assertEqual(order_data["orderDetails"][0]["brand"], "Test Brand")
            self.assertEqual(order_data["orderDetails"][0]["deliveryTime"], "3 días")

            # Check delivery date (3 days from frozen time)
            expected_date = (datetime(2023, 1, 1) + timedelta(days=3)).strftime('%Y-%m-%d')
            self.assertEqual(order_data["orderDetails"][0]["deliveryDate"], expected_date)

            # Verify the adapter method was called
            mock_product_get.assert_called_once()