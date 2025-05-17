import requests

from ...domain.exceptions.authentication_error import AuthenticationError
from ...domain.ports.token_validator import TokenValidatorPort


class TokenValidatorAdapter(TokenValidatorPort):
    """
    Adapter for validating JWT tokens using an external authentication service.
    """

    def __init__(self, auth_service_url: str):
        """
        Initializes the adapters with the URL of the authentication service.
        :param auth_service_url: URL of the authentication service.
        """
        self.auth_service_url = auth_service_url

    def validate_token(self, token: str) -> dict:
        """
        Validates a JWT token using the external authentication service.
        :param token: JWT token to validate.
        :return: User information dictionary if valid.
        :raises AuthenticationError: If token is invalid.
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            # Make a request to the authentication service to validate the token
            response = requests.get(f"{self.auth_service_url}/me", headers=headers)

            if response.status_code != 200:
                raise AuthenticationError(f"Token validation failed: {response.status_code}")

            return response.json()
        except requests.RequestException as e:
            raise AuthenticationError(f"Error connecting to users API: {str(e)}")