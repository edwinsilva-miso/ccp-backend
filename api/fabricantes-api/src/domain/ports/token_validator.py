from abc import ABC, abstractmethod

class TokenValidatorPort(ABC):
    """Port defining the interface for token validation"""

    @abstractmethod
    def validate_token(self, token: str) -> dict:
        """
        Validates a token and returns user information
        :param token: JWT token to validate
        :return: User information dictionary if valid
        :raises: AuthenticationError if token is invalid
        """
        pass
