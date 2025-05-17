import pytest
from unittest.mock import patch
from src.adapters.salesman_adapter import SalesmanAdapter


@pytest.fixture
def salesman_adapter():
    return SalesmanAdapter()


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


def test_get_clients_by_salesman_success(salesman_adapter):
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

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = expected_response
        mock_get.return_value.status_code = 200

        response, status_code = salesman_adapter.get_clients_by_salesman("valid.jwt.token", "salesman123")

        assert status_code == 200
        assert response == expected_response
        mock_get.assert_called_once_with(
            "http://localhost:5106/api/v1/sales/api/v1/salesman/salesman123/clients",
            headers={"Authorization": "Bearer valid.jwt.token"}
        )


def test_get_clients_by_salesman_unauthorized(salesman_adapter):
    error_response = {
        "msg": "Unauthorized"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 401

        response, status_code = salesman_adapter.get_clients_by_salesman("invalid.token", "salesman123")

        assert status_code == 401
        assert response == error_response
        mock_get.assert_called_once()


def test_get_clients_by_salesman_not_found(salesman_adapter):
    error_response = {
        "msg": "Salesman not found"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 404

        response, status_code = salesman_adapter.get_clients_by_salesman("valid.jwt.token", "unknown123")

        assert status_code == 404
        assert response == error_response
        mock_get.assert_called_once()


def test_associate_client_success(salesman_adapter, mock_client_data):
    expected_response = {
        "id": "association123",
        "salesman_id": "salesman123",
        "client_id": "client123"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        mock_post.return_value.status_code = 201

        response, status_code = salesman_adapter.associate_client("valid.jwt.token", "salesman123", mock_client_data)

        assert status_code == 201
        assert response == expected_response
        mock_post.assert_called_once_with(
            "http://localhost:5106/api/v1/sales/api/v1/salesman/salesman123/clients",
            json=mock_client_data,
            headers={"Authorization": "Bearer valid.jwt.token"}
        )


def test_associate_client_unauthorized(salesman_adapter, mock_client_data):
    error_response = {
        "msg": "Unauthorized"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.status_code = 401

        response, status_code = salesman_adapter.associate_client("invalid.token", "salesman123", mock_client_data)

        assert status_code == 401
        assert response == error_response
        mock_post.assert_called_once()


def test_associate_client_invalid_data(salesman_adapter, mock_client_data):
    error_response = {
        "msg": "Invalid client data"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.status_code = 400

        # Modify client data to make it invalid
        invalid_data = mock_client_data.copy()
        invalid_data["client"]["email"] = "invalid-email"

        response, status_code = salesman_adapter.associate_client("valid.jwt.token", "salesman123", invalid_data)

        assert status_code == 400
        assert response == error_response
        mock_post.assert_called_once()