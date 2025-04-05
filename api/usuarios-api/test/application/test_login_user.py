import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.application.errors.errors import UserNotExistsError
from src.application.login_user import LoginUser
from src.domain.entities.user_dto import UserDTO


class TestLoginUser(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock()
        self.login_user = LoginUser(self.user_repository)
        self.test_user = UserDTO(
            id="test-id",
            name="Test User",
            phone="1234567890",
            email="test@example.com",
            password="hashed_password",
            token=None,
            salt="test_salt",
            role="user",
            expire_at=None
        )

    def test_successful_login(self):
        # Arrange
        self.user_repository.find_by_email.return_value = self.test_user
        self.test_user.check_password = Mock(return_value=True)
        expected_token = "test_token"
        expected_expire = datetime.now() + timedelta(hours=1)
        self.test_user.generate_token = Mock()
        self.test_user.token = expected_token
        self.test_user.expired_at = expected_expire

        # Act
        result = self.login_user.execute("test@example.com", "correct_password")

        # Assert
        self.assertEqual(result["id"], "test-id")
        self.assertEqual(result["token"], expected_token)
        self.assertEqual(result["expiresAt"], expected_expire)
        self.user_repository.update.assert_called_once_with(self.test_user)

    def test_login_non_existent_user(self):
        # Arrange
        self.user_repository.find_by_email.return_value = None

        # Act & Assert
        with self.assertRaises(UserNotExistsError):
            self.login_user.execute("nonexistent@example.com", "password")

    def test_login_invalid_password(self):
        # Arrange
        self.user_repository.find_by_email.return_value = self.test_user
        self.test_user.check_password = Mock(return_value=False)

        # Act & Assert
        with self.assertRaises(UserNotExistsError):
            self.login_user.execute("test@example.com", "wrong_password")


if __name__ == '__main__':
    unittest.main()