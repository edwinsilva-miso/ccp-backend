import pytest
from unittest.mock import patch, Mock
from src.adapters.users_adapter import UsersAdapter


@pytest.fixture
def users_adapter():
    return UsersAdapter()


@pytest.fixture
def mock_user_data():
    return {
        "name": "John Doe",
        "phone": "3153334455",
        "email": "johndoe@example.com",
        "password": "pass123",
        "role": "CLIENTE"
    }


def test_create_user_success(users_adapter, mock_user_data):
    expected_response = {
        "id": "123"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        mock_post.return_value.status_code = 201

        response, status_code = users_adapter.create_user(mock_user_data)

        assert status_code == 201
        assert response == expected_response
        mock_post.assert_called_once()


def test_create_user_failure(users_adapter, mock_user_data):
    error_response = {
        "msg": "Invalid user data"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.status_code = 400

        response, status_code = users_adapter.create_user(mock_user_data)

        assert status_code == 400
        assert response == error_response
        mock_post.assert_called_once()


def test_authorize_success(users_adapter):
    expected_response = {
        "token": "valid.jwt.token",
        "expireAt": "2024-03-20T00:00:00"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = expected_response
        mock_post.return_value.status_code = 200

        response, status_code = users_adapter.authorize("test@example.com", "test123")

        assert status_code == 200
        assert response == expected_response
        mock_post.assert_called_once_with(
            "http://localhost:5100/api/v1/users/auth",
            json={"email": "test@example.com", "password": "test123"}
        )


def test_authorize_invalid_credentials(users_adapter):
    error_response = {
        "msg": "Invalid credentials"
    }

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = error_response
        mock_post.return_value.status_code = 401

        response, status_code = users_adapter.authorize("wrong@example.com", "wrong123")

        assert status_code == 401
        assert response == error_response
        mock_post.assert_called_once()


def test_get_user_info_success(users_adapter):
    expected_response = {
        "id": "user-id",
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "role": "CLIENTE"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = expected_response
        mock_get.return_value.status_code = 200

        response, status_code = users_adapter.get_user_info("Bearer valid.jwt.token")

        assert status_code == 200
        assert response == expected_response
        mock_get.assert_called_once_with(
            "http://localhost:5100/api/v1/users/me",
            headers={"Authorization": "Bearer valid.jwt.token"}
        )


def test_get_user_info_invalid_token(users_adapter):
    error_response = {
        "msg": "Invalid token"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 401

        response, status_code = users_adapter.get_user_info("Bearer invalid.token")

        assert status_code == 401
        assert response == error_response
        mock_get.assert_called_once()


def test_get_user_info_user_not_found(users_adapter):
    error_response = {
        "msg": "User not found"
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = error_response
        mock_get.return_value.status_code = 404

        response, status_code = users_adapter.get_user_info("Bearer valid.jwt.token")

        assert status_code == 404
        assert response == error_response
        mock_get.assert_called_once()
