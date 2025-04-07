import pytest
from unittest.mock import Mock, patch
from src.application.errors.errors import ForbiddenError, UserNotExistsError
from src.application.user_token import UserToken
from src.domain.entities.user_dto import UserDTO


class TestUserToken:
    @pytest.fixture
    def setup(self):
        self.user_repository = Mock()
        self.user_token = UserToken(self.user_repository)

        # Create a proper mock for role
        role_mock = Mock()
        role_mock.name = "CLIENTE"

        self.test_user = UserDTO(
            id="test-id",
            name="Test User",
            phone="1234567890",
            email="test@example.com",
            password="hashed_password",
            token="valid_token",
            salt="test_salt",
            role=role_mock,  # Use the configured mock
            expire_at=None
        )

    @patch('src.application.user_token.SecurityUtils')
    def test_execute_success(self, mock_security_utils, setup):
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        mock_payload = {"email": "test@example.com"}

        mock_utils_instance = Mock()
        mock_security_utils.return_value = mock_utils_instance
        mock_utils_instance.decode_token.return_value = mock_payload

        self.user_repository.find_by_email.return_value = self.test_user

        # Act
        result = self.user_token.execute(headers)

        # Assert
        assert result["id"] == "test-id"
        assert result["name"] == "Test User"
        assert result["email"] == "test@example.com"
        assert result["phone"] == "1234567890"
        assert result["role"] == "CLIENTE"
        mock_utils_instance.decode_token.assert_called_once_with(headers)
        self.user_repository.find_by_email.assert_called_once_with("test@example.com")

    def test_execute_missing_headers(self, setup):
        # Arrange
        headers = None

        # Act & Assert
        with pytest.raises(ForbiddenError):
            self.user_token.execute(headers)

    @patch('src.application.user_token.SecurityUtils')
    def test_execute_invalid_token(self, mock_security_utils, setup):
        # Arrange
        headers = {"Authorization": "Bearer invalid_token"}
        mock_utils_instance = Mock()
        mock_security_utils.return_value = mock_utils_instance
        mock_utils_instance.decode_token.side_effect = ForbiddenError

        # Act & Assert
        with pytest.raises(ForbiddenError):
            self.user_token.execute(headers)

    @patch('src.application.user_token.SecurityUtils')
    def test_execute_user_not_found(self, mock_security_utils, setup):
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        mock_payload = {"email": "nonexistent@example.com"}

        mock_utils_instance = Mock()
        mock_security_utils.return_value = mock_utils_instance
        mock_utils_instance.decode_token.return_value = mock_payload

        self.user_repository.find_by_email.return_value = None

        # Act & Assert
        with pytest.raises(UserNotExistsError):
            self.user_token.execute(headers)