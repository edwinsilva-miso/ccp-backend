import pytest
from unittest.mock import patch
from src.adapters.users_adapter import UsersAdapter


@pytest.fixture
def users_adapter():
    return UsersAdapter()


@pytest.fixture
def mock_user_data():
    return {
        "name": "John Doe",
        "phone": "3153334455",
        "email": "jonhdoe@example.com",
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