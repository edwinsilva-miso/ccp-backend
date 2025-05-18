import json
from unittest.mock import patch, Mock

import pytest
from src.domain.entities.recommentation_result_dto import RecommendationResultDTO
from src.interface.blueprints.recommendation_blueprint import recommendations_blueprint


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(recommendations_blueprint)

    # Configure app for testing
    app.config['TESTING'] = True

    # Mock container setup for token validation
    app.container = Mock()
    app.container.token_validator = Mock()

    return app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        # Create application context for the test
        with app.app_context():
            yield test_client


class TestRecommendationBlueprint:
    def setup_method(self):
        self.directivo_id = "456"
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Sample recommendation DTO
        self.sample_recommendation = RecommendationResultDTO(
            id="rec-123",
            product_id="PROD-123",
            events=json.dumps([{'date': '2023-05-30', 'name': 'Sale Event'}]),
            target_sales_amount=200,
            currency="USD",
            recommendation="La cantidad óptima a comprar para Test Product es 150 unidades.",
            created_at="2023-05-15T10:30:00"
        )

        # Sample list of recommendation DTOs
        self.sample_recommendations = [
            self.sample_recommendation,
            RecommendationResultDTO(
                id="rec-456",
                product_id="PROD-456",
                events=json.dumps([{'date': '2023-06-15', 'name': 'Summer Sale'}]),
                target_sales_amount=300,
                currency="EUR",
                recommendation="La cantidad óptima a comprar para Test Product 2 es 200 unidades.",
                created_at="2023-05-16T11:30:00"
            )
        ]

        # Sample request data for making a recommendation
        self.recommendation_data = {
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

    @patch('src.interface.blueprints.recommendation_blueprint.GetAllRecommendations')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_all_recommendations(self, mock_container, mock_get_all_recommendations, client):
        # Mock token validaor
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": self.directivo_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.sample_recommendations
        mock_get_all_recommendations.return_value = mock_use_case

        # Make request
        response = client.get(
            '/api/v1/recommendations/',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == "rec-123"
        assert data[1]['id'] == "rec-456"

        # Verify use case was called
        mock_use_case.execute.assert_called_once()

    @patch('src.interface.blueprints.recommendation_blueprint.MakeRecommendation')
    @patch('src.interface.decorator.token_decorator.container')
    def test_make_recommendation_successfully(self, mock_container, mock_make_recommendation, client):
        # Mock token verification
        # Mock token validaor
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": self.directivo_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock
        mock_use_case = Mock()
        mock_use_case.execute.return_value = self.sample_recommendation
        mock_make_recommendation.return_value = mock_use_case

        # Make request
        response = client.post(
            '/api/v1/recommendations/',
            json=self.recommendation_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['id'] == "rec-123"
        assert data['productId'] == "PROD-123"
        assert data['recommendation'] == "La cantidad óptima a comprar para Test Product es 150 unidades."

        # Verify use case was called with correct data
        mock_use_case.execute.assert_called_once_with(self.recommendation_data)

    @patch('src.interface.blueprints.recommendation_blueprint.GetAllRecommendations')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_all_recommendations_empty_list(self, mock_container, mock_get_all_recommendations, client):
        # Mock token verification
        # Mock token validaor
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": self.directivo_id}
        mock_container.token_validator = mock_auth_service

        # Configure the use case mock to return empty list
        mock_use_case = Mock()
        mock_use_case.execute.return_value = []
        mock_get_all_recommendations.return_value = mock_use_case

        # Make request
        response = client.get(
            '/api/v1/recommendations/',
            headers=self.auth_header
        )

        # Assertions
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    # AUTHENTICATION TESTS
    def test_missing_token(self, client):
        # Execute request without token
        response = client.get('/api/v1/recommendations/')

        # Verify response
        assert response.status_code == 401

    def test_invalid_token_format(self, client):
        # Execute request with invalid token format
        headers = {'Authorization': 'InvalidFormat token123'}
        response = client.get('/api/v1/recommendations/', headers=headers)

        # Verify response
        assert response.status_code == 401

    @patch('src.interface.decorator.token_decorator.container')
    def test_unauthorized_role(self, mock_container, client):
        # Mock token validaor
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "USER", "user_id": self.directivo_id}
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get('/api/v1/recommendations/', headers=self.auth_header)

        # Verify response
        assert response.status_code == 403

    @patch('src.interface.decorator.token_decorator.container')
    def test_make_recommendation_unauthorized(self, mock_container, client):
        # Mock token validaor
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "USER", "user_id": self.directivo_id}
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.post(
            '/api/v1/recommendations/',
            json=self.recommendation_data,
            headers=self.auth_header,
            content_type='application/json'
        )

        # Verify response
        assert response.status_code == 403
