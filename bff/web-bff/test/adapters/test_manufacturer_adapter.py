import pytest
from unittest.mock import patch, Mock
from src.adapters.manufacturers_adapter import ManufacturersAdapter

@pytest.fixture
def manufacturer_adapter():
    return ManufacturersAdapter()

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

def test_create_manufacturer_success(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    expected_response = {
        "id": "123"
    }
    jwt = "valid.jwt.token"

    # Act
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        mock_post.return_value.status_code = 201

        response, status_code = manufacturer_adapter.create_manufacturer(jwt, mock_manufacturer_data)

        assert status_code == 201
        assert response == expected_response
        mock_post.assert_called_once()

def test_get_all_manufacturers_success(manufacturer_adapter):
    # Arrange
    expected_response = [
        {"id": "123", "name": "Fabricante 1", "nit": "123456789-7"},
        {"id": "456", "name": "Fabricante 2", "nit": "987654321-0"}
    ]
    jwt = "valid.jwt.token"

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = expected_response
        mock_get.return_value.status_code = 200

        response, status_code = manufacturer_adapter.get_all_manufacturers(jwt)

        # Assert
        assert status_code == 200
        assert response == expected_response
        mock_get.assert_called_once()


def test_get_manufacturer_by_id_success(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    jwt = "valid.jwt.token"
    manufacturer_id = "123"

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_manufacturer_data
        mock_get.return_value.status_code = 200

        response, status_code = manufacturer_adapter.get_manufacturer_by_id(jwt, manufacturer_id)

        # Assert
        assert status_code == 200
        assert response == mock_manufacturer_data
        mock_get.assert_called_once()


def test_get_manufacturer_by_id_not_found(manufacturer_adapter):
    # Arrange
    error_response = {"msg": "Manufacturer not found"}
    jwt = "valid.jwt.token"
    manufacturer_id = "nonexistent-id"

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 404

        response, status_code = manufacturer_adapter.get_manufacturer_by_id(jwt, manufacturer_id)

        # Assert
        assert status_code == 404
        assert response == error_response
        mock_get.assert_called_once()


def test_get_manufacturer_by_nit_success(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    jwt = "valid.jwt.token"
    nit = "123456789-7"

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_manufacturer_data
        mock_get.return_value.status_code = 200

        response, status_code = manufacturer_adapter.get_manufacturer_by_nit(jwt, nit)

        # Assert
        assert status_code == 200
        assert response == mock_manufacturer_data
        mock_get.assert_called_once()


def test_get_manufacturer_by_nit_not_found(manufacturer_adapter):
    # Arrange
    error_response = {"msg": "Manufacturer not found"}
    jwt = "valid.jwt.token"
    nit = "nonexistent-nit"

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 404

        response, status_code = manufacturer_adapter.get_manufacturer_by_nit(jwt, nit)

        # Assert
        assert status_code == 404
        assert response == error_response
        mock_get.assert_called_once()


def test_create_manufacturer_failure(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    error_response = {"msg": "Invalid manufacturer data"}
    jwt = "valid.jwt.token"

    # Act
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.status_code = 400

        response, status_code = manufacturer_adapter.create_manufacturer(jwt, mock_manufacturer_data)

        # Assert
        assert status_code == 400
        assert response == error_response
        mock_post.assert_called_once()


def test_update_manufacturer_success(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    expected_response = {"msg": "Manufacturer updated successfully"}
    jwt = "valid.jwt.token"
    manufacturer_id = "123"

    # Act
    with patch('requests.put') as mock_put:
        mock_put.return_value.json.return_value = expected_response
        mock_put.return_value.status_code = 200

        response, status_code = manufacturer_adapter.update_manufacturer(jwt, manufacturer_id, mock_manufacturer_data)

        # Assert
        assert status_code == 200
        assert response == expected_response
        mock_put.assert_called_once()


def test_update_manufacturer_not_found(manufacturer_adapter, mock_manufacturer_data):
    # Arrange
    error_response = {"msg": "Manufacturer not found"}
    jwt = "valid.jwt.token"
    manufacturer_id = "nonexistent-id"

    # Act
    with patch('requests.put') as mock_put:
        mock_put.return_value.json.return_value = error_response
        mock_put.return_value.status_code = 404

        response, status_code = manufacturer_adapter.update_manufacturer(jwt, manufacturer_id, mock_manufacturer_data)

        # Assert
        assert status_code == 404
        assert response == error_response
        mock_put.assert_called_once()


def test_delete_manufacturer_success(manufacturer_adapter):
    # Arrange
    expected_response = {"msg": "Manufacturer deleted successfully"}
    jwt = "valid.jwt.token"
    manufacturer_id = "123"

    # Act
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.json.return_value = expected_response
        mock_delete.return_value.status_code = 200

        response, status_code = manufacturer_adapter.delete_manufacturer(jwt, manufacturer_id)

        # Assert
        assert status_code == 200
        assert response == expected_response
        mock_delete.assert_called_once()


def test_delete_manufacturer_204_response(manufacturer_adapter):
    # Arrange
    jwt = "valid.jwt.token"
    manufacturer_id = "123"

    # Act
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.status_code = 204

        response, status_code = manufacturer_adapter.delete_manufacturer(jwt, manufacturer_id)

        # Assert
        assert status_code == 204
        assert response == {}
        mock_delete.assert_called_once()


def test_delete_manufacturer_not_found(manufacturer_adapter):
    # Arrange
    error_response = {"msg": "Manufacturer not found"}
    jwt = "valid.jwt.token"
    manufacturer_id = "nonexistent-id"

    # Act
    with patch('requests.delete') as mock_delete:
        mock_delete.return_value.json.return_value = error_response
        mock_delete.return_value.status_code = 404

        response, status_code = manufacturer_adapter.delete_manufacturer(jwt, manufacturer_id)

        # Assert
        assert status_code == 404
        assert response == error_response
        mock_delete.assert_called_once()