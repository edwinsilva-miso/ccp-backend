import pytest
from unittest.mock import patch, Mock
from src.main import create_app
from src.application.errors.errors import UserAlreadyExistsError, UserNotExistsError, ForbiddenError
from src.domain.entities.user_dto import UserDTO

class TestUsersBlueprint:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_register_user_success(self, client):
        # Arrange
        user_data = {
            "name": "John Doe",
            "phone": "3153334455",
            "email": "jonhdoe@example.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        expected_dto = UserDTO(
            id=None,
            name=user_data["name"],
            phone=user_data["phone"],
            email=user_data["email"],
            password=user_data["password"],
            token=None,
            salt=None,
            role=user_data["role"],
            expire_at=None
        )

        with patch('src.interface.blueprints.users_blueprint.CreateUser') as mock_create_user:
            mock_instance = Mock()
            mock_create_user.return_value = mock_instance
            mock_instance.execute.return_value = "new-user-id"

            # Act
            response = client.post('/api/v1/users/', json=user_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 201
            assert "id" in data
            assert data["id"] == "new-user-id"
            mock_instance.execute.assert_called_once()
            actual_dto = mock_instance.execute.call_args[0][0]
            assert isinstance(actual_dto, UserDTO)
            assert actual_dto.name == expected_dto.name
            assert actual_dto.email == expected_dto.email

    def test_register_user_missing_fields(self, client):
        # Arrange
        incomplete_data = {
            "name": "testuser",
            "email": "test@example.com"
        }

        # Act
        response = client.post('/api/v1/users/', json=incomplete_data)
        data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert "msg" in data
        assert "faltan campos requeridos." in data["msg"].lower()

    def test_register_existing_user(self, client):
        # Arrange
        user_data = {
            "name": "JohnDoe",
            "phone": "3153334455",
            "email": "jonhdoe@example.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        with patch('src.interface.blueprints.users_blueprint.CreateUser') as mock_create_user:
            mock_instance = Mock()
            mock_create_user.return_value = mock_instance
            mock_instance.execute.side_effect = UserAlreadyExistsError()

            # Act
            response = client.post('/api/v1/users/', json=user_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 412
            assert "msg" in data
            assert "el registro ya existe" in data["msg"].lower()

    def test_register_user_invalid_email(self, client):
        # Arrange
        invalid_data = {
            "name": "John Doe",
            "phone": "3153334455",
            "email": "jonhdoeexample.com",
            "password": "pass123",
            "role": "CLIENTE"
        }

        # Act
        response = client.post('/api/v1/users/', json=invalid_data)
        data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert "msg" in data
        assert "formato de campo inválido." in data["msg"].lower()

    def test_login_success(self, client):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        with patch('src.interface.blueprints.users_blueprint.LoginUser') as mock_login_user:
            mock_instance = Mock()
            mock_login_user.return_value = mock_instance
            mock_instance.execute.return_value = {
                "id": "test-id",
                "token": "test-token",
                "expiresAt": "2024-03-20T10:00:00"
            }

            # Act
            response = client.post('/api/v1/users/auth', json=login_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 200
            assert "token" in data
            assert "id" in data
            assert data["token"] == "test-token"
            mock_instance.execute.assert_called_once_with(
                login_data["email"],
                login_data["password"]
            )

    def test_login_missing_fields(self, client):
        # Arrange
        incomplete_data = {
            "email": "test@example.com"
        }

        # Act
        response = client.post('/api/v1/users/auth', json=incomplete_data)
        data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert "msg" in data
        assert "faltan campos requeridos." in data["msg"].lower()

    def test_login_invalid_credentials(self, client):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }

        with patch('src.interface.blueprints.users_blueprint.LoginUser') as mock_login_user:
            mock_instance = Mock()
            mock_login_user.return_value = mock_instance
            mock_instance.execute.side_effect = UserNotExistsError()

            # Act
            response = client.post('/api/v1/users/auth', json=login_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 404
            assert "msg" in data
            assert "usuario no existe" in data["msg"].lower()

    @patch('src.interface.blueprints.users_blueprint.UserToken')
    def test_get_user_info_success(self, mock_user_token, client):
        # Arrange
        test_user = {
            "id": "test-id",
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "role": "user"
        }
        mock_instance = Mock()
        mock_user_token.return_value = mock_instance
        mock_instance.execute.return_value = test_user
        headers = {'Authorization': 'Bearer valid-token'}

        # Act
        response = client.get('/api/v1/users/me', headers=headers)

        # Assert
        assert response.status_code == 200
        mock_instance.execute.assert_called_once()

    @patch('src.interface.blueprints.users_blueprint.UserToken')
    def test_get_user_info_forbidden(self, mock_user_token, client):
        # Arrange
        mock_instance = Mock()
        mock_user_token.return_value = mock_instance
        mock_instance.execute.side_effect = ForbiddenError()
        headers = {'Authorization': 'Bearer invalid-token'}

        # Act
        response = client.get('/api/v1/users/me', headers=headers)

        # Assert
        assert response.status_code == 403

    @patch('src.interface.blueprints.users_blueprint.UserToken')
    def test_get_user_info_user_not_exists(self, mock_user_token, client):
        # Arrange
        mock_instance = Mock()
        mock_user_token.return_value = mock_instance
        mock_instance.execute.side_effect = UserNotExistsError()
        headers = {'Authorization': 'Bearer valid-token'}

        # Act
        response = client.get('/api/v1/users/me', headers=headers)

        # Assert
        assert response.status_code == 404