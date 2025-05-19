import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to sys.path to be able to import modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.blueprints.recommendation_blueprint import recommendation_blueprint


class TestRecommendationBlueprint(unittest.TestCase):

    def setUp(self):
        from flask import Flask
        self.app = Flask(__name__)
        self.app.register_blueprint(recommendation_blueprint)
        self.client = self.app.test_client()
        self.test_jwt = "test_jwt_token"

        # Sample recommendation data
        self.sample_recommendation = {
            "id": "rec-123",
            "productId": "PROD-123",
            "productName": "Test Product",
            "events": json.dumps([{"date": "2023-05-30", "name": "Sale Event"}]),
            "targetSalesAmount": 200.0,
            "currency": "USD",
            "recommendation": "La cantidad óptima a comprar para Test Product es 150 unidades.",
            "createdAt": "2023-05-15T10:30:00"
        }

        # Sample list of recommendations
        self.sample_recommendations = [
            self.sample_recommendation,
            {
                "id": "rec-456",
                "productId": "PROD-456",
                "productName": "Another Product",
                "events": json.dumps([{"date": "2023-06-15", "name": "Summer Sale"}]),
                "targetSalesAmount": 300.0,
                "currency": "EUR",
                "recommendation": "La cantidad óptima a comprar para Another Product es 200 unidades.",
                "createdAt": "2023-05-16T11:30:00"
            }
        ]

        # Sample data for making a recommendation
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

    @patch('src.blueprints.recommendation_blueprint.RecommendationsAdapter')
    def test_get_all_recommendations_success(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_all_recommendations.return_value = (self.sample_recommendations, 200)

        # Act
        response = self.client.get(
            '/bff/v1/mobile/recommendations',
            headers={'Authorization': f'Bearer {self.test_jwt}'}
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_adapter.get_all_recommendations.assert_called_once_with(self.test_jwt)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['id'], 'rec-123')
        self.assertEqual(response_data[1]['id'], 'rec-456')

    @patch('src.blueprints.recommendation_blueprint.RecommendationsAdapter')
    def test_get_all_recommendations_empty(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_all_recommendations.return_value = ([], 200)

        # Act
        response = self.client.get(
            '/bff/v1/mobile/recommendations',
            headers={'Authorization': f'Bearer {self.test_jwt}'}
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 0)

    @patch('src.blueprints.recommendation_blueprint.RecommendationsAdapter')
    def test_get_all_recommendations_error(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        error_response = {"error": "Access denied"}
        mock_adapter.get_all_recommendations.return_value = (error_response, 403)

        # Act
        response = self.client.get(
            '/bff/v1/mobile/recommendations',
            headers={'Authorization': f'Bearer {self.test_jwt}'}
        )

        # Assert
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertEqual(response_data, error_response)

    @patch('src.blueprints.recommendation_blueprint.RecommendationsAdapter')
    def test_make_recommendation_success(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.make_recommendation.return_value = (self.sample_recommendation, 201)

        # Act
        response = self.client.post(
            '/bff/v1/mobile/recommendations',
            headers={'Authorization': f'Bearer {self.test_jwt}'},
            json=self.recommendation_request_data
        )

        # Assert
        self.assertEqual(response.status_code, 201)
        mock_adapter.make_recommendation.assert_called_once_with(
            self.test_jwt, self.recommendation_request_data
        )
        response_data = json.loads(response.data)
        self.assertEqual(response_data['id'], 'rec-123')
        self.assertEqual(response_data['productName'], 'Test Product')

    @patch('src.blueprints.recommendation_blueprint.RecommendationsAdapter')
    def test_make_recommendation_error(self, mock_adapter_class):
        # Arrange
        mock_adapter = MagicMock()
        mock_adapter_class.return_value = mock_adapter
        error_response = {"error": "Invalid data"}
        mock_adapter.make_recommendation.return_value = (error_response, 400)

        # Act
        response = self.client.post(
            '/bff/v1/mobile/recommendations',
            headers={'Authorization': f'Bearer {self.test_jwt}'},
            json=self.recommendation_request_data
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data, error_response)

    def test_missing_auth_token_get(self):
        # Act
        response = self.client.get('/bff/v1/mobile/recommendations')

        # Assert
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['msg'], 'Unauthorized')

    def test_missing_auth_token_post(self):
        # Act
        response = self.client.post(
            '/bff/v1/mobile/recommendations',
            json=self.recommendation_request_data
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['msg'], 'Unauthorized')


if __name__ == '__main__':
    unittest.main()