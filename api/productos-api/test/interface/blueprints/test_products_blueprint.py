import json
import uuid
from unittest.mock import patch, Mock

import pytest
from src.application.errors.errors import ProductNotExistsError, InvalidFormatError
from src.domain.entities.product_dto import ProductDTO
from src.interface.blueprints.products_blueprint import products_blueprint


@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(products_blueprint)

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


class TestProductsBlueprint:
    def setup_method(self):
        self.product_id = uuid.uuid4()  # Use UUID object, not string
        self.product_id_2 = uuid.uuid4()  # Use UUID object, not string
        self.valid_token = "valid_jwt_token"
        self.auth_header = {'Authorization': f'Bearer {self.valid_token}'}

        # Sample product data
        self.sample_product = ProductDTO(
            id=self.product_id,
            name="Test Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Test Description",
            details={"weight": "500g", "color": "red"},
            storage_conditions="Room temperature",
            price=100.0,
            currency="USD",
            delivery_time=3,
            images=["image1.jpg", "image2.jpg"]
        )

        # Sample product list for get_all endpoint
        self.sample_products = [
            self.sample_product,
            ProductDTO(
                id=self.product_id_2,
                name="Test Product 2",
                brand="Test Brand",
                manufacturer_id="test-manufacturer-id",
                description="Test Description 2",
                details={"weight": "300g", "color": "blue"},
                storage_conditions="Refrigerated",
                price=150.0,
                currency="USD",
                delivery_time=5,
                images=["image3.jpg"]
            )
        ]

    # GET ALL PRODUCTS TESTS
    @patch('src.interface.blueprints.products_blueprint.GetAllProducts')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_success(self, mock_container, mock_get_products, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = self.sample_products
        mock_get_products.return_value = mock_use_case_instance

        # Execute request
        response = client.get('/api/v1/products/', headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['id'] == str(self.product_id)
        assert data[1]['id'] == str(self.product_id_2)

        # Verify that the use case was called
        mock_use_case_instance.execute.assert_called_once()

    @patch('src.interface.blueprints.products_blueprint.GetAllProducts')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_products_empty_result(self, mock_container, mock_get_products, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution with empty result
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = []
        mock_get_products.return_value = mock_use_case_instance

        # Execute request
        response = client.get('/api/v1/products/', headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    # GET PRODUCT BY ID TESTS
    @patch('src.interface.blueprints.products_blueprint.GetProductById')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_product_by_id_success(self, mock_container, mock_get_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        # Important: Make the mock handle the conversion between UUID and str
        mock_use_case_instance.execute.return_value = self.sample_product
        mock_get_product.return_value = mock_use_case_instance

        # Execute request with string UUID in URL (as it would be in a real HTTP request)
        response = client.get(f'/api/v1/products/{str(self.product_id)}', headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == str(self.product_id)
        assert data['name'] == "Test Product"
        assert data['price'] == 100.0

        # Verify mock was called with string UUID (as the endpoint would receive it)
        mock_use_case_instance.execute.assert_called_once_with(str(self.product_id))

    @patch('src.interface.blueprints.products_blueprint.GetProductById')
    @patch('src.interface.decorator.token_decorator.container')
    def test_get_product_by_id_not_found(self, mock_container, mock_get_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution raising ProductNotExistsError
        mock_use_case_instance = Mock()

        # Use string representation of UUID for the error message
        product_id_str = str(self.product_id)
        mock_use_case_instance.execute.side_effect = ProductNotExistsError(
            f"Product with ID {product_id_str} not found"
        )
        mock_get_product.return_value = mock_use_case_instance

        # Execute request with string UUID
        response = client.get(f'/api/v1/products/{product_id_str}', headers=self.auth_header)

        # Verify response
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "msg" in data
        assert "El producto no existe." in data["msg"]

        # Verify that execute was called with the string UUID
        mock_use_case_instance.execute.assert_called_once_with(product_id_str)

    # CREATE PRODUCT TESTS
    @patch('src.interface.blueprints.products_blueprint.CreateProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_create_product_success(self, mock_container, mock_create_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = self.product_id
        mock_create_product.return_value = mock_use_case_instance

        # Prepare product data for request
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "manufacturerId": "test-manufacturer-id",
            "description": "Test Description",
            "details": {"weight": "500g", "color": "red"},
            "storageConditions": "Room temperature",
            "price": 100.0,
            "currency": "USD",
            "deliveryTime": 3,
            "images": ["image1.jpg", "image2.jpg"]
        }

        # Execute request
        response = client.post('/api/v1/products/',
                               json=product_data,
                               headers=self.auth_header)

        # Verify response
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['id'] == str(self.product_id)

        # Verify that the use case was called
        mock_use_case_instance.execute.assert_called_once()

    @patch('src.interface.blueprints.products_blueprint.CreateProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_create_product_invalid_format(self, mock_container, mock_create_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution raising InvalidFormatError
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.side_effect = InvalidFormatError("Invalid price format")
        mock_create_product.return_value = mock_use_case_instance

        # Prepare invalid product data
        invalid_product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "manufacturerId": "test-manufacturer-id",
            "description": "Test Description",
            "details": {"weight": "500g", "color": "red"},
            "storageConditions": "Room temperature",
            "price": -100.0,  # Invalid negative price
            "currency": "USD",
            "deliveryTime": 3,
            "images": ["image1.jpg", "image2.jpg"]
        }

        # Execute request
        response = client.post('/api/v1/products/',
                               json=invalid_product_data,
                               headers=self.auth_header)

        # Verify response
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "msg" in data
        assert "Formato de campo inválido." in data["msg"]

    # UPDATE PRODUCT TESTS
    @patch('src.interface.blueprints.products_blueprint.UpdateProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_update_product_success(self, mock_container, mock_update_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        # Create an updated product version
        updated_product = ProductDTO(
            id=self.product_id,
            name="Updated Product",
            brand="Test Brand",
            manufacturer_id="test-manufacturer-id",
            description="Updated Description",
            details={"weight": "600g", "color": "green"},
            storage_conditions="Room temperature",
            price=120.0,
            currency="USD",
            delivery_time=4,
            images=["image1.jpg", "image2.jpg"]
        )
        mock_use_case_instance.execute.return_value = updated_product
        mock_update_product.return_value = mock_use_case_instance

        # Prepare update data
        update_data = {
            "name": "Updated Product",
            "brand": "Test Brand",
            "manufacturerId": "test-manufacturer-id",
            "description": "Updated Description",
            "details": {"weight": "600g", "color": "green"},
            "storageConditions": "Room temperature",
            "price": 120.0,  # Invalid negative price
            "currency": "USD",
            "deliveryTime": 4,
            "images": ["image1.jpg", "image2.jpg"]
        }

        # Execute request
        response = client.put(f'/api/v1/products/{self.product_id}',
                              json=update_data,
                              headers=self.auth_header)

        # Verify response
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == str(self.product_id)
        assert data['name'] == "Updated Product"
        assert data['description'] == "Updated Description"
        assert data['price'] == 120.0

        # Verify that the use case was called with correct parameters
        mock_use_case_instance.execute.assert_called_once()

    @patch('src.interface.blueprints.products_blueprint.UpdateProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_update_product_not_found(self, mock_container, mock_update_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution raising ProductNotExistsError
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.side_effect = ProductNotExistsError(
            f"Product with ID {self.product_id} not found"
        )
        mock_update_product.return_value = mock_use_case_instance

        # Prepare update data
        update_data = {
            "name": "Updated Product",
            "brand": "Test Brand",
            "manufacturerId": "test-manufacturer-id",
            "description": "Updated Description",
            "details": {"weight": "600g", "color": "green"},
            "storageConditions": "Room temperature",
            "price": 120.0,  # Invalid negative price
            "currency": "USD",
            "deliveryTime": 4,
            "images": ["image1.jpg", "image2.jpg"]
        }

        # Execute request
        response = client.put(f'/api/v1/products/{self.product_id}',
                              json=update_data,
                              headers=self.auth_header)

        # Verify response
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "msg" in data
        assert "El producto no existe." in data["msg"]

    # DELETE PRODUCT TESTS
    @patch('src.interface.blueprints.products_blueprint.DeleteProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_delete_product_success(self, mock_container, mock_delete_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.return_value = True
        mock_delete_product.return_value = mock_use_case_instance

        # Execute request
        response = client.delete(f'/api/v1/products/{self.product_id}', headers=self.auth_header)

        # Verify response
        assert response.status_code == 204
        assert response.data == b''  # No content returned

        # Verify that the use case was called with correct parameters
        mock_use_case_instance.execute.assert_called_once_with(str(self.product_id))

    @patch('src.interface.blueprints.products_blueprint.DeleteProduct')
    @patch('src.interface.decorator.token_decorator.container')
    def test_delete_product_not_found(self, mock_container, mock_delete_product, client):
        # Mock token validation
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "DIRECTIVO", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Mock use case execution raising ProductNotExistsError
        mock_use_case_instance = Mock()
        mock_use_case_instance.execute.side_effect = ProductNotExistsError(
            f"Product with ID {self.product_id} not found"
        )
        mock_delete_product.return_value = mock_use_case_instance

        # Execute request
        response = client.delete(f'/api/v1/products/{self.product_id}', headers=self.auth_header)

        # Verify response
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "msg" in data
        assert "El producto no existe." in data["msg"]

    # AUTHENTICATION TESTS
    def test_products_missing_token(self, client):
        # Execute request without token
        response = client.get('/api/v1/products/')

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Authorization header is missing" in data["error"]

    def test_products_invalid_token_format(self, client):
        # Execute request with invalid token format
        headers = {'Authorization': 'InvalidFormat token123'}
        response = client.get('/api/v1/products/', headers=headers)

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid authorization format" in data["error"]

    @patch('src.interface.decorator.token_decorator.container')
    def test_products_unauthorized_role(self, mock_container, client):
        # Mock token validation with unauthorized role
        mock_auth_service = Mock()
        mock_auth_service.validate_token.return_value = {"role": "UNAUTHORIZED_ROLE", "user_id": "test-user"}
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get('/api/v1/products/', headers=self.auth_header)

        # Verify response
        assert response.status_code == 403

        data = json.loads(response.data)
        assert "error" in data
        assert "User does not have the required role" in data["error"]

    @patch('src.interface.decorator.token_decorator.container')
    def test_products_authentication_error(self, mock_container, client):
        # Mock token validation raising AuthenticationError
        from src.domain.exceptions.authentication_error import AuthenticationError

        mock_auth_service = Mock()
        mock_auth_service.validate_token.side_effect = AuthenticationError("Invalid or expired token")
        mock_container.token_validator = mock_auth_service

        # Execute request
        response = client.get('/api/v1/products/', headers=self.auth_header)

        # Verify response
        assert response.status_code == 401

        data = json.loads(response.data)
        assert "error" in data
        assert "Invalid or expired token" in data["error"]
