import unittest
from unittest.mock import patch, Mock
import os
import json
from src.adapters.products_adapter import ProductsAdapter


class TestProductsAdapter(unittest.TestCase):

    def setUp(self):
        self.products_adapter = ProductsAdapter()
        self.jwt = "fake_jwt_token"
        self.product_id = "123e4567-e89b-12d3-a456-426614174000"
        self.manufacturer_id = '123e4567-e89b-12d3-a456-426614174001'
        self.product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "description": "Test Description",
            "manufacturerId": "123e4567-e89b-12d3-a456-426614174001",
            "details": "Test Details",
            "storageConditions": "Test Storage Conditions",
            "price": 100.0,
            "currency": "USD",
            "deliveryTime": "1-2 days",
            "images": ["image1.jpg", "image2.jpg"]
        }
        self.expected_headers = {'Authorization': f'Bearer {self.jwt}'}

    @patch('src.adapters.products_adapter.requests.get')
    def test_get_all_products(self, mock_get):
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = [self.product_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.get_all_products(self.jwt)

        # Verify the result
        self.assertEqual(result, [self.product_data])
        self.assertEqual(status_code, 200)


    @patch('src.adapters.products_adapter.requests.get')
    def test_get_product_by_id(self, mock_get):
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = self.product_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.get_product_by_id(self.jwt, self.product_id)

        # Verify the result
        self.assertEqual(result, self.product_data)
        self.assertEqual(status_code, 200)

    @patch('src.adapters.products_adapter.requests.get')
    def test_get_product_by_manufacturer(self, mock_get):
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = self.product_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.get_products_by_manufacturer(self.jwt, self.manufacturer_id)

        # Verify the result
        self.assertEqual(result, self.product_data)
        self.assertEqual(status_code, 200)

    @patch('src.adapters.products_adapter.requests.post')
    def test_create_product(self, mock_post):
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {"id": self.product_id}
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.create_product(self.jwt, self.product_data)

        # Verify the result
        self.assertEqual(result, {"id": self.product_id})
        self.assertEqual(status_code, 201)

    @patch('src.adapters.products_adapter.requests.put')
    def test_update_product(self, mock_put):
        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = self.product_data
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.update_product(self.jwt, self.product_id, self.product_data)

        # Verify the result
        self.assertEqual(result, self.product_data)
        self.assertEqual(status_code, 200)

    @patch('src.adapters.products_adapter.requests.delete')
    def test_delete_product_success(self, mock_delete):
        # Mock the response for successful deletion (204 No Content)
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.delete_product(self.jwt, self.product_id)

        # Verify the result
        self.assertEqual(result, {})
        self.assertEqual(status_code, 204)

    @patch('src.adapters.products_adapter.requests.delete')
    def test_delete_product_error(self, mock_delete):
        # Mock the response for error (e.g., 404 Not Found)
        mock_response = Mock()
        mock_response.json.return_value = {"msg": "Product not found"}
        mock_response.status_code = 404
        mock_delete.return_value = mock_response

        # Call the method
        result, status_code = self.products_adapter.delete_product(self.jwt, self.product_id)

        # Verify the result
        self.assertEqual(result, {"msg": "Product not found"})
        self.assertEqual(status_code, 404)


if __name__ == '__main__':
    unittest.main()