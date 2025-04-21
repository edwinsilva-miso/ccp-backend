import json
from functools import wraps
from unittest.mock import patch

import pytest
from flask import Flask
from src.blueprints.products_blueprint import products_blueprint


def mock_token_required(f):
    """
    Mock decorator to bypass token validation for testing purposes.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip token validation and pass a mock token
        return f("valid.jwt.token", *args, **kwargs)

    return decorated


@pytest.fixture
def app():
    app = Flask(__name__)
    # Patch the token_required decorator before registering the blueprint
    with patch('src.blueprints.products_blueprint.token_required', mock_token_required):
        app.register_blueprint(products_blueprint, url_prefix='/bff/v1/web/products')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_manufacturer_data():
    return {
        "name": "Test Product",
        "brand": "Test Brand",
        "manufacturerId": "manufacturer_test",
        "description": "Test Description",
        "details": {"color": "gray", "size": "9.5"},
        "storageConditions": "Clean site",
        "price": 199.99,
        "currency": "USD",
        "deliveryTime": 5,
        "images": ["image1.png", "image2.png"]
    }


@pytest.fixture
def mock_token():
    return "valid.jwt.token"


def test_get_all_products_success(client, mock_token):
    # Arrange
    expected_products = [
        {"id": "abc123", "name": "Product 1", "price": 99.99},
        {"id": "def456", "name": "Product 2", "price": 149.99}
    ]

    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_all_products.return_value = (expected_products, 200)

        response = client.get('/bff/v1/web/products/', headers=headers)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_products
        mock_adapter_instance.get_all_products.assert_called_once_with(mock_token)


def test_get_all_products_unauthorized(client):
    # Act
    response = client.get('/bff/v1/web/products/')

    # Assert
    assert response.status_code == 401
    assert json.loads(response.data) == {'msg': 'Unauthorized'}


def test_get_product_by_id_success(client, mock_token):
    # Arrange
    product_id = "abc123"
    expected_product = {
        "id": "abc123",
        "name": "Test Product",
        "brand": "Test Brand",
        "manufacturerId": "manufacturer_test",
        "description": "Test Description",
        "price": 199.99
    }
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_product_by_id.return_value = (expected_product, 200)

        response = client.get(f'/bff/v1/web/products/{product_id}', headers=headers)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_product
        mock_adapter_instance.get_product_by_id.assert_called_once_with(mock_token, product_id)


def test_get_product_by_id_not_found(client, mock_token):
    # Arrange
    product_id = "nonexistent-id"
    error_response = {"msg": "Product not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_product_by_id.return_value = (error_response, 404)

        response = client.get(f'/bff/v1/web/products/{product_id}', headers=headers)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.get_product_by_id.assert_called_once_with(mock_token, product_id)


def test_create_product_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    expected_response = {"id": "abc123", "msg": "Product created successfully"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.create_product.return_value = (expected_response, 201)

        response = client.post('/bff/v1/web/products/', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 201
        assert json.loads(response.data) == expected_response
        mock_adapter_instance.create_product.assert_called_once_with(mock_token, mock_manufacturer_data)


def test_create_product_missing_fields(client, mock_token):
    # Arrange
    invalid_data = {"name": "Invalid Product"}  # Missing required fields
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.post('/bff/v1/web/products/', headers=headers, json=invalid_data)

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == {'msg': 'Missing required fields.'}


def test_update_product_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    product_id = "abc123"
    expected_response = {"msg": "Product updated successfully"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.update_product.return_value = (expected_response, 200)

        response = client.put(f'/bff/v1/web/products/{product_id}', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_adapter_instance.update_product.assert_called_once_with(mock_token, product_id, mock_manufacturer_data)


def test_update_product_missing_fields(client, mock_token):
    # Arrange
    product_id = "abc123"
    invalid_data = {"name": "Invalid Product"}  # Missing required fields
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.put(f'/bff/v1/web/products/{product_id}', headers=headers, json=invalid_data)

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == {'msg': 'Missing required fields.'}


def test_update_product_not_found(client, mock_token, mock_manufacturer_data):
    # Arrange
    product_id = "nonexistent-id"
    error_response = {"msg": "Product not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.update_product.return_value = (error_response, 404)

        response = client.put(f'/bff/v1/web/products/{product_id}', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.update_product.assert_called_once_with(mock_token, product_id, mock_manufacturer_data)


def test_delete_product_success(client, mock_token):
    # Arrange
    product_id = "abc123"
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.delete_product.return_value = ({}, 204)

        response = client.delete(f'/bff/v1/web/products/{product_id}', headers=headers)

        # Assert
        assert response.status_code == 204
        mock_adapter_instance.delete_product.assert_called_once_with(mock_token, product_id)


def test_delete_product_not_found(client, mock_token):
    # Arrange
    product_id = "nonexistent-id"
    error_response = {"msg": "Product not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.products_blueprint.ProductsAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.delete_product.return_value = (error_response, 404)

        response = client.delete(f'/bff/v1/web/products/{product_id}', headers=headers)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.delete_product.assert_called_once_with(mock_token, product_id)
