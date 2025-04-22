import json
from unittest.mock import patch, Mock

import pytest
from src.domain.entities.product_dto import ProductDTO
from src.interface.blueprints.products_manufacturer_blueprint import products_manufacturer_blueprint
from src.application.errors.errors import ProductNotExistsError


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(products_manufacturer_blueprint)

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


class TestProductsManufacturerBlueprint:
    def setup_method(self):
        self.manufacturer_id = "test-manufacturer-id"
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Sample products data
        self.sample_products = [
            ProductDTO(
                id="product-1",
                name="Test Product 1",
                brand="Test Brand",
                manufacturer_id=self.manufacturer_id,
                description="Test Description 1",
                details={"weight": "500g", "color": "red"},
                storage_conditions="Room temperature",
                price=100.0,
                currency="USD",
                delivery_time=3,
                images=["image1.jpg", "image2.jpg"]
            ),
            ProductDTO(
                id="product-2",
                name="Test Product 2",
                brand="Test Brand",
                manufacturer_id=self.manufacturer_id,
                description="Test Description 2",
                details={"weight": "300g", "color": "blue"},
                storage_conditions="Refrigerated",
                price=150.0,
                currency="USD",
                delivery_time=5,
                images=["image3.jpg"]
            )
        ]

    @patch('src.interface.blueprints.products_manufacturer_blueprint.GetProductByManufacturer')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_manufacturer_success(self, mock_container, mock_get_product_use_case, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = self.sample_products
        mock_get_product_use_case.return_value = mock_use_case_instance

        # Execute request
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == "product-1"
        assert data[1]['id'] == "product-2"
        assert data[0]['manufacturer_id'] == self.manufacturer_id

        # Verify that the use case was called with correct parameters
        mock_use_case_instance.execute.assert_called_once_with(self.manufacturer_id)

    @patch('src.interface.blueprints.products_manufacturer_blueprint.GetProductByManufacturer')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_manufacturer_product_not_exists(self, mock_container, mock_get_product_use_case, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution raising ProductNotExistsError
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.side_effect = ProductNotExistsError(
            f"No products found for manufacturer ID {self.manufacturer_id}"
        )
        mock_get_product_use_case.return_value = mock_use_case_instance

        # Execute request
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=self.auth_header)

        # Verify response
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "msg" in data
        assert "El producto no existe." in data["msg"]

    @patch('src.interface.blueprints.products_manufacturer_blueprint.GetProductByManufacturer')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_manufacturer_empty_result(self, mock_container, mock_get_product_use_case, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution with empty result
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = []
        mock_get_product_use_case.return_value = mock_use_case_instance

        # Execute request
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_products_manufacturer_missing_token(self, client):
        # Execute request without token
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products')

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Authorization header is missing" in data["error"]

    def test_get_products_manufacturer_invalid_token_format(self, client):
        # Execute request with invalid token format
        headers = {'Authorization': 'InvalidFormat token123'}
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=headers)

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid authorization format" in data["error"]

    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_manufacturer_unauthorized_role(self, mock_container, client):
        # Mock token validation with unauthorized role
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "UNAUTHORIZED_ROLE", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=self.auth_header)

        # Verify response
        assert response.status_code == 403

        data = json.loads(response.data)
        assert "error" in data
        assert "User does not have the required role" in data["error"]

    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_manufacturer_authentication_error(self, mock_container, client):
        # Mock token validation raising AuthenticationError
        from src.domain.exceptions.authentication_error import AuthenticationError

        mock_auth_service = Mock()
        mock_auth_service.validate_token.side_effect = AuthenticationError("Invalid or expired token")
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get(f'/api/v1/manufacturers/{self.manufacturer_id}/products', headers=self.auth_header)

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid or expired token" in data["error"]