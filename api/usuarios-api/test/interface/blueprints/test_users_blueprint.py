import pytest
from unittest.mock import patch, Mock
from src.main import create_app
from src.application.errors.errors import UserAlreadyExistsError
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
            salt=None,
            role=user_data["role"]
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