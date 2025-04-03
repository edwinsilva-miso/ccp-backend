import pytest
from unittest.mock import patch, Mock
from src.main import create_app
from src.blueprints.users_blueprint import users_blueprint

class TestUsersBlueprint:
    @pytest.fixture
    def client(self):
        app = create_app()
        # Register the blueprint explicitly for testing
        #app.register_blueprint(users_blueprint, url_prefix='/api/v1')
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

        # Mock the adapter at class level
        with patch('src.blueprints.users_blueprint.UsersAdapter') as MockAdapter:
            # Configure the mock instance
            mock_instance = MockAdapter.return_value
            mock_instance.create_user.return_value = (expected_response, 201)

            response = client.post('/bff/v1/mobile/users/', json=user_data)
            data = response.get_json()

            assert response.status_code == 201
            assert data == expected_response
            mock_instance.create_user.assert_called_once_with(user_data)

    def test_register_user_missing_fields(self, client):
        incomplete_data = {
            "name": "testuser",
            "email": "test@example.com"
        }

        response = client.post('/bff/v1/mobile/users/', json=incomplete_data)
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

            response = client.post('/bff/v1/mobile/users/', json=user_data)
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

            response = client.post('/bff/v1/mobile/users/', json=user_data)
            data = response.get_json()

            assert response.status_code == 412
            assert data == error_response
            mock_instance.create_user.assert_called_once_with(user_data)