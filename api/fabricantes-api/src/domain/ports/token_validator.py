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

    # @abstractmethod
    # def get_user_id(self, token: str) -> str:
    #     """Extract the user ID from the provided token."""
    #     pass
    #
    # @abstractmethod
    # def get_user_role(self, token: str) -> str:
    #     """Extract the user role from the provided token."""
    #     pass