import unittest
from unittest.mock import patch, Mock

from src.adapters.products_adapter import ProductsAdapter


class TestProductsAdapter(unittest.TestCase):

    def setUp(self):
        self.products_adapter = ProductsAdapter()
        self.jwt = "fake_jwt_token"
        self.product_id = "123e4567-e89b-12d3-a456-426614174000"
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

    
if __name__ == '__main__':
    unittest.main()
