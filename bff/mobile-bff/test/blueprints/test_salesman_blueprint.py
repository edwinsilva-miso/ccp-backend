import json
import pytest
from unittest.mock import patch, MagicMock
from src.blueprints.salesman_blueprint import salesman_blueprint


@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(salesman_blueprint)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_client_data():
    return {
        "client": {
            "id": "client123",
            "name": "Test Client",
            "phone": "1234567890",
            "email": "client@example.com"
        },
        "address": "123 Test Street",
        "city": "Test City",
        "country": "Test Country",
        "storeName": "Test Store"
    }


@pytest.fixture
def mock_invalid_client_data():
    return {
        "client": {
            "id": "client123",
            "name": "Test Client",
            # Missing phone and email fields
        },
        "address": "123 Test Street",
        "city": "Test City",
        "country": "Test Country"
        # Missing storeName field
    }


def test_get_clients_salesman_success(client):
    expected_response = {
        "clients": [
            {
                "id": "client123",
                "name": "Test Client",
                "email": "client@example.com",
                "phone": "1234567890"
            }
        ]
    }

    with patch('src.adapters.salesman_adapter.SalesmanAdapter.get_clients_by_salesman') as mock_get:
        mock_get.return_value = (expected_response, 200)

        response = client.get(
            '/bff/v1/mobile/salesman/salesman123/clients',
            headers={"Authorization": "Bearer valid.jwt.token"}
        )

        assert response.status_code == 200
        assert json.loads(response.data) == expected_response
        mock_get.assert_called_once_with("valid.jwt.token", "salesman123")


def test_get_clients_salesman_unauthorized(client):
    response = client.get('/bff/v1/mobile/salesman/salesman123/clients')
    assert response.status_code == 401
    assert json.loads(response.data) == {"msg": "Unauthorized"}


def test_get_clients_salesman_not_found(client):
    error_response = {"msg": "Salesman not found"}

    with patch('src.adapters.salesman_adapter.SalesmanAdapter.get_clients_by_salesman') as mock_get:
        mock_get.return_value = (error_response, 404)

        response = client.get(
            '/bff/v1/mobile/salesman/unknown123/clients',
            headers={"Authorization": "Bearer valid.jwt.token"}
        )

        assert response.status_code == 404
        assert json.loads(response.data) == error_response
        mock_get.assert_called_once_with("valid.jwt.token", "unknown123")


def test_associate_client_salesman_success(client, mock_client_data):
    expected_response = {
        "id": "association123",
        "salesman_id": "salesman123",
        "client_id": "client123"
    }

    with patch('src.adapters.salesman_adapter.SalesmanAdapter.associate_client') as mock_associate:
        mock_associate.return_value = (expected_response, 201)

        response = client.post(
            '/bff/v1/mobile/salesman/salesman123/clients',
            headers={"Authorization": "Bearer valid.jwt.token"},
            json=mock_client_data
        )

        assert response.status_code == 201
        assert json.loads(response.data) == expected_response
        mock_associate.assert_called_once_with("valid.jwt.token", "salesman123", mock_client_data)


def test_associate_client_salesman_unauthorized(client, mock_client_data):
    response = client.post(
        '/bff/v1/mobile/salesman/salesman123/clients',
        json=mock_client_data
    )

    assert response.status_code == 401
    assert json.loads(response.data) == {"msg": "Unauthorized"}


def test_associate_client_salesman_missing_fields(client, mock_invalid_client_data):
    response = client.post(
        '/bff/v1/mobile/salesman/salesman123/clients',
        headers={"Authorization": "Bearer valid.jwt.token"},
        json=mock_invalid_client_data
    )

    assert response.status_code == 400
    assert json.loads(response.data) == {"msg": "Faltan campos requeridos."}


def test_associate_client_salesman_bad_request(client, mock_client_data):
    error_response = {"msg": "Invalid client data"}

    with patch('src.adapters.salesman_adapter.SalesmanAdapter.associate_client') as mock_associate:
        mock_associate.return_value = (error_response, 400)

        response = client.post(
            '/bff/v1/mobile/salesman/salesman123/clients',
            headers={"Authorization": "Bearer valid.jwt.token"},
            json=mock_client_data
        )

        assert response.status_code == 400
        assert json.loads(response.data) == error_response
        mock_associate.assert_called_once_with("valid.jwt.token", "salesman123", mock_client_data)


def test_associate_client_empty_payload(client):
    response = client.post(
        '/bff/v1/mobile/salesman/salesman123/clients',
        headers={"Authorization": "Bearer valid.jwt.token"},
        json={}
    )

    assert response.status_code == 400
    assert json.loads(response.data) == {"msg": "Faltan campos requeridos."}