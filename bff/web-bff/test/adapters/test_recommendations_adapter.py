import pytest
from unittest.mock import patch, Mock
import json

from src.adapters.recommendations_adapter import RecommendationsAdapter


class TestRecommendationsAdapter:
    def setup_method(self):
        """Setup common test variables and mocks"""
        self.adapter = RecommendationsAdapter()
        self.jwt_token = "test_jwt_token"

        # Sample product data for decoration
        self.product_data = {
            "id": "PROD-123",
            "name": "Test Product",
            "description": "Test product description",
            "price": 100.0
        }

        # Sample recommendation data returned from API
        self.raw_recommendation = {
            "id": "REC-123",
            "productId": "PROD-123",
            "events": json.dumps([{"date": "2023-05-30", "name": "Sale Event"}]),
            "targetSalesAmount": 200.0,
            "currency": "USD",
            "recommendation": "La cantidad óptima a comprar para Test Product es 150 unidades.",
            "createdAt": "2023-05-15T10:30:00"
        }

        # Sample list of recommendations
        self.recommendations_list = [
            self.raw_recommendation,
            {
                "id": "REC-456",
                "productId": "PROD-456",
                "events": json.dumps([{"date": "2023-06-15", "name": "Summer Sale"}]),
                "targetSalesAmount": 300.0,
                "currency": "EUR",
                "recommendation": "La cantidad óptima a comprar para Test Product 2 es 200 unidades.",
                "createdAt": "2023-05-16T11:30:00"
            }
        ]

        # Sample recommendation data for making a new recommendation
        self.recommendation_request_data = {
            'product': {
                'id': 'PROD-123',
                'name': 'Test Product',
                'stock': 50
            },
            'projection': {
                'salesTarget': 200,
                'currency': 'USD'
            },
            'events': [
                {'date': '2023-05-30', 'name': 'Sale Event'}
            ],
            'manufacturer': {
                'name': 'Test Manufacturer'
            }
        }

    @patch('src.adapters.recommendations_adapter.requests.get')
    @patch('src.adapters.recommendations_adapter.ProductsAdapter')
    def test_get_all_recommendations_success(self, mock_products_adapter, mock_requests_get):
        """Test successful retrieval of all recommendations"""
        # Configure mocks
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.recommendations_list
        mock_requests_get.return_value = mock_response

        # Configure ProductsAdapter mock
        mock_product_adapter_instance = Mock()
        mock_products_adapter.return_value = mock_product_adapter_instance
        mock_product_adapter_instance.get_product_by_id.return_value = (self.product_data, 200)

        # Call the method
        recommendations, status_code = self.adapter.get_all_recommendations(self.jwt_token)

        # Assertions
        assert status_code == 200
        assert len(recommendations) == 2
        assert recommendations[0]['id'] == "REC-123"
        assert recommendations[0]['productName'] == "Test Product"

        # Verify product decoration was called for each recommendation
        assert mock_product_adapter_instance.get_product_by_id.call_count == 2

    @patch('src.adapters.recommendations_adapter.requests.get')
    def test_get_all_recommendations_failure(self, mock_requests_get):
        """Test handling of API failure when getting recommendations"""
        # Configure mock
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Forbidden"}
        mock_requests_get.return_value = mock_response

        # Call the method
        recommendations, status_code = self.adapter.get_all_recommendations(self.jwt_token)

        # Assertions
        assert status_code == 403
        assert recommendations is None

    @patch('src.adapters.recommendations_adapter.requests.post')
    @patch('src.adapters.recommendations_adapter.ProductsAdapter')
    def test_make_recommendation_success(self, mock_products_adapter, mock_requests_post):
        """Test successful creation of a recommendation"""
        # Configure mocks
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.raw_recommendation
        mock_requests_post.return_value = mock_response

        # Configure ProductsAdapter mock
        mock_product_adapter_instance = Mock()
        mock_products_adapter.return_value = mock_product_adapter_instance
        mock_product_adapter_instance.get_product_by_id.return_value = (self.product_data, 200)

        # Call the method
        recommendation, status_code = self.adapter.make_recommendation(
            self.jwt_token,
            self.recommendation_request_data
        )

        # Assertions
        assert status_code == 201
        assert recommendation['id'] == "REC-123"
        assert recommendation['productName'] == "Test Product"

        # Verify product decoration was called
        mock_product_adapter_instance.get_product_by_id.assert_called_once_with(
            self.jwt_token,
            "PROD-123"
        )

    @patch('src.adapters.recommendations_adapter.requests.post')
    def test_make_recommendation_failure(self, mock_requests_post):
        """Test handling of API failure when making a recommendation"""
        # Configure mock
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad Request"}
        mock_requests_post.return_value = mock_response

        # Call the method
        recommendation, status_code = self.adapter.make_recommendation(
            self.jwt_token,
            self.recommendation_request_data
        )

        # Assertions
        assert status_code == 400
        assert recommendation is None

    @patch('src.adapters.recommendations_adapter.ProductsAdapter')
    def test_decorate_recommendation_data(self, mock_products_adapter):
        """Test the decoration of recommendation data with product details"""
        # Configure ProductsAdapter mock
        mock_product_adapter_instance = Mock()
        mock_products_adapter.return_value = mock_product_adapter_instance
        mock_product_adapter_instance.get_product_by_id.return_value = (self.product_data, 200)

        # Call the method
        decorated_recommendation = self.adapter._decorate_recommendation_data(
            self.jwt_token,
            self.raw_recommendation
        )

        # Assertions
        assert decorated_recommendation['productName'] == "Test Product"
        mock_product_adapter_instance.get_product_by_id.assert_called_once_with(
            self.jwt_token,
            "PROD-123"
        )

    @patch('src.adapters.recommendations_adapter.os.environ.get')
    @patch('src.adapters.recommendations_adapter.requests.get')
    def test_custom_api_url(self, mock_requests_get, mock_environ_get):
        """Test that custom API URL from environment is used if provided"""
        # Set custom API URL
        custom_api_url = "http://custom-api-url:8080"
        mock_environ_get.return_value = custom_api_url

        # Re-initialize adapter to use the mocked environment variable
        adapter = RecommendationsAdapter()

        # Configure response mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_requests_get.return_value = mock_response

        # Call the method
        adapter.get_all_recommendations(self.jwt_token)