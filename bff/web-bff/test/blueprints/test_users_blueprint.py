from unittest.mock import patch

import pytest
from src.blueprints.users_blueprint import users_blueprint
from src.main import create_app


class TestUsersBlueprint:
    @pytest.fixture
    def client(self):
        app = create_app()
        # Register the blueprint explicitly for testing
        # app.register_blueprint(users_blueprint, url_prefix='/api/v1')
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_register_user_success(self, client):
        user_data = {
            "name": "John Doe",
            "phone": "3153334455",
            "email": "johndoe@example.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        expected_response = {
            "id": "new-user-id"
        }

        # Mock the adapters at class level
        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            # Configure the mock instance
            mock_instance = MockAdapter.return_value
            mock_instance.create_user.return_value = (expected_response, 201)

            response = client.post('/bff/v1/web/users/', json=user_data)
            data = response.get_json()

            assert response.status_code == 201
            assert data == expected_response
            mock_instance.create_user.assert_called_once_with(user_data)

    def test_register_user_missing_fields(self, client):
        incomplete_data = {
            "name": "testuser",
            "email": "test@example.com"
        }

        response = client.post('/bff/v1/web/users/', json=incomplete_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "msg" in data
        assert "faltan campos requeridos." in data["msg"].lower()

    def test_register_user_api_error(self, client):
        user_data = {
            "name": "John Doe",
            "phone": "3153334455",
            "email": "johndoe@example.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        error_response = {
            "error": "Internal server error"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.create_user.return_value = (error_response, 500)

            response = client.post('/bff/v1/web/users/', json=user_data)
            data = response.get_json()

            assert response.status_code == 500
            assert data == error_response
            mock_instance.create_user.assert_called_once_with(user_data)

    def test_register_user_duplicate_email(self, client):
        user_data = {
            "name": "John Doe",
            "phone": "3153334455",
            "email": "johndoe@example.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        error_response = {
            "msg": "User already exists"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.create_user.return_value = (error_response, 412)

            response = client.post('/bff/v1/web/users/', json=user_data)
            data = response.get_json()

            assert response.status_code == 412
            assert data == error_response
            mock_instance.create_user.assert_called_once_with(user_data)

    def test_authorize_user_success(self, client):
        auth_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        expected_response = {
            "token": "valid.jwt.token",
            "expireAt": "2024-03-20T00:00:00"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.authorize.return_value = (expected_response, 200)

            response = client.post('/bff/v1/web/users/auth', json=auth_data)
            data = response.get_json()

            assert response.status_code == 200
            assert data == expected_response
            mock_instance.authorize.assert_called_once_with(
                auth_data['email'],
                auth_data['password']
            )

    def test_authorize_user_missing_fields(self, client):
        incomplete_data = {
            "email": "test@example.com"
        }

        response = client.post('/bff/v1/web/users/auth', json=incomplete_data)
        data = response.get_json()

        assert response.status_code == 400
        assert "msg" in data
        assert "faltan campos requeridos." in data["msg"].lower()

    def test_authorize_user_invalid_credentials(self, client):
        auth_data = {
            "email": "wrong@example.com",
            "password": "wrongpass"
        }

        error_response = {
            "msg": "Invalid credentials"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.authorize.return_value = (error_response, 401)

            response = client.post('/bff/v1/web/users/auth', json=auth_data)
            data = response.get_json()

            assert response.status_code == 401
            assert data == error_response
            mock_instance.authorize.assert_called_once_with(
                auth_data['email'],
                auth_data['password']
            )

    def test_get_user_info_success(self, client):
        expected_response = {
            "id": "user-id",
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "role": "CLIENTE"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.get_user_info.return_value = (expected_response, 200)

            response = client.get(
                '/bff/v1/web/users/me',
                headers={"Authorization": "Bearer valid.jwt.token"}
            )
            data = response.get_json()

            assert response.status_code == 200
            assert data == expected_response
            mock_instance.get_user_info.assert_called_once_with(
                "Bearer valid.jwt.token"
            )

    def test_get_user_info_missing_token(self, client):
        response = client.get('/bff/v1/web/users/me')
        data = response.get_json()

        assert response.status_code == 401
        assert "msg" in data
        assert "unauthorized" in data["msg"].lower()

    def test_get_user_info_invalid_token(self, client):
        error_response = {
            "msg": "Invalid token"
        }

        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            mock_instance = MockAdapter.return_value
            mock_instance.get_user_info.return_value = (error_response, 401)

            response = client.get(
                '/bff/v1/web/users/me',
                headers={"Authorization": "Bearer invalid.token"}
            )
            data = response.get_json()

            assert response.status_code == 401
            assert data == error_response
            mock_instance.get_user_info.assert_called_once_with(
                "Bearer invalid.token"
            )
