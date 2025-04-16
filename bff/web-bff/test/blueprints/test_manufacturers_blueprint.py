import json
from functools import wraps
from unittest.mock import patch

import pytest
from flask import Flask
from src.blueprints.manufacturers_blueprint import manufacturers_blueprint


def mock_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip token validation and pass a mock token
        return f("valid.jwt.token", *args, **kwargs)

    return decorated


@pytest.fixture
def app():
    app = Flask(__name__)
    # Patch the token_required decorator before registering the blueprint
    with patch('src.blueprints.manufacturers_blueprint.token_required', mock_token_required):
        app.register_blueprint(manufacturers_blueprint, url_prefix='/bff/v1/web/manufacturers')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_manufacturer_data():
    return {
        "name": "Fabricante 1",
        "nit": "123456789-7",
        "address": "Cra 1 # 1 - 10",
        "phone": "131225544",
        "email": "myfactory@mail.com",
        "legal_representative": "John Doe",
        "country": "COLOMBIA"
    }


@pytest.fixture
def mock_token():
    return "valid.jwt.token"


def test_get_all_manufacturers_success(client, mock_token):
    # Arrange
    expected_response = [
        {"id": "123", "name": "Fabricante 1", "nit": "123456789-7"},
        {"id": "456", "name": "Fabricante 2", "nit": "987654321-0"}
    ]
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_all_manufacturers.return_value = (expected_response, 200)


        response = client.get('/bff/v1/web/manufacturers/', headers=headers)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_adapter_instance.get_all_manufacturers.assert_called_once_with(mock_token)


def test_get_manufacturer_by_id_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    manufacturer_id = "123"
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_manufacturer_by_id.return_value = (mock_manufacturer_data, 200)

        response = client.get(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == mock_manufacturer_data
        mock_adapter_instance.get_manufacturer_by_id.assert_called_once_with(mock_token, manufacturer_id)


def test_get_manufacturer_by_id_not_found(client, mock_token):
    # Arrange
    manufacturer_id = "nonexistent-id"
    error_response = {"msg": "Manufacturer not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_manufacturer_by_id.return_value = (error_response, 404)

        response = client.get(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.get_manufacturer_by_id.assert_called_once_with(mock_token, manufacturer_id)


def test_get_manufacturer_by_nit_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    nit = "123456789-7"
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_manufacturer_by_nit.return_value = (mock_manufacturer_data, 200)

        response = client.get(f'/bff/v1/web/manufacturers/search?nit={nit}', headers=headers)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == mock_manufacturer_data
        mock_adapter_instance.get_manufacturer_by_nit.assert_called_once_with(mock_token, nit)


def test_get_manufacturer_by_nit_missing_param(client, mock_token):
    # Arrange
    error_response = {'msg': 'NIT parameter is required.'}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.get('/bff/v1/web/manufacturers/search', headers=headers)

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == error_response


def test_get_manufacturer_by_nit_not_found(client, mock_token):
    # Arrange
    nit = "nonexistent-nit"
    error_response = {"msg": "Manufacturer not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.get_manufacturer_by_nit.return_value = (error_response, 404)

        response = client.get(f'/bff/v1/web/manufacturers/search?nit={nit}', headers=headers)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.get_manufacturer_by_nit.assert_called_once_with(mock_token, nit)


def test_create_manufacturer_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    expected_response = {"id": "123"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.create_manufacturer.return_value = (expected_response, 201)

        response = client.post('/bff/v1/web/manufacturers/', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 201
        assert json.loads(response.data) == expected_response
        mock_adapter_instance.create_manufacturer.assert_called_once_with(mock_token, mock_manufacturer_data)


def test_create_manufacturer_missing_fields(client, mock_token):
    # Arrange
    incomplete_data = {"name": "Test Manufacturer"}
    error_response = {'msg': 'Faltan campos requeridos.'}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.post('/bff/v1/web/manufacturers/', headers=headers, json=incomplete_data)

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == error_response


def test_create_manufacturer_no_data(client, mock_token):
    # Arrange
    error_response = {'msg': 'Faltan campos requeridos.'}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.post('/bff/v1/web/manufacturers/', headers=headers, json={})

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == error_response


def test_update_manufacturer_success(client, mock_token, mock_manufacturer_data):
    # Arrange
    manufacturer_id = "123"
    expected_response = {"msg": "Manufacturer updated successfully"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.update_manufacturer.return_value = (expected_response, 200)

        response = client.put(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_adapter_instance.update_manufacturer.assert_called_once_with(mock_token, manufacturer_id,
                                                                          mock_manufacturer_data)


def test_update_manufacturer_no_data(client, mock_token):
    # Arrange
    manufacturer_id = "123"
    error_response = {'msg': 'Datos requeridos.'}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    response = client.put(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers, json={})

    # Assert
    assert response.status_code == 400
    assert json.loads(response.data) == error_response


def test_update_manufacturer_not_found(client, mock_token, mock_manufacturer_data):
    # Arrange
    manufacturer_id = "nonexistent-id"
    error_response = {"msg": "Manufacturer not found"}
    headers = {'Authorization': f'Bearer {mock_token}'}

    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.update_manufacturer.return_value = (error_response, 404)

        response = client.put(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers, json=mock_manufacturer_data)

        # Assert
        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_adapter_instance.update_manufacturer.assert_called_once_with(mock_token, manufacturer_id,
                                                                          mock_manufacturer_data)


def test_delete_manufacturer_success(client, mock_token):
    # Arrange
    manufacturer_id = "123"
    headers = {'Authorization': f'Bearer {mock_token}'}
    # Act
    with patch('src.blueprints.manufacturers_blueprint.ManufacturersAdapter') as MockAdapter:
        mock_adapter_instance = MockAdapter.return_value
        mock_adapter_instance.delete_manufacturer.return_value = ({}, 204)

        response = client.delete(f'/bff/v1/web/manufacturers/{manufacturer_id}', headers=headers)

        # Assert
        assert response.status_code == 204
        mock_adapter_instance.delete_manufacturer.assert_called_once_with(mock_token, manufacturer_id)

