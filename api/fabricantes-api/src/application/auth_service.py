# src/application/auth_service.py
from ..domain.ports.token_validator import TokenValidatorPort
from ..domain.exceptions.authentication_error import AuthenticationError


class AuthService:
    """Service for authentication-related operations"""

    def __init__(self, token_validator: TokenValidatorPort):
        self.token_validator = token_validator

    def validate_user_token(self, token: str) -> dict:
        """
        Validates a user token and returns user information
        :param token: JWT token to validate
        :return: User information
        :raises: AuthenticationError if token is invalid
        """
        return self.token_validator.validate_token(token)