import unittest
from unittest.mock import Mock

import pytest
from src.application.create_user import CreateUser
from src.application.errors.errors import UserAlreadyExistsError, InvalidFormatError
from src.domain.entities.user_dto import UserDTO
from src.infrastructure.adapters.user_adapter import UserAdapter


class TestCreateUser:
    @pytest.fixture
    def user_adapter_mock(self):
        return Mock(spec=UserAdapter)

    @pytest.fixture
    def create_user_service(self, user_adapter_mock):
        return CreateUser(user_adapter_mock)

    def test_create_user_successfully(self, create_user_service, user_adapter_mock):
        # Arrange
        user_data = UserDTO(
            id="existing-id",
            name="existinguser",
            phone="3153334455",
            email="mail@example.com",
            password="hashedpass",
            salt=None,
            role="CLIENTE"
        )
        user_adapter_mock.find_by_email.return_value = None
        user_adapter_mock.add.return_value = "new-user-id"

        # Act
        result = create_user_service.execute(user_data)

        # Assert
        assert result == "new-user-id"
        user_adapter_mock.find_by_email.assert_called_once_with(user_data.email)
        user_adapter_mock.add.assert_called_once()

    def test_create_user_with_existing_email(self, create_user_service, user_adapter_mock):
        # Arrange
        user_data = UserDTO(
            id=None,
            name="John Doe 2",
            phone="3153334455",
            email="existing@example.com",
            password="pass123",
            salt=None,
            role="CLIENTE"
        )
        user_adapter_mock.find_by_email.return_value = UserDTO(
            id="existing-id",
            name="existinguser",
            phone="3153334455",
            email="existing@example.com",
            password="hashedpass",
            salt="salt",
            role="CLIENTE"
        )

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            create_user_service.execute(user_data)

        user_adapter_mock.find_by_email.assert_called_once_with(user_data.email)
        user_adapter_mock.add.assert_not_called()

    def test_create_user_with_invalid_email(self, create_user_service, user_adapter_mock):
        # Arrange
        user_data = UserDTO(
            id=None,
            name="John Doe 2",
            phone="3153334455",
            email="existingexample.com",
            password="pass123",
            salt=None,
            role="CLIENTE"
        )


        # Act & Assert
        with pytest.raises(InvalidFormatError) as exc_info:
            create_user_service.execute(user_data)

        user_adapter_mock.find_by_email.assert_not_called()
        user_adapter_mock.add.assert_not_called()

    def test_create_user_with_invalid_password(self, create_user_service, user_adapter_mock):
        # Arrange
        user_data = UserDTO(
            id=None,
            name="John Doe 2",
            phone="3153334455",
            email="mail1@other.com",
            password="$%&",
            salt=None,
            role="CLIENTE"
        )


        # Act & Assert
        with pytest.raises(InvalidFormatError) as exc_info:
            create_user_service.execute(user_data)

        user_adapter_mock.find_by_email.assert_not_called()
        user_adapter_mock.add.assert_not_called()

if __name__ == "__main__":
    pytest.main()
